#!/usr/bin/env python3
"""PARASITER — "My base": the user's posts, platforms, sales and links as an Excel workbook and a dashboard page.

Usage:
  python3 mybase.py JOURNAL [--xlsx] [--html] [--out parasite-seo-base] [--lang ru]
                    [--platform P] [--priority high] [--topic T] [--today YYYY-MM-DD]

Without --xlsx / --html both are written:
  <out>.xlsx  sheets: Summary · Posts (one row per page, its state today) · Platforms · Sales · Links ·
              Journal (every event as logged). Header row frozen, filters on, links clickable,
              dates and numbers as real Excel values. Opens in Excel, Google Sheets, Numbers, LibreOffice.
  <out>.html  self-contained dashboard (no external files): totals, status of the base by platform,
              searchable and sortable tables with filters, "Download Excel" and "CSV of what you see".
              The workbook is embedded in the page, so the page is one file: published as a Claude
              artifact with capabilities {"downloads": true}, both buttons work there; opened as a
              local file, they work in the browser. --html alone gives the page with CSV only.

--platform / --priority / --topic narrow the Posts sheet and the page table (the other sheets stay full).
--lang: en, ru, uk, es, pt (labels and statuses; the data itself is never translated).
Reads the same files as worklog.py, never writes to them. Standard library only.
"""
import argparse
import html
import json
import os
import re
import sys
import zipfile
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from xml.sax.saxutils import escape as xesc

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import worklog as wl  # noqa: E402

# ---------- labels ----------

