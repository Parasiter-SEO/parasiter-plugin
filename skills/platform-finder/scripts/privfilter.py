"""PARASITER private filter, run locally.

Hides example posts that belong to PARASITER's author (his accounts, profile paths, topics, platforms)
without sending anything anywhere: the server gives salted hashes (`private_hashes`), this script
hashes the parts of each found URL on the user's machine and drops the matches.

Usage:
  python3 privfilter.py hashes.json urls.txt            # urls.txt: one URL per line (or "URL<TAB>product")
  python3 privfilter.py hashes.json urls.txt --out allowed.json
Prints {"allowed": [...], "hidden": N}. --self-test checks the matcher offline.
"""
import argparse
import hashlib
import json
import re
import sys
from urllib.parse import unquote, urlsplit

HASH_LEN = 20


def split_url(s):
    s = (s or "").strip().strip("<>")
    if not re.match(r"^[a-z][a-z0-9+.-]*://", s, re.I):
        s = "http://" + s
    try:
        p = urlsplit(s)
    except ValueError:
        return "", ""
    host = (p.hostname or "").lower().rstrip(".")
    host = host[4:] if host.startswith("www.") else host
    return host, p.path or ""


def slug(s):
    return re.sub(r"[^a-z0-9а-яіїєґ]+", " ", unquote(s or "").lower()).strip()


def candidates(url, product=""):
    """Every (kind, value) a URL could match. Must stay identical to the server's content.private_candidates."""
    host, path = split_url(url)
    if not host:
        return set()
    out = set()
    parts = host.split(".")
    hosts = [".".join(parts[i:]) for i in range(len(parts) - 1)]
    for h in hosts:
        out.add(("domain", h))
    segs = [x for x in path.lower().split("/") if x]
    for i in range(len(segs)):
        for j in range(i + 1, len(segs) + 1):
            out.add(("path", "/" + "/".join(segs[i:j])))
    for h in hosts:
        for j in range(1, len(segs) + 1):
            out.add(("path", h + "/" + "/".join(segs[:j])))
    for x in unquote(path).lower().split("/"):
        if x:
            out.add(("account", x.lstrip("@")))
    query = unquote(urlsplit(url if "://" in url else "http://" + url).query).lower()
    for x in re.split(r"[=&/@]", query):
        if x:
            out.add(("account", x))
    words = slug(path + " " + (product or "")).split()
    for i in range(len(words)):
        for j in range(i + 1, min(len(words), i + 8) + 1):
            out.add(("topic", " ".join(words[i:j])))
    return out


def phash(salt, kind, value):
    return hashlib.sha256(f"{salt}|{kind}|{value}".encode()).hexdigest()[:HASH_LEN]


def is_private(hashes, url, product=""):
    salt = hashes.get("salt", "")
    sets = {k: set(hashes.get(k) or []) for k in ("domain", "path", "account", "topic")}
    return any(phash(salt, k, v) in sets[k] for k, v in candidates(url, product))


def filter_urls(hashes, lines):
    allowed, hidden = [], 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        url, _, product = line.partition("\t")
        if is_private(hashes, url, product):
            hidden += 1
        else:
            allowed.append(url)
    return {"allowed": allowed, "hidden": hidden}


def self_test():
    salt = "t"
    h = {"salt": salt,
         "domain": [phash(salt, "domain", "hidden.example")],
         "path": [phash(salt, "path", "/members/ownernick"), phash(salt, "path", "forum.example/u/me")],
         "account": [phash(salt, "account", "ownernick")],
         "topic": [phash(salt, "topic", "secret pills")]}
    assert is_private(h, "https://sub.hidden.example/p")
    assert is_private(h, "https://devforum.example/members/ownernick/t/x")
    assert is_private(h, "https://www.forum.example/u/me/post-1")
    assert is_private(h, "https://other.example/secret-pills-honest-review")
    assert is_private(h, "https://x.example/t?user=ownernick")
    assert not is_private(h, "https://other.example/acme")
    assert not is_private(h, "https://notownernick.example/p")
    print("self-test ok")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("hashes", nargs="?")
    ap.add_argument("urls", nargs="?")
    ap.add_argument("--out")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if not a.hashes or not a.urls:
        ap.error("hashes.json and urls.txt are required")
    hashes = json.load(open(a.hashes, encoding="utf-8"))
    res = filter_urls(hashes, open(a.urls, encoding="utf-8").read().splitlines())
    text = json.dumps(res, ensure_ascii=False, indent=1)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(text)
    print(text if not a.out else f'allowed {len(res["allowed"])} · hidden {res["hidden"]} → {a.out}')


if __name__ == "__main__":
    sys.exit(main())
