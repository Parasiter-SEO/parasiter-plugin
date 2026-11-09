---
name: platform-monitor
description: Track which platforms and which of the user's parasite pages are alive — page up or removed, indexed or noindexed, still ranking — and tell the user what to move or republish. Checks run in the user's own Claude (on request, from the check queue or on the user's own schedule); page URLs never go to the server, only counts for a Telegram summary. Use when the user asks "are my pages alive", "is X still working", "check my links", "what died", or after a Google update.
---

# Platform Monitor

## Work label (testing period)

Start every reply produced by this skill with one line naming it, so the user always sees which part of PARASITER is working:
`▸ PARASITER · platform-monitor`
If you called agents for this reply, add them after an arrow: `▸ PARASITER · platform-monitor → serp-analyst, product-researcher`. If you hand off to another skill, the next reply carries that skill's label. One line only, no other system talk.

## Plugin basis and Claude plan — RULE (№33)

Every answer here is PARASITER at work: this skill's steps, Rumer's rules, criteria and references — never general knowledge alone. Name the basis briefly where it matters ("by Rumer's rules", the checklist, score or reference used, "PARASITER platform base"). A request this skill doesn't cover → the right skill; nothing fits → one line "outside PARASITER's skills — I answer by Rumer's general rules", then "0 — menu". Full rule: `navigator/references/agents-and-plan.md`.

**Agents and Claude plan.** Heavy step: checking the user's pages → agent `page-checker`. Mode: `agents:` in `parasite-seo-profile.md`, else `agents_default` from `account_info`.
- `on` (Claude Max, Team) → run the agent; label `▸ PARASITER · <skill> → page-checker`.
- `lite` (Claude Pro) → the **Lite version** below, label `▸ PARASITER · <skill> · Lite`. When the full version would clearly give a better result here, add one line of advice — why, and the phrase **full** ("For 20 products the full version is better: page-checker checks every one, about 3–5× more of your Claude limits. Say **full** — or I keep Lite").
- `offer` (plan not known) → ask once before the first run: "This step of the skill is done by PARASITER's page-checker agent: separate context, deeper, uses more of your Claude limits (best on Max). Run it? Or Lite with the same skill."
- "full" / "audit by agent" → run it this time; "turn on agents" → `agents: on`; "save limits" or a usage limit hit → `agents: lite` (save in the profile, advice from `agents-and-plan.md` §3).

**Lite version:** up to 3 pages checked here, the rest listed as "not checked — say **full**". Lite is the same method in a smaller scope: say what was left out.

## Next steps (end of every reply)

The user must always know what to type next. End every reply with a short numbered block — ready phrases, not skill names:

**What's next? Reply with a number or the phrase:**
1. "<ready phrase>" — <what happens after it, a few words>
2. "<ready phrase>" — <what happens>

- 2–3 options that fit what just happened, the recommended next step first. "1", "yes", "ok", "go" means option 1. Any free wording of the same wish works too ("give me the offers").
- Each option is a complete phrase in the user's working language that they can copy, plus what it does. Never show skill or agent names here: the work label at the top already names the part that is working.
- Offer only what the user's plan includes (`account_info`, once per session). A Pro or Insider feature on a lower plan appears at most once as the last option, marked "(Insider)" or "(Pro)" with one line on what it gives.
- **During first setup** (a step in the profile's `setup:` is still open — not `done`, `skipped` or `not needed`): option 1 is the current setup step, and the setup footer from `navigator` ("First setup checklist") goes under the options — step N of 12, what is done, now, next.
- Things that need no decision (logging, monitoring, saving to the base) are done automatically, not offered.
- **0 — menu (№26):** the last option is always "**0** — menu of all functions". If something is paused (`paused:` in the profile: a day-plan task, a setup step, a draft), option 1 is "**back** to <it>". Never make an option a condition ("first publish…") — every option is an offer.
- **Mark tried:** on this skill's first real run in the session, add or update its line under `tried:` in `parasite-seo-profile.md` (`- <skill> · YYYY-MM-DD · <what, 3–6 words>`; agents too, marked `agent`). When the user seems lost or asks what else there is, add: "All PARASITER functions: say **help**."

Options that usually fit after this part (adapt to the user's products and words):
- "republish my removed pages" — from their saved sources
- "audit the pages that dropped"
- "find a new home for them"

Part of PARASITER by Rumer (Affiliate Credo).

Page checks run **in the user's own Claude**, never on the PARASITER server: the server never receives the user's page addresses (privacy rule). The pages come from the user's journal (`parasite-seo-progress.csv`), the `page-checker` agent opens them, and every result is logged in the journal. Only counts and bare platform domains may go to the server (`pages_report`), so the user gets a Telegram summary and platform cleanups can be spotted across subscribers.

Reply in the user's language.

## Step 0 — Plan check (Pro)

**Step 0 — Plan check.** Call `account_info` once per session (reuse it if already called). Pro or Insider, active → proceed. Free, expired or no key → one line: "This is a Pro feature — checks of every page in your journal — alive, removed, noindex, affiliate link — on request or on your own schedule, with the republish list. Upgrade: https://parasiter.affiliatecredo.com/#pricing", then offer the Free alternative for this skill (open each page yourself in a private window (it opens, isn't removed, the affiliate link works), or audit one page by link — say "audit my article: <link>"), and stop.

## When checks run

- **On request:** "are my pages alive?", "check my pages", "what died?", after a Google update.
- **From the check queue:** the navigator puts due alive checks into today's plan (`work-log` `due`: 2, 7, 14 days after publishing, then every 14 days; ★ pages first).
- **On the user's schedule (recommended once the base has 20+ pages):** offer once — "Want me to check your pages every morning (or every Monday)? It runs in your Claude, costs nothing but Claude usage, and you get a short summary in Telegram." On yes, create a scheduled task in the user's Claude with the session's scheduling tools (the user's own task; it uses their Claude limits): prompt "PARASITER: check my pages due today (platform-monitor, free checks only), log the results, send pages_report". On Claude Pro suggest weekly, not daily. If the session can't schedule tasks, say so and keep the check queue.

## The check (free: alive, noindex, link)

1. Take the pages from the journal: due ones (`work-log` `due`), or all live pages on request, or the ones the user names. Skip pages marked removed.
2. For each URL: HTTP status (live / 404 / login wall / redirect), noindex in meta or header, affiliate link present and working. For more than 3 URLs hand them to the **`page-checker` agent** (URL, main query, platform, expected affiliate link, country) in batches of about 15.
3. Index and positions are **paid** checks on the user's own SEO account — never part of the free check (see Rules).
4. Summary, changes first:
```
Page check · [date]
Changed since [last check]:
▼ [page] — removed / noindex / dropped from top N
▲ [page] — now indexed / entered top 10
Platforms: [X] — 3 of your pages gone this week
Alive: N of M pages
```
5. **With a key:** call `pages_report` with ONLY the numbers and the bare platform domains that lost pages — `checked`, `removed`, `noindex`, `not_indexed`, `dropped`, `domains: [{domain: "example.com", removed: 2}]`. Never send page URLs, titles, queries or sub-IDs: the tool rejects them. The user's Telegram gets the counts; the list stays here.

## Actions

Most urgent first: not indexed → `indexing` (Step 4: wait, resend via another service, or fix / move the page — by days since sending); removed pages → `work-log` `republish --url` (or `--platform X --gone-only` when several died on one platform) — it lists them with their saved sources, and each is rewritten for a new home (`rollout` / platform-finder); refresh pages that dropped (page-audit); stop posting on platforms that stopped indexing.

**Platform cleanup** (a news item of kind `cleanup` in `news_latest`, or several of the user's pages gone on one platform): `republish --platform X` at once — the user's pages there that are already gone, and the source of each for republishing.

## Log every result

Every check result goes into the work journal as a `check` row (`work-log`): `status` live · indexed · not-indexed · noindex · dropped · removed, plus `--position N` when the position for the main query is known (top 10 drives the coverage advice). Priority pages (★) are checked first. Pages to check come from the journal's check queue (`work-log` `due`) — the user does not have to list them again.

## Rules

- Never claim a page is indexed or ranking without a check result; mark unknowns.
- **Privacy:** page URLs never go to the PARASITER server or to Telegram. `pages_report` gets counts and platform domains only. If the user asks the bot or the server to check a URL, explain that checks run in their Claude.
- Index and position checks run on the user's own SEO data account (DataForSEO or SerpApi's free plan; Semrush, Ahrefs, Serpstat or Ubersuggest via their connector or exports). They cost money: before a paid check say so, give the rough cost, and suggest a sample (★ pages, earning pages, the newest pack) instead of the whole base. Alive / noindex / link checks are free.
- Remind to keep a copy of every published text — that is what makes fast republishing possible.
- After a Google update: check all rankings, reduce work on platforms that lost visibility.
