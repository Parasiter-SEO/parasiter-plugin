---
name: work-log
description: The user's parasite SEO journal of work, traffic and sales, and their personal inventory of pages and platforms. Imports pages they already published and builds their own platform base; records every action, sale (by hand or from affiliate network exports) and traffic; ties sales to pages by sub-ID; gives reports for any day, week or month, effectiveness by page, platform, offer, program and content type, and a queue of pages due for checks. Use when the user uploads or pastes their pages, asks for "my platforms", marks priority pages or platforms, asks which pages are in the top, "what should I write and where", "which topics are missing on X", reports work or a sale, uploads a sales or traffic export, asks "what did I do / earn this week", wants a report, or asks what needs checking.
---

# Work Log

## Work label (testing period)

Start every reply produced by this skill with one line naming it, so the user always sees which part of PARASITER is working:
`▸ PARASITER · work-log`
If you called agents for this reply, add them after an arrow: `▸ PARASITER · work-log → serp-analyst, product-researcher`. If you hand off to another skill, the next reply carries that skill's label. One line only, no other system talk.

Part of PARASITER by Rumer (Affiliate Credo).

Parasite SEO is measured in sales, not positions. This skill keeps three things in one place: **what was done** (pages, checks, audits), **what traffic came** (views, affiliate clicks) and **what it earned** (every sale, tied to its page). A page that is in the journal gets checked — alive, still indexed, follows the conversion rules. A sale that is in the journal tells which page, platform, offer and content type actually pay.

Reply in the working language from `parasite-seo-profile.md`. Keep column names and `event` / `status` values in English so the files stay machine-readable.

## Files

In the user's project folder (formats in `references/log-format.md`):
- `parasite-seo-progress.csv` — work journal: pages, checks, audits, traffic, imports (the same file `goals` reads).
- `parasite-seo-sales.csv` — one row per sale, logged by hand or imported.
- `parasite-seo-platforms.csv` — the user's own platform base: one row per platform they publish on (domain, type, language, link rules, account, score, state). Built automatically from their pages; the only file here whose rows are updated in place.

One row per fact. Never edit or delete old rows; corrections and status changes are new rows. If a file has an older, shorter header, the script upgrades the header and keeps every value.

The script `scripts/worklog.py` does all reading, writing and counting. Pass `--date` / `--time` in the user's local time when the machine clock may differ (cloud sandboxes run in UTC). Without code execution, append rows by hand and count the same way.

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
| "Sent it to indexing" | `submitted` |
| platform-monitor / page-checker result | `check` + status live · indexed · not-indexed · noindex · dropped · removed |
| page-audit result | `audit` + score 0–100 |
| "Updated the page" | `refreshed` |
| "Moved it" | `moved` on the old URL + `published` on the new one (new sub-ID) |
| "Registered / tested a platform" | `platform` |
| Other work (research, drafts, images) | `task` + note |

```
python3 scripts/worklog.py add parasite-seo-progress.csv --event published --url https://… --platform medium --offer nordvpn --program "NordVPN (Impact)" --sub-id md-1022-1 --query "nordvpn vs surfshark" --type ab-comparison
```

