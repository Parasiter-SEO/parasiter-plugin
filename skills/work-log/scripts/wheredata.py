"""PARASITER — "Where is my data?": shows the user the exact folder and files that hold their base,
so they can open them and see for themselves that nothing lives on the PARASITER server.

Usage:
  python3 wheredata.py [FOLDER] [--lang en|ru|uk] [--json]

FOLDER defaults to the current folder (the user's project folder). For agencies pass clients/<slug>.
Read-only: lists files, sizes, rows and last change. Never opens the network, never writes.
Standard library only.
"""
import argparse
import json
import os
import sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from export import collect_files  # noqa: E402  (same list of PARASITER files as "export my base")

T = {
    "en": {
        "title": "Your PARASITER data — where it lives",
        "folder": "Folder on this computer",
        "none": "No PARASITER files here yet. Your base is created in this folder as soon as you log your first page, sale or goal.",
        "cols": ("File", "What it is", "Size", "Rows", "Last change"),
        "total": "Files",
        "never_h": "Never sent to the PARASITER server",
        "never": "page URLs, journal, sales, affiliate links, platforms, texts, profile, goals — everything in the files above.",
        "server_h": "What the server knows about you",
        "server": "email, plan and payment dates, a hash of your key, your Telegram ID if linked, notification settings, "
                  "scheduled paid checks described in words (never URLs), and after a page check only counts "
                  "(\"40 checked, 2 removed\") plus the bare platform domain where pages were lost (kept 7 days, without your name).",
        "check_h": "Check it yourself",
        "check": ["Open this folder: the files are plain CSV and Markdown, readable in Excel or any text editor.",
                  "The plugin code is public: https://github.com/Parasiter-SEO/parasiter-plugin",
                  "Privacy policy: https://parasiter.affiliatecredo.com/privacy-en.html · plain-language page: https://parasiter.affiliatecredo.com/data.html"],
        "note": "Your AI assistant (Claude) processes what you work on with it under Anthropic's privacy policy; Rumer as the author has no access to it.",
    },
    "ru": {
        "title": "Ваши данные PARASITER — где они лежат",
        "folder": "Папка на этом компьютере",
        "none": "Файлов PARASITER здесь пока нет. База появится в этой папке, как только вы внесёте первую страницу, продажу или цель.",
        "cols": ("Файл", "Что это", "Размер", "Строк", "Изменён"),
        "total": "Всего файлов",
        "never_h": "Никогда не отправляется на сервер PARASITER",
        "never": "URL страниц, журнал, продажи, партнёрские ссылки, площадки, тексты, профиль, цели — всё, что в файлах выше.",
        "server_h": "Что сервер знает о вас",
        "server": "email, тариф и даты оплат, хеш ключа, Telegram ID (если привязан), настройки уведомлений, "
                  "платные проверки по расписанию, описанные словами (никогда не URL), а после проверки страниц — только числа "
                  "(«проверено 40, удалено 2») и голый домен площадки, где пропали страницы (7 дней, без вашего имени).",
        "check_h": "Проверьте сами",
        "check": ["Откройте эту папку: файлы — обычные CSV и Markdown, открываются в Excel или любом редакторе.",
                  "Код плагина открыт: https://github.com/Parasiter-SEO/parasiter-plugin",
                  "Политика конфиденциальности: https://parasiter.affiliatecredo.com/privacy-en.html · простыми словами: https://parasiter.affiliatecredo.com/data.html"],
        "note": "Ваш ИИ-ассистент (Claude) обрабатывает то, с чем вы в нём работаете, по политике Anthropic; у Rumer как автора доступа к этому нет.",
    },
    "uk": {
        "title": "Ваші дані PARASITER — де вони лежать",
        "folder": "Папка на цьому комп'ютері",
        "none": "Файлів PARASITER тут поки немає. База з'явиться в цій папці, щойно ви внесете першу сторінку, продаж або ціль.",
        "cols": ("Файл", "Що це", "Розмір", "Рядків", "Змінено"),
        "total": "Усього файлів",
        "never_h": "Ніколи не надсилається на сервер PARASITER",
        "never": "URL сторінок, журнал, продажі, партнерські посилання, платформи, тексти, профіль, цілі — усе, що у файлах вище.",
        "server_h": "Що сервер знає про вас",
        "server": "email, тариф і дати оплат, хеш ключа, Telegram ID (якщо прив'язаний), налаштування сповіщень, "
                  "платні перевірки за розкладом, описані словами (ніколи не URL), а після перевірки сторінок — лише числа "
                  "(«перевірено 40, видалено 2») і голий домен платформи, де зникли сторінки (7 днів, без вашого імені).",
        "check_h": "Перевірте самі",
        "check": ["Відкрийте цю папку: файли — звичайні CSV і Markdown, відкриваються в Excel або будь-якому редакторі.",
                  "Код плагіна відкритий: https://github.com/Parasiter-SEO/parasiter-plugin",
                  "Політика конфіденційності: https://parasiter.affiliatecredo.com/privacy.html · простими словами: https://parasiter.affiliatecredo.com/data-uk.html"],
        "note": "Ваш ШІ-асистент (Claude) обробляє те, з чим ви в ньому працюєте, за політикою Anthropic; у Rumer як автора доступу до цього немає.",
    },
}


def human(n):
    for unit in ("B", "KB", "MB"):
        if n < 1024 or unit == "MB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024


def rows(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            n = sum(1 for line in f if line.strip())
    except OSError:
        return None
    return max(n - 1, 0) if path.endswith(".csv") else n


def scan(folder):
    out = []
    for name, desc in collect_files(folder):
        p = os.path.join(folder, name)
        st = os.stat(p)
        out.append({"file": name, "what": desc, "bytes": st.st_size, "rows": rows(p),
                    "changed": datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M")})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", nargs="?", default=".")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    folder = os.path.abspath(a.folder)
    if not os.path.isdir(folder):
        sys.exit(f"Not a folder: {folder}")
    files = scan(folder)
    if a.json:
        print(json.dumps({"folder": folder, "files": files}, ensure_ascii=False, indent=2))
        return
    t = T.get(a.lang, T["en"])
    print(f"# {t['title']}\n")
    print(f"**{t['folder']}:** `{folder}`\n")
    if not files:
        print(t["none"] + "\n")
    else:
        c = t["cols"]
        print(f"| {' | '.join(c)} |")
        print("|" + "---|" * len(c))
        for f in files:
            r = "—" if f["rows"] is None else str(f["rows"])
            print(f"| `{f['file']}` | {f['what']} | {human(f['bytes'])} | {r} | {f['changed']} |")
        print(f"\n{t['total']}: {len(files)}, {human(sum(f['bytes'] for f in files))}\n")
    print(f"**{t['never_h']}:** {t['never']}\n")
    print(f"**{t['server_h']}:** {t['server']}\n")
    print(f"**{t['check_h']}:**")
    for line in t["check"]:
        print(f"- {line}")
    print(f"\n_{t['note']}_")


if __name__ == "__main__":
    main()
