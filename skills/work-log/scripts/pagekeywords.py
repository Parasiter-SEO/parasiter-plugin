#!/usr/bin/env python3
"""PARASITER — which Google queries each of the user's pages ranks for, and which it lost (DataForSEO Labs).

  pagekeywords.py JOURNAL [--platform P] [--priority high] [--topic TEXT] [--country us] [--limit 50] [--dry-run]

One request per page (about $0.013 + $0.0001 per keyword returned). Writes
parasite-seo-keywords.csv next to the journal (one row per page × keyword: volume, position,
previous position, lost, estimated traffic, last seen) and a `check` row per page with its best
position and a short summary. Labs data is a crawl snapshot (dates shown), not a live SERP: use
rankcheck.py for today's positions. Credentials as in rankcheck.py.
"""
import argparse
import csv
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rankcheck as rc  # noqa: E402
import worklog as w  # noqa: E402

LABS = "https://api.dataforseo.com/v3/dataforseo_labs/google"
COLS = ["checked", "page_url", "platform", "keyword", "volume", "position", "previous", "lost", "etv", "seen"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("journal")
    ap.add_argument("--platform"); ap.add_argument("--topic")
    ap.add_argument("--priority", choices=w.PRIORITIES)
    ap.add_argument("--country", default="us"); ap.add_argument("--language", default="en")
    ap.add_argument("--limit", type=int, default=50, help="keywords per page (by search volume)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--login"); ap.add_argument("--password")
    a = ap.parse_args()
    login = a.login or os.environ.get("DATAFORSEO_LOGIN")
    password = a.password or os.environ.get("DATAFORSEO_PASSWORD")
    loc = rc.COUNTRIES.get(a.country.lower()) or sys.exit("Unknown --country")
    today = date.today()
    pages = [p for p in w.page_states(w.read_rows(a.journal), today).values()
             if not p["moved"] and p["priority"] != "low" and w.health(p) not in w.GONE
             and (not a.platform or p["platform"].lower() == a.platform.lower())
             and (not a.priority or p["priority"] == a.priority)
             and (not a.topic or a.topic.lower() in p["topic_key"])]
    print(f"Page keywords · google {a.country} · {len(pages)} pages · about ${len(pages) * (0.0113 + a.limit * 0.0001):.2f} at most")
    if a.dry_run or not pages:
        return
    if not (login and password):
        sys.exit("No DataForSEO credentials (DATAFORSEO_LOGIN / DATAFORSEO_PASSWORD).")
    out_path = os.path.join(os.path.dirname(os.path.abspath(a.journal)), "parasite-seo-keywords.csv")
    rows, checks, summary = [], [], []
    for p in pages:
        url = p["url"] if p["url"].startswith("http") else "https://" + p["url"]  # full URL = this page, not the domain
        d = rc.call("POST", "/ranked_keywords/live", login, password,
                    [{"target": url, "location_code": loc, "language_code": a.language, "limit": a.limit,
                      "historical_serp_mode": "all", "order_by": ["keyword_data.keyword_info.search_volume,desc"]}],
                    base=LABS)
        res = ((d.get("tasks") or [{}])[0].get("result") or [{}])[0] or {}
        live, lost = [], []
        for it in res.get("items") or []:
            kd, se = it["keyword_data"], it["ranked_serp_element"]
            si = se.get("serp_item") or {}
            ch = si.get("rank_changes") or {}
            is_lost = bool(se.get("is_lost") or ch.get("is_lost"))
            r = {"checked": today.isoformat(), "page_url": p["url"], "platform": p["platform"], "keyword": kd["keyword"],
                 "volume": kd["keyword_info"].get("search_volume") or "", "position": "" if is_lost else si.get("rank_group") or "",
                 "previous": ch.get("previous_rank_absolute") or "", "lost": "yes" if is_lost else "",
                 "etv": round(si.get("etv") or 0, 1), "seen": (se.get("last_updated_time") or "")[:10]}
            rows.append(r)
            (lost if is_lost else live).append(r)
        best = min([int(r["position"]) for r in live if r["position"]] or [0]) or None
        top10 = sum(1 for r in live if r["position"] and int(r["position"]) <= 10)
        etv = sum(float(r["etv"] or 0) for r in live)
        note = f"labs: {len(live)} keywords, {top10} in top 10, ~{etv:.0f} visits/mo, {len(lost)} lost"
        checks.append(w.journal_row(date=today.isoformat(), event="check", page_url=p["url"], platform=p["platform"],
                                    status="indexed" if live else "", position=best or "", note=note))
        summary.append((etv, top10, p, live, lost))
    new = not os.path.exists(out_path)
    with open(out_path, "a", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=COLS)
        if new:
            wr.writeheader()
        wr.writerows(rows)
    if checks:
        w.append(a.journal, w.COLUMNS, checks)
    summary.sort(key=lambda s: (-s[0], -s[1]))
    print(f"- {sum(1 for s in summary if s[3])} of {len(summary)} pages rank for at least one query · saved to {os.path.basename(out_path)}")
    print("\n| Page | Platform | Queries | Top 10 | Visits/mo (est.) | Lost |\n|---|---|---|---|---|---|")
    for etv, top10, p, live, lost in summary[:25]:
        if live or lost:
            print(f"| {w.short(p['url'], 50)} | {p['platform']} | {len(live)} | {top10} | {etv:.0f} | {len(lost)} |")
    big_lost = sorted((r for s in summary for r in s[4] if r["volume"]), key=lambda r: -int(r["volume"]))[:15]
    if big_lost:
        print("\n**Biggest lost queries** (volume · was · page)")
        for r in big_lost:
            print(f"- {r['keyword']} · {r['volume']} · #{r['previous'] or '?'} · {w.short(r['page_url'], 45)} (last seen {r['seen']})")


if __name__ == "__main__":
    main()