L = {
    "en": {
        "title": "My post base", "sheet_summary": "Summary", "sheet_posts": "Posts", "sheet_platforms": "Platforms",
        "sheet_sales": "Sales", "sheet_links": "Links", "sheet_journal": "Journal",
        "published": "Published", "page": "Page", "platform": "Platform", "topic": "Topic", "prio": "★",
        "offer": "Offer", "program": "Program", "campaign": "Campaign", "sub_id": "Sub-ID", "query": "Main query",
        "type": "Content type", "status": "Status", "position": "Position", "best_pos": "Best position",
        "pos_date": "Position checked", "last_check": "Last check", "audit": "Audit", "views": "Views",
        "aff_clicks": "Aff. clicks", "sales": "Sales", "commission": "Commission", "currency": "Currency",
        "source": "Source saved", "link_target": "Link to", "link_rel": "Link rel", "age": "Age, days",
        "domain": "Domain", "ptype": "Type", "state": "State", "pages": "Pages", "alive": "Alive",
        "indexed": "Indexed", "top10": "Top 10", "gone": "Gone", "unchecked": "Not checked", "last_page": "Last page",
        "score": "Score", "language": "Language", "links": "Links", "account": "Account", "note": "Note",
        "date": "Date", "order_id": "Order ID", "amount": "Sale amount", "sale_status": "Status",
        "sale_source": "Source", "product": "Product", "link": "Link", "alt_links": "Other links",
        "added": "Added",
        "k_posts": "Posts", "k_platforms": "Platforms", "k_alive": "Alive", "k_indexed": "Indexed",
        "k_top10": "In the top 10", "k_attention": "Need attention", "k_sales": "Sales",
        "k_commission": "Commission", "k_star": "★ priority",
        "k_attention_note": "removed, noindex or not checked yet",
        "built": "Built", "from_files": "From your journal files", "filtered": "Filtered",
        "by_platform": "Status by platform", "search": "Search page, topic, offer, query…", "all": "All",
        "only_star": "★ only", "only_top": "Top 10 only", "reset": "Reset", "shown": "{n} of {m} shown",
        "more": "Show {n} more", "dl_xlsx": "Download Excel", "dl_csv": "CSV of this view",
        "empty": "Nothing matches these filters.", "no_data": "No pages in the journal yet. Import your pages or log the first one.",
        "total": "Total", "est_note": "Sales tied to a page by URL or sub-ID. Sales known only by program are in the Sales tab.",
        "yes": "yes", "unknown_date": "date unknown", "foot": "Numbers come only from your journal, sales and traffic files. Nothing is estimated here.",
        "saved": "Saved", "declined": "Download cancelled",
        "s": {"live": "live", "indexed": "indexed", "not-indexed": "not indexed", "noindex": "noindex",
              "dropped": "dropped", "removed": "removed", "dead": "dead", "moved": "moved",
              "not checked yet": "not checked", "approved": "approved", "pending": "pending",
              "reversed": "reversed", "active": "active", "testing": "testing", "paused": "paused",
              "high": "★", "normal": "", "low": "low"},
    },
    "ru": {
        "title": "Моя база постов", "sheet_summary": "Сводка", "sheet_posts": "Посты", "sheet_platforms": "Площадки",
        "sheet_sales": "Продажи", "sheet_links": "Ссылки", "sheet_journal": "Журнал",
        "published": "Опубликован", "page": "Страница", "platform": "Площадка", "topic": "Тема", "prio": "★",
        "offer": "Оффер", "program": "Программа", "campaign": "Пачка", "sub_id": "Sub-ID", "query": "Главный запрос",
        "type": "Тип контента", "status": "Статус", "position": "Позиция", "best_pos": "Лучшая позиция",
        "pos_date": "Позиция на дату", "last_check": "Последняя проверка", "audit": "Аудит", "views": "Просмотры",
        "aff_clicks": "Клики по ссылке", "sales": "Продажи", "commission": "Комиссия", "currency": "Валюта",
        "source": "Исходник сохранён", "link_target": "Ссылка на", "link_rel": "Тип ссылки", "age": "Возраст, дней",
        "domain": "Домен", "ptype": "Тип", "state": "Состояние", "pages": "Страниц", "alive": "Живые",
        "indexed": "В индексе", "top10": "Топ-10", "gone": "Удалены", "unchecked": "Не проверены", "last_page": "Последний пост",
        "score": "Оценка", "language": "Язык", "links": "Ссылки", "account": "Аккаунт", "note": "Заметка",
        "date": "Дата", "order_id": "Номер заказа", "amount": "Сумма продажи", "sale_status": "Статус",
        "sale_source": "Источник", "product": "Продукт", "link": "Ссылка", "alt_links": "Другие ссылки",
        "added": "Добавлена",
        "k_posts": "Постов", "k_platforms": "Площадок", "k_alive": "Живые", "k_indexed": "В индексе",
        "k_top10": "В топ-10", "k_attention": "Требуют внимания", "k_sales": "Продаж",
        "k_commission": "Комиссия", "k_star": "★ приоритетных",
        "k_attention_note": "удалены, noindex или ещё не проверены",
        "built": "Собрано", "from_files": "Из файлов вашего журнала", "filtered": "Фильтр",
        "by_platform": "Статус постов по площадкам", "search": "Поиск: страница, тема, оффер, запрос…", "all": "Все",
        "only_star": "Только ★", "only_top": "Только топ-10", "reset": "Сбросить", "shown": "Показано {n} из {m}",
        "more": "Показать ещё {n}", "dl_xlsx": "Скачать Excel", "dl_csv": "CSV по фильтру",
        "empty": "По этим фильтрам ничего нет.", "no_data": "В журнале пока нет страниц. Загрузите свои посты или добавьте первый.",
        "total": "Итого", "est_note": "Продажи привязаны к странице по URL или sub-ID. Продажи, известные только по программе, во вкладке «Продажи».",
        "yes": "да", "unknown_date": "дата неизвестна", "foot": "Цифры только из ваших файлов журнала, продаж и трафика. Здесь ничего не оценивается.",
        "saved": "Сохранено", "declined": "Загрузка отменена",
        "s": {"live": "живой", "indexed": "в индексе", "not-indexed": "не в индексе", "noindex": "noindex",
              "dropped": "просел", "removed": "удалён", "dead": "площадка мертва", "moved": "перенесён",
              "not checked yet": "не проверен", "approved": "одобрена", "pending": "в ожидании",
              "reversed": "отменена", "active": "активна", "testing": "тест", "paused": "на паузе",
              "high": "★", "normal": "", "low": "низкий"},
    },
    "uk": {
        "title": "Моя база постів", "sheet_summary": "Зведення", "sheet_posts": "Пости", "sheet_platforms": "Майданчики",
        "sheet_sales": "Продажі", "sheet_links": "Посилання", "sheet_journal": "Журнал",
        "published": "Опубліковано", "page": "Сторінка", "platform": "Майданчик", "topic": "Тема", "prio": "★",
        "offer": "Офер", "program": "Програма", "campaign": "Пачка", "sub_id": "Sub-ID", "query": "Головний запит",
        "type": "Тип контенту", "status": "Статус", "position": "Позиція", "best_pos": "Найкраща позиція",
        "pos_date": "Позиція на дату", "last_check": "Остання перевірка", "audit": "Аудит", "views": "Перегляди",
        "aff_clicks": "Кліки по посиланню", "sales": "Продажі", "commission": "Комісія", "currency": "Валюта",
        "source": "Вихідник збережено", "link_target": "Посилання на", "link_rel": "Тип посилання", "age": "Вік, днів",
        "domain": "Домен", "ptype": "Тип", "state": "Стан", "pages": "Сторінок", "alive": "Живі",
        "indexed": "В індексі", "top10": "Топ-10", "gone": "Видалені", "unchecked": "Не перевірені", "last_page": "Останній пост",
        "score": "Оцінка", "language": "Мова", "links": "Посилання", "account": "Акаунт", "note": "Нотатка",
        "date": "Дата", "order_id": "Номер замовлення", "amount": "Сума продажу", "sale_status": "Статус",
        "sale_source": "Джерело", "product": "Продукт", "link": "Посилання", "alt_links": "Інші посилання",
        "added": "Додано",
        "k_posts": "Постів", "k_platforms": "Майданчиків", "k_alive": "Живі", "k_indexed": "В індексі",
        "k_top10": "У топ-10", "k_attention": "Потребують уваги", "k_sales": "Продажів",
        "k_commission": "Комісія", "k_star": "★ пріоритетних",
        "k_attention_note": "видалені, noindex або ще не перевірені",
        "built": "Зібрано", "from_files": "З файлів вашого журналу", "filtered": "Фільтр",
        "by_platform": "Статус постів по майданчиках", "search": "Пошук: сторінка, тема, офер, запит…", "all": "Усі",
        "only_star": "Лише ★", "only_top": "Лише топ-10", "reset": "Скинути", "shown": "Показано {n} з {m}",
        "more": "Показати ще {n}", "dl_xlsx": "Завантажити Excel", "dl_csv": "CSV за фільтром",
        "empty": "За цими фільтрами нічого немає.", "no_data": "У журналі поки немає сторінок. Завантажте свої пости або додайте перший.",
        "total": "Разом", "est_note": "Продажі прив'язані до сторінки за URL або sub-ID. Продажі, відомі лише за програмою, у вкладці «Продажі».",
        "yes": "так", "unknown_date": "дата невідома", "foot": "Цифри лише з ваших файлів журналу, продажів і трафіку. Тут нічого не оцінюється.",
        "saved": "Збережено", "declined": "Завантаження скасовано",
        "s": {"live": "живий", "indexed": "в індексі", "not-indexed": "не в індексі", "noindex": "noindex",
              "dropped": "просів", "removed": "видалений", "dead": "майданчик мертвий", "moved": "перенесений",
              "not checked yet": "не перевірений", "approved": "схвалена", "pending": "очікує",
              "reversed": "скасована", "active": "активний", "testing": "тест", "paused": "на паузі",
              "high": "★", "normal": "", "low": "низький"},
    },
    "es": {
        "title": "Mi base de publicaciones", "sheet_summary": "Resumen", "sheet_posts": "Publicaciones", "sheet_platforms": "Plataformas",
        "sheet_sales": "Ventas", "sheet_links": "Enlaces", "sheet_journal": "Diario",
        "published": "Publicada", "page": "Página", "platform": "Plataforma", "topic": "Tema", "prio": "★",
        "offer": "Oferta", "program": "Programa", "campaign": "Paquete", "sub_id": "Sub-ID", "query": "Consulta principal",
        "type": "Tipo de contenido", "status": "Estado", "position": "Posición", "best_pos": "Mejor posición",
        "pos_date": "Posición del", "last_check": "Última revisión", "audit": "Auditoría", "views": "Vistas",
        "aff_clicks": "Clics de afiliado", "sales": "Ventas", "commission": "Comisión", "currency": "Moneda",
        "source": "Fuente guardada", "link_target": "Enlace a", "link_rel": "Tipo de enlace", "age": "Edad, días",
        "domain": "Dominio", "ptype": "Tipo", "state": "Estado", "pages": "Páginas", "alive": "Vivas",
        "indexed": "Indexadas", "top10": "Top 10", "gone": "Eliminadas", "unchecked": "Sin revisar", "last_page": "Última página",
        "score": "Puntuación", "language": "Idioma", "links": "Enlaces", "account": "Cuenta", "note": "Nota",
        "date": "Fecha", "order_id": "ID de pedido", "amount": "Importe de venta", "sale_status": "Estado",
        "sale_source": "Origen", "product": "Producto", "link": "Enlace", "alt_links": "Otros enlaces",
        "added": "Añadido",
        "k_posts": "Publicaciones", "k_platforms": "Plataformas", "k_alive": "Vivas", "k_indexed": "Indexadas",
        "k_top10": "En el top 10", "k_attention": "Requieren atención", "k_sales": "Ventas",
        "k_commission": "Comisión", "k_star": "★ prioritarias",
        "k_attention_note": "eliminadas, noindex o sin revisar",
        "built": "Generado", "from_files": "De tus archivos del diario", "filtered": "Filtro",
        "by_platform": "Estado por plataforma", "search": "Buscar página, tema, oferta, consulta…", "all": "Todas",
        "only_star": "Solo ★", "only_top": "Solo top 10", "reset": "Restablecer", "shown": "{n} de {m}",
        "more": "Mostrar {n} más", "dl_xlsx": "Descargar Excel", "dl_csv": "CSV de esta vista",
        "empty": "Nada coincide con estos filtros.", "no_data": "Aún no hay páginas en el diario. Importa tus páginas o registra la primera.",
        "total": "Total", "est_note": "Ventas atribuidas a una página por URL o sub-ID. Las ventas conocidas solo por programa están en Ventas.",
        "yes": "sí", "unknown_date": "fecha desconocida", "foot": "Los números provienen solo de tus archivos de diario, ventas y tráfico. Aquí no se estima nada.",
        "saved": "Guardado", "declined": "Descarga cancelada",
        "s": {"live": "viva", "indexed": "indexada", "not-indexed": "no indexada", "noindex": "noindex",
              "dropped": "bajó", "removed": "eliminada", "dead": "plataforma caída", "moved": "movida",
              "not checked yet": "sin revisar", "approved": "aprobada", "pending": "pendiente",
              "reversed": "revertida", "active": "activa", "testing": "prueba", "paused": "en pausa",
              "high": "★", "normal": "", "low": "baja"},
    },
    "pt": {
        "title": "Minha base de posts", "sheet_summary": "Resumo", "sheet_posts": "Posts", "sheet_platforms": "Plataformas",
        "sheet_sales": "Vendas", "sheet_links": "Links", "sheet_journal": "Diário",
        "published": "Publicado", "page": "Página", "platform": "Plataforma", "topic": "Tema", "prio": "★",
        "offer": "Oferta", "program": "Programa", "campaign": "Pacote", "sub_id": "Sub-ID", "query": "Consulta principal",
        "type": "Tipo de conteúdo", "status": "Status", "position": "Posição", "best_pos": "Melhor posição",
        "pos_date": "Posição em", "last_check": "Última verificação", "audit": "Auditoria", "views": "Visualizações",
        "aff_clicks": "Cliques de afiliado", "sales": "Vendas", "commission": "Comissão", "currency": "Moeda",
        "source": "Fonte salva", "link_target": "Link para", "link_rel": "Tipo de link", "age": "Idade, dias",
        "domain": "Domínio", "ptype": "Tipo", "state": "Estado", "pages": "Páginas", "alive": "Vivas",
        "indexed": "Indexadas", "top10": "Top 10", "gone": "Removidas", "unchecked": "Não verificadas", "last_page": "Última página",
        "score": "Nota", "language": "Idioma", "links": "Links", "account": "Conta", "note": "Nota",
        "date": "Data", "order_id": "ID do pedido", "amount": "Valor da venda", "sale_status": "Status",
        "sale_source": "Origem", "product": "Produto", "link": "Link", "alt_links": "Outros links",
        "added": "Adicionado",
        "k_posts": "Posts", "k_platforms": "Plataformas", "k_alive": "Vivos", "k_indexed": "Indexados",
        "k_top10": "No top 10", "k_attention": "Precisam de atenção", "k_sales": "Vendas",
        "k_commission": "Comissão", "k_star": "★ prioritários",
        "k_attention_note": "removidos, noindex ou não verificados",
        "built": "Gerado", "from_files": "Dos seus arquivos do diário", "filtered": "Filtro",
        "by_platform": "Status por plataforma", "search": "Buscar página, tema, oferta, consulta…", "all": "Todas",
        "only_star": "Só ★", "only_top": "Só top 10", "reset": "Limpar", "shown": "{n} de {m}",
        "more": "Mostrar mais {n}", "dl_xlsx": "Baixar Excel", "dl_csv": "CSV desta visão",
        "empty": "Nada corresponde a estes filtros.", "no_data": "Ainda não há páginas no diário. Importe suas páginas ou registre a primeira.",
        "total": "Total", "est_note": "Vendas ligadas a uma página por URL ou sub-ID. Vendas conhecidas só pelo programa estão em Vendas.",
        "yes": "sim", "unknown_date": "data desconhecida", "foot": "Os números vêm só dos seus arquivos de diário, vendas e tráfego. Nada aqui é estimado.",
        "saved": "Salvo", "declined": "Download cancelado",
        "s": {"live": "vivo", "indexed": "indexado", "not-indexed": "não indexado", "noindex": "noindex",
              "dropped": "caiu", "removed": "removido", "dead": "plataforma morta", "moved": "movido",
              "not checked yet": "não verificado", "approved": "aprovada", "pending": "pendente",
              "reversed": "revertida", "active": "ativa", "testing": "teste", "paused": "pausada",
              "high": "★", "normal": "", "low": "baixa"},
    },
}

GOOD, INFO, WARN, BAD, MUTED = "good", "info", "warn", "bad", "muted"
STATUS_TONE = {"indexed": GOOD, "live": INFO, "not-indexed": WARN, "dropped": WARN, "noindex": BAD,
               "removed": BAD, "dead": BAD, "moved": MUTED, "not checked yet": MUTED}


