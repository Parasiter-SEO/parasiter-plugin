#!/usr/bin/env python3
"""PARASITER — work, traffic and sales journal.

Files (in the user's project folder):
  parasite-seo-progress.csv  work journal: pages, checks, audits, traffic, imports
  parasite-seo-sales.csv     one row per sale / conversion (manual or imported)

Commands:
  add            JOURNAL --event E [--url --platform --offer --program --sub-id --query --type
                 --status --score --views --clicks --aff-clicks --sales --revenue --minutes
                 --note --date --time]
  sale           JOURNAL --program P --commission N [--amount --currency --sub-id --url --offer
                 --order-id --status --network --date --note]
  import-sales   JOURNAL EXPORT.csv --program P [--network N] [--currency C]
                 [--map field=Header ...] [--date-format FMT]
  import-traffic JOURNAL EXPORT.csv [--platform P] [--from D --to D] [--map field=Header ...]
  summary        JOURNAL [--period ...] [--today D]
  effect         JOURNAL [--period ...] [--by page|platform|offer|program|content_type|month]
  due            JOURNAL [--today D]
  pages          JOURNAL [--platform P] [--today D]
  import-pages   JOURNAL FILE [--date D] [--platform P] [--offer O] [--program P] [--campaign C]
                 [--type T] [--map field=Header ...]   (CSV/TSV/TXT or any text with URLs)
  platforms      JOURNAL [--today D]                  personal platform base with stats
  platform-set   JOURNAL --platform P [--domain --type --language --links --account --score
                 --state active|testing|paused|dropped|dead --priority high|normal|low --note]
  tag            JOURNAL (--url U ... | --urls-file F | --platform P | --match TEXT)
                 [--topic --priority --position --offer --program --campaign --query --type]
  import-ranks   JOURNAL EXPORT.csv [--date D] [--map field=Header]   positions from any rank tracker
  ideas          JOURNAL --to P1,P2 [--from P|own-site] [--top-only] [--n 8]   topics for the user's own plan
  rollout        JOURNAL (--topic T | --url U)            where to publish this topic next
  import-links   JOURNAL FILE [--program P] [--commission 40%]   affiliate links library (parasite-seo-links.csv)
  links          JOURNAL [--program P]                 products, links, pages per product, products with no pages
  site-roi       JOURNAL [--period P] [--by platform|page] visits, conversions, revenue on the site vs spend
  backlinks      JOURNAL [--period P] [--target URL]   links our pages give to the own / client site: dofollow, live, anchors, cost
  coverage       JOURNAL [--topic T] [--platform P] [--gaps N]   topics x platforms, what to write where

Periods: today, yesterday, week, last-week, month, last-month, YYYY-MM, YYYY-MM-DD,
YYYY-MM-DD..YYYY-MM-DD, all.  --sales-file FILE overrides the sales file path.
Positions: scripts/rankcheck.py (DataForSEO). Formats: references/log-format.md, references/sales-import.md. Standard library only.
"""
import argparse
import csv
import io
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta

COLUMNS = ["date", "time", "event", "page_url", "platform", "offer", "program", "campaign", "sub_id",
           "main_query", "content_type", "status", "score", "views", "clicks", "aff_clicks",
           "sales", "revenue", "minutes", "note", "topic", "priority", "position",
           "link_target", "link_rel", "anchor", "cost"]
SALE_COLUMNS = ["date", "program", "network", "offer", "sub_id", "page_url", "order_id",
                "amount", "commission", "currency", "status", "source", "note", "referer"]
EVENTS = ["baseline", "published", "submitted", "check", "audit", "refreshed", "moved",
          "platform", "traffic", "stats", "import", "task", "note", "tag", "source"]
PRIORITIES = ["high", "normal", "low"]
TOP = 10
ALIVE = {"live", "indexed", "not-indexed", "dropped"}
INDEXED = {"indexed", "dropped"}
GONE = {"removed", "dead", "noindex"}
CHECK_POINTS = [2, 7, 14]
CHECK_EVERY = 14
RECHECK_NOT_INDEXED = 3
AUDIT_POINTS = [14, 30, 60]
AUDIT_MIN = 70
SALES_EVERY = 7
RECONCILE_EVERY = 30
LABELS = {"published": "published", "submitted": "sent to indexing", "check": "checks",
          "audit": "audits", "refreshed": "refreshed", "moved": "moved",
          "platform": "platforms tested", "traffic": "traffic entries",
          "stats": "stats entries", "import": "imports", "task": "other tasks",
          "note": "notes", "baseline": "baseline", "tag": "tags", "source": "sources saved"}

# column aliases for exports (compared after normalising: lowercase, letters/digits only)
SALE_ALIASES = {
    "date": ["date", "transactiondate", "saledate", "orderdate", "conversiondate", "eventdate",
             "actiondate", "createdat", "created", "datetime", "time", "clickdate",
             "transactiontime", "dateofsale", "lockingdate"],
    "order_id": ["orderid", "order", "transactionid", "receipt", "receiptno", "actionid", "ordernumber",
                 "conversionid", "commissionid", "saleid", "id", "orderno", "transaction",
                 "orderref", "reference"],
    "commission": ["commission", "yourcommission", "publishercommission", "payout",
                   "earnings", "amountearned", "actionearnings", "affiliatecommission",
                   "commissionamount", "netcommission", "partnercommission", "reward",
                   "yourearnings", "affiliateearnings", "commissionusd"],
    "amount": ["saleamount", "orderamount", "ordervalue", "amount", "revenue", "salevalue",
               "itemprice", "price", "orderamountusd", "totalamount", "grossamount", "total"],
    "sub_id": ["subid", "subid1", "sid", "tid", "trackingid", "sharedid", "affsub", "affsub1",
               "clickref", "customid", "afftrack", "campaignkey", "subtracking", "trackingcode",
               "tag", "s1", "label", "subaffiliateid", "trackingtag",
               # GA4 / UTM: agencies set utm_content = the page's sub-ID
               "utmcontent", "sessionmanualadcontent", "manualadcontent", "firstusermanualadcontent"],
    "status": ["status", "actionstatus", "state", "commissionstatus", "transactionstatus",
               "paymentstatus", "approvalstatus", "type", "transactiontype"],
    "offer": ["product", "productname", "offer", "offername", "item", "itemname", "brand",
              "advertiser", "advertisername", "merchant", "merchantname", "campaign",
              "campaignname", "productid"],
    "currency": ["currency", "currencycode", "commissioncurrency", "currencyid", "payoutcurrency"],
    "referer": ["referer", "referrer", "httpreferer", "refererdomain", "referringdomain", "referringurl", "sourceurl"],
}
TRAFFIC_ALIASES = {
    "url": ["url", "link", "page", "pageurl", "posturl", "landingpage", "address", "permalink",
            "story", "storyurl", "articleurl", "landingpagequerystring", "pagepath",
            "pagepathandscreenclass", "fullpageurl"],
    "sub_id": SALE_ALIASES["sub_id"],
    # where the visit or click came from: referrer domain / URL, GA4 source, utm_source
    "source": ["referrer", "referer", "referringdomain", "referringsite", "referringurl",
               "referrerurl", "referrerdomain", "pagereferrer", "sessionsource",
               "sessionsourcemedium", "sourcemedium", "firstusersource", "firstusersourcemedium",
               "source", "utmsource", "trafficsource", "refdomain"],
    "views": ["views", "pageviews", "reads", "visits", "sessions", "impressions", "uniqueviews",
              "viewcount", "totalviews", "hits", "visitors", "plays", "users", "activeusers",
              "totalusers", "listens", "downloads"],
    # site owners / agencies: conversions and revenue on the site from GA4 or the shop (by source or utm_content)
    "conversions": ["conversions", "keyevents", "transactions", "purchases", "ecommercepurchases", "orders",
                    "leads", "goalcompletions", "signups"],
    "site_revenue": ["purchaserevenue", "totalrevenue", "ecommercerevenue", "itemrevenue", "orderrevenue",
                     "salesrevenue"],
    "aff_clicks": ["clicks", "affclicks", "hops", "outboundclicks", "linkclicks", "rawclicks",
                   "uniqueclicks", "totalclicks", "clickthroughs"],
}
STATUS_MAP = {
    "approved": ["approved", "paid", "locked", "completed", "complete", "confirmed", "sale",
                 "settled", "cleared", "accepted", "valid", "success", "closed", "bill",
                 "purchase", "payable", "shipped"],
    "pending": ["pending", "open", "new", "unpaid", "waiting", "processing", "extended",
                "inprogress", "unconfirmed", "hold", "onhold"],
    "reversed": ["reversed", "refunded", "refund", "rfnd", "declined", "rejected", "chargeback",
                 "cgbk", "void", "voided", "cancelled", "canceled", "returned", "invalid",
                 "deleted", "reversal"],
}


PLATFORM_COLUMNS = ["platform", "domain", "type", "language", "links", "account", "score",
                    "state", "priority", "rank", "added", "source", "note"]
PAGE_ALIASES = {
    "url": TRAFFIC_ALIASES["url"] + ["urls", "pages", "postlink", "publishedurl"],
    "date": ["date", "published", "publishdate", "publishedat", "publicationdate", "datepublished",
             "created", "createdat", "posted", "postdate", "added"],
    "platform": ["platform", "site", "domain", "website"],
    "offer": ["offer", "product", "brand", "productname"],
    "program": ["program", "affiliateprogram", "affnetwork", "affiliatenetwork", "network", "partner"],
    "campaign": ["campaign", "pack", "batch", "group", "project"],
    "sub_id": SALE_ALIASES["sub_id"],
    "main_query": ["query", "keyword", "mainquery", "mainkeyword", "kw", "targetkeyword"],
    "content_type": ["type", "contenttype", "format", "articletype"],
    "status": ["status", "state", "indexed"],
    "note": ["note", "notes", "comment", "comments", "title", "headline"],
    "topic": ["topic", "theme", "cluster", "subject"],
    "priority": ["priority", "prio", "important", "main"],
    "position": ["position", "pos", "rank", "ranking", "avgposition", "averageposition", "serp"],
}
# known platforms: domain suffix -> (slug, type)
KNOWN_PLATFORMS = {
    "medium.com": ("medium", "article"), "linkedin.com": ("linkedin", "article"),
    "substack.com": ("substack", "newsletter"), "reddit.com": ("reddit", "community"),
    "quora.com": ("quora", "q&a"), "tumblr.com": ("tumblr", "blog"),
    "blogspot.com": ("blogger", "site-builder"), "wordpress.com": ("wordpress-com", "site-builder"),
    "wixsite.com": ("wix", "site-builder"), "weebly.com": ("weebly", "site-builder"),
    "sites.google.com": ("google-sites", "site-builder"), "notion.site": ("notion", "page"),
    "telegra.ph": ("telegraph", "page"), "github.io": ("github-pages", "site-builder"),
    "hashnode.dev": ("hashnode", "article"), "dev.to": ("dev-to", "article"),
    "vocal.media": ("vocal", "article"), "hubpages.com": ("hubpages", "article"),
    "issuu.com": ("issuu", "document"), "scribd.com": ("scribd", "document"),
    "slideshare.net": ("slideshare", "document"), "academia.edu": ("academia", "document"),
    "facebook.com": ("facebook", "social"), "x.com": ("x", "social"), "twitter.com": ("x", "social"),
    "pinterest.com": ("pinterest", "social"), "youtube.com": ("youtube", "video"),
    "raisely.com": ("raisely", "fundraising"), "gofundme.com": ("gofundme", "fundraising"),
    "eventbrite.com": ("eventbrite", "event"), "patreon.com": ("patreon", "creator"),
    "behance.net": ("behance", "portfolio"), "dribbble.com": ("dribbble", "portfolio"),
    "producthunt.com": ("producthunt", "community"), "steemit.com": ("steemit", "blog"),
}
FORUM_HINTS = ("/threads/", "/thread/", "/topic/", "/t/", "/forum", "/forums/", "showthread",
               "viewtopic", "/community/", "/discussion")
MULTI_TLD = ("co.uk", "com.au", "co.in", "com.br", "co.za", "com.mx", "co.nz", "com.ua", "org.uk",
             "com.tr", "co.jp", "com.ar", "com.sg", "com.ph", "ac.uk", "gov.uk", "edu.au")


def url_domain(url):
    u = re.sub(r"^[a-z]+://", "", (url or "").strip().lower())
    host = u.split("/")[0].split("?")[0].split(":")[0]
    return re.sub(r"^(www|m)\.", "", host)


def platform_of(url):
    """(slug, domain, type guess) for a page URL."""
    host = url_domain(url)
    for suf, (slug, typ) in KNOWN_PLATFORMS.items():
        if host == suf or host.endswith("." + suf):
            return slug, suf, typ
    parts = host.split(".")
    n = 3 if any(host.endswith("." + t) for t in MULTI_TLD) else 2
    base = ".".join(parts[-n:]) if len(parts) >= n else host
    slug = parts[-n] if len(parts) >= n else parts[0]
    low = url.lower()
    typ = "forum" if any(h in low for h in FORUM_HINTS) or host.startswith(("forum.", "forums.", "community.")) else ""
    return slug, base, typ


# ---------- helpers ----------

def norm(h):
    return re.sub(r"[^a-z0-9]", "", (h or "").lower())


def num(v):
    if v is None:
        return None
    s = str(v).strip()
    if not s:
        return None
    neg = s.startswith("(") and s.endswith(")") or "-" in s[:3]
    s = re.sub(r"[^0-9.,]", "", s)
    if not s:
        return None
    if "," in s and "." in s:
        s = s.replace(",", "") if s.rfind(".") > s.rfind(",") else s.replace(".", "").replace(",", ".")
    elif "," in s:
        head, _, tail = s.rpartition(",")
        s = head.replace(",", "") + "." + tail if len(tail) in (1, 2) else s.replace(",", "")
    try:
        x = float(s)
    except ValueError:
        return None
    return -x if neg else x


