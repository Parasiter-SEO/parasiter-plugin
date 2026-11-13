#!/usr/bin/env python3
"""PARASITER — find the platforms where affiliate review pages are published and indexed right now.

  platformscan.py PRODUCTS [--provider dataforseo|serpapi] [--suffix review] [--country us] [--depth 10] [--device desktop]
                  [--base parasite-seo-progress.csv] [--out platforms-scan.csv] [--dry-run] [--live]
                  [--exclusions exclusions.json] [--exclude domain[/path],...] [--collect-only]
  platformscan.py --from-raw platforms-scan.raw.json [--allowed allowed.json] [--exclusions ...]
  platformscan.py --self-test

PRODUCTS: a text file with one affiliate product name per line (or a CSV with a product column),
or comma-separated names. For each product the script searches Google for "<product> review"
through the user's own DataForSEO account (paid: the cost is printed first, --dry-run prints only
the cost) or SerpApi account (--provider serpapi: searches from the monthly quota — the free plan
gives 250 a month; 1 search per query per 10 results) and collects every page in the results that is NOT the product's own site or a store.
Pages are grouped by platform: how many different products have review pages there, the platform
type and whether it is free (user posts) or paid (news / PR / sponsored).

After the paid search everything else is free:
- Exclusions: stop types and the blacklist (references/exclusions.md, merged with the server list
  passed by --exclusions = the saved answer of `exclusions_get`) and the known-dead platforms from
  the server are dropped before any check and only counted.
- Live check: up to 3 example pages per platform are opened (404/410, "page removed" text,
  redirect to the home or login page, empty page, noindex meta / X-Robots-Tag = removed).
  A platform passes only if at least one example is alive. Platforms whose examples are all
  removed are listed apart and their domains saved to platforms-scan-dead.txt (kept locally).
- Sign-up link: found on the home page or common paths (/register, /signup, /join…) and opened
  to check it works; otherwise "sign-up link not found" + the home page.
- Rows are post-first: Post · Product · Pos. · Platform · Type · Free/Paid · Sign-up.

With a PARASITER key, run in two steps so the author's private posts are never shown:
  1) --collect-only  → platforms-scan.raw.json + platforms-scan.examples.txt (URLs to filter)
  2) privfilter.py private-hashes.json <examples file> --out allowed.json (local, nothing is sent)
  3) --from-raw platforms-scan.raw.json --allowed allowed.json  (free: checks + output)

The point is not to find unknown platforms, but the ones where affiliate review pages are
already published AND indexed — proven places to post. Links on them don't matter; that the
page itself is in Google does.

Pattern search, method B (footprints): put one ready Google query per line in PRODUCTS
(e.g. inurl:/discuss "mitolyn") and pass --suffix "" — the lines are searched as they are.

Credentials: from the plugin settings via the dataforseo_run / serpapi_run tool (inherited pipe, --auth-fd). Never written anywhere.
Standard library only.
"""
import argparse
import csv
import fnmatch
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "work-log", "scripts"))
import rankcheck as rc  # noqa: E402
import worklog as w  # noqa: E402

STORES = ("amazon.", "walmart.", "ebay.", "target.com", "iherb.", "gnc.com", "vitaminshoppe.", "costco.",
          "aliexpress.", "temu.", "etsy.com", "bestbuy.", "trustpilot.", "bbb.org", "sitejabber.",
          "google.com", "apple.com", "play.google")
# news / PR / media: posting there is paid (sponsored post, press release, "partner content")
PAID_HINTS = ("news", "times", "post", "journal", "herald", "tribune", "gazette", "observer", "daily",
              "magazine", "mag.", "press", "wire", "media", "chronicle", "insider", "today", "weekly",
              "outlookindia", "hindustan", "deccan", "midday", "mid-day", "benzinga", "yahoo", "marketwatch",
              "globenewswire", "prnewswire", "accessnewswire", "einpresswire", "newswire", "openpr", "ibtimes",
              "sfgate", "seattlepi", "timesunion", "chron.com", "bostonglobe", "miamiherald", "kansascity",
              "tribuneindia", "thehindu", "ndtv", "livemint", "business-standard", "financialexpress",
              "outlook", "cnbc", "forbes", "entrepreneur", "observer.com")
FREE_TYPES = {"article", "community", "q&a", "blog", "site-builder", "page", "document", "social", "video",
              "fundraising", "event", "creator", "portfolio", "newsletter", "forum"}
# hidden upload forms and other people's file folders: abuse, never a platform to use
ABUSE = re.compile(r"(wp-content/uploads?|wpcf7|dndcf7|/uploads?/.*\.pdf$|formidable|gravity_forms|/sites/default/files/.*\.pdf$)", re.I)


