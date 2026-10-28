#!/usr/bin/env python3
"""PARASITER — visual report: one JSON spec in, a styled HTML report (and a PDF when possible) out.

Usage: python3 visual_report.py spec.json [--out report] [--no-pdf]

Writes <out>.html (self-contained: inline SVG charts, no external files) and, when Chromium via
Playwright or WeasyPrint is available, <out>.pdf (A4). Without either, open the HTML and print to PDF.

Spec (all keys optional except title):
{
  "title": "Performance report", "subtitle": "Parasite SEO · affiliate sales",
  "client": "Client or project", "period": "1–31 October 2026", "prepared_by": "Agency / name",
  "date": "2026-10-28", "lang": "en",
  "kpis":   [{"label": "Commission", "value": "$1,234", "note": "approved, from network data"}],
  "charts": [{"type": "bars",  "title": "...", "labels": ["Jan", ...], "series": [{"name": "A", "values": [..]}],
              "unit": "$", "note": "..."},
             {"type": "hbars", "title": "...", "labels": [...], "values": [...], "unit": "", "note": "..."},
             {"type": "line",  "title": "...", "labels": [...], "series": [...], "unit": "$"}],
  "tables": [{"title": "...", "columns": ["Page", "Platform"], "rows": [["<a href=...>..</a>", "..."]], "note": "..."}],
  "sections": [{"title": "What worked", "items": ["...", "..."]}],
  "footnote": "Numbers come from ... Estimates are labelled."
}
Text is escaped except table cells that start with "<a " (links). Numbers in values must be plain numbers.
"""
import html
import json
import shutil
import subprocess
import sys
from pathlib import Path

# Categorical slots 1-3 validated all-pairs (light): blue, orange, aqua; 4-8 for bar/line adjacency only.
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
E = html.escape


def fmt(v, unit=""):
    if v is None:
        return "—"
    s = f"{v:,.0f}" if abs(v) >= 100 or float(v).is_integer() else f"{v:,.2f}"
    if unit in ("$", "€", "£"):
        return unit + s
    return f"{s} {unit}".strip()


def nice_max(m):
    if m <= 0:
        return 1
    mag = 10 ** (len(str(int(m))) - 1)
    for step in (1, 2, 2.5, 5, 10):
        if step * mag >= m:
            return step * mag
    return 10 * mag


def legend(series):
    if len(series) < 2:
        return ""
    items = "".join(f'<span class="lg"><i style="background:{SERIES[i % 8]}"></i>{E(s["name"])}</span>'
                    for i, s in enumerate(series))
    return f'<div class="legend">{items}</div>'


def bars(c):
    labels, series, unit = c["labels"], c["series"], c.get("unit", "")
    W, H, L, B, T = 680, 260, 52, 28, 12
    vmax = nice_max(max((v or 0) for s in series for v in s["values"]))
    pw, ph = W - L - 8, H - B - T
    gw = pw / len(labels)
    n = len(series)
    bw = max(3, min(22, (gw - 10) / n - 2))
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{E(c["title"])}">']
    for k in range(5):
        v = vmax * k / 4
        y = T + ph - ph * k / 4
        out.append(f'<line x1="{L}" x2="{W - 8}" y1="{y:.1f}" y2="{y:.1f}" class="grid"/>'
                   f'<text x="{L - 6}" y="{y + 4:.1f}" class="ax" text-anchor="end">{E(fmt(v, unit))}</text>')
    for gi, lab in enumerate(labels):
        x0 = L + gi * gw + (gw - n * (bw + 2) + 2) / 2
        for si, s in enumerate(series):
            v = s["values"][gi] or 0
            h = ph * v / vmax
            x, y = x0 + si * (bw + 2), T + ph - h
            r = min(4, bw / 2, h)
            path = (f"M{x:.1f},{T + ph:.1f} V{y + r:.1f} Q{x:.1f},{y:.1f} {x + r:.1f},{y:.1f} "
                    f"H{x + bw - r:.1f} Q{x + bw:.1f},{y:.1f} {x + bw:.1f},{y + r:.1f} V{T + ph:.1f} Z") if h > 0 else ""
            if path:
                out.append(f'<path d="{path}" fill="{SERIES[si % 8]}"><title>{E(s["name"])} · {E(lab)}: {E(fmt(v, s.get("unit", unit)))}</title></path>')
        out.append(f'<text x="{L + gi * gw + gw / 2:.1f}" y="{H - 8}" class="ax" text-anchor="middle">{E(lab)}</text>')
    out.append(f'<line x1="{L}" x2="{W - 8}" y1="{T + ph}" y2="{T + ph}" class="base"/></svg>')
    return legend(series) + "".join(out)