def pdate(v):
    try:
        return datetime.strptime(str(v).strip()[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


TRACKING = re.compile(r"^(utm_|_sg|_tp|fbclid|gclid|ref$|ref_|source$|sk$|si$|mc_|_hs|igsh|share)")


def norm_url(u):
    """Compare-key for a page URL: no scheme/www/fragment, tracking parameters dropped, but
    meaningful query parameters kept (profile.php?member_id=…&blog_id=… is a different page)."""
    u = (u or "").strip().lower()
    u = re.sub(r"^https?://", "", u)
    u = re.sub(r"^www\.", "", u)
    u = u.split("#")[0]
    u = re.sub(r"^open\.firstory\.me/", "open.firstory.fm/", u)  # same Firstory story on two domains
    path, _, q = u.partition("?")
    keep = sorted(x for x in q.split("&") if x and not TRACKING.match(x.split("=")[0]))
    path = path.rstrip("/")
    # Gamma: gamma.app/docs/<Title-Slug>-<id> and gamma.app/docs/<id> are the same document
    m = re.match(r"(gamma\.app/(?:docs|public)/)(?:.*-)?([a-z0-9]{15})$", path)
    if m:
        path = "gamma.app/docs/" + m.group(2)
    return path + ("?" + "&".join(keep) if keep else "")


def platforms_path(journal):
    return os.path.join(os.path.dirname(os.path.abspath(journal)), "parasite-seo-platforms.csv")


def sales_path(journal, override=None):
    if override:
        return override
    return os.path.join(os.path.dirname(os.path.abspath(journal)), "parasite-seo-sales.csv")


def fmt(v):
    if v is None:
        return "—"
    return f"{v:,.0f}" if float(v).is_integer() else f"{v:,.2f}"


def money(v, cur="USD"):
    if v is None:
        return "—"
    sym = {"USD": "$", "EUR": "€", "GBP": "£", "": "$"}.get(cur, cur + " ")
    return f"-{sym}{abs(v):,.2f}" if v < 0 else f"{sym}{v:,.2f}"


def pct(v):
    return "—" if v is None else f"{v * 100:.1f}%"


def short(url, n=60):
    u = re.sub(r"^https?://", "", url or "")
    return u if len(u) <= n else u[: n - 1] + "…"


# ---------- reading / writing ----------

def read_csv(path):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return []
    with open(path, newline="", encoding="utf-8-sig") as f:
        return [{(k or "").strip(): (v or "").strip() for k, v in r.items() if k}
                for r in csv.DictReader(f)]


def read_rows(path):
    rows = []
    for i, r in enumerate(read_csv(path)):
        r["_d"] = pdate(r.get("date", ""))
        r["_i"] = i
        r["event"] = r.get("event", "").lower()
        r["status"] = r.get("status", "").lower()
        if r["event"] == "stats" and not r.get("aff_clicks") and r.get("clicks"):
            r["aff_clicks"] = r["clicks"]  # old format: stats clicks were network clicks
        if r["_d"]:
            rows.append(r)
    rows.sort(key=lambda r: (r["_d"], r.get("time", ""), r["_i"]))
    return rows


def ensure_header(path, cols):
    """Create the file or upgrade an older header without changing any values."""
    if os.path.exists(path) and os.path.getsize(path) > 0:
        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            header = [h.strip() for h in (reader.fieldnames or []) if h]
            old = list(reader)
        missing = [c for c in cols if c not in header]
        if missing:
            new_cols = cols + [h for h in header if h not in cols]
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=new_cols, extrasaction="ignore")
                w.writeheader()
                for r in old:
                    w.writerow({(k or "").strip(): v for k, v in r.items() if k})
            print(f"{os.path.basename(path)}: header upgraded ({len(old)} rows kept).")
        with open(path, newline="", encoding="utf-8") as f:
            return next(csv.reader(f))
    with open(path, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(cols)
    return cols


def append(path, cols_default, rows):
    cols = ensure_header(path, cols_default)
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        for r in rows:
            w.writerow(r)


def journal_row(**kw):
    now = datetime.now()
    r = {c: "" for c in COLUMNS}
    r["date"], r["time"] = now.strftime("%Y-%m-%d"), now.strftime("%H:%M")
    r.update({k: ("" if v is None else str(v)) for k, v in kw.items()})
    return r


# ---------- pages ----------

def page_states(rows, today):
    pages = {}
    for r in rows:
        url = r.get("page_url", "")
        if not url or r["_d"] > today:
            continue
        p = pages.setdefault(url, {"url": url, "platform": "", "offer": "", "program": "", "campaign": "",
                                   "sub_id": "", "query": "", "content_type": "",
                                   "published": None, "last_check": None, "status": "",
                                   "ever_indexed": False, "last_audit": None, "score": None,
                                   "last_refresh": None, "moved": None, "first": r["_d"],
                                   "imported": False, "topic": "", "priority": "normal",
                                   "position": None, "pos_date": None, "best_pos": None,
                                   "prev_pos": None, "date_unknown": False,
                                   "link_target": "", "link_rel": "", "anchor": "", "cost": 0.0})
        for k in ("link_target", "link_rel", "anchor"):
            if r.get(k):
                p[k] = r[k].strip().lower() if k == "link_rel" else r[k].strip()
        if num(r.get("cost")):
            p["cost"] += num(r.get("cost"))
        for k, col in (("platform", "platform"), ("offer", "offer"), ("program", "program"),
                       ("campaign", "campaign"),
                       ("sub_id", "sub_id"), ("query", "main_query"),
                       ("content_type", "content_type")):
            if not p[k] and r.get(col):
                p[k] = r[col]
        if r.get("topic"):
            p["topic"] = r["topic"]
        if (r.get("priority") or "").lower() in PRIORITIES:
            p["priority"] = r["priority"].lower()
        ev, st = r["event"], r["status"]
        pos = num(r.get("position"))
        if pos is not None and ev in ("check", "traffic", "note", "tag", "published"):
            p["prev_pos"] = p["position"]
            p["position"], p["pos_date"] = pos, r["_d"]
            p["best_pos"] = pos if p["best_pos"] is None else min(p["best_pos"], pos)
        elif ev == "check" and "· not in top" in (r.get("note") or ""):
            p["prev_pos"], p["position"], p["pos_date"] = p["position"], None, r["_d"]
        if ev == "tag":
            for k, col in (("offer", "offer"), ("program", "program"), ("campaign", "campaign"),
                           ("sub_id", "sub_id"), ("query", "main_query"), ("content_type", "content_type")):
                if r.get(col):
                    p[k] = r[col]
        if ev == "published" and p["published"] is None:
            p["published"] = r["_d"]
            p["imported"] = (r.get("note") or "").startswith("imported from")
            p["date_unknown"] = "publish date unknown" in (r.get("note") or "")
            if st:
                p["status"] = st
        elif ev == "check" and st:
            p["last_check"], p["status"] = r["_d"], st
            if st in INDEXED:
                p["ever_indexed"] = True
        elif ev == "audit" and num(r.get("score")) is not None:
            p["last_audit"], p["score"] = r["_d"], num(r.get("score"))
        elif ev == "refreshed":
            p["last_refresh"] = r["_d"]
        elif ev == "moved":
            p["moved"] = r["_d"]
    for p in pages.values():
        if p["published"] is None:
            p["published"] = p["first"]
        p["age"] = (today - p["published"]).days
        p["topic_key"] = topic_key(p)
    return pages


STOP = {"the", "a", "an", "and", "or", "of", "for", "to", "in", "on", "my", "your", "is", "are", "do",
        "does", "it", "with", "vs", "best", "top", "review", "reviews", "honest", "2024", "2025", "2026",
        "2027", "what", "how", "why", "which", "who", "really", "work", "works", "guide", "p", "pulse",
        "post", "posts", "threads", "thread", "topic", "t", "answer", "view", "home", "html", "htm",
        "php", "blog", "article", "s", "i", "you", "we", "this", "that", "should", "can", "about"}


def slug_words(url):
    path = re.sub(r"^[a-z]+://[^/]+", "", (url or "").lower()).split("?")[0]
    segs = [x for x in path.split("/") if x and not x.startswith("@")]
    seg = max(segs, key=lambda x: len(re.findall(r"[a-z]{3,}", x)), default="")
    words = [w for w in re.split(r"[^a-z0-9]+", seg) if w and w not in STOP and not re.fullmatch(r"[0-9a-f]{6,}|\d+", w)]
    return words[:6]


def topic_key(p):
    """Topic of a page: set topic > main query > offer + content type > words from the URL."""
    t = p.get("topic") or p.get("query")
    if t:
        return re.sub(r"\s+", " ", t.strip().lower())
    if p.get("offer"):
        return (p["offer"] + (" · " + p["content_type"] if p.get("content_type") else "")).lower()
    w = slug_words(p["url"])
    return ("~ " + " ".join(w)) if w else "~ untitled"


def lookups(pages):
    by_sub, by_url = {}, {}
    for p in pages.values():
        if p["sub_id"]:
            by_sub[p["sub_id"].lower()] = p["url"]
        by_url[norm_url(p["url"])] = p["url"]
    return by_sub, by_url


def health(p):
    if p["moved"]:
        return "moved"
    if not p["last_check"]:
        return "not checked yet"
    return p["status"]


# ---------- sales ----------

def sale_status(raw, commission):
    s = norm(raw)
    for k, words in STATUS_MAP.items():
        if s in words or any(s.startswith(w) for w in words if len(w) > 3):
            return k
    if commission is not None and commission < 0:
        return "reversed"
    return "approved" if not s else "pending"


def sale_key(r):
    prog = (r.get("program") or r.get("network") or "").lower()
    if r.get("order_id"):
        return ("o", prog, r["order_id"].lower(), r.get("commission", ""))
    return ("x", prog, r.get("date", ""), (r.get("sub_id") or "").lower(),
            r.get("commission", ""), r.get("amount", ""), r.get("source", ""), r.get("_i"))


def read_sales(path, pages):
    """Latest row per sale wins (status updates); manual sales confirmed by an import are dropped."""
    by_sub, by_url = lookups(pages)
    latest = {}
    for i, r in enumerate(read_csv(path)):
        r["_i"] = i
        r["_d"] = pdate(r.get("date", ""))
        if not r["_d"]:
            continue
        r["_c"] = num(r.get("commission")) or 0.0
        r["_a"] = num(r.get("amount"))
        r["status"] = (r.get("status") or "approved").lower()
        url = r.get("page_url", "")
        if not url and r.get("sub_id"):
            url = by_sub.get(r["sub_id"].lower(), "")
        r["_page"] = by_url.get(norm_url(url), url) if url else ""
        r["_ref"] = (r.get("referer") or "").lower()
        latest[sale_key(r)] = r
    rows = list(latest.values())
    imported = [r for r in rows if r.get("source", "").startswith("import")]
    keep = []
    for r in rows:
        if r.get("source") == "manual" and not r.get("order_id"):
            twin = next((m for m in imported
                         if (m.get("program") or "").lower() == (r.get("program") or "").lower()
                         and abs((m["_d"] - r["_d"]).days) <= 2
                         and abs(m["_c"] - r["_c"]) < 0.01
                         and not m.get("_matched")), None)
            if twin:
                twin["_matched"] = True
                continue
        keep.append(r)
    keep.sort(key=lambda r: (r["_d"], r["_i"]))
    return keep


def counted(r):
    """A sale counts unless it was reversed; negative refund rows count as negative."""
    return r["status"] != "reversed" or r["_c"] < 0


# ---------- periods ----------

def month_bounds(y, m):
    start = date(y, m, 1)
    end = date(y + (m == 12), m % 12 + 1, 1) - timedelta(days=1)
    return start, end


def period_range(period, today, rows, sales=None):
    p = (period or "today").lower()
    if p == "today":
        return today, today, "today"
    if p == "yesterday":
        d = today - timedelta(days=1)
        return d, d, "yesterday"
    if p == "week":
        return today - timedelta(days=today.weekday()), today, "this week"
    if p == "last-week":
        s = today - timedelta(days=today.weekday() + 7)
        return s, s + timedelta(days=6), "last week"
    if p == "month":
        return today.replace(day=1), today, "this month"
    if p == "last-month":
        prev = today.replace(day=1) - timedelta(days=1)
        s, e = month_bounds(prev.year, prev.month)
        return s, e, "last month"
    if p == "all":
        start = min([r["_d"] for r in rows[:1]] + [r["_d"] for r in (sales or [])] + [today])
        return start, today, "all time"
    if ".." in p:
        a, b = p.split("..", 1)
        if pdate(a) and pdate(b):
            return pdate(a), pdate(b), "range"
    if len(p) == 7 and pdate(p + "-01"):
        d = pdate(p + "-01")
        s, e = month_bounds(d.year, d.month)
        return s, e, d.strftime("%B %Y")
    if pdate(p):
        return pdate(p), pdate(p), "day"
    sys.exit(f"Unknown period: {period}")


def previous_range(period, start, end):
    p = (period or "").lower()
    if p in ("month", "last-month") or (len(p) == 7 and pdate(p + "-01")):
        prev = start - timedelta(days=1)
        return month_bounds(prev.year, prev.month)
    length = 7 if p == "week" else (end - start).days + 1
    return start - timedelta(days=length), start - timedelta(days=1)


# ---------- effectiveness ----------

PAGE_DIMS = {"page", "platform", "offer", "content_type", "campaign"}


def estimate_shares(rows, sales, pages, s, e):
    """Spread sales that have no page over the pages of the same program.

    Each unattributed sale is split among pages of its program (or offer) that were
    published by the sale date and not moved before it, weighted by affiliate clicks in
    the period, else views, else equally. Returns ({url: {cur: amount}}, {url: sales},
    unallocated {cur: amount}, methods Counter). Always an estimate.
    """
    traffic = defaultdict(lambda: [0.0, 0.0])
    has = defaultdict(lambda: [False, False])  # page has any clicks / views data
    for r in rows:
        if s <= r["_d"] <= e and r["event"] in ("traffic", "stats") and r.get("page_url"):
            u = r["page_url"]
            if r.get("aff_clicks", "") != "":
                traffic[u][0] += num(r.get("aff_clicks")) or 0
                has[u][0] = True
            if r.get("views", "") != "":
                traffic[u][1] += num(r.get("views")) or 0
                has[u][1] = True
    est, est_n, unalloc, methods = defaultdict(lambda: defaultdict(float)), defaultdict(float), \
        defaultdict(float), Counter()
    for r in sales:
        if not (s <= r["_d"] <= e) or r["_page"] or not counted(r):
            continue
        cur = (r.get("currency") or "USD").upper()
        prog = (r.get("program") or "").lower()
        off = (r.get("offer") or "").lower()
        cands = [p for p in pages.values()
                 if (p["published"] <= r["_d"] or p["date_unknown"]) and not (p["moved"] and p["moved"] < r["_d"])
                 and ((prog and (p["program"] or "").lower() == prog)
                      or (not prog and off and (p["offer"] or "").lower() == off))]
        if r.get("_ref"):  # the network told us which site the buyer came from
            ref = r["_ref"]
            on_ref = [p for p in pages.values() if url_domain(p["url"]).endswith(ref) or ref.endswith(url_domain(p["url"]))]
            on_ref = [p for p in on_ref if p["published"] <= r["_d"] or p["date_unknown"]]
            narrowed = [p for p in cands if p in on_ref] or on_ref
            if narrowed:
                cands = narrowed
                methods["referer (platform known)"] += 1
        if not cands:
            unalloc[cur] += r["_c"]
            methods["no matching pages"] += 1
            continue
        w, m = None, "equal split"
        for idx, label in ((0, "affiliate clicks"), (1, "views")):
            known = [traffic[p["url"]][idx] for p in cands if has[p["url"]][idx]]
            if known and sum(known):
                avg = sum(known) / len(known)  # pages with no data get the average, not zero
                w = [traffic[p["url"]][idx] if has[p["url"]][idx] else avg for p in cands]
                m = label
                break
        if w is None:
            w = [1.0] * len(cands)
        tot = sum(w)
        methods[m] += 1
        for p, wi in zip(cands, w):
            est[p["url"]][cur] += r["_c"] * wi / tot
            est_n[p["url"]] += (1 if r["_c"] > 0 else -1) * wi / tot
    return est, est_n, unalloc, methods


def effect_table(rows, sales, pages, s, e, by):
    """Group pages, traffic and sales in [s, e] by a dimension."""
    groups = defaultdict(lambda: {"pages": set(), "views": 0.0, "aff_clicks": 0.0,
                                  "sales": 0, "commission": defaultdict(float),
                                  "pending": defaultdict(float), "reversed": 0,
                                  "stats_sales": 0.0, "stats_rev": 0.0,
                                  "est": defaultdict(float), "est_n": 0.0})

    def key_for(page_url, fallback=None, d=None):
        if by == "month":
            return d.strftime("%Y-%m") if d else "—"
        if by == "page":
            return page_url or "(sales without a page)"
        p = pages.get(page_url)
        if p and p.get(by):
            return p[by]
        if fallback and fallback.get(by):
            return fallback[by]
        return "(sales without a page)" if not page_url else "(not set)"

    for p in pages.values():
        if p["published"] <= e and not (p["moved"] and p["moved"] < s):
            if by != "month":
                groups[key_for(p["url"])]["pages"].add(p["url"])
    for p in pages.values():
        if by == "month" and s <= p["published"] <= e:
            groups[p["published"].strftime("%Y-%m")]["pages"].add(p["url"])

    pages_with_sales = {r["_page"] for r in sales if r["_page"]}
    for r in rows:
        if not (s <= r["_d"] <= e) or r["event"] not in ("traffic", "stats"):
            continue
        g = groups[key_for(r.get("page_url", ""), r, r["_d"])]
        g["views"] += num(r.get("views")) or 0
        g["aff_clicks"] += num(r.get("aff_clicks")) or 0
        if r["event"] == "stats" and r.get("page_url") not in pages_with_sales:
            g["stats_sales"] += num(r.get("sales")) or 0
            g["stats_rev"] += num(r.get("revenue")) or 0
    for r in sales:
        if not (s <= r["_d"] <= e):
            continue
        g = groups[key_for(r["_page"], r, r["_d"])]
        cur = (r.get("currency") or "USD").upper()
        if r["status"] == "reversed" and r["_c"] >= 0:
            g["reversed"] += 1
            continue
        g["commission"][cur] += r["_c"]
        if r["_c"] > 0:
            g["sales"] += 1
        elif r["_c"] < 0:
            g["sales"] -= 1
            g["reversed"] += 1
        if r["status"] == "pending":
            g["pending"][cur] += r["_c"]
    if by in PAGE_DIMS:
        est, est_n, unalloc, _ = estimate_shares(rows, sales, pages, s, e)
        for url, by_cur in est.items():
            g = groups[key_for(url)]
            for cur, v in by_cur.items():
                g["est"][cur] += v
            g["est_n"] += est_n[url]
        nk = key_for("")
        if nk in groups:
            groups[nk]["est"] = defaultdict(float, unalloc)
            groups[nk]["est_mark"] = True
    return groups


def main_currency(groups):
    c = Counter()
    for g in groups.values():
        for cur, v in g["commission"].items():
            c[cur] += abs(v) + 1
    return c.most_common(1)[0][0] if c else "USD"


def print_effect(groups, by, cur, limit=None):
    out = []
    for k, g in groups.items():
        com = g["commission"].get(cur, 0.0) + g["stats_rev"]
        sales_n = g["sales"] + g["stats_sales"]
        out.append((k, g, com, sales_n))
    out.sort(key=lambda x: (-x[2], -x[1]["views"], str(x[0])))
    if by == "month":
        out.sort(key=lambda x: str(x[0]), reverse=True)
    if limit:
        out = out[:limit]
    head = "Page" if by == "page" else by.replace("_", " ").title()
    has_est = any(g["est"] for g in groups.values())
    if has_est:
        print(f"| {head} | Pages | Views | Aff. clicks | Sales (exact) | Commission (exact) | + Estimated share | Total with estimate | Pending | EPC* | Per page* | Per 1k views* |")
        print("|---|---|---|---|---|---|---|---|---|---|---|---|")
        out.sort(key=lambda x: (-(x[2] + (0 if x[1].get("est_mark") else x[1]["est"].get(cur, 0))),
                                -x[1]["views"], str(x[0])))
        if by == "month":
            out.sort(key=lambda x: str(x[0]), reverse=True)
        for k, g, com, n in out:
            unalloc_row = g.get("est_mark")
            add = g["est"].get(cur, 0.0)
            total = com if unalloc_row else com + add
            pages_n = len(g["pages"])
            epc = total / g["aff_clicks"] if g["aff_clicks"] else None
            per_page = total / pages_n if pages_n else None
            rpm = total / g["views"] * 1000 if g["views"] else None
            name = short(k, 45) if by == "page" else k
            rev = f" ({g['reversed']} reversed)" if g["reversed"] else ""
            share = (f"{money(add, cur)} not shared" if unalloc_row and add
                     else "spread over pages ↑" if unalloc_row
                     else (f"+{money(add, cur)} (~{g['est_n']:.1f} sales)" if add else "—"))
            print(f"| {name} | {pages_n or '—'} | {fmt(g['views']) if g['views'] else '—'} | "
                  f"{fmt(g['aff_clicks']) if g['aff_clicks'] else '—'} | {fmt(n)}{rev} | "
                  f"{money(com, cur)} | {share} | {'—' if unalloc_row else money(total, cur)} | "
                  f"{money(g['pending'].get(cur), cur) if g['pending'].get(cur) else '—'} | "
                  f"{money(epc, cur) if epc is not None and not unalloc_row else '—'} | "
                  f"{money(per_page, cur) if per_page is not None else '—'} | "
                  f"{money(rpm, cur) if rpm is not None and not unalloc_row else '—'} |")
        print("\n\\* with the estimated share. The estimate spreads sales that have no page over the "
              "pages of the same program (by affiliate clicks, else views, else equally; pages with no traffic data get the average). "
              "It shows where money probably comes from, not a fact.")
        others = Counter()
        for g in groups.values():
            for c2, v in g["commission"].items():
                if c2 != cur:
                    others[c2] += v
        if others:
            print("\nOther currencies, not in the table: " +
                  " · ".join(money(v, c2) for c2, v in others.items()))
        return
    print(f"| {head} | Pages | Views | Aff. clicks | Sales | Commission | Pending | EPC | Conv. | Per page | Per 1k views |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for k, g, com, n in out:
        pages_n = len(g["pages"])
        epc = com / g["aff_clicks"] if g["aff_clicks"] else None
        cr = n / g["aff_clicks"] if g["aff_clicks"] else None
        per_page = com / pages_n if pages_n else None
        rpm = com / g["views"] * 1000 if g["views"] else None
        name = short(k, 45) if by == "page" else k
        rev = f" ({g['reversed']} reversed)" if g["reversed"] else ""
        print(f"| {name} | {pages_n or '—'} | {fmt(g['views']) if g['views'] else '—'} | "
              f"{fmt(g['aff_clicks']) if g['aff_clicks'] else '—'} | {fmt(n)}{rev} | "
              f"{money(com, cur)} | {money(g['pending'].get(cur), cur) if g['pending'].get(cur) else '—'} | "
              f"{money(epc, cur) if epc is not None else '—'} | {pct(cr)} | "
              f"{money(per_page, cur) if per_page is not None else '—'} | "
              f"{money(rpm, cur) if rpm is not None else '—'} |")
    others = Counter()
    for g in groups.values():
        for c2, v in g["commission"].items():
            if c2 != cur:
                others[c2] += v
    if others:
        print("\nOther currencies, not in the table: " +
              " · ".join(money(v, c2) for c2, v in others.items()))


# ---------- due ----------

def next_check(p):
    pub, last = p["published"], p["last_check"]
    if last is None:
        return pub + timedelta(days=CHECK_POINTS[0])
    if p["status"] == "not-indexed":
        return last + timedelta(days=RECHECK_NOT_INDEXED)
    for d in CHECK_POINTS:
        if pub + timedelta(days=d) > last:
            return pub + timedelta(days=d)
    return last + timedelta(days=CHECK_EVERY)


def audit_reason(p):
    if p["last_audit"] is None:
        return "never audited"
    if p["last_refresh"] and p["last_refresh"] >= p["last_audit"]:
        return "refreshed after last audit"
    for d in AUDIT_POINTS:
        if p["age"] >= d and p["last_audit"] < p["published"] + timedelta(days=d):
            return f"{d}-day review"
    return None


def sales_due(rows, sales, pages, today):
    """Programs with live pages whose sales were not reported for 7+ days."""
    progs = {}
    for p in pages.values():
        if p["moved"] or p["status"] in GONE:
            continue
        prog = p["program"] or p["offer"]
        if prog:
            progs.setdefault(prog.lower(), prog)
    last_import, last_any = {}, {}
    for r in rows:
        if r["event"] == "import" and r.get("program") and "sales" in r.get("note", ""):
            k = r["program"].lower()
            last_import[k] = max(last_import.get(k, r["_d"]), r["_d"])
            last_any[k] = max(last_any.get(k, r["_d"]), r["_d"])
    for r in sales:
        k = (r.get("program") or "").lower()
        if k and r.get("source") == "manual":
            last_any[k] = max(last_any.get(k, r["_d"]), r["_d"])
    first_pub = {}
    for p in pages.values():
        k = (p["program"] or p["offer"]).lower()
        if k:
            first_pub[k] = min(first_pub.get(k, p["published"]), p["published"])
    out = []
    for k, name in sorted(progs.items()):
        since = last_any.get(k) or first_pub.get(k)
        if since and (today - since).days >= SALES_EVERY:
            li = last_import.get(k)
            why = f"last import {li}" if li else "never imported"
            if last_any.get(k) and last_any.get(k) != li:
                why += f", last manual sale {last_any[k]}"
            out.append((name, why, li))
        elif last_import.get(k) is None or (today - last_import[k]).days >= RECONCILE_EVERY:
            if since and (today - (first_pub.get(k) or today)).days >= RECONCILE_EVERY:
                out.append((name, "monthly reconciliation: export to catch reversals and missed sales",
                            last_import.get(k)))
    return out


def due_lists(rows, sales, pages, today):
    out = defaultdict(list)
    for p in pages.values():
        if p["moved"] or p["status"] == "dead":
            continue
        if p["last_check"] and p["status"] in GONE:
            out["republish"].append((p, f"{p['status']} on {p['last_check']}"))
            continue
        if p["imported"] and not p["last_check"]:
            out["imported"].append((p, "imported, status unknown"))
            continue
        nc = next_check(p)
        if nc <= today:
            late = (today - nc).days
            out["check"].append((p, f"due {nc}" + (f" ({late} d late)" if late else "")))
        if p["age"] >= 14 and not p["ever_indexed"]:
            out["not_indexed"].append((p, f"{p['age']} days, " + (p["status"] or "never checked")))
        if p["score"] is not None and p["score"] < AUDIT_MIN and not (
                p["last_refresh"] and p["last_refresh"] >= p["last_audit"]):
            out["improve"].append((p, f"score {p['score']:.0f} on {p['last_audit']}"))
        reason = audit_reason(p)
        if reason:
            out["audit"].append((p, reason))
        if not p["sub_id"] and p["age"] <= 365:
            out["no_sub"].append((p, "sales counted by program"))
    out["sales"] = sales_due(rows, sales, pages, today)
    return out


# ---------- commands ----------

def counts(rows, s, e):
    # imported pages with an unknown date are inventory, not work done on the import day
    sel = [r for r in rows if s <= r["_d"] <= e
           and not (r["event"] == "published" and "publish date unknown" in (r.get("note") or ""))
           and not (r["event"] == "note" and (r.get("note") or "").startswith("details from "))]
    return sel, Counter(r["event"] for r in sel)


def done_line(c, minutes):
    parts = [f"{c[ev]} {LABELS[ev]}" for ev in EVENTS if ev != "baseline" and c.get(ev)]
    if minutes:
        parts.append(f"{minutes / 60:.1f} h logged")
    return " · ".join(parts) if parts else "nothing logged"


def load(a):
    today = pdate(a.today) if getattr(a, "today", None) else date.today()
    rows = read_rows(a.journal)
    pages = page_states(rows, today)
    sales = read_sales(sales_path(a.journal, a.sales_path_override), pages)
    return today, rows, pages, sales


def money_totals(sales, s, e):
    tot, pend, n, rev_n, unattr = defaultdict(float), defaultdict(float), 0, 0, 0
    for r in sales:
        if not (s <= r["_d"] <= e):
            continue
        cur = (r.get("currency") or "USD").upper()
        if r["status"] == "reversed" and r["_c"] >= 0:
            rev_n += 1
            continue
        tot[cur] += r["_c"]
        if r["_c"] > 0:
            n += 1
            if not r["_page"]:
                unattr += 1
        elif r["_c"] < 0:
            n -= 1
            rev_n += 1
        if r["status"] == "pending":
            pend[cur] += r["_c"]
    return tot, pend, n, rev_n, unattr


def cmd_summary(a):
    today, rows, pages, sales = load(a)
    s, e, label = period_range(a.period, today, rows, sales)
    sel, c = counts(rows, s, e)
    minutes = sum(num(r.get("minutes")) or 0 for r in sel)

    print(f"# Work report · {label} · {s}" + ("" if s == e else f" – {e}"))
    print(f"\n**Done:** {done_line(c, minutes)}")

    tot, pend, n, rev_n, unattr = money_totals(sales, s, e)
    views = sum(num(r.get("views")) or 0 for r in sel if r["event"] in ("traffic", "stats"))
    aclk = sum(num(r.get("aff_clicks")) or 0 for r in sel if r["event"] in ("traffic", "stats"))
    legacy = sum(num(r.get("revenue")) or 0 for r in sel if r["event"] == "stats")
    if tot or rev_n or views or aclk or legacy:
        money_s = " + ".join(money(v, k) for k, v in tot.items()) or money(0)
        line = f"**Sales:** {n} sales · {money_s} commission"
        if any(pend.values()):
            line += " (pending " + " + ".join(money(v, k) for k, v in pend.items() if v) + ")"
        if rev_n:
            line += f" · {rev_n} reversed"
        if unattr:
            line += f" · {n - unattr} tied to a page, {unattr} by program only"
        if legacy:
            line += f" · {money(legacy)} from stats rows"
        print(f"\n{line}")
        if views or aclk:
            print("**Traffic:** " + " · ".join(x for x in (
                      f"{fmt(views)} views" if views else "", f"{fmt(aclk)} affiliate clicks" if aclk else "") if x)
                  + (f" · conv. {pct(n / aclk)}" if aclk and n else ""))

    if a.period not in ("today", "yesterday", None) and s != e:
        ps, pe = previous_range(a.period, s, e)
        _, pc = counts(rows, ps, pe)
        ptot, _, pn, _, _ = money_totals(sales, ps, pe)
        keys = ["published", "check", "audit", "refreshed", "moved", "platform"]
        cmp = [f"{LABELS[k]} {c[k]} vs {pc[k]}" for k in keys if c[k] or pc[k]]
        if n or pn:
            cur = next(iter(tot or ptot), "USD")
            cmp.append(f"sales {n} vs {pn}")
            cmp.append(f"commission {money(tot.get(cur, 0), cur)} vs {money(ptot.get(cur, 0), cur)}")
        if cmp:
            print(f"\n**vs previous period ({ps} – {pe}):** " + " · ".join(cmp))

    if not sel and not any(s <= r["_d"] <= e for r in sales):
        print("\nNothing in the journal for this period.")
    else:
        byday = defaultdict(Counter)
        for r in sel:
            byday[r["_d"]][r["event"]] += 1
        for r in sales:
            if s <= r["_d"] <= e and counted(r) and r["_c"] > 0:
                byday[r["_d"]]["sale"] += 1
        if byday and s != e:
            print("\n## By day\n")
            for d in sorted(byday):
                ev = ", ".join(f"{n2} {LABELS.get(k, 'sales' if k == 'sale' else k)}"
                               for k, n2 in byday[d].items())
                print(f"- **{d} ({d.strftime('%a')})** — {ev}")

        pub = [r for r in sel if r["event"] == "published" and r.get("page_url")]
        if pub:
            print("\n## Pages published\n")
            print("| Date | Page | Platform | Offer | Status now | Audit |")
            print("|---|---|---|---|---|---|")
            hc = Counter()
            for r in pub:
                p = pages.get(r["page_url"])
                h = health(p) if p else "—"
                hc[h] += 1
                sc = fmt(p["score"]) if p and p["score"] is not None else "—"
                print(f"| {r['_d']} | {short(r['page_url'])} | {r.get('platform', '')} | "
                      f"{r.get('offer', '')} | {h} | {sc} |")
            print("\n**Health of these pages:** " + " · ".join(f"{k} {v}" for k, v in hc.most_common()))

        if any(s <= r["_d"] <= e for r in sales):
            groups = effect_table(rows, sales, pages, s, e, "page")
            groups = {k: g for k, g in groups.items() if g["commission"] or g["reversed"]}
            if groups:
                print("\n## Pages that earned\n")
                print_effect(groups, "page", main_currency(groups), limit=10)

        tasks = [r for r in sel if r["event"] in ("task", "platform", "note") and r.get("note")]
        if tasks:
            print("\n## Other work\n")
            for r in tasks:
                print(f"- {r['_d']} · {r['event']} · " + " ".join(x for x in (r.get('platform', ''), r['note']) if x))

    due = due_lists(rows, sales, pages, today)
    parts = [f"{len(due[k])} {t}" for k, t in (
        ("sales", "sales reports to upload"), ("check", "checks due"),
        ("not_indexed", "not indexed 14+ days"), ("republish", "to republish"),
        ("audit", "audits due"), ("improve", "to improve"))
        if due[k]]
    if parts:
        print(f"\n**Needs attention today ({today}):** " + " · ".join(parts) + " — run `due` for the list")


def cmd_effect(a):
    today, rows, pages, sales = load(a)
    s, e, label = period_range(a.period, today, rows, sales)
    groups = effect_table(rows, sales, pages, s, e, a.by)
    groups = {k: g for k, g in groups.items()
              if g["pages"] or g["views"] or g["aff_clicks"] or g["commission"] or g["reversed"]
              or g["stats_rev"]}
    print(f"# Effectiveness by {a.by.replace('_', ' ')} · {label} · {s} – {e}\n")
    if not groups:
        print("No pages, traffic or sales in this period.")
        return
    curs = Counter()
    for g in groups.values():
        for c_, v in list(g["commission"].items()) + list(g["est"].items()):
            curs[c_] += abs(v)
    curs = [c_ for c_, _ in curs.most_common()] or [main_currency(groups)]
    if getattr(a, "currency", None):
        curs = [a.currency.upper()]
    for cur in curs:  # money stays in its currency: one table per currency, never mixed
        if len(curs) > 1:
            print(f"\n## Commission in {cur}\n")
        sub = {k: g for k, g in groups.items()
               if g["commission"].get(cur) or g["est"].get(cur) or (cur == curs[0] and not g["commission"] and not g["est"])}
        print_effect(sub or groups, a.by, cur)
    tot, pend, n, rev_n, unattr = money_totals(sales, s, e)
    live = sum(1 for p in pages.values() if p["published"] <= e and not p["moved"]
               and p["status"] not in GONE)
    print(f"\n**Total:** {n} sales · " + " + ".join(money(tot.get(c_, 0), c_) for c_ in curs) + " commission"
          f" · {live} pages alive or unchecked at period end")
    if n:
        unattr = min(unattr, n)  # refunds lower the net count; never show a negative tied share
        exact = n - unattr
        print(f"\n**Attribution:** {exact} of {n} sales tied to a page exactly ({exact / n * 100:.0f}%), "
              f"{unattr} known only by program. Program and month totals count every sale; "
              "page, platform, offer, content-type and campaign tables add an estimated share for the rest.")
    print("\nEPC = commission / affiliate clicks · Conv. = sales / affiliate clicks · "
          "Per page = commission / pages · Per 1k views = commission / views × 1000. "
          "Numbers only from the user's logs and exports.")


def cmd_due(a):
    today, rows, pages, sales = load(a)
    due = due_lists(rows, sales, pages, today)
    print(f"# Check queue · {today}\n")
    if not any(due.values()):
        print("Nothing due. Pages checked and audited on schedule, sales reported.")
        return
    if due["sales"]:
        print(f"## Upload sales reports ({len(due['sales'])})\n")
        for name, why, li in due["sales"]:
            frm = (li + timedelta(days=1)) if li else None
            span = f"export from {frm} to {today}" if frm else "export everything since the first page"
            print(f"- **{name}** — {why} · {span}")
        print()
    if due["imported"]:
        n = len(due["imported"])
        per = Counter(p["platform"] or "?" for p, _ in due["imported"])
        print(f"## Imported pages, not checked yet ({n}) — one bulk alive / index check\n")
        print("- " + ", ".join(f"{k} {v}" for k, v in per.most_common()))
        print("- Run platform-monitor on the whole list (page-checker agent); statuses and the schedule start from that check.\n")
    sections = [
        ("republish", "Removed / noindex — republish from the saved copy"),
        ("not_indexed", "Not indexed 14+ days after publishing — resubmit, add links or move"),
        ("check", "Alive / index check due"),
        ("improve", f"Audit score under {AUDIT_MIN} — improve, then re-audit"),
        ("audit", "Conversion audit due"),
        ("no_sub", "Optional: no sub-ID — add one if the network supports it, otherwise sales are counted by program"),
    ]
    for key, title in sections:
        items = due[key]
        if not items:
            continue
        print(f"## {title} ({len(items)})\n")
        for p, why in sorted(items, key=lambda x: (PRIORITIES.index(x[0]["priority"]), x[0]["published"])):
            q = f" · “{p['query']}”" if p["query"] else ""
            star = "★ " if p["priority"] == "high" else ""
            print(f"- {star}{short(p['url'])} · {p['platform'] or '?'} · {p['age']} d{q} — {why}")
        print()


def cmd_pages(a):
    today, rows, pages, sales = load(a)
    items = [p for p in pages.values() if (not a.platform or p["platform"] == a.platform)
             and (not a.priority or p["priority"] == a.priority)
             and (not a.topic or a.topic.lower() in p["topic_key"])]
    items.sort(key=lambda p: (PRIORITIES.index(p["priority"]), -(p["published"].toordinal())))
    earned = defaultdict(lambda: [0, 0.0])
    for r in sales:
        if r["_page"] and counted(r):
            earned[r["_page"]][0] += 1 if r["_c"] > 0 else -1 if r["_c"] < 0 else 0
            earned[r["_page"]][1] += r["_c"]
    traffic = defaultdict(lambda: [0.0, 0.0])
    for r in rows:
        if r["event"] in ("traffic", "stats") and r.get("page_url"):
            traffic[r["page_url"]][0] += num(r.get("views")) or 0
            traffic[r["page_url"]][1] += num(r.get("aff_clicks")) or 0
    print(f"# Pages · {today} · {len(items)} total\n")
    if not items:
        print("No pages in the journal yet.")
        return
    print("| Published | Page | Platform | Topic | Prio | Offer | Age | Status | Pos | Audit | Views | Aff. clicks | Sales | Commission |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    hc = Counter()
    for p in items:
        h = health(p)
        hc[h] += 1
        n, c = earned[p["url"]]
        v, ac = traffic[p["url"]]
        pos = "—" if p["position"] is None else (f"**{p['position']:.0f}**" if p["position"] <= TOP else f"{p['position']:.0f}")
        if p["position"] is not None and p.get("prev_pos") is not None and p["prev_pos"] != p["position"]:
            d = p["prev_pos"] - p["position"]
            pos += f" ({'↑' if d > 0 else '↓'}{abs(d):.0f})"
        print(f"| {p['published']} | {short(p['url'], 45)} | {p['platform']} | {short(p['topic_key'], 30)} | "
              f"{'★' if p['priority'] == 'high' else ('low' if p['priority'] == 'low' else '')} | {p['offer']} | "
              f"{p['age']} d | {h} | {pos} | {fmt(p['score'])} | "
              f"{fmt(v) if v else '—'} | {fmt(ac) if ac else '—'} | {n} | {money(c)} |")
    print("\n**Status:** " + " · ".join(f"{k} {v}" for k, v in hc.most_common()))


def cmd_add(a):
    row = journal_row(event=a.event, page_url=a.url, platform=a.platform, offer=a.offer,
                      program=a.program, campaign=a.campaign, sub_id=a.sub_id, main_query=a.query,
                      content_type=a.type, status=a.status, score=a.score, views=a.views,
                      clicks=a.clicks, aff_clicks=a.aff_clicks, sales=a.sales,
                      revenue=a.revenue, minutes=a.minutes, note=a.note, topic=a.topic,
                      priority=a.priority, position=a.position,
                      link_target=a.link_target, link_rel=a.link_rel, anchor=a.anchor, cost=a.cost)
    if a.date:
        row["date"] = a.date
    if a.time:
        row["time"] = a.time
    if not pdate(row["date"]):
        sys.exit("--date must be YYYY-MM-DD")
    append(a.journal, COLUMNS, [row])
    print(f"Logged: {row['date']} {row['event']} {row['page_url'] or row['note']}".strip())


def cmd_site_roi(a):
    """Site owners / agencies: what our pages brought to the site — visits, conversions, revenue — against spend."""
    today, rows, pages, sales = load(a)
    s_, e_, label = period_range(a.period, today, rows)
    agg = defaultdict(lambda: {"pages": set(), "visits": 0.0, "conv": 0.0, "rev": 0.0, "cost": 0.0, "dofollow": 0})
    for r in rows:
        if r["event"] != "traffic" or not (s_ <= r["_d"] <= e_):
            continue
        url = r.get("page_url") or ""
        key = url if a.by == "page" else (r.get("platform") or (pages[url]["platform"] if url in pages else "?"))
        if a.by == "page" and not url:
            key = f"{r.get('platform') or '?'} (platform total)"
        g = agg[key]
        g["visits"] += num(r.get("views")) or 0
        g["conv"] += num(r.get("sales")) or 0
        g["rev"] += num(r.get("revenue")) or 0
    for p in pages.values():
        if not (s_ <= p["published"] <= e_) or p["url"].startswith(("http://own-site", "https://own-site")):
            continue
        if p["platform"] == "own-site":
            continue
        key = p["url"] if a.by == "page" else (p["platform"] or "?")
        g = agg[key]
        g["pages"].add(p["url"])
        g["cost"] += p["cost"]
        if p["link_rel"] in ("dofollow", "follow") and health(p) not in GONE:
            g["dofollow"] += 1
    print(f"# Site results from parasite pages · {label} · by {a.by}\n")
    if not agg:
        print("No pages or traffic in this period. Import GA4 / shop data with `import-traffic … --medium parasite`.")
        return
    print(f"| {'Page' if a.by == 'page' else 'Platform'} | Pages | Visits | Conversions | Conv. rate | Revenue | Spend | Return | Live dofollow |")
    print("|---|---|---|---|---|---|---|---|---|")
    tot = defaultdict(float)
    for k, g in sorted(agg.items(), key=lambda x: (-x[1]["rev"], -x[1]["visits"])):
        cr = f"{100 * g['conv'] / g['visits']:.1f}%" if g["visits"] and g["conv"] else "—"
        ret = g["rev"] - g["cost"]
        print(f"| {short(k, 45)} | {len(g['pages']) or '—'} | {fmt(g['visits']) if g['visits'] else '—'} | "
              f"{fmt(g['conv']) if g['conv'] else '—'} | {cr} | {money(g['rev']) if g['rev'] else '—'} | "
              f"{money(g['cost']) if g['cost'] else '—'} | {money(ret) if (g['rev'] or g['cost']) else '—'} | {g['dofollow'] or '—'} |")
        for f in ("visits", "conv", "rev", "cost", "dofollow"):
            tot[f] += g[f]
    print(f"\n**Total:** {fmt(tot['visits'])} visits · {fmt(tot['conv'])} conversions · revenue {money(tot['rev'])} · "
          f"spend {money(tot['cost'])} · return {money(tot['rev'] - tot['cost'])} · live dofollow links {int(tot['dofollow'])}")
    print("Revenue and conversions come from the site's own data (GA4 or shop export by source / utm_content); "
          "a dash means not measured, not zero.")


# ---------- backlinks (site owners and agencies) ----------

def cmd_backlinks(a):
    """Links our pages give to the user's (or client's) site: dofollow / nofollow, live or gone, cost."""
    today, rows, pages, sales = load(a)
    s_, e_, label = period_range(a.period, today, rows)
    items = [p for p in pages.values() if p["link_target"] and s_ <= p["published"] <= e_
             and (not a.target or a.target.lower() in p["link_target"].lower())]
    traffic = defaultdict(float)
    for r in rows:
        if r["event"] in ("traffic", "stats") and r.get("page_url"):
            traffic[r["page_url"]] += num(r.get("views")) or 0
    print(f"# Backlinks · {label} · {len(items)} pages with a link to the site\n")
    if not items:
        print("No pages with a link target yet. Log one: add --event published --url … --link-target https://site/page "
              "--link-rel dofollow --anchor \"best crm\" [--cost 150]")
        return
    def alive(p):
        return health(p) not in GONE and health(p) != "moved"
    print("| Published | Page | Platform | Links to | Rel | Anchor | Status | Cost | Visits |")
    print("|---|---|---|---|---|---|---|---|---|")
    for p in sorted(items, key=lambda p: p["published"], reverse=True):
        print(f"| {p['published']} | {short(p['url'], 40)} | {p['platform']} | {short(p['link_target'], 35)} | "
              f"{p['link_rel'] or '?'} | {short(p['anchor'], 25) or '—'} | {health(p)} | "
              f"{money(p['cost']) if p['cost'] else 'free'} | {fmt(traffic[p['url']]) if traffic[p['url']] else '—'} |")
    live = [p for p in items if alive(p)]
    dof = [p for p in live if p["link_rel"] in ("dofollow", "follow")]
    spent = sum(p["cost"] for p in items)
    paid = [p for p in items if p["cost"]]
    print(f"\n**Total:** {len(items)} links · live {len(live)} · live dofollow {len(dof)} · "
          f"nofollow/ugc/sponsored {sum(1 for p in live if p['link_rel'] and p['link_rel'] not in ('dofollow', 'follow'))} · "
          f"gone {len(items) - len(live)} · rel unknown {sum(1 for p in items if not p['link_rel'])}")
    if spent:
        print(f"**Spend:** {money(spent)} on {len(paid)} paid placements · per live dofollow link "
              f"{money(spent / len(dof)) if dof else '—'} · visits from paid pages "
              f"{fmt(sum(traffic[p['url']] for p in paid)) or 0}")
    by_t = defaultdict(list)
    for p in live:
        by_t[p["link_target"].split("?")[0].rstrip("/")].append(p)
    print("\n## By target page (live links)\n")
    print("| Target | Live links | Dofollow | Anchors |")
    print("|---|---|---|---|")
    for t, ps in sorted(by_t.items(), key=lambda x: -len(x[1])):
        anchors = Counter(p["anchor"] for p in ps if p["anchor"])
        print(f"| {short(t, 50)} | {len(ps)} | {sum(1 for p in ps if p['link_rel'] in ('dofollow', 'follow'))} | "
              + ", ".join(f"{k} ×{v}" for k, v in anchors.most_common(4)) + " |")
    same = [t for t, ps in by_t.items() if ps and Counter(p["anchor"] for p in ps if p["anchor"]).most_common(1)
            and Counter(p["anchor"] for p in ps if p["anchor"]).most_common(1)[0][1] >= max(3, 0.6 * len(ps))]
    if same:
        print("\n**Attention:** one exact anchor on most links to " + ", ".join(short(t, 40) for t in same)
              + " — vary anchors (brand, URL, natural phrases) so the profile looks natural.")


def cmd_sale(a):
    c = num(a.commission)
    if c is None:
        sys.exit("--commission must be a number")
    d = a.date or date.today().isoformat()
    if not pdate(d):
        sys.exit("--date must be YYYY-MM-DD")
    row = {"date": d, "program": a.program, "network": a.network or "", "offer": a.offer or "",
           "sub_id": a.sub_id or "", "page_url": a.url or "", "order_id": a.order_id or "",
           "amount": a.amount or "", "commission": f"{c:.2f}",
           "currency": (a.currency or "USD").upper(),
           "status": sale_status(a.status or "approved", c), "source": "manual",
           "note": a.note or ""}
    append(sales_path(a.journal, a.sales_path_override), SALE_COLUMNS, [row])
    today = pdate(d)
    pages = page_states(read_rows(a.journal), today)
    attached = row["page_url"] or lookups(pages)[0].get(row["sub_id"].lower(), "")
    print(f"Sale logged: {d} · {a.program} · {money(c, row['currency'])}"
          + (f" · page {short(attached)}" if attached else " · not tied to a page (no URL or known sub-ID)"))


def sniff_rows(path):
    with open(path, encoding="utf-8-sig", errors="replace") as f:
        text = f.read()
    lines = text.splitlines()
    # skip title lines above the header (some exports start with a report title)
    best, start = 0, 0
    for i, ln in enumerate(lines[:15]):
        # fields outside quotes: a data row like "Vitamin D3 + K2 (drops, softgels)" must not win
        n = max(len(next(csv.reader([ln], delimiter=d), [])) - 1 for d in (",", ";", "\t"))
        if n > best:
            best, start = n, i
    body = "\n".join(lines[start:])
    try:
        dialect = csv.Sniffer().sniff(body[:5000], delimiters=",;\t")
    except csv.Error:
        dialect = csv.excel
    reader = csv.reader(io.StringIO(body), dialect)
    header = next(reader, [])
    rows = [r for r in reader if any(x.strip() for x in r)]
    return header, rows


def map_columns(header, aliases, overrides):
    normed = [norm(h) for h in header]
    found = {}
    for field, names in aliases.items():
        if field in overrides:
            want = norm(overrides[field])
            if want in normed:
                found[field] = normed.index(want)
            continue
        for name in names:
            if name in normed:
                found[field] = normed.index(name)
                break
    return found


def parse_dates(values, fmt_hint=None):
    vals = [v.strip() for v in values]
    if fmt_hint:
        out = []
        for v in vals:
            try:
                out.append(datetime.strptime(v[:len(datetime.now().strftime(fmt_hint))], fmt_hint).date())
            except ValueError:
                out.append(None)
        return out
    dayfirst = False
    for v in vals:
        m = re.match(r"(\d{1,2})[/.](\d{1,2})[/.](\d{2,4})", v)
        if m and int(m.group(1)) > 12:
            dayfirst = True
            break
        if m and "." in v[:6]:
            dayfirst = True
    out = []
    for v in vals:
        d = None
        m = re.match(r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})", v)
        if m:
            d = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
        else:
            m = re.match(r"(\d{1,2})[/.](\d{1,2})[/.](\d{2,4})", v)
            if m:
                a1, b1, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
                y += 2000 if y < 100 else 0
                d = (y, b1, a1) if dayfirst else (y, a1, b1)
            else:
                for f in ("%b %d, %Y", "%d %b %Y", "%B %d, %Y", "%d %B %Y", "%b %d %Y"):
                    try:
                        dt = datetime.strptime(re.sub(r"\s+", " ", v.split(" at ")[0])[:20].strip(), f)
                        d = (dt.year, dt.month, dt.day)
                        break
                    except ValueError:
                        continue
        try:
            out.append(date(*d) if d else None)
        except ValueError:
            out.append(None)
    return out


def parse_map(items):
    m = {}
    for it in items or []:
        if "=" not in it:
            sys.exit(f"--map expects field=Header, got {it}")
        k, v = it.split("=", 1)
        m[k.strip()] = v.strip()
    return m


def cmd_import_sales(a):
    header, raw = sniff_rows(a.export)
    if not raw:
        sys.exit("The export has no data rows.")
    cols = map_columns(header, SALE_ALIASES, parse_map(a.map))
    missing = [f for f in ("date", "commission") if f not in cols]
    if missing:
        print("Could not find columns: " + ", ".join(missing))
        print("Columns in the file: " + " | ".join(header))
        sys.exit("Re-run with --map date=\"<header>\" --map commission=\"<header>\"")
    get = lambda r, f: r[cols[f]].strip() if f in cols and cols[f] < len(r) else ""
    dates = parse_dates([get(r, "date") for r in raw], a.date_format)

    today = max([d for d in dates if d] + [date.today()])
    rows = read_rows(a.journal)
    pages = page_states(rows, today)
    by_sub, _ = lookups(pages)
    spath = sales_path(a.journal, a.sales_path_override)
    existing = {}
    for i, r in enumerate(read_csv(spath)):
        r["_i"] = i
        existing[sale_key(r)] = r

    new, dup, updated, bad, unknown_sub, no_sub = [], 0, 0, 0, Counter(), 0
    for r, d in zip(raw, dates):
        c = num(get(r, "commission"))
        if d is None or c is None:
            bad += 1
            continue
        sub = get(r, "sub_id")
        row = {"date": d.isoformat(), "program": a.program, "network": a.network or "",
               "offer": get(r, "offer"), "sub_id": sub, "page_url": "",
               "order_id": get(r, "order_id"), "amount": get(r, "amount"),
               "commission": f"{c:.2f}",
               "currency": (get(r, "currency") or a.currency or "USD").upper(),
               "status": sale_status(get(r, "status"), c),
               "source": f"import:{os.path.basename(a.export)}", "note": "",
               "referer": url_domain(get(r, "referer")) if get(r, "referer") else ""}
        if re.search(r"repeat customer", row["offer"], re.I):  # Everflow-style repeat-order offers
            row["offer"] = re.sub(r"\s*[-–]\s*repeat customer tracking\s*$", "", row["offer"], flags=re.I)
            row["note"] = "repeat customer"
        amt = num(row["amount"])
        row["amount"] = f"{amt:.2f}" if amt is not None else ""
        k = sale_key(row)
        if row["order_id"] and k in existing:
            if existing[k].get("status") == row["status"]:
                dup += 1
                continue
            updated += 1
        elif not row["order_id"]:
            k2 = (row["date"], sub.lower(), row["commission"], row["amount"], a.program.lower())
            if any((e.get("date"), (e.get("sub_id") or "").lower(), e.get("commission"),
                    e.get("amount"), (e.get("program") or "").lower()) == k2
                   and e.get("source", "").startswith("import") for e in existing.values()):
                dup += 1
                continue
        existing[k] = row
        new.append(row)
        if not sub:
            no_sub += 1
        elif sub.lower() not in by_sub:
            unknown_sub[sub] += 1

    if new:
        append(spath, SALE_COLUMNS, new)
    span = [d for d in dates if d]
    note = (f"sales import {os.path.basename(a.export)}: "
            f"{min(span) if span else '?'}..{max(span) if span else '?'}, "
            f"{len(new) - updated} new, {updated} status updates, {dup} already in")
    append(a.journal, COLUMNS, [journal_row(event="import", program=a.program, note=note)])

    good = [r for r in new if r["status"] != "reversed" or num(r["commission"]) < 0]
    tot = sum(num(r["commission"]) for r in good)
    print(f"Imported from {os.path.basename(a.export)} → {a.program}")
    print(f"- Columns used: " + ", ".join(f"{f} = “{header[i]}”" for f, i in cols.items()))
    print(f"- {len(new) - updated} new sales · {updated} status updates · {dup} already in the journal"
          + (f" · {bad} rows skipped (no date or commission)" if bad else ""))
    print(f"- New commission: {money(tot, new[0]['currency'] if new else 'USD')}"
          f" ({sum(1 for r in new if r['status'] == 'pending')} pending,"
          f" {sum(1 for r in new if r['status'] == 'reversed')} reversed)")
    if no_sub:
        print(f"- {no_sub} sales have no sub-ID: counted in program and month totals exactly; "
              "per-page share is estimated in `effect`.")
    if unknown_sub:
        print("- Sub-IDs not found in the journal (add them to the page's published row): "
              + ", ".join(f"{k} ({v})" for k, v in unknown_sub.most_common(15)))
    if "sub_id" not in cols:
        print("- No sub-ID column found. If the export has one under another name, "
              "re-run with --map sub_id=\"<header>\" (duplicates are skipped).")


NO_REFERRER = {"", "(direct)", "direct", "(none)", "none", "(not set)", "notset", "noreferrer",
               "no referrer", "-", "unknown", "(direct) / (none)"}


def source_platform(value, known):
    """Platform slug for a referrer / source / utm_source value, or '' if it is not one of the
    user's platforms. known: {slug or domain: slug}."""
    v = (value or "").strip().lower()
    if v in NO_REFERRER:
        return ""
    v = v.split(" / ")[0].strip()  # GA4 "source / medium"
    if v in NO_REFERRER:
        return ""
    if v in known:
        return known[v]
    if "." in v:
        slug, dom, _ = platform_of(v)
        for k in (url_domain(v), dom, slug):
            if k in known:
                return known[k]
    k = norm(v)
    for name, slug in known.items():
        if norm(name) == k:
            return slug
    return ""


def cmd_import_traffic(a):
    header, raw = sniff_rows(a.export)
    if not raw:
        sys.exit("The export has no data rows.")
    cols = map_columns(header, TRAFFIC_ALIASES, parse_map(a.map))
    if not {"url", "sub_id", "source"} & set(cols) and not a.platform:
        print("Columns in the file: " + " | ".join(header))
        sys.exit("No page URL, sub-ID or referrer/source column found. Re-run with --map url=\"<header>\" "
                 "or --map source=\"<header>\", or pass --platform for a whole-platform report.")
    if "views" not in cols and "aff_clicks" not in cols and "conversions" not in cols and "site_revenue" not in cols:
        print("Columns in the file: " + " | ".join(header))
        sys.exit("No views or clicks column found. Re-run with --map views=\"<header>\" or --map aff_clicks=\"<header>\".")
    get = lambda r, f: r[cols[f]].strip() if f in cols and cols[f] < len(r) else ""
    today = date.today()
    end = pdate(a.to) if a.to else today
    start = pdate(a.from_) if a.from_ else None
    period = f"{start or '?'}..{end}"
    rows = read_rows(a.journal)
    pages = page_states(rows, end)
    by_sub, by_url = lookups(pages)
    seen = {(r.get("page_url"), r.get("platform", "").lower(), r.get("note")) for r in rows
            if r["event"] == "traffic"}

    # the user's platforms: slugs and domains from logged pages and the platform base
    known = {}
    for p in pages.values():
        slug, dom, _ = platform_of(p["url"])
        pl = (p.get("platform") or slug).lower()
        for k in (pl, slug, dom, url_domain(p["url"])):
            known.setdefault(k, pl)
    for slug, r in read_platforms(platforms_path(a.journal)).items():
        known[slug] = slug
        if r.get("domain"):
            known[r["domain"].lower()] = slug
    forced = (a.platform or "").lower()

    totals = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])      # page url -> views, clicks, conversions, revenue
    by_platform = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])  # platform slug -> same (no page match)
    medium = (getattr(a, "medium", None) or "").strip().lower()
    skipped_medium = 0
    unmatched = Counter()
    direct = 0.0
    for r in raw:
        v, c = num(get(r, "views")) or 0, num(get(r, "aff_clicks")) or 0
        cv, rv = num(get(r, "conversions")) or 0, num(get(r, "site_revenue")) or 0
        if not (v or c or cv or rv):
            continue
        if medium:
            src = get(r, "source").lower()
            row_medium = src.split(" / ", 1)[1].strip() if " / " in src else ""
            if row_medium != medium:
                skipped_medium += 1
                continue
        url = ""
        if "url" in cols:
            url = by_url.get(norm_url(get(r, "url")), "")
        if not url and "sub_id" in cols:
            url = by_sub.get(get(r, "sub_id").lower(), "")
        if not url and "source" in cols:  # a referrer that is the page itself
            url = by_url.get(norm_url(get(r, "source")), "")
        if url:
            for i, x in enumerate((v, c, cv, rv)):
                totals[url][i] += x
            continue
        pl = ""
        if "source" in cols:
            pl = source_platform(get(r, "source"), known)
        if not pl and "url" in cols and get(r, "url"):
            pl = source_platform(get(r, "url"), known)
        if not pl and forced and not ({"url", "sub_id", "source"} & set(cols)):
            pl = forced
        if pl:
            for i, x in enumerate((v, c, cv, rv)):
                by_platform[pl][i] += x
            continue
        raw_src = get(r, "source") or get(r, "url") or get(r, "sub_id")
        if "source" in cols and raw_src.strip().lower().split(" / ")[0] in NO_REFERRER:
            direct += v + c
        else:
            unmatched[raw_src or "(empty)"] += v + c

    fname = os.path.basename(a.export)
    out, skipped = [], 0
    for url, (v, c, cv, rv) in totals.items():
        note = f"traffic {period} from {fname}"
        if any(u == url and (n or "").startswith(f"traffic {period}") for u, _, n in seen):
            skipped += 1
            continue
        p = pages[url]
        out.append(journal_row(date=end.isoformat(), event="traffic", page_url=url,
                               platform=forced or p["platform"] or platform_of(url)[0], offer=p["offer"],
                               views=fmt(v) if v else "", aff_clicks=fmt(c) if c else "",
                               sales=fmt(cv) if cv else "", revenue=f"{rv:.2f}" if rv else "",
                               note=note))
    plat_out = 0
    for pl, (v, c, cv, rv) in by_platform.items():
        note = f"traffic {period} platform total from {fname}"
        if any(not u and s == pl and (n or "").startswith(f"traffic {period}") for u, s, n in seen):
            skipped += 1
            continue
        out.append(journal_row(date=end.isoformat(), event="traffic", page_url="", platform=pl,
                               views=fmt(v) if v else "", aff_clicks=fmt(c) if c else "",
                               sales=fmt(cv) if cv else "", revenue=f"{rv:.2f}" if rv else "",
                               note=note))
        plat_out += 1
    if out:
        append(a.journal, COLUMNS, out)
    print(f"Traffic import {fname} · period {period}")
    print(f"- Columns used: " + ", ".join(f"{f} = “{header[i]}”" for f, i in cols.items()))
    print(f"- {len(out) - plat_out} pages updated · {plat_out} platforms updated (whole-platform totals, "
          f"no single page) · {skipped} already imported for this period")
    if by_platform:
        print("- By platform: " + ", ".join(f"{pl} {fmt(x[0] + x[1])}" + (f" · {fmt(x[2])} conv." if x[2] else "")
                                             + (f" · {x[3]:.2f} revenue" if x[3] else "") for pl, x in
                                             sorted(by_platform.items(), key=lambda x: -sum(x[1][:2]))))
    if skipped_medium:
        print(f"- {skipped_medium} rows skipped: medium is not “{medium}” (only our pages' traffic is counted)")
    if direct:
        print(f"- {fmt(direct)} with no referrer (direct, apps, private browsing): counted in totals only, not tied to a platform")
    if unmatched:
        print(f"- {len(unmatched)} sources not among your pages or platforms (new platform? add it with `import-pages` or `platforms`): "
              + ", ".join(f"{short(k, 40)} ({fmt(n)})" for k, n in unmatched.most_common(10)))
    if not a.from_:
        print("- Tip: pass --from and --to with the export's date range so the same period is never counted twice.")


