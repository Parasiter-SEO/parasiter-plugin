#!/usr/bin/env python3
"""PARASITER day plan (and weekly review) as a branded page — №25.

Usage:
  python3 dayplan.py plan.json                 # writes plan-today.html (+ plans/YYYY-MM-DD.html), prints the path
  python3 dayplan.py plan.json --out week.html # any other page with the same layout (weekly review, setup done)
  python3 dayplan.py panel.json                # "kind": "panel" → parasiter-panel.html (all skills under numbers, №26)
  python3 dayplan.py --self-test

plan.json (all text in the user's working language; only "title", "tasks" are required):
{
  "lang": "ru",                      # en | ru | uk — UI labels; anything else falls back to en
  "kind": "plan",                    # plan | week | setup — eyebrow label
  "title": "План на сегодня",
  "date": "2026-11-03",
  "hours": "4 ч",
  "goal": "$50/день к 1 мая 2027",
  "status": "Неделя 1 · отстаём на 1 день", "status_state": "behind",   # good | ok | behind | bad
  "kpis": [{"label": "Посты недели", "value": "0/3", "state": "behind"}, …],
  "tasks": [{"title": "Опубликовать D-Bal Max vs CrazyBulk D-Bal на HackMD", "time": "~45 мин",
             "by": "вы + журнал", "moves": "пост 1/3 · площадка 1/2",
             "say": "Я опубликовал: <ссылка>", "note": "необязательная строка"}],
  "callouts": [{"text": "Не опубликовано: 2 статьи (готовы с 02.11) — пришлите ссылки", "state": "ok"}],
  "why": "Пока ничего не опубликовано: одна живая страница сегодня даёт больше, чем три в черновиках.",
  "next": [{"say": "Напиши профиль автора", "what": "начнём с задачи 1"}],
  "explored": "Освоено: 8 из 21 скилов · 4 из 10 агентов",         # №26 panel (optional; "kind": "panel" = panel only)
  "bases": [{"code": "Б1", "name": "База площадок Rumer", "what": "проверенные площадки", "plan": "Pro"}, …],   # №32, first on the panel
  "panel": [{"name": "План", "items": [{"n": 1, "skill": "navigator", "what": "план на сегодня", "plan": "Pro",
                                         "tried": "03.11", "locked": false}, …]}, …]
}
Checkboxes are remembered in this browser only (localStorage); the plan itself stays in the user's folder.
"""
import html
import json
import os
import sys
from datetime import date

L = {
    "en": {"panel": "PARASITER PANEL", "bases": "Bases and data", "panel_h": "All functions — reply with a number", "menu0": "this menu any time", "tried": "tried", "untried": "not yet", "locked": "not on your plan", "plan": "TODAY'S PLAN", "week": "WEEKLY REVIEW", "setup": "SETUP DONE", "time": "Time today", "goal": "Goal",
           "tasks": "Tasks", "why": "Why this order", "next": "What's next — say", "copy": "Copy", "copied": "Copied",
           "done": "done", "by": "who", "moves": "moves", "of": "of", "foot": "PARASITER by Rumer · your plan stays in your folder"},
    "ru": {"panel": "ПУЛЬТ PARASITER", "bases": "Базы и данные", "panel_h": "Все функции — ответьте номером", "menu0": "это меню в любой момент", "tried": "пробовал", "untried": "ещё нет", "locked": "не в вашем тарифе", "plan": "ПЛАН НА СЕГОДНЯ", "week": "ОБЗОР НЕДЕЛИ", "setup": "НАСТРОЙКА ГОТОВА", "time": "Время сегодня", "goal": "Цель",
           "tasks": "Задачи", "why": "Почему такой порядок", "next": "Что дальше — скажите", "copy": "Копировать",
           "copied": "Скопировано", "done": "сделано", "by": "кто", "moves": "двигает", "of": "из",
           "foot": "PARASITER by Rumer · план хранится в вашей папке"},
    "uk": {"panel": "ПУЛЬТ PARASITER", "bases": "Бази й дані", "panel_h": "Усі функції — відповідайте номером", "menu0": "це меню будь-коли", "tried": "пробував", "untried": "ще ні", "locked": "не у вашому тарифі", "plan": "ПЛАН НА СЬОГОДНІ", "week": "ОГЛЯД ТИЖНЯ", "setup": "НАЛАШТУВАННЯ ГОТОВЕ", "time": "Час сьогодні", "goal": "Ціль",
           "tasks": "Завдання", "why": "Чому такий порядок", "next": "Що далі — скажіть", "copy": "Копіювати",
           "copied": "Скопійовано", "done": "зроблено", "by": "хто", "moves": "рухає", "of": "з",
           "foot": "PARASITER by Rumer · план зберігається у вашій папці"},
}
STATES = {"good": "var(--ok)", "ok": "var(--a)", "behind": "var(--g)", "bad": "var(--bad)"}

