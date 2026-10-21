---
name: content-type-selector
description: Choose WHAT to write before writing — the content type and topic that sells for a given product (A vs B comparison, personal experience, complaints/doubts, packages and pricing, discounts, real discussions, selection tools, original research, decision-tool "best of"). Use whenever the user wants to write, plan or pick a topic for a parasite SEO or affiliate post, asks "what should I write about", or before any conversion content is drafted.
---

# Content Type Selector

Part of PARASITER by Rumer (Affiliate Credo).

Core principle: **do not publish one more retelling of the product. Publish the best answer to a specific doubt the buyer has right before purchase.**

AI answers now cover the basics ("what is it", "how it works", "pros and cons"). People still click when they need what AI cannot give in two sentences: proof, real experience, fresh buying conditions, a detailed comparison, or a recommendation for their specific situation. This skill finds that gap and turns it into a topic.

Reply in the user's language. Keep questions short; ask only what you cannot infer.

## Step 1 — Get the inputs

Ask for (skip what the user already gave):

1. **Product** they promote (and the affiliate offer / network if known).
2. **Competing or alternative products** they know of.
3. **What they have that is unique**: real use of the product, photos, notes, own data, a discount/coupon, knowledge of packages and prices. Be explicit: "Have you personally used it? Do you have any discount or bonus?"
4. **Target country and language.**
5. **Platform** where it will be published, if already chosen (forum, publishing platform, PDF/document, own site, Reddit/Quora, etc.).

If the user does not know alternatives or modifiers, suggest them from the product category and confirm.

## Step 2 — Generate topic candidates

Use the 8 content types in `references/content-types.md` and the 7 query modifier clusters in `references/modifiers-and-serp.md`.

Produce 8–12 concrete topic candidates. Default mix:
- at least 3 comparisons (A vs B, alternatives, standard vs deluxe),
- at least 2 doubts/complaints ("is it legit", "complaints", "worth it"),
- at least 2 purchase topics (packages, price, discount, shipping/warranty/returns),
- personal experience topics **only if the user actually has the experience**,
- research topics only if the user has (or will collect) real data.

Each candidate = a working title + the content type + the buyer doubt it answers.

## Step 3 — SERP gap check

For the top candidates, run the SERP check in `references/modifiers-and-serp.md`: AI Overview, Reddit/forums, videos, shopping blocks, manufacturer pages — on mobile and desktop in the target country.

If web search is available, send the queries of the top 4–6 candidates to the **`serp-analyst` agent** in one batch (queries, country, language). It returns the top 10 per query, the SERP features, People also ask and the open gaps. If web search is not available, guide the user through the check step by step.

The question to answer for each topic: **which buyer question is still not answered well on this results page?** That gap is the topic. If there is no gap and no clear commercial action, drop it.

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