def read_products(arg):
    if os.path.exists(arg):
        with open(arg, encoding="utf-8-sig") as f:
            text = f.read()
        if arg.lower().endswith(".csv"):
            rows = list(csv.DictReader(text.splitlines()))
            if rows:
                col = next((c for c in rows[0] if w.norm(c) in ("product", "productname", "name", "offer")), None)
                if col:
                    return [r[col].strip() for r in rows if r.get(col, "").strip()]
        names = [ln.split("#")[0].strip(" -•\t") for ln in text.splitlines()]
    else:
        names = [x.strip() for x in arg.split(",")]
    seen, out = set(), []
    for n in names:
        if n and not n.startswith("##") and n.lower() not in seen:
            seen.add(n.lower())
            out.append(n)
    return out


def brand_tokens(product):
    toks = [t for t in re.split(r"[^a-z0-9]+", product.lower()) if len(t) >= 3]
    return toks, re.sub(r"[^a-z0-9]", "", product.lower())


def is_brand_site(url, product):
    host = w.url_domain(url)
    toks, joined = brand_tokens(product)
    h = re.sub(r"[^a-z0-9]", "", host)
    return bool(joined and joined in h) or (len(toks) == 1 and toks[0] in h)


EXTRA_TYPES = {"hackmd.io": "page", "zooniverse.org": "community", "corada.com": "community",
               "gamma.app": "page",
               "firstory.me": "podcast", "spotify.com": "podcast",
               "bigcartel.com": "site-builder", "bandcamp.com": "creator", "soundcloud.com": "podcast",
               "kaggle.com": "community", "huggingface.co": "community", "gitlab.io": "site-builder",
               "pastebin.com": "page", "justpaste.it": "page", "rentry.co": "page", "glitch.me": "site-builder",
               "webflow.io": "site-builder", "carrd.co": "site-builder", "jimdosite.com": "site-builder",
               "strikingly.com": "site-builder", "ucoz": "site-builder", "tilda.ws": "site-builder"}
FREE_TYPES |= {"podcast"}


def classify(url):
    slug, dom, typ = w.platform_of(url)
    typ = typ or next((t for d, t in EXTRA_TYPES.items() if dom.endswith(d) or d in dom), "")
    if not typ and urllib.parse.urlsplit(url).path.lower().endswith(".pdf"):
        typ = "document/pdf"  # PDFs are normal findings; the PDF's host is the platform
    low = dom.lower()
    if any(s in low for s in STORES):
        return slug, dom, typ, "store"
    if typ in FREE_TYPES or typ == "forum":
        return slug, dom, typ, "free"
    if any(h in low for h in PAID_HINTS):
        return slug, dom, typ or "news", "paid"
    if low.endswith((".edu", ".gov", ".ac.uk", ".edu.au", ".gov.uk")) or ".edu." in low or ".gov." in low:
        return slug, dom, typ or "institution", "check"
    return slug, dom, typ, "check"


# ---------- exclusions (№4) and known-dead platforms (№6) ----------

LOCAL_EXCLUSIONS = os.path.join(HERE, "..", "references", "exclusions.md")


def load_exclusions(server_json=None, extra=None, local=LOCAL_EXCLUSIONS):
    """{"stop": [(match, reason)], "black": [(match, reason)], "dead": {domain: since}}.
    The local copy (references/exclusions.md) is always loaded; the server answer of
    `exclusions_get` (saved as JSON) and the user's own --exclude entries are merged in."""
    ex = {"stop": [], "black": [], "dead": {}}
    section = None
    if os.path.exists(local):
        with open(local, encoding="utf-8") as f:
            for ln in f:
                low = ln.lower()
                if ln.startswith("## "):
                    section = "stop" if "stop" in low else "black" if "black" in low else None
                m = re.match(r"\|\s*`([^`]+)`\s*\|\s*(.*?)\s*\|\s*$", ln)
                if m and section:
                    ex[section].append((m.group(1).strip().lower(), m.group(2)))
    if server_json and os.path.exists(server_json):
        with open(server_json, encoding="utf-8") as f:
            d = json.load(f)
        for it in d.get("stop_types") or []:
            ex["stop"].append(((it.get("pattern") or "").lower(), it.get("reason", "")))
        for it in d.get("blacklist") or []:
            ex["black"].append(((it.get("match") or "").lower(), it.get("reason", "")))
        for it in d.get("dead") or []:
            if it.get("domain"):
                ex["dead"][it["domain"].lower().lstrip(".")] = it.get("since", "")
    for e in extra or []:
        if e.strip():
            ex["black"].append((e.strip().lower(), "your own exclusion"))
    for k in ("stop", "black"):
        seen, out = set(), []
        for m, r in ex[k]:
            if m and m not in seen:
                seen.add(m)
                out.append((m, r))
        ex[k] = out
    return ex