CSS = """:root{--bg:#07090D;--s:#0E131B;--s2:#151B24;--l:#232B37;--fg:#E8EDF4;--m:#8E9AAB;--a:#3D74FF;--k:#2FD3E0;--g:#E8B23A;--ok:#3DDC97;--bad:#FF5468;color-scheme:dark}
@media (prefers-color-scheme: light){:root{--bg:#F3F5F9;--s:#FFFFFF;--s2:#EEF1F6;--l:#D6DCE5;--fg:#0B1220;--m:#5A6678;--a:#1F57E6;--k:#0A8FA0;--g:#A86F00;--ok:#1C8A55;--bad:#D22F45;color-scheme:light}}
*{box-sizing:border-box}html,body{overflow-x:hidden}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 Geist,"Segoe UI",system-ui,-apple-system,sans-serif}
.wrap{max-width:880px;margin:0 auto;padding:28px 16px 48px}
.mono{font-family:"Geist Mono",ui-monospace,Consolas,monospace}
header{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;flex-wrap:wrap;padding-bottom:18px;border-bottom:1px solid var(--l)}
.eb{font-size:12px;letter-spacing:.14em;color:var(--k)}
h1{font-size:clamp(26px,5vw,36px);line-height:1.1;margin:6px 0 0;letter-spacing:-.02em}
.meta{text-align:right;color:var(--m);font-size:14px}.meta b{color:var(--fg);font-size:18px}
.goal{margin:18px 0 0;padding:14px 16px;background:var(--s);border:1px solid var(--l);border-radius:12px;display:flex;gap:12px;flex-wrap:wrap;align-items:center}
.goal .l{color:var(--m);font-size:13px}.goal .v{font-weight:600}
.pill{display:inline-block;font-size:12px;font-weight:600;padding:3px 10px;border-radius:999px;border:1px solid currentColor;margin-left:auto}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:14px 0 0}
.kpi{background:var(--s);border:1px solid var(--l);border-radius:12px;padding:12px 14px}
.kpi .l{font-size:12px;color:var(--m)}.kpi .v{font-size:26px;font-weight:650;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.bar{height:5px;background:var(--s2);border-radius:5px;margin-top:6px;overflow:hidden}.bar i{display:block;height:100%;border-radius:5px}
h2{font-size:13px;letter-spacing:.12em;color:var(--m);margin:28px 0 10px;font-weight:500}
.task{display:grid;grid-template-columns:auto 1fr;gap:14px;background:var(--s);border:1px solid var(--l);border-radius:14px;padding:16px;margin-bottom:10px;transition:opacity .2s}
.task.done{opacity:.5}.task.done .tt{text-decoration:line-through}
.num{width:32px;height:32px;border-radius:9px;background:color-mix(in srgb,var(--a) 16%,transparent);color:var(--a);display:grid;place-items:center;font-weight:700}
.tt{font-weight:600;font-size:17px;line-height:1.35}
.tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.tag{font-size:12px;padding:2px 8px;border-radius:6px;background:var(--s2);border:1px solid var(--l);color:var(--m)}
.tag.mv{color:var(--ok);border-color:color-mix(in srgb,var(--ok) 40%,transparent)}.tag.tm{color:var(--fg)}
.note{color:var(--m);font-size:14px;margin-top:6px}
.say{display:flex;gap:8px;align-items:center;margin-top:10px;flex-wrap:wrap}
.say code{font-family:"Geist Mono",ui-monospace,Consolas,monospace;font-size:13px;background:var(--s2);border:1px solid var(--l);border-radius:8px;padding:6px 10px;word-break:break-word}
button{font:inherit;font-size:12px;border:1px solid var(--l);background:transparent;color:var(--a);border-radius:8px;padding:5px 10px;cursor:pointer}
label.chk{display:flex;gap:6px;align-items:center;font-size:13px;color:var(--m);margin-top:10px;cursor:pointer;width:max-content}
.callout{border-radius:12px;padding:12px 14px;margin:10px 0 0;border:1px solid;background:color-mix(in srgb,currentColor 8%,transparent)}
.callout span{color:var(--fg)}
.why{background:var(--s);border-left:3px solid var(--k);border-radius:0 12px 12px 0;padding:12px 16px;color:var(--fg)}
.next{display:grid;gap:8px}.next .row{display:flex;gap:10px;align-items:center;flex-wrap:wrap;background:var(--s);border:1px solid var(--l);border-radius:12px;padding:10px 12px}
.next .row .w{color:var(--m);font-size:14px}
.explored{margin:14px 0 0;font-size:14px;color:var(--k)}
.psec{margin:14px 0 6px;font-size:12px;letter-spacing:.12em;color:var(--m)}
.tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:8px}
.tile{background:var(--s);border:1px solid var(--l);border-radius:12px;padding:10px 12px;display:grid;grid-template-columns:auto 1fr;gap:4px 10px;align-items:start}
.tile .n{font-weight:700;color:var(--a);font-size:18px;min-width:26px}
.tile .sk{font-weight:600;font-size:14px;word-break:break-word}.tile .w{grid-column:2;color:var(--m);font-size:13px;line-height:1.35}
.tile .st{grid-column:2;display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin-top:4px;font-size:11px}
.tile .st .ok{color:var(--ok)}.tile .st .no{color:var(--m)}.tile .st .pl{border:1px solid var(--l);border-radius:5px;padding:0 5px;color:var(--m)}
.tile.lock{opacity:.55}.tile.tried{border-color:color-mix(in srgb,var(--ok) 35%,var(--l))}
.tile button{grid-column:2;justify-self:start;margin-top:4px;padding:3px 8px}
footer{margin-top:32px;color:var(--m);font-size:12px;border-top:1px solid var(--l);padding-top:12px}
@media (max-width:560px){.meta{text-align:left}}
@media print{.say button,label.chk{display:none}}"""

