#!/usr/bin/env python3
"""PARASITER — find the platforms where affiliate review pages are published and indexed right now.

  platformscan.py PRODUCTS [--suffix review] [--country us] [--depth 10] [--device desktop]
                  [--base parasite-seo-progress.csv] [--out platforms-scan.csv] [--dry-run] [--live]

PRODUCTS: a text file with one affiliate product name per line (or a CSV with a product column),
or comma-separated names. For each product the script searches Google for "<product> review"
through the user's own DataForSEO account (paid: the cost is printed first, --dry-run prints only
the cost) and collects every page in the results that is NOT the product's own site or a store.
Pages are grouped by platform: how many different products have review pages there, examples,
the platform type and whether it is free (user posts) or paid (news / PR / sponsored).

The point is not to find unknown platforms, but the ones where affiliate review pages are
already published AND indexed — proven places to post. Links on them don't matter; that the
page itself is in Google does.

Credentials: env DATAFORSEO_LOGIN / DATAFORSEO_PASSWORD. Never written anywhere.
"""
import argparse
import csv
import os
import re
import sys
import time
from collections import defaultdict

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
               "pressbooks.pub": "document", "researchgate.net": "document", "gamma.app": "page",
               "audioboom.com": "podcast", "firstory.me": "podcast", "spotify.com": "podcast",
               "bigcartel.com": "site-builder", "bandcamp.com": "creator", "soundcloud.com": "podcast",
               "kaggle.com": "community", "huggingface.co": "community", "gitlab.io": "site-builder",
               "pastebin.com": "page", "justpaste.it": "page", "rentry.co": "page", "glitch.me": "site-builder",
               "webflow.io": "site-builder", "carrd.co": "site-builder", "jimdosite.com": "site-builder",
               "strikingly.com": "site-builder", "ucoz": "site-builder", "tilda.ws": "site-builder"}
FREE_TYPES |= {"podcast"}


def classify(url):
    slug, dom, typ = w.platform_of(url)
    typ = typ or next((t for d, t in EXTRA_TYPES.items() if dom.endswith(d) or d in dom), "")
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


def main():
    ap = argparse.ArgumentParser(description="Platforms where affiliate review pages rank now (DataForSEO)")
    ap.add_argument("products")
    ap.add_argument("--suffix", default="review", help='added to each product: "review" (default), "reviews", "complaints"…')
    ap.add_argument("--country", default="us"); ap.add_argument("--language", default="en")
    ap.add_argument("--depth", type=int, default=10, help="top 10 by default: that is where the traffic is"); ap.add_argument("--device", default="desktop", choices=["desktop", "mobile"])
    ap.add_argument("--base", help="the user's journal: platforms already in their base are marked 'yours'")
    ap.add_argument("--out", default="platforms-scan.csv")
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument("--live", action="store_true"); ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--wait", type=int, default=15)
    a = ap.parse_args()

    products = read_products(a.products)[: a.limit]
    if not products:
        sys.exit("No product names found.")
    loc = rc.COUNTRIES.get(a.country.lower()) or sys.exit("Unknown --country: " + ", ".join(sorted(rc.COUNTRIES)))
    price = (0.002 if a.live else 0.0006) * max(1, a.depth / 10)
    queries = {f"{p} {a.suffix}".strip().lower(): p for p in products}
    print(f"Platform scan · google {a.country} · top {a.depth} · {len(queries)} queries "
          f"(\"<product> {a.suffix}\") · PAID: about ${len(queries) * price:.2f} from your DataForSEO balance")
    if a.dry_run:
        for q in list(queries)[:20]:
            print("  ·", q)
        return
    login, password = os.environ.get("DATAFORSEO_LOGIN"), os.environ.get("DATAFORSEO_PASSWORD")
    if not (login and password):
        sys.exit("No DataForSEO credentials: set DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD.")

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

    yours = set()
    if a.base and os.path.exists(a.base):
        yours = {k for k in w.read_platforms(w.platforms_path(a.base))}
        yours |= {p["platform"].lower() for p in w.page_states(w.read_rows(a.base), __import__("datetime").date.today()).values() if p.get("platform")}

    plat = defaultdict(lambda: {"products": set(), "pages": [], "best": 999, "in_blocks": set(), "abuse": 0})
    meta = {}
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
            p = plat[slug]
            if ABUSE.search(url):
                p["abuse"] += 1
                meta[slug] = (dom, typ, cost)
                continue
            p["products"].add(product)
            if len(p["pages"]) < 3 and url not in p["pages"]:
                p["pages"].append(url)
            if pos:
                p["best"] = min(p["best"], pos)
            if kind != "organic":
                p["in_blocks"].add(kind)
            meta[slug] = (dom, typ, cost)

    rows = []
    for slug, p in plat.items():
        dom, typ, cost = meta[slug]
        if not p["products"] and p["abuse"]:
            cost = "abuse"
        rows.append({"platform": slug, "domain": dom, "type": typ or "?", "cost": cost,
                     "products": len(p["products"]), "best_position": p["best"] if p["best"] < 999 else "",
                     "serp_blocks": " ".join(sorted(p["in_blocks"])), "yours": "yes" if slug in yours else "",
                     "examples": " ".join(p["pages"]), "product_names": "; ".join(sorted(p["products"]))[:300]})
    rows.sort(key=lambda r: (r["cost"] == "abuse", -r["products"], r["best_position"] or 999))
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["platform"])
        wr.writeheader()
        wr.writerows(rows)

    print(f"- {len(results)} result pages read · {len(rows)} platforms with review pages · saved to {a.out}\n")
    for title, keep in (("Free (user posts)", "free"), ("Paid (news / PR / sponsored)", "paid"), ("To check", "check")):
        part = [r for r in rows if r["cost"] == keep]
        if not part:
            continue
        print(f"## {title} — {len(part)}")
        print("| Platform | Type | Products with reviews | Best pos. | SERP blocks | Yours | Example |")
        print("|---|---|---|---|---|---|---|")
        for r in part[:40]:
            print(f"| {r['domain']} | {r['type']} | {r['products']} | {r['best_position']} | {r['serp_blocks']} | {r['yours']} | {r['examples'].split(' ')[0] if r['examples'] else ''} |")
        print()
    bad = [r for r in rows if r["cost"] == "abuse"]
    if bad:
        print(f"Skipped {len(bad)} domains where reviews sit in other organisations' upload folders or forms "
              "(hacked or abused sites — not platforms): " + ", ".join(r["domain"] for r in bad[:10]))


if __name__ == "__main__":
    main()
