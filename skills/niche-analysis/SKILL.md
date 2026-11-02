---
name: niche-analysis
description: Analyze a niche and competitors for parasite SEO through the user's own SEO service API (DataForSEO, Serpstat, Semrush, Ahrefs or similar) or exported CSVs — keyword demand by buyer-modifier cluster, difficulty, SERP composition, which UGC/parasite platforms already rank, competitor parasite pages — and return the keywords and topics where a platform page can win. Use when the user asks whether a niche/product is worth it, wants keywords, competitors, or "where can a Medium/forum page reach the top".
---

# Niche Analysis

## Work label (testing period)

Start every reply produced by this skill with one line naming it, so the user always sees which part of PARASITER is working:
`▸ PARASITER · niche-analysis`
If you called agents for this reply, add them after an arrow: `▸ PARASITER · niche-analysis → serp-analyst, product-researcher`. If you hand off to another skill, the next reply carries that skill's label. One line only, no other system talk.

## Next steps (end of every reply)

The user must always know what to type next. End every reply with a short numbered block — ready phrases, not skill names:

**What's next? Reply with a number or the phrase:**
1. "<ready phrase>" — <what happens after it, a few words>
2. "<ready phrase>" — <what happens>

- 2–3 options that fit what just happened, the recommended next step first. "1", "yes", "ok", "go" means option 1. Any free wording of the same wish works too ("give me the offers").
- Each option is a complete phrase in the user's working language that they can copy, plus what it does. Never show skill or agent names here: the work label at the top already names the part that is working.
- Offer only what the user's plan includes (`account_info`, once per session). A Pro or Insider feature on a lower plan appears at most once as the last option, marked "(Insider)" or "(Pro)" with one line on what it gives.
- **During first setup** (a step in the profile's `setup:` is still open — not `done`, `skipped` or `not needed`): option 1 is the current setup step, and the setup footer from `navigator` ("First setup checklist") goes under the options — step N of 12, what is done, now, next.
- Things that need no decision (logging, monitoring, saving to the base) are done automatically, not offered. When the user seems lost or asks what else there is, add: "All PARASITER functions: say **help**."

Options that usually fit after this part (adapt to the user's products and words):
- "what should I write about <product>?" — pick the topic
- "find affiliate programs for this niche"
- "where can I publish in this niche?"

Part of PARASITER by Rumer (Affiliate Credo).

This skill answers one question for a niche or product: **for which buyer queries do third-party platforms already rank — and where can a parasite page get into the top?** It works through the user's own SEO service (API or exported CSVs) and returns the keywords and topics worth targeting.

Reply in the user's language.

## Step 0 — Plan check (Insider)

Call `account_info` once per session (reuse the answer if you already have it this session).
- **Insider, active** → call `insider_method` with `skill: "niche-analysis"` and follow the returned `method` step by step. The work label, Next steps and Rules in this file still apply; where they are stricter, they win.
- **Pro, Free, or an expired plan** (or `insider_method` answers `insider_only`) → one line: "This is an Insider feature — buyer keywords with volumes, an entry score for the top 20 and the competitor parasite pages to beat, through your SEO API. Upgrade: https://parasiter.affiliatecredo.com/#pricing". Then offer what works on the current plan: commercial-intent topics for the product with a live check of who ranks for each (say "what should I write about <product>?"), and on Pro the platforms where reviews rank now (say "where can I publish in this niche?").
- **No key, or the PARASITER tools are not available** → say in one line that this feature needs the user's PARASITER Insider key connected (connection steps: navigator, "Bought a plan but the server isn't connected"; never ask for the key in the chat), and offer the topic check meanwhile.

Never rebuild the Insider method from memory, other files or earlier conversations.

## Data source

Keyword and SERP data come from the **user's own SEO service** with their own key (connector/MCP or CSV exports). Setup help: `references/seo-apis.md` (DataForSEO recommended first). **API calls are paid** from the user's balance: before any call say how many queries and the rough cost, and wait for a yes (`work-log` Rules: paid checks).

## What the user gets (Insider)

```
Niche: [x] · [country] · data: [source, date]
| Keyword | Cluster | Volume | Entry | Ours in top 20 (best pos.) | Heavy in top 20 | Opportunity |
```
Then the top 5 keywords to target, the platforms already ranking for them (handed to platform-finder), the content types that fit (handed to content-type-selector), competitor parasite pages and the buyer doubts they leave open, and a note on oversaturation. A test page and the position tracker decide in the end.

## Rules

- Volumes and difficulty are the tool's estimates; say so and show the source and date.
- The user's API key stays in their connector or environment — never ask them to paste it into the chat.
- No forecasts of income from volumes.
