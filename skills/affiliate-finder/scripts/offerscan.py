#!/usr/bin/env python3
"""PARASITER — which affiliate products the pages in Google's top push most, and through which programs.

  offerscan.py KEYWORDS [--provider dataforseo|serpapi] [--country us] [--language en] [--depth 10]
               [--pages 80] [--out offers-scan.csv] [--dry-run] [--live]
  offerscan.py --seeds "joint pain, sleep" [--year 2026] ...      build the affiliate-intent query set from seeds
  offerscan.py --urls urls.txt ...                                free: analyze pages found by web search
  offerscan.py --from-json serp.json ...                          free: a saved DataForSEO / SerpApi response
  offerscan.py --self-test

How it works:
1. Queries. KEYWORDS is a text file with one query per line (or comma-separated). With --seeds the
   script builds the affiliate-intent set for each seed: "best <seed>", "<seed> reviews",
   "top <seed> <year>", "<seed> that actually works", "<seed> review scam or legit",
   "<seed> reviews consumer reports", "best <seed> reddit". --dry-run prints the queries and the cost.
2. Search (paid, the user's own account, cost printed first): Google top N through DataForSEO or SerpApi.
   Without an account: collect result URLs with web search into a file and pass --urls (free).
3. Pages (free): every ranking page that is not a store, a giant reference site or a video host is
   opened once. From each page the script reads its title and its outbound links and recognises
   affiliate links: ClickBank (vendor), Digistore24 (product id), BuyGoods, MaxWeb, Amazon (ASIN),
   Impact, CJ, ShareASale, Awin, Rakuten, PartnerStack, Partnerize, Everflow-style trackers and
   cloaked /go/ /recommends/ /out/ links (followed once to see where they land).
4. Products: links are grouped by product (vendor / product id / merchant domain). For each one:
   the network, the product name (most common link text or "X Review" titles), how many different
   ranking pages push it, in how many queries, the best position, and up to 3 example pages.
   Products named in many titles without a recognised affiliate link are listed apart ("named only").

Other affiliates' IDs are never printed or saved: only the network and the product.
Output: a table on screen + <out> (CSV). Standard library only.
"""
import argparse
import csv
import html as htmllib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "work-log", "scripts"))
import rankcheck as rc  # noqa: E402

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
TEMPLATES = ("best {s}", "{s} reviews", "top {s} {y}", "{s} that actually works", "{s} review scam or legit",
             "{s} reviews consumer reports", "best {s} reddit")
# pages that never carry affiliate review content worth reading
SKIP_HOSTS = ("youtube.com", "youtu.be", "wikipedia.org", "facebook.com", "instagram.com", "tiktok.com", "x.com",
              "twitter.com", "pinterest.", "google.", "amazon.", "walmart.", "ebay.", "target.com", "bestbuy.",
              "nih.gov", "mayoclinic.org", "webmd.com", "healthline.com", "clevelandclinic.org", "apple.com")
