#!/usr/bin/env python3
"""PARASITER — work journal: log work, report any period, list pages due for checks.

Usage:
  worklog.py add     JOURNAL.csv --event published --url URL [--platform P] [--offer O]
                     [--query Q] [--type T] [--status S] [--score N] [--clicks N]
                     [--sales N] [--revenue N] [--minutes N] [--note TEXT]
                     [--date YYYY-MM-DD] [--time HH:MM]
  worklog.py summary JOURNAL.csv [--period today|yesterday|week|last-week|month|
                     last-month|YYYY-MM|YYYY-MM-DD|YYYY-MM-DD..YYYY-MM-DD|all] [--today D]
  worklog.py due     JOURNAL.csv [--today D]
  worklog.py pages   JOURNAL.csv [--platform P] [--today D]

Journal format: references/log-format.md. Reads older, shorter headers too.
Standard library only. Output is Markdown.
"""
import argparse
import csv
import os
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta

COLUMNS = ["date", "time", "event", "page_url", "platform", "offer", "main_query",
           "content_type", "status", "score", "clicks", "sales", "revenue", "minutes", "note"]
EVENTS = ["baseline", "published", "submitted", "check", "audit", "refreshed", "moved",
          "platform", "stats", "task", "note"]
ALIVE = {"live", "indexed", "not-indexed", "dropped"}
INDEXED = {"indexed", "dropped"}
GONE = {"removed", "dead", "noindex"}
CHECK_POINTS = [2, 7, 14]
CHECK_EVERY = 14
RECHECK_NOT_INDEXED = 3
AUDIT_POINTS = [14, 30, 60]
AUDIT_MIN = 70
LABELS = {"published": "published", "submitted": "sent to indexing", "check": "checks",
          "audit": "audits", "refreshed": "refreshed", "moved": "moved",
          "platform": "platforms tested", "stats": "stats entries", "task": "other tasks",
          "note": "notes", "baseline": "baseline"}


# ---------- reading ----------

def num(v):
    try:
        return float(str(v).replace(",", "").replace("$", "").strip())
    except (TypeError, ValueError):
        return None