JS = """document.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',()=>{const t=b.getAttribute('data-copy');
const ok=()=>{const o=b.textContent;b.textContent=b.dataset.ok;setTimeout(()=>b.textContent=o,1200)};
try{navigator.clipboard.writeText(t).then(ok,ok)}catch(e){ok()}}));
const KEY='parasiter-plan-'+document.body.dataset.key;let st={};try{st=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
document.querySelectorAll('.task input[type=checkbox]').forEach(c=>{const card=c.closest('.task');c.checked=!!st[c.dataset.i];card.classList.toggle('done',c.checked);
c.addEventListener('change',()=>{st[c.dataset.i]=c.checked;card.classList.toggle('done',c.checked);try{localStorage.setItem(KEY,JSON.stringify(st))}catch(e){}})});"""


def _ratio(v: str):
    try:
        a, b = str(v).split("/")[:2]
        a, b = float(a.strip().split()[0]), float(b.strip().split()[0])
        return max(0.0, min(1.0, a / b)) if b else None
    except (ValueError, IndexError):
        return None


def build(p: dict) -> str:
    e = lambda s: html.escape(str(s or ""))  # noqa: E731
    lab = L.get(p.get("lang", "en"), L["en"])
    kind = p.get("kind", "plan")
    day = p.get("date") or date.today().isoformat()
    parts = [f'<header><div><div class="eb mono">{e(lab.get(kind, lab["plan"]))} · {e(day)}</div><h1>{e(p.get("title"))}</h1></div>']
    if p.get("hours"):
        parts.append(f'<div class="meta">{e(lab["time"])}<br><b>{e(p["hours"])}</b></div>')
    parts.append("</header>")
    if p.get("goal") or p.get("status"):
        col = STATES.get(p.get("status_state", "ok"), "var(--a)")
        parts.append(f'<div class="goal"><span class="l">{e(lab["goal"])}</span><span class="v">{e(p.get("goal"))}</span>'
                     + (f'<span class="pill" style="color:{col}">{e(p["status"])}</span>' if p.get("status") else "") + "</div>")
    if p.get("kpis"):
        cells = []
        for k in p["kpis"]:
            col = STATES.get(k.get("state", "ok"), "var(--a)")
            r = _ratio(k.get("value", ""))
            bar = f'<div class="bar"><i style="width:{round((r or 0) * 100)}%;background:{col}"></i></div>' if r is not None else ""
            cells.append(f'<div class="kpi"><div class="l">{e(k.get("label"))}</div><div class="v" style="color:{col}">{e(k.get("value"))}</div>{bar}</div>')
        parts.append(f'<div class="kpis">{"".join(cells)}</div>')
    for c in p.get("callouts", []):
        col = STATES.get(c.get("state", "ok"), "var(--a)")
        parts.append(f'<div class="callout" style="color:{col}"><span>{e(c.get("text"))}</span></div>')
    if p.get("tasks"):
        parts.append(f'<h2 class="mono">{e(lab["tasks"]).upper()} · {len(p["tasks"])}</h2>')
        for i, t in enumerate(p["tasks"], 1):
            tags = []
            if t.get("time"):
                tags.append(f'<span class="tag tm">⏱ {e(t["time"])}</span>')
            if t.get("by"):
                tags.append(f'<span class="tag">{e(lab["by"])}: {e(t["by"])}</span>')
            if t.get("moves"):
                tags.append(f'<span class="tag mv">↑ {e(lab["moves"])}: {e(t["moves"])}</span>')
            say = (f'<div class="say"><code>{e(t["say"])}</code><button data-copy="{e(t["say"])}" data-ok="{e(lab["copied"])}">{e(lab["copy"])}</button></div>'
                   if t.get("say") else "")
            note = f'<div class="note">{e(t["note"])}</div>' if t.get("note") else ""
            parts.append(f'<div class="task"><div class="num mono">{i}</div><div><div class="tt">{e(t.get("title"))}</div>'
                         f'<div class="tags">{"".join(tags)}</div>{note}{say}'
                         f'<label class="chk"><input type="checkbox" data-i="{i}"> {e(lab["done"])}</label></div></div>')
    if p.get("why"):
        parts.append(f'<h2 class="mono">{e(lab["why"]).upper()}</h2><div class="why">{e(p["why"])}</div>')
    if p.get("next"):
        rows = "".join(f'<div class="row"><code class="mono">{e(n.get("say"))}</code><button data-copy="{e(n.get("say"))}" data-ok="{e(lab["copied"])}">'
                       f'{e(lab["copy"])}</button><span class="w">{e(n.get("what"))}</span></div>' for n in p["next"])
        parts.append(f'<h2 class="mono">{e(lab["next"]).upper()}</h2><div class="next">{rows}</div>')
    if p.get("bases"):
        tiles = "".join(f'<div class="tile"><div class="n mono">{e(b.get("code"))}</div><div class="sk">{e(b.get("name"))}</div>'
                        f'<div class="w">{e(b.get("what"))}</div><div class="st">' + (f'<span class="pl">{e(b.get("plan"))}</span>' if b.get("plan") else "") +
                        f'</div><button data-copy="{e(b.get("code"))}" data-ok="{e(lab["copied"])}">{e(lab["copy"])} {e(b.get("code"))}</button></div>'
                        for b in p["bases"])
        parts.append(f'<div class="psec mono">{e(lab["bases"]).upper()}</div><div class="tiles">{tiles}</div>')
    if p.get("panel"):
        if kind != "panel":
            parts.append(f'<h2 class="mono">{e(lab["panel"])}</h2>')
        parts.append(f'<div class="why" style="border-left-color:var(--a)">{e(lab["panel_h"])} · <b class="mono">0</b> — {e(lab["menu0"])}</div>')
        if p.get("explored"):
            parts.append(f'<div class="explored mono">{e(p["explored"])}</div>')
        for sec in p["panel"]:
            tiles = []
            for it in sec.get("items", []):
                tried = it.get("tried")
                st = (f'<span class="ok">✓ {e(lab["tried"])} {e(tried)}</span>' if tried else f'<span class="no">○ {e(lab["untried"])}</span>')
                pl = f'<span class="pl">{e(it.get("plan"))}</span>' if it.get("plan") else ""
                lk = f'<span class="no">{e(lab["locked"])}</span>' if it.get("locked") else ""
                cls = "tile" + (" tried" if tried else "") + (" lock" if it.get("locked") else "")
                tiles.append(f'<div class="{cls}"><div class="n mono">{e(it.get("n"))}</div><div class="sk mono">{e(it.get("skill"))}</div>'
                             f'<div class="w">{e(it.get("what"))}</div><div class="st">{st}{pl}{lk}</div>'
                             f'<button data-copy="{e(it.get("n"))}" data-ok="{e(lab["copied"])}">{e(lab["copy"])} {e(it.get("n"))}</button></div>')
            parts.append(f'<div class="psec mono">{e(sec.get("name", "")).upper()}</div><div class="tiles">{"".join(tiles)}</div>')
    parts.append(f'<footer class="mono">{e(lab["foot"])}</footer>')
    key = e(f"{kind}-{day}")
    return (f'<!doctype html><html lang="{e(p.get("lang", "en"))}"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(p.get("title"))} · {e(day)}</title>'
            f'<style>{CSS}</style></head><body data-key="{key}"><div class="wrap">{"".join(parts)}</div><script>{JS}</script></body></html>')


