#!/usr/bin/env python3
"""Help sections, shared by the public Help page and its Ukrainian copy.

The plugin's help lives in skills/help/references/{catalog,how-to,faq}.md (English).
The site page https://parasiter.affiliatecredo.com/help.html is built from them by
parasiter-site/tools/build_help.py, which imports this module.

The Ukrainian copy lives in skills/help/uk/<same name>.md. Every section there is
written as

    ## Український заголовок {#english-slug}
    <!-- src: 1a2b3c4d5e -->
    body…

`src` is the fingerprint of the English section the translation was made from.
When the English section changes, the fingerprint no longer matches and the
Ukrainian page shows that section in English until the translation is updated.

    python3 tools/help_uk.py status   # which Ukrainian sections are missing or outdated
    python3 tools/help_uk.py stamp    # after translating: mark sections WITHOUT a src line as current

To update a translation: edit the Ukrainian section, delete its `<!-- src -->` line,
run `stamp`. Sections are matched by the English slug, so the order may differ.
"""
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_DIR = ROOT / "skills" / "help" / "references"
UK_DIR = ROOT / "skills" / "help" / "uk"
FILES = ["catalog", "how-to", "faq"]
# Sections that stay inside the plugin (tool names for Claude, not for readers).
SKIP = ("server-tools",)

HEAD = re.compile(r"^## +(.+?)\s*$")
ANCHOR = re.compile(r"\s*\{#([a-z0-9-]+)\}\s*$")
SRC = re.compile(r"^<!--\s*src:\s*([0-9a-f]+)\s*-->\s*$")
COMMENT = re.compile(r"<!--.*?-->", re.S)


def slug(title):
    t = re.sub(r"\(№\d+\)", "", title.lower())
    t = re.sub(r"[`*_\"'“”«»’]", "", t)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:60].rstrip("-")


def fingerprint(title, body):
    text = COMMENT.sub("", title + "\n" + body)
    text = re.sub(r"\s+", " ", text).strip()
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:10]


def parse(path):
    """[(slug, title, body, src)] for every '## ' section; text before the first one is dropped."""
    out, cur = [], None
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        m = HEAD.match(line)
        if m:
            if cur:
                out.append(cur)
            title = m.group(1)
            a = ANCHOR.search(title)
            if a:
                title = title[: a.start()]
            cur = {"slug": a.group(1) if a else slug(title), "title": title.strip(), "lines": [], "src": None}
            continue
        if cur is None:
            continue
        s = SRC.match(line)
        if s and not cur["lines"] and cur["src"] is None:
            cur["src"] = s.group(1)
            continue
        cur["lines"].append(line)
    if cur:
        out.append(cur)
    res, seen = [], set()
    for c in out:
        sl = c["slug"]
        if any(sl.startswith(k) for k in SKIP):
            continue
        n = 2
        while sl in seen:
            sl = f"{c['slug']}-{n}"; n += 1
        seen.add(sl)
        res.append((sl, c["title"], "\n".join(c["lines"]).strip("\n"), c["src"]))
    return res


def en(name, base=EN_DIR):
    return parse(Path(base) / f"{name}.md")


def uk(name, base=UK_DIR):
    p = Path(base) / f"{name}.md"
    return parse(p) if p.exists() else []


def status(en_dir=EN_DIR, uk_dir=UK_DIR):
    bad = 0
    for name in FILES:
        u = {s: src for s, _, _, src in uk(name, uk_dir)}
        for sl, title, body, _ in en(name, en_dir):
            fp = fingerprint(title, body)
            if sl not in u:
                print(f"missing   {name}.md  #{sl}  ({title})"); bad += 1
            elif u[sl] != fp:
                print(f"outdated  {name}.md  #{sl}  ({title})"); bad += 1
    print("All Ukrainian sections are current." if not bad else f"{bad} section(s) to translate.")
    return bad


def stamp(en_dir=EN_DIR, uk_dir=UK_DIR):
    for name in FILES:
        p = Path(uk_dir) / f"{name}.md"
        if not p.exists():
            continue
        fps = {sl: fingerprint(t, b) for sl, t, b, _ in en(name, en_dir)}
        lines, out, done = p.read_text(encoding="utf-8").splitlines(), [], 0
        for i, line in enumerate(lines):
            out.append(line)
            m = HEAD.match(line)
            a = ANCHOR.search(line) if m else None
            if a and a.group(1) in fps:
                nxt = lines[i + 1] if i + 1 < len(lines) else ""
                if not SRC.match(nxt):
                    out.append(f"<!-- src: {fps[a.group(1)]} -->"); done += 1
        p.write_text("\n".join(out) + "\n", encoding="utf-8")
        print(f"{name}.md: stamped {done}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "stamp":
        stamp()
    sys.exit(1 if status() and cmd == "status" else 0)
