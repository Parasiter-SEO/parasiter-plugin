#!/usr/bin/env python3
"""PARASITER · Forum cluster scan (Rumer's method №68) through the user's own DataForSEO or SerpApi account.

  forumscan.py QUERIES [--provider dataforseo|serpapi] [--country us] [--language en] [--depth 20]
               [--device desktop] [--mine FILE] [--out forum-scan.csv] [--live] [--dry-run]
               [--from-json FILE] [--self-test]

QUERIES: a comma-separated list ("ikaria juice review,ikaria juice results") or a text file, one query per line.

For every query it reads Google's results and records:
  · the "Discussions and forums" block — is it there, which threads are in it (title, forum, age, comments);
  · forum / community threads in the organic top N (XenForo, phpBB, vBulletin, Discourse, Reddit, Quora…);
  · the age of every thread, so the user sees where the top is old (a fresh thread can push it out)
    and where it is crowded with fresh threads;
  · the user's own threads (--mine: the journal CSV or a list of URLs/domains) — to see which of them
    got in and which old threads they displaced on the next run.

It prints a short verdict per query (OPEN / WINDOW / CROWDED / NO FORUMS) and writes every thread to --out.
Nothing is sent anywhere except the search request to the user's own provider.

Credentials: from the plugin settings via the dataforseo_run / serpapi_run tool (inherited pipe, --auth-fd).
Never written anywhere. --dry-run shows the cost first.
"""
import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.parse
from datetime import date, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "work-log", "scripts"))
import rankcheck as rc  # noqa: E402

DF_TYPES = ("discussions_and_forums", "discussions_and_forums_element", "perspectives")
FORUM_PATH = re.compile(
    r"(/threads?/|/t/[^/]+/\d+|/topic|/forums?/|/community/|/communities/|/discussion|/discuss/|viewtopic\.php|"
    r"showthread\.php|/questions?/|/comments/|/board/|/boards/|/r/[^/]+)", re.I)
FORUM_HOSTS = ("reddit.com", "quora.com", "forum.", "forums.", "community.", "communities.", "discuss.",
               "boards.", "board.")
ENGINES = [
    (re.compile(r"/threads/[^/]+\.\d+/?", re.I), "XenForo"),
    (re.compile(r"viewtopic\.php", re.I), "phpBB"),
    (re.compile(r"showthread\.php|/showthread/", re.I), "vBulletin"),
    (re.compile(r"/t/[^/]+/\d+", re.I), "Discourse"),
    (re.compile(r"reddit\.com/r/", re.I), "Reddit"),
    (re.compile(r"quora\.com", re.I), "Quora"),
    (re.compile(r"/topic/\d+|index\.php\?/topic/", re.I), "Invision"),
]
AGO = re.compile(r"(\d+)\s*\+?\s*(minute|hour|day|week|month|year)s?\s+ago", re.I)
COMMENTS = re.compile(r"(\d[\d,]*)\s*\+?\s*(comments?|answers?|replies|posts?)", re.I)
UNIT_DAYS = {"minute": 0, "hour": 0, "day": 1, "week": 7, "month": 30, "year": 365}
DATE_FORMATS = ("%b %d, %Y", "%B %d, %Y", "%d %b %Y", "%d %B %Y", "%Y-%m-%d", "%b %Y", "%B %Y")
OPEN_DAYS, FRESH_DAYS = 180, 45


# ---------- parsing helpers ----------

def host_of(url):
    h = urllib.parse.urlparse(url).netloc.lower()
    return h[4:] if h.startswith("www.") else h


def is_forum(url):
    h = host_of(url)
    return bool(FORUM_PATH.search(urllib.parse.urlparse(url).path + "?" + urllib.parse.urlparse(url).query)) \
        or any(h.startswith(p) or ("." + p.strip(".") + ".") in "." + h + "." or h.endswith(p.strip(".")) for p in FORUM_HOSTS)


def engine_of(url):
    for rx, name in ENGINES:
        if rx.search(url):
            return name
    return ""


