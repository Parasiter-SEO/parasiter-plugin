#!/usr/bin/env python3
"""PARASITER — publication queue: what to publish next, where, and why, ranked by what earns.

Built from the user's own base (journal, sales, platforms, links). Four buckets:
  fix      money pages to push or rescue: positions 4–20 → refresh; traffic but no sales → audit
  scale    a proven topic (top 10, earning, indexed, ★) missing on a strong platform (coverage gaps)
  expand   what the user sells but hasn't tried: products from the links library with no pages,
           earning offers written in only one or two content types
  explore  new offers and platforms: sister products of an earning program, a new platform
           while the base is below Rumer's rule (10 platforms)

File: parasite-seo-queue.csv next to the journal (one row per item, updated in place).
Mix:  parasite-seo-queue-settings.json — share of scale / expand / explore (default 70 / 20 / 10).

Commands:
  build   JOURNAL [--today D]                  refresh the queue from the base (run after every import)
  list    JOURNAL [--bucket B] [--status S] [--n 15] [--json]
  today   JOURNAL [--minutes 120] [--all-platforms] [--json]   what fits into today's time
  plan    JOURNAL (--ids 3,5 | --next N) [--date D]            put items into the plan (status planned)
  set     JOURNAL --id N --status planned|writing|published|skipped|proposed [--url U] [--date D] [--note T]
  mix     JOURNAL 70,20,10                     scale,expand,explore shares
  review  JOURNAL [--days 30]                  results of published queue items: what the queue brought

Standard library only. Uses worklog.py from the same folder.
"""
import argparse
import csv
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import date, timedelta
from types import SimpleNamespace

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import worklog as W  # noqa: E402

QCOLS = ["id", "added", "updated", "status", "bucket", "action", "score", "topic", "platform", "offer",
         "program", "content_type", "minutes", "why", "from_url", "planned_for", "page_url", "result", "note"]
STATUSES = ["proposed", "planned", "writing", "published", "reviewed", "skipped", "expired"]
OPEN = ("proposed", "planned", "writing")
BUCKETS = ["fix", "scale", "expand", "explore"]
BUCKET_LABEL = {"fix": "Fix & push", "scale": "Scale", "expand": "Expand", "explore": "Explore"}
DEFAULT_MIX = {"scale": 70, "expand": 20, "explore": 10}
FIX_PER_DAY = 2
SKIP_DAYS = 30
RUMER_PLATFORMS = 10
PROOF_MIN = 3  # page_strength: top 10 ≈ 3+, earning 3, ★ 2, indexed 1
# order in which content types are tried for an offer that already sells (content-type-selector)
TYPE_LADDER = ["single-review", "ab-comparison", "complaints", "pricing", "experience", "best-of", "discounts", "discussions"]
TYPE_ALIASES = {"review": "single-review", "product-review": "single-review", "vs": "ab-comparison",
                "comparison": "ab-comparison", "a-vs-b": "ab-comparison", "doubts": "complaints",
                "packages": "pricing", "price": "pricing", "personal-experience": "experience",
                "best": "best-of", "top": "best-of", "coupon": "discounts", "discount": "discounts"}
MIN_WRITE = {"book": 150, "document": 90, "article": 90, "blog": 75, "newsletter": 75, "page": 60,
             "site-builder": 60, "forum": 45, "community": 30, "q&a": 30, "podcast": 90,
             "presentation": 60, "video": 120, "social": 20, "own-site": 90}
MIN_ACTION = {"refresh": 30, "audit": 20, "republish": 45, "find-offers": 30, "find-platforms": 40}
SAY = {  # ready phrase for the user, in English; the assistant translates it into the working language
    "write": "write “{topic}” for {platform} — {ctype}",
    "republish": "republish {topic} on {platform}",
    "refresh": "refresh {url}",
    "audit": "audit {url}",
    "find-offers": "find products like {offer} in {program}",
    "find-platforms": "find a new platform for {topic}",
}


# ---------- files ----------

def qpath(journal):
    return os.path.join(os.path.dirname(os.path.abspath(journal)), "parasite-seo-queue.csv")


def spath(journal):
    return os.path.join(os.path.dirname(os.path.abspath(journal)), "parasite-seo-queue-settings.json")


def read_queue(journal):
    return W.read_csv(qpath(journal))


