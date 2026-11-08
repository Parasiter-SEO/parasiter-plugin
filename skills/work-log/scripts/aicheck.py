#!/usr/bin/env python3
"""PARASITER — AI visibility check: is the user's page cited in AI answers for its buyer query?

  aicheck.py JOURNAL [--engines ai_mode,chatgpt,gemini] [--country us] [--language en]
             [--platform P] [--priority high] [--topic TEXT] [--limit N] [--dry-run] [--from-json FILE --engine E]

Engines (through the user's own DataForSEO account, standard queue, about $0.0012 per query per engine):
  ai_mode  — Google AI Mode (closest to Google and Gemini in Search)     /v3/serp/google/ai_mode
  chatgpt  — ChatGPT answers with web search (LLM Scraper)                /v3/ai_optimization/chat_gpt/llm_scraper
  gemini   — Gemini app answers (LLM Scraper)                             /v3/ai_optimization/gemini/llm_scraper
One request per unique query per engine. Every URL the answer cites is compared with the user's pages:
the page is "cited" when its own URL is among the sources; "platform cited" when another page of the
same platform domain is (the platform is trusted by that AI for the query — a good place to post).

Journal: one `check` row per page and engine, without position/status (those stay Google's):
note "ai: <query> · <engine> <country> · cited" | "· platform cited" | "· not cited".
AI answers change from run to run: treat one check as a sample, compare over weeks.
Credentials: only through the dataforseo_run tool (inherited pipe, --auth-fd).
"""
import argparse
import json
import os
import sys
import time
from collections import defaultdict
from datetime import date
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rankcheck as rc  # noqa: E402
import worklog as w  # noqa: E402

ENGINES = {
    "ai_mode": ("https://api.dataforseo.com/v3/serp/google/ai_mode", "Google AI Mode"),
    "chatgpt": ("https://api.dataforseo.com/v3/ai_optimization/chat_gpt/llm_scraper", "ChatGPT"),
    "gemini": ("https://api.dataforseo.com/v3/ai_optimization/gemini/llm_scraper", "Gemini"),
}
PRICE = 0.0012  # standard queue, per query per engine (DataForSEO pricing, Nov 2026)


def host(u):
    h = urlparse(u if "//" in u else "https://" + u).netloc.lower()
    return h[4:] if h.startswith("www.") else h