def host_path(url):
    sp = urllib.parse.urlsplit(url if "://" in url else "http://" + url)
    host = (sp.hostname or "").lower()
    host = re.sub(r"^(www|m)\.", "", host)
    return host, sp.path or "/"


def matches(url, match, typ=""):
    """Host equals or ends with the match's domain; a path in the match must prefix the URL path.
    `*` is a host wildcard; `type:<t>` matches the detected platform type."""
    if match.startswith("type:"):
        return bool(typ) and typ.lower() == match[5:]
    dom, _, path = match.partition("/")
    host, upath = host_path(url)
    if "*" in dom:
        ok = fnmatch.fnmatch(host, dom)
    else:
        ok = host == dom or host.endswith("." + dom)
    if not ok:
        return False
    return not path or upath.lower().startswith("/" + path.rstrip("/"))


def excluded(url, typ, ex):
    """('stop'|'black'|'dead', reason) or None."""
    for kind in ("stop", "black"):
        for m, reason in ex[kind]:
            if matches(url, m, typ):
                return kind, reason
    host, _ = host_path(url)
    for d in ex["dead"]:
        if host == d or host.endswith("." + d):
            return "dead", "known dead since " + (ex["dead"][d] or "?")
    return None


# ---------- free live check of example pages (№6) ----------

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
REMOVED_TEXT = re.compile(
    r"(page (was )?not found|page (you requested |you are looking for )?(could not be found|does ?n[o']t exist|no longer exists)"
    r"|(this|the) (page|post|topic|thread|story|article|content|document|profile|account) (has been|was|is) "
    r"(removed|deleted|suspended|unavailable|no longer available)"
    r"|(post|topic|thread|story|article|content|document) (has been |was )?(removed|deleted)( by| for)"
    r"|no longer available|content (is )?(not available|unavailable)|this account (has been|is) suspended"
    r"|requested (topic|thread|page) (does not exist|could not be found)|nothing (was )?found here"
    r"|sorry,? (that|this) page (doesn|does not|isn|is not))", re.I)
LOGIN_PATH = re.compile(r"(/login|/log-in|/signin|/sign-in|/sign_in|/auth|/account/login|/users/sign_in|/session)", re.I)
NOINDEX_META = re.compile(r"<meta[^>]+name=[\"'](robots|googlebot)[\"'][^>]*content=[\"'][^\"']*noindex", re.I)
NOINDEX_META2 = re.compile(r"<meta[^>]+content=[\"'][^\"']*noindex[^\"']*[\"'][^>]*name=[\"'](robots|googlebot)[\"']", re.I)


