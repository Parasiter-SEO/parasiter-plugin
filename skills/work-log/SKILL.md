---
name: work-log
description: The user's parasite SEO journal of work, traffic and sales, and their personal inventory of pages and platforms; keeps the publication queue — next pages ranked by what earns (fix, scale, expand, explore). Imports pages they already published and builds their own platform base; records every action, sale (by hand or from affiliate network exports) and traffic; ties sales to pages by sub-ID; gives reports for any day, week or month, effectiveness by page, platform, offer, program and content type, and a queue of pages due for checks. Use when the user uploads or pastes their pages, asks for "my platforms", marks priority pages or platforms, asks which pages are in the top, wants to see or download their base of posts ("open my base", "my posts in Excel"), "what should I write and where", "which topics are missing on X", reports work or a sale, uploads a sales or traffic export, asks "what did I do / earn this week", wants a report, asks what needs checking, or asks about Bing or AI-answer visibility.
---

# Work Log

## Work label (testing period)

Start every reply produced by this skill with one line naming it, so the user always sees which part of PARASITER is working:
`▸ PARASITER · work-log`
If you called agents for this reply, add them after an arrow: `▸ PARASITER · work-log → serp-analyst, product-researcher`. If you hand off to another skill, the next reply carries that skill's label. One line only, no other system talk.

## Plugin basis and Claude plan — RULE (№33)

Every answer here is PARASITER at work: this skill's steps, Rumer's rules, criteria and references — never general knowledge alone. Name the basis briefly where it matters ("by Rumer's rules", the checklist, score or reference used, "PARASITER platform base"). A request this skill doesn't cover → the right skill; nothing fits → one line "outside PARASITER's skills — I answer by Rumer's general rules", then "0 — menu". Full rule: `navigator/references/agents-and-plan.md`.

**Agents and Claude plan.** Heavy step: checking the pages in the check queue → agent `page-checker`. Mode: `agents:` in `parasite-seo-profile.md`, else `agents_default` from `account_info`.
- `on` (Claude Max, Team) → run the agent; label `▸ PARASITER · <skill> → page-checker`.
- `lite` (Claude Pro) → the **Lite version** below, label `▸ PARASITER · <skill> · Lite`. When the full version would clearly give a better result here, add one line of advice — why, and the phrase **full** ("For 20 products the full version is better: page-checker checks every one, about 3–5× more of your Claude limits. Say **full** — or I keep Lite").
- `offer` (plan not known) → ask once before the first run: "This step of the skill is done by PARASITER's page-checker agent: separate context, deeper, uses more of your Claude limits (best on Max). Run it? Or Lite with the same skill."
- "full" / "audit by agent" → run it this time; "turn on agents" → `agents: on`; "save limits" or a usage limit hit → `agents: lite` (save in the profile, advice from `agents-and-plan.md` §3).

**Lite version:** up to 3 pages from the queue checked here, the rest stay in the queue. Lite is the same method in a smaller scope: say what was left out.

## Next steps (end of every reply)

The user must always know what to type next. End every reply with a short numbered block — ready phrases, not skill names:

**What's next? Reply with a number or the phrase:**
1. "<ready phrase>" — <what happens after it, a few words>
2. "<ready phrase>" — <what happens>

