#!/usr/bin/env python3
"""PARASITER — find the platforms where affiliate review pages are published and indexed right now.

  platformscan.py PRODUCTS [--provider dataforseo|serpapi] [--suffix review] [--country us] [--depth 10] [--device desktop]
                  [--base parasite-seo-progress.csv] [--out platforms-scan.csv] [--dry-run] [--live]
                  [--exclusions exclusions.json] [--exclude domain[/path],...] [--collect-only]
  platformscan.py --from-raw platforms-scan.raw.json [--allowed allowed.json] [--exclusions ...]
  platformscan.py --check-urls urls.txt [--out checks.csv]
  platformscan.py --verify candidates.tsv [--top 5] [--depth 10] [--dry-run] [--out platforms-verify.csv]
  platformscan.py --self-test

PRODUCTS: a text file with one affiliate product name per line (or a CSV with a product column),
or comma-separated names. For each product the script searches Google for "<product> review"
through the user's own DataForSEO account (paid: the cost is printed first, --dry-run prints only
the cost) or SerpApi account (--provider serpapi: searches from the monthly quota — the free plan
gives 250 a month; 1 search per query per 10 results) and collects every page in the results that is NOT the product's own site or a store.
Pages are grouped by platform: how many different products have review pages there, the platform
type and whether it is free (user posts) or paid (news / PR / sponsored).

After the paid search everything else is free:
- Exclusions: stop types and the blacklist (references/exclusions.md, merged with the server list
  passed by --exclusions = the saved answer of `exclusions_get`) and the known-dead platforms from
  the server are dropped before any check and only counted.
- Live check: up to 3 example pages per platform are opened. Two fields per page (№71):
  thread availability LIVE THREAD / REDIRECTED / REMOVED / FETCH BLOCKED / UNVERIFIED (404/410,
  "page removed" text, HTTP or client-side redirect — JavaScript or meta refresh — to the index,
  home or login page, empty stub, or the expected topic missing at the destination) and indexing
  eligibility INDEXABLE / NOINDEX / UNVERIFIED (meta robots / googlebot, X-Robots-Tag). An example
  counts as working only when it is LIVE THREAD and INDEXABLE.
  A platform passes only if at least one example is alive. Platforms whose examples are all
  removed are listed apart and their domains saved to platforms-scan-dead.txt (kept locally).
- Sign-up link: found on the home page or common paths (/register, /signup, /join…) and opened
  to check it works; otherwise "sign-up link not found" + the home page.
- Rows are post-first: Post · Product · Pos. · Platform · Type · Free/Paid · Sign-up.

With a PARASITER key, run in two steps so the author's private posts are never shown:
  1) --collect-only  → platforms-scan.raw.json + platforms-scan.examples.txt (URLs to filter)
  2) privfilter.py private-hashes.json <examples file> --out allowed.json (local, nothing is sent)
  3) --from-raw platforms-scan.raw.json --allowed allowed.json  (free: checks + output)

The point is not to find unknown platforms, but the ones where affiliate review pages are
already published AND indexed — proven places to post. Links on them don't matter; that the
page itself is in Google does.

Blocked hosts (№91): a page that answers 403 / 429 / a captcha / a timeout is not dropped. The script looks for
free evidence elsewhere — the RSS / Atom feed (the page's own feed link, <thread>.rss, /feed …), the sitemap
(robots.txt Sitemap lines, /sitemap.xml, one level of sitemap index) and the platform's public API where it has one
(Discourse /t/<id>.json, Flarum /api/discussions/<id>, Reddit .json, WordPress /wp-json) — and marks the page
"blocked — evidence from <source> (date)". Indexing stays unverified; an API that says the topic is gone marks it removed.

Targeted verification (№90) — between free discovery and a full paid SERP scan: --verify reads the hosted results
of a free search (URL<TAB>target query…), checks them free, ranks them (live and indexable first, forums and
communities, domains with several products) and picks only the top --top (default 5). For those only: a Google index
check (site:<url>) and the position for the target query on the user's own SerpApi / DataForSEO. --dry-run prints
the pick and "~N searches" / "~$X" first. Output keeps two lists apart: "Verified in Google" and
"Found in web search — not verified in Google".

Pattern search, method B (footprints): put one ready Google query per line in PRODUCTS
(e.g. inurl:/discuss "mitolyn") and pass --suffix "" — the lines are searched as they are.

Credentials: from the plugin settings via the dataforseo_run / serpapi_run tool (inherited pipe, --auth-fd). Never written anywhere.
Standard library only.
"""
import argparse
import csv
import fnmatch
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "work-log", "scripts"))
import rankcheck as rc  # noqa: E402
import worklog as w  # noqa: E402

# Stores and review aggregators: never a platform to publish on. Matched by host label / domain
# suffix, never by substring (№66: "google.com" as a substring removed sites.google.com).
STORE_BRANDS = ("amazon", "walmart", "ebay", "iherb", "vitaminshoppe", "costco", "aliexpress", "temu",
                "bestbuy", "trustpilot", "sitejabber")          # any host label: amazon.co.uk, smile.amazon.com
STORE_DOMAINS = ("target.com", "gnc.com", "etsy.com", "bbb.org", "apple.com",
                 "google.com", "play.google.com")               # the domain itself or its subdomains
# Google / Apple hosts where users publish: platforms, checked before the store rule
PUBLISHING_HOSTS = {"sites.google.com": "site-builder", "docs.google.com": "document",
                    "drive.google.com": "document", "groups.google.com": "community",
                    "discussions.apple.com": "community"}


def host_of(url):
    return re.sub(r"^(www|m)\.", "", (urllib.parse.urlsplit(url if "://" in url else "http://" + url).hostname or "").lower())


def suffix_match(host, domain):
    return host == domain or host.endswith("." + domain)


def is_store(host):
    labels = host.split(".")
    return any(b in labels for b in STORE_BRANDS) or any(suffix_match(host, d) for d in STORE_DOMAINS)
# news / PR / media: posting there is paid (sponsored post, press release, "partner content")
PAID_HINTS = ("news", "times", "post", "journal", "herald", "tribune", "gazette", "observer", "daily",
              "magazine", "mag.", "press", "wire", "media", "chronicle", "insider", "today", "weekly",
              "outlookindia", "hindustan", "deccan", "midday", "mid-day", "benzinga", "yahoo", "marketwatch",
              "globenewswire", "prnewswire", "accessnewswire", "einpresswire", "newswire", "openpr", "ibtimes",
              "sfgate", "seattlepi", "timesunion", "chron.com", "bostonglobe", "miamiherald", "kansascity",
              "tribuneindia", "thehindu", "ndtv", "livemint", "business-standard", "financialexpress",
              "outlook", "cnbc", "forbes", "entrepreneur", "observer.com")
FREE_TYPES = {"article", "community", "q&a", "blog", "site-builder", "page", "document", "social", "video",
              "fundraising", "event", "creator", "portfolio", "newsletter", "forum"}
# hidden upload forms and other people's file folders: abuse, never a platform to use
ABUSE = re.compile(r"(wp-content/uploads?|wpcf7|dndcf7|/uploads?/.*\.pdf$|formidable|gravity_forms|/sites/default/files/.*\.pdf$)", re.I)


def read_products(arg):
    if os.path.exists(arg):
        with open(arg, encoding="utf-8-sig") as f:
            text = f.read()
        if arg.lower().endswith(".csv"):
            rows = list(csv.DictReader(text.splitlines()))
            if rows:
                col = next((c for c in rows[0] if w.norm(c) in ("product", "productname", "name", "offer")), None)
                if col:
                    return [r[col].strip() for r in rows if r.get(col, "").strip()]
        names = [ln.split("#")[0].strip(" -•\t") for ln in text.splitlines()]
    else:
        names = [x.strip() for x in arg.split(",")]
    seen, out = set(), []
    for n in names:
        if n and not n.startswith("##") and n.lower() not in seen:
            seen.add(n.lower())
            out.append(n)
    return out


def brand_tokens(product):
    toks = [t for t in re.split(r"[^a-z0-9]+", product.lower()) if len(t) >= 3]
    return toks, re.sub(r"[^a-z0-9]", "", product.lower())


def is_brand_site(url, product):
    host = w.url_domain(url)
    toks, joined = brand_tokens(product)
    h = re.sub(r"[^a-z0-9]", "", host)
    return bool(joined and joined in h) or (len(toks) == 1 and toks[0] in h)


EXTRA_TYPES = {"hackmd.io": "page", "zooniverse.org": "community", "corada.com": "community",
               "gamma.app": "page",
               "firstory.me": "podcast", "spotify.com": "podcast",
               "bigcartel.com": "site-builder", "bandcamp.com": "creator", "soundcloud.com": "podcast",
               "kaggle.com": "community", "huggingface.co": "community", "gitlab.io": "site-builder",
               "pastebin.com": "page", "justpaste.it": "page", "rentry.co": "page", "glitch.me": "site-builder",
               "webflow.io": "site-builder", "carrd.co": "site-builder", "jimdosite.com": "site-builder",
               "strikingly.com": "site-builder", "ucoz": "site-builder", "tilda.ws": "site-builder"}
FREE_TYPES |= {"podcast"}


def classify(url):
    slug, dom, typ = w.platform_of(url)
    host = host_of(url)
    pub = next((d for d in PUBLISHING_HOSTS if suffix_match(host, d)), None)
    if pub:  # a publishing service on a big brand's domain: the service is the platform
        typ = typ or PUBLISHING_HOSTS[pub]
        return (slug if dom == pub else pub.split(".")[0] + "-" + pub.split(".")[1]), pub, typ, "free"
    typ = typ or next((t for d, t in EXTRA_TYPES.items() if suffix_match(host, d) or (d == "ucoz" and "ucoz" in host)), "")
    if not typ and urllib.parse.urlsplit(url).path.lower().endswith(".pdf"):
        typ = "document/pdf"  # PDFs are normal findings; the PDF's host is the platform
    low = dom.lower()
    if is_store(host):
        return slug, dom, typ, "store"
    if typ in FREE_TYPES or typ == "forum":
        return slug, dom, typ, "free"
    if any(h in low for h in PAID_HINTS):
        return slug, dom, typ or "news", "paid"
    if low.endswith((".edu", ".gov", ".ac.uk", ".edu.au", ".gov.uk")) or ".edu." in low or ".gov." in low:
        return slug, dom, typ or "institution", "check"
    return slug, dom, typ, "check"


# ---------- exclusions (№4) and known-dead platforms (№6) ----------

LOCAL_EXCLUSIONS = os.path.join(HERE, "..", "references", "exclusions.md")


