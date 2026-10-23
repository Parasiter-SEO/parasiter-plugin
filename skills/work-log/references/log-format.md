# Journal formats

Two files in the user's project folder. One row per fact. Never edit old rows; add a new one.

## parasite-seo-progress.csv — work and traffic

Shared by `work-log`, `goals`, `navigator` and `client-reports`.

```
date,time,event,page_url,platform,offer,program,campaign,sub_id,main_query,content_type,status,score,views,clicks,aff_clicks,sales,revenue,minutes,note
2026-10-19,09:00,baseline,,,,,,,,,,,,,,,400,,"30 live pages, 4/week, 10 h/week, $400/month"
2026-10-20,11:20,published,https://medium.com/@me/vpn-compare,medium,nordvpn,NordVPN (Impact),vpn-test,md-1020-1,nordvpn vs surfshark,ab-comparison,live,,,,,,,90,
2026-10-20,11:35,audit,https://medium.com/@me/vpn-compare,medium,nordvpn,,,,,,,82,,,,,,10,
2026-10-20,11:40,submitted,https://medium.com/@me/vpn-compare,medium,,,,,,,,,,,,,,,
2026-10-22,08:10,check,https://medium.com/@me/vpn-compare,medium,,,,,,,indexed,,,,,,,,
2026-10-27,18:00,traffic,https://medium.com/@me/vpn-compare,medium,nordvpn,,,,,,,,1200,,40,,,,traffic 2026-10-20..2026-10-27 from medium-stats.csv
2026-10-27,18:05,import,,,,NordVPN (Impact),,,,,,,,,,,,,"sales import impact.csv: 2026-10-20..2026-10-27, 3 new, 0 status updates, 0 already in"
2026-10-29,10:00,check,https://forum-x.com/t/123,forum-x,,,,,,,removed,,,,,,,,
2026-10-29,10:30,moved,https://forum-x.com/t/123,forum-x,,,,,,,,,,,,,,,"to https://other.com/p/9"
```

| Column | Meaning |
|---|---|
| `date`, `time` | user's local date YYYY-MM-DD, time HH:MM (optional) |
| `event` | see below |
| `page_url` | the page; empty for baseline / task / platform / import |
| `platform` | slug: medium, linkedin, reddit, forum-x |
| `offer` | product or brand slug |
| `program` | affiliate program or network account the sales come from: "ClickBank", "NordVPN (Impact)", "Amazon US". Must match the `--program` used for imports |
| `campaign` | the pack the page belongs to ("keto-pack-oct"): pages published together for one offer, judged together |
| `sub_id` | optional: tracking value in this page's affiliate link (on `published`); ties sales to the exact page when the network passes it |
| `main_query`, `content_type` | on `published` |
| `status` | on `check` (and optionally `published`), see below |
| `score` | page-audit 0–100, on `audit` |
| `views` | platform views / reads / visits for the period, on `traffic` |
| `clicks` | search clicks (Search Console), on `traffic` |
| `aff_clicks` | clicks on the affiliate link (network click / hop report), on `traffic` |
| `sales`, `revenue` | only on `stats` (aggregate numbers when single sales cannot be imported); on `baseline`, `revenue` = monthly revenue now |
| `minutes` | time spent |
| `note` | free text |

Older journals with fewer columns are read as they are; the first write upgrades the header and keeps all values. Old `stats` rows with `clicks` are read as affiliate clicks.

### Events

`baseline` · `published` · `submitted` · `check` · `audit` · `refreshed` · `moved` · `platform` · `traffic` · `stats` · `import` · `task` · `note`

### Statuses

`live` (opens, index unknown) · `indexed` · `not-indexed` · `noindex` · `dropped` (indexed, lost ranking) · `removed` (404, deleted, banned) · `dead` (platform gone)

Alive = latest check live, indexed, not-indexed or dropped. Indexed = latest check indexed or dropped.

## parasite-seo-sales.csv — sales

```
date,program,network,offer,sub_id,page_url,order_id,amount,commission,currency,status,source,note
2026-10-21,ClickBank,ClickBank,KetoX,li-1010-1,,ABC123,79.00,42.50,USD,approved,import:clickbank-oct.csv,
2026-10-22,NordVPN (Impact),,,md-1020-1,,,,30.00,USD,approved,manual,told in chat
2026-10-25,ClickBank,ClickBank,KetoX,li-1010-1,,ABC123,-79.00,-42.50,USD,reversed,import:clickbank-oct2.csv,
```

| Column | Meaning |
|---|---|
| `date` | sale date |
| `program`, `network` | as in the journal |
| `offer` | product from the export |
| `sub_id` | from the export; the page is found through the journal's `published` rows |
| `page_url` | only when the user names the page directly |
| `order_id` | transaction / receipt / action ID; used to skip duplicates and apply status changes |
| `amount` | sale amount (customer paid) |
| `commission` | what the user earns — the number every report uses |
| `currency` | ISO code |
| `status` | `approved` · `pending` · `reversed` |
| `source` | `manual` or `import:<file>` |

Counting rules:
- Latest row per order wins (a later import with a new status updates the sale).
- `reversed` with positive commission: shown, not counted. Negative rows (refunds, chargebacks): subtract.
- A `manual` sale without order ID is dropped when an imported sale of the same program and commission within ±2 days exists.
- Sales are attributed to a page by `page_url`, else by `sub_id` → the page whose `published` row has that sub-ID. Adding a sub-ID to a page later attributes its past sales too.
- Sales without a page are normal. They count exactly in program and month totals. Page, platform, offer, content-type and campaign views add an **estimated share**: each untied sale is split over the pages of the same program published by the sale date and not moved before it, by affiliate clicks in the period, else views, else equally; pages with no traffic data get the average weight. Always shown as an estimate.

## parasite-seo-platforms.csv — my platform base

```
platform,domain,type,language,links,account,score,state,added,source,note
medium,medium.com,article,en,nofollow,@rumer,78,active,2026-10-23,my pages,
healthboards,healthboards.com,forum,en,nofollow,rumer_k,72,testing,2026-10-23,my pages,first 3 posts
```

| Column | Meaning |
|---|---|
| `platform` | slug, the same as `platform` in the journal |
| `domain` | registrable domain or known platform domain |
| `type` | article · community · forum · q&a · document · site-builder · page · newsletter · social · video · event · fundraising · portfolio … |
| `language` | main language the user publishes in there |
| `links` | dofollow · nofollow · ugc · none · removed |
| `account` | account name or note (never passwords) |
| `score` | last platform-analyzer score 0–100 |
| `state` | active · testing · paused · dropped · dead |
| `added`, `source` | when and how it entered the base: my pages, journal, manual, analyzer |

One row per platform, updated in place (`platform-set`). Page counts, statuses and sales are never stored here: `platforms` computes them from the journal and sales files.

Imported pages (`import-pages`) are `published` rows with the note "imported from <file>"; until their first `check` they are listed in the check queue as one bulk check, not page by page.

## Schedules

- Alive + index check: day 2, 7, 14 after publishing, then every 14 days; after `not-indexed`, in 3 days. Server (Pro) checks daily and its results come in as `check` rows.
- Audit: at publishing, after every `refreshed`, and at the 14/30/60-day review. Under 70 = needs improvement.
- Sales upload: per program with live pages, if nothing was imported or logged for 7 days; export at least monthly even with manual logging.