# ---------- inventory: existing pages and the personal platform base ----------

def read_platforms(path):
    return {r.get("platform", "").lower(): r for r in read_csv(path) if r.get("platform")}


def write_platforms(path, reg):
    cols = PLATFORM_COLUMNS[:]
    for r in reg.values():
        cols += [k for k in r if k not in cols]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for k in sorted(reg):
            w.writerow(reg[k])


def register_platforms(journal, found, source):
    """Add platforms not yet in the base. found: {slug: (domain, type)}. Returns new slugs."""
    path = platforms_path(journal)
    reg = read_platforms(path)
    new = []
    for slug, (dom, typ) in found.items():
        if not slug:
            continue
        r = reg.get(slug.lower())
        if r is None:
            reg[slug.lower()] = {"platform": slug, "domain": dom, "type": typ, "state": "active",
                                 "added": date.today().isoformat(), "source": source}
            new.append(slug)
        else:
            if not r.get("domain") and dom:
                r["domain"] = dom
            if not r.get("type") and typ:
                r["type"] = typ
    if new or reg:
        write_platforms(path, reg)
    return new


def urls_from_text(path):
    with open(path, encoding="utf-8-sig", errors="replace") as f:
        text = f.read()
    return text, re.findall(r"https?://[^\s,;\"'<>()\[\]]+", text)


