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

Periods: today, yesterday, week, last-week, month, last-month, YYYY-MM, YYYY-MM-DD,
YYYY-MM-DD..YYYY-MM-DD, all.  --sales-file FILE overrides the sales file path.
Formats: references/log-format.md, references/sales-import.md. Standard library only.
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
           "sales", "revenue", "minutes", "note"]
SALE_COLUMNS = ["date", "program", "network", "offer", "sub_id", "page_url", "order_id",
                "amount", "commission", "currency", "status", "source", "note"]
EVENTS = ["baseline", "published", "submitted", "check", "audit", "refreshed", "moved",
          "platform", "traffic", "stats", "import", "task", "note"]
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
          "note": "notes", "baseline": "baseline"}

# column aliases for exports (compared after normalising: lowercase, letters/digits only)
SALE_ALIASES = {
    "date": ["date", "transactiondate", "saledate", "orderdate", "conversiondate", "eventdate",
             "actiondate", "createdat", "created", "datetime", "time", "clickdate",
             "transactiontime", "dateofsale", "lockingdate"],
    "order_id": ["orderid", "transactionid", "receipt", "receiptno", "actionid", "ordernumber",
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
               "tag", "s1", "label", "subaffiliateid", "trackingtag"],
    "status": ["status", "actionstatus", "state", "commissionstatus", "transactionstatus",
               "paymentstatus", "approvalstatus", "type", "transactiontype"],
    "offer": ["product", "productname", "offer", "offername", "item", "itemname", "brand",
              "advertiser", "advertisername", "merchant", "merchantname", "campaign",
              "campaignname", "productid"],
    "currency": ["currency", "currencycode", "commissioncurrency"],
}
TRAFFIC_ALIASES = {
    "url": ["url", "link", "page", "pageurl", "posturl", "landingpage", "address", "permalink",
            "story", "storyurl", "articleurl"],
    "sub_id": SALE_ALIASES["sub_id"],
    "views": ["views", "pageviews", "reads", "visits", "sessions", "impressions", "uniqueviews",
              "viewcount", "totalviews", "hits", "visitors", "plays"],
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


def norm_url(u):
    u = (u or "").strip().lower()
    u = re.sub(r"^https?://", "", u)
    u = re.sub(r"^www\.", "", u)
    u = u.split("#")[0].split("?")[0]
    return u.rstrip("/")


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
                                   "last_refresh": None, "moved": None, "first": r["_d"]})
        for k, col in (("platform", "platform"), ("offer", "offer"), ("program", "program"),
                       ("campaign", "campaign"),
                       ("sub_id", "sub_id"), ("query", "main_query"),
                       ("content_type", "content_type")):
            if not p[k] and r.get(col):
                p[k] = r[col]
        ev, st = r["event"], r["status"]
        if ev == "published" and p["published"] is None:
            p["published"] = r["_d"]
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
    return pages


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


def period_range(period, today, rows):
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
        start = rows[0]["_d"] if rows else today
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
                 if p["published"] <= r["_d"] and not (p["moved"] and p["moved"] < r["_d"])
                 and ((prog and (p["program"] or "").lower() == prog)
                      or (not prog and off and (p["offer"] or "").lower() == off))]
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
    if limit:
        out = out[:limit]
    head = "Page" if by == "page" else by.replace("_", " ").title()
    has_est = any(g["est"] for g in groups.values())
    if has_est:
        print(f"| {head} | Pages | Views | Aff. clicks | Sales (exact) | Commission (exact) | + Estimated share | Total with estimate | Pending | EPC* | Per page* | Per 1k views* |")
        print("|---|---|---|---|---|---|---|---|---|---|---|---|")
        out.sort(key=lambda x: (-(x[2] + (0 if x[1].get("est_mark") else x[1]["est"].get(cur, 0))),
                                -x[1]["views"], str(x[0])))
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
    sel = [r for r in rows if s <= r["_d"] <= e]
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
    s, e, label = period_range(a.period, today, rows)
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
    s, e, label = period_range(a.period, today, rows)
    groups = effect_table(rows, sales, pages, s, e, a.by)
    groups = {k: g for k, g in groups.items()
              if g["pages"] or g["views"] or g["aff_clicks"] or g["commission"] or g["reversed"]
              or g["stats_rev"]}
    print(f"# Effectiveness by {a.by.replace('_', ' ')} · {label} · {s} – {e}\n")
    if not groups:
        print("No pages, traffic or sales in this period.")
        return
    cur = main_currency(groups)
    print_effect(groups, a.by, cur)
    tot, pend, n, rev_n, unattr = money_totals(sales, s, e)
    live = sum(1 for p in pages.values() if p["published"] <= e and not p["moved"]
               and p["status"] not in GONE)
    print(f"\n**Total:** {n} sales · {money(tot.get(cur, 0), cur)} commission"
          f" · {live} pages alive or unchecked at period end"
          + (f" · {money(tot.get(cur, 0) / live, cur)} per page" if live else ""))
    if n:
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
        for p, why in sorted(items, key=lambda x: x[0]["published"]):
            q = f" · “{p['query']}”" if p["query"] else ""
            print(f"- {short(p['url'])} · {p['platform'] or '?'} · {p['age']} d{q} — {why}")
        print()


