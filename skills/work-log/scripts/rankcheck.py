#!/usr/bin/env python3
"""PARASITER — position check for the user's own pages through DataForSEO (Google organic).

  rankcheck.py JOURNAL [--country us] [--language en] [--depth 100] [--platform P] [--priority high]
               [--topic TEXT] [--limit N] [--live] [--dry-run] [--from-json FILE]

Credentials: env DATAFORSEO_LOGIN / DATAFORSEO_PASSWORD, or --login / --password.
Never written to any file. One SERP request per unique query; every page of the user found in
the results gets its position. Results go into the journal as `check` rows (position, status
indexed when found) with the note "rank: <query> · google <country>"; pages not found get
"not in top N". Standard queue (cheapest) by default; --live answers at once at a higher price.
"""
import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import worklog as w  # noqa: E402

API = "https://api.dataforseo.com/v3/serp/google/organic"
COUNTRIES = {"us": 2840, "uk": 2826, "gb": 2826, "ca": 2124, "au": 2036, "nz": 2554, "ie": 2372,
             "in": 2356, "de": 2276, "fr": 2250, "es": 2724, "it": 2380, "nl": 2528, "br": 2076,
             "mx": 2484, "pl": 2616, "ua": 2804, "za": 2710, "sg": 2702, "ph": 2608}


