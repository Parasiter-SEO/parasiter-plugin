# Repeat this result (№75)

"I saw this page in the top and want the same" — the reason many of Rumer's students came to him. The user pastes a link to a page that ranks (or a query plus "the page at #3"); PARASITER shows **how it was done** and plans **the same result for the user's own product**. The pattern is taken, never the text.

**Triggers:** "repeat this result", "how did they rank this", "I want the same as this page", "break down this page", "розбери цю сторінку", "повтори этот результат", a pasted URL with "how?" / "same for me". Work label: `▸ PARASITER · navigator` (agents named after the arrow when used).

**Plan check first:** call `repeat_result` with `action=start` (every key). `allowed: false` (Free, used this week) → say when it opens (Monday) and what Pro gives, offer the Free alternatives (page audit of the page, a platform scan), stop. No key → run it, there is no counter. **Never** send the page URL to the server — `repeat_result` only counts runs.

## 1 · The breakdown (one screen)

Open the page (and its query in Google: SerpApi free plan or DataForSEO with the cost shown first; without them, web search — say it is not a Google position). Fill:

| What | On this page |
|---|---|
| Platform | domain, type, Rumer's class (proven / Web 2.0 / Web 3.0), the platform's own rules for affiliate posts (read them: allowed / limited / forbidden, link) |
| Query and position | the buyer query it ranks for, position, date checked (or "not checked") |
| Format | content type by Rumer's list (best-of, A vs B, personal experience, complaints, prices, expert review…) |
| Title and snippet | the title pattern, what the snippet promises |
| Structure | first screen, quick facts box, author block, headings, length, tables, images, CTAs |
| Links | how many, where, anchor style, follow / nofollow, a redirect domain or not |
| Age and freshness | published / updated date, comments or replies |
| Account | author profile signals (age, other posts) when visible |
| Indexing | indexed, noindex, canonical |
| Why it works | 3 lines: the 3 things that most likely put it there |

Use `platform-analyzer` for the platform rows (Pro; on Free the quick read of rules and indexing only) and `page-audit` scoring on the page itself to name its strengths. Agents (`serp-analyst`, `page-checker`) when the plan and Claude plan allow.

## 2 · The same for you

- **Product:** the user's product (profile) or ask once; no product → `starter_offers` (Rumer's starter programs).
- **Where:** the same platform if its rules allow and posting there is free; plus 2 alternatives of the same type from the platform base (Free: the 50 base).
- **What:** the same format for the user's product — `content-type-selector` confirms the topic and query; `sales-review-writer` writes it in the platform's format, the user's own facts and experience (no invented results), images by `post-illustrations`; `page-audit` 80+ before publishing.
- **How it gets found:** indexing (`indexing`) and the checks: day 3 index, day 7 position.
- Offer it as the next step: "1 — write mine for <product> on <platform>". On the beginner path, this becomes the current post (`first-post.md` Step 5 onward).

## Rules

- Learn the pattern, never copy text, images or the author's identity; no parody of competitors.
- A page that breaks the platform's rules or uses spam (fake reviews, cloaking, hacked pages) is not something to repeat: say so plainly and show the honest version.
- Results vary: a page in the top today says what works now, not what you will earn.
- Stuck or unsure? "Write to Rumer: /support in @parasiter_bot."
