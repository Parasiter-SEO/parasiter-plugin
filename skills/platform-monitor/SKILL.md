---
name: platform-monitor
description: Track which platforms and which of the user's parasite pages are alive — page up or removed, indexed or noindexed, still ranking — and tell the user what to move or republish. Uses the server's scheduled checks on Pro, or runs a manual check on a list of URLs. Use when the user asks "are my pages alive", "is X still working", "check my links", "what died", or after a Google update.
---

# Platform Monitor

## Work label (testing period)

Start every reply produced by this skill with one line naming it, so the user always sees which part of PARASITER is working:
`▸ PARASITER · platform-monitor`
If you called agents for this reply, add them after an arrow: `▸ PARASITER · platform-monitor → serp-analyst, product-researcher`. If you hand off to another skill, the next reply carries that skill's label. One line only, no other system talk.

## Next steps (end of every reply)

The user should always see where to go next without asking. End each reply with one short line of 2–3 options that fit what just happened, each with the phrase to say, e.g. `Next: republish removed pages from their saved sources (`work-log` republish) · `page-audit` for pages that dropped · `platform-finder` (a new home).` Offer only what their plan includes; a Pro/Insider feature on Free is named once with its plan in brackets. When the user seems lost or asks what else there is, add: "All PARASITER functions: say **help**." Things that need no decision (logging, monitoring, saving to the base) are done automatically, not offered.

Part of PARASITER by Rumer (Affiliate Credo).

Daily checking is a server job, not a chat job: the server checks tracked pages and platforms on a schedule; this skill reads the results and turns them into actions. Without the server it can run a one-off manual check.

Reply in the user's language.

## Mode A — Server (Pro)

Tools: `monitor_status` (status of tracked pages and platforms, changes since a date), `monitor_track` (add/remove the user's URLs with their main query).

1. Tracking is automatic, never a question: compare `monitor_status` with the journal (`parasite-seo-progress.csv`) and add every journal page that is not tracked yet with `monitor_track` (URL + main query + platform), skipping pages marked removed. Say how many were added in one line. No journal yet → ask for the list of URLs once, then track them.
2. `monitor_status` → show changes first:
```
Monitoring · [date]
Changed since [last check]:
▼ [page] — removed / noindex / dropped from top N
▲ [page] — now indexed / entered top 10
Platforms: [X] stopped indexing new posts · [Y] cleanup wave
Alive: N of M pages
```
3. Actions, most urgent first: for removed pages, `work-log` `republish --url` (or `--platform X --gone-only` when several died on one platform) — it lists them with their saved sources, and each is rewritten for a new home (`rollout` / platform-finder); refresh pages that dropped (page-audit); stop posting on platforms that stopped indexing.
4. **Platform cleanup** (a news item of kind `cleanup`, or several of the user's pages gone on one platform): `republish --platform X` at once — the user's pages there, which are already gone, and the source of each for republishing.

## Mode B — Manual check (Free)

For each URL the user gives (with web fetch/search if available; otherwise give the user the steps):
- HTTP status: live / 404 / login wall / redirect.
- noindex in meta or header.
- Indexed: `site:` or the exact title in Google.
- Position for the main query: with the user's DataForSEO account, `work-log` `scripts/rankcheck.py` checks all pages at once (Mode 9); otherwise ask for the number from their rank tracker.
- Affiliate link still present and working.

For more than 3 URLs, hand the list to the **`page-checker` agent** (URL, main query, platform, expected affiliate link, country) — split long lists into batches of about 15 — and build the summary from its tables.

Output the same summary table, marked "manual check, [date]". Suggest the server for ongoing tracking only once.

## Log every result

Every check result goes into the work journal as a `check` row (`work-log`): `status` live · indexed · not-indexed · noindex · dropped · removed, plus `--position N` when the position for the main query is known (top 10 drives the coverage advice). Priority pages (★) are checked first. Pages to check come from the journal's check queue (`work-log` `due`) — the user does not have to list them again.

## Rules

- Never claim a page is indexed or ranking without a check result; mark unknowns.
- Index and position checks run on the user's own SEO data account (DataForSEO recommended; Semrush, Ahrefs, Serpstat or Ubersuggest via their connector or exports). They cost money: before a paid check say so, give the rough cost, and suggest a sample (★ pages, earning pages, the newest pack) instead of the whole base. Alive / noindex / link checks are free.
- Remind to keep a copy of every published text — that is what makes fast republishing possible.
- After a Google update: check all rankings, reduce work on platforms that lost visibility.
