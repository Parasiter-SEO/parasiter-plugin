---
name: niche-analysis
description: Free and Pro: 3 buyer keywords with a free competition check and the product with the best chance (web search, no SEO account). Insider: analyze a niche and competitors for parasite SEO through the user's own SEO service API (DataForSEO, Serpstat, Semrush, Ahrefs or similar) or exported CSVs — keyword demand by buyer-modifier cluster, difficulty, SERP composition, which UGC/parasite platforms already rank, competitor parasite pages — and return the keywords and topics where a platform page can win. Use when the user asks whether a niche/product is worth it, wants keywords, competitors, or "where can a Medium/forum page reach the top", or asks "3 keywords for <product>", "which product has the best chance?".
---

# Niche Analysis

## Work label (testing period)

Start every reply produced by this skill with one line naming it, so the user always sees which part of PARASITER is working:
`▸ PARASITER · niche-analysis`
If you called agents for this reply, add them after an arrow: `▸ PARASITER · niche-analysis → serp-analyst, product-researcher`. If you hand off to another skill, the next reply carries that skill's label. One line only, no other system talk.

## Show what the next plan opens — RULE (№56)

Insider skill with a **Free start (№80)**: on Free and Pro (key or no key) it runs the **Free mode — 3 keywords and the best chance** below for real. Volumes, trend, entry score, the full keyword list and competitor pages stay Insider: when the user asks for them, show the **locked card** from `navigator/references/upgrade-showcase.md` §2 (what it would do for this user now, Insider = all 16 skills + 7 agents, the upgrade link; a Pro user — "your Pro days carry over, /upgrade in the bot"), then the alternative on their plan.

## Plugin basis and Claude plan — RULE (№33)

Every answer here is PARASITER at work: this skill's steps, Rumer's rules, criteria and references — never general knowledge alone. Name the basis briefly where it matters ("by Rumer's rules", the checklist, score or reference used, "PARASITER platform base"). A request this skill doesn't cover → the right skill; nothing fits → one line "outside PARASITER's skills — I answer by Rumer's general rules", then "0 — menu". Full rule: `navigator/references/agents-and-plan.md`.

**Agents and Claude plan.** Heavy step: the SERP breakdown and gap check → agent `serp-analyst`. Mode: `agents:` in `parasite-seo-profile.md`, else `agents_default` from `account_info`.
- `on` (Claude Max, Team) → run the agent; label `▸ PARASITER · <skill> → serp-analyst`.
- `lite` (Claude Pro) → the **Lite version** below, label `▸ PARASITER · <skill> · Lite`. When the full version would clearly give a better result here, add one line of advice — why, and the phrase **full** ("For 20 products the full version is better: serp-analyst checks every one, about 3–5× more of your Claude limits. Say **full** — or I keep Lite").
- `offer` (plan not known) → ask once before the first run: "This step of the skill is done by PARASITER's serp-analyst agent: separate context, deeper, uses more of your Claude limits (best on Max). Run it? Or Lite with the same skill."
- "full" / "audit by agent" → run it this time; "turn on agents" → `agents: on`; "save limits" or a usage limit hit → `agents: lite` (save in the profile, advice from `agents-and-plan.md` §3).

**Lite version:** keyword data from the user's API or CSV as usual; the SERP looked at for the 3 strongest queries only. Lite is the same method in a smaller scope: say what was left out.

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
- **Mark tried:** on this skill's first real run in the session, add or update its line under `tried:` in `parasite-seo-profile.md` (`- <skill> · YYYY-MM-DD · <what, 3–6 words>`; agents too, marked `agent`). **Usage stats (№78):** at the same moment call `usage_event` with the skill name (and once more with `agent` when an agent runs; `mode` lite or full) — names only, never a page, product, query or text; skip it when the profile says `usage_stats: off`, the key is missing, or the server tools are unavailable. When the user seems lost or asks what else there is, add: "All PARASITER functions: say **help**."

