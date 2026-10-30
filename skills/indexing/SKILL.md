---
name: indexing
description: Help the user get parasite pages into Google and keep score — check what blocks indexing first, the free ways, Rumer's comparison of the top indexers (prices, refunds, speed, test results) and which to use or mix, a clean list to paste into the services the user sends to themselves, then log every submission, recheck on schedule and show which service, mix and platform index best. Use when the user publishes a page, says "index this / these", "not indexed", "which indexer", "how do I index faster", "sent to SpeedyIndex / Omega", or the check queue lists pages not indexed.
---

# Indexing

## Work label (testing period)

Start every reply produced by this skill with one line naming it, so the user always sees which part of PARASITER is working:
`▸ PARASITER · indexing`
If you called agents for this reply, add them after an arrow: `▸ PARASITER · indexing → index-checker`. If you hand off to another skill, the next reply carries that skill's label. One line only, no other system talk.

## Next steps (end of every reply)

The user should always see where to go next without asking. End each reply with one short line of 2–3 options that fit what just happened, each with the phrase to say, e.g. `Next: "my indexing stats" · `platform-monitor` (recheck in 4 days) · `page-audit` for pages that stay out.` Offer only what their plan includes. When the user seems lost or asks what else there is, add: "All PARASITER functions: say **help**." Things that need no decision (logging, scheduling the recheck, monitoring) are done automatically, not offered.

Part of PARASITER by Rumer (Affiliate Credo). Plan: **Pro**. Reply in the user's language.

A page that is not in Google can't rank and can't earn. On parasite pages the user can't use Search Console (they don't own the site), so speed comes from three things: the platform itself, links from pages Google already crawls, and a paid indexer. This skill advises on all three in order and remembers what worked. **The user sends pages to indexers themselves** (their dashboard, Telegram bot or plugin), to one service or several; PARASITER never sends, never holds indexer keys and never buys credits.

Files: `references/indexers.md` (top services, prices, refunds, API, test results, checked date), `references/methods.md` (free ways, own-site ways, what Google says, how to check). Settings live in the user's profile `parasite-seo-profile.md` under `indexing:` (the services they use, alone or mixed, and when they send).

## Step 0 — First time: pick the setup (once, then saved)

No `indexing:` in the profile → ask in one message, with the short table from `indexers.md` (top 5 rows: service, price per URL, refund of unindexed credits, test result):
1. **Which indexers** — the ones they already use (one or several), or Rumer's picks from `indexers.md` (say why in one line). "None, free ways only" is a valid answer. Mixing is fine (see Step 3).
2. **When they send:** `instant` — every new page right after publishing (Rumer's way for pages that matter: costs cents, saves days) · `after-check` — free ways first, the indexer only for pages still out after the platform's usual indexing time (cheapest) · `manual` — only when the user asks.

Save the answers under `indexing:` in the profile. Change them any time the user says so.

## Step 1 — Before paying: is the page indexable?

Never send a page that can't be indexed — it wastes money and hides the real problem. For each URL (the `index-checker` agent does this for more than 3): page opens without login, no `noindex` in meta or `X-Robots-Tag`, canonical not pointing elsewhere, not blocked by robots.txt, real content (not a stub or a duplicate of the user's other page). Also read the platform's indexing speed from the user's platform base and `platform_get`: a platform that "stopped indexing new posts" or was hit by a cleanup is a reason to move the page, not to pay for it (`platform-monitor`, `work-log` `republish`).

Report blockers as: `[URL] — noindex on the page · fix: … / move to …`.

## Step 2 — Free ways (always, they cost nothing)

From `references/methods.md`, pick the 2–3 that fit what the user has, and name the exact page to use:
- **A link from a page Google already crawls**: the user's indexed pages on strong platforms (their own base — `work-log` `pages` shows indexed ones), their profile or hub page, their own site.
- **Inside the platform**: link the new post from the user's older indexed posts there, profile, collections, tags.
- **Share where crawlers come often**: X, Pinterest, a Reddit / community answer where self-links are allowed, a YouTube description.
- **Own site only**: Search Console URL Inspection, sitemap, IndexNow (Bing and others, not Google).
Say plainly what Google says (`methods.md`): links are how Google finds pages; no service can force indexing.

## Step 3 — The list to send, and logging it

Mode `instant`, or `after-check` and the page is still not indexed after the platform's usual time (no data → 3 days), or the user asks:
1. Give the **clean list** (only pages that passed Step 1, one URL per line, duplicates removed) and, for each of the user's services, where to paste it and the rough cost: "12 URLs → Rapid URL Indexer dashboard, ~$0.60, unindexed credits back after 14 days; SpeedyIndex bot, pay only for indexed." The user sends it themselves.
2. **Mixing services** is the user's choice and often sensible: one cheap service for every page, a strong second one (Indexceptional) for ★ and earning pages, or a different service per platform. Say the trade-off once: sent to two at the same time, you won't know which one worked — the stats show the mix as its own line.
3. When the user says they sent it ("sent", "sent to SpeedyIndex and Rapid"), **log every URL at once**, no question: `work-log` `add --event submitted --url … --note "via <Service>"` (several services: `--note "via SpeedyIndex + Rapid URL Indexer"`) and `--cost <price per URL>` if known. The journal puts the page on a recheck in 4 days (`RECHECK_AFTER_SUBMIT`) and counts results per service and per mix.

## Step 4 — Recheck and decide

Rechecks come from the journal's queue (`work-log` `due`) and run through `platform-monitor` (page-checker; DataForSEO checks only with the user's yes, as there). Each result is logged as `check` with indexed / not-indexed.

Still out after the recheck:
1. Before the service's refund window closes (SpeedyIndex 7 days, GIGA 9, IndexMeNow 10, Rapid URL Indexer 14 — `indexers.md`) → wait; resending now pays twice.
2. After the window → one more free way (a new link from a crawled page) and suggest resending once, preferably to another service (Indexceptional is the strong second try for ★ pages).
3. Still out after the second round → the page is the problem, not the indexer: `page-audit` (thin, duplicate, AI-looking text) or move it to a stronger platform (`work-log` `republish`). Say it in one line; don't keep paying.

## Step 5 — Indexing stats ("my indexing stats", "which indexer works")

```
python3 skills/work-log/scripts/worklog.py index-stats parasite-seo-progress.csv [--platform medium]
```
Shows per service (and per mix of services): sent, indexed, rate, median days, money spent, cost per indexed page; per platform: rate, how many were indexed without an indexer, median days to index; and the pages sent but not indexed yet. Read it out as 3–4 lines: which service works best for *this user's* platforms, which platforms index on their own (don't pay there), where to stop paying. Suggest switching the default service only when the numbers say so (10+ checked submissions).

## Rules

- Never say a page is indexed without a check result.
- Don't recommend ping services, the Google Indexing API or IndexNow for Google (`methods.md` says why).
- Never claim a service guarantees indexing or "uses Google's API officially". Prices, rates and speeds in `indexers.md` are as published or tested on the date shown; say "about" and that they change.
- PARASITER doesn't send pages to indexers, create accounts or buy credits: the user does. Don't ask for indexer API keys; if the user pastes one into the chat, tell them to rotate it.
- Indexing is the user's own pages only.
