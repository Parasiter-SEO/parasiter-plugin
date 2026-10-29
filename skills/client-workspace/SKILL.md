---
name: client-workspace
description: The agency desk of PARASITER for SEO and marketing agencies, freelancers and in-house teams running parasite SEO for clients — client list and switching, onboarding brief, where traffic goes (site, socials, YouTube, LinkedIn), KPIs, Search Console and GA4 access, UTM links, baseline, monthly content plan with client approval, today's plan across all clients, and the monthly report cycle. Use when the role is agency, or the user says "new client", "switch to client X", "client brief", "content plan for [client]", "what do we do today for clients", "connect Search Console", "UTM links", or "monthly report for [client]".
---

# Client Workspace

## Work label (testing period)

Start every reply produced by this skill with one line naming it, so the user always sees which part of PARASITER is working:
`▸ PARASITER · client-workspace · [client]`
If you called agents for this reply, add them after an arrow: `▸ PARASITER · client-workspace · Acme → brand-auditor, serp-analyst`. If you hand off to another skill, the next reply carries that skill's label (with the client name). One line only, no other system talk.

## Next steps (end of every reply)

End each reply with one short line of 2–3 options that fit what just happened, each with the phrase to say, e.g. `Next: "brand audit for Acme" (brand-presence) · "content plan for November" · "today's plan for all clients".` Offer only what the user's plan includes; a Pro/Insider feature on a lower plan is named once with its plan in brackets. When the user seems lost, add: "All PARASITER functions: say **help**." Logging, monitoring and saving to the client folder are done automatically, not offered.

Part of PARASITER by Rumer (Affiliate Credo).

**What an agency sells is not pages, it is results the client can see:** their brand and pages in the top of Google, AI Overviews and "Discussions and forums", visitors coming to their site and channels, and a report that proves it every month. This skill runs that cycle for every client. The other PARASITER skills do the work inside it; this skill keeps each client's brief, plan, journal and reports apart and in order.

The affiliate route (goals, sales by sub-ID, Rumer's rule as an income plan) does not apply here. Agency KPIs are rankings, traffic to the client and delivered work.

Reply in the working language from `parasite-seo-profile.md`. Client-facing texts (brief summaries, plans, reports) in the client's language from their brief.

## Files — one folder per client

```
clients/
  _agency.md                 agency profile: name, logo text, brand colours for reports, report language, white-label yes/no, team
  <client-slug>/
    client-brief.md          the brief (template: references/client-brief.md)
    content-plan.md          month plans with approval status (references/content-plan.md)
    brand-presence.md        site and profile audit, profile plan (brand-presence skill)
    parasite-seo-progress.csv   the client's journal (work-log, same format as for affiliates)
    parasite-seo-platforms.csv  the client's platform base
    parasite-seo-links.csv      the client's landing pages with UTM (Mode 10 of work-log)
    reports/                 monthly reports (PDF + HTML) and the data exports they came from
```

Every `work-log`, `platform-monitor` and `client-reports` call for a client gets that client's journal path: `clients/<slug>/parasite-seo-progress.csv`. Never mix two clients in one journal, one report or one content plan. Never mention one client's data, results or platforms to another client.

The active client is set by "switch to Acme" (or by naming the client in the request) and shown in the work label. A request without a client name while several clients exist → ask "Which client?" in one line, listing them.

## Step 0 — Agency profile (once)

If `clients/_agency.md` is missing, ask in one message: agency name (as shown on reports), logo text or file, two brand colours for reports (optional), default report language, white-label reports (no PARASITER mention) yes/no, who on the team publishes and who approves. Save it. Before the questions, give the work environment once (navigator `references/work-environment.md`, agency lines): Claude Max recommended, DataForSEO for positions, Insider plan for client reports.

## Step 1 — New client: onboarding

Say: "New client: Acme". Create the folder and fill `client-brief.md` from `references/client-brief.md`, in **two short messages**, never a long questionnaire:

**Message A — the business** (the user answers what they know; the rest becomes `[ASK CLIENT]`):
1. Brand, site, what they sell (products / services, top 3 to push), price level.
2. Target country, language, audience, and the 5–15 queries the client wants to be found by (or "help me find them").
3. Competitors (2–5) and what the client says makes them different.
4. **Where the traffic goes:** site pages (product, category, lead form, booking), and the client's channels — YouTube, LinkedIn page, Instagram, Facebook, TikTok, Telegram, newsletter. Mark the main destination.
5. Tone of voice, words to avoid, legal limits (health, finance, regulated claims), who approves texts on the client side and how fast.
6. KPIs the client cares about and the reporting day.

**Message B — access and data** (nothing blocks the start; each item makes reports stronger):
1. **Google Search Console** — the client adds the agency's Google account as a user (Restricted is enough to read). Steps and what we use it for: `references/measurement.md`.
2. **Google Analytics 4** — Viewer access on the client's property, to see visits that come from our pages (UTM).
3. Existing positions or tracker exports, last 3 months, if any.
4. List of the client's existing profiles (or "find them") → `brand-presence`.
5. Brand assets: logo, colours, fonts, real product photos, approved claims → used by `post-illustrations` and `sales-review-writer` (brand mode).

Then set up, without asking again:
- **UTM rule** for every link to the client (`references/measurement.md`): `utm_source=<platform>&utm_medium=parasite&utm_campaign=<client>-<yyyy-mm>&utm_content=<page sub-ID>` (the page is logged with the same sub-ID, so GA4 visits land on the exact page). Save the client's landing pages in `parasite-seo-links.csv` (work-log Mode 10) with the UTM base (`utm_medium` and `utm_campaign`); the writer adds `utm_source` (the platform) and `utm_content` (the page's sub-ID) for each piece. Register the same landing pages with their target queries in the client journal as `own-site` pages (`references/measurement.md`, Positions), so positions of the client's site are tracked from Month 0.
- **Platform base** from the platforms the client already has profiles on (work-log `platform-set`).