def pdate(v):
    try:
        return datetime.strptime(str(v).strip()[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def read_rows(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = []
        for i, r in enumerate(csv.DictReader(f)):
            r = {k.strip(): (v or "").strip() for k, v in r.items() if k}
            r["_d"] = pdate(r.get("date", ""))
            r["_i"] = i
            r["event"] = r.get("event", "").lower()
            r["status"] = r.get("status", "").lower()
            if r["_d"]:
                rows.append(r)
    rows.sort(key=lambda r: (r["_d"], r.get("time", ""), r["_i"]))
    return rows


# ---------- page state ----------

def page_states(rows, today):
    pages = {}
    for r in rows:
        url = r.get("page_url", "")
        if not url or r["_d"] > today:
            continue
        p = pages.setdefault(url, {"url": url, "platform": "", "offer": "", "query": "",
                                   "published": None, "last_check": None, "status": "",
                                   "ever_indexed": False, "last_audit": None, "score": None,
                                   "last_refresh": None, "moved": None, "sales": 0.0,
                                   "revenue": 0.0, "first": r["_d"]})
        for k, col in (("platform", "platform"), ("offer", "offer"), ("query", "main_query")):
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
        elif ev == "stats":
            p["sales"] += num(r.get("sales")) or 0
            p["revenue"] += num(r.get("revenue")) or 0
    for p in pages.values():
        if p["published"] is None:
            p["published"] = p["first"]
        p["age"] = (today - p["published"]).days
    return pages


def health(p):
    if p["moved"]:
        return "moved"
    if not p["last_check"]:
        return "not checked yet"
    return p["status"]


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
        point = p["published"] + timedelta(days=d)
        if p["age"] >= d and p["last_audit"] < point:
            return f"{d}-day review"
    return None


def due_lists(pages, today):
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
    return out


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
        if not rows:
            return today, today, "all time"
        return rows[0]["_d"], max(today, rows[-1]["_d"]), "all time"
    if ".." in p:
        a, b = p.split("..", 1)
        s, e = pdate(a), pdate(b)
        if s and e:
            return s, e, "range"
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
    length = (end - start).days + 1
    if p == "week":
        length = 7
    return start - timedelta(days=length), start - timedelta(days=1)


# ---------- commands ----------

def fmt(v):
    if v is None:
        return "—"
    return f"{v:,.0f}" if float(v).is_integer() else f"{v:,.2f}"


def short(url, n=60):
    u = url.replace("https://", "").replace("http://", "")
    return u if len(u) <= n else u[: n - 1] + "…"


def counts(rows, s, e):
    sel = [r for r in rows if s <= r["_d"] <= e]
    return sel, Counter(r["event"] for r in sel)


def done_line(c, minutes):
    parts = [f"{c[ev]} {LABELS[ev]}" for ev in EVENTS if ev != "baseline" and c.get(ev)]
    other = sum(v for k, v in c.items() if k not in LABELS)
    if other:
        parts.append(f"{other} other")
    if minutes:
        parts.append(f"{minutes / 60:.1f} h logged")
    return " · ".join(parts) if parts else "nothing logged"


def cmd_summary(a):
    today = pdate(a.today) if a.today else date.today()
    rows = read_rows(a.journal)
    s, e, label = period_range(a.period, today, rows)
    sel, c = counts(rows, s, e)
    minutes = sum(num(r.get("minutes")) or 0 for r in sel)
    pages = page_states(rows, today)

    print(f"# Work report · {label} · {s}" + ("" if s == e else f" – {e}"))
    print()
    print(f"**Done:** {done_line(c, minutes)}")
    if a.period not in ("today", "yesterday", None) and s != e:
        ps, pe = previous_range(a.period, s, e)
        _, pc = counts(rows, ps, pe)
        keys = ["published", "submitted", "check", "audit", "refreshed", "moved", "platform"]
        cmp = [f"{LABELS[k]} {c[k]} vs {pc[k]}" for k in keys if c[k] or pc[k]]
        if cmp:
            print(f"\n**vs previous period ({ps} – {pe}):** " + " · ".join(cmp))

    if not sel:
        print("\nNothing in the journal for this period.")
    else:
        print("\n## By day\n")
        byday = defaultdict(Counter)
        for r in sel:
            byday[r["_d"]][r["event"]] += 1
        for d in sorted(byday):
            ev = ", ".join(f"{n} {LABELS.get(k, k)}" for k, n in byday[d].items())
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

        tasks = [r for r in sel if r["event"] in ("task", "platform", "note") and r.get("note")]
        if tasks:
            print("\n## Other work\n")
            for r in tasks:
                print(f"- {r['_d']} · {r['event']} · {r.get('platform', '')} {r['note']}".replace("  ", " "))

        st = [r for r in sel if r["event"] == "stats"]
        if st:
            cl = sum(num(r.get("clicks")) or 0 for r in st)
            sa = sum(num(r.get("sales")) or 0 for r in st)
            rv = sum(num(r.get("revenue")) or 0 for r in st)
            print(f"\n**Results logged (stats rows):** {fmt(cl)} clicks · {fmt(sa)} sales · ${rv:,.2f}")

    due = due_lists(pages, today)
    if any(due.values()):
        print(f"\n**Needs attention today ({today}):** "
              f"{len(due['check'])} checks due · {len(due['not_indexed'])} not indexed 14+ days · "
              f"{len(due['republish'])} to republish · {len(due['audit'])} audits due · "
              f"{len(due['improve'])} to improve — run `due` for the list")


def cmd_due(a):
    today = pdate(a.today) if a.today else date.today()
    pages = page_states(read_rows(a.journal), today)
    due = due_lists(pages, today)
    sections = [
        ("republish", "Removed / noindex — republish from the saved copy"),
        ("not_indexed", "Not indexed 14+ days after publishing — resubmit, add links or move"),
        ("check", "Alive / index check due"),
        ("improve", f"Audit score under {AUDIT_MIN} — improve, then re-audit"),
        ("audit", "Conversion audit due"),
    ]
    print(f"# Check queue · {today}\n")
    if not any(due.values()):
        print("Nothing due. All tracked pages are checked and audited on schedule.")
        return
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
    today = pdate(a.today) if a.today else date.today()
    pages = page_states(read_rows(a.journal), today)
    items = [p for p in pages.values() if not a.platform or p["platform"] == a.platform]
    items.sort(key=lambda p: p["published"], reverse=True)
    print(f"# Pages · {today} · {len(items)} total\n")
    if not items:
        print("No pages in the journal yet.")
        return
    print("| Published | Page | Platform | Offer | Age | Status | Checked | Audit | Sales | Revenue |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    hc = Counter()
    for p in items:
        h = health(p)
        hc[h] += 1
        print(f"| {p['published']} | {short(p['url'], 50)} | {p['platform']} | {p['offer']} | "
              f"{p['age']} d | {h} | {p['last_check'] or '—'} | {fmt(p['score'])} | "
              f"{fmt(p['sales'])} | ${p['revenue']:,.2f} |")
    print("\n**Status:** " + " · ".join(f"{k} {v}" for k, v in hc.most_common()))


def cmd_add(a):
    now = datetime.now()
    row = {
        "date": a.date or now.strftime("%Y-%m-%d"), "time": a.time or now.strftime("%H:%M"),
        "event": a.event, "page_url": a.url or "", "platform": a.platform or "",
        "offer": a.offer or "", "main_query": a.query or "", "content_type": a.type or "",
        "status": a.status or "", "score": a.score or "", "clicks": a.clicks or "",
        "sales": a.sales or "", "revenue": a.revenue or "", "minutes": a.minutes or "",
        "note": a.note or "",
    }
    if not pdate(row["date"]):
        sys.exit("--date must be YYYY-MM-DD")
    path = a.journal
    if os.path.exists(path) and os.path.getsize(path) > 0:
        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            header = reader.fieldnames or []
            old = list(reader)
        if [h.strip() for h in header] != COLUMNS:
            extra = [h for h in header if h and h.strip() not in COLUMNS]
            cols = COLUMNS + extra
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
                w.writeheader()
                for r in old:
                    w.writerow({k.strip(): v for k, v in r.items() if k})
            print(f"Journal header upgraded to the full format ({len(old)} rows kept).")
        with open(path, newline="", encoding="utf-8") as f:
            cols = next(csv.reader(f))
    else:
        cols = COLUMNS
        with open(path, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(cols)
    with open(path, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=cols, extrasaction="ignore").writerow(row)
    print(f"Logged: {row['date']} {row['event']} {row['page_url'] or row['note']}".strip())


def main():
    ap = argparse.ArgumentParser(description="PARASITER work journal")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("summary")
    s.add_argument("journal")
    s.add_argument("--period", default="today")
    s.add_argument("--today")
    s.set_defaults(fn=cmd_summary)

    d = sub.add_parser("due")
    d.add_argument("journal")
    d.add_argument("--today")
    d.set_defaults(fn=cmd_due)

    p = sub.add_parser("pages")
    p.add_argument("journal")
    p.add_argument("--platform")
    p.add_argument("--today")
    p.set_defaults(fn=cmd_pages)

    ad = sub.add_parser("add")
    ad.add_argument("journal")
    ad.add_argument("--event", required=True, choices=EVENTS)
    for opt in ("url", "platform", "offer", "query", "type", "status", "score", "clicks",
                "sales", "revenue", "minutes", "note", "date", "time"):
        ad.add_argument(f"--{opt}")
    ad.set_defaults(fn=cmd_add)

    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
