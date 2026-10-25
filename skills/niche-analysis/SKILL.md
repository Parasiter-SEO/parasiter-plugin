---
name: niche-analysis
description: Analyze a niche and competitors for parasite SEO through the user's own SEO service API (DataForSEO, Serpstat, Semrush, Ahrefs or similar) or exported CSVs — keyword demand by buyer-modifier cluster, difficulty, SERP composition, which UGC/parasite platforms already rank, competitor parasite pages — and return the keywords and topics where a platform page can win. Use when the user asks whether a niche/product is worth it, wants keywords, competitors, or "where can a Medium/forum page reach the top".
---

# Niche Analysis

## Work label (testing period)

Start every reply produced by this skill with one line naming it, so the user always sees which part of PARASITER is working:
`▸ PARASITER · niche-analysis`
If you called agents for this reply, add them after an arrow: `▸ PARASITER · niche-analysis → serp-analyst, product-researcher`. If you hand off to another skill, the next reply carries that skill's label. One line only, no other system talk.

Part of PARASITER by Rumer (Affiliate Credo).

The key question is not "how big is the niche" but **"for which buyer queries do third-party platforms already rank?"** If forums, Medium, Reddit, LinkedIn or press releases sit in the top 10, a parasite page can get there too. If the top 10 is all brands and big review sites, look elsewhere.

Reply in the user's language.

## Data source

This skill needs keyword and SERP data. There are no free APIs that give it reliably, so it uses the **user's own SEO service** with their own key:
- If an SEO service connector/MCP is available in the session (DataForSEO, Serpstat, Semrush, Ahrefs…), use it.
- If not, ask the user to export from their tool: keyword list with volume and difficulty, and the top-10 URLs for the main queries (CSV). Analyse the files.
- With neither, run a limited manual version: send the main queries to the **`serp-analyst` agent** (SERP composition only, no volumes) and say so.

Setup help for connectors: `references/seo-apis.md` (DataForSEO recommended first).

**API calls are paid** (the user's balance). Before pulling volumes or SERPs, say how many queries and the rough cost, and wait for a yes (`work-log` Rules: paid checks). Start small: the 20–50 most commercial queries, not every variation.

## Step 1 — Seed

Product(s), category, competitors, country, language. Build seed queries with the 7 modifier clusters (comparison, distrust, purchase, package, experience, platform, evidence) — the same clusters the content-type-selector skill uses. **Commercial intent only**: "best …", "[product] review(s)", "vs", "results", "legit / worth it", "complaints", "price / discount / coupon", "where to buy", "alternatives". Leave out "how to take / use", "what is", "dosage", "login", "customer service" — readers, not buyers.

## Step 2 — Demand

Pull volumes for product + modifier queries; "[product] review" and "best [category]" are the first two to read — they show how popular the offer is in search (the author's main offer filter, see affiliate-finder). The author's rule: a product needs some real demand — even 100–500 searches/month confirms it. Completely unknown products only make sense inside a best-of comparison where they can be placed high honestly.

## Step 3 — SERP composition

For the top 20–50 queries get the top 10 and classify each result: brand/merchant, big review site, UGC/parasite platform (forum, Reddit, Quora, Medium, LinkedIn, Scribe, Google Sites, press release, PDF host…), video, other. Note AI Overview and the Discussions and forums block where data shows them.

When the SEO tool gives URLs but not page types, or the user has no tool, hand the queries to the `serp-analyst` agent in batches of up to 10 and merge its tables.

## Step 4 — Competitor parasite pages

List the parasite pages already ranking: platform, URL, content type, what they do well, what buyer doubt they leave unanswered (the gap). The `serp-analyst` agent's "Open gaps" section feeds this step.

## Step 5 — Output

```
Niche: [x] · [country] · data: [source, date]
| Keyword | Cluster | Volume | Difficulty | Platforms in top 10 | Opportunity |
```
Opportunity = high when volume is real, buying intent is strong and ≥1 UGC/parasite platform is in the top 10.

Then: top 5 keywords to target, which platforms rank for them in the top 10 (hand to platform-finder — those are proven platforms for this niche), and which content types fit, best-of lists first (hand to content-type-selector). Add a short note on oversaturation: products every affiliate pushes (heavy spam, refunds) convert worse no matter the ranking.

## Rules

- Volumes and difficulty are the tool's estimates; say so and show the source and date.
- The user's API key stays in their connector or environment — never ask them to paste it into the chat.
- No forecasts of income from volumes.