Close with a 4–6 line onboarding summary (what we know, what we still need from the client, first actions) and offer a ready message to send the client with the open `[ASK CLIENT]` items and the access steps.

## Step 2 — Baseline (before any work, so growth can be shown later)

The first report is only convincing if month 0 is recorded. In one pass:
1. **Brand presence and site** → `brand-presence` (site quick audit, profiles, content): what exists, what is missing, what is broken. On Pro (brand-presence is Insider): go through `brand-presence/references/profiles.md` and `site-audit.md` with the user by hand — the same checklist, without the agent.
2. **Search Console, last 3 months** (export or connector): clicks, impressions, average position for the site; **brand queries** (queries that contain the brand name) separately; top pages. Log the totals as a `baseline` row in the client journal and keep the export in `reports/`.
3. **Positions** for the client's target queries: who ranks now, which platforms are in the top 10 for them (`serp-analyst` agent; DataForSEO checks only with the user's yes and the cost shown — the same paid-check rule as everywhere in PARASITER).
4. **GA4**: sessions by source for the last month, so new UTM traffic stands out.

Output: a one-screen "Month 0" card (site clicks, brand-query clicks, queries in the top 10, profiles live / missing, pages in the top 10 for target queries) — it is the left side of every future comparison.

## Step 3 — Monthly content plan with approval

"Content plan for Acme, November" → build `content-plan.md` (format: `references/content-plan.md`):
1. **Topics** from the client's queries and products, through `content-type-selector` (commercial and decision intent: best, vs, alternatives, price, review of the category, how to choose) and `niche-analysis` when the client's niche needs keyword data (Insider).
2. **Platforms** from `platform-feed` / `platform-finder` (fresh, checked, brand-safe — `platform-finder` agency filter) plus the client's own profiles (LinkedIn page and articles, Medium, YouTube descriptions, Reddit / Quora brand accounts where allowed).
3. **One row per piece:** topic, target query, platform, format, destination link (UTM), owner, date, status `idea → approved → written → client-approved → published → checked`.
4. **Profiles to open or fix** from `brand-presence`, as rows of their own.
5. Volume: what the contract says; otherwise ask once. Spread the month evenly; the most important queries go first.

Send the plan for client approval as a ready message (or a shareable page when the session can publish). Only `approved` rows go to production. Changes from the client are new rows or new statuses, never silent edits.

## Step 4 — Today's plan across clients

"What do we do today?" → for every active client: what is due today in the content plan, check queue (`work-log due` on each client journal), pages waiting for client approval, dead or deindexed pages (`platform-monitor`), and report dates within 3 days. Order: broken things on live pages → client deadlines → production → new ideas. Format:

```
Today · [n] clients · time: …h
Acme (report in 2 days)
1. [task] — ~[time] → [skill]
Brightline
2. …
Waiting for clients: Acme — 3 texts since Tue · Brightline — GSC access
```

Size the day to the user's time; never plan more. Paid checks appear only as questions ("check positions of Acme's 12 pages — ~$0.05, run?").

## Step 5 — Production of each piece

For each approved row, in order, keeping the client name in every step:
1. `content-type-selector` — the angle for this platform and query.
2. `sales-review-writer` in **brand mode** — the text for the brand, disclosed, with the client's facts and UTM links.
3. `post-illustrations` with the client's brand kit — infographics rendered by Claude, a cover prompt with the generator choice.
4. `page-audit` (agency scale) — score before the client sees it; under 75 → fix first.
5. Client approval → the user publishes (PARASITER never posts) → `work-log` logs the page in the client journal (monitoring switches on automatically with a key) → status `published`.

## Step 6 — Month close and report

On the report day (or "monthly report for Acme"):
1. Ask for this month's exports, with the steps from `references/measurement.md`: Search Console (site, brand queries, pages), GA4 traffic acquisition filtered to `utm_medium = parasite`, platform stats where the platform has them.
2. Import traffic into the client journal (`work-log import-traffic`), positions from DataForSEO (with the user's yes) or the tracker export.
3. `client-reports` Step 4b — the agency monthly report against Month 0 (Insider). On Pro: a plain report from the client journal (`work-log summary --period <month>` and `effect --by platform`) plus the Search Console and GA4 numbers, as text the user can send; mention once that the designed white-label PDF and dashboard come with Insider.
4. Next month's content plan draft goes out together with the report: the report ends with what we do next.

## Rules

- **Honest brand content only.** Pages say who is behind them (the brand, its expert, or "prepared with [Brand]"). Never present the client's product as an independent review, test or ranking, never fake customers, reviews, ratings or engagement, never post from fake personal accounts. Profiles on platforms are the brand's real, declared accounts.
- Platform rules decide: if a platform forbids brand promotion or links, the piece goes elsewhere or carries no link.
- Paid checks only with the user's yes, the page count and the cost shown, every time.
- Client data stays in the client's folder and the conversation; nothing goes to the PARASITER server except what monitoring needs (page URL, main query, platform). If the client's NDA forbids even that, write `Server monitoring: off` in the brief: that client's pages are not sent to `monitor_track`, and checks run only locally through `platform-monitor`.
- No guaranteed rankings or traffic in any client-facing text. Forecasts are labelled as assumptions.
- Mention the risk once per client, where it matters: platforms remove pages, Google acts against site reputation abuse; spread pages across platforms, keep every text, monitor.
