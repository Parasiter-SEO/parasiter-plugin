#!/usr/bin/env python3
"""PARASITER — "Export my base": everything the user built, in one zip they keep.

Usage:
  python3 export.py JOURNAL [--out parasite-seo-export-YYYY-MM-DD.zip] [--lang en] [--no-excel] [--today YYYY-MM-DD]

What goes in the zip:
  original/            every PARASITER file from the project folder, byte for byte
                       (journal, sales, platforms, links, keywords, profile, goals, writer notes)
  parasite-seo-base.xlsx   the same data as an Excel workbook (Posts · Platforms · Sales · Links · Journal),
                       built by mybase.py when a journal exists
  README.txt           what each file is and how to bring the base back

Works on any plan and without a key: the data is the user's, it never lives on the PARASITER server.
Reads the files, never writes to them. Standard library only.
"""
import argparse
import hashlib
import os
import sys
import tempfile
import zipfile
from datetime import date, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

FILES = [
    ("parasite-seo-progress.csv", "Work journal: pages, checks, audits, traffic, imports"),
    ("parasite-seo-sales.csv", "Sales and conversions (manual and imported)"),
    ("parasite-seo-platforms.csv", "Your personal platform base"),
    ("parasite-seo-links.csv", "Your affiliate links and products"),
    ("parasite-seo-keywords.csv", "Keywords your pages rank for"),
    ("parasite-seo-queue.csv", "Publication queue: your next pages, ranked, planned and published"),
    ("parasite-seo-queue-settings.json", "Publication queue mix (scale / expand / explore)"),
    ("parasite-seo-profile.md", "Your PARASITER profile: role, language, time, settings"),
    ("parasite-seo-goals.md", "Goals, milestones and weekly targets"),
    ("parasite-seo-writer.md", "Writer settings: voice, author block, disclosure"),
]
PREFIX = "parasite-seo-"
SKIP_EXT = (".zip", ".xlsx", ".html", ".pdf", ".docx", ".jpg", ".png")


def collect_files(folder):
    """Known files first (with their description), then any other parasite-seo-* data file in the folder."""
    known = {n for n, _ in FILES}
    found = [(n, desc) for n, desc in FILES if os.path.isfile(os.path.join(folder, n))]
    for n in sorted(os.listdir(folder)):
        if n.startswith(PREFIX) and n not in known and not n.lower().endswith(SKIP_EXT) \
                and not n.startswith(PREFIX + "export") and os.path.isfile(os.path.join(folder, n)):
            found.append((n, "Other PARASITER data file"))
    return found


def readme(found, excel, today):
    lines = [
        "PARASITER — your base, exported " + today.isoformat(),
        "",
        "This is everything PARASITER keeps for you. It was always in your own folder;",
        "this zip is a copy you can store anywhere. Your journal, sales and links never go to the PARASITER server.",
        "",
        "FILES",
    ]
    for n, desc in found:
        lines.append(f"  original/{n}  —  {desc}")
    if excel:
        lines.append("  parasite-seo-base.xlsx  —  the same data as an Excel workbook (Excel, Google Sheets, Numbers, LibreOffice)")
    lines += [
        "",
        "BRING IT BACK",
        "  1. Put the files from original/ into the folder where you work with Claude (your project folder).",
        "  2. Say \"my base\" or \"journal\" — PARASITER picks up where you stopped.",
        "  Nothing is lost when a plan ends: the files are plain CSV and Markdown, readable without PARASITER.",
        "",
        "CHECKSUMS (SHA-256)",
    ]
    return lines


def main():
    ap = argparse.ArgumentParser(description="PARASITER: export the user's whole base into one zip")
    ap.add_argument("journal", help="parasite-seo-progress.csv (or any file in the project folder)")
    ap.add_argument("--out")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--no-excel", action="store_true")
    ap.add_argument("--today")
    a = ap.parse_args()

    folder = os.path.dirname(os.path.abspath(a.journal))
    if not os.path.isdir(folder):
        sys.exit(f"Folder not found: {folder}")
    today = datetime.strptime(a.today, "%Y-%m-%d").date() if a.today else date.today()
    found = collect_files(folder)
    if not found:
        sys.exit(f"No PARASITER files in {folder} — nothing to export yet.")
    out = a.out or os.path.join(folder, f"parasite-seo-export-{today.isoformat()}.zip")

    excel = None
    journal = os.path.join(folder, "parasite-seo-progress.csv")
    if not a.no_excel and os.path.isfile(journal):
        try:
            import mybase
            t = mybase.L.get(a.lang, mybase.L["en"])
            d = mybase.collect(journal, today)
            tmp = tempfile.mkdtemp()
            excel = os.path.join(tmp, "parasite-seo-base.xlsx")
            mybase.build_workbook(d, t, excel)
        except Exception as e:          # the raw files are the export; Excel is a bonus
            print(f"Excel skipped ({e.__class__.__name__}: {e}); the original files are all in the zip.")
            excel = None

    lines = readme(found, bool(excel), today)
    total = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for n, _ in found:
            p = os.path.join(folder, n)
            with open(p, "rb") as f:
                data = f.read()
            total += len(data)
            z.writestr("original/" + n, data)
            lines.append(f"  {hashlib.sha256(data).hexdigest()}  original/{n}")
        if excel:
            z.write(excel, "parasite-seo-base.xlsx")
        z.writestr("README.txt", "\n".join(lines) + "\n")

    rows = 0
    for n, _ in found:
        if n.endswith(".csv"):
            with open(os.path.join(folder, n), encoding="utf-8", errors="replace") as f:
                rows += max(0, sum(1 for _ in f) - 1)
    print(f"Export: {out}")
    print(f"{len(found)} files · {rows} rows · {total // 1024 + 1} KB" + (" · Excel workbook inside" if excel else ""))
    for n, _ in found:
        print(f"  - {n}")


if __name__ == "__main__":
    main()
