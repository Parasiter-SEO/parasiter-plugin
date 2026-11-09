#!/usr/bin/env python3
"""PARASITER — position check for the user's own pages through DataForSEO or SerpApi (Google or Bing organic).

  rankcheck.py JOURNAL [--provider dataforseo|serpapi] [--engine google|bing] [--country us] [--language en] [--depth 100] [--platform P] [--priority high]
               [--topic TEXT] [--limit N] [--live] [--dry-run] [--from-json FILE]

Credentials: from the plugin settings only — the bundled parasiter-dataforseo server (dataforseo_run tool)
or parasiter-serpapi server (serpapi_run tool, --provider serpapi) passes them through an inherited pipe (--auth-fd). Never from files, arguments or the chat.
Never written to any file. One SERP request per unique query; every page of the user found in
the results gets its position. Results go into the journal as `check` rows (position, status
indexed when found) with the note "rank: <query> · google <country>"; pages not found get
"not in top N". Standard queue (cheapest) by default; --live answers at once at a higher price.
--engine bing: Bing positions (Bing results feed ChatGPT search and Copilot). Bing rows carry no
position/status columns (those stay Google's): the note says "rank: <query> · bing <country> <device> · bing #N"
or "· bing out of top N", and worklog keeps it as bing_pos.
--provider serpapi: the user's own SerpApi key (free plan: 250 searches a month). SerpApi returns 10
Google results per search, so top 30 = 3 searches per query (fewer when the results run out); Bing up
to 50 results in one search. Answers at once (no queue, no --collect).
"""
import math
import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import worklog as w  # noqa: E402

API = "https://api.dataforseo.com/v3/serp/google/organic"
ENGINES = ("google", "bing")
COUNTRIES = {"us": 2840, "uk": 2826, "gb": 2826, "ca": 2124, "au": 2036, "nz": 2554, "ie": 2372,
             "in": 2356, "de": 2276, "fr": 2250, "es": 2724, "it": 2380, "nl": 2528, "br": 2076,
             "mx": 2484, "pl": 2616, "ua": 2804, "za": 2710, "sg": 2702, "ph": 2608}


NO_CREDS = ("DataForSEO is not set up for this run: add your API login and password in the PARASITER plugin settings "
            "(/plugin → PARASITER → configure options) and run paid checks through the dataforseo_run tool.")


def read_auth(fd):
    """Login and password handed over by the parasiter-dataforseo server through an inherited pipe."""
    if fd is None:
        return None, None
    try:
        data = os.read(int(fd), 4096).decode()
        os.close(int(fd))
    except OSError:
        return None, None
    login, _, password = data.partition("\n")
    return login.strip() or None, password.strip() or None


def call(method, path, login, password, body=None, base=None, tries=8):
    """API call with retries: right after account verification DataForSEO answers 40104 on some
    requests for a while; network hiccups and 5xx are retried too."""
    for i in range(tries):
        data = _call(method, path, login, password, body, base)
        code = data.get("status_code")
        if code == 20000 or code not in (40104, 50000, 50301, 50401) or i == tries - 1:
            break
        time.sleep(3 + 2 * i)
    if data.get("status_code") != 20000:
        sys.exit(f"DataForSEO error {data.get('status_code')}: {data.get('status_message')}")
    return data