def cmd_import_pages(a):
    text, loose = urls_from_text(a.file)
    header, raw = ([], [])
    if max(text[:3000].count(","), text[:3000].count(";"), text[:3000].count("\t")) > 0:
        header, raw = sniff_rows(a.file)
    cols = map_columns(header, PAGE_ALIASES, parse_map(a.map)) if header else {}
    if "url" not in cols and header:
        for i in range(len(header)):  # a column whose values are URLs
            if raw and sum(1 for r in raw[:20] if i < len(r) and re.match(r"https?://", r[i].strip())) >= max(1, len(raw[:20]) // 2):
                cols["url"] = i
                break
    get = lambda r, f: r[cols[f]].strip() if f in cols and cols[f] < len(r) else ""
    items = []
    if "url" in cols:
        dates = parse_dates([get(r, "date") for r in raw]) if "date" in cols else [None] * len(raw)
        for r, d in zip(raw, dates):
            u = get(r, "url")
            if re.match(r"https?://", u):
                items.append((u, d, {f: get(r, f) for f in cols if f not in ("url", "date")}))
    else:
        items = [(u.rstrip(".,"), None, {}) for u in loose]
    if not items:
        if header:
            print("Columns in the file: " + " | ".join(header))
        sys.exit("No page URLs found. Give a list of links (one per line) or a table with a URL column (--map url=\"<header>\").")

    rows = read_rows(a.journal)
    known = page_states(rows, date.max)
    have = {norm_url(u): p for u, p in known.items()}
    default_d = pdate(a.date) if a.date else None
    out, dup, seen, found, undated, filled = [], 0, set(), {}, 0, 0
    for u, d, extra in items:
        k = norm_url(u)
        if k in have and k not in seen:  # page already in: add only details it is missing
            p = have[k]
            add = {f: v for f, v in (("offer", extra.get("offer") or a.offer),
                                     ("program", extra.get("program") or a.program),
                                     ("campaign", extra.get("campaign") or a.campaign),
                                     ("sub_id", extra.get("sub_id")),
                                     ("main_query", extra.get("main_query")),
                                     ("content_type", extra.get("content_type") or a.type))
                   if v and not p.get({"main_query": "query"}.get(f, f))}
            if add:
                out.append(journal_row(date=date.today().isoformat(), time="", event="note",
                                       page_url=p["url"], platform=p["platform"],
                                       note="details from " + os.path.basename(a.file), **add))
                filled += 1
        if not k or k in have or k in seen:
            dup += 1
            seen.add(k)
            continue
        seen.add(k)
        slug, dom, typ = platform_of(u)
        given = (a.platform or extra.get("platform") or "").strip()
        if given:
            slug = platform_of("https://" + given)[0] if "." in given and " " not in given else given
        slug = (slug or "").lower().replace(" ", "-")
        found.setdefault(slug, (dom, typ))
        d = d or default_d
        if not d:
            undated += 1
        st = (extra.get("status") or "").lower()
        st = st if st in ALIVE | GONE | {"dead"} else ""
        note = "imported from " + os.path.basename(a.file) + ("" if d else "; publish date unknown")
        if extra.get("note"):
            note += "; " + extra["note"]
        out.append(journal_row(date=(d or date.today()).isoformat(), time="", event="published", page_url=u,
                               platform=slug, offer=extra.get("offer") or a.offer,
                               program=extra.get("program") or a.program,
                               campaign=extra.get("campaign") or a.campaign,
                               sub_id=extra.get("sub_id"), main_query=extra.get("main_query"),
                               content_type=extra.get("content_type") or a.type, status=st, note=note,
                               topic=extra.get("topic"),
                               priority=(extra.get("priority") or "").lower() if (extra.get("priority") or "").lower() in PRIORITIES else "",
                               position=extra.get("position") if num(extra.get("position")) is not None else ""))
    if out:
        append(a.journal, COLUMNS, out)
    new = register_platforms(a.journal, found, "my pages")
    added = [r for r in out if r["event"] == "published"]
    per = Counter(r["platform"] for r in added)
    print(f"Pages import {os.path.basename(a.file)}")
    if cols:
        print("- Columns used: " + ", ".join(f"{f} = “{header[i]}”" for f, i in cols.items()))
    print(f"- {len(added)} pages added to the journal · {dup} already there or repeated"
          + (f" · details added to {filled} of them" if filled else ""))
    if per:
        print(f"- Platforms ({len(per)}): " + ", ".join(f"{k} {v}" for k, v in per.most_common()))
    if new:
        print(f"- New in your platform base: {len(new)} ({', '.join(new[:15])}{'…' if len(new) > 15 else ''})")
    if undated:
        print(f"- {undated} pages without a publish date: dated today. Give dates (column or --date) for correct ages and check schedule.")
    missing = [f for f in ("offer", "program") if not any(r[f] for r in added)]
    if added and missing:
        print(f"- No {' / '.join(missing)} on these pages: sales can't be counted per offer/program until you add them (re-import with columns, or --offer/--program per batch).")
    if added:
        print("- Next: check which pages are alive and indexed (platform-monitor / page-checker), then audit the ones that matter.")


def platform_stats(rows, sales, pages, today):
    st = defaultdict(lambda: {"pages": 0, "alive": 0, "indexed": 0, "gone": 0, "unchecked": 0,
                              "first": None, "last": None, "sales": 0, "comm": 0.0, "views": 0.0,
                              "score": None, "tested": None})
    for p in pages.values():
        if not p["platform"]:
            continue
        s = st[p["platform"].lower()]
        s["pages"] += 1
        h = health(p)
        if h == "not checked yet":
            s["unchecked"] += 1
        elif h in ALIVE:
            s["alive"] += 1
        elif h in GONE or h == "moved":
            s["gone"] += 1
        if h in INDEXED:
            s["indexed"] += 1
        s["first"] = min(filter(None, [s["first"], p["published"]]))
        s["last"] = max(filter(None, [s["last"], p["published"]]))
    for r in sales:
        if r["_page"] and counted(r) and r["_page"] in pages:
            s = st[pages[r["_page"]]["platform"].lower()]
            s["sales"] += 1 if r["_c"] > 0 else -1 if r["_c"] < 0 else 0
            s["comm"] += r["_c"]
    for r in rows:
        pl = (r.get("platform") or "").lower()
        if not pl:
            continue
        if r["event"] in ("traffic", "stats"):
            st[pl]["views"] += num(r.get("views")) or 0
        if r["event"] == "platform":
            st[pl]["tested"] = r["_d"]
            if num(r.get("score")) is not None:
                st[pl]["score"] = num(r.get("score"))
    return st


def cmd_platforms(a):
    today, rows, pages, sales = load(a)
    reg = read_platforms(platforms_path(a.journal))
    found = {}
    for p in pages.values():  # pages logged one by one also feed the base
        if p["platform"] and p["platform"].lower() not in reg:
            _, dom, typ = platform_of(p["url"])
            found[p["platform"]] = (dom, typ)
    for r in rows:
        if r["event"] == "platform" and r.get("platform") and r["platform"].lower() not in reg:
            found[r["platform"]] = ("", "")
    if found:
        register_platforms(a.journal, found, "journal")
        reg = read_platforms(platforms_path(a.journal))
    st = platform_stats(rows, sales, pages, today)
    print(f"# My platforms · {today} · {len(reg)} in the base\n")
    if not reg:
        print("No platforms yet. Import your pages (import-pages) or log one: add --event platform --platform <slug>.")
        return
    tops = Counter(p["platform"].lower() for p in pages.values()
                   if p["position"] is not None and p["position"] <= TOP and not p["moved"] and health(p) not in GONE)
    print(f"| Platform | Domain | Type | State | Prio | Pages | Alive | Indexed | Top {TOP} | Gone | Not checked | Last page | Sales | Commission | Score |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    order = sorted(reg.values(), key=lambda r: (num(r.get("rank")) or 99, PRIORITIES.index(r.get("priority") or "normal"),
                                                -st[r["platform"].lower()]["pages"], r["platform"]))
    attention, waiting = [], []
    for r in order:
        s = st[r["platform"].lower()]
        score = r.get("score") or (fmt(s["score"]) if s["score"] is not None else "")
        prio = {"high": "★", "low": "low"}.get(r.get("priority") or "", "")
        print(f"| {r['platform']} | {r.get('domain') or '—'} | {r.get('type') or '?'} | {r.get('state') or 'active'} | {prio} | "
              f"{s['pages']} | {s['alive']} | {s['indexed']} | {tops[r['platform'].lower()]} | {s['gone']} | {s['unchecked']} | "
              f"{s['last'] or '—'} | {s['sales']} | {money(s['comm'])} | {score or '—'} |")
        checked = s["pages"] - s["unchecked"]
        if checked >= 3 and s["gone"] / checked >= 0.5 and (r.get("state") or "active") == "active":
            attention.append(f"{r['platform']}: {s['gone']} of {checked} checked pages gone — mark dropped or move pages")
        if s["pages"] == 0 and (r.get("state") or "active") in ("active", "testing"):
            waiting.append(r["platform"])
        elif not r.get("type"):
            attention.append(f"{r['platform']}: type unknown — run platform-analyzer once")
    tot = sum(s["pages"] for s in st.values())
    unchecked = sum(s["unchecked"] for s in st.values())
    print(f"\n**Total:** {tot} pages on {sum(1 for r in reg.values() if st[r['platform'].lower()]['pages'])} platforms"
          + (f" · {unchecked} not checked yet" if unchecked else ""))
    if waiting:
        print(f"\n**No pages yet on {len(waiting)} platforms — send their lists:** " + ", ".join(waiting))
    if attention:
        print("\n**Needs attention**")
        for x in attention[:12]:
            print("- " + x)


