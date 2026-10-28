---
name: platform-analyzer
description: Break down one parasite SEO platform before investing time in it — affiliate reviews ranking in the top 10 there, registration, indexing of fresh pages, noindex, moderation and keyword filters, account warm-up, content limits, free or paid, stability — and give a 0–100 score with a verdict on what to publish there. Use when the user asks "should I post on X", "is X still working", "analyze this platform/forum", or before the first post on a new platform.
---

# Platform Analyzer

## Work label (testing period)

Start every reply produced by this skill with one line naming it, so the user always sees which part of PARASITER is working:
`▸ PARASITER · platform-analyzer`
If you called agents for this reply, add them after an arrow: `▸ PARASITER · platform-analyzer → serp-analyst, product-researcher`. If you hand off to another skill, the next reply carries that skill's label. One line only, no other system talk.

## Next steps (end of every reply)

The user should always see where to go next without asking. End each reply with one short line of 2–3 options that fit what just happened, each with the phrase to say, e.g. `Next: `content-type-selector` (what sells there) · `sales-review-writer` (write the first test post) · `platform-finder` (more like it).` Offer only what their plan includes; a Pro/Insider feature on Free is named once with its plan in brackets. When the user seems lost or asks what else there is, add: "All PARASITER functions: say **help**." Things that need no decision (logging, monitoring, saving to the base) are done automatically, not offered.

Part of PARASITER by Rumer (Affiliate Credo).

A platform is worth it when **review pages of affiliate products already rank there in the Google top 10 and fresh pages get indexed.** How long it will live doesn't decide anything: if it is in the top now, it goes to work now — even if it lives a day. A platform whose affiliate pages have lived 2+ weeks counts as **stable**. Whether links on it are indexed or followed doesn't matter — the page itself being indexed does. Every verdict says whether the platform is **free** (users post) or **paid** (news, PR, sponsored).

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
4. **Affiliate reviews ranking there (the main check)** — search `site:domain review` and "[product] review" for a few affiliate products: are review pages on this domain in the Google top 10, in "Discussions and forums" or AI Overview? None → the platform is not proven, however good it looks.
5. **Link to the offer** — possible anywhere (body, profile, signature, description)? Outbound warning page? Link only after N posts? Link indexing and nofollow don't matter.
6. **Moderation** — pre-moderation, keyword blacklists (platforms block typical affiliate words), automatic AI spam removal, cleanup waves, bans.
7. **Account needs** — warm-up (XenForo forums, Medium, LinkedIn need aged/active accounts), points systems, first-post limits.
8. **Content format** — length/character limits, images, tables, editor (BBCode), title uniqueness.
9. **Stability label** (not a reason to skip) — how long affiliate pages on it have lived: 2+ weeks = stable, less or unknown = new, pages being removed now = unstable.
10. **Fit** — does the platform's audience and format suit the content type and offer?

## Step 4 — Score

Score with `references/scoring.md` (0–100) and show:

```
[Platform] · score NN/100 · checked [date]
Free / Paid · Affiliate reviews in top 10: … | Indexing: … | Stability: stable / new / unstable | Link: …
Verdict: [publish now / test 1–3 posts / skip] — affiliate reviews in the top 10 now = publish now
Best content type here: …
How to post: [account, title, link placement, tone]
```

Write the result into the user's platform base: `work-log` `platform-set --platform <slug> --domain … --type … --links … --score NN --state testing|active|dropped` and a journal row `add --event platform --platform <slug> --score NN --note "verdict: …"`.

## Rules

- State what was checked live and what is assumed or from history.
- Recommend testing with 1–3 posts before scaling; never mass-post from one account.
- Respect platform rules; if links or the format are not allowed, say so instead of suggesting tricks to hide them.
- Remind: keep a copy of every text; platforms delete without notice.