# ---------- collecting ----------

def collect(journal, today, sales_override=None, platform=None, priority=None, topic=None):
    rows = wl.read_rows(journal)
    pages = wl.page_states(rows, today)
    sales = wl.read_sales(wl.sales_path(journal, sales_override), pages)
    srcs = wl.page_sources(rows)
    cur_count = Counter((r.get("currency") or "USD").upper() for r in sales)
    cur = cur_count.most_common(1)[0][0] if cur_count else "USD"

    earned = defaultdict(lambda: [0, defaultdict(float)])
    for r in sales:
        if r["_page"] and wl.counted(r):
            earned[r["_page"]][0] += 1 if r["_c"] > 0 else -1 if r["_c"] < 0 else 0
            earned[r["_page"]][1][(r.get("currency") or "USD").upper()] += r["_c"]
    traffic = defaultdict(lambda: [0.0, 0.0])
    for r in rows:
        if r["event"] in ("traffic", "stats") and r.get("page_url"):
            traffic[r["page_url"]][0] += wl.num(r.get("views")) or 0
            traffic[r["page_url"]][1] += wl.num(r.get("aff_clicks")) or 0

    out_pages = []
    for p in pages.values():
        if platform and (p["platform"] or "").lower() != platform.lower():
            continue
        if priority and p["priority"] != priority:
            continue
        if topic and topic.lower() not in p["topic_key"]:
            continue
        n, by_cur = earned[p["url"]]
        com = by_cur.get(cur, 0.0)
        other = {k: round(v, 2) for k, v in by_cur.items() if k != cur and v}
        v, ac = traffic[p["url"]]
        out_pages.append({
            "url": p["url"], "published": None if p["date_unknown"] else p["published"].isoformat(),
            "platform": p["platform"], "topic": re.sub(r"^~ ", "", p["topic_key"]), "topic_guessed": p["topic_key"].startswith("~ "),
            "priority": p["priority"], "offer": p["offer"], "program": p["program"], "campaign": p["campaign"],
            "sub_id": p["sub_id"], "query": p["query"], "type": p["content_type"], "status": wl.health(p),
            "position": p["position"], "prev_pos": p.get("prev_pos"), "best_pos": p["best_pos"],
            "pos_date": p["pos_date"].isoformat() if p["pos_date"] else None,
            "last_check": p["last_check"].isoformat() if p["last_check"] else None,
            "score": p["score"], "views": v or None, "aff_clicks": ac or None, "sales": n or None,
            "commission": round(com, 2) if com else None, "other_cur": other,
            "age": None if p["date_unknown"] else p["age"], "source": srcs.get(p["url"], ""),
            "link_target": p.get("link_target", ""), "link_rel": p.get("link_rel", ""),
        })
    out_pages.sort(key=lambda x: x["published"] or "", reverse=True)
    out_pages.sort(key=lambda x: wl.PRIORITIES.index(x["priority"]))

    # platforms: registry + whatever pages show
    reg = wl.read_platforms(wl.platforms_path(journal))
    st = wl.platform_stats(rows, sales, pages, today)
    tops = Counter(p["platform"].lower() for p in pages.values()
                   if p["position"] is not None and p["position"] <= wl.TOP and not p["moved"]
                   and wl.health(p) not in wl.GONE)
    names = {k: r for k, r in reg.items()}
    for p in pages.values():
        if p["platform"] and p["platform"].lower() not in names:
            _, dom, typ = wl.platform_of(p["url"])
            names[p["platform"].lower()] = {"platform": p["platform"], "domain": dom, "type": typ}
    out_plat = []
    for k, r in names.items():
        s = st[k]
        out_plat.append({
            "platform": r.get("platform") or k, "domain": r.get("domain", ""), "type": r.get("type", ""),
            "state": r.get("state") or "active", "priority": r.get("priority") or "normal",
            "rank": wl.num(r.get("rank")), "pages": s["pages"], "alive": s["alive"], "indexed": s["indexed"],
            "top10": tops[k], "gone": s["gone"], "unchecked": s["unchecked"],
            "last_page": s["last"].isoformat() if s["last"] else None, "sales": s["sales"] or None,
            "commission": round(s["comm"], 2) if s["comm"] else None,
            "score": wl.num(r.get("score")) if r.get("score") else s["score"],
            "language": r.get("language", ""), "links": r.get("links", ""), "account": r.get("account", ""),
            "note": r.get("note", ""),
        })
    out_plat.sort(key=lambda x: (x["rank"] or 99, wl.PRIORITIES.index(x["priority"] if x["priority"] in wl.PRIORITIES else "normal"),
                                 -x["pages"], x["platform"].lower()))

    out_sales = []
    for r in sorted(sales, key=lambda r: (r["_d"], r["_i"]), reverse=True):
        out_sales.append({
            "date": r["_d"].isoformat(), "program": r.get("program", ""), "offer": r.get("offer", ""),
            "page": r["_page"], "sub_id": r.get("sub_id", ""), "order_id": r.get("order_id", ""),
            "amount": r["_a"], "commission": round(r["_c"], 2), "currency": (r.get("currency") or "USD").upper(),
            "status": r["status"], "source": "manual" if r.get("source") == "manual" else (r.get("source") or "").replace("import:", ""),
            "counted": wl.counted(r),
        })

    links = [{k: r.get(k, "") for k in wl.LINK_COLUMNS} for r in wl.read_csv(wl.links_path(journal))]

    journal_cols = list(wl.COLUMNS)
    raw = wl.read_csv(journal)
    for r in raw:
        journal_cols += [k for k in r if k not in journal_cols]

    alive = [p for p in out_pages if p["status"] in wl.ALIVE]
    tot = defaultdict(float)
    n_sales = 0
    for r in sales:
        if wl.counted(r):
            tot[(r.get("currency") or "USD").upper()] += r["_c"]
            n_sales += 1 if r["_c"] > 0 else -1 if r["_c"] < 0 else 0
    kpi = {
        "posts": len(out_pages), "star": sum(1 for p in out_pages if p["priority"] == "high"),
        "platforms": len({p["platform"].lower() for p in out_pages if p["platform"]}),
        "alive": len(alive), "indexed": sum(1 for p in out_pages if p["status"] in wl.INDEXED),
        "top10": sum(1 for p in out_pages if p["position"] is not None and p["position"] <= wl.TOP
                     and p["status"] not in wl.GONE and p["status"] != "moved"),
        "attention": sum(1 for p in out_pages if p["status"] in wl.GONE or p["status"] == "not checked yet"),
        "gone": sum(1 for p in out_pages if p["status"] in wl.GONE),
        "unchecked": sum(1 for p in out_pages if p["status"] == "not checked yet"),
        "sales": n_sales, "commission": {k: round(v, 2) for k, v in tot.items() if v},
    }
    return {"today": today.isoformat(), "currency": cur, "pages": out_pages, "platforms": out_plat,
            "sales": out_sales, "links": links, "journal": raw, "journal_cols": journal_cols, "kpi": kpi,
            "filters": {k: v for k, v in (("platform", platform), ("priority", priority), ("topic", topic)) if v},
            "has_links_to_site": any(p["link_target"] for p in out_pages)}


# ---------- xlsx (no dependencies) ----------