- 2–3 options that fit what just happened, the recommended next step first. "1", "yes", "ok", "go" means option 1. Any free wording of the same wish works too ("give me the offers").
- Each option is a complete phrase in the user's working language that they can copy, plus what it does. Never show skill or agent names here: the work label at the top already names the part that is working.
- Offer only what the user's plan includes (`account_info`, once per session). A Pro or Insider feature on a lower plan appears at most once as the last option, marked "(Insider)" or "(Pro)" with one line on what it gives.
- **During first setup** (a step in the profile's `setup:` is still open — not `done`, `skipped` or `not needed`): option 1 is the current setup step, and the setup footer from `navigator` ("First setup checklist") goes under the options — step N of 12, what is done, now, next.
- Things that need no decision (logging, monitoring, saving to the base) are done automatically, not offered.
- **0 — menu (№26):** the last option is always "**0** — menu of all functions". If something is paused (`paused:` in the profile: a day-plan task, a setup step, a draft), option 1 is "**back** to <it>". Never make an option a condition ("first publish…") — every option is an offer.
- **Mark tried:** on this skill's first real run in the session, add or update its line under `tried:` in `parasite-seo-profile.md` (`- <skill> · YYYY-MM-DD · <what, 3–6 words>`; agents too, marked `agent`). When the user seems lost or asks what else there is, add: "All PARASITER functions: say **help**."

Options that usually fit after this part (adapt to the user's products and words):
- "what earns and where to scale?" — report with charts
- "which topics are missing on my strong platforms?"
- "check positions of my new pages" — paid, cost shown first
- "am I cited in AI answers?" / "check my Bing positions" — paid, cost shown first

Part of PARASITER by Rumer (Affiliate Credo).

Parasite SEO is measured in sales, not positions. This skill keeps three things in one place: **what was done** (pages, checks, audits), **what traffic came** (views, affiliate clicks) and **what it earned** (every sale, tied to its page). A page that is in the journal gets checked — alive, still indexed, follows the conversion rules. A sale that is in the journal tells which page, platform, offer and content type actually pay.

Reply in the working language from `parasite-seo-profile.md`. Keep column names and `event` / `status` values in English so the files stay machine-readable.

## Step 0 — Plan check (Pro)

**Step 0 — Plan check.** Call `account_info` once per session (reuse it if already called). Pro or Insider, active → proceed. **Always allowed on any plan, with or without a key (№34):** "export my base", "download my data", "my base in Excel", "open my base" — Mode "Export my base" and the My base dashboard below. The files are the user's own and never live on the server, so a lapsed plan never locks the user out of their own data; run these without the upgrade line. Everything else: Free, expired or no key → one line: "This is a Pro feature — the journal of your pages, sales and traffic, your platform base, sales imports from networks, reports and the check queue. Upgrade: https://parasiter.affiliatecredo.com/#pricing", then offer the Free alternative for this skill (tell the goals tracker what you did — say "I published 3 pages" or "2 sales today" — and it counts them in your weekly plan-vs-fact; keep the page links in your own table meanwhile), and stop.

## Files

In the user's project folder (formats in `references/log-format.md`):
- `parasite-seo-progress.csv` — work journal: pages, checks, audits, traffic, imports (the same file `goals` reads).
- `parasite-seo-sales.csv` — one row per sale, logged by hand or imported.
- `parasite-seo-queue.csv` — the publication queue (Mode 12): next pages ranked by what earns, updated in place.
- `parasite-seo-platforms.csv` — the user's own platform base: one row per platform they publish on (domain, type, language, link rules, account, score, state). Built automatically from their pages; the only file here whose rows are updated in place.

One row per fact. Never edit or delete old rows; corrections and status changes are new rows. If a file has an older, shorter header, the script upgrades the header and keeps every value.

The script `scripts/worklog.py` does all reading, writing and counting. Pass `--date` / `--time` in the user's local time when the machine clock may differ (cloud sandboxes run in UTC). Without code execution, append rows by hand and count the same way.

## Agency and site owner roles — one journal per client or site

For agencies every client has its own folder and journal: `clients/<slug>/parasite-seo-progress.csv` (with its own platforms and links files next to it). Pass that path to every command; the scripts work the same. Never log two clients in one journal.
- **Links library (Mode 10)** holds the client's destination pages with the UTM base (`client-workspace/references/measurement.md`), not affiliate links.
- **Every client page gets a sub-ID equal to its `utm_content`** (`--sub-id md-best-crm`): GA4 exports with "Session manual ad content" then credit visits to the exact page; exports by "Session source / medium" credit the platform.
- **Traffic (Mode 3)** = GA4 visits to the client's site from our pages, platform stats (views, reads, plays) and the client's own channel stats. Search Console exports of the client's site are kept in `clients/<slug>/reports/` for `client-reports`, not imported as page traffic (they describe the client's site, not our pages).
- **Sales** are optional: only when the client shares leads or orders by source. Reports read "—" for sales otherwise.
- The client's own landing pages are journal pages of the platform `own-site` with their target query (`client-workspace/references/measurement.md`), so the position check covers them too.
- **Links to the site** (site owners, and agencies doing link building): log the link each page gives — `add --event published --url … --link-target https://site/page --link-rel dofollow --anchor "acme crm" --cost 150` (`--cost` for paid placements). `backlinks [--period P] [--target URL]`: links live, dofollow per target page, anchors (warns when one exact anchor dominates), spend per live dofollow link. A check that finds the page removed or noindexed takes its link out of "live". Linking rules of each platform go into the platform base: `platform-set --links dofollow|nofollow|ugc|sponsored`.
- **Results on the site:** `import-traffic ga4.csv --from … --to … --medium parasite` takes Sessions, Key events (or Conversions, Transactions) and Purchase revenue per page (Session manual ad content = sub-ID) or platform (Session source); `site-roi [--period month] [--by platform|page]` gives visits, conversions, conversion rate, revenue, spend and return. Revenue is the site's own revenue, not a commission; a dash means not measured.
- Paid checks, page checks, the check queue and Rules below apply per client.

## Mode 0 — Import pages you already have (inventory)

Most users start with pages already live. The first job is to put all of them in the journal, so the system knows the user's inventory of posts and platforms and every page gets checked.

The user uploads or pastes anything with links: a text list, a CSV / TSV, an Excel sheet (save as CSV or convert with the xlsx skill first), a Google Sheet export, notes with URLs mixed in.

```
python3 scripts/worklog.py import-pages parasite-seo-progress.csv my-pages.csv [--date 2026-09-01] [--offer ketox --program ClickBank --campaign keto-pack-sep] [--map url="Post link"]
```

- Columns are found by name: link/URL, published date, platform/site, offer/product, program/network, campaign/pack, sub-ID, keyword, content type, status, notes or title. A column full of URLs is used even without a known header. Plain text: every URL in it is taken.
- The platform comes from the domain (medium.com → `medium`, `*.substack.com` → `substack`, forum.example.com → `example`); known platforms also get a type (article, community, q&a, forum, document, site-builder…).
- Pages already in the journal are not added twice; uploading the list again with more columns (or with `--offer/--program`) fills in what they are missing.
- Dates are not needed and never asked for. An imported base without dates is marked "publish date unknown": it counts as inventory, not as work done on the import day. If the user's file has dates, they are used. A fresh page logged as it is published (Mode 1) simply gets today's date.
- No offer or program → sales can't be counted per offer or program for those pages. Ask per batch, not per page: "These 40 Medium pages — which offer and program?" and re-run the import on the same list with `--offer/--program`, or upload a fuller table: pages already in the journal get only the details they are missing (a `note` row), nothing is duplicated.
- Every new platform goes into the user's platform base (Mode 7).

After the import, report in 4–5 lines: pages added, per platform, new platforms in the base, pages without offer/program. Then offer the first check, because the system knows nothing about the pages' status yet:

- **Alive check** (page opens, not removed, no noindex, affiliate link in place) — free, runs through `platform-monitor` → `page-checker`.
- **Index and position checks need the user's own SEO data account.** Say so plainly: "To check indexing and positions, connect your own SEO API — DataForSEO is recommended (pay per check, Claude runs it itself); if you already have Semrush, Ahrefs, Serpstat or Ubersuggest, connect that or upload its export." Setup: `niche-analysis/references/seo-apis.md`.
- **Before any paid check, warn that it is not free and suggest a sample**: priority (★) pages, pages that earn or get clicks, the newest pack, or one page per topic — not the whole base. Give the rough cost for the chosen number of pages (from `seo-apis.md` and Mode 9 / 9b) and wait for the user's yes. Check the whole base only when the user asks for it after seeing the cost. Imported pages wait in their own queue section until that first check; only then do they get the regular check and audit schedule (audits only for pages that matter: live and indexed, or earning).

## Mode 1 — Log work as you go

Whenever the user reports work, or another skill finishes a step, add the row right away.

| User says / skill finishes | Row (`add --event …`) |
|---|---|
| "Published / added an article: URL" | `published` + platform, offer, program, campaign (pack), sub-ID if any, main query, content type |
| "Sent it to indexing" | `submitted` + `--note "via <service>"` (several: `"via SpeedyIndex + Rapid URL Indexer"`) + `--cost <price per URL>` if known (the recheck comes 4 days later; `index-stats` counts results per service and per mix) |
| platform-monitor / page-checker result | `check` + status live · indexed · not-indexed · noindex · dropped · removed |
| page-audit result | `audit` + score 0–100 |
| "Updated the page" | `refreshed` |
| "Moved it" | `moved` on the old URL + `published` on the new one (new sub-ID) |
| "Registered / tested a platform" | `platform` |
| Other work (research, drafts, images) | `task` + note |

```
python3 scripts/worklog.py add parasite-seo-progress.csv --event published --url https://… --platform medium --offer nordvpn --program "NordVPN (Impact)" --sub-id md-1022-1 --query "nordvpn vs surfshark" --type ab-comparison
```

**Topics from the approved list.** When a `published` page matches a topic in the profile's `topics:` (by platform, title or slug), set that topic to `published <URL>`. Links may arrive in a batch — plain URLs, a list, a message or a screenshot: log them all in one reply, then hand all of them to `indexing` together (one clean list), and put each on the check queue (index at 3–7 days, positions at 14 days).

**Program and campaign on every page.** `program` is the affiliate account the sales come from (must match the import's `--program`); `campaign` is the pack the page belongs to ("keto-pack-oct", 20 articles published together). These two are enough to count every sale. A **sub-ID** is a bonus: where the network supports it, it ties a sale to the exact page. Offer one (`md-1022-1`, see `references/sales-import.md`) but never block or nag — many programs, coupons and merchant sites cannot pass it.

After a `published` row: hand the page to `indexing` by the user's `indexing:` setting in the profile (`instant` → the clean list to send now; `after-check` → indexer only if still out at the recheck; no setting yet → `indexing` Step 0 once). The user sends to indexers themselves. Every page that enters the journal — published, imported (Mode 0) or added from a list — gets its alive checks from the check queue (2, 7, 14 days, then every 14 days); the checks run in the user's Claude (`platform-monitor`), and the page's URL never leaves the project. If the user worked on the text themselves (edited, rewrote, added photos — not a plain AI draft), offer once to save its source with the page (Mode 11): "Save the .docx with this page so you can republish it if it's removed?" Confirm in one line ("Logged: Medium, sub-ID md-1022-1. Alive check Oct 24, index check Oct 26."); for a batch, one short table (page · platform · topic · next check).

## Mode 2 — Log sales

**One sale, by hand** — "made a sale, $42 from the keto article":
```
python3 scripts/worklog.py sale parasite-seo-progress.csv --program ClickBank --commission 42 --sub-id li-1010-1 [--url … --amount 79 --order-id … --status pending]
```
Ask only for program and commission; page (URL or sub-ID) if the user knows it. A manual sale that later appears in an import is matched (same program, commission, ±2 days) and counted once.

**Network export** — the main source of truth: it has every sale, sub-IDs, pending/approved status and refunds. When the user uploads a CSV export:
```
python3 scripts/worklog.py import-sales parasite-seo-progress.csv export.csv --program ClickBank --network ClickBank
```
The script finds the columns (date, order ID, commission, amount, sub-ID, status, product, currency) under the names networks use, handles `,`/`;` files, US/EU dates and decimals, skips rows already imported, records status changes (pending → approved, refunds) as new rows, and logs an `import` row in the journal. If it cannot find a column it prints the file's headers: map them with `--map commission="Your Earnings"` and re-run. Excel export → save as CSV first (or convert with the xlsx skill). PDF or screenshot only → read the sales from it and log them with `sale`, one by one, marking `--note "from screenshot"`.

After an import, report in 3–4 lines: new sales, commission, pending, refunds. If sub-IDs appear that are not in the journal, ask once which page they belong to and add them to that page's `published` row so past and future sales attach.

### Weekly sales upload

The check queue (Mode 5) lists every program with live pages whose sales were not imported or logged for 7 days, and asks for a monthly export even when sales are logged by hand (exports catch refunds and missed sales). The navigator raises it on the first session of the week. Ask plainly: "Upload this week's export from ClickBank and Impact: [date] to today." How to export: `references/sales-import.md`.

### Monday check-in (from the Telegram bot)

Every Monday at 10:00 (Kyiv) the PARASITER bot asks Pro and Insider users with Telegram linked to bring last week's numbers here. The user says **"weekly check-in"** (or "Monday check-in", "here are my sales for the week", or just uploads exports on a Monday). Run it as one short flow:

1. `weekly_checkin` (action `status`) gives the period to log (last Monday–Sunday). Without a key or Telegram, use last Monday–Sunday in the user's time zone.
2. Ask for what they have, in one message, all optional except sales:
   - **Sales** — the export from every program with live pages (`due` lists them), for that period → `import-sales` (Mode 2). Screenshot or PDF → read and log with `sale`.
   - **Traffic** — platform stats (views, plays, clicks) and the network click report → `import-traffic` with `--from/--to` = the period (Mode 3).
   - **UTM / analytics** — GA4 "Session source / medium", utm_source reports, Search Console pages → `import-traffic` the same way.
   Take whatever comes; never block the check-in on a missing file — name what is missing in one line and go on.
3. Report the week: `summary --period last-week` and `effect --period last-week --by platform`, 4–6 lines: sales and commission vs the week before, best page and platform, traffic without sales (→ page-audit), pages that dropped or died (from the latest page check). With a goals file, add the pace line from the `goals` weekly review. Charts and PDF as always (client-reports style) when the user wants the full report.
4. **Offer a position check** to see how keywords and posts moved: "Check positions of ★ / earning / new pages? N pages ≈ $X on your DataForSEO." It is paid — ask which pages and show the cost first, run only after a yes (Mode 9, Rules). If they want it every Monday, set it up with `paid_check_schedule` (they choose pages and cost once; the bot warns before each run).
5. `weekly_checkin` action `done` — the bot then stops nudging for this week. Only the fact "logged" goes to the server, never sales or traffic.

"Turn off Monday check-ins" → `telegram_settings` checkin `off` (or `/checkin off` in the bot); "turn them on" → `on`.

### Sales without a page are normal

Often a sale cannot be tied to an article: the network shows no sub-ID or referrer, the buyer came back days later, or 20 articles of a pack promote the same offer. UTM tags don't solve it either — they land in the merchant's analytics, which the affiliate never sees. So the journal works on three levels and never treats an untied sale as an error:

1. **Exact** — the sale has a page (URL or a known sub-ID).
2. **By program / campaign** — every sale has a program; program, month and campaign totals count all of them exactly. Judge a pack by its total: "20 keto pages, October: 6 sales, $240, $12 per page".
3. **Estimated share** — page, platform, offer, content-type and campaign tables spread untied sales over the pages of the same program that were live at the sale date, weighted by affiliate clicks, else views, else equally. Always labelled as an estimate; use it to see where money *probably* comes from, never report it as fact.

Always show the attribution share ("3 of 12 sales tied to a page"). Ask "which page was it?" only when the user might really know (a single sale on a fresh page); never require it.

Ways to tie more sales, where the platform and network allow (offer once, don't push):
- sub-ID per page, or at least per platform or per pack;
- Amazon and programs without sub-IDs: a separate tracking ID per platform or pack;
- a unique coupon code per platform or pack, when the merchant gives codes;
- affiliate clicks per page from the network's click report — even without sale attribution, clicks make the estimate much better.
Redirect links through the user's own domain count clicks per page, but some platforms remove or penalise redirects and shorteners — warn before suggesting them.

## Mode 3 — Traffic

Views and clicks are what turn sales into conversion. Take any traffic data the user has — file, screenshot or a number — at any level:
- **Per page** — platform stats (Medium, LinkedIn, Gamma analytics, podcast plays, YouTube, forum views), Search Console, GA4 landing pages, network clicks by sub-ID: `import-traffic export.csv --platform medium --from 2026-10-01 --to 2026-10-21`. Matching by page URL or sub-ID.
- **Per platform** — network click reports grouped by referrer (Post Affiliate Pro, Everflow `referer`), GA4 "Session source / medium", utm_source: the same `import-traffic`; a referrer that is a logged page credits that page, a referrer domain of one of the user's platforms credits the platform. A whole-platform total with no page column: `--platform gamma`.
- **No referrer / direct** — reported in the import summary, not tied to anything.
- From a screenshot: read it into a small table, show it to the user, then `add --event traffic --url … --views 1200 --date <period end> --note "traffic 2026-10-01..2026-10-21"` (or `--platform X` with no URL for a platform total).

Sources the import does not recognise (a referrer domain that is not one of the user's platforms) are listed: offer to add them to the platform base — that is often a page or platform the user forgot to log. Where each network and platform keeps its reports: `references/sales-import.md`.

Always pass the export's date range: the same page or platform and period are never counted twice. Traffic is dated at the end of its period.

## Mode 4 — Reports

**Work report** — "what did I do today / this week / in September": `summary --period <period>` (`today`, `yesterday`, `week`, `last-week`, `month`, `last-month`, `YYYY-MM`, `YYYY-MM-DD`, `YYYY-MM-DD..YYYY-MM-DD`, `all`). It shows: work done, sales and commission, traffic, comparison with the previous period, work by day, pages published with their status now, pages that earned, and what needs attention.

**Effectiveness** — "what earns", "which platforms/offers work", "is the system paying off": `effect --period <period> --by page|platform|offer|program|campaign|content_type|month`. Per group: pages, views, affiliate clicks, sales, commission, pending, EPC, conversion, commission per page, per 1,000 views. `--by program`, `--by month` count every sale exactly; page-level views show exact sales plus the estimated share. `--by month --period all` shows the trend since the baseline — the clearest answer to "is the system paying off".

Read the table for the user in 3–5 lines: what earns most per page, what gets traffic but no sales (→ page-audit: first screen, CTA, intent), what gets nothing after 30–60 days (→ reposition or drop), which content type and platform to do more of. Compare with the baseline in `parasite-seo-goals.md` when it exists. Deeper client-facing reports: `client-reports`.

## Mode 5 — Check queue

"What needs checking?" or at session start (the navigator asks): `due`. It lists, most urgent first:
- **Sales reports to upload** — per program, with the date range to export.
- **Removed / noindex** — republish from the saved copy, log `moved`.
- **Not indexed 14+ days** — resubmit, add links, or move.
- **Alive check due** (free: page opens, no noindex, link in place) — 2, 7, 14 days after publishing, then every 14 days.
- **Index / position check suggested** (paid) — new pages not yet indexed, ★ pages, earning pages, pages that dropped. The queue only *suggests* them; nothing paid runs from the queue on its own (see Rules: paid checks).
- **Audit score under 70** — improve with page-audit, log `refreshed` + new `audit`.
- **Audit due** — never audited, refreshed since, or 14/30/60-day review.
- **Optional: no sub-ID** — shown only in the full queue; sales are still counted by program.

Checks of more than 3 URLs go to the `page-checker` agent (via platform-monitor); every result is logged as `check`.

## Mode 6 — Page registry

`pages [--platform medium]` — every page with platform, offer, sub-ID, age, status, audit score, views, affiliate clicks, sales and commission.

## Mode 6b — My base: open it and download it

The base is the user's asset, so they can look at it nicely and take it with them. Three ways, picked by the words they use:

| User says | Give |
|---|---|
| "show my posts", "my pages on Medium", "which pages are in the top" | a short answer in the chat: `pages` (filters `--platform`, `--topic`, `--priority`), 10–20 rows, the rest summed up |
| "open my base", "show my base nicely", "dashboard of my posts", "I want to see all my posts" | the dashboard page |
| "download / export / send me my posts", "my base in Excel", "a table of my posts" | the Excel file (the dashboard too, unless they only asked for the file) |

```
python3 scripts/mybase.py parasite-seo-progress.csv --lang ru [--out parasite-seo-base] [--platform medium] [--priority high] [--topic keto]
```
Writes, next to the journal:
- `parasite-seo-base.xlsx` — sheets **Summary** (totals, status by platform), **Posts** (one row per page as it stands today: published, link, platform, topic, ★, offer, program, campaign, sub-ID, main query, content type, status, position, best position, last check, audit, views, affiliate clicks, sales, commission, age, saved source; plus link target and rel when pages link to the user's own site), **Platforms**, **Sales**, **Links**, **Journal** (every event as logged). Header frozen, filters on, links clickable, dates and numbers are real Excel values, top-10 positions highlighted. Opens in Excel, Google Sheets (File → Import), Numbers and LibreOffice.
- `parasite-seo-base.html` — the dashboard: totals (posts, ★, platforms, alive, indexed, top 10, need attention, sales and commission per currency), status of posts by platform, and tabs Posts · Platforms · Sales · Links with search, filters (platform, status, topic, offer, ★ only, top 10 only) and sorting by any column. Buttons **Download Excel** (the workbook is inside the page) and **CSV of this view** (exactly the rows the filters show). Light and dark, works on a phone.

`--lang` = the working language from `parasite-seo-profile.md` (en, ru, uk, es, pt; other languages get English labels). Labels and statuses are translated, the data never is. `--xlsx` or `--html` writes only one of them; `--platform / --priority / --topic` narrow the Posts sheet and the page table. The script only reads the journal files.

### Export my base — keep everything (any plan, no key needed)

"export my base", "download all my data", "back up my base", "I'm cancelling — what about my data?", or a lapsed / Free user asking for their journal:

```
python3 scripts/export.py parasite-seo-progress.csv --lang ru
```
One zip next to the journal, `parasite-seo-export-YYYY-MM-DD.zip`: `original/` — every PARASITER file byte for byte (journal, sales, platforms, links, keywords, profile, goals, writer notes); `parasite-seo-base.xlsx` — the same data as Excel; `README.txt` — what each file is, how to bring the base back, SHA-256 checksums. Reads only, works without a journal too (exports whatever PARASITER files exist).

Send the zip as a file. Then say in 2 lines: the base always lives in their own folder and never on the PARASITER server, so ending a plan deletes nothing of it; after renewal (same key within 30 days of the end) or a new plan PARASITER continues from the same files. Offer once: "Want a monthly backup reminder?" (a scheduled task in their Claude, if they agree).

When the user says they're switching plan (Insider → Pro, Pro → Insider): nothing to move — files stay, the key stays the same (see help, "Change plan").

Delivering:
- **Claude app / claude.ai** (can publish pages): publish the `.html` as a private artifact with `capabilities: {"downloads": true}` — without it the download buttons are hidden. Keep the same artifact for the user's base and republish it to the same URL when they ask again, so the link stays. Also send the `.xlsx` as a file when they asked for Excel.
- **Claude Code** (no publishing): give both file paths; the `.html` opens in any browser with working buttons.
- Agencies: run it on the client's journal (`clients/<slug>/parasite-seo-progress.csv`) with `--out clients/<slug>/reports/<yyyy-mm>/base`; never mix clients in one base. It is the full inventory, so it can go to the client as an attachment to the monthly report.

Reply in 2–3 lines: what the base holds now (posts, platforms, alive, top 10, need attention) and one thing to act on from it (for example "4 pages not checked yet — check them now?"). Never retype the table in the chat.

## Mode 7 — My platform base

"My platforms", "where do I publish", "which platforms work for me": `platforms`. One row per platform the user has used: domain, type, state, pages, alive, indexed, gone, not checked, last page, sales, commission, score. It flags platforms where half or more of the checked pages are gone, and platforms with no type yet (→ `platform-analyzer` once).

The user can also give the list of all domains they publish on first (`platform-set` per domain): platforms with no pages yet are listed as "send their lists" in `platforms`, and the navigator reminds once per session until each list arrives or the platform is marked `paused`/`dropped`.

The base fills itself: from `import-pages`, from every `published` page logged later on a new platform, and from `platform` events. Facts the user or another skill learns go in with `platform-set`:

```
python3 scripts/worklog.py platform-set parasite-seo-progress.csv --platform healthboards --type forum --links nofollow --language en --account "rumer_k (aged 2y)" --score 72 --state active
```

States: `active` (publishing), `testing` (1–3 test posts), `paused`, `dropped` (stopped: died, cleaned up, no traffic), `dead` (platform gone). Never write logins or passwords here — an account name is enough.

Other skills use the base: `platform-finder` excludes or marks platforms already in it, `platform-analyzer` writes its score and verdict back with `platform-set`, the navigator prefers `active` platforms with live, indexed pages for new posts.

## Mode 9b — What each page ranks for, and what it lost

`scripts/pagekeywords.py` (run through `dataforseo_run`, script `pagekeywords`) asks DataForSEO Labs, page by page (full URL, never the bare domain — a domain target returns the whole site), which queries the page ranks for, their volume and estimated traffic, and which queries it lost and when. One page ≈ $0.013–0.02.
```
python3 scripts/pagekeywords.py parasite-seo-progress.csv [--priority high] [--platform medium] [--dry-run]
```
Results: `parasite-seo-keywords.csv` (page × keyword) and a `check` row per page (best position, "labs: N keywords, M in top 10, ~V visits/mo, L lost"). Use it to find the pages that really bring traffic, the queries lost before a sales drop, and proven topics for `ideas` / coverage. Labs is a crawl snapshot (each keyword shows when it was last seen); confirm today's positions for the main queries with `rankcheck.py`.

## Mode 10 — Affiliate links library (basic setup)

Part of the first setup, together with the pages and platforms: the user's affiliate links for every product they promote. Articles take the link from here, so the writer never has to ask, and the library shows which products have no pages yet.

The user gives them any way: a list of links, a table (product, link, program, commission), screenshots of the network's "my links" page (read the links from the image and write them into a list first; ask about links cut off in the image), or one at a time ("my link for X is …").
```
python3 scripts/worklog.py import-links parasite-seo-progress.csv links.csv --program VitaBrand --commission 40%
python3 scripts/worklog.py links parasite-seo-progress.csv [--program VitaBrand]
```
- One row per link in `parasite-seo-links.csv` (program, product, link, alt_links, commission, added, note). Product names come from a product column, else from the link (`/omega-3-fish-oil` → "omega 3 fish oil"); store and category pages are kept as "(store page) …" for "shop all" CTAs. Already known links are skipped.
- Several links for one product (drops, softgels, bundle page) → give them the same product name; the first is the main link.
- `links` lists every product with its link, how many live pages already cover it and on which platforms, and ends with **products with no pages yet** — the topics to write. Pick the platform with `ideas` / `coverage`.
- After a new import, offer once: "N products have no pages — want a plan for them?"
- These are the user's links: never replace them with other links, never shorten or cloak them; the platform's rules on affiliate links apply.

## Mode 11 — My reviews: sources kept with their pages

The user keeps the texts they really worked on (most people work in .docx) next to the published page, so a removed page or a whole platform cleanup costs minutes, not days.
```
python3 scripts/worklog.py source parasite-seo-progress.csv --url https://… --file "Flexotone review final.docx" [--note "v2 with my photos"]
python3 scripts/worklog.py republish parasite-seo-progress.csv --platform medium [--gone-only]
python3 scripts/worklog.py republish parasite-seo-progress.csv --url https://…
```
- `source` copies the file into `parasite-seo-sources/` next to the journal (named date-platform-topic) and links it to the page. A newer source for the same page replaces the old one in lists; files are never deleted.
- Only the user's own worked texts are worth saving. A plain AI draft is quicker to write again than to store — say so if the user asks to save every draft.
- `republish` lists the user's pages on a platform (or one page) with status, topic, offer, position, earnings and the saved source; ★ and earning pages first. After a removal or a cleanup: each page is rewritten for its new home (new title and angle, the platform's format, current prices) from its source, or rebuilt from the topic and facts when there is none; pick the new home with `rollout --url` or platform-finder, then log the new page as `published` and the old one as `moved`.

## Mode 8 — Topics, priorities, top positions and what to write where

The base is not only a list: it tells the user where each topic stands and where it is missing.

**Topics.** A topic groups pages on the same subject across platforms ("keto gummies review", "nordvpn vs surfshark"). It is the page's `topic`, else its main query, else offer + content type, else words guessed from the URL (shown with `~`). After an import, propose topic names from URLs and titles in batches and confirm with the user, then set them:
```
python3 scripts/worklog.py tag parasite-seo-progress.csv --match keto --topic "keto gummies review"
python3 scripts/worklog.py tag parasite-seo-progress.csv --urls-file batch.txt --topic "glp1 patch review"
```
`tag` works on `--url` (repeatable), `--urls-file`, `--platform` or `--match` (text in URL or topic) and can also set `--offer --program --campaign --query --type --position`. Latest tag wins.

**Priorities.** The user marks what matters most: `tag … --priority high|normal|low` for pages and topics, `platform-set --platform medium --priority high` for platforms. Priority pages come first in the check queue and page list (★), priority platforms and topics weigh more in the advice below. Ask once after the import: "Which platforms and which pages are your main ones?"

**Top positions.** Every check can carry the page's position for its main query (`add --event check … --position 4`, or `tag --position` from a rank tracker / Search Console export). Top 10 is shown in bold in `pages` (`--priority high`, `--topic …` filters), counted per platform in `platforms`, and is the strongest proof that a topic works. Ask for positions when the user has a rank tracker or Search Console; never guess them.

**Coverage — what to write where.** `coverage` builds a matrix of topics × platforms (position, indexed, live, not indexed, lost, missing) and then lists the best gaps: a proven topic (top 10, earning, indexed or priority) missing on a strong platform (priority, pages in the top 10, high index rate, sales, analyzer score; platforms losing pages and dropped/dead/paused ones are pushed down or skipped). Each gap says why: "#4 on medium; healthboards has 2 pages in the top 10".
```
python3 scripts/worklog.py coverage parasite-seo-progress.csv [--topic keto] [--platform quora] [--gaps 10] [--by-platform]
```
`--by-platform` answers "which of my topics are missing on each of my top platforms": per platform, in the user's own order, the topics they already have elsewhere. The user's order of platforms ("Medium is my #1") goes in with `platform-set --rank 1`; it outweighs every other signal.
Read it to the user as 3–5 concrete suggestions: topic → platform → why → the content type to use there. A new page on a topic must be rewritten for the platform (new angle or content type, the platform's format), never copied — duplicates get filtered and hurt both pages. Hand the chosen gap to `content-type-selector` and `sales-review-writer`. The navigator uses this list for "new content" in the daily plan.

## Mode 12 — Publication queue: what to publish next, ranked by what earns

"What should I write and where?", "plan me topics", "add them to the plan", "what can I scale?", "which products haven't I tried?" → the queue. It turns the whole base — pages, positions, sales, traffic, links — into one ranked list of next pages, so the user never starts from a blank page and the plan always comes from their own numbers.
```
python3 scripts/pubqueue.py build parasite-seo-progress.csv        # refresh from the base
python3 scripts/pubqueue.py list  parasite-seo-progress.csv [--bucket scale|expand|explore|fix] [--n 15]
python3 scripts/pubqueue.py today parasite-seo-progress.csv --minutes 120 [--json]
python3 scripts/pubqueue.py plan  parasite-seo-progress.csv --ids 3,5 [--date 2026-11-07]   (or --next 3)
python3 scripts/pubqueue.py set   parasite-seo-progress.csv --id 7 --status skipped|writing|published [--url …]
python3 scripts/pubqueue.py mix   parasite-seo-progress.csv 70,20,10
python3 scripts/pubqueue.py review parasite-seo-progress.csv
```
File `parasite-seo-queue.csv` next to the journal (one row per item, updated in place); the mix in `parasite-seo-queue-settings.json`.

**Four buckets, each item with its reason:**
- **Fix & push** — money pages first: positions 4–20 → refresh to reach the top 3 / top 10 (Rumer: sales start in the top 3); 100+ views or 5+ affiliate clicks in 60 days and no sales → page-audit. At most 2 a day ahead of new pages.
- **Scale** — a proven topic (top 10, earning or ★) missing on a strong platform (the `coverage` gaps, weighted by what the offer and content type earn). Topics that are only indexed wait for data. A page removed from a platform comes back as "republish".
- **Expand** — what the user sells but hasn't tried: products from the links library with no pages (programs that already pay first), and earning offers written in only one or two content types → the next buyer intents (A vs B, complaints, pricing, experience, best-of).
- **Explore** — sister products of a program that pays (→ affiliate-finder), a new platform while the base is under Rumer's rule of 10 (→ platform-finder, the user picks).

**Mix.** New pages come in the user's proportion, default **70 / 20 / 10** (scale / expand / explore); "more experiments" / "only what works" → `mix`. Scores (0–100) rank items within their bucket.

**The loop.** Run `build` after every import of pages, sales, traffic or positions (and in the Monday check-in). It adds new items, refreshes scores, retires items that are no longer relevant, and marks queue items **published** by itself when a matching page appears in the journal (same platform and topic, logged after the item). `review` shows what the queue brought — earning, top 10, commission per bucket; those pages then weigh content types, offers and platforms in the next `build`. "Skip #N" hides an item for 30 days; it comes back only if still relevant.

**How to show it.** `today` / `list` → 3–8 items, one line each: topic → platform · content type · ~minutes · why — then "Which go into the plan? Reply with numbers." The numbers go to `plan`. The user's platform choice rules (navigator): `today` uses only ★ platforms when the user has marked any; other items stay in the queue. A chosen write item → content-type-selector → sales-review-writer (a new angle for the platform, never a copy), then `add --event published` as usual — the queue links itself. No data yet (a new user) → nothing to rank: say so in one line and go to content-type-selector with the user's offers.

## Mode 8b — Topics for the user's own plan

When the user says what they will publish today and where, `ideas` answers per target platform:
```
python3 scripts/worklog.py ideas parasite-seo-progress.csv --to medium,linkedin [--n 8]
python3 scripts/worklog.py ideas parasite-seo-progress.csv --to thermaltake --from own-site --top-only
```
`--to` takes any platforms, including new ones not in the base. `--from` limits the source topics to platforms or types (`own-site` = the user's own sites, registered with `platform-set --type own-site`; their positions come from the position check, Search Console or a tracker export). `--top-only` keeps only topics with a page in the top 10.

## Mode 8c — Roll a topic out to every platform

`rollout --topic "keto gummies review"` (or `--url <page just published>`): the user's active platforms that don't have this topic yet, in the user's order (rank, ★ first), with the format each platform needs. Run it after every new page (sales-review-writer Step 7) and when the user says "I wrote about X".

## Mode 9 — Positions of every page, automatically (DataForSEO)

**How paid scripts run:** every DataForSEO call goes through the `dataforseo_run` tool of the bundled `parasiter-dataforseo` server (script + the same args as below, `cwd` = the folder with the user's files); it takes the login and password from the plugin settings. `--dry-run`, `--from-json`, `--from-raw` and `--self-test` are free and may also run directly with python3. `dataforseo_status` says whether DataForSEO is set up and shows the balance.

Search Console and free webmaster tools only see sites the user owns, so they can't see parasite pages. PARASITER checks Google itself through the user's own DataForSEO account (pay per request, from about $0.0006 per query: 50 queries a week cost cents a month).

```
python3 scripts/rankcheck.py parasite-seo-progress.csv --dry-run            # what will be checked and the cost
python3 scripts/rankcheck.py parasite-seo-progress.csv [--country us] [--priority high] [--platform medium]
```

- Besides organic positions, every SERP block is read: a page cited in the **AI Overview**, "Discussions and forums", images or videos is logged as indexed with "cited in …" even when it is not in the organic list (parasite pages often live there). The output lists these citations.
- Default: Google desktop, US, top 30 (billed per 10 results; top 30 is where traffic is). `--device mobile` for the mobile SERP, `--depth 100` for a full check, `--country uk` etc. Positions differ by country, device and exact wording (extender ≠ extenders): when the user sees a different position, check the exact query, country and device before doubting the tool.
- One request per unique query covers every page of the user that ranks for it (two platforms on one query = one request). The query is the page's main query, else its named topic; pages with neither are listed — set them with `tag --query`.
- Found pages get a `check` row with their position and status `indexed`; pages not in the top 100 get "not in top 100". The output lists changes since the last check: new in the top 10, up, down, out.
- Standard queue by default (cheapest, results in a few minutes); `--live` answers at once for about 3× the price. DataForSEO bills per 10 results, so the top 100 costs 10× the top 10: use `--depth 10` (or 30) when only the top matters. Before **every** run: ask which pages and how many, show the `--dry-run` cost, wait for a yes (Rules: paid checks).
- Tasks not downloaded in time (or after an error) are already paid: `--collect 24` downloads them for free; `--skip-today` re-runs only pages not checked today.
- Credentials: the user's API login and password (app.dataforseo.com → API Access) go only into the plugin settings (/plugin → PARASITER → configure options → DataForSEO API login / password); the password is kept in secure storage. Never ask for them in the chat and never write them into any file, profile or journal. If `dataforseo_status` says it is not set up, give the user these steps once. If the assistant's sandbox blocks the network, the user allows `api.dataforseo.com` in their assistant's settings.
- Weekly is enough; after a Google update, suggest a run the same day.
- **Scheduled paid check** — only if the user asks for it. Set it up with the user: day and time, which pages (★, earning, new not yet indexed, a platform, a list), how many, and the cost per run from a `--dry-run`; if the user has ★ pages, also the "only ★" count and cost. Register it with `paid_check_schedule` (action=set; list / cancel to review or stop it). The server warns the user in Telegram ahead of every run (the day before, or that morning — always 6+ hours): *"Tomorrow at 10:00: position check of 61 earning pages, ~$0.12 from your SEO API balance"* with buttons **Run as planned · Only ★ · Skip this time · Change** (after Change, a text message sets the new pages).
  The assistant's scheduled task calls `paid_check_pending` (id) right before the run and does exactly what it returns: `run: true` → run that set; `run: false` → don't run, say why in the next session; `run: "if_within_cost"` → work out the pages the user wrote, dry-run, and run only if the cost is not above `cost_limit_usd`, else wait for a yes. No answer in Telegram = run as planned; a run the user was not warned about never runs. After the run, `paid_check_report` sends the result and the real cost to the user's Telegram.
  Without the server or a linked Telegram there is no way to warn the user, so scheduled paid checks are not offered: the check is suggested in the next session and runs after a yes.
- Any rank tracker instead (Ubersuggest, SE Ranking, ProRankTracker, SEO PowerSuite…): upload its CSV export — `import-ranks parasite-seo-progress.csv export.csv`. Rows are matched by URL, else by keyword to the page's query or topic. If the tracker shows another page of the same platform ranking (trackers follow a domain, and medium.com or linkedin.com is everyone's domain), the row is skipped, never credited to the user. Weekly export = weekly history.
- Single positions from the user's own notes: `tag --position` (or `add --event check --position`).

### Mode 9c — Bing positions and AI answers (beyond Google)

Traffic is no longer Google only: ChatGPT search and Copilot lean on Bing results, and AI answers (Google AI Mode, Gemini, ChatGPT) cite a few sources per query, very often user platforms. Both checks are paid from the user's DataForSEO balance, same rules as Mode 9 (which pages, `--dry-run` cost, a yes before every run), and run through `dataforseo_run`.

```
python3 scripts/rankcheck.py parasite-seo-progress.csv --engine bing --dry-run       # Bing positions, same options as Google
python3 scripts/aicheck.py parasite-seo-progress.csv --dry-run                         # Google AI Mode (default)
python3 scripts/aicheck.py parasite-seo-progress.csv --engines ai_mode,chatgpt,gemini --priority high
```

- **Bing** (`rankcheck --engine bing`): Bing positions go into the journal as notes ("bing #4"), never into the Google position column; `pages` shows them as "B 4". A page strong in Bing but weak in Google is a ChatGPT/Copilot asset — say so.
- **AI answers** (`aicheck`): for each page's query, the answer of Google AI Mode (closest to Google; default), ChatGPT and/or Gemini, about $0.0012 per query per engine. Each page gets one of: **cited** (the page itself is a source), **platform cited** (another page of the same platform is a source — the AI trusts this platform for the query: a good sign to publish there and improve the page), **not cited**. The output also lists other domains the AIs cite for the user's queries — platform ideas to check with `platform-analyzer` before posting.
- AI answers change from run to run: one check is a sample. Compare monthly on the same queries, not day to day. Start with ★ or earning pages and AI Mode only; add ChatGPT and Gemini when the user wants the full picture.
- Not cited but the page ranks in Google or Bing → run `page-audit`: its **AI-ready** line says what to add (answer first, facts with dates, named comparison table, Q&A).
- The user's **own site** (site owners, agencies): Bing Webmaster Tools → AI Performance shows how often Copilot cites the site and for which queries; the CSV exports can be uploaded to `client-reports`. Parasite pages live on other people's domains, so this report and IndexNow only work for sites the user owns.

## Rules

- **Queue after data.** After any import (pages, sales, traffic, ranks) or a position check, run `pubqueue.py build` without asking and add one line to the import report: "Queue: N new — say *what should I write next?*".
- **Legal products and content only.** PARASITER works only with legal products and content. Don't write, plan, find platforms for or log pages that promote pirated software, films, books or courses, file-upload / download or "free download" schemes, cracks and keygens, counterfeit or illegal goods, or content that breaks the target platform's rules or the law of the target country. Say so in one line, without lecturing, and offer a legal alternative (the official product or a legal affiliate offer). This rule is part of the PARASITER offer the user accepted.
- **Paid checks only with the user's yes, every time.** Index checks, position checks (Mode 9), page keywords (Mode 9b) and any other call that spends the user's SEO API balance: before each run ask **how many pages and which** — ★ pages, earning pages, new pages not yet indexed, one platform, or the user's own list — show the rough cost for that number (`--dry-run`), and run only after a clear yes. Never run them silently from the check queue, the daily plan or the weekly review, and never extend an earlier yes to a new run or a bigger set. A scheduled weekly run exists only if the user set it up themselves with the pages and the cost shown. The user must always know what they are paying for.
- **★ pages.** Offer the user to star their main pages (`tag --priority high`) after the import; ★ pages are the default proposal for every paid check.

- Facts only. Never mark a page indexed or alive without a check result; never record a sale the user did not report or export.
- Commission is what counts; reversed sales are shown but not counted, refunds subtract. Pending is shown separately.
- Money stays in its currency; do not convert unless the user gives a rate.
- No income forecasts in reports; label any estimate.
- Exports contain customer data: keep only the columns the journal needs and keep the files in the user's project. Never send them to third-party services.
- If a period looks empty, say so and ask whether something was not logged — do not fill gaps.
