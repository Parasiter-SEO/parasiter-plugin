#!/usr/bin/env python3
"""PARASITER — performance report from a publications log CSV.

Usage: python3 report.py log.csv [--today YYYY-MM-DD]

Expected columns (missing numeric values are treated as unknown):
url, platform, published, offer, content_type, main_query, country, sub_id,
status, impressions, clicks, affiliate_clicks, sales, commission
Prints per-page metrics and totals by platform, content type and offer (Markdown).
"""
import csv
import sys
from collections import defaultdict
from datetime import date


def num(v):
    try:
        return float(str(v).replace(",", "").replace("$", "").strip())
    except (TypeError, ValueError):
        return None


def fmt(v, money=False, pct=False):
    if v is None:
        return "—"
    if pct:
        return f"{v * 100:.1f}%"
    if money:
        return f"${v:,.2f}"
    return f"{v:,.0f}" if float(v).is_integer() else f"{v:,.2f}"


def page_metrics(r, today):
    imp, clk = num(r.get("impressions")), num(r.get("clicks"))
    aclk, sales, com = num(r.get("affiliate_clicks")), num(r.get("sales")), num(r.get("commission"))
    m = {
        "epc": com / aclk if com is not None and aclk else None,
        "cr": sales / aclk if sales is not None and aclk else None,
        "ctr": clk / imp if clk is not None and imp else None,
        "rpm": None,
        "age": None,
    }
    if imp and clk and sales is not None and com is not None and sales:
        m["rpm"] = (clk / imp) * (sales / clk) * (com / sales) * 1000
    try:
        m["age"] = (today - date.fromisoformat(r.get("published", "")[:10])).days
    except ValueError:
        pass
    return m


def review_point(age):
    if age is None:
        return "—"
    if age < 14:
        return "too early"
    if age < 30:
        return "14-day check"
    if age < 60:
        return "30-day check"
    return "60-day decision"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    today = date.today()
    if "--today" in sys.argv:
        today = date.fromisoformat(sys.argv[sys.argv.index("--today") + 1])
    with open(sys.argv[1], newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    print(f"# Performance report · {today.isoformat()} · {len(rows)} publications\n")
    print("| Page | Platform | Type | Age | Aff. clicks | Sales | Commission | EPC | CR | RPM | Review |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    groups = {k: defaultdict(lambda: [0, 0.0, 0.0, 0.0]) for k in ("platform", "content_type", "offer")}
    ranked = []
    for r in rows:
        m = page_metrics(r, today)
        com = num(r.get("commission")) or 0.0
        ranked.append((com, r.get("url", "")))
        print(
            f"| {r.get('url','')} | {r.get('platform','')} | {r.get('content_type','')} | "
            f"{fmt(m['age'])} | {fmt(num(r.get('affiliate_clicks')))} | {fmt(num(r.get('sales')))} | "
            f"{fmt(num(r.get('commission')), money=True)} | {fmt(m['epc'], money=True)} | "
            f"{fmt(m['cr'], pct=True)} | {fmt(m['rpm'], money=True)} | {review_point(m['age'])} |"
        )
        for k in groups:
            g = groups[k][r.get(k, "") or "(none)"]
            g[0] += 1
            g[1] += num(r.get("affiliate_clicks")) or 0
            g[2] += num(r.get("sales")) or 0
            g[3] += com

    for k, title in (("platform", "By platform"), ("content_type", "By content type"), ("offer", "By offer")):
        print(f"\n## {title}\n")
        print("| Group | Pages | Aff. clicks | Sales | Commission | Per page | EPC |")
        print("|---|---|---|---|---|---|---|")
        for name, (n, ac, s, c) in sorted(groups[k].items(), key=lambda x: -x[1][3]):
            print(f"| {name} | {n} | {fmt(ac)} | {fmt(s)} | {fmt(c, money=True)} | "
                  f"{fmt(c / n if n else None, money=True)} | {fmt(c / ac if ac else None, money=True)} |")

    total = sum(c for c, _ in ranked)
    print(f"\n**Total commission (from data): {fmt(total, money=True)}**\n")
    print("## Top 5 pages\n")
    for c, u in sorted(ranked, reverse=True)[:5]:
        print(f"- {u} — {fmt(c, money=True)}")


if __name__ == "__main__":
    main()