BAD_XML = re.compile("[\x00-\x08\x0b\x0c\x0e-\x1f￾￿]")
STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<numFmts count="2"><numFmt numFmtId="164" formatCode="#,##0.00"/><numFmt numFmtId="165" formatCode="yyyy-mm-dd"/></numFmts>
<fonts count="6">
<font><sz val="11"/><name val="Calibri"/><family val="2"/></font>
<font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/><family val="2"/></font>
<font><u/><sz val="11"/><color rgb="FF1F5FD6"/><name val="Calibri"/><family val="2"/></font>
<font><b/><sz val="16"/><color rgb="FF101826"/><name val="Calibri"/><family val="2"/></font>
<font><b/><sz val="11"/><name val="Calibri"/><family val="2"/></font>
<font><sz val="10"/><color rgb="FF6B7280"/><name val="Calibri"/><family val="2"/></font>
</fonts>
<fills count="4">
<fill><patternFill patternType="none"/></fill>
<fill><patternFill patternType="gray125"/></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FF16233A"/><bgColor indexed="64"/></patternFill></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FFE3F6EC"/><bgColor indexed="64"/></patternFill></fill>
</fills>
<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="10">
<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
<xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1" applyAlignment="1"><alignment vertical="center" wrapText="1"/></xf>
<xf numFmtId="165" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/>
<xf numFmtId="164" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/>
<xf numFmtId="0" fontId="2" fillId="0" borderId="0" xfId="0" applyFont="1"/>
<xf numFmtId="3" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/>
<xf numFmtId="0" fontId="3" fillId="0" borderId="0" xfId="0" applyFont="1"/>
<xf numFmtId="0" fontId="4" fillId="0" borderId="0" xfId="0" applyFont="1"/>
<xf numFmtId="3" fontId="4" fillId="3" borderId="0" xfId="0" applyNumberFormat="1" applyFont="1" applyFill="1"/>
<xf numFmtId="0" fontId="5" fillId="0" borderId="0" xfId="0" applyFont="1"/>
</cellXfs>
<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>"""
S_TEXT, S_HEAD, S_DATE, S_MONEY, S_LINK, S_INT, S_TITLE, S_BOLD, S_TOP, S_MUTED = range(10)
EPOCH = date(1899, 12, 30)


def col_letter(i):
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def sheet_name(s, used):
    s = re.sub(r"[\[\]:*?/\\]", " ", s)[:31].strip() or "Sheet"
    base, n = s, 2
    while s.lower() in used:
        s = f"{base[:28]} {n}"
        n += 1
    used.add(s.lower())
    return s


class Sheet:
    """kind per column: text, date, money, int, num, url."""

    def __init__(self, name, header=None, kinds=None, widths=None):
        self.name, self.header, self.kinds, self.widths = name, header, kinds, widths
        self.rows, self.links, self.free = [], [], []   # free: (row_cells) for summary-like sheets

    def cell(self, ref, v, kind, style=None):
        if v is None or v == "":
            return ""
        if kind == "date":
            d = v if isinstance(v, date) else wl.pdate(v)
            if d:
                return f'<c r="{ref}" s="{style if style is not None else S_DATE}"><v>{(d - EPOCH).days}</v></c>'
            kind = "text"
        if kind in ("money", "int", "num") and isinstance(v, (int, float)):
            st = style if style is not None else (S_MONEY if kind == "money" else S_INT if kind == "int" else S_TEXT)
            return f'<c r="{ref}" s="{st}"><v>{round(v, 4)}</v></c>'
        t = BAD_XML.sub("", str(v))[:32000]
        st = style if style is not None else (S_LINK if kind == "url" and t.startswith("http") else S_TEXT)
        if kind == "url" and t.startswith("http") and len(self.links) < 60000:
            self.links.append((ref, t))
        return f'<c r="{ref}" t="inlineStr" s="{st}"><is><t xml:space="preserve">{xesc(t)}</t></is></c>'

    def xml(self):
        out, r = [], 0
        if self.free:
            for cells in self.free:
                r += 1
                cs = "".join(self.cell(f"{col_letter(i)}{r}", v, k, s) for i, (v, k, s) in enumerate(cells))
                out.append(f'<row r="{r}">{cs}</row>')
        if self.header:
            r += 1
            hdr_row = r
            cs = "".join(self.cell(f"{col_letter(i)}{r}", h, "text", S_HEAD) for i, h in enumerate(self.header))
            out.append(f'<row r="{r}" ht="22" customHeight="1">{cs}</row>')
            for row in self.rows:
                r += 1
                cs = []
                for i, v in enumerate(row):
                    style = None
                    if isinstance(v, tuple):
                        v, style = v
                    cs.append(self.cell(f"{col_letter(i)}{r}", v, self.kinds[i], style))
                out.append(f'<row r="{r}">{"".join(cs)}</row>')
        ncols = len(self.header) if self.header else max((len(c) for c in self.free), default=1)
        last = f"{col_letter(ncols - 1)}{max(r, 1)}"
        views = ""
        if self.header and not self.free:
            views = ('<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" '
                     'activePane="bottomLeft" state="frozen"/><selection pane="bottomLeft" activeCell="A2" sqref="A2"/>'
                     '</sheetView></sheetViews>')
        else:
            views = '<sheetViews><sheetView workbookViewId="0" showGridLines="0"/></sheetViews>'
        cols = ""
        if self.widths:
            cols = "<cols>" + "".join(f'<col min="{i + 1}" max="{i + 1}" width="{w}" customWidth="1"/>'
                                      for i, w in enumerate(self.widths)) + "</cols>"
        af = ""
        if self.header and not self.free and self.rows:
            af = f'<autoFilter ref="A1:{last}"/>'
        hl = ""
        if self.links:
            hl = "<hyperlinks>" + "".join(f'<hyperlink ref="{ref}" r:id="rId{i + 1}"/>'
                                          for i, (ref, _) in enumerate(self.links)) + "</hyperlinks>"
        self.filter_ref = f"A1:{last}" if af else None
        return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
                'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
                f'<dimension ref="A1:{last}"/>{views}<sheetFormatPr defaultRowHeight="15"/>{cols}'
                f'<sheetData>{"".join(out)}</sheetData>{af}{hl}'
                '<pageMargins left="0.5" right="0.5" top="0.6" bottom="0.6" header="0.3" footer="0.3"/></worksheet>')

    def rels(self):
        items = "".join(f'<Relationship Id="rId{i + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
                        f'relationships/hyperlink" Target="{xesc(u, {chr(34): "&quot;"})}" TargetMode="External"/>'
                        for i, (_, u) in enumerate(self.links))
        return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships '
                f'xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{items}</Relationships>')


def abs_ref(ref):
    return ":".join(re.sub(r"([A-Z]+)(\d+)", r"$\1$\2", part) for part in ref.split(":"))


def write_xlsx(sheets, path):
    bodies = [s.xml() for s in sheets]  # builds links first
    n = len(sheets)
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
          '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
          '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
          '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
          + "".join(f'<Override PartName="/xl/worksheets/sheet{i + 1}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
                    for i in range(n)) + "</Types>")
    root_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
                 '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
                 '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
                 '</Relationships>')
    defined = "".join(f'<definedName name="_xlnm._FilterDatabase" localSheetId="{i}" hidden="1">'
                      f"'{xesc(s.name)}'!{abs_ref(s.filter_ref)}</definedName>"
                      for i, s in enumerate(sheets) if s.filter_ref)
    wb = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
          'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><bookViews><workbookView/></bookViews><sheets>'
          + "".join(f'<sheet name="{xesc(s.name, {chr(34): "&quot;"})}" sheetId="{i + 1}" r:id="rId{i + 1}"/>' for i, s in enumerate(sheets))
          + "</sheets>" + (f"<definedNames>{defined}</definedNames>" if defined else "") + "</workbook>")
    wb_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
               + "".join(f'<Relationship Id="rId{i + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i + 1}.xml"/>'
                         for i in range(n))
               + f'<Relationship Id="rId{n + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
               + "</Relationships>")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<dc:title>PARASITER base</dc:title><dc:creator>PARASITER</dc:creator>'
            f'<dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created></cp:coreProperties>')
    app = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
           '<Application>PARASITER</Application></Properties>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", root_rels)
        z.writestr("docProps/core.xml", core)
        z.writestr("docProps/app.xml", app)
        z.writestr("xl/workbook.xml", wb)
        z.writestr("xl/_rels/workbook.xml.rels", wb_rels)
        z.writestr("xl/styles.xml", STYLES)
        for i, (s, body) in enumerate(zip(sheets, bodies)):
            z.writestr(f"xl/worksheets/sheet{i + 1}.xml", body)
            if s.links:
                z.writestr(f"xl/worksheets/_rels/sheet{i + 1}.xml.rels", s.rels())


def build_workbook(d, t, path):
    used = set()
    st = t["s"]
    cur = d["currency"]
    k = d["kpi"]

    summary = Sheet(sheet_name(t["sheet_summary"], used))
    summary.widths = [30, 22, 50]
    com = " · ".join(wl.money(v, c) for c, v in k["commission"].items()) or "—"
    summary.free = [
        [(t["title"], "text", S_TITLE)],
        [(f'{t["built"]} {d["today"]} · {t["from_files"]}' + (f' · {t["filtered"]}: ' + ", ".join(f"{a}={b}" for a, b in d["filters"].items()) if d["filters"] else ""), "text", S_MUTED)],
        [],
        [(t["k_posts"], "text", S_BOLD), (k["posts"], "int", S_INT)],
        [(t["k_star"], "text", None), (k["star"], "int", S_INT)],
        [(t["k_platforms"], "text", None), (k["platforms"], "int", S_INT)],
        [(t["k_alive"], "text", None), (k["alive"], "int", S_INT)],
        [(t["k_indexed"], "text", None), (k["indexed"], "int", S_INT)],
        [(t["k_top10"], "text", S_BOLD), (k["top10"], "int", S_TOP)],
        [(t["gone"], "text", None), (k["gone"], "int", S_INT)],
        [(t["unchecked"], "text", None), (k["unchecked"], "int", S_INT)],
        [(t["k_sales"], "text", None), (k["sales"], "int", S_INT)],
        [(t["k_commission"], "text", S_BOLD), (com, "text", S_BOLD)],
        [],
        [(t["by_platform"], "text", S_BOLD)],
    ]
    for p in d["platforms"]:
        if p["pages"]:
            summary.free.append([(p["platform"], "text", None), (p["pages"], "int", S_INT),
                                 (f'{t["alive"]} {p["alive"]} · {t["indexed"]} {p["indexed"]} · {t["top10"]} {p["top10"]} · '
                                  f'{t["gone"]} {p["gone"]} · {t["unchecked"]} {p["unchecked"]}', "text", S_MUTED)])
    summary.free += [[], [(t["foot"], "text", S_MUTED)]]

    show_link = d["has_links_to_site"]
    hdr = [t["published"], t["page"], t["platform"], t["topic"], t["prio"], t["offer"], t["program"], t["campaign"],
           t["sub_id"], t["query"], t["type"], t["status"], t["position"], t["best_pos"], t["pos_date"],
           t["last_check"], t["audit"], t["views"], t["aff_clicks"], t["sales"], f'{t["commission"]}, {cur}',
           t["age"], t["source"]]
    kinds = ["date", "url", "text", "text", "text", "text", "text", "text", "text", "text", "text", "text",
             "int", "int", "date", "date", "int", "int", "int", "int", "money", "int", "text"]
    widths = [12, 52, 14, 28, 4, 16, 18, 14, 12, 30, 16, 14, 9, 9, 12, 12, 7, 10, 10, 8, 12, 9, 28]
    if show_link:
        hdr += [t["link_target"], t["link_rel"]]
        kinds += ["url", "text"]
        widths += [36, 10]
    posts = Sheet(sheet_name(t["sheet_posts"], used), hdr, kinds, widths)
    for p in d["pages"]:
        pos = p["position"]
        row = [p["published"] or "", p["url"], p["platform"], p["topic"], "★" if p["priority"] == "high" else "",
               p["offer"], p["program"], p["campaign"], p["sub_id"], p["query"], p["type"],
               st.get(p["status"], p["status"]), (pos, S_TOP) if pos is not None and pos <= wl.TOP else pos,
               p["best_pos"], p["pos_date"], p["last_check"], p["score"], p["views"], p["aff_clicks"], p["sales"],
               p["commission"], p["age"], p["source"]]
        if show_link:
            row += [p["link_target"], p["link_rel"]]
        posts.rows.append(row)

    plats = Sheet(sheet_name(t["sheet_platforms"], used),
                  [t["platform"], t["domain"], t["ptype"], t["state"], t["prio"], t["pages"], t["alive"], t["indexed"],
                   t["top10"], t["gone"], t["unchecked"], t["last_page"], t["sales"], f'{t["commission"]}, {cur}',
                   t["score"], t["language"], t["links"], t["account"], t["note"]],
                  ["text", "text", "text", "text", "text", "int", "int", "int", "int", "int", "int", "date", "int",
                   "money", "int", "text", "text", "text", "text"],
                  [16, 22, 12, 10, 4, 8, 8, 9, 8, 9, 11, 12, 8, 12, 8, 9, 10, 18, 30])
    for p in d["platforms"]:
        plats.rows.append([p["platform"], p["domain"], p["type"], st.get(p["state"], p["state"]),
                           "★" if p["priority"] == "high" else "", p["pages"], p["alive"], p["indexed"],
                           (p["top10"], S_TOP) if p["top10"] else p["top10"], p["gone"], p["unchecked"],
                           p["last_page"], p["sales"], p["commission"], p["score"], p["language"], p["links"],
                           p["account"], p["note"]])
    sheets = [summary, posts, plats]

    if d["sales"]:
        sales = Sheet(sheet_name(t["sheet_sales"], used),
                      [t["date"], t["program"], t["offer"], t["page"], t["sub_id"], t["order_id"], t["amount"],
                       t["commission"], t["currency"], t["sale_status"], t["sale_source"]],
                      ["date", "text", "text", "url", "text", "text", "money", "money", "text", "text", "text"],
                      [12, 20, 18, 46, 12, 16, 12, 12, 9, 12, 26])
        for r in d["sales"]:
            sales.rows.append([r["date"], r["program"], r["offer"], r["page"], r["sub_id"], r["order_id"], r["amount"],
                               r["commission"], r["currency"], st.get(r["status"], r["status"]), r["source"]])
        sheets.append(sales)
    if d["links"]:
        links = Sheet(sheet_name(t["sheet_links"], used),
                      [t["program"], t["product"], t["link"], t["alt_links"], t["commission"], t["added"], t["note"]],
                      ["text", "text", "url", "text", "text", "date", "text"], [18, 28, 52, 30, 11, 12, 28])
        for r in d["links"]:
            links.rows.append([r["program"], r["product"], r["link"], r["alt_links"], r["commission"], r["added"], r["note"]])
        sheets.append(links)
    if d["journal"]:
        cols = d["journal_cols"]
        kind = {"date": "date", "page_url": "url", "score": "num", "views": "num", "clicks": "num", "aff_clicks": "num",
                "sales": "num", "revenue": "money", "minutes": "num", "position": "num", "cost": "money"}
        j = Sheet(sheet_name(t["sheet_journal"], used), cols, [kind.get(c, "text") for c in cols],
                  [12 if c == "date" else 46 if c == "page_url" else 40 if c == "note" else 12 for c in cols])
        for r in d["journal"]:
            j.rows.append([wl.num(r.get(c)) if kind.get(c) in ("num", "money") and wl.num(r.get(c)) is not None
                           else r.get(c, "") for c in cols])
        sheets.append(j)
    write_xlsx(sheets, path)
    return [s.name for s in sheets]


# ---------- html dashboard ----------

def build_html(d, t, lang, xlsx_name, path, xlsx_b64=""):
    data = {k: d[k] for k in ("today", "currency", "pages", "platforms", "sales", "links", "kpi", "filters",
                              "has_links_to_site")}
    payload = json.dumps({"d": data, "t": t, "lang": lang, "xlsx": xlsx_name or "", "xlsx_b64": xlsx_b64,
                          "tones": STATUS_TONE, "top": wl.TOP}, ensure_ascii=False, default=str)
    payload = payload.replace("</", "<\\/").replace("<!--", "<\\!--")
    page = TEMPLATE.replace("__TITLE__", html.escape(t["title"])).replace("__LANG__", lang).replace("__DATA__", payload)
    page = HEAD + page + "</body></html>"
    with open(path, "w", encoding="utf-8") as f:
        f.write(page)


# Same document shape the Claude artifact publisher uses, so the file opens in standards mode as a local file
# and is recognised (not nested) when published as an artifact.
HEAD = ('<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1,'
        'viewport-fit=cover"><style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);'
        'padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,-apple-system,sans-serif}'
        'img{max-width:100%}[hidden]{display:none!important}</style></head><body>')

TEMPLATE = r"""<title>__TITLE__</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Geist+Mono:wght@400;500&display=swap">
<style>
/* Layout: one control-room column — totals strip, status-by-platform bars, then a filterable register in tabs. */
:root{
  --bg:#f5f7fa; --panel:#ffffff; --line:#dde3ec; --ink:#0d1522; --sub:#5a6577; --dot:#d3dae5;
  --accent:#1d5ff0; --accent2:#0891b2; --accent-soft:#e6eeff;
  --good:#0e8a52; --good-bg:#e2f5ea; --info:#1d5ff0; --info-bg:#e6eeff; --warn:#b06a00; --warn-bg:#fdf1dc;
  --bad:#c42b2b; --bad-bg:#fbe6e6; --muted:#6b7586; --muted-bg:#edf0f4;
  --font:"Geist",ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  --mono:"Geist Mono",ui-monospace,"SFMono-Regular",Menlo,Consolas,monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#0b0f16; --panel:#111824; --line:#1f2a3a; --ink:#e7edf6; --sub:#8a97ab; --dot:#18212e;
  --accent:#4d8dff; --accent2:#22d3ee; --accent-soft:#132544;
  --good:#3ccf8e; --good-bg:#0f2a1f; --info:#4d8dff; --info-bg:#132544; --warn:#f2b24b; --warn-bg:#2e2310;
  --bad:#ff6b6b; --bad-bg:#331617; --muted:#8a97ab; --muted-bg:#18212e; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#0b0f16; --panel:#111824; --line:#1f2a3a; --ink:#e7edf6; --sub:#8a97ab; --dot:#18212e;
  --accent:#4d8dff; --accent2:#22d3ee; --accent-soft:#132544;
  --good:#3ccf8e; --good-bg:#0f2a1f; --info:#4d8dff; --info-bg:#132544; --warn:#f2b24b; --warn-bg:#2e2310;
  --bad:#ff6b6b; --bad-bg:#331617; --muted:#8a97ab; --muted-bg:#18212e; color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font-family:var(--font);font-size:14px;line-height:1.45;
  background-image:radial-gradient(var(--dot) 1px,transparent 1px);background-size:18px 18px}
