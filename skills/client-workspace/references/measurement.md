# Measurement for clients — Search Console, GA4, UTM, positions

Agency KPIs come from three places. Each answers a different question; none replaces the others.

| Source | Answers | Used at |
|---|---|---|
| **Positions** (DataForSEO through `work-log` Mode 9, or a tracker export) | Are our pages and the brand in the top 10 / top 3, AI Overview, "Discussions and forums" for the client's queries? | Baseline, weekly for ★ pages (with the user's yes), monthly report |
| **GA4 + UTM** | How many visitors did our pages send to the client's site, to which pages, and what did they do there (leads, sign-ups, purchases if the client tracks them)? | Every monthly report |
| **Search Console** (the client's own site) | Is the client's site itself getting more Google visibility — clicks, impressions, average position, and especially **brand queries**? | Onboarding (Month 0), every monthly report, a growth check after 30–60 days |

Search Console only sees the client's own site in Google. It does not see visits from our pages on other platforms — those are in GA4, tagged with UTM. Say this to the user once at onboarding, so nobody expects parasite pages in the client's Search Console.

## When Search Console comes in

1. **Onboarding — Month 0.** Last 3 months: total clicks and impressions, brand-query clicks, top pages, top queries. Without it, the report has nothing to compare against.
2. **Every monthly report.** The same numbers for the month, compared with Month 0 and with the previous month.
3. **30–60 days after the first pieces go live.** Brand queries and branded impressions: people who met the brand on platforms search for it. This is the clearest indirect effect of parasite SEO on the client's own site; report it as a trend, never as a promise.
4. **When a client page is a target itself** (the client wants their product page to rank): positions of that page and its queries.

### Giving access (the client does this)
- Search Console → the property → **Settings → Users and permissions → Add user** → the agency's Google account → permission **Restricted** (enough to read reports). Full only if the agency also fixes the site.
- Alternative without access: the client exports **Performance → Search results → Export** (CSV / Google Sheets) for the period with Queries and Pages tabs.
- If a Search Console connector is available in the user's assistant, use it with the client's permission; otherwise exports.

### Reading it
- Brand queries = queries that contain the brand name or its spellings; list the spellings in the brief.
- Compare equal periods (month to month, Month 0 average to this month). Mark partial months.

## GA4 — visits from our pages

- Access: GA4 **Admin → Property access management → + → Add users** → the agency's account → role **Viewer**.
- Monthly export: **Reports → Acquisition → Traffic acquisition**, dimension **Session source / medium**, filter `medium = parasite` (or add the secondary dimension **Session manual campaign name**), date range = the month → **Share → Download file → CSV**.
- Import into the client journal: `python3 scripts/worklog.py import-traffic clients/acme/parasite-seo-progress.csv ga4-nov.csv --from 2026-11-01 --to 2026-11-30` (work-log Mode 3). `Session source / medium` (utm_source = platform) credits the platform's total.
- **Per page:** export with **Session manual ad content** (= `utm_content`) as the dimension next to Session source. Each page is logged with its sub-ID equal to its `utm_content` (`work-log add … --sub-id pb-how-to-choose-crm`), so GA4 visits land on the exact page.
- Key events (leads, sign-ups, purchases) — report them only if the client tracks them in GA4; never estimate conversions the client doesn't measure.

## UTM rule — every link to the client

```
?utm_source=<platform>&utm_medium=parasite&utm_campaign=<client-slug>-<yyyy-mm>&utm_content=<page sub-ID>
```
- `utm_source` — the platform slug as in the journal (medium, linkedin, pressbooks, reddit…).
- `utm_medium=parasite` — the same for every piece, so one filter shows all our traffic. The client may prefer `referral-content`; use their name if they ask, and keep it constant.
- `utm_campaign` — client and month of publishing.
- `utm_content` — the page's sub-ID, short and unique (`pb-how-to-choose-crm`): the same value is logged as the page's sub-ID in the client journal, so GA4 visits are credited to the exact page.
- Links to the client's own social profiles and channels (YouTube, LinkedIn page) get no UTM; their platform stats are the source.
- Unlike affiliate work (where UTM goes to the merchant and is useless), for clients UTM is the main proof of traffic: the agency sees the client's analytics.

## Positions

- Client target queries and every published page's main query, through `work-log` Mode 9 on the user's DataForSEO account — always with the user's yes, the number of pages and the cost shown.
- Also record: AI Overview citations, "Discussions and forums", image and video blocks (Mode 9 sees them).
- Without DataForSEO: the user's tracker export (Ubersuggest, SE Ranking, Semrush…) imported with work-log.