def p_kind(src):
    try:
        with open(src, encoding="utf-8") as f:
            return json.load(f).get("kind", "plan")
    except (OSError, ValueError):
        return "plan"


def main(argv):
    if "--self-test" in argv:
        sample = {"lang": "ru", "title": "План на сегодня", "hours": "4 ч", "goal": "$50/день к 1 мая 2027",
                  "status": "Неделя 1 · отстаём на 1 день", "status_state": "behind",
                  "kpis": [{"label": "Посты недели", "value": "0/3", "state": "behind"}, {"label": "Площадки", "value": "0/2", "state": "behind"}],
                  "tasks": [{"title": "Опубликовать статью", "time": "~45 мин", "by": "вы + журнал", "moves": "пост 1/3", "say": "Я опубликовал: <ссылка>"}],
                  "callouts": [{"text": "Не опубликовано: 2 статьи", "state": "ok"}], "why": "Одна живая страница важнее трёх черновиков.",
                  "next": [{"say": "План на сегодня", "what": "обновить план"}]}
        sample["explored"] = "Освоено: 1 из 21 скилов"
        sample["panel"] = [{"name": "План", "items": [{"n": 1, "skill": "navigator", "what": "план", "plan": "Pro", "tried": "03.11"},
                                                      {"n": 3, "skill": "affiliate-finder", "what": "офферы", "plan": "Insider", "locked": True}]}]
        out = build(sample)
        assert "ПУЛЬТ PARASITER" in out and "✓ пробовал 03.11" in out and "не в вашем тарифе" in out
        panel_only = build({"lang": "en", "kind": "panel", "title": "PARASITER panel", "panel": sample["panel"],
                            "bases": [{"code": "B1", "name": "Rumer's platform base", "what": "checked platforms", "plan": "Pro"}]})
        assert "BASES AND DATA" in panel_only and "Copy B1" in panel_only
        assert "PARASITER PANEL" in panel_only and "Copy 1" in panel_only
        assert "Опубликовать статью" in out and "0/3" in out and "<script>" in out and "Копировать" in out
        assert "&lt;ссылка&gt;" in out                       # user text is escaped
        print("self-test ok")
        return 0
    if not argv:
        print(__doc__)
        return 2
    src = argv[0]
    default = "parasiter-panel.html" if p_kind(src) == "panel" else "plan-today.html"
    out = argv[argv.index("--out") + 1] if "--out" in argv else default
    with open(src, encoding="utf-8") as f:
        p = json.load(f)
    page = build(p)
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    if "--out" not in argv and p.get("kind", "plan") == "plan":   # keep a dated copy of each day's plan
        os.makedirs("plans", exist_ok=True)
        day = p.get("date") or date.today().isoformat()
        with open(os.path.join("plans", f"{day}.html"), "w", encoding="utf-8") as f:
            f.write(page)
    print(os.path.abspath(out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