.wrap{max-width:1240px;margin:0 auto;padding-block:20px 40px;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));
  display:flex;flex-direction:column;gap:18px}
header{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:12px}
.brand{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent2);
  display:flex;align-items:center;gap:8px}
.brand i{width:7px;height:7px;border-radius:50%;background:var(--accent2);box-shadow:0 0 8px var(--accent2)}
h1{margin:4px 0 2px;font-size:clamp(22px,4vw,30px);font-weight:700;letter-spacing:-.01em;text-wrap:balance}
.meta{color:var(--sub);font-size:12.5px;font-family:var(--mono)}
.actions{display:flex;flex-wrap:wrap;gap:8px}
.btn{font:500 13px var(--font);border-radius:8px;padding:8px 13px;border:1px solid var(--line);background:var(--panel);
  color:var(--ink);cursor:pointer;text-decoration:none;display:inline-flex;align-items:center;gap:7px}
.btn.primary{background:var(--accent);border-color:var(--accent);color:#fff}
.btn:hover{border-color:var(--accent)}
.btn:focus-visible,select:focus-visible,input:focus-visible,.tab:focus-visible,th button:focus-visible{outline:2px solid var(--accent2);outline-offset:2px}
.btn svg{width:15px;height:15px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(138px,1fr));gap:10px}
.kpi{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px 14px;min-width:0}
.kpi .l{font-size:11.5px;color:var(--sub);text-transform:uppercase;letter-spacing:.06em}
.kpi .v{font:600 26px/1.15 var(--mono);font-variant-numeric:tabular-nums;margin-top:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.kpi .n{font-size:11.5px;color:var(--sub);margin-top:2px}
.kpi.top .v{color:var(--good)} .kpi.att .v{color:var(--warn)} .kpi.att.zero .v{color:var(--ink)}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px;min-width:0}
.panel h2{font-size:14px;margin:0 0 12px;font-weight:600}
.bars{display:grid;gap:8px}
.bar{display:grid;grid-template-columns:minmax(80px,150px) 1fr 44px;align-items:center;gap:10px;font-size:12.5px}
.bar .nm{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.track{display:flex;height:12px;border-radius:6px;overflow:hidden;background:var(--muted-bg)}
.track span{height:100%}
.bar .ct{font-family:var(--mono);text-align:right;color:var(--sub);font-variant-numeric:tabular-nums}
.legend{display:flex;flex-wrap:wrap;gap:12px;margin-top:12px;font-size:12px;color:var(--sub)}
.legend b{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:5px;vertical-align:-1px}
.tabs{display:flex;gap:4px;flex-wrap:wrap;border-bottom:1px solid var(--line);margin:-4px 0 14px}
.tab{font:500 13.5px var(--font);background:none;border:0;border-bottom:2px solid transparent;color:var(--sub);
  padding:8px 12px;cursor:pointer;margin-bottom:-1px}
.tab[aria-selected="true"]{color:var(--ink);border-bottom-color:var(--accent)}
.tab .c{font-family:var(--mono);font-size:11.5px;color:var(--sub);margin-left:5px}
.tools{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:12px}
.tools input[type=search]{flex:1 1 220px;min-width:0;font:13px var(--font);padding:8px 11px;border-radius:8px;
  border:1px solid var(--line);background:var(--bg);color:var(--ink)}
select{font:13px var(--font);padding:7px 9px;border-radius:8px;border:1px solid var(--line);background:var(--bg);color:var(--ink);max-width:180px}
.chip{display:inline-flex;align-items:center;gap:6px;font-size:13px;padding:6px 10px;border-radius:999px;border:1px solid var(--line);cursor:pointer;user-select:none}
.chip input{accent-color:var(--accent);margin:0}
.count{font-family:var(--mono);font-size:12px;color:var(--sub);margin-left:auto}
.tbl{overflow-x:auto;border:1px solid var(--line);border-radius:10px}
table{border-collapse:collapse;width:100%;font-size:13px}
th,td{padding:8px 10px;text-align:left;border-bottom:1px solid var(--line);white-space:nowrap;vertical-align:middle}
th{background:var(--bg);font-weight:500;color:var(--sub);font-size:12px;position:sticky;top:0}
th button{all:unset;cursor:pointer;display:inline-flex;gap:4px;align-items:center}
th button::after{content:"";width:8px;opacity:.8}
th[aria-sort="ascending"] button::after{content:"↑"} th[aria-sort="descending"] button::after{content:"↓"}
tbody tr:hover td{background:var(--accent-soft)}
td.num{text-align:right;font-family:var(--mono);font-variant-numeric:tabular-nums}
td.pg{max-width:340px;overflow:hidden;text-overflow:ellipsis}
td.pg a{color:var(--accent);text-decoration:none}
td.pg a:hover{text-decoration:underline}
td.pg small{display:block;color:var(--sub);font-size:11.5px;overflow:hidden;text-overflow:ellipsis}
td.tw{white-space:normal;min-width:160px;max-width:260px}
.pill{display:inline-block;font-size:11.5px;font-weight:500;padding:2px 8px;border-radius:999px;white-space:nowrap}
.good{background:var(--good-bg);color:var(--good)} .info{background:var(--info-bg);color:var(--info)}
.warn{background:var(--warn-bg);color:var(--warn)} .bad{background:var(--bad-bg);color:var(--bad)}
.muted{background:var(--muted-bg);color:var(--muted)}
.pos-top{font-weight:700;color:var(--good)}
.delta{font-size:11px;margin-left:4px} .up{color:var(--good)} .down{color:var(--bad)}
.star{color:var(--warn)}
.guess{color:var(--sub);font-style:italic}
.empty{padding:28px;text-align:center;color:var(--sub)}
.more{margin:12px auto 0;display:flex}
tfoot td{font-weight:600;background:var(--bg)}
.foot{color:var(--sub);font-size:12px}
.toast{position:fixed;left:50%;transform:translateX(-50%);bottom:calc(18px + env(safe-area-inset-bottom,0px));
  background:var(--ink);color:var(--bg);padding:8px 14px;border-radius:8px;font-size:13px}
@media (max-width:560px){.bar{grid-template-columns:90px 1fr 36px}.count{margin-left:0;width:100%}}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style>
<div class="wrap" id="app">
  <header>
    <div>
      <div class="brand"><i></i>PARASITER</div>
      <h1 id="h1"></h1>
      <div class="meta" id="meta"></div>
    </div>
    <div class="actions" id="actions"></div>
  </header>
  <section class="kpis" id="kpis"></section>
  <section class="panel" id="byplat" hidden><h2 id="byplat-h"></h2><div class="bars" id="bars"></div><div class="legend" id="legend"></div></section>
  <section class="panel">
    <div class="tabs" role="tablist" id="tabs"></div>
    <div id="view"></div>
  </section>
  <p class="foot" id="foot"></p>
</div>
<div class="toast" id="toast" hidden></div>
<script type="application/json" id="data">__DATA__</script>
<script>
(function(){
const P=JSON.parse(document.getElementById('data').textContent);
const D=P.d,T=P.t,S=T.s,TOP=P.top;
const $=s=>document.querySelector(s);
const esc=v=>String(v==null?'':v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const nf=new Intl.NumberFormat(P.lang==='en'?'en-US':P.lang,{maximumFractionDigits:0});
const mf=new Intl.NumberFormat(P.lang==='en'?'en-US':P.lang,{minimumFractionDigits:2,maximumFractionDigits:2});
const sym={USD:'$',EUR:'€',GBP:'£'};
const money=(v,c)=>v==null?'—':((v<0?'−':'')+(sym[c]||((c||'')+' '))+mf.format(Math.abs(v)));
const num=v=>v==null||v===''?'—':nf.format(v);
const st=s=>S[s]!=null&&S[s]!==''?S[s]:s;
const fmtT=(s,o)=>s.replace(/\{(\w+)\}/g,(_,k)=>o[k]);
function host(u){try{return new URL(u).hostname.replace(/^www\./,'')}catch(e){return u}}
function path(u){try{const x=new URL(u);return decodeURIComponent(x.pathname+x.search).replace(/\/$/,'')||'/'}catch(e){return ''}}

document.title=T.title;
$('#h1').textContent=T.title;
$('#meta').textContent=T.built+' '+D.today+(Object.keys(D.filters).length?' · '+T.filtered+': '+Object.entries(D.filters).map(e=>e[1]).join(', '):'');
$('#foot').textContent=T.foot;

// ---- downloads ----
let DL=null; const inViewer=!!(window.claude&&window.claude.use);
const ico='<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M8 2v8m0 0l-3-3m3 3l3-3M3 13h10"/></svg>';
const acts=$('#actions');
if(P.xlsx_b64){acts.insertAdjacentHTML('beforeend','<button class="btn primary" id="dl-x" type="button">'+ico+esc(T.dl_xlsx)+'</button>')}
acts.insertAdjacentHTML('beforeend','<button class="btn" id="dl-c" type="button">'+ico+esc(T.dl_csv)+'</button>');
function toast(m){const t=$('#toast');t.textContent=m;t.hidden=false;clearTimeout(toast.h);toast.h=setTimeout(()=>t.hidden=true,2200)}
async function save(name,data,type){
  if(DL){try{await DL.save({filename:name,data});toast(T.saved)}catch(e){if(e&&e.code==='declined')toast(T.declined)}return}
  if(inViewer)return;
  const b=data instanceof Blob?data:new Blob([data],{type:type||'text/csv;charset=utf-8'});
  const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=name;document.body.appendChild(a);a.click();
  setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove()},500);
}
// The workbook travels inside the page (base64), so the button works in an artifact and as a local file alike.
if(P.xlsx_b64)$('#dl-x').addEventListener('click',()=>{const bin=atob(P.xlsx_b64);const u=new Uint8Array(bin.length);
  for(let i=0;i<bin.length;i++)u[i]=bin.charCodeAt(i);
  save(P.xlsx||'parasiter-base.xlsx',new Blob([u],{type:'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}),'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')});
if(inViewer){claude.use('downloads').then(d=>{DL=d;if(!d)acts.hidden=true}).catch(()=>{acts.hidden=true})}
$('#dl-c').addEventListener('click',()=>{const v=views[cur];if(!v)return;
  const rows=v.csv();const csv='﻿'+rows.map(r=>r.map(c=>{c=c==null?'':String(c);return /[",;\n]/.test(c)?'"'+c.replace(/"/g,'""')+'"':c}).join(',')).join('\r\n');
  save('parasiter-'+cur+'-'+D.today+'.csv',csv)});

// ---- KPIs ----
const K=D.kpi;
const com=Object.entries(K.commission).map(e=>money(e[1],e[0])).join(' · ')||'—';
const tiles=[
  ['',T.k_posts,num(K.posts),K.star?(T.k_star+': '+K.star):''],
  ['',T.k_platforms,num(K.platforms),''],
  ['',T.k_alive,num(K.alive),K.posts?Math.round(K.alive/K.posts*100)+'%':''],
  ['',T.k_indexed,num(K.indexed),''],
  ['top',T.k_top10,num(K.top10),''],
  ['att'+(K.attention?'':' zero'),T.k_attention,num(K.attention),T.k_attention_note],
  ['',T.k_sales,num(K.sales),com]];
$('#kpis').innerHTML=tiles.map(t=>'<div class="kpi '+t[0]+'"><div class="l">'+esc(t[1])+'</div><div class="v">'+esc(t[2])+'</div>'+(t[3]?'<div class="n">'+esc(t[3])+'</div>':'')+'</div>').join('');

// ---- status by platform ----
const groups=[['good',['indexed']],['info',['live','not-indexed','dropped']],['muted',['not checked yet']],['bad',['noindex','removed','dead','moved']]];
const gLabel={good:T.indexed,info:T.alive,muted:T.unchecked,bad:T.gone};
const byP={};D.pages.forEach(p=>{const k=p.platform||'—';const g=byP[k]||(byP[k]={n:0,good:0,info:0,muted:0,bad:0});g.n++;
  const gr=groups.find(x=>x[1].includes(p.status));g[gr?gr[0]:'muted']++});
const plist=Object.entries(byP).sort((a,b)=>b[1].n-a[1].n).slice(0,14);
if(plist.length){
  $('#byplat').hidden=false;$('#byplat-h').textContent=T.by_platform;
  const mx=plist[0][1].n;
  $('#bars').innerHTML=plist.map(([k,g])=>'<div class="bar"><span class="nm" title="'+esc(k)+'">'+esc(k)+'</span><div class="track" style="width:'+Math.max(6,g.n/mx*100)+'%">'+
    groups.map(x=>g[x[0]]?'<span style="width:'+(g[x[0]]/g.n*100)+'%;background:var(--'+x[0]+')" title="'+esc(gLabel[x[0]]+': '+g[x[0]])+'"></span>':'').join('')+
    '</div><span class="ct">'+g.n+'</span></div>').join('');
  $('#legend').innerHTML=groups.map(x=>'<span><b style="background:var(--'+x[0]+')"></b>'+esc(gLabel[x[0]])+'</span>').join('');
}

// ---- table engine ----
function table(cfg){
  // cfg: id, rows, cols:[{k,label,cls,sort:fn,cell:fn,csv:fn}], filters(row)->bool, tools(html), bind(rerender), foot(rows)
  let sortK=cfg.sortK||null,dir=cfg.dir||1,limit=100;
  const host=document.createElement('div');
  function filtered(){let r=cfg.rows.filter(cfg.filter||(()=>true));
    if(sortK){const c=cfg.cols.find(c=>c.k===sortK);const f=c.sort||(x=>x[sortK]);
      r=r.slice().sort((a,b)=>{let x=f(a),y=f(b);const nx=x==null||x==='',ny=y==null||y==='';if(nx&&ny)return 0;if(nx)return 1;if(ny)return -1;
        return (typeof x==='number'&&typeof y==='number'?x-y:String(x).localeCompare(String(y)))*dir})}
    return r}
  function render(){const r=filtered();
    const head='<tr>'+cfg.cols.map(c=>'<th'+(c.cls==='num'?' style="text-align:right"':'')+(sortK===c.k?' aria-sort="'+(dir>0?'ascending':'descending')+'"':'')+'><button type="button" data-k="'+c.k+'">'+esc(c.label)+'</button></th>').join('')+'</tr>';
    const body=r.slice(0,limit).map(x=>'<tr>'+cfg.cols.map(c=>'<td class="'+(c.cls||'')+'">'+c.cell(x)+'</td>').join('')+'</tr>').join('');
    const foot=cfg.foot&&r.length?cfg.foot(r):'';
    host.querySelector('.tb').innerHTML=r.length?'<table><thead>'+head+'</thead><tbody>'+body+'</tbody>'+foot+'</table>':'<div class="empty">'+esc(cfg.rows.length?T.empty:(cfg.emptyText||T.empty))+'</div>';
    const cnt=host.querySelector('.count');if(cnt)cnt.textContent=fmtT(T.shown,{n:r.length,m:cfg.rows.length});
    const mb=host.querySelector('.more');mb.hidden=r.length<=limit;mb.textContent=fmtT(T.more,{n:Math.min(100,r.length-limit)});
    host.querySelectorAll('th button').forEach(b=>b.onclick=()=>{const k=b.dataset.k;if(sortK===k)dir=-dir;else{sortK=k;const c=cfg.cols.find(c=>c.k===k);dir=c.asc?1:c.cls==='num'?-1:1}render()});
  }
  host.innerHTML=(cfg.tools||'<div class="tools"><span class="count"></span></div>')+'<div class="tbl tb"></div><button class="btn more" type="button" hidden></button>';
  host.querySelector('.more').onclick=()=>{limit+=100;render()};
  if(cfg.bind)cfg.bind(host,()=>{limit=100;render()});
  return {el:host,render,csv:()=>[cfg.cols.map(c=>c.label)].concat(filtered().map(x=>cfg.cols.map(c=>c.csv?c.csv(x):x[c.k])))};
}

// posts
const opts=(vals)=>'<option value="">'+esc(T.all)+'</option>'+[...new Set(vals.filter(Boolean))].sort((a,b)=>a.localeCompare(b)).map(v=>'<option>'+esc(v)+'</option>').join('');
const stOpts='<option value="">'+esc(T.all)+'</option>'+[...new Set(D.pages.map(p=>p.status))].map(v=>'<option value="'+esc(v)+'">'+esc(st(v))+'</option>').join('');
const F={q:'',platform:'',status:'',topic:'',offer:'',star:false,top:false};
function posCell(p){if(p.position==null)return '—';let s='<span class="'+(p.position<=TOP?'pos-top':'')+'">'+nf.format(p.position)+'</span>';
  if(p.prev_pos!=null&&p.prev_pos!==p.position){const d=p.prev_pos-p.position;s+='<span class="delta '+(d>0?'up':'down')+'">'+(d>0?'↑':'↓')+Math.abs(d)+'</span>'}return s}
const postCols=[
  {k:'priority',label:'★',cell:p=>p.priority==='high'?'<span class="star" title="★">★</span>':'',sort:p=>p.priority==='high'?0:p.priority==='normal'?1:2,csv:p=>p.priority==='high'?'★':''},
  {k:'published',label:T.published,cell:p=>p.published?esc(p.published):'<span class="guess">'+esc(T.unknown_date)+'</span>',csv:p=>p.published||''},
  {k:'url',label:T.page,cls:'pg',cell:p=>'<a href="'+esc(p.url)+'" target="_blank" rel="noopener noreferrer">'+esc(host(p.url))+'</a><small title="'+esc(p.url)+'">'+esc(path(p.url))+'</small>',sort:p=>p.url},
  {k:'platform',label:T.platform,cell:p=>esc(p.platform||'—')},
  {k:'topic',label:T.topic,cls:'tw',cell:p=>p.topic_guessed?'<span class="guess">'+esc(p.topic)+'</span>':esc(p.topic)},
  {k:'offer',label:T.offer,cell:p=>esc(p.offer||'—')},
  {k:'status',label:T.status,cell:p=>'<span class="pill '+(P.tones[p.status]||'muted')+'">'+esc(st(p.status))+'</span>',csv:p=>st(p.status)},
  {k:'position',label:T.position,cls:'num',asc:true,cell:posCell},
  {k:'score',label:T.audit,cls:'num',cell:p=>num(p.score)},
  {k:'views',label:T.views,cls:'num',cell:p=>num(p.views)},
  {k:'aff_clicks',label:T.aff_clicks,cls:'num',cell:p=>num(p.aff_clicks)},
  {k:'sales',label:T.sales,cls:'num',cell:p=>num(p.sales)},
  {k:'commission',label:T.commission,cls:'num',cell:p=>money(p.commission,D.currency)},
  {k:'query',label:T.query,cell:p=>esc(p.query||'—')},
  {k:'program',label:T.program,cell:p=>esc(p.program||'—')},
  {k:'sub_id',label:T.sub_id,cell:p=>esc(p.sub_id||'—')},
  {k:'last_check',label:T.last_check,cell:p=>esc(p.last_check||'—')}];
if(D.has_links_to_site)postCols.push({k:'link_target',label:T.link_target,cell:p=>esc(p.link_target||'—')},{k:'link_rel',label:T.link_rel,cell:p=>esc(p.link_rel||'—')});
const postsTools='<div class="tools"><input type="search" id="f-q" placeholder="'+esc(T.search)+'" aria-label="'+esc(T.search)+'">'+
  '<select id="f-platform" aria-label="'+esc(T.platform)+'">'+opts(D.pages.map(p=>p.platform)).replace('>'+esc(T.all)+'<','>'+esc(T.platform)+': '+esc(T.all)+'<')+'</select>'+
  '<select id="f-status" aria-label="'+esc(T.status)+'">'+stOpts.replace('>'+esc(T.all)+'<','>'+esc(T.status)+': '+esc(T.all)+'<')+'</select>'+
  '<select id="f-topic" aria-label="'+esc(T.topic)+'">'+opts(D.pages.map(p=>p.topic)).replace('>'+esc(T.all)+'<','>'+esc(T.topic)+': '+esc(T.all)+'<')+'</select>'+
  '<select id="f-offer" aria-label="'+esc(T.offer)+'">'+opts(D.pages.map(p=>p.offer)).replace('>'+esc(T.all)+'<','>'+esc(T.offer)+': '+esc(T.all)+'<')+'</select>'+
  (K.star?'<label class="chip"><input type="checkbox" id="f-star">'+esc(T.only_star)+'</label>':'')+
  (K.top10?'<label class="chip"><input type="checkbox" id="f-top">'+esc(T.only_top)+'</label>':'')+
  '<button class="btn" type="button" id="f-reset">'+esc(T.reset)+'</button><span class="count"></span></div>';
const views={};
views.posts=table({rows:D.pages,cols:postCols,tools:postsTools,emptyText:T.no_data,
  filter:p=>{if(F.platform&&p.platform!==F.platform)return false;if(F.status&&p.status!==F.status)return false;
    if(F.topic&&p.topic!==F.topic)return false;if(F.offer&&p.offer!==F.offer)return false;
    if(F.star&&p.priority!=='high')return false;if(F.top&&!(p.position!=null&&p.position<=TOP))return false;
    if(F.q){const h=(p.url+' '+p.topic+' '+p.offer+' '+p.query+' '+p.platform+' '+p.program+' '+p.sub_id+' '+p.campaign).toLowerCase();
      if(!F.q.split(/\s+/).every(w=>h.includes(w)))return false}return true},
  bind:(el,re)=>{const on=(id,k,ev,get)=>{const x=el.querySelector('#'+id);if(x)x.addEventListener(ev,()=>{F[k]=get(x);re()})};
    on('f-q','q','input',x=>x.value.trim().toLowerCase());
    ['platform','status','topic','offer'].forEach(k=>on('f-'+k,k,'change',x=>x.value));
    on('f-star','star','change',x=>x.checked);on('f-top','top','change',x=>x.checked);
    el.querySelector('#f-reset').addEventListener('click',()=>{Object.assign(F,{q:'',platform:'',status:'',topic:'',offer:'',star:false,top:false});
      el.querySelectorAll('input[type=search],select').forEach(x=>x.value='');el.querySelectorAll('input[type=checkbox]').forEach(x=>x.checked=false);re()})}});

views.platforms=table({rows:D.platforms,cols:[
  {k:'platform',label:T.platform,cell:p=>(p.priority==='high'?'<span class="star">★ </span>':'')+'<b>'+esc(p.platform)+'</b>'},
  {k:'domain',label:T.domain,cell:p=>esc(p.domain||'—')},
  {k:'type',label:T.ptype,cell:p=>esc(p.type||'—')},
  {k:'state',label:T.state,cell:p=>'<span class="pill '+({active:'good',testing:'info',paused:'warn',dropped:'muted',dead:'bad'}[p.state]||'muted')+'">'+esc(st(p.state))+'</span>',csv:p=>st(p.state)},
  {k:'pages',label:T.pages,cls:'num',cell:p=>num(p.pages)},
  {k:'alive',label:T.alive,cls:'num',cell:p=>num(p.alive)},
  {k:'indexed',label:T.indexed,cls:'num',cell:p=>num(p.indexed)},
  {k:'top10',label:T.top10,cls:'num',cell:p=>p.top10?'<span class="pos-top">'+p.top10+'</span>':'0'},
  {k:'gone',label:T.gone,cls:'num',cell:p=>p.gone?'<span style="color:var(--bad)">'+p.gone+'</span>':'0'},
  {k:'unchecked',label:T.unchecked,cls:'num',cell:p=>num(p.unchecked)},
  {k:'last_page',label:T.last_page,cell:p=>esc(p.last_page||'—')},
  {k:'sales',label:T.sales,cls:'num',cell:p=>num(p.sales)},
  {k:'commission',label:T.commission,cls:'num',cell:p=>money(p.commission,D.currency)},
  {k:'score',label:T.score,cls:'num',cell:p=>num(p.score)},
  {k:'links',label:T.links,cell:p=>esc(p.links||'—')}]});

if(D.sales.length){
  views.sales=table({rows:D.sales,cols:[
    {k:'date',label:T.date,cell:r=>esc(r.date)},
    {k:'program',label:T.program,cell:r=>esc(r.program)},
    {k:'offer',label:T.offer,cell:r=>esc(r.offer||'—')},
    {k:'page',label:T.page,cls:'pg',cell:r=>r.page?'<a href="'+esc(r.page)+'" target="_blank" rel="noopener noreferrer">'+esc(host(r.page))+'</a><small>'+esc(path(r.page))+'</small>':'<span class="guess">—</span>',sort:r=>r.page},
    {k:'sub_id',label:T.sub_id,cell:r=>esc(r.sub_id||'—')},
    {k:'amount',label:T.amount,cls:'num',cell:r=>money(r.amount,r.currency)},
    {k:'commission',label:T.commission,cls:'num',cell:r=>'<span style="'+(r.counted?'':'text-decoration:line-through;color:var(--sub)')+'">'+money(r.commission,r.currency)+'</span>'},
    {k:'currency',label:T.currency,cell:r=>esc(r.currency)},
    {k:'status',label:T.sale_status,cell:r=>'<span class="pill '+({approved:'good',pending:'warn',reversed:'bad'}[r.status]||'muted')+'">'+esc(st(r.status))+'</span>',csv:r=>st(r.status)},
    {k:'source',label:T.sale_source,cell:r=>esc(r.source)}],
    foot:r=>{const t={};r.forEach(x=>{if(x.counted)t[x.currency]=(t[x.currency]||0)+x.commission});
      return '<tfoot><tr><td colspan="6">'+esc(T.total)+'</td><td class="num">'+Object.entries(t).map(e=>money(e[1],e[0])).join(' · ')+'</td><td colspan="3"></td></tr></tfoot>'}});
}
if(D.links.length){
  views.links=table({rows:D.links,cols:[
    {k:'program',label:T.program,cell:r=>esc(r.program)},
    {k:'product',label:T.product,cell:r=>esc(r.product)},
    {k:'link',label:T.link,cls:'pg',cell:r=>'<a href="'+esc(r.link)+'" target="_blank" rel="noopener noreferrer">'+esc(host(r.link))+'</a><small>'+esc(path(r.link))+'</small>'},
    {k:'commission',label:T.commission,cell:r=>esc(r.commission||'—')},
    {k:'added',label:T.added,cell:r=>esc(r.added||'—')}]});
}

const tabDefs=[['posts',T.sheet_posts,D.pages.length],['platforms',T.sheet_platforms,D.platforms.length]];
if(views.sales)tabDefs.push(['sales',T.sheet_sales,D.sales.length]);
if(views.links)tabDefs.push(['links',T.sheet_links,D.links.length]);
let cur='posts';
const tabs=$('#tabs');
tabs.innerHTML=tabDefs.map(t=>'<button class="tab" role="tab" type="button" id="tab-'+t[0]+'" aria-selected="false">'+esc(t[1])+'<span class="c">'+t[2]+'</span></button>').join('');
function show(name){cur=name;tabDefs.forEach(t=>$('#tab-'+t[0]).setAttribute('aria-selected',t[0]===name?'true':'false'));
  const v=$('#view');v.replaceChildren(views[name].el);views[name].render();
  try{localStorage.setItem('parasiter-base-tab',name)}catch(e){}}
tabDefs.forEach(t=>$('#tab-'+t[0]).addEventListener('click',()=>show(t[0])));
let start='posts';try{const s=localStorage.getItem('parasiter-base-tab');if(s&&views[s])start=s}catch(e){}
show(start);
})();
</script>
"""


def main():
    ap = argparse.ArgumentParser(description="PARASITER: my base as Excel and a dashboard page")
    ap.add_argument("journal")
    ap.add_argument("--xlsx", action="store_true")
    ap.add_argument("--html", action="store_true")
    ap.add_argument("--out", default=None, help="file name without extension (default: parasite-seo-base next to the journal)")
    ap.add_argument("--lang", default="en", choices=sorted(L))
    ap.add_argument("--platform"); ap.add_argument("--topic")
    ap.add_argument("--priority", choices=wl.PRIORITIES)
    ap.add_argument("--today")
    ap.add_argument("--sales-file")
    a = ap.parse_args()
    if not os.path.exists(a.journal):
        sys.exit(f"Journal not found: {a.journal}")
    today = wl.pdate(a.today) if a.today else date.today()
    both = not a.xlsx and not a.html
    out = a.out or os.path.join(os.path.dirname(os.path.abspath(a.journal)), "parasite-seo-base")
    out = re.sub(r"\.(xlsx|html)$", "", out)
    t = L[a.lang]
    d = collect(a.journal, today, a.sales_file, a.platform, a.priority, a.topic)
    k = d["kpi"]
    xname = None
    if a.xlsx or both:
        xname = out + ".xlsx"
        names = build_workbook(d, t, xname)
        print(f"Excel: {xname} · sheets: {', '.join(names)}")
    if a.html or both:
        b64 = ""
        if xname:
            import base64
            with open(xname, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
        build_html(d, t, a.lang, os.path.basename(xname) if xname else "", out + ".html", b64)
        print(f"Dashboard: {out}.html" + (" (the Excel file is inside the page: its Download Excel button works offline and in an artifact)" if xname else ""))
    print(f"{k['posts']} posts on {k['platforms']} platforms · alive {k['alive']} · indexed {k['indexed']} · "
          f"top {wl.TOP}: {k['top10']} · gone {k['gone']} · not checked {k['unchecked']} · "
          f"{len(d['sales'])} sales rows · {len(d['links'])} links")


if __name__ == "__main__":
    main()