def _call(method, path, login, password, body=None, base=None):
    req = urllib.request.Request((base or API) + path, method=method,
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
    return data


SERPAPI = "https://serpapi.com/search.json"
SERPAPI_GL = {"uk": "gb"}
SERPAPI_SKIP = {"organic_results", "search_metadata", "search_parameters", "search_information",
                "pagination", "serpapi_pagination", "ads", "shopping_results"}
NO_SERPAPI = ("SerpApi is not set up for this run: add your SerpApi API key in the PARASITER plugin settings "
              "(/plugin → PARASITER → configure options) and run checks through the serpapi_run tool.")


def serpapi_searches(depth, engine):
    """Searches one query costs on SerpApi: Google gives 10 results per search, Bing up to 50."""
    return 1 if engine == "bing" else max(1, math.ceil(depth / 10))


def serpapi_get(params, key):
    url = SERPAPI + "?" + urllib.parse.urlencode({**params, "api_key": key, "output": "json"})
    try:
        with urllib.request.urlopen(urllib.request.Request(url), timeout=90) as r:
            data = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            msg = json.loads(e.read().decode()).get("error") or e.reason
        except Exception:
            msg = e.reason
        hint = {401: " Check the SerpApi key in the plugin settings.",
                429: " Your SerpApi searches for this month are used up or the hourly limit is reached."}.get(e.code, "")
        sys.exit(f"SerpApi HTTP {e.code}: {msg}.{hint}")
    except urllib.error.URLError as e:
        sys.exit(f"Can't reach serpapi.com ({e.reason}). Allow the domain in your assistant's network settings.")
    if data.get("error") and not data.get("organic_results"):
        if "hasn't returned any results" in data["error"]:
            return data
        sys.exit(f"SerpApi error: {data['error']}")
    return data


def serpapi_parse(responses):
    """Organic (position, url) and non-organic (block, url) from one query's SerpApi pages, in order."""
    items, feats, n = [], [], 0
    for d in responses:
        for it in d.get("organic_results") or []:
            n += 1
            if it.get("link"):
                items.append((n, it["link"]))
        for k, v in d.items():
            if k not in SERPAPI_SKIP:
                feats += [(k, u) for u in set(urls_in(v))]
    return items, feats


def serpapi_query(q, key, a):
    base = {"engine": a.engine, "q": q}
    if a.engine == "bing":
        base.update({"cc": a.country.upper(), "count": min(a.depth, 50)})
        if a.device == "mobile":
            base["device"] = "mobile"
        return [serpapi_get(base, key)]
    base.update({"gl": SERPAPI_GL.get(a.country.lower(), a.country.lower()), "hl": a.language,
                 "device": a.device, "num": 10})
    out = []
    for start in range(0, a.depth, 10):
        d = serpapi_get({**base, "start": start}, key)
        out.append(d)
        if len(d.get("organic_results") or []) < 5 or not (d.get("serpapi_pagination") or {}).get("next"):
            break
    return out


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


def urls_in(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from urls_in(v)
    elif isinstance(o, list):
        for v in o:
            yield from urls_in(v)
    elif isinstance(o, str) and o.startswith("http"):
        yield o


def serp_features(task):
    """Non-organic blocks that cite pages: AI Overview, Discussions and forums, videos, PAA…"""
    out = []
    for res in task.get("result") or []:
        for it in res.get("items") or []:
            if it.get("type") != "organic":
                out += [(it.get("type"), u) for u in set(urls_in(it))]
    return out


def match(page_url, serp_url):
    a, b = w.norm_url(page_url), w.norm_url(serp_url)
    return a == b or b.startswith(a + "/") or a.startswith(b + "/")


def main():
    ap = argparse.ArgumentParser(description="Position check of the user's pages (DataForSEO or SerpApi)")
    ap.add_argument("journal")
    ap.add_argument("--provider", default="dataforseo", choices=["dataforseo", "serpapi"],
                    help="whose account pays: dataforseo (default) or serpapi")
    ap.add_argument("--engine", default="google", choices=ENGINES, help="google (default) or bing")
    ap.add_argument("--country", default="us"); ap.add_argument("--language", default="en")
    ap.add_argument("--depth", type=int, default=None, help="results to check; DataForSEO default 30 (billed per 10), SerpApi default 10 (1 search per 10)")
    ap.add_argument("--device", default="desktop", choices=["desktop", "mobile"])
    ap.add_argument("--platform"); ap.add_argument("--topic")
    ap.add_argument("--priority", choices=w.PRIORITIES)
    ap.add_argument("--limit", type=int, default=200, help="max queries per run")
    ap.add_argument("--live", action="store_true"); ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--auth-fd", help=argparse.SUPPRESS)
    ap.add_argument("--from-json", help="parse a saved DataForSEO response (SerpApi: a list of saved responses) instead of calling the API")
    ap.add_argument("--wait", type=int, default=15, help="minutes to wait for the standard queue")
    ap.add_argument("--skip-today", action="store_true", help="skip pages already rank-checked today")
    ap.add_argument("--collect", type=int, metavar="HOURS",
                    help="don't post new tasks: download results of tasks already paid in the last HOURS (free)")
    a = ap.parse_args()
    if a.depth is None:
        a.depth = 10 if a.provider == "serpapi" else 30

    today = date.today()
    rows_all = w.read_rows(a.journal)
    pages = w.page_states(rows_all, today)
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
        if q and a.skip_today and any(r for r in rows_all if r.get("page_url") == p["url"] and r["event"] == "check"
                                      and r["_d"] == today and (r.get("note") or "").startswith("rank:")
                                      and ((" · bing " in r["note"]) == (a.engine == "bing"))):
            continue
        (by_q[q.lower()].append(p) if q else skipped.append(p))
    queries = sorted(by_q, key=lambda q: min(w.PRIORITIES.index(p["priority"]) for p in by_q[q]))[: a.limit]
    results, feats = {}, {}
    loc = COUNTRIES.get(a.country.lower())
    if not loc:
        sys.exit("Unknown --country. Use one of: " + ", ".join(sorted(COUNTRIES)))
    bing = a.engine == "bing"
    if a.provider == "serpapi":
        if a.collect:
            sys.exit("--collect is for DataForSEO only: SerpApi answers at once, there is nothing to collect.")
        per = serpapi_searches(a.depth, a.engine)
        print(f"Position check · SerpApi · {a.engine} {a.country} · top {a.depth} · {len(queries)} queries for "
              f"{sum(len(by_q[q]) for q in queries)} pages · up to {len(queries) * per} SerpApi searches "
              f"({per} per query; the free plan has 250 a month)"
              + ("" if bing or per == 1 else f" · top 10 only: --depth 10, {len(queries)} searches"))
        if skipped:
            print(f"- {len(skipped)} pages have no query or named topic: set them with `worklog.py tag --query` first")
        if a.dry_run or not queries:
            for q in queries[:30]:
                print(f"  · {q} ({len(by_q[q])} pages)")
            return
        if a.from_json:
            for d in json.load(open(a.from_json)):
                q = ((d.get("search_parameters") or {}).get("q") or "").lower()
                results.setdefault(q, []).append(d)
            for q in list(results):
                results[q], feats[q] = serpapi_parse(results[q])
        else:
            key, _ = read_auth(a.auth_fd)
            if not key:
                sys.exit(NO_SERPAPI)
            used = 0
            for q in queries:
                pages_ = serpapi_query(q, key, a)
                used += len(pages_)
                results[q], feats[q] = serpapi_parse(pages_)
            print(f"- {used} SerpApi searches used")
        return report(a, today, pages, queries, by_q, results, feats, bing)
    # DataForSEO bills per 10 results: top 100 = 10 pages of results
    price = (0.002 if a.live else 0.0006) * max(1, a.depth / 10)
    api = API.replace("/google/", f"/{a.engine}/")
    globals()["API"] = api          # call() defaults to API
    print(f"Position check · {a.engine} {a.country} · top {a.depth} · {len(queries)} queries for "
          f"{sum(len(by_q[q]) for q in queries)} pages · about ${len(queries) * price:.2f}"
          + ("" if a.collect else f" (top 10 only: --depth 10, about ${len(queries) * price / max(1, a.depth / 10):.2f})"))
    if skipped:
        print(f"- {len(skipped)} pages have no query or named topic: set them with `worklog.py tag --query` first")
    if a.dry_run or (not queries and not a.collect):
        for q in queries[:30]:
            print(f"  · {q} ({len(by_q[q])} pages)")
        return

    login, password = read_auth(a.auth_fd)
    if a.collect:
        if not (login and password):
            sys.exit(NO_CREDS)
        from datetime import datetime, timedelta, timezone
        now = datetime.now(timezone.utc)
        fmt_ = "%Y-%m-%d %H:%M:%S +00:00"
        req = [{"datetime_from": (now - timedelta(hours=a.collect)).strftime(fmt_),
                "datetime_to": now.strftime(fmt_), "limit": 1000, "include_metadata": True}]
        d = call("POST", "/id_list", login, password, req, base="https://api.dataforseo.com/v3/serp")
        ids = [x["id"] for t in d.get("tasks") or [] for x in (t.get("result") or [])
               if f"{a.engine}/organic/task_post" in (x.get("url") or "")]
        print(f"- {len(ids)} paid tasks from the last {a.collect} h: downloading results (free)")
        for tid in ids:
            g = call("GET", f"/task_get/advanced/{tid}", login, password)
            for tt in g.get("tasks") or []:
                kw = ((tt.get("data") or {}).get("keyword") or "").lower()
                if tt.get("result") and kw:
                    results[kw] = serp_items(tt)
                    feats[kw] = serp_features(tt)
        queries = [q for q in by_q if q in results]
        print(f"- results for {len(queries)} of your queries")
    elif a.from_json:
        data = json.load(open(a.from_json))
        for t in data.get("tasks") or []:
            kw = ((t.get("data") or {}).get("keyword") or "").lower()
            results[kw] = serp_items(t)
    else:
        if not (login and password):
            sys.exit(NO_CREDS)
        body = [{"keyword": q, "location_code": loc, "language_code": a.language, "depth": a.depth,
                 "device": a.device, "tag": q} for q in queries]
        if a.live:
            for chunk in [body[i:i + 1] for i in range(len(body))]:  # live: one task per request
                d = call("POST", "/live/advanced", login, password, chunk)
                for t in d.get("tasks") or []:
                    k_ = (t.get("data") or {}).get("keyword", "").lower()
                    results[k_] = serp_items(t)
                    feats[k_] = serp_features(t)
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
                                feats[ids[tid]] = serp_features(tt)
                            ids.pop(tid)
            if ids:
                print(f"- {len(ids)} tasks not ready yet: they are paid and kept 3 days. Later run with --collect 24 to download them for free.")

    return report(a, today, pages, queries, by_q, results, feats, bing)


def report(a, today, pages, queries, by_q, results, feats, bing):
    """Journal rows and the summary, the same for every provider."""
    rows, found, top, found_feat, bing_moves = [], 0, 0, [], []
    d = today.isoformat()
    for q in queries:
        if q not in results:
            continue
        items = results[q]
        for p in by_q[q]:
            pos = next((rk for rk, u in items if match(p["url"], u)), None)
            cited = sorted({ty for ty, u in feats.get(q, []) if match(p["url"], u)})
            note = f"rank: {q} · {a.engine} {a.country} {a.device}" + (f" · cited in {', '.join(cited)}" if cited else "")
            if bing:  # Bing rows never touch the Google position/status columns
                prev = pages[p["url"]].get("bing_pos")
                note += f" · bing #{pos}" if pos is not None else f" · bing out of top {a.depth}"
                found += pos is not None
                top += pos is not None and pos <= w.TOP
                rows.append(w.journal_row(date=d, event="check", page_url=p["url"], platform=p["platform"],
                                          main_query=q, note=note))
                bing_moves.append((prev, pos, p, q))
                continue
            if cited:
                found_feat.append(f"{w.short(p['url'], 50)} · {q}: {', '.join(cited)}")
            if pos is not None:
                found += 1
                top += pos <= w.TOP
                rows.append(w.journal_row(date=d, event="check", page_url=p["url"], platform=p["platform"],
                                          status="indexed", position=pos, main_query=q, note=note))
            elif cited:  # not in organic results, but Google shows it in a SERP block: it is indexed
                rows.append(w.journal_row(date=d, event="check", page_url=p["url"], platform=p["platform"],
                                          status="indexed", main_query=q, note=note + f" · not in organic top {a.depth}"))
            else:
                rows.append(w.journal_row(date=d, event="check", page_url=p["url"], platform=p["platform"],
                                          main_query=q, note=note + f" · not in top {a.depth}"))
    if rows:
        w.append(a.journal, w.COLUMNS, rows)
    print(f"- {len(rows)} pages checked on {a.engine.title()}{' (SerpApi)' if a.provider == 'serpapi' else ''} · {found} found in the top {a.depth} · {top} in the top {w.TOP}")
    if found_feat:
        print("\n**Cited in SERP blocks (AI Overview, forums, videos…)**")
        for line in found_feat[:25]:
            print("- " + line)
    if bing:
        out = []
        for prev, pos, p, q in bing_moves:
            if prev != pos and (prev is not None or (pos is not None and pos <= w.TOP)):
                out.append(f"{w.short(p['url'], 50)} · {q}: Bing {prev if prev is not None else '—'} → {pos if pos is not None else f'out of top {a.depth}'}")
        if out:
            print("\n**Bing changes since the last check**")
            for line in out[:25]:
                print("- " + line)
        return
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
