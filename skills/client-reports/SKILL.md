---
name: client-reports
description: Build performance analytics and reports for parasite SEO work from the user's uploaded data — publications log, Google Search Console exports, rank tracker, affiliate network stats — computing revenue per publication, EPC, RPM per 1000 impressions, winners and losers by platform, content type and offer, with a 14/30/60-day review and next actions. Use when the user uploads reports or stats, asks what is working, which platforms or pages earn, wants a client or weekly report, or asks what to update next.
---

# Client Reports

## Work label (testing period)

Start every reply produced by this skill with one line naming it, so the user always sees which part of PARASITER is working:
`▸ PARASITER · client-reports`
If you called agents for this reply, add them after an arrow: `▸ PARASITER · client-reports → serp-analyst, product-researcher`. If you hand off to another skill, the next reply carries that skill's label. One line only, no other system talk.

Part of PARASITER by Rumer (Affiliate Credo).

Measure commissions, not just positions. A page in the top 3 with no sales is a cost; a page on page two that sells is a winner to feed.

Reply in the user's language. Reports for clients can be in the client's language.

## Step 1 — Collect

Ask for what the user has (any subset works):
1. **Publications log** — URL, platform, date, product/offer, content type, main query, country. Template: `references/log-template.csv`. If the user keeps the work journal (`parasite-seo-progress.csv`, `work-log`), take URLs, platforms, offers, dates, statuses, traffic and sales (`parasite-seo-sales.csv`) from it instead of asking; `work-log effect` already gives per-page, platform, offer and program numbers — use them and add the client view.
2. **Search Console** (own pages/sites) — performance export by page and query: impressions, clicks, CTR, position.
3. **Rank tracker** export for parasite pages (third-party platforms have no Search Console).
4. **Affiliate stats** — clicks, conversions, commission by sub-ID/link or by day.
5. Platform stats if available (views on Medium, forum views).

Sub-IDs are a bonus, not a requirement: many sales can't be tied to a page, and that is normal. Count every sale exactly by program, offer and pack, and spread untied sales over the pages as a labelled estimate (`work-log` Mode 2). Mention sub-IDs once, where the network supports them; never block the report on them.

## Step 2 — Join and compute

Run `scripts/report.py` when code execution is available (CSV in → per-page and per-group tables out); otherwise compute in the conversation. Metrics (definitions in `references/metrics.md`):
- Revenue per publication, EPC, conversion rate.
- RPM_SERP = (clicks / impressions) × (sales / clicks) × avg commission × 1000 — only where impressions exist.
- Age of each page, alive/indexed status (from platform-monitor if connected), position and how many pages are in the top 3 (where sales start).
Group by platform, content type, offer, country.

## Step 3 — Read the numbers

- **Winners**: top pages by revenue/EPC → refresh deal box and date, add comparison blocks, improve CTA (page-audit), republish the format on other platforms.
- **Rank without sales**: page-audit — usually first screen, author, CTA or wrong intent.
- **Dead or deindexed**: `work-log` `republish` — the pages with their saved sources, rewritten for a new home.
- **Losers after 60 days**: reposition topic/type, don't clone.
- **Platforms**: reduce effort where visibility dropped (especially after Google updates).

Review points: 14, 30 and 60 days after publication.

## Step 4 — Report

```
Report · [period] · [client/project]
Summary: N live pages · X clicks · Y sales · $Z commission (from user data)
Rumer's rule: N/10 platforms · N/100 live posts · top 3: N/15
Top 5 pages | Platforms | Content types | Offers
What worked / What didn't / Next 5 actions
```
For a client report, offer a clean document version; keep internal notes (platform sources, methods) out of client-facing text unless the user wants them in.

## Rules

- Only numbers from the user's files; label any estimate.
- No forecasts presented as promises.
- Keep client data in the conversation/project; do not suggest uploading it to third-party services.
