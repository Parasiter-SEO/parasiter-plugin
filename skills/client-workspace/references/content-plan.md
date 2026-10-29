# Monthly content plan — format

Saved as `clients/<client-slug>/content-plan.md`, one section per month, newest on top. Sent to the client for approval; only `approved` rows go to production.

```markdown
## November 2026 · Acme · 12 pieces + 4 profiles · status: sent for approval 2026-10-29

Focus: [the 2–3 queries / products this month moves]

| # | Date | Topic / angle | Target query | Platform | Format | Destination (UTM) | Owner | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | Nov 3 | Best [category] for [audience] in 2026 — Acme among 8 options, disclosed | best [category] | Medium (brand account) | best-of guide 1,800 words | /product?utm_source=medium&utm_medium=parasite&utm_campaign=acme-2026-11&utm_content=md-best-category | Anna | approved |
| 2 | Nov 4 | Acme vs [competitor]: honest comparison by Acme's team | acme vs competitor | LinkedIn article | A vs B | /compare?… | Anna | idea |
| 3 | Nov 6 | How to choose [category]: 7 questions buyers ask | how to choose [category] | Pressbooks chapter | guide | /guide?… | Max | idea |
| P1 | Nov 2 | Open brand profile | — | Quora (brand account) | profile + 2 answers | site | Max | approved |

Statuses: idea → approved → written → client-approved → published → checked
Notes from client: […]
```

## How to build it

- **Topics:** decision and commercial intent first (best, vs, alternatives, price, how to choose, review of the category, problems the product solves). Informational "what is" topics only when the client needs awareness and accepts it.
- **Platforms:** the client's own declared profiles first (LinkedIn page, Medium, YouTube descriptions, brand Reddit / Quora accounts where the community allows brand participation), then fresh checked platforms from `platform-feed` / `platform-finder` (agency filter: brand-safe, allows declared brand content).
- **One topic → several platforms** in the same month, each a new angle and format (work-log `rollout`), never a copy.
- **Profiles:** each missing or weak profile from `brand-presence` is its own row (P1, P2…).
- **Volume:** as the contract says; spread evenly over the month; the main query's pieces go first.
- **Approval message to the client:** the table, 3 lines on why this plan (queries, platforms, what we expect to move — no guarantees), and the question "Approve all, or tell us which rows to change?"