def cmd_platform_set(a):
    path = platforms_path(a.journal)
    reg = read_platforms(path)
    key = a.platform.lower()
    r = reg.setdefault(key, {"platform": a.platform, "state": "active",
                             "added": date.today().isoformat(), "source": "manual"})
    for f in ("domain", "type", "language", "links", "account", "score", "state", "priority", "rank", "note"):
        v = getattr(a, f)
        if v is not None:
            r[f] = v
    write_platforms(path, reg)
    print(f"Platform base: {r['platform']} · " + " · ".join(f"{f} {r[f]}" for f in PLATFORM_COLUMNS[1:] if r.get(f)))


def cmd_tag(a):
    """Set topic / priority / position / offer … on many pages at once (a `tag` row per page)."""
    rows = read_rows(a.journal)
    pages = page_states(rows, date.max)
    by_norm = {norm_url(u): p for u, p in pages.items()}
    targets = []
    urls = list(a.url or [])
    if a.urls_file:
        urls += urls_from_text(a.urls_file)[1]
    for u in urls:
        p = by_norm.get(norm_url(u))
        if p:
            targets.append(p)
        else:
            print(f"- not in the journal: {short(u)}")
    if a.platform or a.match:
        for p in pages.values():
            if a.platform and p["platform"].lower() != a.platform.lower():
                continue
            if a.match and a.match.lower() not in (p["url"] + " " + p["topic_key"]).lower():
                continue
            targets.append(p)
    seen, out = set(), []
    for p in targets:
        if p["url"] in seen:
            continue
        seen.add(p["url"])
        out.append(journal_row(date=a.date or date.today().isoformat(),
                               time="" if a.date else datetime.now().strftime("%H:%M"), event="tag", page_url=p["url"],
                               platform=p["platform"], topic=a.topic, priority=a.priority,
                               position=a.position, offer=a.offer, program=a.program, campaign=a.campaign,
                               main_query=a.query, content_type=a.type, note=a.note))
    if not out:
        sys.exit("No pages matched. Use --url, --urls-file, --platform or --match.")
    append(a.journal, COLUMNS, out)
    what = ", ".join(f"{k} {v}" for k, v in (("topic", a.topic), ("priority", a.priority), ("position", a.position),
                                             ("offer", a.offer), ("program", a.program), ("campaign", a.campaign),
                                             ("query", a.query), ("type", a.type)) if v)
    print(f"Tagged {len(out)} pages: {what or a.note or '—'}")


