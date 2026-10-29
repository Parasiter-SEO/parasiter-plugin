---
name: page-audit
description: Audit a parasite SEO or affiliate page by link or pasted text and find why it does not get clicks or sales — snippet and title, first screen, quick facts and deals box, author block, table of contents and headings, structure for the content type, CTAs, honesty and disclosure, platform fit, readability, indexing — with a 0–100 score and a prioritized fix list; for agencies, client pages are scored on the brand scale (disclosure, brand voice, UTM links, design in the client's style) before the client sees them. Use when the user asks to check, review, audit or improve a page, article or post, asks "why no sales", or before publishing a draft.
---

# Page Audit

## Work label (testing period)

Start every reply produced by this skill with one line naming it, so the user always sees which part of PARASITER is working:
`▸ PARASITER · page-audit`
If you called agents for this reply, add them after an arrow: `▸ PARASITER · page-audit → serp-analyst, product-researcher`. If you hand off to another skill, the next reply carries that skill's label. One line only, no other system talk.

## Next steps (end of every reply)

The user should always see where to go next without asking. End each reply with one short line of 2–3 options that fit what just happened, each with the phrase to say, e.g. `Next: `sales-review-writer` (apply the fixes) · `independent-auditor` second opinion · `post-illustrations` (snippet photo).` Offer only what their plan includes; a Pro/Insider feature on Free is named once with its plan in brackets. When the user seems lost or asks what else there is, add: "All PARASITER functions: say **help**." Things that need no decision (logging, monitoring, saving to the base) are done automatically, not offered.

Part of PARASITER by Rumer (Affiliate Credo).

Ranking is not the problem — conversion is. A page that ranks but does not sell usually fails in the first screen: no reason to trust the author, no clear offer, no decision help. This audit checks the page the way a buyer reads it.

Reply in the user's language; quote page fragments in the page's language.

## Step 1 — Get the page

- **Link**: fetch it if possible. If the platform blocks fetching or needs login, ask the user to paste the text (and a screenshot of the first screen if they can).
- **Text**: use as given.
Ask: target query, content type (if unclear), platform, offer/affiliate link, country.
**Agency role:** read the client's brief (`clients/<slug>/client-brief.md`) instead of asking — query, destination, voice, approved claims and brand kit are there. Score with **Brand rules** (scoring 1b) in place of Rumer's rules, plus Copywriting. A client page goes to the client only at 75+ (the journal's check queue flags under 70, so 70–74 is yours to catch before sending); log the audit in the client's journal. When the independent auditor runs, pass it the role and the brief.

## Step 1b — Independent reader

If the page was written in this same conversation (for example by sales-review-writer), do not grade it yourself first: send the text, query, type, platform, country, the checklist and the scoring to the **`independent-auditor` agent**. It reads the page without the writing context, like a doubtful buyer. Use its report as the base and add your own findings in Step 2. For pages the user brings from outside, the agent is optional — use it when the user asks for a second opinion.

## Step 2 — Check

Run the checklist in `references/audit-checklist.md` in this order — the first screen decides most sales:

1. **Snippet** — title and description: value, keyword, a reason to click after the AI answer.
2. **First screen** — photo right under the title (for the snippet image; recommend one if missing), facts box for the main product (price, quality, my rating, offers, link), one clear CTA.
3. **Author** — who, role, why trust, why listen; real, not a generic "expert".
4. **Hook** — problem → solution → bridge → what the page gives.
5. **TOC and headings** — headings alone tell the conclusion.
6. **Structure and Rumer's blocks** — pains, facts → solution, life after, prices and offers, comparison + alternatives, 1,500+ words, plus the blocks of the content type (sales-review-writer templates).
6b. **Copywriting** — useful on its own; problem opened and solved with the product; motivates the click and the purchase; images that support the text.
7. **CTAs** — at decision points; why this product / this offer / now; best landing page.
8. **Honesty** — no fake tests, reviews, results, prices, deadlines; disclosure; last-checked date.
9. **Platform fit** — length, tone, formatting, link rules of the platform.
10. **Readability** — mobile: short paragraphs, lists, tables that fit.
11. **Technical** (link only) — indexed? noindex? links live and landing on the right page?

## Step 3 — Score and report

Score with `references/scoring.md`: **two scores — Rumer's rules and Copywriting — and their average.** When the independent auditor ran, show its scores too and explain any gap of more than 10 points. Report:

```
Page score NN/100 · [type] · [platform]
Rumer's rules NN/100 (client pages: Brand rules NN/100) · Copywriting NN/100
Critical (fix first)
• … — why it costs sales — exact fix
Medium
• …
Good
• …
Fastest win: [one change]
```
If there is no photo under the title, it is always in the list: "Add a real or custom photo at the top — it is what Google takes for the snippet image" + a prompt via `post-illustrations`.

Give rewritten fragments for the top 1–3 critical issues (new title, quick facts box, author intro, CTA) — ready to paste. Offer to rewrite the whole page with sales-review-writer.

## Rules

- Judge only what is on the page; mark assumptions.
- Never "fix" by adding invented facts, reviews or urgency. Missing facts → `[VERIFY: …]` and ask the user.
- Re-audit after fixes and show the score change.
- If the page has a URL, log the score in the work journal as an `audit` row (`work-log`); after fixes, log `refreshed` and the new `audit`.
