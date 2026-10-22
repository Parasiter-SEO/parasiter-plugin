# Journal format — parasite-seo-progress.csv

One file, shared by `work-log`, `goals`, `navigator` and `client-reports`. One row per fact. Never edit old rows; add a new one.

```
date,time,event,page_url,platform,offer,main_query,content_type,status,score,clicks,sales,revenue,minutes,note
2026-10-19,09:00,baseline,,,,,,,,,,400,,"30 live pages, 4/week, 10 h/week, $400/month"
2026-10-20,11:20,published,https://medium.com/@me/vpn-compare,medium,vpn,nordvpn vs surfshark,ab-comparison,live,,,,,90,
2026-10-20,11:35,audit,https://medium.com/@me/vpn-compare,medium,vpn,,,,82,,,,10,first screen ok
2026-10-20,11:40,submitted,https://medium.com/@me/vpn-compare,medium,vpn,,,,,,,,,GSC not available: pinged via links
2026-10-22,08:10,check,https://medium.com/@me/vpn-compare,medium,vpn,,,indexed,,,,,,
2026-10-27,18:00,stats,https://medium.com/@me/vpn-compare,medium,vpn,,,,,34,2,18.40,,from network
2026-10-29,10:00,check,https://forum-x.com/t/123,forum-x,vpn,,,removed,,,,,,
2026-10-29,10:30,moved,https://forum-x.com/t/123,forum-x,vpn,,,,,,,,,"to https://other.com/p/9"
```

## Columns

| Column | Meaning |
|---|---|
| `date` | YYYY-MM-DD, the user's local date |
| `time` | HH:MM, optional |
| `event` | see below |
| `page_url` | the page this row is about; empty for baseline / task / platform rows without a page |
| `platform` | short slug: medium, linkedin, reddit, forum-x |
| `offer` | product or program slug |
| `main_query` | the query the page targets (on `published`) |
| `content_type` | from content-type-selector: ab-comparison, top-list, single-review, deals, research… |
| `status` | see below |
| `score` | page-audit score 0–100 (on `audit`) |
| `clicks`, `sales`, `revenue` | on `stats`: for the period since the last stats row of that page. On `baseline`: monthly revenue now |
| `minutes` | time spent, if the user says |
| `note` | free text |

Older journals have only `date,event,page_url,platform,offer,status,clicks,sales,revenue,note`. Keep them; the script reads any subset of columns by name.

## Events

| Event | When |
|---|---|
| `baseline` | starting point from goals Mode 1 |
| `published` | page went live (new URL) |
| `submitted` | sent to indexing (Search Console, indexing service, links) |
| `check` | alive / index check result → `status` |
| `audit` | page-audit result → `score` |
| `refreshed` | content updated (deal box, date, CTA, blocks) |
| `moved` | page left this URL; the new URL gets its own `published` row |
| `platform` | new platform registered or tested (`platform`, `note`) |
| `stats` | clicks / sales / revenue from the network or platform |
| `task` | any other work: research, drafts, images (`note`, `minutes`) |
| `note` | anything else worth remembering |

## Statuses (on `check`, optionally on `published`)

`live` (page opens, index unknown) · `indexed` · `not-indexed` · `noindex` · `dropped` (indexed but lost ranking) · `removed` (404, deleted, banned account) · `dead` (platform gone)

A page counts as alive when its latest check is live, indexed, not-indexed or dropped. It counts as indexed only when its latest check is `indexed` or `dropped`.

## Check schedule

- Alive + index: day 2, 7, 14 after `published`, then every 14 days. After `not-indexed`: recheck in 3 days. Server (Pro) checks daily; its results come in through `monitor_status` and are logged as `check` rows.
- Audit: at publishing; again after every `refreshed`; review points at 14, 30, 60 days. Score under 70 = needs improvement.
- Not indexed 14+ days after publishing: flag for resubmit, links or move.
