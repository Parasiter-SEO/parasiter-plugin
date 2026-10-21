---
name: platform-feed
description: Show the author's feed of new platforms, top-platform lists and weekly parasite SEO market analysis from the PARASITER server, and turn it into actions for the user's niche and level. Use when the user asks "what's new", "new platforms", "top platforms this week", "market analysis", "what changed after the Google update", or the navigator reports fresh feed items.
---

# Platform Feed

Part of PARASITER by Rumer (Affiliate Credo).

The feed is the author's live work: new platforms as he finds them, ranked top-platform lists, weekly market analysis (what died, what came back, what Google changed). It is updated as findings appear — several times a week, sometimes less. **Never describe it as daily.**

Reply in the user's language.

## Requires the server

Tools: `feed_latest` (new platforms and notes), `analysis_latest` (weekly analysis and top list), `account_info` (plan).

If they are not available: say the feed comes with a Pro key, explain in one line what it contains, and offer platform-finder for a live search instead. Do not invent feed items.

## Step 1 — Fetch

- "What's new" → `feed_latest` since the user's last check (or last 14 days).
- "Top platforms" / "market analysis" → `analysis_latest`.
- Plan shapes what comes back: Pro sees new platforms ~7 days after they are found; Insider the same day. If the user is on Pro, you may mention once that Insider gets them first — no pressure.

## Step 2 — Present

New platforms:
```
New platforms (since [date])
| Platform | Type | Language | Indexing | Links | Note from Rumer | Found |
```
Weekly analysis: a 4–6 line summary in your words (what died, what is rising, what to do), then the top list as a table. Keep the author's notes and any identifiers in the server text unchanged.

## Step 3 — Make it actionable

Filter by the user's niche, language and level (profile from navigator if available):
- Beginner: one platform to try, with platform-analyzer first.
- Intermediate/advanced: which 2–3 platforms to test this week, and which platforms from their own list to reduce after the latest changes.

End with one next step.

## Rules

- Feed data is for the subscriber's own use; do not reformat it into a shareable list for publishing elsewhere.
- Everything is a snapshot with a date; platforms change fast — recheck before posting.
- No income claims from the analysis.