# affiliate link signatures: (network, regex on the full URL, how to get the product key)
NETWORKS = [
    ("ClickBank", re.compile(r"(?:^|//)([a-z0-9]+)\.[a-z0-9]+\.hop\.clickbank\.net", re.I), "group1"),
    ("ClickBank", re.compile(r"hop\.clickbank\.net/?\?[^#]*\bvendor=([a-z0-9]+)", re.I), "group1"),
    ("ClickBank", re.compile(r"(?:^|//)([a-z0-9]+)\.hop\.clickbank\.net", re.I), "group1"),
    ("Digistore24", re.compile(r"digistore24\.com/(?:redir|product|socialproof)/(\d+)", re.I), "group1"),
    ("Digistore24", re.compile(r"checkout-ds24\.com/(?:redir|product)/(\d+)", re.I), "group1"),
    ("BuyGoods", re.compile(r"buygoods\.com/[^\s\"']*?[?&]product=([a-z0-9_-]+)", re.I), "group1"),
    ("BuyGoods", re.compile(r"buygoods\.com", re.I), "dest"),
    ("MaxWeb", re.compile(r"maxweb[a-z]*\.(?:com|net|io)", re.I), "dest"),
    ("Amazon", re.compile(r"amazon\.[a-z.]+/(?:[^?\s]*/)?(?:dp|gp/product)/([A-Z0-9]{10})[^\s]*[?&]tag=", re.I), "group1"),
    ("Amazon", re.compile(r"amzn\.to/", re.I), "dest"),
    ("Impact", re.compile(r"(?:^|//)([a-z0-9-]+)\.(?:sjv\.io|pxf\.io|evyy\.net|ojrq\.net|mvvx\.net|vqgz\.net|7eer\.net)", re.I), "group1"),
    ("CJ", re.compile(r"(?:anrdoezrs\.net|jdoqocy\.com|tkqlhce\.com|dpbolvw\.net|kqzyfj\.com|qksrv\.net)", re.I), "dest"),
    ("ShareASale", re.compile(r"shareasale\.com/r\.cfm[^\s\"']*?[?&]m=(\d+)", re.I), "group1"),
    ("Awin", re.compile(r"awin1\.com/cread\.php[^\s\"']*?awinmid=(\d+)", re.I), "group1"),
    ("Rakuten", re.compile(r"(?:click\.linksynergy\.com|linksynergy)", re.I), "dest"),
    ("PartnerStack", re.compile(r"(?:^|//)(?:get\.|try\.)?([a-z0-9-]+)\.partnerlinks\.io", re.I), "group1"),
    ("Partnerize", re.compile(r"prf\.hn/click", re.I), "dest"),
    ("Everflow / tracker", re.compile(r"[?&](?:aff_id|affid|affiliate_id|a_aid|aff|hop|hopid|clickid|sub_?id|oid)=", re.I), "host"),
]
CLOAK = re.compile(r"/(?:go|recommends|recommend|out|visit|link|refer|official|buy|get|try)/[a-z0-9_-]{2,}/?$", re.I)
DEST_PARAMS = ("url", "u", "murl", "ued", "urllink", "destination", "dest", "redirect", "r", "p")
TITLE_NAME = re.compile(r"^\s*(?:the\s+)?([A-Z][\w+&'.-]*(?:\s+[A-Z0-9][\w+&'.-]*){0,3})\s+(?:Reviews?|Review:|vs\.?)\b")


def host(u):
    try:
        h = urllib.parse.urlsplit(u).hostname or ""
    except ValueError:
        return ""
    return h[4:] if h.startswith("www.") else h


def site(h):
    parts = h.split(".")
    return ".".join(parts[-3:]) if len(parts) > 2 and len(parts[-1]) == 2 and len(parts[-2]) <= 3 else ".".join(parts[-2:])


def skip_page(u):
    h = host(u)
    return not h or any(s in h for s in SKIP_HOSTS)


# ---------- queries ----------

def build_queries(a):
    if a.seeds:
        seeds = [s.strip() for s in a.seeds.split(",") if s.strip()]
        return [t.format(s=s, y=a.year).lower() for s in seeds for t in TEMPLATES]
    src = a.keywords or ""
    if os.path.exists(src):
        with open(src, encoding="utf-8") as f:
            items = [ln.strip() for ln in f if ln.strip() and not ln.startswith("#")]
    else:
        items = [x.strip() for x in src.split(",") if x.strip()]
    seen, out = set(), []
    for q in items:
        if q.lower() not in seen:
            seen.add(q.lower())
            out.append(q.lower())
    return out


# ---------- search ----------

def read_key(fd):
    if fd is None:
        return None
    try:
        data = os.read(int(fd), 4096).decode().strip()
        os.close(int(fd))
        return data or None
    except OSError:
        return None