def age_days(text, today):
    """Days since a date written as '3 months ago', 'Mar 5, 2024' or an ISO timestamp; None if unknown."""
    if not text:
        return None
    s = str(text).strip()
    m = AGO.search(s)
    if m:
        return int(m.group(1)) * UNIT_DAYS[m.group(2).lower()]
    iso = re.match(r"(\d{4}-\d{2}-\d{2})", s)
    if iso:
        try:
            return (today - date.fromisoformat(iso.group(1))).days
        except ValueError:
            pass
    for f in DATE_FORMATS:
        try:
            return (today - datetime.strptime(s, f).date()).days
        except ValueError:
            continue
    return None


def first_age(values, today):
    for v in values:
        d = age_days(v, today)
        if d is not None:
            return d, str(v)
    return None, ""


def comments_of(values):
    for v in values:
        m = COMMENTS.search(str(v or ""))
        if m:
            return int(m.group(1).replace(",", ""))
    return None


def thread(block, pos, title, url, source, date_vals, extra_vals, today):
    d, raw = first_age(date_vals + extra_vals, today)
    return {"block": block, "position": pos, "title": (title or "").strip(), "url": url, "domain": host_of(url),
            "forum": (source or "").strip(), "engine": engine_of(url), "date": raw, "age_days": d,
            "comments": comments_of(extra_vals + date_vals)}


def parse_serpapi(responses, today, depth):
    out, n, df_pos = [], 0, 0
    for d in responses:
        for it in d.get("organic_results") or []:
            n += 1
            url = it.get("link") or ""
            if url and n <= depth and is_forum(url):
                ext = list((it.get("rich_snippet") or {}).get("top", {}).get("extensions") or []) + \
                    list((it.get("rich_snippet") or {}).get("bottom", {}).get("extensions") or [])
                out.append(thread("organic", n, it.get("title"), url, it.get("source") or it.get("displayed_link"),
                                  [it.get("date")], ext + [it.get("snippet") or ""], today))
        for key in ("discussions_and_forums", "perspectives"):
            for it in d.get(key) or []:
                url = it.get("link") or ""
                if not url:
                    continue
                df_pos += 1
                out.append(thread("discussions_and_forums" if key == "discussions_and_forums" else "perspectives",
                                  df_pos, it.get("title"), url, it.get("source"), [it.get("date")],
                                  list(it.get("extensions") or []), today))
    return out


def parse_dataforseo(task, today, depth):
    out, df_pos = [], 0
    for res in task.get("result") or []:
        for it in res.get("items") or []:
            typ = it.get("type") or ""
            if typ == "organic":
                url = it.get("url") or ""
                pos = it.get("rank_group") or it.get("rank_absolute") or 0
                if url and pos <= depth and is_forum(url):
                    out.append(thread("organic", pos, it.get("title"), url, it.get("website_name") or it.get("domain"),
                                      [it.get("timestamp"), it.get("pre_snippet")],
                                      [it.get("description") or ""], today))
            elif typ in DF_TYPES:
                block = "perspectives" if typ == "perspectives" else "discussions_and_forums"
                for el in it.get("items") or [it]:
                    url = el.get("url") or ""
                    if not url:
                        continue
                    df_pos += 1
                    out.append(thread(block, df_pos, el.get("title"), url, el.get("source") or el.get("domain"),
                                      [el.get("timestamp"), el.get("date")],
                                      [str(x) for x in (el.get("extensions") or [])] +
                                      [str(el.get("votes_count") or ""), str(el.get("description") or "")], today))
    return out


# ---------- the user's own threads ----------

def load_mine(path):
    """URLs and bare domains of the user's own threads: the journal CSV (url column) or a plain list."""
    urls, domains = set(), set()
    if not path:
        return urls, domains
    if not os.path.exists(path):
        sys.exit(f"--mine file not found: {path}")
    with open(path, encoding="utf-8-sig") as f:
        text = f.read()
    cells = []
    if path.lower().endswith(".csv"):
        for row in csv.DictReader(text.splitlines()):
            cells += [v for k, v in row.items() if k and k.lower() in ("url", "page_url", "link") and v]
    else:
        cells = re.split(r"[\s,]+", text)
    for c in cells:
        c = c.strip()
        if c.startswith("http"):
            urls.add(norm(c))
        elif "." in c:
            domains.add(c.lower().removeprefix("www."))
    return urls, domains