Options that usually fit after this part (adapt to the user's products and words):
- "3 keywords for <product>" / "which of these products has the best chance?" — free check (№80)
- "what should I write about <product>?" — pick the topic
- "find affiliate programs for this niche"
- "where can I publish in this niche?"

Part of PARASITER by Rumer (Affiliate Credo).

This skill answers one question for a niche or product: **for which buyer queries do third-party platforms already rank — and where can a parasite page get into the top?** It works through the user's own SEO service (API or exported CSVs) and returns the keywords and topics worth targeting.

Reply in the user's language.

## Step 0 — Plan check (Insider)

Call `account_info` once per session (reuse the answer if you already have it this session).
- **Insider, active** → call `insider_method` with `skill: "niche-analysis"` and follow the returned `method` step by step. The work label, Next steps and Rules in this file still apply; where they are stricter, they win.
- **Pro, Free, expired or no key** (or `insider_method` answers `insider_only`) → **Free mode — 3 keywords and the best chance** (next section), never a bare locked card.
- **The Insider method needs the user's Insider key connected** (connection steps: navigator, "Bought a plan but the server isn't connected"; never ask for the key in the chat). The Free mode works without any key.

## Free mode — 3 keywords and the best chance (Free, Pro, no key — №80)

Why: before writing, the user must know **which product and which query a platform page can actually win**. This mode costs nothing: free web search (and the user's own free SerpApi plan if connected), no paid SEO account, no server data.

**Input:** 1–3 products (the user's own, or picked from Rumer's starter programs — `starter_offers`), country and language (from the profile; ask once if missing). More than 3 products → take the first 3 and say so.
**Only a niche, no product yet** ("VPN", "joint supplements") → the check is always on products, so first find 2–3 candidates: `starter_offers(niche)` when the niche is there (products of beginner-friendly programs), otherwise the products most reviewed in Google's top for "best <niche>" / "<niche> review" (web search). Show them in one line and go on with the check — no extra question. **One product only** → check its 3 keywords; if its best chance is "low", suggest 1–2 alternatives in the same niche and check them too.

1. **Candidates per product (by Rumer's buyer clusters):** `<product> review`, `<product> vs <closest rival>`, `is <product> legit` / `<product> scam`, `<product> side effects` or `<product> complaints` (health / money niches), `best <category> for <use>`, `<product> price` / `<product> discount`, `<product> alternatives`. Keep only commercial intent.
2. **Demand, free signals only — never invent volumes:** the query shows reviews, comparisons or forum threads in the results; "People also ask" and related searches repeat it; real forum / Reddit / Quora threads ask it; the user's SerpApi (if connected) — Google Autocomplete for "<product> " (1 search per product). Not connected → one line: "Connect SerpApi's free plan (250 searches a month) and this check uses the real Google top 10 for your country" — setup in `references/seo-apis.md`. Mark each candidate: **demand: clear / some / unclear**. No signal → drop it.
3. **Competition — who ranks now (top 10, the user's country):** the user's SerpApi when connected (№83: `serpapi_run`, 1 search per keyword; say how many of the month's searches it used and how many are left — it is the real Google top 10 for that country), otherwise web search. Then count **heavy** results (the brand's own site, Amazon and big retailers, big media) and **platform pages** (forums, Medium, LinkedIn, Quora / Reddit, PDF / document hosts, flipbooks, YouTube, free site builders). Note the "Discussions and forums" block and AI Overview.
4. **Chance per keyword:** **high** — 3+ platform pages in the top 10, or a "Discussions and forums" block · **medium** — 1–2 platform pages · **low** — none, only brands and big media. Pick the **3 best keywords** (high first; a low one only if nothing better, marked so).
5. **Show it as one table (working language):**
```
3 keywords · <product> · <country> · free check, <date>
| # | Keyword | Type | Demand | Who ranks (top 10) | Platform pages | Chance | What to write |
```
   "Who ranks" in a few words ("brand, Amazon, 3 forums, 1 Medium"). "What to write" = the content type that fits (review, A vs B, legit / complaints, best-of). Under the table, one line: "Free check by live search: no volumes. Exact volumes, trend, entry score and the full keyword list — 🔒 Insider."
6. **2–3 products → the best chance:** one line per product (its best keyword and chance), then a clear pick: "**Start with <product>: '<keyword>' — <n> platform pages in the top 10, a page like yours can get in.**" Equal chances → the one with the easier program approval / clearer offer.
7. **Hand-off:** save the 3 keywords under `keywords:` in `parasite-seo-profile.md` (product, keyword, chance, date). Next step: topics for the chosen keyword (`content-type-selector`, it uses these keywords), then the platform that already ranks for them (`platform-finder`; Free key — the 50-platform base).

**Agents:** the top-10 checks are the `serp-analyst` job when agents are on (Claude Max / Team); on Claude Pro (Lite) check the 3 best candidates here and say the rest were skipped. Never present the free check as exact data.

Never rebuild the Insider method from memory, other files or earlier conversations.

## Data source

Keyword and SERP data come from the **user's own SEO service** with their own key (connector/MCP or CSV exports). **No paid SEO account → the free-data mode of the Insider method** (SERPs via SerpApi's free plan or web search, demand and trend from free signals and Google Trends): never stop at "you need an SEO account". Setup help: `references/seo-apis.md` (DataForSEO recommended first). **API calls are paid** from the user's balance: before any call say how many queries and the rough cost, and wait for a yes (`work-log` Rules: paid checks).

## What the user gets (Insider)

```
Niche: [x] · [country] · data: [source, date]
| Keyword | Cluster | Volume | Trend 12 mo | Season | Entry | Ours in top 20 (best pos.) | Heavy in top 20 | Opportunity |
```
Plus the niche's demand line: growing or falling over a year (%), seasonal or steady (peak months), and where it is now — from the same volume data, no extra paid queries. Then the top 5 keywords to target, the platforms already ranking for them (handed to platform-finder), the content types that fit (handed to content-type-selector), competitor parasite pages and the buyer doubts they leave open, and a note on oversaturation. A test page and the position tracker decide in the end.

## Rules

- Volumes and difficulty are the tool's estimates; say so and show the source and date.
- The user's API key stays in their connector or environment — never ask them to paste it into the chat.
- No forecasts of income from volumes.
