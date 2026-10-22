---
name: work-log
description: The user's parasite SEO work journal. Records every action the moment it happens — page published, sent to indexing, checked alive/indexed, audited, refreshed, moved, platform tested, sales — and turns the journal into work reports for today, yesterday, a week, a month or any date range, plus a queue of pages due for alive/index checks and conversion audits. Use when the user reports work ("added an article", "indexed it", "published 3 pages", "2 sales"), asks "what did I do today / this week / in September", wants a weekly or monthly work report, or asks which pages need checking or fixing.
---

# Work Log

Part of PARASITER by Rumer (Affiliate Credo).

Every piece of work goes into one journal the moment it is done. A page that is in the journal gets checked: is it alive, is it still indexed, does it follow the conversion rules. A page that is not in the journal is invisible — it will die or drop out of the index and nobody will notice.

Reply in the working language from `parasite-seo-profile.md`. Keep the journal's column names and `event` / `status` values in English so it stays machine-readable.

## The journal

One file in the user's project folder: `parasite-seo-progress.csv` (the same file `goals` reads). One row per fact, never edit old rows — add a new one. Columns, events and statuses: `references/log-format.md`.

If the file does not exist, create it with the header row. If it has the older, shorter header, keep the old rows and continue with the full header: the script reads both.

## Mode 1 — Log as you go

Whenever the user reports work, or another skill finishes a step, add the row(s) right away — do not wait for the end of the day.

| User says / skill finishes | Rows |
|---|---|
| "Published / added an article: URL" | `published` (+ `platform`, `offer`, `main_query`, `content_type` if known) |
| "Sent it to indexing" | `submitted` |
| platform-monitor or page-checker result | `check` with `status` alive · indexed · not-indexed · noindex · removed |
| page-audit result | `audit` with `score` (0–100) |
| "Updated / refreshed the page" | `refreshed` |
| "Moved it to another platform" | `moved` on the old URL + `published` on the new one |
| "Registered / tested a new platform" | `platform` |
| "2 sales from X" / network stats | `stats` with `clicks`, `sales`, `revenue` |
| Other work (research, drafts, images) | `task` with a short `note` |

Ask only for what is missing and matters: the URL for a page, the platform, the main query. Never ask twice in a session for the same field. If the user says how long it took, put it in `minutes`.

When code execution is available, append with the script so the CSV stays valid:
```
python3 scripts/worklog.py add parasite-seo-progress.csv --event published --url https://… --platform medium --offer vpn --query "nordvpn vs surfshark" --type ab-comparison
```
Pass `--date` and `--time` in the user's local time when the machine's clock may differ (cloud sandboxes run in UTC). Otherwise append the row yourself, quoting any field with a comma.

Confirm in one line: what was logged and what happens next ("Logged: published on Medium. Index check due Oct 24, audit now?").

### Right after a `published` row

1. **Audit** — if the page has no `audit` row yet, offer page-audit now (link or text). Log the score.
2. **Track** — with the server (Pro): call `monitor_track` with URL, main query and platform so alive/index checks run on schedule. Without it, the page lands in the manual check queue (Mode 3).
3. Remind once per session to keep a copy of the text — that is what makes republishing fast.

## Mode 2 — Work report

"What did I do today / yesterday / this week / last month / in September / from 1 to 15 Oct?"

Run `python3 scripts/worklog.py summary parasite-seo-progress.csv --period <period>` (periods: `today`, `yesterday`, `week`, `last-week`, `month`, `last-month`, `YYYY-MM`, `YYYY-MM-DD`, `YYYY-MM-DD..YYYY-MM-DD`, `all`). Without code execution, count from the file the same way.

```
Work report · [period] · [dates]
Done: N published · N sent to indexing · N checks · N audits · N refreshed · N moved · N platforms tested · [time]
By day: [date — what was done]
Pages published: [url — platform — offer — status now — audit score]
Health of these pages: alive N · indexed N · not indexed N · removed N · not checked yet N
Results logged: clicks · sales · revenue (only from stats rows)
Needs attention: [from Mode 3]
```
For a week or month add: comparison with the previous period of the same length, and against `goals` targets if a goals file exists (pages published vs weekly target). For money and per-page earnings, hand off to `client-reports`.

## Mode 3 — Check queue

"What needs checking?", or at the start of a session (the navigator asks for it):

Run `python3 scripts/worklog.py due parasite-seo-progress.csv`. It lists:
- **Index / alive check due** — 2, 7 and 14 days after publishing, then every 14 days; pages whose last check was `not-indexed` are rechecked after 3 days.
- **Not indexed after 14 days** — resubmit, add internal/external links, or move.
- **Removed / noindex** — republish from the saved copy (platform-finder for a new home), log `moved`.
- **Audit due** — never audited, audited before the last refresh, or the 14/30/60-day review point reached.
- **Needs improvement** — last audit score under 70 → page-audit fixes, then `refreshed` + new `audit`.

Send checks of more than 3 URLs to the `page-checker` agent (via platform-monitor) and log every result as a `check` row. Send audits to page-audit and log the score.

## Mode 4 — Page registry

"Show all my pages" / "what's the status of my Medium pages": `python3 scripts/worklog.py pages parasite-seo-progress.csv [--platform medium]` — one line per URL with platform, age, latest status and date, last audit score, sales logged.

## Rules

- Log facts only. Never mark a page indexed or alive without a check result; "not checked yet" is a valid state.
- Never rewrite or delete old rows; corrections are new rows with a `note`.
- Reports count what is in the journal. If a period looks empty, say so and ask whether something was not logged — do not fill gaps with guesses.
- Revenue numbers come only from the user's stats; no forecasts in work reports.
- Keep the journal in the user's project; do not send it to third-party services.