def cmd_pages(a):
    today, rows, pages, sales = load(a)
    items = [p for p in pages.values() if not a.platform or p["platform"] == a.platform]
    items.sort(key=lambda p: p["published"], reverse=True)
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
    print("| Published | Page | Platform | Offer | Sub-ID | Age | Status | Audit | Views | Aff. clicks | Sales | Commission |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    hc = Counter()
    for p in items:
        h = health(p)
        hc[h] += 1
        n, c = earned[p["url"]]
        v, ac = traffic[p["url"]]
        print(f"| {p['published']} | {short(p['url'], 45)} | {p['platform']} | {p['offer']} | "
              f"{p['sub_id'] or '—'} | {p['age']} d | {h} | {fmt(p['score'])} | "
              f"{fmt(v) if v else '—'} | {fmt(ac) if ac else '—'} | {n} | {money(c)} |")
    print("\n**Status:** " + " · ".join(f"{k} {v}" for k, v in hc.most_common()))


def cmd_add(a):
    row = journal_row(event=a.event, page_url=a.url, platform=a.platform, offer=a.offer,
                      program=a.program, campaign=a.campaign, sub_id=a.sub_id, main_query=a.query,
                      content_type=a.type, status=a.status, score=a.score, views=a.views,
                      clicks=a.clicks, aff_clicks=a.aff_clicks, sales=a.sales,
                      revenue=a.revenue, minutes=a.minutes, note=a.note)
    if a.date:
        row["date"] = a.date
    if a.time:
        row["time"] = a.time
    if not pdate(row["date"]):
        sys.exit("--date must be YYYY-MM-DD")
    append(a.journal, COLUMNS, [row])
    print(f"Logged: {row['date']} {row['event']} {row['page_url'] or row['note']}".strip())


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
        n = max(ln.count(","), ln.count(";"), ln.count("\t"))
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
               "source": f"import:{os.path.basename(a.export)}", "note": ""}
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


def cmd_import_traffic(a):
    header, raw = sniff_rows(a.export)
    if not raw:
        sys.exit("The export has no data rows.")
    cols = map_columns(header, TRAFFIC_ALIASES, parse_map(a.map))
    if "url" not in cols and "sub_id" not in cols:
        print("Columns in the file: " + " | ".join(header))
        sys.exit("No page URL or sub-ID column found. Re-run with --map url=\"<header>\".")
    if "views" not in cols and "aff_clicks" not in cols:
        print("Columns in the file: " + " | ".join(header))
        sys.exit("No views or clicks column found. Re-run with --map views=\"<header>\".")
    get = lambda r, f: r[cols[f]].strip() if f in cols and cols[f] < len(r) else ""
    today = date.today()
    end = pdate(a.to) if a.to else today
    start = pdate(a.from_) if a.from_ else None
    period = f"{start or '?'}..{end}"
    rows = read_rows(a.journal)
    pages = page_states(rows, end)
    by_sub, by_url = lookups(pages)
    seen = {(r.get("page_url"), r.get("note")) for r in rows if r["event"] == "traffic"}

    totals = defaultdict(lambda: [0.0, 0.0])
    unmatched = Counter()
    for r in raw:
        url = ""
        if "url" in cols:
            url = by_url.get(norm_url(get(r, "url")), "")
        if not url and "sub_id" in cols:
            url = by_sub.get(get(r, "sub_id").lower(), "")
        v, c = num(get(r, "views")) or 0, num(get(r, "aff_clicks")) or 0
        if not url:
            if v or c:
                unmatched[get(r, "url") or get(r, "sub_id")] += v + c
            continue
        totals[url][0] += v
        totals[url][1] += c
    out, skipped = [], 0
    for url, (v, c) in totals.items():
        note = f"traffic {period} from {os.path.basename(a.export)}"
        if (url, note) in seen or any(n.startswith(f"traffic {period}") for u, n in seen if u == url):
            skipped += 1
            continue
        p = pages[url]
        out.append(journal_row(date=end.isoformat(), event="traffic", page_url=url,
                               platform=a.platform or p["platform"], offer=p["offer"],
                               views=fmt(v) if v else "", aff_clicks=fmt(c) if c else "",
                               note=note))
    if out:
        append(a.journal, COLUMNS, out)
    print(f"Traffic import {os.path.basename(a.export)} · period {period}")
    print(f"- Columns used: " + ", ".join(f"{f} = “{header[i]}”" for f, i in cols.items()))
    print(f"- {len(out)} pages updated · {skipped} already imported for this period")
    if unmatched:
        print(f"- {len(unmatched)} rows not in the journal (not your logged pages or not published yet): "
              + ", ".join(short(k, 40) for k, _ in unmatched.most_common(10)))
    if not a.from_:
        print("- Tip: pass --from and --to with the export's date range so the same period is never counted twice.")


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
    ef.add_argument("--period", default="month")
    ef.add_argument("--by", default="page",
                    choices=["page", "platform", "offer", "program", "campaign", "content_type", "month"])
    ef.set_defaults(fn=cmd_effect)

    d = sub.add_parser("due"); common(d); d.set_defaults(fn=cmd_due)

    p = sub.add_parser("pages"); common(p)
    p.add_argument("--platform"); p.set_defaults(fn=cmd_pages)

    ad = sub.add_parser("add"); common(ad, today=False)
    ad.add_argument("--event", required=True, choices=EVENTS)
    for opt in ("url", "platform", "offer", "program", "campaign", "sub-id", "query", "type", "status",
                "score", "views", "clicks", "aff-clicks", "sales", "revenue", "minutes",
                "note", "date", "time"):
        ad.add_argument(f"--{opt}")
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
    it.set_defaults(fn=cmd_import_traffic)

    a = ap.parse_args()
    a.sales_path_override = getattr(a, "sales_file", None)
    a.fn(a)


if __name__ == "__main__":
    main()