def search(a, queries):
    """{query: [(position, url)]}. Paid: cost printed first, nothing runs with --dry-run."""
    if a.provider == "serpapi":
        per = rc.serpapi_searches(a.depth, "google")
        print(f"Offer scan · google {a.country} · top {a.depth} · {len(queries)} queries · SerpApi: "
              f"{len(queries) * per} searches from your monthly quota")
    else:
        price = (0.002 if a.live else 0.0006) * max(1, a.depth / 10)
        print(f"Offer scan · google {a.country} · top {a.depth} · {len(queries)} queries · PAID: about "
              f"${len(queries) * price:.2f} from your DataForSEO balance")
    if a.dry_run:
        for q in queries:
            print("  ·", q)
        return None
    if a.provider == "serpapi":
        key = read_key(a.auth_fd)
        if not key:
            sys.exit(rc.NO_SERPAPI)
        a.engine = "google"
        out = {}
        for q in queries:
            items, _ = rc.serpapi_parse(rc.serpapi_query(q, key, a))
            out[q] = items[: a.depth]
        return out
    loc = rc.COUNTRIES.get(a.country.lower()) or sys.exit("Unknown --country: " + ", ".join(sorted(rc.COUNTRIES)))
    login, password = rc.read_auth(a.auth_fd)
    if not (login and password):
        sys.exit(rc.NO_CREDS)
    body = [{"keyword": q, "location_code": loc, "language_code": a.language, "depth": a.depth, "device": "desktop", "tag": q}
            for q in queries]
    out = {}
    if a.live:
        for item in body:
            for t in rc.call("POST", "/live/advanced", login, password, [item]).get("tasks") or []:
                out[(t.get("data") or {}).get("keyword", "").lower()] = rc.serp_items(t)
        return out
    ids = {}
    for i in range(0, len(body), 100):
        for t in rc.call("POST", "/task_post", login, password, body[i:i + 100]).get("tasks") or []:
            if t.get("id"):
                ids[t["id"]] = (t.get("data") or {}).get("keyword", "").lower()
    print(f"- {len(ids)} tasks queued, waiting for results (usually 1–5 minutes)…")
    deadline = time.time() + a.wait * 60
    while ids and time.time() < deadline:
        time.sleep(20)
        for t in rc.call("GET", "/tasks_ready", login, password).get("tasks") or []:
            for r in t.get("result") or []:
                if r.get("id") in ids:
                    for tt in rc.call("GET", f"/task_get/advanced/{r['id']}", login, password).get("tasks") or []:
                        out[ids[r["id"]]] = rc.serp_items(tt)
                    ids.pop(r["id"])
    if ids:
        print(f"- {len(ids)} tasks not ready yet (paid, kept 3 days by DataForSEO).")
    return out


def from_json(path):
    data = json.load(open(path, encoding="utf-8"))
    out = {}
    if isinstance(data, dict) and data.get("tasks"):                      # DataForSEO
        for t in data["tasks"]:
            out[((t.get("data") or {}).get("keyword") or "").lower()] = rc.serp_items(t)
    else:                                                                   # SerpApi: one response or a list
        for d in data if isinstance(data, list) else [data]:
            q = ((d.get("search_parameters") or {}).get("q") or "").lower()
            items, _ = rc.serpapi_parse([d])
            out.setdefault(q, []).extend(items)
    return out


def from_urls(path):
    with open(path, encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip().startswith("http")]
    return {"(web search)": [(None, u) for u in lines]}


# ---------- pages ----------