**Program and campaign on every page.** `program` is the affiliate account the sales come from (must match the import's `--program`); `campaign` is the pack the page belongs to ("keto-pack-oct", 20 articles published together). These two are enough to count every sale. A **sub-ID** is a bonus: where the network supports it, it ties a sale to the exact page. Offer one (`md-1022-1`, see `references/sales-import.md`) but never block or nag — many programs, coupons and merchant sites cannot pass it.

After a `published` row: offer page-audit if the page has no audit; with the server (Pro) call `monitor_track` (URL, main query, platform); remind once per session to keep a copy of the text. Confirm in one line ("Logged: Medium, sub-ID md-1022-1. Index check Oct 24. Audit now?").

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

`scripts/pagekeywords.py` asks DataForSEO Labs, page by page (full URL, never the bare domain — a domain target returns the whole site), which queries the page ranks for, their volume and estimated traffic, and which queries it lost and when. One page ≈ $0.013–0.02.
```
python3 scripts/pagekeywords.py parasite-seo-progress.csv [--priority high] [--platform pressbooks] [--dry-run]
```
Results: `parasite-seo-keywords.csv` (page × keyword) and a `check` row per page (best position, "labs: N keywords, M in top 10, ~V visits/mo, L lost"). Use it to find the pages that really bring traffic, the queries lost before a sales drop, and proven topics for `ideas` / coverage. Labs is a crawl snapshot (each keyword shows when it was last seen); confirm today's positions for the main queries with `rankcheck.py`.

## Mode 10 — Affiliate links library (basic setup)

Part of the first setup, together with the pages and platforms: the user's affiliate links for every product they promote. Articles take the link from here, so the writer never has to ask, and the library shows which products have no pages yet.

The user gives them any way: a list of links, a table (product, link, program, commission), screenshots of the network's "my links" page (read the links from the image and write them into a list first; ask about links cut off in the image), or one at a time ("my link for X is …").
```
python3 scripts/worklog.py import-links parasite-seo-progress.csv links.csv --program NUTRAHARMONY --commission 40%
python3 scripts/worklog.py links parasite-seo-progress.csv [--program NUTRAHARMONY]
```
- One row per link in `parasite-seo-links.csv` (program, product, link, alt_links, commission, added, note). Product names come from a product column, else from the link (`/omega-3-fish-oil` → "omega 3 fish oil"); store and category pages are kept as "(store page) …" for "shop all" CTAs. Already known links are skipped.
- Several links for one product (drops, softgels, bundle page) → give them the same product name; the first is the main link.
- `links` lists every product with its link, how many live pages already cover it and on which platforms, and ends with **products with no pages yet** — the topics to write. Pick the platform with `ideas` / `coverage`.
- After a new import, offer once: "N products have no pages — want a plan for them?"
- These are the user's links: never replace them with other links, never shorten or cloak them; the platform's rules on affiliate links apply.

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

## Mode 8b — Topics for the user's own plan

When the user says what they will publish today and where, `ideas` answers per target platform:
```
python3 scripts/worklog.py ideas parasite-seo-progress.csv --to researchgate,pressbooks [--n 8]
python3 scripts/worklog.py ideas parasite-seo-progress.csv --to thermaltake --from own-site --top-only
```
`--to` takes any platforms, including new ones not in the base. `--from` limits the source topics to platforms or types (`own-site` = the user's own sites, registered with `platform-set --type own-site`; their positions come from the position check, Search Console or a tracker export). `--top-only` keeps only topics with a page in the top 10.

## Mode 8c — Roll a topic out to every platform

`rollout --topic "lymphatic drainage drops"` (or `--url <page just published>`): the user's active platforms that don't have this topic yet, in the user's order (rank, ★ first), with the format each platform needs. Run it after every new page (sales-review-writer Step 7) and when the user says "I wrote about X".

## Mode 9 — Positions of every page, automatically (DataForSEO)

Search Console and free webmaster tools only see sites the user owns, so they can't see parasite pages. PARASITER checks Google itself through the user's own DataForSEO account (pay per request, from about $0.0006 per query: 50 queries a week cost cents a month).

```
python3 scripts/rankcheck.py parasite-seo-progress.csv --dry-run            # what will be checked and the cost
python3 scripts/rankcheck.py parasite-seo-progress.csv [--country us] [--priority high] [--platform researchgate]
```

- Besides organic positions, every SERP block is read: a page cited in the **AI Overview**, "Discussions and forums", images or videos is logged as indexed with "cited in …" even when it is not in the organic list (parasite pages often live there). The output lists these citations.
- Default: Google desktop, US, top 30 (billed per 10 results; top 30 is where traffic is). `--device mobile` for the mobile SERP, `--depth 100` for a full check, `--country uk` etc. Positions differ by country, device and exact wording (extender ≠ extenders): when the user sees a different position, check the exact query, country and device before doubting the tool.
- One request per unique query covers every page of the user that ranks for it (two platforms on one query = one request). The query is the page's main query, else its named topic; pages with neither are listed — set them with `tag --query`.
- Found pages get a `check` row with their position and status `indexed`; pages not in the top 100 get "not in top 100". The output lists changes since the last check: new in the top 10, up, down, out.
- Standard queue by default (cheapest, results in a few minutes); `--live` answers at once for about 3× the price. DataForSEO bills per 10 results, so the top 100 costs 10× the top 10: use `--depth 10` (or 30) when only the top matters. Before **every** run: ask which pages and how many, show the `--dry-run` cost, wait for a yes (Rules: paid checks).
- Tasks not downloaded in time (or after an error) are already paid: `--collect 24` downloads them for free; `--skip-today` re-runs only pages not checked today.
- Credentials: the user's API login and password (app.dataforseo.com → API Access) in the environment as `DATAFORSEO_LOGIN` / `DATAFORSEO_PASSWORD`. Never write them into any file, profile or journal. If the assistant's sandbox blocks the network, the user allows `api.dataforseo.com` in their assistant's settings.
- Weekly is enough; after a Google update, suggest a run the same day.
- **Scheduled paid check** — only if the user asks for it. Set it up with the user: day and time, which pages (★, earning, new not yet indexed, a platform, a list), the maximum number of pages and the cost per run. Register it on the server with `paid_check_schedule` so the user is warned in Telegram on the day: *"Today at 10:00: position check of 24 ★ pages, ~$0.05 from your DataForSEO balance"* with buttons **Run as planned · Only ★ · Skip this time · Change** (a text reply changes the set). The assistant's scheduled task calls `paid_check_pending` right before the run and does exactly what it returns: run as planned, the corrected set, or nothing. No answer in Telegram = run as planned (the user set it up and was warned). After the run, the result and the real cost go to the same Telegram chat.
  Without the server or a linked Telegram there is no way to warn the user, so scheduled paid checks are not offered: the check is suggested in the next session and runs after a yes.
- Any rank tracker instead (Ubersuggest, SE Ranking, ProRankTracker, SEO PowerSuite…): upload its CSV export — `import-ranks parasite-seo-progress.csv export.csv`. Rows are matched by URL, else by keyword to the page's query or topic. If the tracker shows another page of the same platform ranking (trackers follow a domain, and researchgate.net or medium.com is everyone's domain), the row is skipped, never credited to the user. Weekly export = weekly history.
- Single positions from the user's own notes: `tag --position` (or `add --event check --position`).

## Rules

- **Paid checks only with the user's yes, every time.** Index checks, position checks (Mode 9), page keywords (Mode 9b) and any other call that spends the user's SEO API balance: before each run ask **how many pages and which** — ★ pages, earning pages, new pages not yet indexed, one platform, or the user's own list — show the rough cost for that number (`--dry-run`), and run only after a clear yes. Never run them silently from the check queue, the daily plan or the weekly review, and never extend an earlier yes to a new run or a bigger set. A scheduled weekly run exists only if the user set it up themselves with the pages and the cost shown. The user must always know what they are paying for.
- **★ pages.** Offer the user to star their main pages (`tag --priority high`) after the import; ★ pages are the default proposal for every paid check.

- Facts only. Never mark a page indexed or alive without a check result; never record a sale the user did not report or export.
- Commission is what counts; reversed sales are shown but not counted, refunds subtract. Pending is shown separately.
- Money stays in its currency; do not convert unless the user gives a rate.
- No income forecasts in reports; label any estimate.
- Exports contain customer data: keep only the columns the journal needs and keep the files in the user's project. Never send them to third-party services.
- If a period looks empty, say so and ask whether something was not logged — do not fill gaps.