def line(c):
    labels, series, unit = c["labels"], c["series"], c.get("unit", "")
    W, H, L, B, T = 680, 260, 52, 28, 14
    vmax = nice_max(max((v or 0) for s in series for v in s["values"]))
    pw, ph = W - L - 16, H - B - T
    step = pw / max(1, len(labels) - 1)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{E(c["title"])}">']
    for k in range(5):
        y = T + ph - ph * k / 4
        out.append(f'<line x1="{L}" x2="{W - 16}" y1="{y:.1f}" y2="{y:.1f}" class="grid"/>'
                   f'<text x="{L - 6}" y="{y + 4:.1f}" class="ax" text-anchor="end">{E(fmt(vmax * k / 4, unit))}</text>')
    for i, lab in enumerate(labels):
        out.append(f'<text x="{L + i * step:.1f}" y="{H - 8}" class="ax" text-anchor="middle">{E(lab)}</text>')
    for si, s in enumerate(series):
        pts = [(L + i * step, T + ph - ph * (v or 0) / vmax) for i, v in enumerate(s["values"])]
        col = SERIES[si % 8]
        out.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{col}" stroke-width="2" stroke-linejoin="round"/>')
        for (x, y), v, lab in zip(pts, s["values"], labels):
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{col}" class="pt"><title>{E(s["name"])} · {E(lab)}: {E(fmt(v, unit))}</title></circle>')
    out.append(f'<line x1="{L}" x2="{W - 16}" y1="{T + ph}" y2="{T + ph}" class="base"/></svg>')
    return legend(series) + "".join(out)


def hbars(c):
    labels, values, unit = c["labels"], c["values"], c.get("unit", "")
    vmax = max(values) or 1
    rows = []
    for lab, v in zip(labels, values):
        w = 100 * v / vmax
        rows.append(f'<div class="hb"><span class="hl">{E(lab)}</span><span class="ht"><i style="width:{w:.1f}%;background:{SERIES[0]}"></i></span>'
                    f'<b>{E(fmt(v, unit))}</b></div>')
    return f'<div class="hbars">{"".join(rows)}</div>'


def chart(c):
    body = {"bars": bars, "line": line, "hbars": hbars}[c.get("type", "bars")](c)
    note = f'<p class="cn">{E(c["note"])}</p>' if c.get("note") else ""
    wide = " wide" if c.get("type", "bars") != "hbars" else ""
    return f'<figure class="card{wide}"><figcaption>{E(c["title"])}</figcaption>{body}{note}</figure>'


def cell(v):
    v = "" if v is None else str(v)
    return v if v.startswith("<a ") else E(v)


def table(t):
    head = "".join(f"<th>{E(c)}</th>" for c in t["columns"])
    rows = "".join("<tr>" + "".join(f"<td>{cell(v)}</td>" for v in r) + "</tr>" for r in t["rows"])
    note = f'<p class="cn">{E(t["note"])}</p>' if t.get("note") else ""
    return f'<section class="card wide tbl"><h2>{E(t["title"])}</h2><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>{note}</section>'


def section(s):
    items = "".join(f"<li>{E(i)}</li>" for i in s.get("items", []))
    return f'<section class="card"><h2>{E(s["title"])}</h2><ul>{items}</ul></section>'


