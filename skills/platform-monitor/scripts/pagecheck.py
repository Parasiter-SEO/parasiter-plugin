#!/usr/bin/env python3
"""PARASITER — cheap page check of the user's journal (№76).

  pagecheck.py JOURNAL [--due | --all | --urls FILE | --platform SLUG] [--limit N] [--log] [--today YYYY-MM-DD]
  pagecheck.py --self-test

Why it exists: on Claude Pro the expensive part of a page check is Claude reading every page.
This script opens the pages itself, on the user's computer, and prints ONLY a short summary —
what changed and the counts — so a check of 50 pages costs about the same Claude usage as one
ordinary reply. Nothing is sent anywhere: page addresses stay on the user's computer.

For each page (same rules as platformscan.py --check-urls, №71):
- Thread availability: LIVE THREAD / REDIRECTED / REMOVED / FETCH BLOCKED / UNVERIFIED
- Indexing eligibility: INDEXABLE / NOINDEX / UNVERIFIED (meta robots, X-Robots-Tag)
- Affiliate link: found / NOT FOUND / no library — any link from parasite-seo-links.csv
  (next to the journal) or the link domain is on the page.

Pages: --due (default) = the journal's check queue (work-log `due`: alive checks due and imported
pages never checked); --all = every page not moved or dead; --platform = one platform;
--urls = a file with one URL per line. ★ pages first. --limit caps the run (default 60).

--log appends a `check` row per page to the journal: live, removed or noindex (pages the
script could not open are not logged — they stay in the queue to check by hand).
Full table: pagecheck-results.csv next to the journal.

Not a Google check: whether a page is indexed or ranking needs the user's SEO data account
(rankcheck.py / indexing). This script never claims a position.
"""
import argparse
import csv
import importlib.util
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILLS = HERE.parent.parent


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, SKILLS / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ps = _load("platformscan", "platform-finder/scripts/platformscan.py")
wl = _load("worklog", "work-log/scripts/worklog.py")


def link_keys(journal):
    """Normalized affiliate links and their hosts from the user's links library."""
    path = wl.links_path(journal)
    if not os.path.exists(path):
        return None
    full, hosts = set(), set()
    for r in wl.read_csv(path):
        for u in [r.get("link", "")] + re.split(r"[\s;|]+", r.get("alt_links", "") or ""):
            u = (u or "").strip()
            if not re.match(r"https?://", u):
                continue
            k = re.sub(r"^https?://(www\.)?", "", u.lower()).split("#")[0].rstrip("/")
            full.add(k)
            hosts.add(k.split("/")[0])
    return {"full": full, "hosts": hosts}


def link_status(html, keys):
    if keys is None:
        return "no library"
    low = html.lower().replace("&amp;", "&")
    if any(k in low for k in keys["full"]):
        return "found"
    if any(re.search(r"https?://(www\.)?" + re.escape(h) + r"[/\"'?]", low) for h in keys["hosts"]):
        return "found"
    return "NOT FOUND"


def check_one(url, keys):
    """Availability + indexing (platformscan rules) + affiliate link on the final page."""
    r = ps.check_url(url)
    r["link"] = "—"
    if r["availability"] == ps.LIVE:
        try:
            body = ps.fetch(r["final"] or url)[3].decode("utf-8", "replace")
            r["link"] = link_status(body, keys)
        except Exception:
            r["link"] = "unverified"
    return r


def status_of(r):
    """Journal status from a check result, or None when the page could not be verified."""
    if r["availability"] == ps.LIVE:
        return "noindex" if r["indexing"] == ps.NOINDEX else "live"
    if r["availability"] == ps.GONE:
        return "removed"
    return None


def pick_pages(a, pages, today):
    items = [p for p in pages.values() if not p["moved"] and p["status"] != "dead"]
    if a.urls:
        want = [ln.strip() for ln in open(a.urls, encoding="utf-8") if ln.strip() and not ln.startswith("#")]
        known = {wl.norm_url(p["url"]): p for p in items}
        return [known.get(wl.norm_url(u)) or {"url": u, "platform": "", "priority": "normal", "status": ""} for u in want]
    if a.platform:
        items = [p for p in items if (p["platform"] or "").lower() == a.platform.lower()]
    elif not a.all:
        due = wl.due_lists([], [], pages, today)  # rows/sales only matter for the sales queue
        keep = {id(p) for key in ("check", "imported") for p, _ in due[key]}
        items = [p for p in items if id(p) in keep]
    return sorted(items, key=lambda p: (wl.PRIORITIES.index(p.get("priority") or "normal"), p["url"]))