def write_queue(journal, items):
    with open(qpath(journal), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=QCOLS, extrasaction="ignore")
        w.writeheader()
        for it in sorted(items, key=lambda r: int(r["id"])):
            w.writerow(it)


def read_mix(journal):
    try:
        with open(spath(journal), encoding="utf-8") as f:
            m = json.load(f).get("mix") or {}
        if all(k in m for k in DEFAULT_MIX):
            return {k: float(m[k]) for k in DEFAULT_MIX}
    except (OSError, ValueError):
        pass
    return dict(DEFAULT_MIX)


def key_of(it):
    return "|".join((it.get(k) or "").strip().lower() for k in ("bucket", "action", "topic", "platform", "from_url"))


def norm_type(t):
    t = re.sub(r"[^a-z&-]+", "-", (t or "").lower()).strip("-")
    return TYPE_ALIASES.get(t, t)


def load(journal, today):
    a = SimpleNamespace(journal=journal, today=today, sales_path_override=None)
    return W.load(a)


# ---------- weights learned from the base (the feedback loop) ----------

def learned_weights(rows, pages, sales):
    """Commission per page by content type and by offer, relative to the base average.
    Every published queue item becomes a page here, so the queue learns from its own results."""
    comm_page = defaultdict(float)
    for r in sales:
        if r["_page"] and W.counted(r):
            comm_page[r["_page"]] += r["_c"]
    live = [p for p in pages.values() if not p["moved"]]
    tot = sum(comm_page.values())
    avg = tot / len(live) if live else 0
    by_type = defaultdict(list)
    for p in live:
        by_type[norm_type(p["content_type"])].append(comm_page.get(p["url"], 0.0))
    w_type = {}
    for t, v in by_type.items():
        if t and len(v) >= 3 and avg > 0:
            w_type[t] = max(0.7, min(1.4, (sum(v) / len(v)) / avg))
    # offer / program value: every counted sale, attributed or not
    offer_c, prog_c = defaultdict(float), defaultdict(float)
    for r in sales:
        if not W.counted(r):
            continue
        p = pages.get(r["_page"]) if r["_page"] else None
        off = ((p or {}).get("offer") or r.get("offer") or "").lower()
        prog = ((p or {}).get("program") or r.get("program") or "").lower()
        if off:
            offer_c[off] += r["_c"]
        if prog:
            prog_c[prog] += r["_c"]
    all_c = sum(prog_c.values()) or sum(offer_c.values())
    return w_type, offer_c, prog_c, all_c, comm_page


def display_names(pages, sales):
    """Original spelling of programs and offers (keys are lowercased)."""
    names = {}
    for x in list(pages.values()) + list(sales):
        for k in ("program", "offer"):
            v = (x.get(k) or "").strip()
            if v:
                names.setdefault(v.lower(), v)
    return names


def offer_weight(offer, program, offer_c, prog_c, all_c):
    if not all_c:
        return 1.0
    share = offer_c.get((offer or "").lower(), 0) / all_c or 0.5 * prog_c.get((program or "").lower(), 0) / all_c
    return 1.0 + min(0.6, share)


def minutes_for(action, ptype):
    if action == "write":
        return MIN_WRITE.get((ptype or "").lower(), 75)
    return MIN_ACTION.get(action, 30)


# ---------- candidates ----------