def visible_text(html):
    t = re.sub(r"(?is)<(script|style|noscript|svg|template)[^>]*>.*?</\1>", " ", html)
    t = re.sub(r"(?s)<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def judge(orig_url, status, final_url, headers, body):
    """Pure decision: ('live'|'removed'|'unknown', why). No network here, so it is unit-tested."""
    if status in (404, 410):
        return "removed", f"HTTP {status}"
    if status and status >= 400:
        return "unknown", f"HTTP {status} (site blocks the check — open by hand)"
    if "noindex" in (headers.get("x-robots-tag") or "").lower():
        return "removed", "noindex (X-Robots-Tag)"
    o_host, o_path = host_path(orig_url)
    f_host, f_path = host_path(final_url or orig_url)
    if final_url and final_url != orig_url:
        if LOGIN_PATH.search(f_path) and not LOGIN_PATH.search(o_path):
            return "removed", "redirect to the login page"
        if f_path.rstrip("/") == "" and o_path.rstrip("/") != "":
            return "removed", "redirect to the home page"
    ctype = (headers.get("content-type") or "").lower()
    if "pdf" in ctype or o_path.lower().endswith(".pdf"):
        if body[:5] == b"%PDF-" or "pdf" in ctype:
            return ("live", "PDF opens") if len(body) > 1000 else ("removed", "empty PDF")
        # a PDF link that now serves HTML: judge the HTML below
    html = body.decode("utf-8", "replace")
    if NOINDEX_META.search(html) or NOINDEX_META2.search(html):
        return "removed", "noindex (meta robots)"
    text = visible_text(html)
    title = " ".join(re.findall(r"(?is)<title[^>]*>(.*?)</title>", html))[:300]
    heads = " ".join(re.findall(r"(?is)<h1[^>]*>(.*?)</h1>", html))[:300]
    if REMOVED_TEXT.search(title) or REMOVED_TEXT.search(visible_text(heads)) or REMOVED_TEXT.search(text[:1500]):
        return "removed", "'page removed / not found' text"
    if len(text) < 150:
        if len(html) > 20000:
            return "unknown", "page is built by scripts — open by hand"
        return "removed", "empty page"
    return "live", f"HTTP {status or 200}"


def fetch(url, limit=600_000, timeout=20):
    """(status, final_url, headers{lower}, body bytes) or raises."""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.8",
                                               "Accept": "text/html,application/xhtml+xml,application/pdf,*/*;q=0.8"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.geturl(), {k.lower(): v for k, v in r.headers.items()}, r.read(limit)
    except urllib.error.HTTPError as e:
        try:
            body = e.read(limit)
        except Exception:
            body = b""
        return e.code, e.geturl() or url, {k.lower(): v for k, v in (e.headers or {}).items()}, body


def check_page(url):
    try:
        return judge(url, *fetch(url))
    except urllib.error.URLError as e:
        reason = str(getattr(e, "reason", e))
        if "Name or service not known" in reason or "getaddrinfo" in reason or "nodename" in reason:
            return "removed", "domain does not resolve"
        return "unknown", "could not open: " + reason[:60]
    except Exception as e:  # timeouts, TLS, broken servers
        return "unknown", "could not open: " + str(e)[:60]


# ---------- sign-up link (№5) ----------

SIGNUP_PATHS = ("/register", "/signup", "/sign-up", "/join", "/user/register", "/users/sign_up",
                "/create-account", "/account/register", "/accounts/signup", "/registration",
                "/member/register", "/register.php", "/ucp.php?mode=register", "/index.php?register/",
                "/login/register", "/start", "/get-started")
SIGNUP_HREF = re.compile(r"""<a[^>]+href=["']([^"'#]+)["'][^>]*>(.*?)</a>""", re.I | re.S)
SIGNUP_WORD = re.compile(r"(sign ?up|register|registration|create (an |your )?account|join( now| free| us)?$|get started)", re.I)
SIGNUP_URLW = re.compile(r"(register|sign-?up|sign_up|join|create-?account|registration)", re.I)
SIGNUP_PAGE = re.compile(r"(type=[\"']password|sign ?up|register|create (an |your )?account|e-?mail)", re.I)
FORUM_ROOTS = ("forum", "forums", "community", "board", "boards", "discussions", "discuss")


def signup_ok(url, home):
    try:
        status, final, headers, body = fetch(url, limit=300_000, timeout=15)
    except Exception:
        return False
    if status != 200:
        return False
    if host_path(final)[1].rstrip("/") == "" and host_path(url)[1].rstrip("/") != "":
        return False  # bounced to the home page
    return bool(SIGNUP_PAGE.search(body.decode("utf-8", "replace")))


def find_signup(example_url, domain=""):
    """(signup_url or None, home_url). Looks on the home page for a sign-up link, then tries common paths."""
    sp = urllib.parse.urlsplit(example_url)
    domain = (domain or host_path(example_url)[0]).lower()
    home = f"{sp.scheme}://{sp.netloc}/"
    seg = (sp.path.strip("/").split("/") or [""])[0].lower()
    roots = [home.rstrip("/")] + ([home + seg] if seg in FORUM_ROOTS else [])
    cands = []
    for root in reversed(roots):
        try:
            status, final, headers, body = fetch(root + "/", limit=400_000, timeout=15)
        except Exception:
            continue
        if status != 200:
            continue
        for href, label in SIGNUP_HREF.findall(body.decode("utf-8", "replace")):
            lab = visible_text(label)
            if SIGNUP_URLW.search(href) or SIGNUP_WORD.search(lab):
                u = urllib.parse.urljoin(final, href.strip())
                hu = host_path(u)[0]
                if u.startswith("http") and (hu == domain or hu.endswith("." + domain)) and u not in cands:
                    cands.append(u)
    for root in reversed(roots):
        cands += [root + p for p in SIGNUP_PATHS]
    for u in cands[:12]:
        if signup_ok(u, home):
            return u, home
    return None, home


# ---------- scan ----------

def read_key(fd):
    if fd is None:
        return None
    try:
        data = os.read(int(fd), 4096).decode().strip()
        os.close(int(fd))
        return data or None
    except OSError:
        return None


def serpapi_task(responses):
    """One query's SerpApi pages as a DataForSEO-shaped task, so group() reads both the same way."""
    items, feats = rc.serpapi_parse(responses)
    return {"result": [{"items": [{"type": "organic", "url": u, "rank_group": pos} for pos, u in items]
                        + [{"type": kind, "url": u} for kind, u in feats]}]}


def run_search(a, products):
    queries = {f"{p} {a.suffix}".strip().lower(): p for p in products}
    probe = f"\"<product> {a.suffix}\"" if a.suffix.strip() else "queries as written"
    if a.provider == "serpapi":
        per = rc.serpapi_searches(a.depth, "google")
        print(f"Platform scan · google {a.country} · top {a.depth} · {len(queries)} queries ({probe}) · "
              f"SerpApi: {len(queries) * per} searches from your monthly quota")
    else:
        loc = rc.COUNTRIES.get(a.country.lower()) or sys.exit("Unknown --country: " + ", ".join(sorted(rc.COUNTRIES)))
        price = (0.002 if a.live else 0.0006) * max(1, a.depth / 10)
        print(f"Platform scan · google {a.country} · top {a.depth} · {len(queries)} queries "
              f"({probe}) · PAID: about ${len(queries) * price:.2f} from your DataForSEO balance")
    if a.dry_run:
        for q in list(queries)[:20]:
            print("  ·", q)
        return None, queries
    if a.provider == "serpapi":
        key = read_key(a.auth_fd)
        if not key:
            sys.exit(rc.NO_SERPAPI)
        a.engine = "google"
        return {q: serpapi_task(rc.serpapi_query(q, key, a)) for q in queries}, queries
    login, password = rc.read_auth(a.auth_fd)
    if not (login and password):
        sys.exit(rc.NO_CREDS)
    body = [{"keyword": q, "location_code": loc, "language_code": a.language, "depth": a.depth,
             "device": a.device, "tag": q} for q in queries]
    results = {}
    if a.live:
        for item in body:
            d = rc.call("POST", "/live/advanced", login, password, [item])
            for t in d.get("tasks") or []:
                results[(t.get("data") or {}).get("keyword", "").lower()] = t
    else:
        ids = {}
        for i in range(0, len(body), 100):
            d = rc.call("POST", "/task_post", login, password, body[i:i + 100])
            for t in d.get("tasks") or []:
                if t.get("id"):
                    ids[t["id"]] = (t.get("data") or {}).get("keyword", "").lower()
        print(f"- {len(ids)} tasks queued, waiting for results (usually 1–5 minutes)…")
        deadline = time.time() + a.wait * 60
        while ids and time.time() < deadline:
            time.sleep(20)
            ready = rc.call("GET", "/tasks_ready", login, password)
            for t in ready.get("tasks") or []:
                for r in t.get("result") or []:
                    if r.get("id") in ids:
                        g = rc.call("GET", f"/task_get/advanced/{r['id']}", login, password)
                        for tt in g.get("tasks") or []:
                            results[ids[r["id"]]] = tt
                        ids.pop(r["id"])
        if ids:
            print(f"- {len(ids)} tasks not ready yet (paid, kept 3 days by DataForSEO).")
    return results, queries


def group(results, queries, products, ex):
    """Platforms with all their pages (best position first) + skipped counts."""
    plat = defaultdict(lambda: {"products": set(), "pages": [], "best": 999, "in_blocks": set(), "abuse": 0})
    meta, skipped = {}, {"stop": set(), "black": set(), "dead": set()}
    for q, task in results.items():
        product = queries.get(q, q)
        found = [(pos, u, "organic") for pos, u in rc.serp_items(task)]
        found += [(None, u, kind) for kind, u in rc.serp_features(task)]
        for pos, url, kind in found:
            if not url.startswith("http") or any(is_brand_site(url, pr) for pr in products):
                continue
            slug, dom, typ, cost = classify(url)
            if cost == "store":
                continue
            hit = excluded(url, typ, ex)
            if hit:
                skipped[hit[0]].add(dom)
                continue
            p = plat[slug]
            meta[slug] = (dom, typ, cost)
            if ABUSE.search(url):
                p["abuse"] += 1
                continue
            p["products"].add(product)
            if url not in [x["url"] for x in p["pages"]]:
                p["pages"].append({"url": url, "product": product, "position": pos})
            if pos:
                p["best"] = min(p["best"], pos)
            if kind != "organic":
                p["in_blocks"].add(kind)
    out = []
    for slug, p in plat.items():
        dom, typ, cost = meta[slug]
        if not p["products"] and p["abuse"]:
            cost = "abuse"
        pages = sorted(p["pages"], key=lambda x: x["position"] or 999)
        out.append({"platform": slug, "domain": dom, "type": typ or "?", "cost": cost,
                    "products": sorted(p["products"]), "best_position": p["best"] if p["best"] < 999 else "",
                    "serp_blocks": sorted(p["in_blocks"]), "pages": pages})
    return out, {k: sorted(v) for k, v in skipped.items()}


def verify(platforms, signup=True, workers=8):
    """Live-check up to 3 examples per platform; find a sign-up link for the live free / to-check ones."""
    jobs = [(i, j, pg["url"]) for i, p in enumerate(platforms) if p["cost"] != "abuse"
            for j, pg in enumerate(p["pages"][:3])]
    with ThreadPoolExecutor(workers) as pool:
        for (i, j, _), res in zip(jobs, pool.map(lambda t: check_page(t[2]), jobs)):
            platforms[i]["pages"][j]["status"], platforms[i]["pages"][j]["why"] = res
    for p in platforms:
        st = [pg.get("status") for pg in p["pages"][:3]]
        p["live"] = "abuse" if p["cost"] == "abuse" else "live" if "live" in st else \
            "removed" if st and all(s == "removed" for s in st) else "unverified"
    todo = [p for p in platforms if signup and p["live"] == "live" and p["cost"] in ("free", "check")]
    with ThreadPoolExecutor(workers) as pool:
        for p, (su, home) in zip(todo, pool.map(lambda p: find_signup(next(pg["url"] for pg in p["pages"] if pg.get("status") == "live"), p["domain"]), todo)):
            p["signup"], p["home"] = su, home
    return platforms


def load_allowed(path):
    if not path:
        return None
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    return set(d.get("allowed") or []) if isinstance(d, dict) else set(d)


def signup_cell(p):
    if p["cost"] == "paid":
        return "paid placement — buy via the site's advertising / PR contact"
    if p.get("signup"):
        return p["signup"]
    return f"sign-up link not found · {p.get('home') or 'https://' + p['domain'] + '/'}"


def report(platforms, skipped, out, allowed, yours, today):
    shown_hidden = 0
    rows = []
    for p in platforms:
        live_pages = [pg for pg in p["pages"][:3] if pg.get("status") == "live"]
        if allowed is not None:
            before = len(live_pages)
            live_pages = [pg for pg in live_pages if pg["url"] in allowed]
            shown_hidden += before - len(live_pages)
        p["shown"] = live_pages
        rows.append({"post": live_pages[0]["url"] if live_pages else "",
                     "product": live_pages[0]["product"] if live_pages else "",
                     "position": (live_pages[0]["position"] or "") if live_pages else "",
                     "platform": p["domain"], "type": p["type"], "cost": p["cost"],
                     "signup": signup_cell(p) if p["live"] == "live" else "",
                     "status": p["live"], "products": len(p["products"]), "best_position": p["best_position"],
                     "serp_blocks": " ".join(p["serp_blocks"]), "yours": "yes" if p["platform"] in yours else "",
                     "more_posts": " ".join(pg["url"] for pg in live_pages[1:]),
                     "checks": " ".join(f"{pg['url']} → {pg.get('status', '-')}: {pg.get('why', '')}" for pg in p["pages"][:3]),
                     "product_names": "; ".join(p["products"])[:300], "checked": today})
    order = {"live": 0, "unverified": 1, "removed": 2, "abuse": 3}
    rows.sort(key=lambda r: (order[r["status"]], -r["products"], r["position"] or r["best_position"] or 999))
    with open(out, "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["post"])
        wr.writeheader()
        wr.writerows(rows)

    live = [r for r in rows if r["status"] == "live"]
    dead = [r for r in rows if r["status"] == "removed"]
    unver = [r for r in rows if r["status"] == "unverified"]
    n_found = len([r for r in rows if r["status"] != "abuse"])
    n_skip = len(skipped["stop"]) + len(skipped["black"])
    print(f"Found {n_found} platforms · live {len(live)} · removed {len(dead)} · "
          f"skipped by stop / black list {n_skip}"
          + (f" · skipped as known dead {len(skipped['dead'])}" if skipped["dead"] else "")
          + (f" · could not verify {len(unver)}" if unver else "") + f" · checked {today} · saved to {out}\n")
    by_slug = {p["domain"]: p for p in platforms}
    for title, keep in (("Free (user posts)", "free"), ("Paid (news / PR / sponsored)", "paid"), ("To check", "check")):
        part = [r for r in live if r["cost"] == keep]
        if not part:
            continue
        print(f"## {title} — {len(part)}")
        print("| # | Post | Product | Pos. | Platform | Type | Free/Paid | Sign-up |")
        print("|---|---|---|---|---|---|---|---|")
        for i, r in enumerate(part[:40], 1):
            fp = "Paid" if keep == "paid" else "Free" if keep == "free" else "Free?"
            post = r["post"] or f"example: find your own with \"{(by_slug[r['platform']]['products'] or ['product'])[0]} review\""
            print(f"| {i} | {post} | {r['product']} | {r['position']} | {r['platform']}{' (yours)' if r['yours'] else ''} "
                  f"| {r['type']} | {fp} | {r['signup']} |")
            for pg in by_slug[r["platform"]]["shown"][1:3]:
                print(f"|  | ↳ {pg['url']} | {pg['product']} | {pg['position'] or ''} |  |  |  |  |")
        print()
    if dead:
        print("In Google, but the pages are removed (not in the working list): "
              + ", ".join(f"{r['platform']}" for r in dead[:30]))
    if unver:
        print("Could not verify (the site blocks automatic checks — open an example by hand): "
              + ", ".join(r["platform"] for r in unver[:30]))
    if n_skip:
        print("Skipped by stop / black list: " + ", ".join(skipped["stop"] + skipped["black"])[:600])
    bad = [r for r in rows if r["status"] == "abuse"]
    if bad:
        print(f"Skipped {len(bad)} domains where reviews sit in other organisations' upload folders or forms "
              "(hacked or abused sites — not platforms): " + ", ".join(r["platform"] for r in bad[:10]))
    if allowed is not None and shown_hidden:
        print(f"{shown_hidden} example posts hidden by the PARASITER filter.")
    dead_path = os.path.splitext(out)[0] + "-dead.txt"
    with open(dead_path, "w", encoding="utf-8") as f:
        hosts = sorted({host_path(by_slug[r["platform"]]["pages"][0]["url"])[0] for r in dead if by_slug[r["platform"]]["pages"]})
        f.write("\n".join(hosts) + ("\n" if hosts else ""))
    if dead:
        print(f"Dead domains saved to {dead_path} — skip them in your next scans (--exclude) so you don't pay to scan them again.")


def self_test():
    ex = load_exclusions()
    assert ex["stop"] and ex["black"], "local exclusions.md not parsed"
    cases = [("https://www.youtube.com/watch?v=1", "video", "stop"), ("https://youtu.be/x", "", "stop"),
             ("https://bucket.s3.amazonaws.com/a.pdf", "", "stop"), ("https://b.s3.us-east-1.amazonaws.com/x.pdf", "", "stop"),
             ("https://www.quora.com/q", "q&a", "stop"), ("https://foo.blogspot.com/2026/x.html", "", "black"),
             ("https://www.fitness.com/forum/threads/1", "forum", "black"), ("https://www.fitness.com/articles/1", "", None),
             ("https://community.synology.com/enu/forum/1", "", "black"), ("https://medium.com/@a/b", "article", None),
             ("https://example.org/files/guide.pdf", "document/pdf", None)]
    for url, typ, want in cases:
        got = (excluded(url, typ, ex) or (None,))[0]
        assert got == want, (url, got, want)
    ex["dead"]["deadforum.example"] = "2026-10-01"
    assert excluded("https://www.deadforum.example/t/1", "forum", ex)[0] == "dead"
    page = b"<html><head><title>Product X review</title></head><body>" + b"<p>Real review text. </p>" * 20 + b"</body></html>"
    u = "https://forum.example.com/threads/x-review.1/"
    assert judge(u, 200, u, {}, page)[0] == "live"
    assert judge(u, 404, u, {}, b"")[0] == "removed"
    assert judge(u, 410, u, {}, b"")[0] == "removed"
    assert judge(u, 200, "https://forum.example.com/", {}, page)[0] == "removed"
    assert judge(u, 200, "https://forum.example.com/login?next=1", {}, page)[0] == "removed"
    assert judge(u, 200, u, {"x-robots-tag": "noindex"}, page)[0] == "removed"
    assert judge(u, 200, u, {}, page.replace(b"<head>", b"<head><meta name=\"robots\" content=\"noindex,follow\">"))[0] == "removed"
    assert judge(u, 200, u, {}, b"<html><title>Oops! That page can\xe2\x80\x99t be found</title><h1>Page not found</h1></html>")[0] == "removed"
    assert judge(u, 200, u, {}, b"<html><body></body></html>")[0] == "removed"
    assert judge(u, 403, u, {}, b"")[0] == "unknown"
    assert judge("https://x.example/a.pdf", 200, "https://x.example/a.pdf", {"content-type": "application/pdf"}, b"%PDF-" + b"0" * 2000)[0] == "live"
    assert classify("https://docs.example.net/files/x.pdf")[2] == "document/pdf"
    assert ABUSE.search("https://uni.edu/wp-content/uploads/2026/x.pdf")
    t = serpapi_task([{"organic_results": [{"position": 1, "link": "https://forum.example.com/t/x-review/1"}],
                       "discussions_and_forums": [{"link": "https://www.reddit.com/r/x/comments/1"}]}])
    assert rc.serp_items(t) == [(1, "https://forum.example.com/t/x-review/1")]
    assert ("discussions_and_forums", "https://www.reddit.com/r/x/comments/1") in rc.serp_features(t)
    print("self-test ok")


def main():
    ap = argparse.ArgumentParser(description="Platforms where affiliate review pages rank now (DataForSEO or SerpApi) + free live check")
    ap.add_argument("products", nargs="?")
    ap.add_argument("--provider", default="dataforseo", choices=["dataforseo", "serpapi"])
    ap.add_argument("--suffix", default="review", help='added to each product: "review" (default), "reviews", "complaints"…')
    ap.add_argument("--country", default="us"); ap.add_argument("--language", default="en")
    ap.add_argument("--depth", type=int, default=10, help="top 10 by default: that is where the traffic is"); ap.add_argument("--device", default="desktop", choices=["desktop", "mobile"])
    ap.add_argument("--base", help="the user's journal: platforms already in their base are marked 'yours'")
    ap.add_argument("--out", default="platforms-scan.csv")
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument("--live", action="store_true"); ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--wait", type=int, default=15)
    ap.add_argument("--exclusions", help="saved JSON answer of the server's exclusions_get (stop types, blacklist, dead)")
    ap.add_argument("--exclude", default="", help="the user's own exclusions: domain[/path],…")
    ap.add_argument("--collect-only", action="store_true", help="search + group only; write <out>.raw.json and the example URLs for the local private filter")
    ap.add_argument("--from-raw", help="continue from a --collect-only file (free: live check, sign-up links, output)")
    ap.add_argument("--allowed", help='JSON {"allowed": [...]} from privfilter.py: only these example posts are shown')
    ap.add_argument("--no-live-check", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--no-signup", action="store_true", help="skip the sign-up link search")
    ap.add_argument("--auth-fd", help=argparse.SUPPRESS)
    ap.add_argument("--self-test", action="store_true", help="offline test of exclusions and the live-check rules")
    a = ap.parse_args()
    if a.self_test:
        return self_test()

    ex = load_exclusions(a.exclusions, a.exclude.split(","))
    base_out = os.path.splitext(a.out)[0]
    if a.from_raw:
        with open(a.from_raw, encoding="utf-8") as f:
            raw = json.load(f)
        platforms, skipped = raw["platforms"], raw["skipped"]
        # the server list may be newer than the collect step: apply it again
        keep = []
        for p in platforms:
            hit = excluded("https://" + p["domain"] + "/", p["type"], ex) or \
                next((excluded(pg["url"], p["type"], ex) for pg in p["pages"] if excluded(pg["url"], p["type"], ex)), None)
            if hit:
                skipped.setdefault(hit[0], []).append(p["domain"])
            else:
                keep.append(p)
        platforms = keep
    else:
        if not a.products:
            ap.error("PRODUCTS is required (or --from-raw / --self-test)")
        products = read_products(a.products)[: a.limit]
        if not products:
            sys.exit("No product names found.")
        results, queries = run_search(a, products)
        if results is None:
            return
        platforms, skipped = group(results, queries, products, ex)
        print(f"- {len(results)} result pages read · {len(platforms)} platforms before checks")
        if a.collect_only:
            with open(base_out + ".raw.json", "w", encoding="utf-8") as f:
                json.dump({"platforms": platforms, "skipped": skipped, "date": date.today().isoformat()}, f)
            urls = [pg["url"] for p in platforms if p["cost"] != "abuse" for pg in p["pages"][:3]]
            with open(base_out + ".examples.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(urls) + "\n")
            print(f"- saved {base_out}.raw.json and {len(urls)} example URLs in {base_out}.examples.txt "
                  f"→ run privfilter.py on them, then: --from-raw {base_out}.raw.json --allowed allowed.json")
            return

    yours = set()
    if a.base and os.path.exists(a.base):
        yours = {k for k in w.read_platforms(w.platforms_path(a.base))}
        yours |= {p["platform"].lower() for p in w.page_states(w.read_rows(a.base), date.today()).values() if p.get("platform")}
    if a.no_live_check:
        for p in platforms:
            p["live"] = "unverified"
    else:
        print(f"- free live check of up to 3 example pages on {len([p for p in platforms if p['cost'] != 'abuse'])} platforms…")
        verify(platforms, signup=not a.no_signup)
    report(platforms, skipped, a.out, load_allowed(a.allowed), yours, date.today().isoformat())


if __name__ == "__main__":
    main()