def main():
    ap = argparse.ArgumentParser(description="Cheap page check of the journal: availability, noindex, affiliate link")
    ap.add_argument("journal", nargs="?")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--due", action="store_true", help="the check queue (default)")
    g.add_argument("--all", action="store_true")
    g.add_argument("--platform")
    g.add_argument("--urls")
    ap.add_argument("--limit", type=int, default=60)
    ap.add_argument("--log", action="store_true", help="append check rows to the journal")
    ap.add_argument("--today")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if not a.journal:
        ap.error("give the journal (parasite-seo-progress.csv)")

    today = wl.pdate(a.today) if a.today else date.today()
    rows = wl.read_rows(a.journal)
    pages = wl.page_states(rows, today)
    items = pick_pages(a, pages, today)
    if not items:
        print("Nothing to check: no pages due. Say \"check all my pages\" for a full run.")
        return
    left = max(0, len(items) - a.limit)
    items = items[:a.limit]
    keys = link_keys(a.journal)
    with ThreadPoolExecutor(8) as pool:
        res = list(pool.map(lambda p: check_one(p["url"], keys), items))

    out_csv = os.path.join(os.path.dirname(os.path.abspath(a.journal)), "pagecheck-results.csv")
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["checked", "url", "platform", "previous", "availability", "indexing", "affiliate_link", "why", "final"])
        for p, r in zip(items, res):
            w.writerow([today.isoformat(), p["url"], p.get("platform") or "", p.get("status") or "",
                        r["availability"], r["indexing"], r["link"], r["why"], r["final"]])

    changed, blocked, nolink = [], [], []
    n_live = n_gone = n_noidx = 0
    for p, r in zip(items, res):
        st = status_of(r)
        prev = p.get("status") or ""
        star = "★ " if p.get("priority") == "high" else ""
        tag = f"{star}{wl.short(p['url'], 60)} · {p.get('platform') or '?'}"
        if st is None:
            blocked.append(f"- {tag} — {r['why']}")
            continue
        n_live += st == "live"
        n_gone += st == "removed"
        n_noidx += st == "noindex"
        was_alive = prev in ("", "live", "indexed", "not-indexed", "dropped")
        if st in ("removed", "noindex") and (was_alive or prev != st):
            changed.append(f"▼ {tag} — {st}: {r['why']}")
        elif st == "live" and prev in ("removed", "noindex"):
            changed.append(f"▲ {tag} — live again")
        if st == "live" and r["link"] == "NOT FOUND":
            nolink.append(f"- {tag} — affiliate link not on the page")

    print(f"# Page check · {today} · {len(items)} pages (script, no page text read by Claude)\n")
    print(f"Live {n_live} · removed {n_gone} · noindex {n_noidx} · could not open {len(blocked)}"
          + (f" · {left} more due — run again" if left else ""))
    if changed:
        print("\n## Changed\n" + "\n".join(changed))
    else:
        print("\nNo page removed or noindexed since the last check.")
    if nolink:
        print("\n## Affiliate link missing\n" + "\n".join(nolink))
    if keys is None:
        print("\n(No links library yet — affiliate links not checked. Import them: worklog.py import-links.)")
    if blocked:
        print("\n## Open by hand (site blocks automatic checks)\n" + "\n".join(blocked[:10])
              + (f"\n- … and {len(blocked) - 10} more in the CSV" if len(blocked) > 10 else ""))
    print(f"\nFull table: {os.path.basename(out_csv)}. Not a Google check: indexing and positions need your SEO data account.")

    if a.log:
        logged = []
        for p, r in zip(items, res):
            st = status_of(r)
            if st:
                note = "pagecheck" + ("; affiliate link not found" if r["link"] == "NOT FOUND" else "")
                logged.append(wl.journal_row(event="check", page_url=p["url"], platform=p.get("platform") or "",
                                             status=st, note=note) | {"date": today.isoformat()})
        if logged:
            wl.append(a.journal, wl.COLUMNS, logged)
        print(f"Logged {len(logged)} check rows in the journal.")


def self_test():
    keys = {"full": {"hop.clickbank.net/?affiliate=me&vendor=x"}, "hosts": {"hop.clickbank.net"}}
    assert link_status('<a href="https://hop.clickbank.net/?affiliate=me&amp;vendor=x">buy</a>', keys) == "found"
    assert link_status('<a href="https://www.hop.clickbank.net/other">buy</a>', keys) == "found"
    assert link_status('<a href="https://example.com/">x</a>', keys) == "NOT FOUND"
    assert link_status("anything", None) == "no library"
    assert status_of({"availability": ps.LIVE, "indexing": ps.NOINDEX}) == "noindex"
    assert status_of({"availability": ps.LIVE, "indexing": ps.INDEXABLE}) == "live"
    assert status_of({"availability": ps.GONE, "indexing": ps.UNVER}) == "removed"
    assert status_of({"availability": ps.BLOCKED, "indexing": ps.UNVER}) is None
    print("pagecheck self-test: ok")


if __name__ == "__main__":
    main()