def load_exclusions(server_json=None, extra=None, local=LOCAL_EXCLUSIONS):
    """{"stop": [(match, reason)], "black": [(match, reason)], "dead": {domain: since}}.
    The local copy (references/exclusions.md) is always loaded; the server answer of
    `exclusions_get` (saved as JSON) and the user's own --exclude entries are merged in."""
    ex = {"stop": [], "black": [], "dead": {}}
    section = None
    if os.path.exists(local):
        with open(local, encoding="utf-8") as f:
            for ln in f:
                low = ln.lower()
                if ln.startswith("## "):
                    section = "stop" if "stop" in low else "black" if "black" in low else None
                m = re.match(r"\|\s*`([^`]+)`\s*\|\s*(.*?)\s*\|\s*$", ln)
                if m and section:
                    ex[section].append((m.group(1).strip().lower(), m.group(2)))
    if server_json and os.path.exists(server_json):
        with open(server_json, encoding="utf-8") as f:
            d = json.load(f)
        for it in d.get("stop_types") or []:
            ex["stop"].append(((it.get("pattern") or "").lower(), it.get("reason", "")))
        for it in d.get("blacklist") or []:
            ex["black"].append(((it.get("match") or "").lower(), it.get("reason", "")))
        for it in d.get("dead") or []:
            if it.get("domain"):
                ex["dead"][it["domain"].lower().lstrip(".")] = it.get("since", "")
    for e in extra or []:
        if e.strip():
            ex["black"].append((e.strip().lower(), "your own exclusion"))
    for k in ("stop", "black"):
        seen, out = set(), []
        for m, r in ex[k]:
            if m and m not in seen:
                seen.add(m)
                out.append((m, r))
        ex[k] = out
    return ex


def host_path(url):
    sp = urllib.parse.urlsplit(url if "://" in url else "http://" + url)
    host = (sp.hostname or "").lower()
    host = re.sub(r"^(www|m)\.", "", host)
    return host, sp.path or "/"


def matches(url, match, typ=""):
    """Host equals or ends with the match's domain; a path in the match must prefix the URL path.
    `*` is a host wildcard; `type:<t>` matches the detected platform type."""
    if match.startswith("type:"):
        return bool(typ) and typ.lower() == match[5:]
    dom, _, path = match.partition("/")
    host, upath = host_path(url)
    if "*" in dom:
        ok = fnmatch.fnmatch(host, dom)
    else:
        ok = host == dom or host.endswith("." + dom)
    if not ok:
        return False
    return not path or upath.lower().startswith("/" + path.rstrip("/"))


def excluded(url, typ, ex):
    """('stop'|'black'|'dead', reason) or None."""
    for kind in ("stop", "black"):
        for m, reason in ex[kind]:
            if matches(url, m, typ):
                return kind, reason
    host, _ = host_path(url)
    for d in ex["dead"]:
        if host == d or host.endswith("." + d):
            return "dead", "known dead since " + (ex["dead"][d] or "?")
    return None


# ---------- free live check of example pages (№6) ----------

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
REMOVED_TEXT = re.compile(
    r"(page (was )?not found|page (you requested |you are looking for )?(could not be found|does ?n[o']t exist|no longer exists)"
    r"|(this|the) (page|post|topic|thread|story|article|content|document|profile|account) (has been|was|is) "
    r"(removed|deleted|suspended|unavailable|no longer available)"
    r"|(post|topic|thread|story|article|content|document) (has been |was )?(removed|deleted)( by| for)"
    r"|no longer available|content (is )?(not available|unavailable)|this account (has been|is) suspended"
    r"|requested (topic|thread|page) (does not exist|could not be found)|nothing (was )?found here"
    r"|sorry,? (that|this) page (doesn|does not|isn|is not))", re.I)
LOGIN_PATH = re.compile(r"(/login|/log-in|/signin|/sign-in|/sign_in|/auth|/account/login|/users/sign_in|/session)", re.I)
NOINDEX_META = re.compile(r"<meta[^>]+name=[\"'](robots|googlebot)[\"'][^>]*content=[\"'][^\"']*noindex", re.I)
NOINDEX_META2 = re.compile(r"<meta[^>]+content=[\"'][^\"']*noindex[^\"']*[\"'][^>]*name=[\"'](robots|googlebot)[\"']", re.I)


