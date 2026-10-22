---
name: work-log
description: The user's parasite SEO journal of work, traffic and sales. Records every action the moment it happens (page published, sent to indexing, checked alive/indexed, audited, refreshed, moved, platform tested), every sale (logged by hand or imported from affiliate network exports) and traffic (platform views, affiliate clicks), ties sales to pages by sub-ID, and turns it all into reports for any day, week or month, effectiveness tables by page, platform, offer, program and content type, and a queue of pages due for checks plus sales reports due for upload. Use when the user reports work or a sale ("added an article", "indexed it", "made a sale"), uploads a sales or traffic export, asks "what did I do / earn this week", wants a weekly or monthly report, asks which pages, platforms or offers earn, or what needs checking.
---

# Work Log

Part of PARASITER by Rumer (Affiliate Credo).

Parasite SEO is measured in sales, not positions. This skill keeps three things in one place: **what was done** (pages, checks, audits), **what traffic came** (views, affiliate clicks) and **what it earned** (every sale, tied to its page). A page that is in the journal gets checked — alive, still indexed, follows the conversion rules. A sale that is in the journal tells which page, platform, offer and content type actually pay.

Reply in the working language from `parasite-seo-profile.md`. Keep column names and `event` / `status` values in English so the files stay machine-readable.

## Files

In the user's project folder (formats in `references/log-format.md`):
- `parasite-seo-progress.csv` — work journal: pages, checks, audits, traffic, imports (the same file `goals` reads).
- `parasite-seo-sales.csv` — one row per sale, logged by hand or imported.

One row per fact. Never edit or delete old rows; corrections and status changes are new rows. If a file has an older, shorter header, the script upgrades the header and keeps every value.

The script `scripts/worklog.py` does all reading, writing and counting. Pass `--date` / `--time` in the user's local time when the machine clock may differ (cloud sandboxes run in UTC). Without code execution, append rows by hand and count the same way.

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

Views and clicks are what turn sales into conversion. Two sources:
- **Platform stats** (Medium stats, LinkedIn post analytics, forum views, YouTube, Search Console for own pages): export or screenshot → `import-traffic export.csv --platform medium --from 2026-10-01 --to 2026-10-21`. Matching is by page URL. From a screenshot, log per page: `add --event traffic --url … --views 1200 --date <period end> --note "traffic 2026-10-01..2026-10-21"`.
- **Affiliate clicks** (network click / hop reports by sub-ID): the same `import-traffic`; matching is by sub-ID.

Always pass the export's date range: the same page and period are never counted twice. Traffic is dated at the end of its period.

## Mode 4 — Reports

**Work report** — "what did I do today / this week / in September": `summary --period <period>` (`today`, `yesterday`, `week`, `last-week`, `month`, `last-month`, `YYYY-MM`, `YYYY-MM-DD`, `YYYY-MM-DD..YYYY-MM-DD`, `all`). It shows: work done, sales and commission, traffic, comparison with the previous period, work by day, pages published with their status now, pages that earned, and what needs attention.

**Effectiveness** — "what earns", "which platforms/offers work", "is the system paying off": `effect --period <period> --by page|platform|offer|program|campaign|content_type|month`. Per group: pages, views, affiliate clicks, sales, commission, pending, EPC, conversion, commission per page, per 1,000 views. `--by program`, `--by month` count every sale exactly; page-level views show exact sales plus the estimated share. `--by month --period all` shows the trend since the baseline — the clearest answer to "is the system paying off".

Read the table for the user in 3–5 lines: what earns most per page, what gets traffic but no sales (→ page-audit: first screen, CTA, intent), what gets nothing after 30–60 days (→ reposition or drop), which content type and platform to do more of. Compare with the baseline in `parasite-seo-goals.md` when it exists. Deeper client-facing reports: `client-reports`.

## Mode 5 — Check queue

"What needs checking?" or at session start (the navigator asks): `due`. It lists, most urgent first:
- **Sales reports to upload** — per program, with the date range to export.
- **Removed / noindex** — republish from the saved copy, log `moved`.
- **Not indexed 14+ days** — resubmit, add links, or move.
- **Alive / index check due** — 2, 7, 14 days after publishing, then every 14 days; `not-indexed` rechecked after 3 days.
- **Audit score under 70** — improve with page-audit, log `refreshed` + new `audit`.
- **Audit due** — never audited, refreshed since, or 14/30/60-day review.
- **Optional: no sub-ID** — shown only in the full queue; sales are still counted by program.

Checks of more than 3 URLs go to the `page-checker` agent (via platform-monitor); every result is logged as `check`.

## Mode 6 — Page registry

`pages [--platform medium]` — every page with platform, offer, sub-ID, age, status, audit score, views, affiliate clicks, sales and commission.

## Rules

- Facts only. Never mark a page indexed or alive without a check result; never record a sale the user did not report or export.
- Commission is what counts; reversed sales are shown but not counted, refunds subtract. Pending is shown separately.
- Money stays in its currency; do not convert unless the user gives a rate.
- No income forecasts in reports; label any estimate.
- Exports contain customer data: keep only the columns the journal needs and keep the files in the user's project. Never send them to third-party services.
- If a period looks empty, say so and ask whether something was not logged — do not fill gaps.
