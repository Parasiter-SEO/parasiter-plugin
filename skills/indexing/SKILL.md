---
name: indexing
description: Help the user get parasite pages into Google and keep score — check what blocks indexing first, the only free way (your own site + Search Console), Rumer's comparison of the top indexers (prices, refunds, speed, test results) and which to use or mix, a clean list to paste into the services the user sends to themselves, then log every submission, recheck on schedule and show which service, mix and platform index best. Use when the user publishes a page, says "index this / these", "not indexed", "which indexer", "how do I index faster", "sent to SpeedyIndex / Omega", the user uploads their base of pages, or the check queue lists pages not indexed.
---

# Indexing

## Work label (testing period)

Start every reply produced by this skill with one line naming it, so the user always sees which part of PARASITER is working:
`▸ PARASITER · indexing`
If you called agents for this reply, add them after an arrow: `▸ PARASITER · indexing → index-checker`. If you hand off to another skill, the next reply carries that skill's label. One line only, no other system talk.

## Show what the next plan opens — RULE (№56)

Pro skill. On Free or with no key, Step 0 answers with the **locked card** from `navigator/references/upgrade-showcase.md` §2 (what it would do for this user now, Insider = all 21 skills for $39 / Pro = 17 for $19, the upgrade link), then the Free alternative. Pro user: Insider-only parts of this skill are shown as 🔒 Insider where they come up, one line each.

## Plugin basis and Claude plan — RULE (№33)

Every answer here is PARASITER at work: this skill's steps, Rumer's rules, criteria and references — never general knowledge alone. Name the basis briefly where it matters ("by Rumer's rules", the checklist, score or reference used, "PARASITER platform base"). A request this skill doesn't cover → the right skill; nothing fits → one line "outside PARASITER's skills — I answer by Rumer's general rules", then "0 — menu". Full rule: `navigator/references/agents-and-plan.md`.

**Agents and Claude plan.** Heavy step: the index check of a list of pages → agent `index-checker`. Mode: `agents:` in `parasite-seo-profile.md`, else `agents_default` from `account_info`.
- `on` (Claude Max, Team) → run the agent; label `▸ PARASITER · <skill> → index-checker`.
- `lite` (Claude Pro) → the **Lite version** below, label `▸ PARASITER · <skill> · Lite`. When the full version would clearly give a better result here, add one line of advice — why, and the phrase **full** ("For 20 products the full version is better: index-checker checks every one, about 3–5× more of your Claude limits. Say **full** — or I keep Lite").
- `offer` (plan not known) → ask once before the first run: "This step of the skill is done by PARASITER's index-checker agent: separate context, deeper, uses more of your Claude limits (best on Max). Run it? Or Lite with the same skill."
- "full" / "audit by agent" → run it this time; "turn on agents" → `agents: on`; "save limits" or a usage limit hit → `agents: lite` (save in the profile, advice from `agents-and-plan.md` §3).

**Lite version:** up to 3 pages checked here (index checks may be paid — ask first, as before), the rest listed for the user. Lite is the same method in a smaller scope: say what was left out.

## Next steps (end of every reply)

The user must always know what to type next. End every reply with a short numbered block — ready phrases, not skill names:

**What's next? Reply with a number or the phrase:**
1. "<ready phrase>" — <what happens after it, a few words>
2. "<ready phrase>" — <what happens>

