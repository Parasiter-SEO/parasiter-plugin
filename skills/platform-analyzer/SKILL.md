---
name: platform-analyzer
description: Break down one parasite SEO platform before investing time in it — registration, indexing of fresh posts, noindex, link rules, moderation and keyword filters, account warm-up, content limits, SERP presence, lifespan and removal risk — and give a 0–100 score with a verdict on what to publish there. Use when the user asks "should I post on X", "is X still working", "analyze this platform/forum", or before the first post on a new platform.
---

# Platform Analyzer

Part of PARASITER by Rumer (Affiliate Credo).

A platform is worth it when three things are true: **Google indexes and ranks fresh pages on it, readers can reach your offer from it, and your page survives long enough to sell.** Everything else is detail.

Reply in the user's language.

## Step 1 — Inputs

Platform domain (or a URL of a post on it), the niche/offer, language, and whether the user already has an account (age, activity).

## Step 2 — Server data (Pro)

If `platform_get` is available, call it: last status, history (when it ranked, cleanups), the author's notes, indexing speed. Use it as the starting point and say how fresh it is. Without the server, do the checks below live.

## Step 3 — Checks

Use web search / fetch where available; otherwise give the user each check as a short instruction. Details and how to read results: `references/checks.md`.

1. **Registration** — open for new users? Captcha, app, phone, invite, paid plan, old accounts only?
2. **Fresh indexing** — are posts from the last 1–2 weeks indexed (`site:` + recent)? How fast?
3. **noindex** — meta robots and X-Robots-Tag on new posts/profiles; some platforms noindex new accounts only.
4. **Ranking** — does the platform rank for buyer queries in this or similar niches (top 10, "Discussions and forums", AI Overview citations)?
5. **Links** — allowed? live and clickable? nofollow/ugc? outbound-link warning page (hurts CTR)? link only after N posts?
6. **Moderation** — pre-moderation, keyword blacklists (platforms block typical affiliate words), automatic AI spam removal, cleanup waves, bans.
7. **Account needs** — warm-up (XenForo forums, Medium, LinkedIn need aged/active accounts), points systems, first-post limits.
8. **Content format** — length/character limits, images, tables, editor (BBCode), title uniqueness.
9. **Lifespan** — how long posts stayed in the past; cleanup history.
10. **Fit** — does the platform's audience and format suit the content type and offer?

## Step 4 — Score

Score with `references/scoring.md` (0–100) and show:

```
[Platform] · score NN/100 · checked [date]
Indexing: … | Google trust: … | Links: … | Removal risk: …
Verdict: [publish / test 1–3 posts / skip]
Best content type here: …
How to post: [account, title, link placement, tone]
```

## Rules

- State what was checked live and what is assumed or from history.
- Recommend testing with 1–3 posts before scaling; never mass-post from one account.
- Respect platform rules; if links or the format are not allowed, say so instead of suggesting tricks to hide them.
- Remind: keep a copy of every text; platforms delete without notice.