def call(method, path, login, password, body=None):
    req = urllib.request.Request(API + path, method=method,
                                 data=json.dumps(body).encode() if body is not None else None)
    tok = base64.b64encode(f"{login}:{password}".encode()).decode()
    req.add_header("Authorization", "Basic " + tok)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            data = json.loads(e.read().decode())
        except Exception:
            sys.exit(f"DataForSEO HTTP {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        sys.exit(f"Can't reach api.dataforseo.com ({e.reason}). Allow the domain in your assistant's network settings.")
    if data.get("status_code") != 20000:
        sys.exit(f"DataForSEO error {data.get('status_code')}: {data.get('status_message')}")
    return data


def query_of(p):
    q = (p.get("query") or "").strip()
    if q:
        return q
    t = p.get("topic_key") or ""
    return "" if t.startswith("~") or " · " in t else t


def serp_items(task):
    out = []
    for res in task.get("result") or []:
        for it in res.get("items") or []:
            if it.get("type") == "organic" and it.get("url"):
                out.append((it.get("rank_group") or it.get("rank_absolute"), it["url"]))
    return out


def match(page_url, serp_url):
    a, b = w.norm_url(page_url), w.norm_url(serp_url)
    return a == b or b.startswith(a + "/") or a.startswith(b + "/")


def main():
    ap = argparse.ArgumentParser(description="Position check of the user's pages (DataForSEO)")
    ap.add_argument("journal")
    ap.add_argument("--country", default="us"); ap.add_argument("--language", default="en")
    ap.add_argument("--depth", type=int, default=100)
    ap.add_argument("--platform"); ap.add_argument("--topic")
    ap.add_argument("--priority", choices=w.PRIORITIES)
    ap.add_argument("--limit", type=int, default=200, help="max queries per run")
    ap.add_argument("--live", action="store_true"); ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--login"); ap.add_argument("--password")
    ap.add_argument("--from-json", help="parse a saved DataForSEO response instead of calling the API")
    ap.add_argument("--wait", type=int, default=15, help="minutes to wait for the standard queue")
    a = ap.parse_args()

    today = date.today()
    pages = w.page_states(w.read_rows(a.journal), today)
    by_q, skipped = defaultdict(list), []
    for p in pages.values():
        if p["moved"] or w.health(p) in w.GONE:
            continue
        if a.platform and p["platform"].lower() != a.platform.lower():
            continue
        if a.priority and p["priority"] != a.priority:
            continue
        if a.topic and a.topic.lower() not in p["topic_key"]:
            continue
        q = query_of(p)
        (by_q[q.lower()].append(p) if q else skipped.append(p))
    queries = sorted(by_q, key=lambda q: min(w.PRIORITIES.index(p["priority"]) for p in by_q[q]))[: a.limit]
    loc = COUNTRIES.get(a.country.lower())
    if not loc:
        sys.exit("Unknown --country. Use one of: " + ", ".join(sorted(COUNTRIES)))
    price = 0.002 if a.live else 0.0006
    print(f"Position check · google {a.country} · top {a.depth} · {len(queries)} queries for "
          f"{sum(len(by_q[q]) for q in queries)} pages · about ${len(queries) * price * max(1, a.depth / 100):.2f}")
    if skipped:
        print(f"- {len(skipped)} pages have no query or named topic: set them with `worklog.py tag --query` first")
    if a.dry_run or not queries:
        for q in queries[:30]:
            print(f"  · {q} ({len(by_q[q])} pages)")
        return

    results = {}
    if a.from_json:
        data = json.load(open(a.from_json))
        for t in data.get("tasks") or []:
            kw = ((t.get("data") or {}).get("keyword") or "").lower()
            results[kw] = serp_items(t)
    else:
        login = a.login or os.environ.get("DATAFORSEO_LOGIN")
        password = a.password or os.environ.get("DATAFORSEO_PASSWORD")
        if not (login and password):
            sys.exit("No DataForSEO credentials: set DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD (API login and password from app.dataforseo.com → API Access).")
        body = [{"keyword": q, "location_code": loc, "language_code": a.language, "depth": a.depth,
                 "tag": q} for q in queries]
        if a.live:
            for chunk in [body[i:i + 1] for i in range(len(body))]:  # live: one task per request
                d = call("POST", "/live/advanced", login, password, chunk)
                for t in d.get("tasks") or []:
                    results[(t.get("data") or {}).get("keyword", "").lower()] = serp_items(t)
        else:
            ids = {}
            for i in range(0, len(body), 100):
                d = call("POST", "/task_post", login, password, body[i:i + 100])
                for t in d.get("tasks") or []:
                    if t.get("id"):
                        ids[t["id"]] = (t.get("data") or {}).get("keyword", "").lower()
            print(f"- {len(ids)} tasks queued, waiting for results (usually 1–5 minutes)…")
            deadline = time.time() + a.wait * 60
            while ids and time.time() < deadline:
                time.sleep(20)
                ready = call("GET", "/tasks_ready", login, password)
                for t in ready.get("tasks") or []:
                    for r in t.get("result") or []:
                        tid = r.get("id")
                        if tid in ids:
                            g = call("GET", f"/task_get/advanced/{tid}", login, password)
                            for tt in g.get("tasks") or []:
                                results[ids[tid]] = serp_items(tt)
                            ids.pop(tid)
            if ids:
                print(f"- {len(ids)} tasks not ready yet: run again later, they are paid already and kept 3 days by DataForSEO.")

    rows, found, top = [], 0, 0
    d = today.isoformat()
    for q in queries:
        if q not in results:
            continue
        items = results[q]
        for p in by_q[q]:
            pos = next((rk for rk, u in items if match(p["url"], u)), None)
            note = f"rank: {q} · google {a.country}"
            if pos is not None:
                found += 1
                top += pos <= w.TOP
                rows.append(w.journal_row(date=d, event="check", page_url=p["url"], platform=p["platform"],
                                          status="indexed", position=pos, main_query=q, note=note))
            else:
                rows.append(w.journal_row(date=d, event="check", page_url=p["url"], platform=p["platform"],
                                          main_query=q, note=note + f" · not in top {a.depth}"))
    if rows:
        w.append(a.journal, w.COLUMNS, rows)
    print(f"- {len(rows)} pages checked · {found} found in the top {a.depth} · {top} in the top {w.TOP}")
    moves = []
    for r in rows:
        p = pages[r["page_url"]]
        old, new = p["position"], w.num(r["position"])
        if old is not None and new is not None and old != new:
            moves.append((new - old, f"{w.short(p['url'], 50)} · {r['main_query']}: {old:.0f} → {new:.0f}"))
        elif old is not None and new is None:
            moves.append((999, f"{w.short(p['url'], 50)} · {r['main_query']}: {old:.0f} → out of top {a.depth}"))
        elif old is None and new is not None and new <= w.TOP:
            moves.append((-999, f"{w.short(p['url'], 50)} · {r['main_query']}: new in top {w.TOP}, #{new:.0f}"))
    if moves:
        print("\n**Changes since the last check**")
        for _, line in sorted(moves)[:25]:
            print("- " + line)


if __name__ == "__main__":
    main()
