---
name: client-reports
description: Build performance analytics and reports for parasite SEO work from the user's uploaded data — publications log, Google Search Console exports, rank tracker, affiliate network stats — computing revenue per publication, EPC, RPM per 1000 impressions, winners and losers by platform, content type and offer, with a 14/30/60-day review and next actions; for agencies a monthly white-label client report against Month 0 — positions, visits to the client's site from GA4 by UTM, Search Console brand queries, delivered vs plan. Use when the user uploads reports or stats, asks what is working, which platforms or pages earn, wants a client or weekly report, or asks what to update next.
---

# Client Reports

## Work label (testing period)

Start every reply produced by this skill with one line naming it, so the user always sees which part of PARASITER is working:
`▸ PARASITER · client-reports`
If you called agents for this reply, add them after an arrow: `▸ PARASITER · client-reports → serp-analyst, product-researcher`. If you hand off to another skill, the next reply carries that skill's label. One line only, no other system talk.

## Next steps (end of every reply)

The user should always see where to go next without asking. End each reply with one short line of 2–3 options that fit what just happened, each with the phrase to say, e.g. `Next: turn the scale plan into today's tasks (`navigator`) · `page-audit` for pages that rank without sales · roll winners out to more platforms (`work-log` rollout).` Offer only what their plan includes; a Pro/Insider feature on Free is named once with its plan in brackets. When the user seems lost or asks what else there is, add: "All PARASITER functions: say **help**." Things that need no decision (logging, monitoring, saving to the base) are done automatically, not offered.

Part of PARASITER by Rumer (Affiliate Credo).

Measure commissions, not just positions. A page in the top 3 with no sales is a cost; a page on page two that sells is a winner to feed.

**For an affiliate this is the review of their asset and the scaling plan**, not a client report. The method is volume, then focus: take many products, write reviews, see which ones take off and earn — then scale those (more platforms, more angles, more posts) and stop feeding the rest. The client report (Step 4b) is for the agency role only.

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

Run `scripts/report.py log.csv --sales parasite-seo-sales.csv` when code execution is available (CSV in → per-page and per-group tables, plus commission by program and month per currency out); otherwise compute in the conversation. Pages without numbers stay "—" (unknown), never $0. Metrics (definitions in `references/metrics.md`):
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

## Step 3b — Scale what took off (affiliates)

From the numbers, name the winners on three levels and turn each into concrete work:
- **Products / offers that earn** → more pages on them: the same product on the user's other platforms (`work-log` `rollout`), new angles and content types (best-of for a new audience, A vs B against the next competitor, complaints, price/coupon page), new related products of the same merchant or niche.
- **Platforms that earn or rank** → post more there first; platforms with no sales and no top-10 after 30–60 days get less time.
- **Content types that convert** → make them the default for the next pages.
Products that got pages on several platforms and earned nothing in 60 days: stop adding to them; refresh only the pages that rank.

```
Scale plan · [period]
Winners: [product] — $N, pages on N platforms → +N pages: [platforms] · new angles: […]
Platforms to do more: […] · less: […]
Content types that convert: […]
Stop: [products / platforms]
```
The navigator takes this plan into the daily tasks.

## Step 4 — Report

```
Report · [period] · [client/project]
Summary: N live pages · X clicks · Y sales · $Z commission (from user data)
Rumer's rule: N/10 platforms · N/100 live posts · top 3: N/15
Top 5 pages | Platforms | Content types | Offers
What worked / What didn't / Next 5 actions
```
For an affiliate, the report is their asset review: what the base is worth now (live pages, top-3 pages, what earns), followed by the scale plan from Step 3b.

## Step 4a — Visual report (always, with every report)