def page_strength(p, earned):
    """How proven a page's topic is: top position, earning, indexed, priority."""
    sc = 0.0
    if p["position"] is not None and p["position"] <= TOP:
        sc += 3 + (TOP - p["position"]) / TOP
    elif p["position"] is not None and p["position"] <= 20:
        sc += 1.5
    if earned.get(p["url"], [0, 0.0])[1] > 0:
        sc += 3
    if p["ever_indexed"]:
        sc += 1
    if p["priority"] == "high":
        sc += 2
    return sc


def cmd_coverage(a):
    today, rows, pages, sales = load(a)
    reg = read_platforms(platforms_path(a.journal))
    earned = defaultdict(lambda: [0, 0.0])
    for r in sales:
        if r["_page"] and counted(r):
            earned[r["_page"]][0] += 1
            earned[r["_page"]][1] += r["_c"]
    live = [p for p in pages.values() if not p["moved"] and health(p) not in GONE and p["platform"]]
    gone = [p for p in pages.values() if p["moved"] or health(p) in GONE]
    topics = defaultdict(dict)  # topic -> platform -> best page
    for p in live:
        cur = topics[p["topic_key"]].get(p["platform"].lower())
        if cur is None or page_strength(p, earned) > page_strength(cur, earned):
            topics[p["topic_key"]][p["platform"].lower()] = p
    lost = defaultdict(set)
    for p in gone:
        lost[p["topic_key"]].add(p["platform"].lower())
    # platform strength
    st = platform_stats(rows, sales, pages, today)
    plat = {}
    for key in set(st) | set(reg):
        s, r = st[key], reg.get(key, {})
        state = (r.get("state") or "active")
        if state in ("dropped", "dead", "paused"):
            continue
        checked = s["pages"] - s["unchecked"]
        top = sum(1 for p in live if p["platform"].lower() == key and p["position"] is not None and p["position"] <= TOP)
        idx = s["indexed"] / checked if checked else None
        strength = (3 if (r.get("priority") == "high") else 0) + top * 1.5 + (2 * idx if idx is not None else 0.5) \
            + (2 if s["comm"] > 0 else 0) + ((num(r.get("score")) or 0) / 50) - (2 if r.get("priority") == "low" else 0) \
            - (3 * s["gone"] / checked if checked else 0) \
            + (max(0, 11 - num(r.get("rank"))) if num(r.get("rank")) else 0)
        plat[key] = {"name": r.get("platform") or key, "strength": strength, "rank": num(r.get("rank")), "top": top, "idx": idx,
                     "pages": s["pages"], "priority": r.get("priority") or "normal", "state": state,
                     "type": r.get("type") or ""}
    if a.platform:
        plat = {k: v for k, v in plat.items() if k == a.platform.lower()}
    names = sorted(plat, key=lambda k: -plat[k]["strength"])
    tlist = sorted(topics, key=lambda t: (-max(page_strength(p, earned) for p in topics[t].values()), -len(topics[t]), t))
    if a.topic:
        tlist = [t for t in tlist if a.topic.lower() in t]
    print(f"# Topic coverage · {today} · {len(tlist)} topics × {len(names)} platforms\n")
    if not tlist:
        print("No live pages with platforms yet. Import your pages first (import-pages).")
        return
    unnamed = sum(1 for t in tlist if t.startswith("~ "))
    cols = names[: a.max_platforms]
    print("| Topic | " + " | ".join(plat[k]["name"] for k in cols) + " | On |")
    print("|---|" + "---|" * len(cols) + "---|")
    for t in tlist[: a.limit]:
        cells = []
        for k in cols:
            p = topics[t].get(k)
            if p is None:
                cells.append("✗ lost" if k in lost[t] else "·")
            elif p["position"] is not None and p["position"] <= TOP:
                cells.append(f"**#{p['position']:.0f}**")
            elif p["position"] is not None:
                cells.append(f"#{p['position']:.0f}")
            elif health(p) in INDEXED:
                cells.append("✓ idx")
            elif health(p) == "not-indexed":
                cells.append("no idx")
            else:
                cells.append("✓")
        star = " ★" if any(p["priority"] == "high" for p in topics[t].values()) else ""
        print(f"| {t}{star} | " + " | ".join(cells) + f" | {len(topics[t])} |")
    print("\n`#N` position (bold = top 10) · `✓ idx` indexed · `✓` live, not checked · `no idx` not indexed · `✗ lost` page removed · `·` no page · ★ priority")
    if len(names) > len(cols):
        print(f"Showing the {len(cols)} strongest platforms of {len(names)}; --platform P for one.")
    if unnamed:
        print(f"{unnamed} topics are guessed from URLs (marked ~): name them with `tag --topic` so pages on the same subject group together.")

    # gaps: proven topic missing on a strong platform
    gaps = []
    for t in tlist:
        if t.startswith("~ ") and not a.include_guessed:
            continue
        have = topics[t]
        proof = max(page_strength(p, earned) for p in have.values())
        best = max(have.values(), key=lambda p: page_strength(p, earned))
        for k in names:
            if k in have:
                continue
            pl = plat[k]
            if pl["pages"] == 0 and pl["priority"] != "high":
                continue
            score = proof * 1.0 + pl["strength"] + (1 if k in lost[t] else 0)
            why = []
            if best["position"] is not None and best["position"] <= TOP:
                why.append(f"#{best['position']:.0f} on {best['platform']}")
            if earned.get(best["url"], [0, 0])[1] > 0:
                why.append(f"earns on {best['platform']}")
            if best["priority"] == "high":
                why.append("priority topic")
            if pl["top"]:
                why.append(f"{pl['name']} has {pl['top']} pages in the top {TOP}")
            elif pl["idx"] is not None:
                why.append(f"{pl['name']} indexes {pl['idx'] * 100:.0f}%")
            if pl["rank"]:
                why.append(f"{pl['name']} is your #{pl['rank']:.0f} platform")
            elif pl["priority"] == "high":
                why.append(f"{pl['name']} is a priority platform")
            if k in lost[t]:
                why.append("your page there was removed — republish")
            gaps.append((score, t, pl["name"], best, why))
    gaps.sort(key=lambda g: -g[0])
    if a.by_platform:
        print("\n## Missing on each platform (topics you have elsewhere)\n")
        for k in names:
            miss = [(sc, t, best) for sc, t, pname, best, why in gaps if pname == plat[k]["name"]]
            if not miss:
                continue
            rk = f"#{plat[k]['rank']:.0f} " if plat[k]["rank"] else ""
            print(f"**{rk}{plat[k]['name']}** — {len(miss)} topics missing")
            for sc, t, best in miss[: a.gaps]:
                print(f"- {t} (have on {best['platform']})")
            print()
        return
    print(f"\n## What to write where — {min(len(gaps), a.gaps)} best gaps\n")
    if not gaps:
        print("No gaps: every named topic is on every active platform, or topics still need names (tag --topic).")
        return
    for i, (sc, t, pname, best, why) in enumerate(gaps[: a.gaps], 1):
        print(f"{i}. **{t}** → {pname} · from {short(best['url'], 50)}" + (f" — {'; '.join(why)}" if why else ""))
    print("\nRewrite for the new platform, don't copy: new angle or content type, the platform's format. Check the topic's SERP first (content-type-selector).")