def norm(url):
    p = urllib.parse.urlparse(url.strip())
    return (host_of(url) + p.path.rstrip("/")).lower()


def is_mine(t, urls, domains):
    return norm(t["url"]) in urls


# ---------- verdict ----------

def verdict(threads):
    df = [t for t in threads if t["block"] == "discussions_and_forums"]
    forums = threads
    if not forums:
        return "NO FORUMS", "no forum threads in the block or the top — a forum post is a long shot here; pick another query"
    ages = [t["age_days"] for t in forums if t["age_days"] is not None]
    fresh = [a for a in ages if a <= FRESH_DAYS]
    old = [a for a in ages if a >= OPEN_DAYS]
    block = "block ON" if df else "no block"
    if ages and len(old) >= max(1, len(ages) // 2) and not fresh:
        return "OPEN", f"{block}; the forum threads are old (newest {min(ages)} days) — fresh threads can push them out: post the cluster now"
    if fresh and len(fresh) >= max(2, len(ages) // 2):
        return "CROWDED", f"{block}; {len(fresh)} threads under {FRESH_DAYS} days — others post here now: different angles, more threads, keep yours active"
    if not ages:
        return "WINDOW", f"{block}; ages not shown by Google — open the threads and check their dates"
    return "WINDOW", f"{block}; mixed ages (newest {min(ages)} days) — 3–5 threads with new angles have a real chance"


# ---------- search ----------

def read_queries(arg):
    if arg and os.path.exists(arg):
        with open(arg, encoding="utf-8-sig") as f:
            items = [ln.strip() for ln in f if ln.strip() and not ln.startswith("#")]
    else:
        items = [x.strip() for x in (arg or "").split(",") if x.strip()]
    seen, out = set(), []
    for q in items:
        if q.lower() not in seen:
            seen.add(q.lower())
            out.append(q)
    return out


def read_key(fd):
    if fd is None:
        return None
    try:
        data = os.read(int(fd), 4096).decode().strip()
        os.close(int(fd))
    except OSError:
        return None
    return data or None


def search(a, queries, today):
    if a.provider == "serpapi":
        per = rc.serpapi_searches(a.depth, "google")
        print(f"Forum scan · google {a.country} · top {a.depth} + Discussions and forums · {len(queries)} queries · "
              f"SerpApi: {len(queries) * per} searches from your monthly quota")
    else:
        loc = rc.COUNTRIES.get(a.country.lower()) or sys.exit("Unknown --country: " + ", ".join(sorted(rc.COUNTRIES)))
        price = (0.002 if a.live else 0.0006) * max(1, a.depth / 10)
        print(f"Forum scan · google {a.country} · top {a.depth} + Discussions and forums · {len(queries)} queries · "
              f"PAID: about ${len(queries) * price:.3f} from your DataForSEO balance")
    if a.dry_run:
        for q in queries[:30]:
            print("  ·", q)
        return None
    raw = {}
    if a.provider == "serpapi":
        key = read_key(a.auth_fd) or sys.exit(rc.NO_SERPAPI)
        a.engine = "google"
        for q in queries:
            raw[q] = {"provider": "serpapi", "data": rc.serpapi_query(q, key, a)}
        return raw
    login, password = rc.read_auth(a.auth_fd)
    if not (login and password):
        sys.exit(rc.NO_CREDS)
    body = [{"keyword": q, "location_code": loc, "language_code": a.language, "depth": a.depth,
             "device": a.device, "tag": q} for q in queries]
    if a.live:
        for item in body:
            d = rc.call("POST", "/live/advanced", login, password, [item])
            for t in d.get("tasks") or []:
                raw[(t.get("data") or {}).get("keyword", item["keyword"])] = {"provider": "dataforseo", "data": t}
        return raw
    ids = {}
    for i in range(0, len(body), 100):
        d = rc.call("POST", "/task_post", login, password, body[i:i + 100])
        for t in d.get("tasks") or []:
            if t.get("id"):
                ids[t["id"]] = (t.get("data") or {}).get("keyword", "")
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
                        raw[ids[r["id"]]] = {"provider": "dataforseo", "data": tt}
                    ids.pop(r["id"])
    if ids:
        print(f"- {len(ids)} tasks not ready yet (paid, kept 3 days by DataForSEO): run again later with --live off.")
    return raw


def analyse(raw, today, depth, mine):
    urls, domains = mine
    rows, summary = [], []
    for q, r in raw.items():
        threads = parse_serpapi(r["data"], today, depth) if r["provider"] == "serpapi" \
            else parse_dataforseo(r["data"], today, depth)
        seen = set()
        uniq = []
        for t in threads:
            k = (t["block"], norm(t["url"]))
            if k not in seen:
                seen.add(k)
                t["query"] = q
                t["mine"] = "yes" if is_mine(t, urls, domains) else ""
                t["my_forum"] = "yes" if t["domain"] in domains else ""
                uniq.append(t)
        v, why = verdict(uniq)
        summary.append((q, v, why, uniq))
        rows += uniq
    return rows, summary


def report(rows, summary, out):
    cols = ["query", "block", "position", "title", "url", "domain", "forum", "engine", "date", "age_days",
            "comments", "mine", "my_forum"]
    with open(out, "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        wr.writeheader()
        wr.writerows(rows)
    print()
    for q, v, why, threads in summary:
        df = [t for t in threads if t["block"] == "discussions_and_forums"]
        org = [t for t in threads if t["block"] == "organic"]
        mine = [t for t in threads if t["mine"]]
        print(f"■ {q} — {v}: {why}")
        print(f"  Discussions and forums: {len(df)} threads · forum threads in the organic top: {len(org)}"
              + (f" · yours in: {len(mine)}" if mine else ""))
        for t in sorted(threads, key=lambda x: (x["block"] != "discussions_and_forums", x["position"]))[:8]:
            age = f"{t['age_days']} d" if t["age_days"] is not None else "age ?"
            com = f" · {t['comments']} comments" if t["comments"] is not None else ""
            tag = " · YOURS" if t["mine"] else (" · your forum" if t["my_forum"] else "")
            where = "D&F" if t["block"] == "discussions_and_forums" else ("persp." if t["block"] == "perspectives" else f"#{t['position']}")
            print(f"   {where:>6} · {age:>7}{com} · {t['engine'] or t['domain']} · {t['title'][:70]}{tag}")
            print(f"          {t['url']}")
    engines = {}
    for r in rows:
        if r["engine"]:
            engines[r["engine"]] = engines.get(r["engine"], 0) + 1
    if engines:
        print("\nForum engines in these results: " + ", ".join(f"{k} {v}" for k, v in sorted(engines.items(), key=lambda x: -x[1])))
    print(f"\nSaved {len(rows)} threads to {out}. Verdicts: OPEN = old top, post now · WINDOW = room for new angles · "
          f"CROWDED = fresh competition, more threads and keep them active · NO FORUMS = pick another query.")


# ---------- self-test ----------

def self_test():
    today = date(2026, 11, 18)
    assert age_days("3 months ago", today) == 90
    assert age_days("1 year ago", today) == 365
    assert age_days("Mar 5, 2026", today) == (today - date(2026, 3, 5)).days
    assert age_days("2026-11-01T10:00:00+00:00", today) == 17
    assert comments_of(["Posted by x", "120+ comments"]) == 120
    assert engine_of("https://forum.example.com/threads/ikaria-review.12345/") == "XenForo"
    assert engine_of("https://boards.example.org/viewtopic.php?t=9") == "phpBB"
    assert engine_of("https://discuss.example.com/t/my-results/882") == "Discourse"
    assert is_forum("https://www.reddit.com/r/supplements/comments/abc/x/")
    assert is_forum("https://forum.example.com/threads/x.1/")
    assert not is_forum("https://www.healthline.com/nutrition/ikaria-juice")
    sp = [{"organic_results": [
        {"position": 1, "link": "https://www.healthline.com/x", "title": "Review"},
        {"position": 2, "link": "https://forum.example.com/threads/my-ikaria-results.555/", "title": "My results",
         "date": "Jan 10, 2025"}],
        "discussions_and_forums": [
            {"title": "Anyone tried Ikaria?", "link": "https://www.reddit.com/r/loseit/comments/1/x/", "date": "2 years ago",
             "source": "Reddit · r/loseit", "extensions": ["40+ comments"]},
            {"title": "Ikaria 3 months in", "link": "https://forum.example.com/threads/ikaria-3-months.777/",
             "date": "14 months ago", "extensions": ["12 posts"]}]}]
    th = parse_serpapi(sp, today, 20)
    assert len(th) == 3, th
    df = [t for t in th if t["block"] == "discussions_and_forums"]
    assert df[0]["age_days"] == 730 and df[0]["comments"] == 40 and df[1]["engine"] == "XenForo"
    v, _ = verdict(th)
    assert v == "OPEN", v
    dfs = {"result": [{"items": [
        {"type": "organic", "rank_group": 3, "url": "https://community.example.com/t/x/12", "title": "X", "timestamp": "2026-11-10 08:00:00 +00:00"},
        {"type": "discussions_and_forums", "items": [
            {"type": "discussions_and_forums_element", "url": "https://www.quora.com/Is-x-legit", "title": "Is X legit?",
             "timestamp": "2026-10-30 08:00:00 +00:00", "source": "Quora"},
            {"type": "discussions_and_forums_element", "url": "https://www.reddit.com/r/a/comments/2/y/", "title": "Y",
             "timestamp": "2026-11-12 08:00:00 +00:00"}]}]}]}
    th2 = parse_dataforseo(dfs, today, 20)
    assert len(th2) == 3 and th2[0]["age_days"] == 8, th2
    assert verdict(th2)[0] == "CROWDED"
    assert verdict([])[0] == "NO FORUMS"
    mine = ({norm("https://forum.example.com/threads/ikaria-3-months.777/")}, {"forum.example.com"})
    rows, summ = analyse({"ikaria juice review": {"provider": "serpapi", "data": sp}}, today, 20, mine)
    assert sum(1 for r in rows if r["mine"]) == 1 and sum(1 for r in rows if r["my_forum"]) == 2
    print("self-test ok")


def main():
    ap = argparse.ArgumentParser(description="Forum cluster scan: Discussions and forums block + forum threads in the top, with ages")
    ap.add_argument("queries", nargs="?")
    ap.add_argument("--provider", default="dataforseo", choices=["dataforseo", "serpapi"])
    ap.add_argument("--country", default="us")
    ap.add_argument("--language", default="en")
    ap.add_argument("--depth", type=int, default=20, help="organic top N to read for forum threads (default 20)")
    ap.add_argument("--device", default="desktop", choices=["desktop", "mobile"])
    ap.add_argument("--mine", help="the user's journal CSV or a list of their thread URLs / forum domains")
    ap.add_argument("--out", default="forum-scan.csv")
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--wait", type=int, default=15)
    ap.add_argument("--from-json", help="saved raw results ({query: {provider, data}}) — no search, free")
    ap.add_argument("--save-raw", help="also save the raw results here (to re-read later with --from-json)")
    ap.add_argument("--auth-fd", help=argparse.SUPPRESS)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    today = date.today()
    if a.from_json:
        with open(a.from_json, encoding="utf-8") as f:
            raw = json.load(f)
    else:
        queries = read_queries(a.queries)
        if not queries:
            sys.exit("Give the queries: \"q1,q2\" or a file with one query per line.")
        raw = search(a, queries, today)
        if raw is None:
            return
        if a.save_raw:
            with open(a.save_raw, "w", encoding="utf-8") as f:
                json.dump(raw, f)
    rows, summary = analyse(raw, today, a.depth, load_mine(a.mine))
    report(rows, summary, a.out)


if __name__ == "__main__":
    main()