def cited_urls(task):
    """Every URL in the answer (sources, references, links); domain-level match is done separately."""
    return {u for u in rc.urls_in(task.get("result") or []) if not u.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif"))}


def verdict(page_url, urls):
    if any(rc.match(page_url, u) for u in urls):
        return "cited"
    if host(page_url) and any(host(u) == host(page_url) for u in urls):
        return "platform cited"
    return "not cited"


def run_engine(engine, queries, loc, lang, login, password, wait_min):
    base = ENGINES[engine][0]
    body = [{"keyword": q, "location_code": loc, "language_code": lang, "tag": q} for q in queries]
    ids, out = {}, {}
    for i in range(0, len(body), 100):
        d = rc.call("POST", "/task_post", login, password, body[i:i + 100], base=base)
        for t in d.get("tasks") or []:
            if t.get("id"):
                ids[t["id"]] = (t.get("data") or {}).get("keyword", "").lower()
            elif t.get("status_code") != 20100:
                print(f"- {ENGINES[engine][1]}: task refused ({t.get('status_code')} {t.get('status_message')})")
    print(f"- {ENGINES[engine][1]}: {len(ids)} tasks queued, waiting (usually a few minutes, up to 45)…")
    deadline = time.time() + wait_min * 60
    while ids and time.time() < deadline:
        time.sleep(20)
        ready = rc.call("GET", "/tasks_ready", login, password, base=base)
        for t in ready.get("tasks") or []:
            for r in t.get("result") or []:
                tid = r.get("id")
                if tid in ids:
                    g = rc.call("GET", f"/task_get/advanced/{tid}", login, password, base=base)
                    for tt in g.get("tasks") or []:
                        out[ids[tid]] = cited_urls(tt)
                    ids.pop(tid)
    if ids:
        print(f"- {ENGINES[engine][1]}: {len(ids)} tasks not ready yet (paid, kept 30 days). Run again later with the same queries "
              f"— or open them in the DataForSEO dashboard.")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("journal")
    ap.add_argument("--engines", default="ai_mode", help="comma list: ai_mode,chatgpt,gemini (default ai_mode)")
    ap.add_argument("--country", default="us"); ap.add_argument("--language", default="en")
    ap.add_argument("--platform"); ap.add_argument("--topic")
    ap.add_argument("--priority", choices=w.PRIORITIES)
    ap.add_argument("--limit", type=int, default=50, help="max queries per run")
    ap.add_argument("--wait", type=int, default=20, help="minutes to wait for the standard queue")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--from-json", help="parse a saved DataForSEO response (with --engine) instead of calling the API")
    ap.add_argument("--engine", choices=list(ENGINES), help="engine of the --from-json file")
    ap.add_argument("--auth-fd", help=argparse.SUPPRESS)
    a = ap.parse_args()

    engines = [e.strip() for e in a.engines.split(",") if e.strip()]
    bad = [e for e in engines if e not in ENGINES]
    if bad:
        sys.exit("Unknown engine: " + ", ".join(bad) + ". Use: " + ", ".join(ENGINES))
    if a.from_json:
        if not a.engine:
            sys.exit("--from-json needs --engine")
        engines = [a.engine]
    loc = rc.COUNTRIES.get(a.country.lower())
    if not loc:
        sys.exit("Unknown --country. Use one of: " + ", ".join(sorted(rc.COUNTRIES)))

    today = date.today()
    pages = w.page_states(w.read_rows(a.journal), today)
    by_q, skipped = defaultdict(list), 0
    for p in pages.values():
        if p["moved"] or w.health(p) in w.GONE:
            continue
        if a.platform and p["platform"].lower() != a.platform.lower():
            continue
        if a.priority and p["priority"] != a.priority:
            continue
        if a.topic and a.topic.lower() not in p["topic_key"]:
            continue
        q = rc.query_of(p)
        if q:
            by_q[q.lower()].append(p)
        else:
            skipped += 1
    queries = sorted(by_q, key=lambda q: min(w.PRIORITIES.index(p["priority"]) for p in by_q[q]))[: a.limit]
    cost = len(queries) * len(engines) * PRICE
    print(f"AI visibility check · {', '.join(ENGINES[e][1] for e in engines)} · {a.country} · {len(queries)} queries for "
          f"{sum(len(by_q[q]) for q in queries)} pages · " + (f"about ${cost:.2f}" if cost >= 0.01 else "under $0.01"))
    if skipped:
        print(f"- {skipped} pages have no query or named topic: set them with `worklog.py tag --query` first")
    if a.dry_run or not queries:
        for q in queries[:30]:
            print(f"  · {q} ({len(by_q[q])} pages)")
        return

    results = {}
    if a.from_json:
        data = json.load(open(a.from_json))
        results[a.engine] = {((t.get("data") or {}).get("keyword") or "").lower(): cited_urls(t) for t in data.get("tasks") or []}
    else:
        login, password = rc.read_auth(a.auth_fd)
        if not (login and password):
            sys.exit(rc.NO_CREDS)
        for e in engines:
            results[e] = run_engine(e, queries, loc, a.language, login, password, a.wait)

    rows, lines, platform_hits = [], defaultdict(list), defaultdict(set)
    d = today.isoformat()
    for e, res in results.items():
        for q in queries:
            if q not in res:
                continue
            for p in by_q[q]:
                v = verdict(p["url"], res[q])
                rows.append(w.journal_row(date=d, event="check", page_url=p["url"], platform=p["platform"],
                                          main_query=q, note=f"ai: {q} · {e} {a.country} · {v}"))
                lines[v].append(f"{w.short(p['url'], 50)} · {q} · {ENGINES[e][1]}")
            for u in res[q]:
                platform_hits[host(u)].add(e)
    if rows:
        w.append(a.journal, w.COLUMNS, rows)
    print(f"- {len(rows)} checks · cited {len(lines['cited'])} · platform cited {len(lines['platform cited'])} · "
          f"not cited {len(lines['not cited'])}")
    for v, title in (("cited", "Your page is cited"), ("platform cited", "Your platform is cited (another page of it)")):
        if lines[v]:
            print(f"\n**{title}**")
            for line in lines[v][:25]:
                print("- " + line)
    mine = {host(p["platform"]) for p in pages.values() if p["platform"]}
    other = sorted(((len(es), h) for h, es in platform_hits.items() if h and h not in mine), reverse=True)[:15]
    if other:
        print("\n**Other domains these AIs cite for your queries** (platform ideas — check the rules before posting)")
        for n, h in other:
            print(f"- {h} ({n} engine{'s' if n > 1 else ''})")


if __name__ == "__main__":
    main()
