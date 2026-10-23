---
name: platform-monitor
description: Track which platforms and which of the user's parasite pages are alive — page up or removed, indexed or noindexed, still ranking — and tell the user what to move or republish. Uses the server's scheduled checks on Pro, or runs a manual check on a list of URLs. Use when the user asks "are my pages alive", "is X still working", "check my links", "what died", or after a Google update.
---

# Platform Monitor

Part of PARASITER by Rumer (Affiliate Credo).

Daily checking is a server job, not a chat job: the server checks tracked pages and platforms on a schedule; this skill reads the results and turns them into actions. Without the server it can run a one-off manual check.

Reply in the user's language.

## Mode A — Server (Pro)

Tools: `monitor_status` (status of tracked pages and platforms, changes since a date), `monitor_track` (add/remove the user's URLs with their main query).

1. If the user has no tracked pages, offer to add them: list of URLs + main query + platform. Call `monitor_track`.
2. `monitor_status` → show changes first:
```
Monitoring · [date]
Changed since [last check]:
▼ [page] — removed / noindex / dropped from top N
▲ [page] — now indexed / entered top 10
Platforms: [X] stopped indexing new posts · [Y] cleanup wave
Alive: N of M pages
```
3. Actions, most urgent first: republish removed pages elsewhere from the saved copy (platform-finder for a new home), refresh pages that dropped (page-audit), stop posting on platforms that stopped indexing.

## Mode B — Manual check (Free)

For each URL the user gives (with web fetch/search if available; otherwise give the user the steps):
- HTTP status: live / 404 / login wall / redirect.
- noindex in meta or header.
- Indexed: `site:` or the exact title in Google.
- Position for the main query (if the user has a rank tracker or Search Console, ask for the number).
- Affiliate link still present and working.

For more than 3 URLs, hand the list to the **`page-checker` agent** (URL, main query, platform, expected affiliate link, country) — split long lists into batches of about 15 — and build the summary from its tables.

Output the same summary table, marked "manual check, [date]". Suggest the server for ongoing tracking only once.

## Log every result

Every check result goes into the work journal as a `check` row (`work-log`): `status` live · indexed · not-indexed · noindex · dropped · removed, plus `--position N` when the position for the main query is known (top 10 drives the coverage advice). Priority pages (★) are checked first. Pages to check come from the journal's check queue (`work-log` `due`) — the user does not have to list them again.

## Rules

- Never claim a page is indexed or ranking without a check result; mark unknowns.
- Remind to keep a copy of every published text — that is what makes fast republishing possible.
- After a Google update: check all rankings, reduce work on platforms that lost visibility.