def candidates(journal, today):
    today_, rows, pages, sales = load(journal, today)
    reg = W.read_platforms(W.platforms_path(journal))
    cov = W.coverage_model(today_, rows, pages, sales, journal)
    plat, names = cov["plat"], cov["names"]
    w_type, offer_c, prog_c, all_c, comm_page = learned_weights(rows, pages, sales)
    nm = display_names(pages, sales)
    ptype = {k: (v.get("type") or "") for k, v in plat.items()}
    pname = {k: v["name"] for k, v in plat.items()}
    out = []

    def add(**kw):
        kw.setdefault("from_url", "")
        kw.setdefault("offer", "")
        kw.setdefault("program", "")
        kw.setdefault("content_type", "")
        kw["minutes"] = str(minutes_for(kw["action"], ptype.get((kw.get("platform") or "").lower())))
        out.append(kw)

    # ---- scale: proven topic missing on a strong platform
    for sc, topic, pl_name, best, why in cov["gaps"]:
        proof = W.page_strength(best, cov["earned"])
        if proof < PROOF_MIN:  # only indexed, no position or sales yet: not proven, wait for data
            continue
        ctype = norm_type(best["content_type"]) or ""
        w = offer_weight(best["offer"], best["program"], offer_c, prog_c, all_c) * w_type.get(ctype, 1.0)
        republish = any("removed" in x for x in why)
        pstr = plat.get(pl_name.lower(), {}).get("strength", 0)
        add(bucket="scale", action="republish" if republish else "write", raw=proof * (1 + max(0, pstr) / 10) * w, topic=topic,
            platform=pl_name, offer=best["offer"], program=best["program"], content_type=ctype,
            why="; ".join(why) or "proven topic", from_url=best["url"])

    live = [p for p in pages.values() if not p["moved"] and W.health(p) not in W.GONE and p["platform"]]

    # ---- fix: positions 4–20 → push into the top 3 / top 10
    for p in live:
        pos = p["position"]
        if pos is None or pos < 4 or pos > 20:
            continue
        gain = 6 if pos <= 10 else 3
        earn = comm_page.get(p["url"], 0)
        add(bucket="fix", action="refresh", raw=gain + (3 if earn > 0 else 0) + (2 if p["priority"] == "high" else 0),
            topic=p["topic_key"], platform=p["platform"], offer=p["offer"], program=p["program"],
            content_type=norm_type(p["content_type"]), from_url=p["url"],
            why=f"#{pos:.0f} — {'into the top 3' if pos <= 10 else 'into the top 10'} (Rumer: sales start in the top 3)"
                + (f"; earns {W.money(earn)}" if earn > 0 else ""))
    # ---- fix: traffic or affiliate clicks, no sales in 60 days
    s60 = (today_ - timedelta(days=60))
    clicks, views = defaultdict(float), defaultdict(float)
    for r in rows:
        if r["event"] in ("traffic", "stats") and r.get("page_url") and r["_d"] >= s60:
            clicks[r["page_url"]] += W.num(r.get("aff_clicks")) or 0
            views[r["page_url"]] += W.num(r.get("views")) or 0
    sold60 = {r["_page"] for r in sales if r["_page"] and r["_d"] >= s60 and W.counted(r) and r["_c"] > 0}
    for p in live:
        u = p["url"]
        if u in sold60 or p["age"] < 30 or not (clicks[u] >= 5 or views[u] >= 100):
            continue
        add(bucket="fix", action="audit", raw=4 + min(4, clicks[u] / 10) + min(2, views[u] / 500),
            topic=p["topic_key"], platform=p["platform"], offer=p["offer"], program=p["program"],
            content_type=norm_type(p["content_type"]), from_url=u,
            why=f"{views[u]:.0f} views, {clicks[u]:.0f} affiliate clicks in 60 days, no sales — first screen, CTA, intent")

    strong = [k for k in names if plat[k]["pages"] > 0 or plat[k]["priority"] == "high"]
    best_plat = strong[0] if strong else None

    # ---- expand: products in the links library with no pages
    lib = W.read_csv(W.links_path(journal))
    seen_prod = set()
    for r in lib:
        prod = r.get("product") or ""
        if not prod or prod.startswith("(") or (r["program"], prod) in seen_prod:
            continue
        seen_prod.add((r["program"], prod))
        lw = {w for w in re.split(r"[^a-z0-9]+", prod.lower()) if len(w) > 2 and w not in W.STOP}
        need = min(2, len(lw))
        covered = need and any(len(lw & set(re.split(r"[^a-z0-9]+", (p["topic_key"] + " " + p["offer"] + " " + p["url"]).lower()))) >= need
                               for p in live)
        if covered or not best_plat:
            continue
        pw = 1.0 + (0.8 if prog_c.get(r["program"].lower(), 0) > 0 else 0)
        comm = W.num((r.get("commission") or "").rstrip("%")) or 0
        add(bucket="expand", action="write", raw=3 * pw + comm / 20, topic=f"{prod} review", platform=pname[best_plat],
            offer=prod, program=r["program"], content_type="single-review",
            why=f"your link is ready, no page yet" + (f"; {r['program']} already pays you" if pw > 1 else "")
                + (f"; {r['commission']} commission" if r.get("commission") else ""))
    # ---- expand: earning offers written in only one or two content types
    by_offer = defaultdict(list)
    for p in live:
        if p["offer"]:
            by_offer[p["offer"].lower()].append(p)
    for off, ps in by_offer.items():
        if offer_c.get(off, 0) <= 0:
            continue
        have = {norm_type(p["content_type"]) for p in ps if p["content_type"]}
        if len(have) > 2:
            continue
        home = max(ps, key=lambda p: (comm_page.get(p["url"], 0), -(p["position"] or 99)))
        missing = [t for t in TYPE_LADDER if t not in have][:2]
        for i, t in enumerate(missing):
            add(bucket="expand", action="write", raw=5 + offer_c[off] / max(1.0, all_c) * 10 - i,
                topic=f"{ps[0]['offer']} · {t}", platform=home["platform"], offer=ps[0]["offer"], program=home["program"],
                content_type=t, from_url=home["url"],
                why=f"{ps[0]['offer']} earns {W.money(offer_c[off])}, written only as {', '.join(sorted(have)) or 'one type'} — new buyer intent")

    # ---- explore: sister products of an earning program; new platform below Rumer's rule
    lib_by_prog = Counter(r["program"].lower() for r in lib if not (r.get("product") or "").startswith("("))
    for prog, c in sorted(prog_c.items(), key=lambda x: -x[1])[:2]:
        if c <= 0 or lib_by_prog.get(prog, 0) > 3:
            continue
        top_offer = max((o for o in offer_c if any(p["program"].lower() == prog and p["offer"].lower() == o for p in live)),
                        key=lambda o: offer_c[o], default="")
        add(bucket="explore", action="find-offers", raw=4 + c / max(1.0, all_c) * 5, topic=f"sister products · {nm.get(prog, prog)}",
            platform="", offer=nm.get(top_offer, top_offer), program=nm.get(prog, prog),
            why=f"{nm.get(prog, prog)} pays you {W.money(c)} but you promote {lib_by_prog.get(prog, 0) or 'few'} of its products — same buyers, more products")
    active = [k for k, r in reg.items() if (r.get("state") or "active") in ("active", "testing")]
    if len(active) < RUMER_PLATFORMS and cov["gaps"]:
        top_topic = cov["gaps"][0][1]
        add(bucket="explore", action="find-platforms", raw=3.5, topic=top_topic, platform="",
            why=f"{len(active)} of {RUMER_PLATFORMS} platforms (Rumer's rule) — test 1–3 posts of your best topic on a new one")
    # normalise to 0–100 within each bucket: the score ranks items of the same kind
    top = defaultdict(float)
    for c in out:
        top[c["bucket"]] = max(top[c["bucket"]], c["raw"])
    for c in out:
        c["score"] = str(max(1, round(100 * c.pop("raw") / (top[c["bucket"]] or 1))))
    return today_, pages, out