RANK_ALIASES = {
    "url": TRAFFIC_ALIASES["url"] + ["rankingurl", "rankingpage", "foundurl", "targeturl", "landingurl", "urlfound"],
    "query": ["keyword", "keywords", "query", "searchterm", "term", "kw"],
    "position": ["position", "rank", "ranking", "currentposition", "currentrank", "pos", "googleposition",
                 "positiontoday", "googlerank", "latestposition", "googleuspos", "serpposition"],
}


def cmd_import_ranks(a):
    """Positions from any rank tracker export (Ubersuggest, SE Ranking, ProRankTracker, Rank Tracker…)."""
    header, raw = sniff_rows(a.export)
    if not raw:
        sys.exit("The export has no data rows.")
    cols = map_columns(header, RANK_ALIASES, parse_map(a.map))
    if "position" not in cols or ("url" not in cols and "query" not in cols):
        print("Columns in the file: " + " | ".join(header))
        sys.exit("Need a position column and a URL or keyword column. Re-run with --map position=\"<header>\" url=\"<header>\".")
    get = lambda r, f: r[cols[f]].strip() if f in cols and cols[f] < len(r) else ""
    d = a.date or date.today().isoformat()
    rows = read_rows(a.journal)
    pages = page_states(rows, date.max)
    by_url = {norm_url(u): p for u, p in pages.items()}
    by_q = defaultdict(list)
    for p in pages.values():
        for q in {p["query"].lower(), p["topic_key"]} - {""}:
            by_q[q].append(p)
    out, unmatched, other_domain = [], [], 0
    for r in raw:
        pos_raw = get(r, "position")
        pos = num(re.sub(r"[^0-9.,]", "", pos_raw)) if pos_raw and pos_raw not in ("-", "—", ">100", "100+") else None
        u, q = get(r, "url"), get(r, "query")
        targets = []
        if u and norm_url(u) in by_url:
            targets = [by_url[norm_url(u)]]
        elif q and q.lower() in by_q:
            cand = by_q[q.lower()]
            if u:  # tracker shows a URL that is not the user's page: someone else ranks, not the user
                dom = url_domain(u)
                targets = [p for p in cand if url_domain(p["url"]) == dom and norm_url(p["url"]) == norm_url(u)]
                if not targets:
                    other_domain += 1
                    continue
            else:
                targets = [p for p in cand if not a.platform or p["platform"].lower() == a.platform.lower()]
        if not targets:
            unmatched.append(u or q)
            continue
        for p in targets:
            note = f"rank: {q or p['query'] or p['topic_key']} · {os.path.basename(a.export)}"
            if pos is not None and pos > 0:
                out.append(journal_row(date=d, time="", event="check", page_url=p["url"], platform=p["platform"],
                                       status="indexed", position=f"{pos:.0f}", main_query=q, note=note))
            else:
                out.append(journal_row(date=d, time="", event="check", page_url=p["url"], platform=p["platform"],
                                       main_query=q, note=note + " · not in top 100"))
    if out:
        append(a.journal, COLUMNS, out)
    top = sum(1 for r in out if num(r["position"]) is not None and num(r["position"]) <= TOP)
    print(f"Rank import {os.path.basename(a.export)} · {d}")
    print("- Columns used: " + ", ".join(f"{f} = “{header[i]}”" for f, i in cols.items()))
    print(f"- {len(out)} page positions logged · {top} in the top {TOP}")
    if other_domain:
        print(f"- {other_domain} rows show another page of the same platform ranking, not yours: skipped")
    if unmatched:
        print(f"- {len(unmatched)} rows not matched to your pages: " + ", ".join(short(x, 40) for x in unmatched[:10]))


def cmd_ideas(a):
    """Topics for the user's own plan: what to publish on the target platforms today.
    --to: target platforms (may be new, not yet in the base); --from: only topics proven there;
    --top-only: only topics with a page in the top 10."""
    today, rows, pages, sales = load(a)
    reg = read_platforms(platforms_path(a.journal))
    earned = defaultdict(float)
    for r in sales:
        if r["_page"] and counted(r):
            earned[r["_page"]] += r["_c"]
    src = {x.strip().lower() for x in (a.from_ or "").split(",") if x.strip()}
    if src:  # accept types too: "own-site" = every platform of that type
        src |= {k for k, r in reg.items() if (r.get("type") or "").lower() in src}
    live = [p for p in pages.values() if p["platform"] and not p["moved"] and health(p) not in GONE]
    topics = defaultdict(list)
    for p in live:
        topics[p["topic_key"]].append(p)
    targets = [x.strip() for x in a.to.split(",") if x.strip()]
    print(f"# Topics for your plan · {today}\n")
    for tgt in targets:
        key = tgt.lower()
        r = reg.get(key)
        state = (r or {}).get("state") or ("new — not in your base" if not r else "active")
        have = {t for t, ps in topics.items() if any(p["platform"].lower() == key for p in ps)}
        cands = []
        for t, ps in topics.items():
            if t in have or (t.startswith("~ ") and not a.include_guessed):
                continue
            pool = [p for p in ps if p["platform"].lower() != key and (not src or p["platform"].lower() in src)]
            if a.top_only:
                pool = [p for p in pool if p["position"] is not None and p["position"] <= TOP]
            if not pool:
                continue
            best = max(pool, key=lambda p: page_strength(p, {u: [1, c] for u, c in earned.items()}))
            nplat = len({p["platform"].lower() for p in ps})
            sc = page_strength(best, {u: [1, c] for u, c in earned.items()}) + 0.3 * nplat
            why = []
            if best["position"] is not None:
                why.append(f"#{best['position']:.0f} on {best['platform']}")
            if earned.get(best["url"]):
                why.append(f"earns {money(earned[best['url']])}")
            if best["priority"] == "high":
                why.append("★")
            if nplat > 1:
                why.append(f"on {nplat} platforms")
            cands.append((sc, t, best, why))
        cands.sort(key=lambda c: -c[0])
        print(f"## {tgt} · {state} · {len(have)} of your topics already there\n")
        if not cands:
            print("No topics to add" + (" from those sources" if src else "") + (" with a top-10 page" if a.top_only else "")
                  + ". " + ("Positions unknown yet: run the position check, or drop --top-only." if a.top_only else "") + "\n")
            continue
        for i, (sc, t, best, why) in enumerate(cands[: a.n], 1):
            print(f"{i}. **{t}** — from {short(best['url'], 55)}" + (f" ({'; '.join(why)})" if why else ""))
        if len(cands) > a.n:
            print(f"… {len(cands) - a.n} more (--n {len(cands)})")
        if not r:
            print(f"\n{tgt} is new: check it once with platform-analyzer before the first post.")
        print()


LINK_COLUMNS = ["program", "product", "link", "alt_links", "commission", "added", "note"]
LINK_ALIASES = {
    "link": ["link", "url", "affiliatelink", "shortenedlink", "shortlink", "trackinglink", "referrallink", "afflink"],
    "product": ["product", "productname", "name", "offer", "item", "title"],
    "program": ["program", "network", "brand", "merchant", "advertiser"],
    "commission": ["commission", "rate", "payout", "commissionrate"],
    "note": ["note", "notes", "comment"],
}
STORE_PAGES = {"faq", "all-products", "main-page", "home", "shop", "products", "collections", "about", "contact",
               "herbal", "minerals", "daily-vitamins", "blog", "cart"}


def links_path(journal):
    return os.path.join(os.path.dirname(os.path.abspath(journal)), "parasite-seo-links.csv")


def product_from_link(url):
    path = re.sub(r"^[a-z]+://[^/]+", "", (url or "").lower()).split("?")[0].strip("/")
    seg = path.split("/")[-1] if path else ""
    if seg in STORE_PAGES or not seg:
        return "", True
    words = [x for x in re.split(r"[^a-z0-9]+", seg) if x and x not in ("usda", "organic", "supplement", "supplements", "products", "p", "go", "ref")]
    return " ".join(words), False


def cmd_import_links(a):
    """The user's affiliate links library: one row per product, from any list, table or pasted text."""
    text, loose = urls_from_text(a.file)
    header, raw = ([], [])
    if max(text[:3000].count(","), text[:3000].count(";"), text[:3000].count("\t")) > 0:
        header, raw = sniff_rows(a.file)
    cols = map_columns(header, LINK_ALIASES, parse_map(a.map)) if header else {}
    get = lambda r, f: r[cols[f]].strip() if f in cols and cols[f] < len(r) else ""
    items = []
    if "link" in cols:
        for r in raw:
            if re.match(r"https?://", get(r, "link")):
                items.append({f: get(r, f) for f in cols})
    else:
        items = [{"link": u.rstrip(".,")} for u in loose]
    if not items:
        sys.exit("No links found. Give a list of affiliate links (one per line), a table with a link column, or paste them.")
    path = links_path(a.journal)
    have = {norm_url(r["link"]): r for r in read_csv(path)}
    rows = list(have.values())
    added, dup, store = 0, 0, 0
    for it in items:
        k = norm_url(it["link"])
        if k in have:
            dup += 1
            continue
        prod, is_store = product_from_link(it["link"])
        prod = it.get("product") or prod
        if is_store and not it.get("product"):
            store += 1
            prod = "(store page) " + (re.sub(r"^[a-z]+://[^/]+/?", "", it["link"]).strip("/") or "home")
        r = {"program": it.get("program") or a.program or url_domain(it["link"]), "product": prod, "link": it["link"],
             "alt_links": "", "commission": it.get("commission") or a.commission or "",
             "added": date.today().isoformat(), "note": it.get("note") or ""}
        have[k] = r
        rows.append(r)
        added += 1
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=LINK_COLUMNS, extrasaction="ignore")
        wr.writeheader()
        for r in sorted(rows, key=lambda r: (r["program"].lower(), r["product"].startswith("("), r["product"])):
            wr.writerow(r)
    progs = Counter(r["program"] for r in rows)
    print(f"Links library {os.path.basename(path)}: {added} added · {dup} already there · {store} store/category pages")
    print("- Programs: " + ", ".join(f"{k} {v}" for k, v in progs.most_common()))
    print("- Products are named from the link; rename any with a table that has a product column, or edit the file.")
    print("- Next: `links` shows which products have no pages yet — your topics to write.")


