---
name: indexing
description: Get the user's parasite pages into Google fast and keep score — check what blocks indexing first, use the free ways, then send pages to the indexer the user chose (top services compared with prices, speed, refunds and API), log every submission, recheck on schedule and show which service and which platform index best. Use when the user publishes a page, says "index this / these", "not indexed", "which indexer", "how do I index faster", "send to SpeedyIndex / Omega", or the check queue lists pages not indexed.
---

# Indexing

## Work label (testing period)

Start every reply produced by this skill with one line naming it, so the user always sees which part of PARASITER is working:
`▸ PARASITER · indexing`
If you called agents for this reply, add them after an arrow: `▸ PARASITER · indexing → index-runner`. If you hand off to another skill, the next reply carries that skill's label. One line only, no other system talk.

## Next steps (end of every reply)

The user should always see where to go next without asking. End each reply with one short line of 2–3 options that fit what just happened, each with the phrase to say, e.g. `Next: "my indexing stats" · `platform-monitor` (recheck in 4 days) · `page-audit` for pages that stay out.` Offer only what their plan includes. When the user seems lost or asks what else there is, add: "All PARASITER functions: say **help**." Things that need no decision (logging, scheduling the recheck, monitoring) are done automatically, not offered.

Part of PARASITER by Rumer (Affiliate Credo). Plan: **Pro**. Reply in the user's language.

A page that is not in Google can't rank and can't earn. On parasite pages the user can't use Search Console (they don't own the site), so speed comes from three things: the platform itself, links from pages Google already crawls, and a paid indexer. This skill runs that in order and remembers what worked.

Files: `references/indexers.md` (top services, prices, refunds, API, test results, checked date), `references/methods.md` (free ways, own-site ways, what Google says, how to check). Settings live in the user's profile `parasite-seo-profile.md` under `indexing:` (service, mode, budget per page). API keys never go into a file or the chat: they go in the environment (`SPEEDYINDEX_API_KEY`, `RAPIDURLINDEXER_API_KEY`, `OMEGA_INDEXER_API_KEY`, … as named in `indexers.md`).

## Step 0 — First time: pick the setup (once, then saved)

No `indexing:` in the profile → ask in one message, with the short table from `indexers.md` (top 5 rows: service, price per URL, refund of unindexed credits, API, test result):
1. **Which indexer** — the one they already use, or Rumer's pick from `indexers.md` (say why in one line). "None, free ways only" is a valid answer.
2. **When to send:** `instant` — every new page goes to the indexer right after publishing (Rumer's way for pages that matter: costs cents, saves days) · `after-check` — free ways first, the indexer only for pages still out after the platform's usual indexing time (cheapest) · `manual` — only when the user asks.
3. **How:** by API with their key (Claude sends it, the `index-runner` agent) or by hand (Claude prepares the list, they paste it into the service's dashboard or Telegram bot).

Save the answers under `indexing:` in the profile. Change them any time the user says so.

## Step 1 — Before paying: is the page indexable?

Never send a page that can't be indexed — it wastes money and hides the real problem. For each URL (the `index-runner` agent does this for more than 3): page opens without login, no `noindex` in meta or `X-Robots-Tag`, canonical not pointing elsewhere, not blocked by robots.txt, real content (not a stub or a duplicate of the user's other page). Also read the platform's indexing speed from the user's platform base and `platform_get`: a platform that "stopped indexing new posts" or was hit by a cleanup is a reason to move the page, not to pay for it (`platform-monitor`, `work-log` `republish`).

Report blockers as: `[URL] — noindex on the page · fix: … / move to …`.

## Step 2 — Free ways (always, they cost nothing)

From `references/methods.md`, pick the 2–3 that fit what the user has, and name the exact page to use:
- **A link from a page Google already crawls**: the user's indexed pages on strong platforms (their own base — `work-log` `pages` shows indexed ones), their profile or hub page, their own site.
- **Inside the platform**: link the new post from the user's older indexed posts there, profile, collections, tags.
- **Share where crawlers come often**: X, Pinterest, a Reddit / community answer where self-links are allowed, a YouTube description.
- **Own site only**: Search Console URL Inspection, sitemap, IndexNow (Bing and others, not Google).
Say plainly what Google says (`methods.md`): links are how Google finds pages; no service can force indexing.

## Step 3 — Send to the indexer

Mode `instant`, or `after-check` and the page is still not indexed after the platform's usual time (no data → 3 days), or the user asks:
1. Show the count and the price: "12 URLs × ~$0.05 = ~$0.60 on Rapid URL Indexer, unindexed credits refunded after 14 days. Send?" Wait for yes, unless the user set a budget per page in the profile and this is within it.
2. **API**: hand the list to the **`index-runner` agent** (URLs, service, env variable with the key) — it checks blockers again, submits, returns the task ID, accepted URLs and the charge. **By hand**: give a clean list, one URL per line, and the exact place to paste it (from `indexers.md`).
3. **Log every URL at once**, no question: `work-log` `add --event submitted --url … --note "via <Service>" --cost <price per URL>`. The journal then puts the page on a recheck in 4 days (`RECHECK_AFTER_SUBMIT`) and counts the service's results.

High-value pages (★, earning, a pack for a new offer) can go to two services, one after the other, if the first fails — never both at once (you can't tell which one worked).

## Step 4 — Recheck and decide

Rechecks come from the journal's queue (`work-log` `due`) and run through `platform-monitor` (page-checker; DataForSEO checks only with the user's yes, as there). Each result is logged as `check` with indexed / not-indexed.

Still out after the recheck:
1. 4–7 days after sending → wait, it's normal for most services (`indexers.md` has typical days).
2. 14 days → one more free way (a new link from a crawled page) and resend once, preferably via the other service.
3. Still out after the second round → the page is the problem, not the indexer: `page-audit` (thin, duplicate, AI-looking text) or move it to a stronger platform (`work-log` `republish`). Say it in one line; don't keep paying.

## Step 5 — Indexing stats ("my indexing stats", "which indexer works")

```
python3 ../work-log/scripts/worklog.py index-stats parasite-seo-progress.csv [--platform medium]
```
Shows per service: sent, indexed, rate, median days, money spent, cost per indexed page; per platform: rate, how many were indexed without an indexer, median days to index; and the pages sent but not indexed yet. Read it out as 3–4 lines: which service works best for *this user's* platforms, which platforms index on their own (don't pay there), where to stop paying. Suggest switching the default service only when the numbers say so (10+ checked submissions).

## Rules

- Never say a page is indexed without a check result.
- Never claim a service guarantees indexing or "uses Google's API officially". Prices, rates and speeds in `indexers.md` are as published or tested on the date shown; say "about" and that they change.
- No CAPTCHA solving, no account creation, no payment on the user's behalf: buying credits is the user's step.
- The user's API keys stay in the environment. If they paste one into the chat, tell them to rotate it.
- Indexing is the user's own pages only.