# ---------- build: merge candidates into the queue, link published pages ----------

def link_published(items, pages, today):
    """Queue items that became pages: same platform, matching topic or offer, published after the item was added."""
    done = []
    for it in items:
        if it["status"] not in OPEN or it["action"] not in ("write", "republish") or not it["platform"]:
            continue
        added = W.pdate(it["added"]) or today
        words = {w for w in re.split(r"[^a-z0-9]+", (it["topic"] + " " + it["offer"]).lower()) if len(w) > 2 and w not in W.STOP}
        for p in pages.values():
            if p["platform"].lower() != it["platform"].lower() or p["date_unknown"] or p["published"] < added - timedelta(days=1):
                continue
            pw = set(re.split(r"[^a-z0-9]+", (p["topic_key"] + " " + p["offer"] + " " + p["url"]).lower()))
            if p["topic_key"] == it["topic"].lower() or (words and len(words & pw) >= min(2, len(words))):
                it.update(status="published", page_url=p["url"], updated=p["published"].isoformat())
                done.append(it)
                break
    return done


def cmd_build(a):
    today, pages, cands = candidates(a.journal, a.today)
    items = read_queue(a.journal)
    by_key = {key_of(it): it for it in items}
    nid = max((int(it["id"]) for it in items), default=0)
    fresh, kept, new = set(), 0, 0
    for c in cands:
        k = key_of(c)
        fresh.add(k)
        it = by_key.get(k)
        if it:
            if it["status"] == "skipped" and (today - (W.pdate(it["updated"]) or today)).days < SKIP_DAYS:
                continue
            if it["status"] in ("skipped", "expired", "proposed"):
                it.update(status="proposed", score=c["score"], why=c["why"], minutes=c["minutes"],
                          content_type=it.get("content_type") or c["content_type"], updated=today.isoformat())
                kept += 1
            elif it["status"] in ("planned", "writing"):
                it.update(score=c["score"], why=c["why"])
            continue
        nid += 1
        it = {**c, "id": str(nid), "added": today.isoformat(), "updated": today.isoformat(), "status": "proposed",
              "planned_for": "", "page_url": "", "result": "", "note": ""}
        items.append(it)
        by_key[k] = it
        new += 1
    expired = 0
    for it in items:
        if it["status"] == "proposed" and key_of(it) not in fresh:
            it.update(status="expired", updated=today.isoformat())
            expired += 1
    done = link_published(items, pages, today)
    write_queue(a.journal, items)
    open_n = Counter(it["bucket"] for it in items if it["status"] in OPEN)
    print(f"Queue {os.path.basename(qpath(a.journal))} · {today}: {new} new · {kept} updated · {expired} no longer relevant"
          f" · {len(done)} published from the queue")
    print("- Open: " + " · ".join(f"{BUCKET_LABEL[b]} {open_n.get(b, 0)}" for b in BUCKETS))
    for it in done:
        print(f"- ✓ #{it['id']} {it['topic']} → {it['platform']}: {W.short(it['page_url'], 60)}")
    if not cands:
        print("- Nothing to propose yet: import pages, sales and links first (import-pages, import-sales, import-links).")


