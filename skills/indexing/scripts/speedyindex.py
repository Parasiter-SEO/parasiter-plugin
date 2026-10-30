#!/usr/bin/env python3
"""SpeedyIndex API helper for the PARASITER indexing skill (API docs: https://en.speedyindex.com/api.html).

The key is read from the environment (SPEEDYINDEX_API_KEY), never from the command line or a file.

  python3 speedyindex.py balance
  python3 speedyindex.py send urls.txt [--title "pack oct"] [--drip-days 3]
  python3 speedyindex.py status TASK_ID [TASK_ID ...]
  python3 speedyindex.py report TASK_ID
  python3 speedyindex.py check urls.txt            # index-checker task (Google)

urls.txt: one URL per line (blank lines and # comments ignored). Prints JSON from the API.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

HOST = os.environ.get("SPEEDYINDEX_HOST", "https://api.speedyindex.com").rstrip("/")
CODES = {0: "ok", 1: "insufficient balance — top up tokens in the bot or dashboard", 2: "validation error"}


def key():
    k = os.environ.get("SPEEDYINDEX_API_KEY", "").strip()
    if not k:
        sys.exit("SPEEDYINDEX_API_KEY is not set. Put your key from @SpeedyIndexBot or the dashboard in the environment.")
    return k


def call(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(HOST + path, data=data, method=method,
                                 headers={"Authorization": key(), "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            out = json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode()[:300]}")
    except urllib.error.URLError as e:
        sys.exit(f"Can't reach {HOST}: {e.reason}")
    code = out.get("code")
    if code not in (None, 0):
        sys.exit(f"SpeedyIndex error {code}: {CODES.get(code, 'see API docs')} · {json.dumps(out)[:300]}")
    return out


def read_urls(path):
    urls, seen = [], set()
    for line in open(path, encoding="utf-8"):
        u = line.strip()
        if u and not u.startswith("#") and u.startswith("http") and u not in seen:
            seen.add(u)
            urls.append(u)
    if not urls:
        sys.exit("No URLs in the file.")
    if len(urls) > 10000:
        sys.exit("Max 10,000 URLs per task — split the list.")
    return urls


def task_body(urls, title, drip):
    body = {"title": title or "PARASITER", "urls": urls, "pay_per_indexed": True}
    if drip:
        if not 2 <= drip <= 30 or len(urls) < drip:
            sys.exit("--drip-days must be 2–30 and not more than the number of URLs.")
        body.update(drip_feed=True, drip_feed_days=drip)
    return body


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("balance")
    s = sub.add_parser("send"); s.add_argument("file"); s.add_argument("--title"); s.add_argument("--drip-days", type=int)
    st = sub.add_parser("status"); st.add_argument("task_ids", nargs="+")
    rp = sub.add_parser("report"); rp.add_argument("task_id")
    ck = sub.add_parser("check"); ck.add_argument("file"); ck.add_argument("--title")
    a = ap.parse_args()
    if a.cmd == "balance":
        out = call("GET", "/v2/account")
    elif a.cmd == "send":
        urls = read_urls(a.file)
        out = call("POST", "/v2/task/google/indexer/create", task_body(urls, a.title, a.drip_days))
        out["_sent"] = len(urls)
    elif a.cmd == "status":
        out = call("POST", "/v2/task/google/indexer/status", {"task_ids": a.task_ids[:1000]})
    elif a.cmd == "report":
        out = call("POST", "/v2/task/google/indexer/fullreport", {"task_id": a.task_id})
    else:
        urls = read_urls(a.file)
        out = call("POST", "/v2/task/google/checker/create", {"title": a.title or "PARASITER check", "urls": urls})
        out["_sent"] = len(urls)
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