def fetch(url, limit=900_000, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.8"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.geturl(), r.read(limit).decode("utf-8", "replace")
    except Exception:
        return url, ""


def resolve(url, timeout=12):
    """Where a cloaked link lands (one request, follows redirects)."""
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.geturl()
    except urllib.error.HTTPError as e:
        return e.geturl() or url
    except Exception:
        return url


LINK = re.compile(r"<a\b[^>]*?href=[\"']([^\"'#>]+)[\"'][^>]*>(.*?)</a>", re.I | re.S)
TAG = re.compile(r"<[^>]+>")


def dest_of(u):
    qs = urllib.parse.parse_qs(urllib.parse.urlsplit(u).query)
    for k in DEST_PARAMS:
        for v in qs.get(k, []):
            v = urllib.parse.unquote(v)
            if v.startswith("http"):
                return v
    return ""


def classify(u):
    """(network, product key) for an affiliate link, or None. Never returns the affiliate's own ID."""
    for net, rx, how in NETWORKS:
        m = rx.search(u)
        if not m:
            continue
        if how == "group1":
            return net, m.group(1).lower()
        if how == "dest":
            d = dest_of(u)
            return net, site(host(d)) if d else "?"
        return net, site(host(u))
    return None


def page_links(page_url, body):
    """[(network, product key, anchor text)] for the affiliate links on one page."""
    own = site(host(page_url))
    out, cloaked = [], []
    for href, inner in LINK.findall(body):
        href = htmllib.unescape(href.strip())
        u = urllib.parse.urljoin(page_url, href)
        if not u.startswith("http"):
            continue
        text = re.sub(r"\s+", " ", htmllib.unescape(TAG.sub(" ", inner))).strip()[:80]
        c = classify(u)
        if c:
            out.append((c[0], c[1], text))
        elif site(host(u)) == own and CLOAK.search(urllib.parse.urlsplit(u).path):
            cloaked.append((u, text))
    for u, text in list(dict.fromkeys(cloaked))[:6]:                      # cloaked links: one request each
        land = resolve(u)
        c = classify(land)
        if c:
            out.append((c[0], c[1], text))
        elif site(host(land)) != own and not skip_page(land):
            out.append(("direct / own tracker", site(host(land)), text))
    return out


def title_of(body):
    m = re.search(r"<title[^>]*>(.*?)</title>", body, re.I | re.S)
    return re.sub(r"\s+", " ", htmllib.unescape(m.group(1))).strip()[:160] if m else ""


def analyze(serp, max_pages, workers=8):
    pages = {}                                                              # url -> {queries, best}
    for q, items in serp.items():
        for pos, u in items:
            if skip_page(u):
                continue
            p = pages.setdefault(u, {"queries": set(), "best": None})
            p["queries"].add(q)
            if pos and (p["best"] is None or pos < p["best"]):
                p["best"] = pos
    order = sorted(pages, key=lambda u: (-len(pages[u]["queries"]), pages[u]["best"] or 99))[:max_pages]
    print(f"- {len(pages)} ranking pages · reading {len(order)} of them (free)…")

    def one(u):
        final, body = fetch(u)
        return u, title_of(body), page_links(final, body) if body else []
    with ThreadPoolExecutor(workers) as ex:
        read = list(ex.map(one, order))
    products = {}
    named = Counter()
    for u, title, links in read:
        m = TITLE_NAME.match(title or "")
        if m:
            named[m.group(1).strip()] += 1
        for net, key, text in links:
            if key in ("?", ""):
                continue
            p = products.setdefault((net, key), {"network": net, "key": key, "pages": {}, "queries": set(), "best": None, "names": Counter()})
            p["pages"][u] = title
            p["queries"] |= pages[u]["queries"]
            b = pages[u]["best"]
            if b and (p["best"] is None or b < p["best"]):
                p["best"] = b
            if text and len(text) > 2 and not re.match(r"(?i)^(click|here|buy|order|check|visit|get|see|shop|learn)\b", text):
                p["names"][text] += 1
    return products, named, len(order), sum(1 for _, _, l in read if l)


# ---------- output ----------

def name_of(p):
    if p["names"]:
        return p["names"].most_common(1)[0][0]
    for t in p["pages"].values():
        m = TITLE_NAME.match(t or "")
        if m:
            return m.group(1)
    return p["key"]


def report(products, named, read, with_links, out):
    rows = sorted(products.values(), key=lambda p: (-len(p["pages"]), -len(p["queries"]), p["best"] or 99))
    print(f"\nProducts the top pages push · {date.today().isoformat()} · {read} pages read, {with_links} with affiliate links")
    print("| # | Product | Network | Product key | Pages | Queries | Best pos. | Example page |")
    print("|---|---|---|---|---|---|---|---|")
    for i, p in enumerate(rows[:40], 1):
        ex = next(iter(p["pages"]))
        print(f"| {i} | {name_of(p)} | {p['network']} | {p['key']} | {len(p['pages'])} | {len(p['queries'])} | {p['best'] or '—'} | {ex} |")
    linked = {name_of(p).lower() for p in rows}
    only = [(n, c) for n, c in named.most_common(30) if c >= 2 and n.lower() not in linked]
    if only:
        print("\nNamed in several titles, no affiliate link recognised (check the program by hand): "
              + ", ".join(f"{n} ({c})" for n, c in only[:15]))
    with open(out, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["product", "network", "product_key", "pages", "queries", "best_position", "example_pages", "checked"])
        for p in rows:
            wr.writerow([name_of(p), p["network"], p["key"], len(p["pages"]), len(p["queries"]), p["best"] or "",
                         " ".join(list(p["pages"])[:3]), date.today().isoformat()])
    print(f"\nSaved {out} ({len(rows)} products). Other affiliates' IDs are not shown or saved.")


def self_test():
    html = """<title>Zenvita Review 2026: Does It Work?</title>
    <a href="https://hop.clickbank.net/?affiliate=someone&vendor=zenvita">Zenvita official site</a>
    <a href="https://www.digistore24.com/redir/412345/someone/">Sleepora</a>
    <a href="https://nordvpn.sjv.io/c/123/456/789">NordVPN deal</a>
    <a href="https://www.shareasale.com/r.cfm?b=1&u=999&m=47&urllink=">Brand</a>
    <a href="https://www.amazon.com/dp/B0ABCDEF12?tag=someone-20">on Amazon</a>
    <a href="/about">About</a>"""
    links = page_links("https://blog.example.com/zenvita-review", html)
    got = {(n, k) for n, k, _ in links}
    want = {("ClickBank", "zenvita"), ("Digistore24", "412345"), ("Impact", "nordvpn"), ("ShareASale", "47"), ("Amazon", "b0abcdef12")}
    assert want <= got, got
    assert not any("someone" in k for _, k, _ in links), "affiliate IDs must never be kept"
    assert TITLE_NAME.match("Zenvita Review 2026: Does It Work?").group(1) == "Zenvita"
    assert skip_page("https://www.youtube.com/watch?v=1") and not skip_page("https://medium.com/@a/x")
    a = argparse.Namespace(seeds="joint pain", year=2026, keywords=None)
    assert "best joint pain reddit" in build_queries(a)
    print("self-test ok")


def main():
    ap = argparse.ArgumentParser(description="Which affiliate products the top pages push, and through which programs")
    ap.add_argument("keywords", nargs="?", help="file with one query per line, or comma-separated queries")
    ap.add_argument("--seeds", help="comma-separated niche seeds: the script builds the affiliate-intent queries")
    ap.add_argument("--year", type=int, default=date.today().year)
    ap.add_argument("--provider", default="dataforseo", choices=["dataforseo", "serpapi"])
    ap.add_argument("--country", default="us"); ap.add_argument("--language", default="en")
    ap.add_argument("--depth", type=int, default=10, help="top 10 by default")
    ap.add_argument("--pages", type=int, default=80, help="max ranking pages to open (free)")
    ap.add_argument("--limit", type=int, default=150, help="max queries per run")
    ap.add_argument("--out", default="offers-scan.csv")
    ap.add_argument("--live", action="store_true"); ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--wait", type=int, default=15)
    ap.add_argument("--urls", help="free: a file of result URLs collected with web search")
    ap.add_argument("--from-json", help="free: a saved DataForSEO or SerpApi response")
    ap.add_argument("--auth-fd", help=argparse.SUPPRESS)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if a.urls:
        serp = from_urls(a.urls)
    elif a.from_json:
        serp = from_json(a.from_json)
    else:
        queries = build_queries(a)[: a.limit]
        if not queries:
            ap.error("give KEYWORDS, --seeds, --urls or --from-json")
        serp = search(a, queries)
        if serp is None:
            return
    products, named, read, with_links = analyze(serp, a.pages)
    report(products, named, read, with_links, a.out)


if __name__ == "__main__":
    main()