# ---------- ordering by the mix ----------

def ordered(items, mix, fix_first=FIX_PER_DAY):
    """Fix items first (at most fix_first), then scale / expand / explore interleaved by the mix shares."""
    pool = {b: sorted([it for it in items if it["bucket"] == b], key=lambda it: -int(it["score"] or 0)) for b in BUCKETS}
    res = pool["fix"][:fix_first]
    rest_fix = pool["fix"][fix_first:]
    credit = {b: 0.0 for b in DEFAULT_MIX}
    total = sum(mix.values()) or 1
    while any(pool[b] for b in DEFAULT_MIX):
        for b in DEFAULT_MIX:
            credit[b] += mix[b] / total
        b = max((b for b in DEFAULT_MIX if pool[b]), key=lambda b: credit[b])
        credit[b] -= 1
        res.append(pool[b].pop(0))
    return res + rest_fix


def say(it):
    tpl = SAY.get(it["action"], "{topic}")
    return tpl.format(ctype=(it["content_type"] or "page").replace("-", " "), topic=it["topic"], platform=it["platform"],
                      url=W.short(it["from_url"], 60), offer=it["offer"] or "your best seller", program=it["program"])


def line(it):
    tgt = f" → **{it['platform']}**" if it["platform"] else ""
    ct = f" · {it['content_type']}" if it["content_type"] and it["action"] == "write" else ""
    when = f" · planned {it['planned_for']}" if it["planned_for"] and it["status"] in ("planned", "writing") else ""
    st = "" if it["status"] == "proposed" else f" [{it['status']}]"
    return (f"#{it['id']} **{it['topic']}**{tgt}{ct} · {it['action']} · ~{it['minutes']} min · {it['score']}/100{when}{st}\n"
            f"   why: {it['why']}\n   say: “{say(it)}”")


def as_json(its):
    return json.dumps([{k: it.get(k, "") for k in QCOLS} | {"say": say(it)} for it in its], ensure_ascii=False, indent=1)


def empty_msg(journal):
    if os.path.exists(qpath(journal)):
        return ("Nothing in the queue yet: it is built from your pages, positions, sales and links. "
                "Import them first (import-pages, import-sales, import-links), or pick a first topic with content-type-selector.")
    return "No queue yet: run `pubqueue.py build` first."