CSS = """
:root{--paper:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--muted:#7a7974;--line:#e4e2dc;--accent:#2a78d6;--soft:#f3f2ee}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#1a1a19;--ink:#f0efec;--ink2:#c3c2b7;--muted:#9a998f;--line:#34332f;--soft:#24241f}}
:root[data-theme="dark"]{--paper:#1a1a19;--ink:#f0efec;--ink2:#c3c2b7;--muted:#9a998f;--line:#34332f;--soft:#24241f}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.5 "Inter","Segoe UI",system-ui,-apple-system,sans-serif}
main{max-width:860px;margin:0 auto;padding:36px 16px 48px}
header.top{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;border-bottom:2px solid var(--ink);padding-bottom:16px;margin-bottom:22px}
.eyebrow{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
h1{font-size:28px;line-height:1.15;margin:4px 0 4px;letter-spacing:-.02em}
.sub{color:var(--ink2);margin:0}
.meta{text-align:right;font-size:13px;color:var(--ink2)}
.meta b{color:var(--ink);font-weight:600}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(128px,1fr));gap:10px;margin-bottom:18px}
.kpi{background:var(--soft);border-radius:10px;padding:12px 14px}
.kpi .l{font-size:12px;color:var(--ink2)}
.kpi .v{font-size:26px;font-weight:650;letter-spacing:-.02em;font-variant-numeric:tabular-nums;line-height:1.2;margin-top:2px}
.kpi .n{font-size:12px;color:var(--muted)}
.grid2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
.card{border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin:0;break-inside:avoid}
.card.wide{grid-column:1/-1}
figcaption,.card h2{font-size:15px;font-weight:650;margin:0 0 8px}
svg{width:100%;height:auto;display:block}
.grid{stroke:var(--line);stroke-width:1}
.base{stroke:var(--ink2);stroke-width:1}
.ax{font-size:11px;fill:var(--muted);font-variant-numeric:tabular-nums}
.pt{stroke:var(--paper);stroke-width:2}
.legend{display:flex;gap:14px;flex-wrap:wrap;font-size:12px;color:var(--ink2);margin-bottom:6px}
.lg i{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:6px;vertical-align:-1px}
.hbars{display:grid;gap:8px}
.hb{display:grid;grid-template-columns:minmax(80px,42%) 1fr auto;gap:10px;align-items:center;font-size:13px}
.hl{color:var(--ink2);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.ht{height:12px;background:var(--soft);border-radius:4px;overflow:hidden}
.ht i{display:block;height:100%;border-radius:0 4px 4px 0}
.hb b{font-variant-numeric:tabular-nums;font-weight:600}
.cn{font-size:12px;color:var(--muted);margin:8px 0 0}
table{width:100%;border-collapse:collapse;font-size:13px}
th{text-align:left;font-weight:600;color:var(--ink2);border-bottom:1px solid var(--ink2);padding:6px 8px 6px 0}
td{border-bottom:1px solid var(--line);padding:6px 8px 6px 0;vertical-align:top;overflow-wrap:break-word}
td:first-child{white-space:nowrap}
.card.tbl{break-inside:auto}
.secs{grid-column:1/-1;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
td a{color:var(--accent);text-decoration:none}
ul{margin:0;padding-left:18px}
li{margin:4px 0}
.foot{font-size:12px;color:var(--muted);margin-top:18px;border-top:1px solid var(--line);padding-top:10px}
@media (max-width:640px){.grid2,.secs{grid-template-columns:1fr}.meta{text-align:left}.hb{grid-template-columns:1fr auto}.hl{grid-column:1/-1}}
@page{size:A4;margin:14mm 12mm}
@media print{:root{--paper:#fff}body{font-size:12.5px}main{padding:0;max-width:none}.card{border-color:#ddd}a{color:inherit}}
"""


def render(spec):
    kp = "".join(f'<div class="kpi"><div class="l">{E(k["label"])}</div><div class="v">{E(str(k["value"]))}</div>'
                 + (f'<div class="n">{E(k["note"])}</div>' if k.get("note") else "") + "</div>" for k in spec.get("kpis", []))
    secs = [section(s) for s in spec.get("sections", [])]
    blocks = [chart(c) for c in spec.get("charts", [])] + ([f'<div class="secs">{"".join(secs)}</div>'] if secs else []) + [table(t) for t in spec.get("tables", [])]
    meta = "".join(f"<div>{E(a)}: <b>{E(spec[k])}</b></div>" for k, a in (("client", "Client"), ("period", "Period"), ("prepared_by", "Prepared by"), ("date", "Date")) if spec.get(k))
    foot = f'<p class="foot">{E(spec["footnote"])}</p>' if spec.get("footnote") else ""
    return (f'<!doctype html><html lang="{E(spec.get("lang", "en"))}"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(spec["title"])}</title><style>{CSS}</style></head>'
            f'<body><main><header class="top"><div><div class="eyebrow">{E(spec.get("eyebrow", "Report"))}</div><h1>{E(spec["title"])}</h1>'
            f'<p class="sub">{E(spec.get("subtitle", ""))}</p></div><div class="meta">{meta}</div></header>'
            f'<div class="kpis">{kp}</div><div class="grid2">{"".join(blocks)}</div>{foot}</main></body></html>')


def to_pdf(html_path: Path, pdf_path: Path) -> str:
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page()
            pg.goto(html_path.resolve().as_uri())
            pg.emulate_media(media="print")
            pg.pdf(path=str(pdf_path), format="A4", print_background=True, prefer_css_page_size=True)
            b.close()
        return "playwright"
    except Exception:
        pass
    try:
        from weasyprint import HTML
        HTML(filename=str(html_path)).write_pdf(str(pdf_path))
        return "weasyprint"
    except Exception:
        pass
    for exe in ("chromium", "chromium-browser", "google-chrome", "chrome"):
        if shutil.which(exe):
            r = subprocess.run([exe, "--headless", "--disable-gpu", f"--print-to-pdf={pdf_path}", html_path.resolve().as_uri()],
                               capture_output=True, timeout=120)
            if r.returncode == 0 and pdf_path.exists():
                return exe
    return ""


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return
    spec = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    out = Path(args[args.index("--out") + 1]) if "--out" in args else Path(args[0]).with_suffix("")
    html_path = out.with_suffix(".html")
    html_path.write_text(render(spec), encoding="utf-8")
    print(f"HTML: {html_path}")
    if "--no-pdf" not in args:
        how = to_pdf(html_path, out.with_suffix(".pdf"))
        print(f"PDF: {out.with_suffix('.pdf')} (via {how})" if how else
              "PDF: not created (no Playwright, WeasyPrint or Chrome here). Open the HTML and print to PDF.")


if __name__ == "__main__":
    main()