- 2–3 options that fit what just happened, the recommended next step first. "1", "yes", "ok", "go" means option 1. Any free wording of the same wish works too ("give me the offers").
- Each option is a complete phrase in the user's working language that they can copy, plus what it does. Never show skill or agent names here: the work label at the top already names the part that is working.
- Offer only what the user's plan includes (`account_info`, once per session). On a lower plan the last option before "0" is always one locked feature of the next plan that fits this step, marked "🔒 Pro" or "🔒 Insider" with what it gives (`navigator/references/upgrade-showcase.md`, №56).
- **During first setup** (a step in the profile's `setup:` is still open — not `done`, `skipped` or `not needed`): option 1 is the current setup step, and the setup footer from `navigator` ("First setup checklist") goes under the options — step N of 12, what is done, now, next.
- Things that need no decision (logging, monitoring, saving to the base) are done automatically, not offered.
- **0 — menu (№26):** the last option is always "**0** — menu of all functions". If something is paused (`paused:` in the profile: a day-plan task, a setup step, a draft), option 1 is "**back** to <it>". Never make an option a condition ("first publish…") — every option is an offer.
- **Mark tried:** on this skill's first real run in the session, add or update its line under `tried:` in `parasite-seo-profile.md` (`- <skill> · YYYY-MM-DD · <what, 3–6 words>`; agents too, marked `agent`). When the user seems lost or asks what else there is, add: "All PARASITER functions: say **help**."

Options that usually fit after this part (adapt to the user's products and words):
- "my indexing stats" — which service works best
- "recheck my pages" — after the waiting time
- "audit the pages that stay out of the index"

Part of PARASITER by Rumer (Affiliate Credo). Plan: **Pro**. Reply in the user's language.

A page that is not in Google can't rank and can't earn. **There are no free tricks — RULE (Rumer, №27).** Links from indexed pages, links inside the platform, posts on X, Pinterest, Reddit, YouTube descriptions, pings: in Rumer's experience none of it gets parasite pages indexed, so never offer them. Two ways only:
1. **Your own site + Google Search Console (free)** — only for users with their own site verified in Search Console: link the new page from a page of their site and request indexing of *that own page* in Search Console. No own site → don't mention this way.
2. **An indexing service (paid)** — the main way: regular services (results in days, about $0.03–0.25 per URL, `references/indexers.md`) and instant services (see "Instant indexing" below).
This skill picks the service, gives the clean list, logs what was sent and remembers what worked. **The user sends pages to indexers themselves** (their dashboard, Telegram bot or plugin), to one service or several; PARASITER never sends, never holds indexer keys and never buys credits.

Files: `references/indexers.md` (top services, prices, refunds, API, test results, checked date), `references/methods.md` (the own-site way, what Google says, blockers, how to check). Settings live in the user's profile `parasite-seo-profile.md` under `indexing:` (the services they use, alone or mixed, and when they send).

## Plan check (Pro) — before anything else

**Step 0 — Plan check.** Call `account_info` once per session (reuse it if already called). Pro or Insider, active → proceed. Free, expired or no key → the locked card (№56, `navigator/references/upgrade-showcase.md` §2) built on: "This is a Pro feature — what blocks indexing, Rumer's comparison of the top indexers, a clean list for your indexer, rechecks and stats by service. Upgrade: https://parasiter.affiliatecredo.com/?utm_source=plugin&utm_medium=upgrade&utm_campaign=indexing#pricing", then offer what works on their plan (the indexing services and prices from Rumer's list — say "which indexer should I use?"; with your own site in Search Console, the own-site way), and stop.

## Step 0 — First time: pick the setup (once, then saved)

**When:** in the first setup — right after the user's base is uploaded (navigator Message B, `work-log` Mode 0), or at setup step 8 if nothing was uploaded; later, at the first new page, whenever there is still no `indexing:` in the profile. Don't wait for the first logged publication or for a page "not indexed 14+ days".

No `indexing:` in the profile → ask in one message, with the short table from `indexers.md` (top 5 rows: service, price per URL, refund of unindexed credits, test result):
1. **Which indexers** — the ones they already use (one or several), or Rumer's picks from `indexers.md` (say why in one line). "None yet" is a valid answer (then: the own-site way if they have a verified site, otherwise the list waits until they pick a service). Mixing is fine (see Step 3).
2. **When they send:** `instant` — every new page right after publishing (Rumer's way for pages that matter: costs cents, saves days) · `after-check` — the indexer only for pages still out after the platform's usual indexing time (cheapest; some platforms index on their own) · `manual` — only when the user asks.

Save the answers under `indexing:` in the profile (first setup: mark step 8 `done`). Change them any time the user says so.

**Imported base with pages out of the index** (marked so in the user's table or export, or found by a check the user agreed to): offer them as the first task right away — Step 1 on those pages, then the clean list for the chosen indexer (Step 3).

## Batch from "I published"

Links often come in a batch after the user publishes several articles (`work-log` Mode 1, sales-review-writer Step 8). Accept the whole batch at once — plain URLs, a list, a message or a screenshot — run Step 1 on all of them and return **one clean list** (one URL per line, duplicates and blocked pages removed, blockers listed under it). The check queue gets every page: **index check at 3–7 days, positions at 14 days** — say the dates in one line.

## Step 1 — Before paying: is the page indexable?

Never send a page that can't be indexed — it wastes money and hides the real problem. For each URL (the `index-checker` agent does this for more than 3): page opens without login, no `noindex` in meta or `X-Robots-Tag`, canonical not pointing elsewhere, not blocked by robots.txt, real content (not a stub or a duplicate of the user's other page). Also read the platform's indexing speed from the user's platform base and `platform_get`: a platform that "stopped indexing new posts" or was hit by a cleanup is a reason to move the page, not to pay for it (`platform-monitor`, `work-log` `republish`).

Report blockers as: `[URL] — noindex on the page · fix: … / move to …`.

## Step 2 — Own site (free) and instant indexing

- **Own site + Search Console** — only when the profile says the user has a site verified in Search Console: "Put a link to the new page on a page of your site (a post, a hub page, the home page), then in Search Console → URL Inspection → Request indexing for **your** page. Google follows the link to the new page." Remove the link later if you like, once the page is indexed. No own site → skip this point entirely.
- **Instant indexing** — say once, in these words (translated into the working language): "There are instant indexing services: a page usually gets into the index within one to a few minutes. They are paid — one link can cost about $0.50. The specific tools are kept secret, but you can find them yourself." Never name an instant service.
- Nothing else. No links from other pages, no social posts, no pings — not even as "might help".

## Step 3 — The list to send, and logging it

Mode `instant`, or `after-check` and the page is still not indexed after the platform's usual time (no data → 3 days), or the user asks:
1. Give the **clean list** (only pages that passed Step 1, one URL per line, duplicates removed) and, for each of the user's services, where to paste it and the rough cost: "12 URLs → Rapid URL Indexer dashboard, ~$0.60, unindexed credits back after 14 days; SpeedyIndex bot, pay only for indexed." The user sends it themselves.
2. **Mixing services** is the user's choice and often sensible: one cheap service for every page, a strong second one (Indexceptional) for ★ and earning pages, or a different service per platform. Say the trade-off once: sent to two at the same time, you won't know which one worked — the stats show the mix as its own line.
3. When the user says they sent it ("sent", "sent to SpeedyIndex and Rapid"), **log every URL at once**, no question: `work-log` `add --event submitted --url … --note "via <Service>"` (several services: `--note "via SpeedyIndex + Rapid URL Indexer"`) and `--cost <price per URL>` if known. The journal puts the page on a recheck in 4 days (`RECHECK_AFTER_SUBMIT`) and counts results per service and per mix.

## Step 4 — Recheck and decide

Rechecks come from the journal's queue (`work-log` `due`) and run through `platform-monitor` (page-checker; DataForSEO checks only with the user's yes, as there). Each result is logged as `check` with indexed / not-indexed.

Still out after the recheck:
1. Before the service's refund window closes (SpeedyIndex 7 days, GIGA 9, IndexMeNow 10, Rapid URL Indexer 14 — `indexers.md`) → wait; resending now pays twice.
2. After the window → suggest resending once, preferably to another service (Indexceptional is the strong second try for ★ pages).
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