def cmd_list(a):
    items = read_queue(a.journal)
    if not items:
        sys.exit(empty_msg(a.journal))
    sts = [a.status] if a.status else list(OPEN)
    sel = [it for it in items if it["status"] in sts and (not a.bucket or it["bucket"] == a.bucket)]
    mix = read_mix(a.journal)
    sel = ordered(sel, mix, fix_first=len(sel) if a.bucket else FIX_PER_DAY)[: a.n]
    if a.json:
        print(as_json(sel))
        return
    open_n = Counter(it["bucket"] for it in items if it["status"] in OPEN)
    print(f"# Publication queue · mix {mix['scale']:.0f}/{mix['expand']:.0f}/{mix['explore']:.0f} (scale/expand/explore)\n")
    print(" · ".join(f"{BUCKET_LABEL[b]} {open_n.get(b, 0)}" for b in BUCKETS) + "\n")
    cur = None
    for it in sel:
        if a.bucket and cur != it["bucket"]:
            cur = it["bucket"]
        print(f"{BUCKET_LABEL[it['bucket']]} · " + line(it))
    print("\nNew pages are rewritten for each platform (new angle, the platform's format) — never copied.")


def cmd_today(a):
    items = read_queue(a.journal)
    if not items:
        sys.exit(empty_msg(a.journal))
    today = W.pdate(a.today) if a.today else date.today()
    reg = W.read_platforms(W.platforms_path(a.journal))
    high = {k for k, r in reg.items() if (r.get("priority") or "") == "high"}
    ok_plat = (lambda it: True) if (a.all_platforms or not high) else \
        (lambda it: not it["platform"] or it["platform"].lower() in high)
    due = [it for it in items if it["status"] in ("planned", "writing") and (W.pdate(it["planned_for"]) or today) <= today]
    due.sort(key=lambda it: (it["status"] != "writing", it["planned_for"], -int(it["score"] or 0)))
    pick, used = [], 0
    for it in due:
        pick.append(it)
        used += int(it["minutes"] or 0)
    others = [it for it in items if it["status"] == "proposed" and ok_plat(it)]
    for it in ordered(others, read_mix(a.journal)):
        m = int(it["minutes"] or 0)
        if used + m > a.minutes:
            continue
        pick.append(it)
        used += m
    if a.json:
        print(as_json(pick))
        return
    print(f"# From the queue for today · {used} of {a.minutes} min\n")
    if not pick:
        print("Nothing fits today's time" + (" on your ★ platforms (--all-platforms to widen)" if high and not a.all_platforms else "") + ".")
    for i, it in enumerate(pick, 1):
        tag = "planned" if it["status"] in ("planned", "writing") else BUCKET_LABEL[it["bucket"]]
        print(f"{i}. [{tag}] " + line(it))
    skipped_plat = sum(1 for it in items if it["status"] == "proposed" and not ok_plat(it))
    if skipped_plat:
        print(f"\n{skipped_plat} items are on platforms not marked ★ — kept in the queue (--all-platforms).")
    print("\nPut them into the plan: `plan --ids …`. Say “skip #N” for what you won't do — it comes back in 30 days only if still relevant.")


def cmd_plan(a):
    items = read_queue(a.journal)
    today = W.pdate(a.today) if a.today else date.today()
    when = (W.pdate(a.date) or today).isoformat()
    if a.ids:
        ids = {x.strip().lstrip("#") for x in a.ids.split(",") if x.strip()}
        sel = [it for it in items if it["id"] in ids and it["status"] in OPEN + ("skipped", "expired")]
        missing = ids - {it["id"] for it in sel}
        if missing:
            print("Not in the open queue: " + ", ".join(f"#{x}" for x in sorted(missing, key=int)))
    else:
        sel = ordered([it for it in items if it["status"] == "proposed"], read_mix(a.journal))[: a.next or 3]
    for it in sel:
        it.update(status="planned", planned_for=when, updated=today.isoformat())
    write_queue(a.journal, items)
    print(f"Planned for {when}: {len(sel)}")
    for it in sel:
        print("- " + line(it).split("\n")[0])


def cmd_set(a):
    items = read_queue(a.journal)
    today = W.pdate(a.today) if a.today else date.today()
    it = next((x for x in items if x["id"] == a.id.lstrip("#")), None)
    if not it:
        sys.exit(f"No item #{a.id} in the queue.")
    it.update(status=a.status, updated=(W.pdate(a.date) or today).isoformat())
    if a.status == "planned":
        it["planned_for"] = (W.pdate(a.date) or today).isoformat()
    if a.url:
        it["page_url"] = a.url
    if a.note:
        it["note"] = a.note
    write_queue(a.journal, items)
    print(f"#{it['id']} {it['topic']} → {it['platform'] or '—'}: {a.status}"
          + ("  (log the page in the journal too: `worklog.py add --event published …`)" if a.status == "published" and a.url else ""))