def cmd_links(a):
    today, rows, pages, sales = load(a)
    lib = read_csv(links_path(a.journal))
    if a.program:
        lib = [r for r in lib if r["program"].lower() == a.program.lower()]
    if not lib:
        sys.exit("No affiliate links yet. Import them: import-links <file> --program <name> [--commission 40%].")
    live = [p for p in pages.values() if not p["moved"] and health(p) not in GONE]

    def words(x):
        return {w for w in re.split(r"[^a-z0-9]+", (x or "").lower())
                if (len(w) > 2 or re.search(r"\d", w)) and w not in STOP and w not in
                ("supplement", "supplements", "capsules", "drops", "liquid", "gummies", "softgels", "spray",
                 "best", "usda", "organic", "extract", "support")}

    def covers(page, link_words):
        pw = words(page["topic_key"] + " " + page["offer"] + " " + page["url"])
        need = min(2, len(link_words))
        return need > 0 and len(link_words & pw) >= need
    groups = defaultdict(list)
    for r in lib:
        if r["product"].startswith("("):
            continue
        groups[(r["program"], r["product"])].append(r)
    print(f"# Affiliate links · {len(lib)} links · {len(groups)} products\n")
    print("| Program | Product | Link | Pages | Platforms |")
    print("|---|---|---|---|---|")
    missing = []
    for (prog, prod), rs in sorted(groups.items()):
        lws = [words(product_from_link(r["link"])[0]) for r in rs]
        hit = [p for p in live if any(covers(p, lw) for lw in lws)]
        plats = sorted({p["platform"] for p in hit})
        if not hit:
            missing.append((prog, prod))
        print(f"| {prog} | {prod} | {short(rs[0]['link'], 45)} | {len(hit) or '—'} | {', '.join(plats) or '—'} |")
    if missing:
        print(f"\n**No pages yet for {len(missing)} products** — topics to write: " + ", ".join(p for _, p in missing))
        print("Use `ideas` / coverage to pick the platform; the writer takes the link from this library.")


FORMATS = {"book": "long chapter (2,000–3,500 words), full structure", "document": "analytical review document, clearly a buyer's comparison",
           "forum": "native forum thread + 2–5 own replies, unique title", "community": "community post, ends with a question",
           "podcast": "episode: description 800–1,500 words + short script", "presentation": "visual guide in 8–15 cards",
           "article": "blog article 1,500–2,000+ words", "blog": "blog post 1,500+ words", "q&a": "answer to a real question",
           "page": "single page article", "site-builder": "page article", "newsletter": "newsletter post"}


def cmd_rollout(a):
    """Where to publish a topic next: the user's active platforms that don't have it yet."""
    today, rows, pages, sales = load(a)
    reg = read_platforms(platforms_path(a.journal))
    topic = (a.topic or "").lower()
    if a.url:
        p = next((p for u, p in pages.items() if norm_url(u) == norm_url(a.url)), None)
        if not p:
            sys.exit("That page is not in the journal: log it first (add --event published).")
        topic = p["topic_key"]
    if not topic:
        sys.exit("Give --topic or --url.")
    on = defaultdict(list)
    for p in pages.values():
        if topic in p["topic_key"] and not p["moved"] and health(p) not in GONE:
            on[p["platform"].lower()].append(p)
    rank = lambda r: (num(r.get("rank")) or 99, PRIORITIES.index(r.get("priority") or "normal"), r["platform"])
    act = [r for r in reg.values() if (r.get("state") or "active") in ("active", "testing")]
    used = Counter(p["platform"].lower() for p in pages.values())
    missing = [r for r in sorted(act, key=rank) if r["platform"].lower() not in on
               and "mirror" not in (r.get("note") or "").lower()          # syndicated copies (Spotify ← Audioboom)
               and (used[r["platform"].lower()] or r.get("priority") == "high")]  # platforms the user actually publishes on
    print(f"# Rollout · “{topic}” · on {len(on)} platforms · missing on {len(missing)}\n")
    if on:
        print("**Already there:** " + ", ".join(f"{k} ({len(v)})" + (f" #{min(p['position'] for p in v if p['position']):.0f}" if any(p['position'] for p in v) else "") for k, v in on.items()))
    if missing:
        print("\n| Platform | Priority | Type | Format for this platform |\n|---|---|---|---|")
        for r in missing:
            prio = {"high": "★"}.get(r.get("priority") or "", "")
            print(f"| {r['platform']} | {prio} | {r.get('type') or '?'} | {FORMATS.get((r.get('type') or '').lower(), 'check the platform format')} |")
        print("\nEach version: new title and angle, the platform's format, same verified facts and your links. Never a copy.")


# ---------- sources: the user's own worked texts, kept to republish ----------

def sources_dir(journal):
    return os.path.join(os.path.dirname(os.path.abspath(journal)), "parasite-seo-sources")


def page_sources(rows):
    """page url -> latest saved source (relative path)."""
    out = {}
    for r in rows:
        if r["event"] == "source" and r.get("page_url"):
            note = r.get("note") or ""
            if note.startswith("source: "):
                out[r["page_url"]] = note[len("source: "):].split(" · ")[0]
    return out


def cmd_source(a):
    """Save the source of a published page (the user's own .docx / .md / .txt) next to the journal."""
    import shutil
    rows = read_rows(a.journal)
    pages = page_states(rows, date.today())
    page = next((u for u in pages if norm_url(u) == norm_url(a.url)), None)
    if not page:
        sys.exit("That page is not in the journal: log it first (add --event published --url …).")
    if not (a.file or a.text_file):
        sys.exit("Give --file (the .docx / .md / .txt the user worked on).")
    src = a.file or a.text_file
    if not os.path.exists(src):
        sys.exit(f"File not found: {src}")
    d = sources_dir(a.journal)
    os.makedirs(d, exist_ok=True)
    plat = pages[page]["platform"] or platform_of(page)[0]
    base = re.sub(r"[^a-z0-9]+", "-", " ".join(list(slug_words(page))[:6]).lower()).strip("-") or "page"
    ext = os.path.splitext(src)[1].lower() or ".txt"
    name = f"{date.today().isoformat()}-{plat}-{base}{ext}"
    shutil.copyfile(src, os.path.join(d, name))
    rel = f"parasite-seo-sources/{name}"
    append(a.journal, COLUMNS, [journal_row(date=a.date or date.today().isoformat(), event="source", page_url=page,
                                            platform=plat, note=f"source: {rel}" + (f" · {a.note}" if a.note else ""))])
    print(f"Saved the source of {short(page)} → {rel}. If the page is removed, `republish --url` brings it back.")


def cmd_republish(a):
    """Pages to bring back after a removal or a platform cleanup, with their saved sources."""
    today, rows, pages, sales = load(a)
    srcs = page_sources(rows)
    if a.url:
        items = [p for u, p in pages.items() if norm_url(u) == norm_url(a.url)]
    else:
        pl = (a.platform or "").lower()
        if not pl:
            sys.exit("Give --platform or --url.")
        items = [p for p in pages.values() if (p["platform"] or platform_of(p["url"])[0]).lower() == pl and not p["moved"]]
        if a.gone_only:
            items = [p for p in items if health(p) in GONE]
    if not items:
        print("No pages found for that platform or URL in the journal.")
        return
    earned = defaultdict(float)
    for r in sales:
        if r["_page"] and counted(r):
            earned[r["_page"]] += r["_c"]
    items.sort(key=lambda p: (PRIORITIES.index(p["priority"]), -earned[p["url"]], p["position"] or 999))
    with_src = sum(1 for p in items if p["url"] in srcs)
    print(f"# Republish · {a.platform or short(a.url)} · {len(items)} pages · {with_src} with a saved source\n")
    print("| Page | Status | Topic | Offer | Pos. | Earned | Source |")
    print("|---|---|---|---|---|---|---|")
    for p in items:
        print(f"| {short(p['url'], 50)} | {health(p)} | {p['topic_key']} | {p['offer'] or ''} | "
              f"{p['position'] or ''} | {fmt(earned[p['url']]) if earned[p['url']] else ''} | {srcs.get(p['url'], 'none')} |")
    print("\nOrder: ★ and earning pages first. With a source: rewrite it for the new platform (new title and angle, "
          "the platform's format, current prices). Without one: rebuild from the topic and the facts box — "
          "an AI draft is quicker to write again than to recover. Pick the new home with `rollout --url` or platform-finder.")


def main():
    ap = argparse.ArgumentParser(description="PARASITER work, traffic and sales journal")
    ap.add_argument("--sales-file", help="sales file (default: parasite-seo-sales.csv next to the journal)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p, today=True):
        p.add_argument("journal")
        p.add_argument("--sales-file", default=argparse.SUPPRESS)
        if today:
            p.add_argument("--today")

    s = sub.add_parser("summary"); common(s)
    s.add_argument("--period", default="today"); s.set_defaults(fn=cmd_summary)

    ef = sub.add_parser("effect"); common(ef)
    ef.add_argument("--period", default="month"); ef.add_argument("--currency")
    ef.add_argument("--by", default="page",
                    choices=["page", "platform", "offer", "program", "campaign", "content_type", "month"])
    ef.set_defaults(fn=cmd_effect)

    d = sub.add_parser("due"); common(d); d.set_defaults(fn=cmd_due)

    p = sub.add_parser("pages"); common(p)
    p.add_argument("--platform"); p.add_argument("--topic")
    p.add_argument("--priority", choices=PRIORITIES); p.set_defaults(fn=cmd_pages)

    ad = sub.add_parser("add"); common(ad, today=False)
    ad.add_argument("--event", required=True, choices=EVENTS)
    for opt in ("url", "platform", "offer", "program", "campaign", "sub-id", "query", "type", "status",
                "score", "views", "clicks", "aff-clicks", "sales", "revenue", "minutes",
                "note", "date", "time", "topic", "position",
                "link-target", "link-rel", "anchor", "cost"):
        ad.add_argument(f"--{opt}")
    ad.add_argument("--priority", choices=PRIORITIES)
    ad.set_defaults(fn=cmd_add)

    sa = sub.add_parser("sale"); common(sa, today=False)
    sa.add_argument("--program", required=True)
    sa.add_argument("--commission", required=True)
    for opt in ("amount", "currency", "sub-id", "url", "offer", "order-id", "status",
                "network", "date", "note"):
        sa.add_argument(f"--{opt}")
    sa.set_defaults(fn=cmd_sale)

    im = sub.add_parser("import-sales"); common(im, today=False)
    im.add_argument("export")
    im.add_argument("--program", required=True)
    im.add_argument("--network"); im.add_argument("--currency")
    im.add_argument("--map", action="append", help="field=Header, e.g. sub_id=\"Tracking ID\"")
    im.add_argument("--date-format", help="strptime format if dates are not detected, e.g. %%d/%%m/%%Y")
    im.set_defaults(fn=cmd_import_sales)

    it = sub.add_parser("import-traffic"); common(it, today=False)
    it.add_argument("export")
    it.add_argument("--platform")
    it.add_argument("--from", dest="from_"); it.add_argument("--to")
    it.add_argument("--map", action="append")
    it.add_argument("--medium", help="count only rows whose source / medium has this medium, e.g. parasite")
    it.set_defaults(fn=cmd_import_traffic)

    sr = sub.add_parser("site-roi"); common(sr)
    sr.add_argument("--period", default="month"); sr.add_argument("--by", default="platform", choices=["platform", "page"])
    sr.set_defaults(fn=cmd_site_roi)

    ip = sub.add_parser("import-pages"); common(ip, today=False)
    ip.add_argument("file")
    for opt in ("date", "platform", "offer", "program", "campaign", "type"):
        ip.add_argument(f"--{opt}")
    ip.add_argument("--map", action="append")
    ip.set_defaults(fn=cmd_import_pages)

    pl = sub.add_parser("platforms"); common(pl); pl.set_defaults(fn=cmd_platforms)

    ir = sub.add_parser("import-ranks"); common(ir, today=False)
    ir.add_argument("export"); ir.add_argument("--platform"); ir.add_argument("--date")
    ir.add_argument("--map", action="append")
    ir.set_defaults(fn=cmd_import_ranks)

    so = sub.add_parser("source"); common(so, today=False)
    so.add_argument("--url", required=True); so.add_argument("--file"); so.add_argument("--text-file")
    so.add_argument("--date"); so.add_argument("--note"); so.set_defaults(fn=cmd_source)
    rp = sub.add_parser("republish"); common(rp)
    rp.add_argument("--platform"); rp.add_argument("--url"); rp.add_argument("--gone-only", action="store_true")
    rp.set_defaults(fn=cmd_republish)
    ro = sub.add_parser("rollout"); common(ro); ro.add_argument("--topic"); ro.add_argument("--url"); ro.set_defaults(fn=cmd_rollout)

    il = sub.add_parser("import-links"); common(il, today=False)
    il.add_argument("file"); il.add_argument("--program"); il.add_argument("--commission")
    il.add_argument("--map", action="append"); il.set_defaults(fn=cmd_import_links)

    lk = sub.add_parser("links"); common(lk); lk.add_argument("--program"); lk.set_defaults(fn=cmd_links)

    bl = sub.add_parser("backlinks"); common(bl)
    bl.add_argument("--period", default="all"); bl.add_argument("--target"); bl.set_defaults(fn=cmd_backlinks)

    tg = sub.add_parser("tag"); common(tg, today=False)
    tg.add_argument("--url", action="append")
    tg.add_argument("--urls-file")
    tg.add_argument("--platform"); tg.add_argument("--match", help="substring of URL or topic")
    for opt in ("topic", "position", "offer", "program", "campaign", "query", "type", "note", "date"):
        tg.add_argument(f"--{opt}")
    tg.add_argument("--priority", choices=PRIORITIES)
    tg.set_defaults(fn=cmd_tag)

    idp = sub.add_parser("ideas"); common(idp)
    idp.add_argument("--to", required=True, help="target platforms, comma-separated (new ones allowed)")
    idp.add_argument("--from", dest="from_", help="source platforms or types (own-site), comma-separated")
    idp.add_argument("--top-only", action="store_true", help="only topics with a page in the top 10")
    idp.add_argument("--n", type=int, default=8)
    idp.add_argument("--include-guessed", action="store_true")
    idp.set_defaults(fn=cmd_ideas)

    cv = sub.add_parser("coverage"); common(cv)
    cv.add_argument("--topic"); cv.add_argument("--platform")
    cv.add_argument("--limit", type=int, default=40)
    cv.add_argument("--gaps", type=int, default=10)
    cv.add_argument("--max-platforms", type=int, default=8)
    cv.add_argument("--include-guessed", action="store_true")
    cv.add_argument("--by-platform", action="store_true", help="list missing topics per platform")
    cv.set_defaults(fn=cmd_coverage)

    ps = sub.add_parser("platform-set"); common(ps, today=False)
    ps.add_argument("--platform", required=True)
    for opt in ("domain", "type", "language", "links", "account", "score", "note"):
        ps.add_argument(f"--{opt}")
    ps.add_argument("--state", choices=["active", "testing", "paused", "dropped", "dead"])
    ps.add_argument("--priority", choices=PRIORITIES)
    ps.add_argument("--rank", help="your own order of platforms: 1 = best")
    ps.set_defaults(fn=cmd_platform_set)

    a = ap.parse_args()
    a.sales_path_override = getattr(a, "sales_file", None)
    a.fn(a)


if __name__ == "__main__":
    main()
