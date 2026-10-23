---
name: platform-feed
description: The PARASITER news feed from the author — new platforms, plugin updates, ideas, weekly market analysis, polls and announcements — from the server, turned into actions for the user's niche and time; also connects the user's Telegram for the Pro / Insider channels, the Insider group and personal notifications. Use when the user asks "what's new", "any updates", "new platforms", "top platforms this week", "market analysis", "what changed after the Google update", "poll results", "connect Telegram", "Telegram notifications", or the navigator reports unseen news.
---

# PARASITER Feed

Part of PARASITER by Rumer (Affiliate Credo).

The feed is the author's live work: new platforms as he finds them, plugin updates, ideas and tips, weekly market analysis (what died, what came back, what Google changed), polls and announcements. It is updated as findings appear — several times a week, sometimes less. **Never describe it as daily.**

The same news goes out in three places: here in Claude, in the Telegram channel of the user's plan (PARASITER Pro or PARASITER Insider), and — for Insider — the private group. Personal notifications (pages that died, weekly sales reminder, billing) come from the PARASITER bot.

Reply in the user's working language.

## Requires the server (Pro or Insider)

Tools: `news_latest`, `news_seen`, `feed_latest`, `analysis_latest`, `account_info`, `telegram_link`, `telegram_status`, `telegram_settings`, `telegram_unlink`.

If they are not available, or the plan is Free: say in one line that the feed and Telegram channels come with Pro and Insider, what they contain, and offer platform-finder for a live search instead. Do not invent feed items, updates or poll results.

## Mode 1 — What's new

1. `news_latest` (default: since the user last saw news). For platform details also `feed_latest`; for the full weekly analysis `analysis_latest`.
2. Present by type, newest first, most useful first:
```
What's new · since [date]
Platforms: [n] new — [name: type, language, note] …
Update: PARASITER [version] — [what changed for you in one line]
Idea from Rumer: [one line]
Analysis: [3–4 lines in your words]
Poll: [question] — [results so far, or "vote in the Telegram channel"]
```
   New platforms as a table when there are more than 3:
   `| Platform | Type | Language | Indexing | Links | Note from Rumer | Found |`
3. Make it actionable for this user's niche, language and time: no live pages yet — one platform to try, with platform-analyzer first; otherwise 2–3 platforms to test this week and which of their platforms to reduce after the latest changes. For an `update`, say what the user can now do and the phrase to start it.
4. Call `news_seen` after showing, so the navigator does not repeat it.

Plan shapes what comes back: Pro sees new platforms ~7 days after they are found, Insider the same day. On Pro you may mention once that Insider gets them first — no pressure.

## Mode 2 — Connect Telegram

"Connect Telegram", "I want notifications", or the navigator's one-time offer to a paid user who has not linked:
1. `telegram_status`. Already linked → show what is on and the chats joined.
2. Not linked → `telegram_link`, then:
   "Open this link and press **Start**: [link] (valid 30 minutes). The bot will confirm and send you invites to [PARASITER Pro channel] / [PARASITER Insider channel and the Insider group]."
   Telegram bots cannot write to someone first, so this link is the only way — a username is not enough.
3. Explain the personal notifications in 4 short lines (page alerts, Monday sales reminder, news digest, billing), at most one message a day, quiet at night, and that any type can be turned off.
4. "Turn off X" → `telegram_settings`. "Disconnect Telegram" → `telegram_unlink` (channel access also ends; reconnect any time).

## Rules

- Feed and channel content is for the subscriber's own use; do not reformat it into a shareable list for publishing elsewhere, and do not suggest forwarding channel posts.
- Everything is a snapshot with a date; platforms change fast — recheck before posting.
- No income claims from the analysis or ideas.
- Never ask for the user's Telegram password, phone or code — only the bot link.
