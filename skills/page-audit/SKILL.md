---
name: page-audit
description: Audit a parasite SEO or affiliate page by link or pasted text and find why it does not get clicks or sales — snippet and title, first screen, quick facts and deals box, author block, table of contents and headings, structure for the content type, CTAs, honesty and disclosure, platform fit, readability, indexing — with a 0–100 score and a prioritized fix list; for agencies, client pages are scored on the brand scale (disclosure, brand voice, UTM links, design in the client's style) before the client sees them. Use when the user asks to check, review, audit or improve a page, article or post, asks "why no sales", or before publishing a draft.
---

# Page Audit

## Work label (testing period)

Start every reply produced by this skill with one line naming it, so the user always sees which part of PARASITER is working:
`▸ PARASITER · page-audit`
If you called agents for this reply, add them after an arrow: `▸ PARASITER · page-audit → serp-analyst, product-researcher`. If you hand off to another skill, the next reply carries that skill's label. One line only, no other system talk.

## Show what the next plan opens — RULE (№56)

Free skill. After its result, a Free user (no key or Free key) gets the "🔒 On Pro / Insider this step would also" block with the lines for this skill from `navigator/references/upgrade-showcase.md` §3, made concrete for what was just done; a Pro user gets the one Insider line. At most one block per reply, below the result, never on error or bad-news replies; `upsell: compact` in the profile → one line per session.

## Plugin basis and Claude plan — RULE (№33)

Every answer here is PARASITER at work: this skill's steps, Rumer's rules, criteria and references — never general knowledge alone. Name the basis briefly where it matters ("by Rumer's rules", the checklist, score or reference used, "PARASITER platform base"). A request this skill doesn't cover → the right skill; nothing fits → one line "outside PARASITER's skills — I answer by Rumer's general rules", then "0 — menu". Full rule: `navigator/references/agents-and-plan.md`.

**Agents and Claude plan.** Heavy step: the audit itself → agent `independent-auditor`. Mode: `agents:` in `parasite-seo-profile.md`, else `agents_default` from `account_info`.
- `on` (Claude Max, Team) → run the agent; label `▸ PARASITER · <skill> → independent-auditor`.
- `lite` (Claude Pro) → the **Lite version** below, label `▸ PARASITER · <skill> · Lite`. When the full version would clearly give a better result here, add one line of advice — why, and the phrase **full** ("For 20 products the full version is better: independent-auditor checks every one, about 3–5× more of your Claude limits. Say **full** — or I keep Lite").
- `offer` (plan not known) → ask once before the first run: "This step of the skill is done by PARASITER's independent-auditor agent: separate context, deeper, uses more of your Claude limits (best on Max). Run it? Or Lite with the same skill."
- "full" / "audit by agent" → run it this time; "turn on agents" → `agents: on`; "save limits" or a usage limit hit → `agents: lite` (save in the profile, advice from `agents-and-plan.md` §3).

**Lite version:** self-check by `references/audit-checklist.md` with the score from `references/scoring.md`, labelled **"not independent"**. Exception in every mode: a page written in this conversation always gets the offer of `independent-auditor`, with the reason (it hasn't seen how the text was written). Lite is the same method in a smaller scope: say what was left out.

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
- If the article already carries the writer's self-check line ("Check by Rumer's rules: N/100 …"), don't offer an audit first: option 1 is "write the next one" (the next topic of the approved list) or "I published" (send the links), and a full audit only as the last option.
- "apply the fixes" — rewrite with every fix
- "second opinion" — a fresh-eyes review
- "make the snippet photo"

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
12. **AI-ready (0–5)** — answer first, quotable facts with dates, named comparison table, Q&A block, clear entities (`audit-checklist.md`, "AI answers"). Reported as its own line, not part of the two scores.

## Step 3 — Score and report

Score with `references/scoring.md`: **two scores — Rumer's rules and Copywriting — and their average.** When the independent auditor ran, show its scores too and explain any gap of more than 10 points. Report:

```
Page score NN/100 · [type] · [platform]
Rumer's rules NN/100 (client pages: Brand rules NN/100) · Copywriting NN/100
AI-ready N/5 — [what is missing, if anything]
Critical (fix first)
• … — why it costs sales — exact fix
Medium
• …
Good
• …
Fastest win: [one change]
```
If there is no photo under the title, it is always in the list: "Add a real product photo at the top — it is what Google takes for the snippet image." Then the free way, in this order (from `post-illustrations`, "How we work with images"): the user's own or the merchant's real product photo; otherwise one ready cover prompt in a code block with the link [Open Gemini](https://gemini.google.com) — free, about 30 seconds (ChatGPT / DALL·E only if the user already pays for it). Missing infographics: Claude draws them in the chat as JPG for free. If the user hasn't heard it yet, add the one line once: "How we work with images: infographics I draw myself, the cover is made free in Gemini from my prompt — 30 seconds."

Give rewritten fragments for the top 1–3 critical issues (new title, quick facts box, author intro, CTA) — ready to paste. Offer to rewrite the whole page with sales-review-writer.

## Rules

- Judge only what is on the page; mark assumptions.
- Never "fix" by adding invented facts, reviews or urgency. Missing facts → `[VERIFY: …]` and ask the user.
- Re-audit after fixes and show the score change.
- If the page has a URL, log the score in the work journal as an `audit` row (`work-log`); after fixes, log `refreshed` and the new `audit`.