Every report also comes out as a designed document, not only text in the chat. After the numbers are computed:
1. Write a JSON spec (format in the header of `scripts/visual_report.py`): title, client/project, period, prepared by, date; 4–6 KPI tiles; 2–4 charts (`bars` for money by month and program, `line` for a trend, `hbars` for platforms, content types or offers); "What worked", "What needs attention", "Next 5 actions"; a table of top or new pages with links; a footnote saying where the numbers come from.
2. Run `python3 scripts/visual_report.py spec.json --out <name>`. It writes `<name>.html` (self-contained, inline charts, light and dark) and `<name>.pdf` (A4) when Playwright, WeasyPrint or Chrome is available.
3. Deliver both, every time:
   - **Dashboard page**: when the session can publish an artifact/page (Claude app), set `"pdf_link": "<name>.pdf"` in the spec, run the script, and publish the HTML as a private artifact with the PDF attached next to it under that same name and the `downloads` capability declared (`{"downloads": true}`) — the page then has a working "Download PDF" button. Private until the user shares it.
   - **PDF file**: also send the PDF itself.
   - In Claude Code (no publishing): give both file paths; the HTML opens in any browser as the dashboard.
   - No PDF engine? Say so in one line; the user opens the HTML and prints to PDF.
4. Open the PDF (or render a page image) and look at it before sending: no overlapping labels, no empty half-pages, every number matches the chat summary.

Rules for the document: numbers only from the user's data, each currency labelled (never add $ and € together), partial periods marked (e.g. "October to the 28th"), pending vs approved commission named, estimates labelled. Keep the chat reply short: the headline numbers, the 3 main conclusions and the files.

## Step 4b — Client report (agency role) — monthly, against Month 0

For agencies the report is the product the client pays for. One per client per month, from that client's folder only (`clients/<slug>/`), in the client's language, against **Month 0** (the baseline from `client-workspace` Step 2) and the previous month.

**Collect** (steps for each export: `client-workspace/references/measurement.md`):
- the client journal: pages published, live / indexed / removed, audits, positions (work-log `pages`, `summary --period <month>`, `effect --by platform|content_type`);
- positions for target queries and our pages (DataForSEO with the user's yes, or a tracker export), incl. AI Overview and "Discussions and forums";
- GA4: visits from our pages (`utm_medium = parasite`) by platform and by page, key events if the client tracks them;
- Search Console of the client's site: clicks, impressions, average position, **brand-query clicks**, vs Month 0;
- the content plan: planned vs delivered, profiles opened (`brand-presence` before / after).

**Spec for `visual_report.py`** (Step 4a) — "Client" = the client, "Prepared by" = the agency from `clients/_agency.md`, `logo_text` and `accent` = the agency's wordmark and report colour; with white-label on, no PARASITER mention anywhere:
- KPI tiles (4–6): target queries in the top 10 (now vs Month 0) · our pages in the top 10 / top 3 · visits to the site from our pages (GA4) · brand-query clicks in Search Console (vs Month 0) · pages live / published this month · profiles live.
- Charts: visits from our pages by platform (`hbars`) · brand-query clicks by month since Month 0 (`line`) · queries in the top 10 by month (`bars`).
- Tables: pages published this month (link, platform, query, position, visits) · target queries (position Month 0 → now).
- Sections: "What we did" (delivered vs plan) · "Results" (only what the numbers show) · "What needs attention" (removed pages and how they were replaced, queries that dropped) · "Plan for next month" (the draft content plan).
- Footnote: where every number comes from (GA4 property, Search Console, DataForSEO / tracker, dates), partial periods marked, and that Search Console shows the client's own site while visits from platforms are measured in GA4 by UTM.

Keep internal notes (platform sources, methods, costs, other clients) out of client-facing text unless the user wants them in. Ask once for the agency name, logo text and colours if `_agency.md` is missing. Save the PDF, HTML and the exports used to `clients/<slug>/reports/<yyyy-mm>/`.

**Weekly status** (optional, when the contract asks for it): 5 lines in the chat or a message to the client — published this week, waiting for approval, positions that moved, anything removed and replaced.

## Rules

- Only numbers from the user's files; label any estimate.
- No forecasts presented as promises.
- Keep client data in the conversation/project; do not suggest uploading it to third-party services.