def visible_text(html):
    t = re.sub(r"(?is)<(script|style|noscript|svg|template)[^>]*>.*?</\1>", " ", html)
    t = re.sub(r"(?s)<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t).strip()


# №71 (beta report on v0.51.0): two separate fields for every example page.
#   availability: LIVE THREAD · REDIRECTED / REMOVED · FETCH BLOCKED · UNVERIFIED
#   indexing:     INDEXABLE · NOINDEX · UNVERIFIED
# HTTP 200 alone proves nothing: a ~80-byte page with window.location.href to the forum index is a dead
# thread. Client-side redirects (JavaScript, meta refresh) are followed one hop and the destination must
# still carry the expected discussion.
LIVE, GONE, BLOCKED, UNVER = "LIVE THREAD", "REDIRECTED / REMOVED", "FETCH BLOCKED", "UNVERIFIED"
INDEXABLE, NOINDEX = "INDEXABLE", "NOINDEX"
JS_REDIRECT = re.compile(r"""(?:window|document|top|self|parent)?\.?location(?:\.href)?\s*=\s*["']([^"']+)["']"""
                         r"""|location\.(?:replace|assign)\(\s*["']([^"']+)["']""", re.I)
META_TAG = re.compile(r"<meta\b[^>]*>", re.I)
BLOCK_TEXT = re.compile(r"(just a moment\.\.\.|checking your browser|cf-chl|attention required|access denied|"
                        r"enable javascript and cookies|verify you are (a )?human|captcha)", re.I)
INDEX_SEGMENTS = {"", "forum", "forums", "community", "board", "boards", "discussions", "discuss", "index.php",
                  "index.html", "home", "topics", "threads", "latest", "categories", "c", "t", "f"}
SLUG_STOP = {"the", "and", "for", "with", "that", "this", "from", "your", "you", "are", "was", "how", "what",
             "why", "does", "threads", "thread", "topic", "topics", "forum", "forums", "post", "posts", "index",
             "html", "php", "viewtopic", "showthread", "discussion", "discussions", "community", "page"}


def _attr(tag, name):
    m = re.search(name + r"""\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))""", tag, re.I)
    return (m.group(1) or m.group(2) or m.group(3) or "") if m else ""


def noindex_reason(headers, html):
    """'X-Robots-Tag' / 'meta robots' / '' — noindex or none for all bots or for Googlebot."""
    for part in re.split(r",(?=\s*[a-z0-9_-]+\s*:\s*[a-z])|\n", headers.get("x-robots-tag") or "", flags=re.I):
        m = re.match(r"\s*([a-z0-9_-]+)\s*:\s*([a-z].*)", part, re.I)
        bot, rules = (m.group(1).lower(), m.group(2)) if m and m.group(1).lower() != "unavailable_after" else ("", part)
        if bot in ("", "googlebot") and re.search(r"\b(noindex|none)\b", rules, re.I):
            return "X-Robots-Tag"
    for tag in META_TAG.findall(html):
        if _attr(tag, "name").lower() in ("robots", "googlebot") and re.search(r"\b(noindex|none)\b", _attr(tag, "content"), re.I):
            return "meta robots"
    return ""


def client_redirect(html, base_url):
    """Target URL of a meta refresh or a script redirect, or ''. A script redirect counts only on a stub
    page (little visible text): ordinary pages carry location.href in click handlers."""
    for tag in META_TAG.findall(html):
        if _attr(tag, "http-equiv").lower() == "refresh":
            m = re.search(r"url\s*=\s*['\"]?([^'\";]+)", _attr(tag, "content"), re.I)
            delay = re.match(r"\s*(\d+)", _attr(tag, "content"))
            if m and (not delay or int(delay.group(1)) <= 10):
                return urllib.parse.urljoin(base_url, m.group(1).strip())
    if len(visible_text(html)) < 300:
        m = JS_REDIRECT.search(html)
        if m:
            return urllib.parse.urljoin(base_url, (m.group(1) or m.group(2)).strip())
    return ""


def is_index_path(path):
    segs = [x for x in path.lower().split("?")[0].split("/") if x]
    return all(x in INDEX_SEGMENTS for x in segs)


def expected_tokens(url, expect=""):
    """Words the discussion must carry: from the expected title, else from the URL slug."""
    src = expect or urllib.parse.unquote(host_path(url)[1])
    words = [x for x in re.split(r"[^a-z0-9]+", src.lower()) if len(x) >= 4 and not x.isdigit() and x not in SLUG_STOP]
    return list(dict.fromkeys(words))[:8]


def topic_present(tokens, html):
    if not tokens:
        return None                       # nothing to compare (e.g. /t/12345): not proven either way
    hay = (" ".join(re.findall(r"(?is)<title[^>]*>(.*?)</title>", html)) + " " + visible_text(html)).lower()
    hits = sum(t in hay for t in tokens)
    return hits >= max(1, min(3, (len(tokens) + 1) // 2))


def assess(orig_url, status, final_url, headers, body, expect="", hop=None):
    """Pure decision (unit-tested). hop = (status, final_url, headers, body) of the client-redirect target,
    when the caller fetched it. Returns {availability, indexing, why, final}."""
    def out(av, why, ix=UNVER, final=None):
        return {"availability": av, "indexing": ix, "why": why, "final": final or final_url or orig_url}
    if status in (404, 410):
        return out(GONE, f"HTTP {status}")
    if status in (401, 403, 429) or (status and status >= 500):
        return out(BLOCKED, f"HTTP {status} — the site blocks automatic checks, open by hand")
    if status and status >= 400:
        return out(UNVER, f"HTTP {status}")
    o_host, o_path = host_path(orig_url)
    f_host, f_path = host_path(final_url or orig_url)
    tokens = expected_tokens(orig_url, expect)
    if final_url and final_url != orig_url:
        if LOGIN_PATH.search(f_path) and not LOGIN_PATH.search(o_path):
            return out(GONE, "HTTP redirect to the login page")
        if is_index_path(f_path) and not is_index_path(o_path):
            return out(GONE, "HTTP redirect to the forum index / home page")
    ctype = (headers.get("content-type") or "").lower()
    if "pdf" in ctype or o_path.lower().endswith(".pdf"):
        if body[:5] == b"%PDF-" or "pdf" in ctype:
            ix = NOINDEX if noindex_reason(headers, "") else INDEXABLE
            return out(LIVE, "PDF opens", ix) if len(body) > 1000 else out(GONE, "empty PDF")
    html = body.decode("utf-8", "replace")
    target = client_redirect(html, final_url or orig_url)
    if target:
        kind = "meta refresh" if any(_attr(t, "http-equiv").lower() == "refresh" for t in META_TAG.findall(html)) else "JavaScript redirect"
        t_path = host_path(target)[1]
        if hop is None:
            if is_index_path(t_path) or LOGIN_PATH.search(t_path):
                return out(GONE, f"HTTP {status or 200} but {kind} to {target} ({len(body)} bytes) — the thread is gone", final=target)
            return out(UNVER, f"{kind} to {target} — destination not opened, check by hand", final=target)
        dest = assess(target, *hop, expect=expect or " ".join(tokens))
        if dest["availability"] == LIVE and not is_index_path(t_path) and not LOGIN_PATH.search(t_path):
            dest["why"] = f"moved: {kind} to {dest['final']} · " + dest["why"]
            return dest
        why = f"HTTP {status or 200} but {kind} to {target}"
        if dest["availability"] == LIVE or is_index_path(t_path):
            why += " (forum index / home)" if is_index_path(t_path) else " (expected discussion not there)"
        else:
            why += f" → {dest['why']}"
        return out(GONE, why + " — the thread is gone", final=dest["final"])
    if BLOCK_TEXT.search(" ".join(re.findall(r"(?is)<title[^>]*>(.*?)</title>", html))) or \
            (len(visible_text(html)) < 600 and BLOCK_TEXT.search(html)):
        return out(BLOCKED, "bot check / captcha page — open by hand")
    text = visible_text(html)
    title = " ".join(re.findall(r"(?is)<title[^>]*>(.*?)</title>", html))[:300]
    heads = " ".join(re.findall(r"(?is)<h1[^>]*>(.*?)</h1>", html))[:300]
    if REMOVED_TEXT.search(title) or REMOVED_TEXT.search(visible_text(heads)) or REMOVED_TEXT.search(text[:1500]):
        return out(GONE, "'page removed / not found' text")
    if len(text) < 150:
        if len(html) > 20000:
            return out(UNVER, "page is built by scripts — open by hand")
        return out(GONE, f"empty page ({len(body)} bytes)")
    nr = noindex_reason(headers, html)
    ix = NOINDEX if nr else INDEXABLE
    ix_why = f" · noindex ({nr})" if nr else ""
    found = topic_present(tokens, html)
    if found is False:
        if final_url and final_url != orig_url:
            return out(GONE, f"HTTP redirect to {final_url} — expected discussion not there")
        return out(UNVER, "page opens but the expected topic is not on it — check by hand" + ix_why, ix)
    return out(LIVE, f"HTTP {status or 200}" + (" · topic found" if found else " · topic not compared") + ix_why, ix)


def judge(orig_url, status, final_url, headers, body, expect="", hop=None):
    """Scan verdict ('live'|'removed'|'unknown', why) from assess(): a working example must be a live
    thread AND indexable — a noindexed page is never proof that the platform's posts get into Google."""
    return verdict(assess(orig_url, status, final_url, headers, body, expect, hop))


def fetch(url, limit=600_000, timeout=20):
    """(status, final_url, headers{lower}, body bytes) or raises."""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.8",
                                               "Accept": "text/html,application/xhtml+xml,application/pdf,*/*;q=0.8"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.geturl(), {k.lower(): v for k, v in r.headers.items()}, r.read(limit)
    except urllib.error.HTTPError as e:
        try:
            body = e.read(limit)
        except Exception:
            body = b""
        return e.code, e.geturl() or url, {k.lower(): v for k, v in (e.headers or {}).items()}, body


def check_url(url, expect="", fallback=True, get=None):
    """Network wrapper of assess(): follows one client-side redirect. №91: a page the host blocks (403, captcha,
    timeout) is not dropped — free evidence is looked for in its RSS / Atom feed, sitemap and public API."""
    own_get, get = get, get or fetch
    try:
        res = get(url)
        hop = None
        if res[0] and res[0] < 400:
            target = client_redirect(res[3].decode("utf-8", "replace"), res[1] or url)
            if target:
                try:
                    hop = get(target)
                except Exception:
                    hop = None
        r = assess(url, *res, expect=expect, hop=hop)
        html = res[3].decode("utf-8", "replace") if res[3] else ""
    except urllib.error.URLError as e:
        reason = str(getattr(e, "reason", e))
        if "Name or service not known" in reason or "getaddrinfo" in reason or "nodename" in reason:
            return {"availability": GONE, "indexing": UNVER, "why": "domain does not resolve", "final": url}
        r, html = {"availability": BLOCKED, "indexing": UNVER, "why": "could not open: " + reason[:60], "final": url}, ""
    except Exception as e:  # timeouts, TLS, broken servers
        r, html = {"availability": BLOCKED, "indexing": UNVER, "why": "could not open: " + str(e)[:60], "final": url}, ""
    if fallback and r["availability"] == BLOCKED:
        r = with_fallback(r, url, html, expect, own_get)
    return r


def verdict(r):
    if r["availability"] == LIVE:
        return ("removed", "noindex — " + r["why"]) if r["indexing"] == NOINDEX else ("live", r["why"])
    if r["availability"] == BLOCKED and r.get("evidence_source"):
        return "blocked", r["why"]          # №91 kept with its evidence, never dropped as "could not verify"
    return ("removed" if r["availability"] == GONE else "unknown"), r["why"]


# ---------- №91 live-check fallback when a host blocks automatic fetches ----------
# Order: RSS / Atom feed → sitemap → the platform's public API (all free). Google's cache is gone (retired 2024):
# the indexed snippet from a site: search is used instead, in --verify (the user's SerpApi / DataForSEO).
FEED_LINK = re.compile(r"<link\b[^>]*type=[\"']application/(?:rss|atom)\+xml[\"'][^>]*>", re.I)
FEED_PATHS = ("/feed", "/rss", "/feed.xml", "/rss.xml", "/atom.xml", "/index.xml", "/latest.rss",
              "/forums/-/index.rss", "/feed/")
SITEMAP_PATHS = ("/sitemap.xml", "/sitemap_index.xml", "/sitemap-index.xml", "/wp-sitemap.xml", "/sitemap/sitemap.xml")
XML_DATE = re.compile(r"<(pubDate|updated|published|dc:date|lastBuildDate|lastmod)[^>]*>\s*([^<]{6,40}?)\s*</\1>", re.I)


def _key(u):
    """Compare-key of a page URL: no scheme, www, query, fragment or trailing slash."""
    u = re.sub(r"^https?://(www\.|m\.)?", "", (u or "").strip().lower()).split("#")[0].split("?")[0]
    return u.rstrip("/")


def same_page(a, b):
    """The feed / sitemap entry is this page (or one of its posts: /t/slug/12 and /t/slug/12/4)."""
    ka, kb = _key(a), _key(b)
    return bool(ka) and (ka == kb or kb.startswith(ka + "/") or ka.startswith(kb + "/")) and ka.count("/") >= 1 and kb.count("/") >= 1


def _date(s):
    m = re.search(r"(\d{4}-\d{2}-\d{2})", s or "")
    if m:
        return m.group(1)
    for fmt in ("%a, %d %b %Y", "%d %b %Y"):
        try:
            from datetime import datetime
            return datetime.strptime(re.sub(r"\s+\d{1,2}:\d{2}.*$", "", s.strip()), fmt).date().isoformat()
        except ValueError:
            continue
    return (s or "").strip()[:25]


def _body(res):
    body = res[3] or b""
    if body[:2] == b"\x1f\x8b":
        import gzip
        try:
            body = gzip.decompress(body)
        except Exception:
            return ""
    return body.decode("utf-8", "replace")


def feed_urls(url, html=""):
    sp = urllib.parse.urlsplit(url)
    root = f"{sp.scheme}://{sp.netloc}"
    out = [urllib.parse.urljoin(url, _attr(t, "href")) for t in FEED_LINK.findall(html or "") if _attr(t, "href")]
    path = sp.path.rstrip("/")
    if path:
        out += [root + path + ".rss", root + path + "/feed"]           # Discourse topic feed · WordPress post comments
    out += [root + p for p in FEED_PATHS]
    seen = []
    for u in out:
        if u.startswith("http") and u not in seen:
            seen.append(u)
    return seen[:10]


def find_in_feed(xml, url):
    """(date, title) when the RSS / Atom document lists this page, else None."""
    if not re.search(r"<(rss|feed|rdf:RDF)\b", xml or "", re.I):
        return None
    for block in re.findall(r"(?is)<(?:item|entry)\b.*?</(?:item|entry)>", xml):
        links = re.findall(r"(?is)<link[^>]*>\s*(https?://[^<\s]+)\s*</link>", block) + \
            [_attr(t, "href") for t in re.findall(r"(?i)<link\b[^>]*>", block)] + \
            re.findall(r"(?is)<guid[^>]*>\s*(https?://[^<\s]+)\s*</guid>", block)
        if any(lk and same_page(url, lk) for lk in links):
            d = XML_DATE.search(block)
            t = re.search(r"(?is)<title[^>]*>(.*?)</title>", block)
            return (_date(d.group(2)) if d else "", visible_text(re.sub(r"<!\[CDATA\[|\]\]>", "", t.group(1)))[:90] if t else "")
    head = re.split(r"(?i)<(?:item|entry)\b", xml, maxsplit=1)[0]          # a topic's own feed: the channel is the page
    links = re.findall(r"(?is)<link[^>]*>\s*(https?://[^<\s]+)\s*</link>", head) + \
        [_attr(t, "href") for t in re.findall(r"(?i)<link\b[^>]*>", head)]
    if any(lk and _key(lk) == _key(url) for lk in links):
        d = XML_DATE.search(xml)
        t = re.search(r"(?is)<title[^>]*>(.*?)</title>", head)
        return (_date(d.group(2)) if d else "", visible_text(re.sub(r"<!\[CDATA\[|\]\]>", "", t.group(1)))[:90] if t else "")
    return None


def sitemap_urls(robots_txt, root):
    out = [ln.split(":", 1)[1].strip() for ln in (robots_txt or "").splitlines() if ln.lower().startswith("sitemap:")]
    return [u for u in out if u.startswith("http")] + [root + p for p in SITEMAP_PATHS]


def find_in_sitemap(xml, url):
    """('found', lastmod) · ('index', [child sitemaps, newest first]) · None."""
    if re.search(r"<sitemapindex\b", xml or "", re.I):
        kids = re.findall(r"(?is)<sitemap>\s*<loc>\s*([^<\s]+)\s*</loc>(?:\s*<lastmod>\s*([^<\s]+)\s*</lastmod>)?", xml)
        return "index", [u for u, _ in sorted(kids, key=lambda k: k[1] or "", reverse=True)]
    for loc, rest in re.findall(r"(?is)<url>\s*<loc>\s*([^<\s]+)\s*</loc>(.*?)</url>", xml or ""):
        if _key(loc) == _key(url):
            m = re.search(r"(?is)<lastmod>\s*([^<\s]+)", rest)
            return "found", (_date(m.group(1)) if m else "")
    return None


def api_check(url, get):
    """The platform's public API, where it has one: (source, detail, date, removed) or None."""
    sp = urllib.parse.urlsplit(url)
    root, path, host = f"{sp.scheme}://{sp.netloc}", sp.path, host_of(url)
    tries = []
    m = re.search(r"/t/(?:[^/]+/)?(\d+)", path)
    if m:
        tries.append(("Discourse API", root + f"/t/{m.group(1)}.json"))
    m = re.search(r"/d/(\d+)", path)
    if m:
        tries.append(("Flarum API", root + f"/api/discussions/{m.group(1)}"))
    if suffix_match(host, "reddit.com") and "/comments/" in path:
        tries.append(("Reddit API", root + path.rstrip("/") + ".json"))
    slug = path.rstrip("/").rsplit("/", 1)[-1]
    if slug and not slug.isdigit() and "." not in slug and not m:
        tries.append(("WordPress REST API", root + "/wp-json/wp/v2/posts?slug=" + urllib.parse.quote(slug) + "&_fields=link,date,title"))
    for name, api in tries:
        try:
            res = get(api)
        except Exception:
            continue
        ctype = (res[2].get("content-type") or "").lower()
        if "json" not in ctype:
            continue
        try:
            d = json.loads(_body(res) or "null")
        except ValueError:
            continue
        if res[0] in (404, 410) and name != "WordPress REST API":
            return name, "the API says the topic does not exist", "", True
        if res[0] != 200:
            continue
        if name == "Discourse API" and isinstance(d, dict) and d.get("id"):
            return name, f"topic \"{(d.get('title') or '')[:70]}\", {d.get('posts_count', '?')} posts", _date(d.get("created_at") or ""), False
        if name == "Flarum API" and isinstance(d, dict) and (d.get("data") or {}).get("attributes"):
            a = d["data"]["attributes"]
            return name, f"discussion \"{(a.get('title') or '')[:70]}\"", _date(a.get("createdAt") or ""), False
        if name == "Reddit API" and isinstance(d, list) and d:
            try:
                post = d[0]["data"]["children"][0]["data"]
            except (KeyError, IndexError, TypeError):
                continue
            gone = bool(post.get("removed_by_category")) or post.get("selftext") in ("[removed]", "[deleted]")
            day = date.fromtimestamp(post["created_utc"]).isoformat() if post.get("created_utc") else ""
            return name, ("post removed" if gone else f"post \"{(post.get('title') or '')[:70]}\""), day, gone
        if name == "WordPress REST API" and isinstance(d, list):
            for it in d:
                if same_page(url, it.get("link") or ""):
                    title = visible_text(((it.get("title") or {}).get("rendered")) or "")[:70]
                    return name, f"post \"{title}\"", _date(it.get("date") or ""), False
    return None


def blocked_evidence(url, html="", get=None):
    """№91 free evidence for a page the host would not let us open. Returns {source, detail, date, removed} or None."""
    get = get or (lambda u: fetch(u, limit=2_000_000, timeout=15))
    for fu in feed_urls(url, html):
        try:
            res = get(fu)
        except Exception:
            continue
        if res[0] == 200:
            hit = find_in_feed(_body(res), url)
            if hit:
                return {"source": "RSS/Atom feed", "detail": (f'"{hit[1]}" in ' if hit[1] else "listed in ") + fu,
                        "date": hit[0], "removed": False}
    sp = urllib.parse.urlsplit(url)
    root = f"{sp.scheme}://{sp.netloc}"
    try:
        rob = get(root + "/robots.txt")
        robots = _body(rob) if rob[0] == 200 else ""
    except Exception:
        robots = ""
    todo, seen, opened = sitemap_urls(robots, root), set(), 0
    while todo and opened < 12:
        sm = todo.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        try:
            res = get(sm)
        except Exception:
            continue
        opened += 1
        if res[0] != 200:
            continue
        hit = find_in_sitemap(_body(res), url)
        if hit and hit[0] == "found":
            return {"source": "sitemap", "detail": "listed in " + sm, "date": hit[1], "removed": False}
        if hit and hit[0] == "index":
            todo = hit[1][:6] + todo
    hit = api_check(url, get)
    if hit:
        return {"source": hit[0], "detail": hit[1], "date": hit[2], "removed": hit[3]}
    return None


def with_fallback(r, url, html="", expect="", get=None):
    """A FETCH BLOCKED result + the evidence found elsewhere: 'blocked — evidence from <source>'."""
    ev = blocked_evidence(url, html, (lambda u: get(u)) if get else None)
    if not ev:
        r = dict(r)
        r["why"] += " · no feed, sitemap or public API lists it"
        return r
    r = dict(r)
    if ev["removed"]:
        r.update(availability=GONE, why=f"blocked page · removed per {ev['source']}: {ev['detail']}")
        return r
    r["evidence_source"], r["evidence_date"] = ev["source"], ev["date"]
    r["why"] = (f"blocked — evidence from {ev['source']}: {ev['detail']}" + (f" ({ev['date']})" if ev["date"] else "")
                + " · indexing not verified")
    return r


def check_page(url, expect=""):
    return verdict(check_url(url, expect))


def check_urls_cli(path, out):
    """--check-urls: one URL per line, optionally TAB + expected thread title. Prints both fields."""
    rows = []
    with open(path, encoding="utf-8") as f:
        items = [ln.rstrip("\n").split("\t", 1) for ln in f if ln.strip() and not ln.startswith("#")]
    with ThreadPoolExecutor(8) as pool:
        res = list(pool.map(lambda it: check_url(it[0].strip(), it[1].strip() if len(it) > 1 else ""), items))
    print("| URL | Thread availability | Indexing eligibility | Evidence | Why | Final URL |")
    print("|---|---|---|---|---|---|")
    for it, r in zip(items, res):
        ev = (f"blocked — evidence from {r['evidence_source']}" + (f" ({r['evidence_date']})" if r.get("evidence_date") else "")) \
            if r.get("evidence_source") else ""
        rows.append({"url": it[0].strip(), "availability": r["availability"], "indexing": r["indexing"], "evidence": ev,
                     "why": r["why"], "final": r["final"], "checked": date.today().isoformat()})
        print(f"| {it[0].strip()} | {r['availability']} | {r['indexing']} | {ev or '—'} | {r['why']} | {r['final']} |")
    if out:
        with open(out, "w", newline="", encoding="utf-8") as f:
            wr = csv.DictWriter(f, fieldnames=["url", "availability", "indexing", "evidence", "why", "final", "checked"])
            wr.writeheader()
            wr.writerows(rows)
    print("\nThread availability and indexing eligibility are page checks only — not a Google position. "
          "A position is written only from a dated Google check (SerpApi / DataForSEO).")


# ---------- sign-up link (№5) ----------

SIGNUP_PATHS = ("/register", "/signup", "/sign-up", "/join", "/user/register", "/users/sign_up",
                "/create-account", "/account/register", "/accounts/signup", "/registration",
                "/member/register", "/register.php", "/ucp.php?mode=register", "/index.php?register/",
                "/login/register", "/start", "/get-started")
SIGNUP_HREF = re.compile(r"""<a[^>]+href=["']([^"'#]+)["'][^>]*>(.*?)</a>""", re.I | re.S)
SIGNUP_WORD = re.compile(r"(sign ?up|register|registration|create (an |your )?account|join( now| free| us)?$|get started)", re.I)
SIGNUP_URLW = re.compile(r"(register|sign-?up|sign_up|join|create-?account|registration)", re.I)
SIGNUP_PAGE = re.compile(r"(type=[\"']password|sign ?up|register|create (an |your )?account|e-?mail)", re.I)
FORUM_ROOTS = ("forum", "forums", "community", "board", "boards", "discussions", "discuss")


def signup_ok(url, home):
    try:
        status, final, headers, body = fetch(url, limit=300_000, timeout=15)
    except Exception:
        return False
    if status != 200:
        return False
    if host_path(final)[1].rstrip("/") == "" and host_path(url)[1].rstrip("/") != "":
        return False  # bounced to the home page
    return bool(SIGNUP_PAGE.search(body.decode("utf-8", "replace")))


def find_signup(example_url, domain=""):
    """(signup_url or None, home_url). Looks on the home page for a sign-up link, then tries common paths."""
    sp = urllib.parse.urlsplit(example_url)
    domain = (domain or host_path(example_url)[0]).lower()
    home = f"{sp.scheme}://{sp.netloc}/"
    seg = (sp.path.strip("/").split("/") or [""])[0].lower()
    roots = [home.rstrip("/")] + ([home + seg] if seg in FORUM_ROOTS else [])
    cands = []
    for root in reversed(roots):
        try:
            status, final, headers, body = fetch(root + "/", limit=400_000, timeout=15)
        except Exception:
            continue
        if status != 200:
            continue
        for href, label in SIGNUP_HREF.findall(body.decode("utf-8", "replace")):
            lab = visible_text(label)
            if SIGNUP_URLW.search(href) or SIGNUP_WORD.search(lab):
                u = urllib.parse.urljoin(final, href.strip())
                hu = host_path(u)[0]
                if u.startswith("http") and (hu == domain or hu.endswith("." + domain)) and u not in cands:
                    cands.append(u)
    for root in reversed(roots):
        cands += [root + p for p in SIGNUP_PATHS]
    for u in cands[:12]:
        if signup_ok(u, home):
            return u, home
    return None, home


# ---------- scan ----------

def read_key(fd):
    if fd is None:
        return None
    try:
        data = os.read(int(fd), 4096).decode().strip()
        os.close(int(fd))
        return data or None
    except OSError:
        return None


def serpapi_task(responses):
    """One query's SerpApi pages as a DataForSEO-shaped task, so group() reads both the same way."""
    items, feats = rc.serpapi_parse(responses)
    return {"result": [{"items": [{"type": "organic", "url": u, "rank_group": pos} for pos, u in items]
                        + [{"type": kind, "url": u} for kind, u in feats]}]}


def run_search(a, products):
    queries = {f"{p} {a.suffix}".strip().lower(): p for p in products}
    probe = f"\"<product> {a.suffix}\"" if a.suffix.strip() else "queries as written"
    if a.provider == "serpapi":
        per = rc.serpapi_searches(a.depth, "google")
        print(f"Platform scan · google {a.country} · top {a.depth} · {len(queries)} queries ({probe}) · "
              f"SerpApi: {len(queries) * per} searches from your monthly quota")
    else:
        loc = rc.COUNTRIES.get(a.country.lower()) or sys.exit("Unknown --country: " + ", ".join(sorted(rc.COUNTRIES)))
        price = (0.002 if a.live else 0.0006) * max(1, a.depth / 10)
        print(f"Platform scan · google {a.country} · top {a.depth} · {len(queries)} queries "
              f"({probe}) · PAID: about ${len(queries) * price:.2f} from your DataForSEO balance")
    if a.dry_run:
        for q in list(queries)[:20]:
            print("  ·", q)
        return None, queries
    if a.provider == "serpapi":
        key = read_key(a.auth_fd)
        if not key:
            sys.exit(rc.NO_SERPAPI)
        a.engine = "google"
        return {q: serpapi_task(rc.serpapi_query(q, key, a)) for q in queries}, queries
    login, password = rc.read_auth(a.auth_fd)
    if not (login and password):
        sys.exit(rc.NO_CREDS)
    body = [{"keyword": q, "location_code": loc, "language_code": a.language, "depth": a.depth,
             "device": a.device, "tag": q} for q in queries]
    results = {}
    if a.live:
        for item in body:
            d = rc.call("POST", "/live/advanced", login, password, [item])
            for t in d.get("tasks") or []:
                results[(t.get("data") or {}).get("keyword", "").lower()] = t
    else:
        ids = {}
        for i in range(0, len(body), 100):
            d = rc.call("POST", "/task_post", login, password, body[i:i + 100])
            for t in d.get("tasks") or []:
                if t.get("id"):
                    ids[t["id"]] = (t.get("data") or {}).get("keyword", "").lower()
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
                            results[ids[r["id"]]] = tt
                        ids.pop(r["id"])
        if ids:
            print(f"- {len(ids)} tasks not ready yet (paid, kept 3 days by DataForSEO).")
    return results, queries


def group(results, queries, products, ex):
    """Platforms with all their pages (best position first) + skipped counts."""
    plat = defaultdict(lambda: {"products": set(), "pages": [], "best": 999, "in_blocks": set(), "abuse": 0})
    meta, skipped = {}, {"stop": set(), "black": set(), "dead": set()}
    for q, task in results.items():
        product = queries.get(q, q)
        found = [(pos, u, "organic") for pos, u in rc.serp_items(task)]
        found += [(None, u, kind) for kind, u in rc.serp_features(task)]
        for pos, url, kind in found:
            if not url.startswith("http") or any(is_brand_site(url, pr) for pr in products):
                continue
            slug, dom, typ, cost = classify(url)
            if cost == "store":
                continue
            hit = excluded(url, typ, ex)
            if hit:
                skipped[hit[0]].add(dom)
                continue
            p = plat[slug]
            meta[slug] = (dom, typ, cost)
            if ABUSE.search(url):
                p["abuse"] += 1
                continue
            p["products"].add(product)
            if url not in [x["url"] for x in p["pages"]]:
                p["pages"].append({"url": url, "product": product, "position": pos})
            if pos:
                p["best"] = min(p["best"], pos)
            if kind != "organic":
                p["in_blocks"].add(kind)
    out = []
    for slug, p in plat.items():
        dom, typ, cost = meta[slug]
        if not p["products"] and p["abuse"]:
            cost = "abuse"
        pages = sorted(p["pages"], key=lambda x: x["position"] or 999)
        out.append({"platform": slug, "domain": dom, "type": typ or "?", "cost": cost,
                    "products": sorted(p["products"]), "best_position": p["best"] if p["best"] < 999 else "",
                    "serp_blocks": sorted(p["in_blocks"]), "pages": pages})
    return out, {k: sorted(v) for k, v in skipped.items()}


def verify(platforms, signup=True, workers=8):
    """Live-check up to 3 examples per platform; find a sign-up link for the live free / to-check ones."""
    jobs = [(i, j, pg["url"]) for i, p in enumerate(platforms) if p["cost"] != "abuse"
            for j, pg in enumerate(p["pages"][:3])]
    with ThreadPoolExecutor(workers) as pool:
        for (i, j, _), r in zip(jobs, pool.map(lambda t: check_url(t[2]), jobs)):
            pg = platforms[i]["pages"][j]
            pg["availability"], pg["indexing"] = r["availability"], r["indexing"]
            pg["status"], pg["why"] = verdict(r)
            if r.get("evidence_source"):
                pg["evidence_source"], pg["evidence_date"] = r["evidence_source"], r.get("evidence_date", "")
    for p in platforms:
        st = [pg.get("status") for pg in p["pages"][:3]]
        p["live"] = "abuse" if p["cost"] == "abuse" else "live" if "live" in st else "blocked" if "blocked" in st else \
            "removed" if st and all(s == "removed" for s in st) else "unverified"
    todo = [p for p in platforms if signup and p["live"] in ("live", "blocked") and p["cost"] in ("free", "check")]
    with ThreadPoolExecutor(workers) as pool:
        for p, (su, home) in zip(todo, pool.map(lambda p: find_signup(next(pg["url"] for pg in p["pages"] if pg.get("status") in ("live", "blocked")), p["domain"]), todo)):
            p["signup"], p["home"] = su, home
    return platforms


def load_allowed(path):
    if not path:
        return None
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    return set(d.get("allowed") or []) if isinstance(d, dict) else set(d)


def signup_cell(p):
    if p["cost"] == "paid":
        return "paid placement — buy via the site's advertising / PR contact"
    if p.get("signup"):
        return p["signup"]
    return f"sign-up link not found · {p.get('home') or 'https://' + p['domain'] + '/'}"


# №70 evidence labels, research history and discovery status (beta-tester report on v0.50.0)
def load_history(paths, journal=None, today=None):
    """Everything the user already has on a platform: earlier scans (platforms-scan*.csv) and the journal's positions.
    Returns {key: {"urls": set, "best": (pos, query/product, date, source) or None}} keyed by platform slug AND host."""
    hist = defaultdict(lambda: {"urls": set(), "best": None})

    def add(keys, url, pos, what, day, src):
        for k in {x.lower() for x in keys if x}:
            h = hist[k]
            if url:
                h["urls"].add(url.rstrip("/"))
            try:
                pos = int(float(pos)) if str(pos or "").strip() else None
            except ValueError:
                pos = None
            if pos and (h["best"] is None or pos < h["best"][0]):
                h["best"] = (pos, what or "", day or "", src)
    for path in paths:
        if not path or not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                dom = (r.get("platform") or "").lower()
                for u in [r.get("post", "")] + (r.get("more_posts") or "").split():
                    if u:
                        add([dom, host_of(u)], u, r.get("position") if u == r.get("post") else "", r.get("product"),
                            r.get("checked"), os.path.basename(path))
                if r.get("best_position"):
                    add([dom], "", r.get("best_position"), r.get("product_names", "").split(";")[0], r.get("checked"),
                        os.path.basename(path))
    if journal and os.path.exists(journal):
        for pg in w.page_states(w.read_rows(journal), today or date.today()).values():
            pos = pg.get("best_pos") or pg.get("position")
            add([pg.get("platform", ""), host_of(pg["url"])], pg["url"], pos, pg.get("query") or pg.get("offer"),
                str(pg.get("pos_date") or ""), "your journal")
    return hist


def evidence_cell(pg, live_status):
    """№70 never "ranks" without a position read from Google: ranking verified (a ranking page is indexed) ·
    seen in a Google block · example URL verified live only. №91 blocked pages carry where the evidence came from."""
    if live_status == "blocked" and pg:
        day = f" ({pg['evidence_date']})" if pg.get("evidence_date") else ""
        pos = f" · seen at #{pg['position']} in the search" if pg.get("position") else ""
        return f"blocked — evidence from {pg.get('evidence_source', '?')}{day}{pos} · indexing not verified"
    if live_status != "live":
        return "example removed" if live_status == "removed" else "could not verify"
    if pg and pg.get("position"):
        return f"Google ranking verified: #{pg['position']} (today) · example URL verified live"
    if pg:
        return "Seen in a Google block, position not recorded · example URL verified live"
    return "Example URL verified live · Google ranking not checked"


def history_of(p, hist):
    keys = {p["platform"].lower(), p["domain"].lower()}
    keys |= {host_of(pg["url"]) for pg in p["pages"]}
    urls, best = set(), None
    for k in keys:
        h = hist.get(k)
        if not h:
            continue
        urls |= h["urls"]
        if h["best"] and (best is None or h["best"][0] < best[0]):
            best = h["best"]
    return urls, best


def discovery_cell(p, hist, yours):
    """NEW platform · EXISTING with NEW evidence · EXISTING repeated from saved research."""
    urls, best = history_of(p, hist)
    known = bool(urls or best) or p["platform"] in yours or p["domain"] in yours
    if not known:
        return "NEW platform"
    now_urls = {pg["url"].rstrip("/") for pg in p["pages"]}
    better = p["best_position"] and (best is None or int(p["best_position"]) < best[0])
    if (now_urls - urls) or better:
        return "EXISTING · NEW evidence"
    return "EXISTING · repeated from saved research"


def history_cell(p, hist, live_status):
    """The best earlier evidence, and a conflict line when today's scan disagrees with it (never overwrite history)."""
    _, best = history_of(p, hist)
    if not best:
        return "", ""
    pos, what, day, src = best
    cell = f"#{pos}" + (f' "{what}"' if what else "") + (f" ({day}" if day else " (") + f", {src})"
    conflict = ""
    if live_status == "removed":
        conflict = f"history shows #{pos} on {day or '?'}; today the examples are removed — recheck before dropping"
    elif not p["best_position"]:
        conflict = f"history shows #{pos} on {day or '?'}; this scan did not see it in the top — recheck, history kept"
    return cell, conflict


def report(platforms, skipped, out, allowed, yours, today, hist=None):
    shown_hidden = 0
    rows = []
    for p in platforms:
        live_pages = [pg for pg in p["pages"][:3] if pg.get("status") == "live"] or \
            [pg for pg in p["pages"][:3] if pg.get("status") == "blocked"]
        if allowed is not None:
            before = len(live_pages)
            live_pages = [pg for pg in live_pages if pg["url"] in allowed]
            shown_hidden += before - len(live_pages)
        p["shown"] = live_pages
        rows.append({"post": live_pages[0]["url"] if live_pages else "",
                     "product": live_pages[0]["product"] if live_pages else "",
                     "position": (live_pages[0]["position"] or "") if live_pages else "",
                     "platform": p["domain"], "type": p["type"], "cost": p["cost"],
                     "signup": signup_cell(p) if p["live"] in ("live", "blocked") else "",
                     "status": p["live"], "products": len(p["products"]), "best_position": p["best_position"],
                     "serp_blocks": " ".join(p["serp_blocks"]), "yours": "yes" if p["platform"] in yours else "",
                     "more_posts": " ".join(pg["url"] for pg in live_pages[1:]),
                     "checks": " ".join(f"{pg['url']} → {pg.get('availability', pg.get('status', '-'))} · {pg.get('indexing', 'UNVERIFIED')}: {pg.get('why', '')}"
                                       for pg in p["pages"][:3]),
                     "product_names": "; ".join(p["products"])[:300], "checked": today})
        hist = hist if hist is not None else {}
        rows[-1]["evidence"] = evidence_cell(live_pages[0] if live_pages else None, p["live"])
        rows[-1]["discovery"] = discovery_cell(p, hist, yours)
        rows[-1]["history"], rows[-1]["conflict"] = history_cell(p, hist, p["live"])
        rows[-1]["policy"] = "UNKNOWN"          # the platform's own rules: filled by the skill with the official URL
    order = {"live": 0, "blocked": 1, "unverified": 2, "removed": 3, "abuse": 4}
    rows.sort(key=lambda r: (order[r["status"]], -r["products"], r["position"] or r["best_position"] or 999))
    with open(out, "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["post"])
        wr.writeheader()
        wr.writerows(rows)

    live = [r for r in rows if r["status"] in ("live", "blocked")]
    n_blocked = sum(r["status"] == "blocked" for r in rows)
    dead = [r for r in rows if r["status"] == "removed"]
    unver = [r for r in rows if r["status"] == "unverified"]
    n_found = len([r for r in rows if r["status"] != "abuse"])
    n_skip = len(skipped["stop"]) + len(skipped["black"])
    print(f"Found {n_found} platforms · live {len(live) - n_blocked} · "
          + (f"blocked with evidence {n_blocked} · " if n_blocked else "") + f"removed {len(dead)} · "
          f"skipped by stop / black list {n_skip}"
          + (f" · skipped as known dead {len(skipped['dead'])}" if skipped["dead"] else "")
          + (f" · could not verify {len(unver)}" if unver else "") + f" · checked {today} · saved to {out}\n")
    found_rows = [r for r in rows if r["status"] in ("live", "blocked", "unverified")]
    n_new = sum(r["discovery"] == "NEW platform" for r in found_rows)
    n_ev = sum(r["discovery"] == "EXISTING · NEW evidence" for r in found_rows)
    n_rep = sum(r["discovery"].startswith("EXISTING · repeated") for r in found_rows)
    print(f"Discovery: NEW platforms {n_new} · EXISTING with NEW evidence {n_ev} · EXISTING repeated from saved research {n_rep}")
    if found_rows and not n_new:
        print("No genuinely new platform in this scan: every platform found is already in your base or earlier research.")
    conf = [r for r in rows if r["conflict"]]
    if conf:
        print("History conflicts (kept, not overwritten): " + " · ".join(f"{r['platform']}: {r['conflict']}" for r in conf[:15]))
    print()
    by_slug = {p["domain"]: p for p in platforms}
    for title, keep in (("Free (user posts)", "free"), ("Paid (news / PR / sponsored)", "paid"), ("To check", "check")):
        part = [r for r in live if r["cost"] == keep]
        if not part:
            continue
        print(f"## {title} — {len(part)}")
        print("| # | Post | Product | Pos. | Platform | Discovery | Evidence | History | Policy | Type | Free/Paid | Sign-up |")
        print("|---|---|---|---|---|---|---|---|---|---|---|---|")
        for i, r in enumerate(part[:40], 1):
            fp = "Paid" if keep == "paid" else "Free" if keep == "free" else "Free?"
            post = r["post"] or f"example: find your own with \"{(by_slug[r['platform']]['products'] or ['product'])[0]} review\""
            print(f"| {i} | {post} | {r['product']} | {r['position']} | {r['platform']}{' (yours)' if r['yours'] else ''} "
                  f"| {r['discovery']} | {r['evidence']} | {r['history'] or '—'} | {r['policy']} | {r['type']} | {fp} | {r['signup']} |")
            for pg in by_slug[r["platform"]]["shown"][1:3]:
                print(f"|  | ↳ {pg['url']} | {pg['product']} | {pg['position'] or ''} |  |  |  |  |  |  |  |  |")
        print()
    if dead:
        print("In Google, but the pages are removed (not in the working list): "
              + ", ".join(f"{r['platform']}" for r in dead[:30]))
    if unver:
        print("Could not verify (the site blocks automatic checks and no feed, sitemap or public API lists the page — open an example by hand): "
              + ", ".join(r["platform"] for r in unver[:30]))
    if n_skip:
        print("Skipped by stop / black list: " + ", ".join(skipped["stop"] + skipped["black"])[:600])
    bad = [r for r in rows if r["status"] == "abuse"]
    if bad:
        print(f"Skipped {len(bad)} domains where reviews sit in other organisations' upload folders or forms "
              "(hacked or abused sites — not platforms): " + ", ".join(r["platform"] for r in bad[:10]))
    if allowed is not None and shown_hidden:
        print(f"{shown_hidden} example posts hidden by the PARASITER filter.")
    dead_path = os.path.splitext(out)[0] + "-dead.txt"
    with open(dead_path, "w", encoding="utf-8") as f:
        hosts = sorted({host_path(by_slug[r["platform"]]["pages"][0]["url"])[0] for r in dead if by_slug[r["platform"]]["pages"]})
        f.write("\n".join(hosts) + ("\n" if hosts else ""))
    if dead:
        print(f"Dead domains saved to {dead_path} — skip them in your next scans (--exclude) so you don't pay to scan them again.")


# ---------- №90 cheap targeted verification: between free discovery and a full paid SERP scan ----------
# Free discovery (web search, the agent, a pattern search) finds hosted pages; only the top few most promising
# get a Google check on the user's own SerpApi / DataForSEO: indexed? (site:<url>) and position for the target
# query. The cost is printed first. Two lists, never mixed: "found in web search" vs "verified in Google".
TYPE_WEIGHT = {"forum": 30, "community": 30, "q&a": 25, "article": 15, "blog": 15, "page": 12, "site-builder": 12,
               "document": 10, "document/pdf": 10, "social": 8, "video": 5}
VERIFY_TOP = 5


def read_candidates(path):
    """Hosted results of free discovery: TSV `URL<TAB>target query[<TAB>product][<TAB>type]` or a CSV with
    url / post, query (or product → "<product> review"), product, type, status columns (platforms-scan.csv works)."""
    out = []
    with open(path, encoding="utf-8") as f:
        text = f.read()
    first = text.splitlines()[0] if text.strip() else ""
    if path.lower().endswith(".csv") and ("post" in first or "url" in first):
        for r in csv.DictReader(text.splitlines()):
            u = (r.get("url") or r.get("post") or "").strip()
            if not u.startswith("http"):
                continue
            prod = (r.get("product") or "").strip()
            out.append({"url": u, "query": (r.get("query") or (f"{prod} review" if prod else "")).strip(), "product": prod,
                        "type": (r.get("type") or "").strip(), "status": (r.get("status") or "").strip()})
    else:
        for ln in text.splitlines():
            if not ln.strip() or ln.startswith("#"):
                continue
            parts = [x.strip() for x in ln.split("\t")] + ["", "", ""]
            if parts[0].startswith("http"):
                out.append({"url": parts[0], "query": parts[1], "product": parts[2], "type": parts[3], "status": ""})
    seen, uniq = set(), []
    for c in out:
        k = _key(c["url"])
        if k not in seen:
            seen.add(k)
            uniq.append(c)
    return uniq


def promise(c, by_domain):
    """Rank score of one hosted result: a live, indexable page first, then evidence of a blocked one; forums and
    communities before other types; a domain hosting several products' reviews before a one-off. Dead / noindex: -1."""
    st = c.get("status") or ""
    if st in ("removed", "abuse"):
        return -1
    base = {"live": 300, "blocked": 200}.get(st, 100)
    typ = c.get("type") or classify(c["url"])[2] or ""
    return base + TYPE_WEIGHT.get(typ, 6) + 5 * min(6, by_domain.get(host_of(c["url"]), 1)) + (4 if c.get("query") else 0)


def pick(cands, top=VERIFY_TOP):
    by_domain = defaultdict(set)
    for c in cands:
        by_domain[host_of(c["url"])].add((c.get("product") or c.get("query") or c["url"]).lower())
    counts = {d: len(v) for d, v in by_domain.items()}
    scored = sorted(((promise(c, counts), i, c) for i, c in enumerate(cands)), key=lambda x: (-x[0], x[1]))
    chosen, doms = [], set()
    for sc, _, c in scored:                     # one page per domain first: more platforms for the same cost
        if sc >= 0 and host_of(c["url"]) not in doms and len(chosen) < top:
            chosen.append(c); doms.add(host_of(c["url"]))
    for sc, _, c in scored:
        if sc >= 0 and c not in chosen and len(chosen) < top:
            chosen.append(c)
    return chosen


def site_query(url):
    return "site:" + re.sub(r"^https?://", "", url).split("#")[0].rstrip("/")


def verify_cost(chosen, provider, depth=10):
    """{index, positions, searches, usd}: 1 site: search per page + 1 search per unique target query (per 10 results)."""
    per = max(1, math.ceil(depth / 10))
    idx = len(chosen)
    queries = {c["query"].lower() for c in chosen if c.get("query")}
    searches = idx + len(queries) * per
    usd = idx * 0.002 + len(queries) * 0.002 * per          # DataForSEO live endpoint
    return {"index": idx, "positions": len(queries), "searches": searches, "usd": round(usd, 3),
            "label": (f"~{searches} SerpApi searches ({idx} index + {len(queries)} position" + (f" × {per}" if per > 1 else "") + ")")
            if provider == "serpapi" else f"~${usd:.3f} DataForSEO ({idx} index + {len(queries)} position checks, live)"}


def verify_pages(chosen, search, depth=10, today=None):
    """search(query, depth) → [{position, url, title, snippet, date}] organic. Pure apart from search (unit-tested)."""
    today = today or date.today().isoformat()
    cache = {}

    def run(q, d):
        if (q, d) not in cache:
            cache[(q, d)] = search(q, d)
        return cache[(q, d)]
    out = []
    for c in chosen:
        r = dict(c, checked=today)
        hits = run(site_query(c["url"]), 10)
        own = next((h for h in hits if same_page(c["url"], h["url"])), None)
        r["indexed"] = bool(own)
        r["index_cell"] = ("indexed ✓ (site: check" + (f', snippet "{own["snippet"][:60]}"' if own and own.get("snippet") else "")
                           + (f", {own['date']}" if own and own.get("date") else "") + f", {today})") if own else \
            f"not in Google's index (site: check, {today})"
        if c.get("query"):
            res = run(c["query"], depth)
            hit = next((h for h in res if same_page(c["url"], h["url"])), None)
            dom = next((h for h in res if host_of(h["url"]) == host_of(c["url"])), None)
            r["position"] = hit["position"] if hit else ""
            r["position_cell"] = (f'#{hit["position"]} for "{c["query"]}" ({today})' if hit else
                                  f'not in top {depth} for "{c["query"]}"' + (f" · another page of the domain at #{dom['position']}" if dom else "")
                                  + f" ({today})")
            if hit:
                r["indexed"] = True                 # a ranking page is indexed even if site: missed it
        else:
            r["position"], r["position_cell"] = "", "no target query given"
        out.append(r)
    return out


def _provider_search(a):
    """The user's own account behind search(query, depth): SerpApi or DataForSEO (live endpoint)."""
    if a.provider == "serpapi":
        key = read_key(a.auth_fd)
        if not key:
            sys.exit(rc.NO_SERPAPI)

        def search(q, depth):
            ns = argparse.Namespace(engine="google", country=a.country, language=a.language, device=a.device, depth=depth)
            out, n = [], 0
            for d in rc.serpapi_query(q, key, ns):
                for it in d.get("organic_results") or []:
                    n += 1
                    if it.get("link"):
                        out.append({"position": it.get("position") or n, "url": it["link"], "title": it.get("title", ""),
                                    "snippet": it.get("snippet", ""), "date": it.get("date", "")})
            return out
        return search
    login, password = rc.read_auth(a.auth_fd)
    if not (login and password):
        sys.exit(rc.NO_CREDS)
    loc = rc.COUNTRIES.get(a.country.lower()) or sys.exit("Unknown --country: " + ", ".join(sorted(rc.COUNTRIES)))

    def search(q, depth):
        d = rc.call("POST", "/live/advanced", login, password,
                    [{"keyword": q, "location_code": loc, "language_code": a.language, "depth": depth, "device": a.device}])
        out = []
        for t in d.get("tasks") or []:
            for res in t.get("result") or []:
                for it in res.get("items") or []:
                    if it.get("type") == "organic" and it.get("url"):
                        out.append({"position": it.get("rank_group") or it.get("rank_absolute"), "url": it["url"],
                                    "title": it.get("title") or "", "snippet": it.get("description") or "",
                                    "date": (it.get("timestamp") or "")[:10]})
        return out
    return search


def verify_cli(a):
    cands = read_candidates(a.verify)
    if not cands:
        sys.exit("No candidate URLs in " + a.verify + " (one per line: URL<TAB>target query).")
    todo = [c for c in cands if not c.get("status")]
    if todo and not a.no_live_check:
        print(f"- free page check of {len(todo)} found pages first (feeds / sitemaps / APIs when a host blocks)…")
        with ThreadPoolExecutor(8) as pool:
            for c, r in zip(todo, pool.map(lambda c: check_url(c["url"], c.get("product") or ""), todo)):
                c["status"], c["why"] = verdict(r)
                c["evidence_source"] = r.get("evidence_source", "")
    chosen = pick(cands, a.top)
    cost = verify_cost(chosen, a.provider, a.depth)
    print(f"Targeted verification · google {a.country} · top {len(chosen)} of {len(cands)} found pages · "
          f"cost before running: {cost['label']}")
    for i, c in enumerate(chosen, 1):
        print(f"  {i}. {c['url']} · \"{c.get('query') or '—'}\" · {c.get('status') or 'not checked'}")
    if a.dry_run:
        print("\nDry run: nothing was searched. Run again without --dry-run after the user says yes "
              f"(--top N changes how many pages are verified; now {a.top}).")
        return
    res = verify_pages(chosen, _provider_search(a), a.depth)
    chosen_keys = {_key(c["url"]) for c in chosen}
    rest = [c for c in cands if _key(c["url"]) not in chosen_keys]
    today = date.today().isoformat()
    print(f"\n## Verified in Google — {len(res)} · {a.provider} · {today}")
    print("| # | Page | Target query | In Google's index | Position | Page check |")
    print("|---|---|---|---|---|---|")
    for i, r in enumerate(res, 1):
        print(f"| {i} | {r['url']} | {r.get('query') or '—'} | {r['index_cell']} | {r['position_cell']} | {r.get('status') or '—'} |")
    print(f"\n## Found in web search — not verified in Google — {len(rest)}")
    if rest:
        print("| # | Page | Target query | Page check |")
        print("|---|---|---|---|")
        for i, c in enumerate(rest, len(res) + 1):
            print(f"| {i} | {c['url']} | {c.get('query') or '—'} | {c.get('status') or 'not checked'} |")
    print("\nOnly the first list was checked in Google. The second one was seen in web search: no index check, no position.")
    print(f"Spent: {cost['label'].lstrip('~')}")
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        fields = ["url", "query", "product", "type", "status", "verified_in_google", "indexed", "position", "index_cell",
                  "position_cell", "checked"]
        wr = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        wr.writeheader()
        for r in res:
            wr.writerow(dict(r, verified_in_google="yes"))
        for c in rest:
            wr.writerow(dict(c, verified_in_google="no", checked=today))
    print(f"Saved to {a.out}")


def self_test():
    ex = load_exclusions()
    assert ex["stop"] and ex["black"], "local exclusions.md not parsed"
    cases = [("https://www.youtube.com/watch?v=1", "video", "stop"), ("https://youtu.be/x", "", "stop"),
             ("https://bucket.s3.amazonaws.com/a.pdf", "", "stop"), ("https://b.s3.us-east-1.amazonaws.com/x.pdf", "", "stop"),
             ("https://www.quora.com/q", "q&a", "stop"), ("https://foo.blogspot.com/2026/x.html", "", "black"),
             ("https://www.fitness.com/forum/threads/1", "forum", "black"), ("https://www.fitness.com/articles/1", "", None),
             ("https://community.synology.com/enu/forum/1", "", "black"), ("https://medium.com/@a/b", "article", None),
             ("https://example.org/files/guide.pdf", "document/pdf", None)]
    for url, typ, want in cases:
        got = (excluded(url, typ, ex) or (None,))[0]
        assert got == want, (url, got, want)
    ex["dead"]["deadforum.example"] = "2026-10-01"
    assert excluded("https://www.deadforum.example/t/1", "forum", ex)[0] == "dead"
    page = b"<html><head><title>Product X review</title></head><body>" + b"<p>Real review text. </p>" * 20 + b"</body></html>"
    u = "https://forum.example.com/threads/x-review.1/"
    assert judge(u, 200, u, {}, page)[0] == "live"
    assert judge(u, 404, u, {}, b"")[0] == "removed"
    assert judge(u, 410, u, {}, b"")[0] == "removed"
    assert judge(u, 200, "https://forum.example.com/", {}, page)[0] == "removed"
    assert judge(u, 200, "https://forum.example.com/login?next=1", {}, page)[0] == "removed"
    assert judge(u, 200, u, {"x-robots-tag": "noindex"}, page)[0] == "removed"
    assert judge(u, 200, u, {}, page.replace(b"<head>", b"<head><meta name=\"robots\" content=\"noindex,follow\">"))[0] == "removed"
    assert judge(u, 200, u, {}, b"<html><title>Oops! That page can\xe2\x80\x99t be found</title><h1>Page not found</h1></html>")[0] == "removed"
    assert judge(u, 200, u, {}, b"<html><body></body></html>")[0] == "removed"
    assert judge(u, 403, u, {}, b"")[0] == "unknown"
    # №71: JS / meta-refresh stubs, noindex as its own field, topic at the destination
    stub = b'<script>window.location.href="https://forum.example.com/";</script>'
    assert len(stub) < 100
    r = assess(u, 200, u, {}, stub)
    assert r["availability"] == GONE and "JavaScript redirect" in r["why"], r
    r = assess(u, 200, u, {}, stub, hop=(200, "https://forum.example.com/", {}, page))
    assert r["availability"] == GONE, r
    meta = b'<html><head><meta http-equiv="refresh" content="0; url=/forums/"></head><body></body></html>'
    assert assess(u, 200, u, {}, meta)["availability"] == GONE
    moved = b'<script>location.replace("/threads/x-review-new.9/")</script>'
    r = assess(u, 200, u, {}, moved, hop=(200, "https://forum.example.com/threads/x-review-new.9/", {}, page))
    assert r["availability"] == LIVE and r["why"].startswith("moved"), r
    r = assess(u, 200, u, {}, moved, hop=(200, "https://forum.example.com/threads/other.9/", {},
                                          b"<title>Other</title><body>" + b"<p>Unrelated chatter here. </p>" * 20))
    assert r["availability"] == GONE, r
    ni = assess(u, 200, u, {}, page.replace(b"<head>", b"<head><meta content=\"noindex\" name=\"robots\">"))
    assert ni["availability"] == LIVE and ni["indexing"] == NOINDEX, ni
    assert assess(u, 200, u, {"x-robots-tag": "googlebot: noindex, nofollow"}, page)["indexing"] == NOINDEX
    assert assess(u, 200, u, {"x-robots-tag": "otherbot: noindex"}, page)["indexing"] == INDEXABLE
    assert assess(u, 200, u, {"x-robots-tag": "unavailable_after: 25 Jun 2030 15:00:00 PST"}, page)["indexing"] == INDEXABLE
    assert assess(u, 200, u, {}, page)["indexing"] == INDEXABLE
    assert assess(u, 403, u, {}, b"")["availability"] == BLOCKED
    assert assess(u, 200, u, {}, b"<title>Just a moment...</title>")["availability"] == BLOCKED
    assert assess(u, 200, "https://forum.example.com/threads/other.2/", {},
                  b"<title>Other</title><body>" + b"<p>Unrelated chatter here. </p>" * 20)["availability"] == GONE
    assert assess(u, 200, u, {}, b"<title>Forum</title><body>" + b"<p>Unrelated chatter here. </p>" * 20)["availability"] == UNVER
    handler = page.replace(b"</body>", b"<a onclick=\"location.href='/login'\">x</a></body>")
    assert assess(u, 200, u, {}, handler)["availability"] == LIVE        # handlers on a full page are not redirects
    assert judge("https://x.example/a.pdf", 200, "https://x.example/a.pdf", {"content-type": "application/pdf"}, b"%PDF-" + b"0" * 2000)[0] == "live"
    assert classify("https://docs.example.net/files/x.pdf")[2] == "document/pdf"
    # №66: stores matched by domain, not substring; Google Sites & co. are platforms
    assert classify("https://sites.google.com/view/x-review/home")[3] == "free"
    assert classify("https://sites.google.com/view/x-review/home")[2] == "site-builder"
    assert classify("https://docs.google.com/document/d/abc/edit")[3] == "free"
    assert classify("https://groups.google.com/g/x/c/abc")[3] == "free"
    assert classify("https://www.google.com/search?q=x")[3] == "store"
    assert classify("https://play.google.com/store/apps/details?id=x")[3] == "store"
    assert classify("https://www.amazon.co.uk/dp/B0X")[3] == "store"
    assert classify("https://smile.amazon.com/dp/B0X")[3] == "store"
    assert classify("https://www.target.com/p/x")[3] == "store"
    assert classify("https://forum.nottarget.community/t/x-review/1")[3] != "store"
    assert classify("https://googlecomputing-forum.example/threads/x.1/")[3] != "store"
    assert ABUSE.search("https://uni.edu/wp-content/uploads/2026/x.pdf")
    t = serpapi_task([{"organic_results": [{"position": 1, "link": "https://forum.example.com/t/x-review/1"}],
                       "discussions_and_forums": [{"link": "https://www.reddit.com/r/x/comments/1"}]}])
    assert rc.serp_items(t) == [(1, "https://forum.example.com/t/x-review/1")]
    assert ("discussions_and_forums", "https://www.reddit.com/r/x/comments/1") in rc.serp_features(t)
    # №70 evidence, history and discovery
    assert "ranking not checked" in evidence_cell({"url": "u", "position": None}, "live") or \
        "position not recorded" in evidence_cell({"url": "u", "position": None}, "live")
    assert evidence_cell({"url": "u", "position": 3}, "live").startswith("Google ranking verified: #3")
    assert evidence_cell(None, "live") == "Example URL verified live · Google ranking not checked"
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        old = os.path.join(d, "old.csv")
        with open(old, "w", newline="", encoding="utf-8") as f:
            wr = csv.DictWriter(f, fieldnames=["post", "product", "position", "platform", "more_posts", "best_position", "product_names", "checked"])
            wr.writeheader()
            wr.writerow({"post": "https://known.example/t/a-review", "product": "Acme", "position": "2",
                         "platform": "known.example", "checked": "2026-10-24"})
        hist = load_history([old])
        known = {"platform": "known.example", "domain": "known.example", "best_position": "",
                 "pages": [{"url": "https://known.example/t/a-review", "position": None}]}
        assert discovery_cell(known, hist, set()) == "EXISTING · repeated from saved research"
        cell, conflict = history_cell(known, hist, "live")
        assert "#2" in cell and "2026-10-24" in cell and "recheck" in conflict      # history kept, conflict reported
        known2 = dict(known, pages=[{"url": "https://known.example/t/b-review", "position": 5}], best_position=5)
        assert discovery_cell(known2, hist, set()) == "EXISTING · NEW evidence"
        fresh = {"platform": "fresh.example", "domain": "fresh.example", "best_position": 4,
                 "pages": [{"url": "https://fresh.example/x", "position": 4}]}
        assert discovery_cell(fresh, hist, set()) == "NEW platform" and history_cell(fresh, hist, "live") == ("", "")
    # №91 blocked host: evidence from the feed, sitemap or public API instead of dropping the page
    T = "https://forum.example.com/t/acme-review/123"

    def fake(routes):
        def get(u):
            if u in routes:
                code, ctype, body = routes[u]
                return code, u, {"content-type": ctype}, body.encode()
            return 404, u, {"content-type": "text/html"}, b"<html>not found</html>"
        return get
    rss = ("<rss><channel><title>Forum</title><item><title>Acme review — 3 months</title>"
           "<link>https://forum.example.com/t/acme-review/123/4</link><pubDate>Thu, 20 Nov 2026 10:00:00 +0000</pubDate>"
           "</item></channel></rss>")
    blocked = {T: (403, "text/html", "<title>Just a moment...</title>")}
    r = check_url(T, get=fake(blocked | {"https://forum.example.com/feed": (200, "application/rss+xml", rss)}))
    assert r["availability"] == BLOCKED and r["evidence_source"] == "RSS/Atom feed" and r["evidence_date"] == "2026-11-20", r
    assert r["why"].startswith("blocked — evidence from RSS/Atom feed") and verdict(r)[0] == "blocked"
    idx = ('<sitemapindex><sitemap><loc>https://forum.example.com/sm-old.xml</loc><lastmod>2025-01-01</lastmod></sitemap>'
           '<sitemap><loc>https://forum.example.com/sm-new.xml</loc><lastmod>2026-11-01</lastmod></sitemap></sitemapindex>')
    sm = f"<urlset><url><loc>{T}</loc><lastmod>2026-11-02T08:00:00Z</lastmod></url></urlset>"
    r = check_url(T, get=fake(blocked | {"https://forum.example.com/robots.txt": (200, "text/plain", "Sitemap: https://forum.example.com/smi.xml"),
                                         "https://forum.example.com/smi.xml": (200, "application/xml", idx),
                                         "https://forum.example.com/sm-new.xml": (200, "application/xml", sm)}))
    assert r["evidence_source"] == "sitemap" and r["evidence_date"] == "2026-11-02", r
    api = json.dumps({"id": 123, "title": "Acme review", "posts_count": 7, "created_at": "2026-10-30T09:00:00Z"})
    r = check_url(T, get=fake(blocked | {"https://forum.example.com/t/123.json": (200, "application/json", api)}))
    assert r["evidence_source"] == "Discourse API" and "7 posts" in r["why"] and r["evidence_date"] == "2026-10-30", r
    r = check_url(T, get=fake(blocked | {"https://forum.example.com/t/123.json": (404, "application/json", '{"errors":["not found"]}')}))
    assert r["availability"] == GONE and "removed per Discourse API" in r["why"], r
    r = check_url(T, get=fake(blocked))
    assert r["availability"] == BLOCKED and not r.get("evidence_source") and "no feed, sitemap or public API" in r["why"]
    assert verdict(r)[0] == "unknown"
    wp = "https://blog.example.org/acme-review/"
    wpj = json.dumps([{"link": wp, "date": "2026-11-11T10:00:00", "title": {"rendered": "Acme review"}}])
    r = check_url(wp, get=fake({wp: (429, "text/html", ""), "https://blog.example.org/wp-json/wp/v2/posts?slug=acme-review&_fields=link,date,title": (200, "application/json", wpj)}))
    assert r["evidence_source"] == "WordPress REST API" and r["evidence_date"] == "2026-11-11", r
    assert evidence_cell({"url": T, "position": 4, "evidence_source": "sitemap", "evidence_date": "2026-11-02"}, "blocked") == \
        "blocked — evidence from sitemap (2026-11-02) · seen at #4 in the search · indexing not verified"
    # №90 targeted verification: pick the most promising few, cost first, two separate lists
    cands = [{"url": "https://forum.a.example/t/acme-review/1", "query": "acme review", "product": "Acme", "type": "forum", "status": "live"},
             {"url": "https://forum.a.example/t/zeta-review/2", "query": "zeta review", "product": "Zeta", "type": "forum", "status": "live"},
             {"url": "https://docs.b.example/acme", "query": "acme review", "product": "Acme", "type": "document", "status": "live"},
             {"url": "https://gone.c.example/acme", "query": "acme review", "product": "Acme", "status": "removed"},
             {"url": "https://blk.d.example/t/acme/9", "query": "acme reviews", "product": "Acme", "type": "forum", "status": "blocked"},
             {"url": "https://x.e.example/acme", "query": "acme review", "product": "Acme", "type": "page", "status": "unknown"}]
    ch = pick(cands, 3)
    assert [c["url"] for c in ch] == ["https://forum.a.example/t/acme-review/1", "https://docs.b.example/acme",
                                      "https://blk.d.example/t/acme/9"], ch
    assert all("gone.c.example" not in c["url"] for c in pick(cands, 10))           # removed pages are never paid for
    assert len({host_of(c["url"]) for c in ch}) == 3                                # one page per domain first
    cost = verify_cost(ch, "serpapi")
    assert cost["index"] == 3 and cost["searches"] == 3 + cost["positions"] and cost["label"].startswith("~")
    assert verify_cost(ch, "dataforseo")["label"].startswith("~$")
    seen = []

    def search(q, depth):
        seen.append(q)
        if q.startswith("site:forum.a.example"):
            return [{"position": 1, "url": "https://forum.a.example/t/acme-review/1", "title": "Acme", "snippet": "Acme review thread", "date": "Nov 3, 2026"}]
        if q == "acme review":
            return [{"position": 2, "url": "https://docs.b.example/other"}, {"position": 6, "url": "https://forum.a.example/t/acme-review/1/"}]
        return []
    res = verify_pages(ch, search, 10, "2026-11-28")
    by = {r["url"]: r for r in res}
    z = by["https://forum.a.example/t/acme-review/1"]
    assert z["indexed"] and z["position"] == 6 and z["index_cell"].startswith("indexed ✓") and z["position_cell"].startswith("#6")
    d = by["https://docs.b.example/acme"]
    assert not d["indexed"] and "not in Google's index" in d["index_cell"] and "another page of the domain at #2" in d["position_cell"]
    assert by["https://blk.d.example/t/acme/9"]["position_cell"].startswith('not in top 10 for "acme reviews"')
    assert len(seen) == len(set(seen))                                            # one search per unique query
    import tempfile
    with tempfile.TemporaryDirectory() as dd:
        tsv = os.path.join(dd, "c.tsv")
        with open(tsv, "w", encoding="utf-8") as f:
            f.write("# found by web search\nhttps://f.example/t/a-review\tacme review\tAcme\tforum\nhttps://f.example/t/a-review/\tdup\n")
        assert [c["query"] for c in read_candidates(tsv)] == ["acme review"]
    print("self-test ok")


def main():
    ap = argparse.ArgumentParser(description="Platforms where affiliate review pages rank now (DataForSEO or SerpApi) + free live check")
    ap.add_argument("products", nargs="?")
    ap.add_argument("--provider", default="dataforseo", choices=["dataforseo", "serpapi"])
    ap.add_argument("--suffix", default="review", help='added to each product: "review" (default), "reviews", "complaints"…')
    ap.add_argument("--country", default="us"); ap.add_argument("--language", default="en")
    ap.add_argument("--depth", type=int, default=10, help="top 10 by default: that is where the traffic is"); ap.add_argument("--device", default="desktop", choices=["desktop", "mobile"])
    ap.add_argument("--base", help="the user's journal: platforms already in their base are marked 'yours'")
    ap.add_argument("--out", default="platforms-scan.csv")
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument("--live", action="store_true"); ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--wait", type=int, default=15)
    ap.add_argument("--exclusions", help="saved JSON answer of the server's exclusions_get (stop types, blacklist, dead)")
    ap.add_argument("--exclude", default="", help="the user's own exclusions: domain[/path],…")
    ap.add_argument("--collect-only", action="store_true", help="search + group only; write <out>.raw.json and the example URLs for the local private filter")
    ap.add_argument("--from-raw", help="continue from a --collect-only file (free: live check, sign-up links, output)")
    ap.add_argument("--allowed", help='JSON {"allowed": [...]} from privfilter.py: only these example posts are shown')
    ap.add_argument("--no-live-check", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--no-signup", action="store_true", help="skip the sign-up link search")
    ap.add_argument("--auth-fd", help=argparse.SUPPRESS)
    ap.add_argument("--history", default="", help="earlier scans / research CSVs, comma-separated (the previous --out file is always read too): "
                                                  "platforms found before are marked EXISTING and their old rankings are shown, never overwritten")
    ap.add_argument("--self-test", action="store_true", help="offline test of exclusions and the live-check rules")
    ap.add_argument("--check-urls", help="free page check only: a file with one URL per line (optionally TAB + expected thread title); "
                                         "prints thread availability and indexing eligibility as two fields (№71)")
    ap.add_argument("--verify", help="№90 targeted verification: a file of hosted results from free discovery "
                                      "(URL<TAB>target query[<TAB>product][<TAB>type], or a CSV with url/post + query/product); "
                                      "the top --top pages get a Google index check (site:) and a position check on the user's account")
    ap.add_argument("--top", type=int, default=VERIFY_TOP, help="how many pages --verify checks in Google (default 5)")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if a.verify:
        if a.out == "platforms-scan.csv":
            a.out = "platforms-verify.csv"
        return verify_cli(a)
    if a.check_urls:
        return check_urls_cli(a.check_urls, a.out if a.out != "platforms-scan.csv" else "")

    ex = load_exclusions(a.exclusions, a.exclude.split(","))
    base_out = os.path.splitext(a.out)[0]
    if a.from_raw:
        with open(a.from_raw, encoding="utf-8") as f:
            raw = json.load(f)
        platforms, skipped = raw["platforms"], raw["skipped"]
        # the server list may be newer than the collect step: apply it again
        keep = []
        for p in platforms:
            hit = excluded("https://" + p["domain"] + "/", p["type"], ex) or \
                next((excluded(pg["url"], p["type"], ex) for pg in p["pages"] if excluded(pg["url"], p["type"], ex)), None)
            if hit:
                skipped.setdefault(hit[0], []).append(p["domain"])
            else:
                keep.append(p)
        platforms = keep
    else:
        if not a.products:
            ap.error("PRODUCTS is required (or --from-raw / --self-test)")
        products = read_products(a.products)[: a.limit]
        if not products:
            sys.exit("No product names found.")
        results, queries = run_search(a, products)
        if results is None:
            return
        platforms, skipped = group(results, queries, products, ex)
        print(f"- {len(results)} result pages read · {len(platforms)} platforms before checks")
        if a.collect_only:
            with open(base_out + ".raw.json", "w", encoding="utf-8") as f:
                json.dump({"platforms": platforms, "skipped": skipped, "date": date.today().isoformat()}, f)
            urls = [pg["url"] for p in platforms if p["cost"] != "abuse" for pg in p["pages"][:3]]
            with open(base_out + ".examples.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(urls) + "\n")
            print(f"- saved {base_out}.raw.json and {len(urls)} example URLs in {base_out}.examples.txt "
                  f"→ run privfilter.py on them, then: --from-raw {base_out}.raw.json --allowed allowed.json")
            return

    yours = set()
    if a.base and os.path.exists(a.base):
        yours = {k for k in w.read_platforms(w.platforms_path(a.base))}
        yours |= {p["platform"].lower() for p in w.page_states(w.read_rows(a.base), date.today()).values() if p.get("platform")}
    if a.no_live_check:
        for p in platforms:
            p["live"] = "unverified"
    else:
        print(f"- free live check of up to 3 example pages on {len([p for p in platforms if p['cost'] != 'abuse'])} platforms…")
        verify(platforms, signup=not a.no_signup)
    hist_paths = [x.strip() for x in a.history.split(",") if x.strip()] + [a.out]
    hist = load_history(hist_paths, a.base, date.today())          # read BEFORE the new scan overwrites --out
    report(platforms, skipped, a.out, load_allowed(a.allowed), yours, date.today().isoformat(), hist)


if __name__ == "__main__":
    main()