def cmd_mix(a):
    parts = [W.num(x) for x in a.shares.replace("/", ",").split(",")]
    if len(parts) != 3 or any(p is None or p < 0 for p in parts) or not sum(parts):
        sys.exit("Give three numbers: scale,expand,explore — e.g. 70,20,10.")
    mix = dict(zip(DEFAULT_MIX, parts))
    with open(spath(a.journal), "w", encoding="utf-8") as f:
        json.dump({"mix": mix}, f)
    print(f"Mix saved: scale {parts[0]:.0f} · expand {parts[1]:.0f} · explore {parts[2]:.0f}")


def cmd_review(a):
    today, rows, pages, sales = load(a.journal, a.today)
    items = read_queue(a.journal)
    link_published(items, pages, today)
    comm = defaultdict(float)
    for r in sales:
        if r["_page"] and W.counted(r):
            comm[r["_page"]] += r["_c"]
    by_b = defaultdict(lambda: [0, 0, 0, 0.0])  # items, earning, top10, commission
    print(f"# What the queue brought · {today}\n")
    for it in items:
        if it["status"] not in ("published", "reviewed") or not it["page_url"]:
            continue
        p = pages.get(it["page_url"]) or next((q for u, q in pages.items() if W.norm_url(u) == W.norm_url(it["page_url"])), None)
        if not p:
            continue
        c = comm.get(p["url"], 0.0)
        top = p["position"] is not None and p["position"] <= W.TOP
        res = f"{W.health(p)}" + (f", #{p['position']:.0f}" if p["position"] is not None else "") + (f", {W.money(c)}" if c else ", no sales yet")
        it["result"] = res
        if p["age"] >= a.days and it["status"] == "published":
            it.update(status="reviewed", updated=today.isoformat())
        b = by_b[it["bucket"]]
        b[0] += 1
        b[1] += 1 if c > 0 else 0
        b[2] += 1 if top else 0
        b[3] += c
        print(f"- #{it['id']} [{BUCKET_LABEL[it['bucket']]}] {it['topic']} → {it['platform']} · {p['age']} d · {res}")
    write_queue(a.journal, items)
    if not by_b:
        print("No queue items published yet.")
        return
    print("\n| Bucket | Pages | Earning | Top 10 | Commission |\n|---|---|---|---|---|")
    for b in BUCKETS:
        if b in by_b:
            n, e, t, c = by_b[b]
            print(f"| {BUCKET_LABEL[b]} | {n} | {e} | {t} | {W.money(c)} |")
    print("\nThese pages feed the next `build`: content types, offers and platforms that earn weigh more, the rest less.")


def main():
    ap = argparse.ArgumentParser(description="PARASITER publication queue")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("journal")
        p.add_argument("--today")

    b = sub.add_parser("build"); common(b); b.set_defaults(fn=cmd_build)
    ls = sub.add_parser("list"); common(ls)
    ls.add_argument("--bucket", choices=BUCKETS); ls.add_argument("--status", choices=STATUSES)
    ls.add_argument("--n", type=int, default=15); ls.add_argument("--json", action="store_true"); ls.set_defaults(fn=cmd_list)
    td = sub.add_parser("today"); common(td)
    td.add_argument("--minutes", type=int, default=120); td.add_argument("--all-platforms", action="store_true")
    td.add_argument("--json", action="store_true"); td.set_defaults(fn=cmd_today)
    pl = sub.add_parser("plan"); common(pl)
    pl.add_argument("--ids"); pl.add_argument("--next", type=int); pl.add_argument("--date"); pl.set_defaults(fn=cmd_plan)
    st = sub.add_parser("set"); common(st)
    st.add_argument("--id", required=True); st.add_argument("--status", required=True, choices=STATUSES)
    st.add_argument("--url"); st.add_argument("--date"); st.add_argument("--note"); st.set_defaults(fn=cmd_set)
    mx = sub.add_parser("mix"); common(mx); mx.add_argument("shares"); mx.set_defaults(fn=cmd_mix)
    rv = sub.add_parser("review"); common(rv); rv.add_argument("--days", type=int, default=30); rv.set_defaults(fn=cmd_review)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
