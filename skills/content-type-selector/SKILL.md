---
name: content-type-selector
description: Choose WHAT to write before writing — the content type and topic that sells for a given product (A vs B comparison, personal experience, complaints/doubts, packages and pricing, discounts, real discussions, selection tools, original research, decision-tool "best of"). Use whenever the user wants to write, plan or pick a topic for a parasite SEO or affiliate post, asks "what should I write about", or before any conversion content is drafted.
---

# Content Type Selector

## Work label (testing period)

Start every reply produced by this skill with one line naming it, so the user always sees which part of PARASITER is working:
`▸ PARASITER · content-type-selector`
If you called agents for this reply, add them after an arrow: `▸ PARASITER · content-type-selector → serp-analyst, product-researcher`. If you hand off to another skill, the next reply carries that skill's label. One line only, no other system talk.

## Next steps (end of every reply)

The user should always see where to go next without asking. End each reply with one short line of 2–3 options that fit what just happened, each with the phrase to say, e.g. `Next: `sales-review-writer` (write it now) · `platform-analyzer` (check the platform first) · `post-illustrations` (cover and infographic).` Offer only what their plan includes; a Pro/Insider feature on Free is named once with its plan in brackets. When the user seems lost or asks what else there is, add: "All PARASITER functions: say **help**." Things that need no decision (logging, monitoring, saving to the base) are done automatically, not offered.

Part of PARASITER by Rumer (Affiliate Credo).

Core principle: **do not publish one more retelling of the product. Publish the best answer to a specific doubt the buyer has right before purchase.**

AI answers now cover the basics ("what is it", "how it works", "pros and cons"). People still click when they need what AI cannot give in two sentences: proof, real experience, fresh buying conditions, a detailed comparison, or a recommendation for their specific situation. This skill finds that gap and turns it into a topic.

Reply in the user's language. Keep questions short; ask only what you cannot infer.

**Agency role:** the product, competitors, queries, country and voice come from `clients/<slug>/client-brief.md`; ideas come from the client's content plan and `brand-presence` gaps. The same buyer-doubt logic applies, in formats a brand can publish honestly: how to choose, best-of with the brand disclosed as one of the options, [brand] vs [competitor] by the brand's team, alternatives to [competitor], price / plans explained, case study, problem → solution. "Personal experience" needs a real person at the client who used it — otherwise drop it; "my rating" is never used for the brand's own product. The brief goes to `sales-review-writer` brand mode.

## Step 1 — Get the inputs

If the user doesn't know what or where to write, start from their own base: `work-log` `coverage` lists proven topics (top 10, earning, priority) missing on their strong platforms. Offer the top 3 gaps ("glp1 patch review → Medium: #7 and earning on the forum, Medium is your priority platform"); the chosen gap gives the product, the platform and the page to learn from. The new page takes a different angle or content type from the existing one.

Ask for (skip what the user already gave):

1. **Product** they promote (and the affiliate offer / network if known).
2. **Competing or alternative products** they know of.
3. **What they have that is unique**: real use of the product, photos, notes, own data, a discount/coupon, knowledge of packages and prices. Be explicit: "Have you personally used it? Do you have any discount or bonus?"
4. **Target country and language.**
5. **Platform** where it will be published, if already chosen (forum, publishing platform, PDF/document, own site, Reddit/Quora, etc.).

If the user does not know alternatives or modifiers, suggest them from the product category and confirm.

## Step 2 — Generate topic candidates

**Commercial intent only.** Every topic must target a query people type when they are about to buy or choosing what to buy: "best …", "[product] review", "[product] vs …", "[product] results", "is [product] legit / worth it", "[product] complaints", "[product] price / discount / coupon", "where to buy [product]", "[product] alternatives". Drop informational queries — "how to take / how to use [brand]", "what is …", "dosage", "ingredients list", "login", "customer service", "cancel subscription": they bring readers, not buyers.

Find the topics through the buyer's needs, not only the product name: what problem they want solved ("best … for men over 50", "best … for joint pain", "… that actually works") and what they search on the way to buying. Use web search: Google autocomplete for "best [category]" and "[product] r…/v…", People also ask, related searches, Reddit and forum questions — keep only the commercial ones.

Use the 8 content types in `references/content-types.md` and the 7 query modifier clusters in `references/modifiers-and-serp.md`. The author's core formats, in this order:
1. **Best-of lists** ("10 / 14 / 15 best … for …") — always offered, first in the list. At least 2 best-of topics in every set, each for a different need or audience.
2. **Personal experience / my results** — when the user really used the product.
3. **A vs B** — the product against its closest competitor or alternative.
4. **Expert review** — the author's expertise and research, when there is no personal use.
Then doubts ("legit", "complaints", "worth it") and purchase topics (packages, price, discount, shipping/warranty).

Produce 8–12 concrete topic candidates. Default mix:
- at least 2 best-of lists (first),
- at least 2 comparisons (A vs B, alternatives, standard vs deluxe),
- at least 2 doubts/complaints,
- at least 1 purchase topic,
- personal experience / my results **only if the user actually has the experience** — otherwise the expert-review angle,
- research topics only if the user has (or will collect) real data.

Each candidate = a working title + the content type + the commercial query + the buyer doubt it answers.

## Step 3 — SERP gap check

For **every** candidate (web search is free), run the SERP check in `references/modifiers-and-serp.md`: AI Overview, Reddit/forums, videos, shopping blocks, manufacturer pages — on mobile and desktop in the target country.

If web search is available, send the queries of all candidates to the **`serp-analyst` agent** in one batch (queries, country, language). It returns the top 10 per query, the SERP features, People also ask and the open gaps. If web search is not available, guide the user through the check step by step.

The question to answer for each topic: **which buyer question is still not answered well on this results page?** That gap is the topic. Also check the intent: if the results page is mostly how-to guides, manufacturer FAQs or news, the query is not commercial — drop or reword it. If there is no gap and no clear commercial action, drop it.

## Step 4 — Score and pick

Score each surviving topic with the 12-point filter in `references/scoring.md` (6 criteria × 0/1/2). Show a compact table: topic, type, score, decision.

- 10–12 → test first
- 7–9 → publish when there is time
- 4–6 → reposition the topic
- 0–3 → do not publish

Say clearly: the score is a filter for ideas, not a ranking prediction.

Recommend the top 1–2 topics and explain in one sentence each why they are closest to the money.

## Step 5 — Hand off a content brief

For the chosen topic, output a brief in exactly this format, so the writing skill can use it:

```
CONTENT BRIEF
Title: …
Content type: …
Buyer doubt / intent: …
Target query + modifiers: …
Country / language: …
Platform: …
SERP gap to fill: …
Unique assets the author has: (experience, photos, data, discount…)
Products to recommend + when each is the right choice: …
Main CTA: … (one)
Must include: (table, scenarios, FAQ, disclosure, last-checked date…)
Must NOT include: invented tests, reviews, results, prices, warranty terms or clinical claims
Score: …/12
```

Then ask: "Write it now?" — and pass the brief to the content writing skill.

## Honesty rules (always)

- Personal-experience and journal content only when the user really has that experience. If not, offer a comparison, doubts or purchase-guide angle instead — never fake a "My 90-day trial".
- Discounts, prices, packages, shipping, warranty: only real, current terms the user can verify; add a last-checked date.
- Complaints content separates confirmed facts, individual complaints and opinion, and says when the product is NOT the right choice.
- Health, results and safety topics: no guaranteed outcomes, no personal experience presented as clinical evidence.
- Publish only where the platform allows the format and the links.

These rules are also why the content converts: buyers trust specific, honest pages.
