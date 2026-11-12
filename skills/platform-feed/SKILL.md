---
name: platform-feed
description: The PARASITER news feed from the author — new platforms, plugin updates, ideas, weekly market analysis, polls and announcements — from the server, turned into actions for the user's niche and time; also connects the user's Telegram for the Pro / Insider channels, the Insider group and personal notifications. Use when the user asks "what's new", "any updates", "new platforms", "top platforms this week", "market analysis", "what changed after the Google update", "poll results", "connect Telegram", "Telegram notifications", or the navigator reports unseen news.
---

# PARASITER Feed

## Work label (testing period)

Start every reply produced by this skill with one line naming it, so the user always sees which part of PARASITER is working:
`▸ PARASITER · platform-feed`
If you called agents for this reply, add them after an arrow: `▸ PARASITER · platform-feed → serp-analyst, product-researcher`. If you hand off to another skill, the next reply carries that skill's label. One line only, no other system talk.

## Plugin basis and Claude plan — RULE (№33)

Every answer here is PARASITER at work: this skill's steps, Rumer's rules, criteria and references — never general knowledge alone. Name the basis briefly where it matters ("by Rumer's rules", the checklist, score or reference used, "PARASITER platform base"). A request this skill doesn't cover → the right skill; nothing fits → one line "outside PARASITER's skills — I answer by Rumer's general rules", then "0 — menu". Full rule: `navigator/references/agents-and-plan.md`.

## Next steps (end of every reply)

The user must always know what to type next. End every reply with a short numbered block — ready phrases, not skill names:

**What's next? Reply with a number or the phrase:**
1. "<ready phrase>" — <what happens after it, a few words>
2. "<ready phrase>" — <what happens>

- 2–3 options that fit what just happened, the recommended next step first. "1", "yes", "ok", "go" means option 1. Any free wording of the same wish works too ("give me the offers").
- Each option is a complete phrase in the user's working language that they can copy, plus what it does. Never show skill or agent names here: the work label at the top already names the part that is working.
- Offer only what the user's plan includes (`account_info`, once per session). A Pro or Insider feature on a lower plan appears at most once as the last option, marked "(Insider)" or "(Pro)" with one line on what it gives. Profile says Pro or Insider but `account_info` shows no key or Free → the navigator's "key isn't connected" warning at the top (№44), never a quiet Free run.
- **During first setup** (a step in the profile's `setup:` is still open — not `done`, `skipped` or `not needed`): option 1 is the current setup step, and the setup footer from `navigator` ("First setup checklist") goes under the options — step N of 12, what is done, now, next.
- Things that need no decision (logging, monitoring, saving to the base) are done automatically, not offered.
- **0 — menu (№26):** the last option is always "**0** — menu of all functions". If something is paused (`paused:` in the profile: a day-plan task, a setup step, a draft), option 1 is "**back** to <it>". Never make an option a condition ("first publish…") — every option is an offer.
- **Mark tried:** on this skill's first real run in the session, add or update its line under `tried:` in `parasite-seo-profile.md` (`- <skill> · YYYY-MM-DD · <what, 3–6 words>`; agents too, marked `agent`). When the user seems lost or asks what else there is, add: "All PARASITER functions: say **help**."

Options that usually fit after this part (adapt to the user's products and words):
- "analyze the new platform" — score it before posting
- "what should I write there?"
- "connect Telegram" — alerts and your plan's channel

Part of PARASITER by Rumer (Affiliate Credo).

The feed is the author's live work: new platforms as he finds them, plugin updates, ideas and tips, weekly market analysis (what died, what came back, what Google changed), polls and announcements. It is updated as findings appear — several times a week, sometimes less. **Never describe it as daily.**

The same news goes out in three places: here in Claude, in the Telegram channel of the user's plan (PARASITER Pro or PARASITER Insider), and — for Insider — the private group. Personal notifications (the user's own pages that died — one summary a day, weekly sales reminder, billing) come from the PARASITER bot. Platform-wide news, including cleanups, goes to the channel only, never as personal messages, so nobody gets the same news twice.

Reply in the user's working language.

## Step 0 — Plan check (Pro)

**Step 0 — Plan check.** Call `account_info` once per session (reuse it if already called). Pro or Insider, active → proceed. Free, expired or no key → one line: "This is a Pro feature — Rumer's feed: new checked platforms with live example posts, weekly market analysis, news and the Pro / Insider Telegram channels. Upgrade: https://parasiter.affiliatecredo.com/#pricing", then offer the Free alternative for this skill (the free channel @parasiter_plugin (https://t.me/parasiter_plugin) with plugin news, how-tos and tips, open to everyone), and stop. **Exception — "connect Telegram" on a Free key:** run Mode 2 with the Free key (`telegram_link` works on Free): the bot links the Free key and sends the free channel; Rumer's announcements come there personally; `/offers off` in the bot stops them.

## Requires the server (Pro or Insider)

Tools: `news_latest`, `news_seen`, `feed_latest`, `analysis_latest`, `account_info`, `telegram_link`, `telegram_status`, `telegram_settings`, `telegram_unlink`; for scheduled paid checks (work-log Mode 9) `paid_check_schedule`, `paid_check_pending`, `paid_check_report`; for the Monday sales check-in (work-log) `weekly_checkin`.

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
   New platforms as a table when there are more than 3, post-first:
   `| Post (live example) | Product | Pos. | Platform | Type | Free/Paid | Sign-up | Note from Rumer | Found |`
   Post = the first of the row's `examples` (best position; 1–2 more under it); none → "example: find your own with \"[product] review\"". Sign-up = `signup_url`, or "sign-up link not found" + the home page. Examples come already filtered by the server; never add posts from elsewhere. Drop any platform that matches the exclusions (`exclusions_get`, else `../platform-finder/references/exclusions.md`) or is in its `dead` list.
3. **Cleanup items first** (kind `cleanup`: the server saw pages removed on a platform across many subscribers): if the user has pages there, run `work-log` `republish --platform X` and show their pages with the saved sources to republish; otherwise one line: don't post there for a few days.
4. Make it actionable for this user's niche, language and time: new platforms are **candidates** — number them, star the ones you'd suggest with one line why, and end with "Which ones do we take? Reply with numbers (e.g. 1, 3)"; the chosen ones are saved as priority platforms exactly as in platform-finder Step 5. Never pick for the user. Also say which of their platforms to reduce after the latest changes. For an `update`, say what the user can now do and the phrase to start it.
5. Call `news_seen` after showing, so the navigator does not repeat it.

Plan shapes what comes back: Pro sees new platforms ~7 days after they are found, Insider the same day. On Pro you may mention once that Insider gets them first — no pressure.

## Mode 2 — Connect Telegram

"Connect Telegram", "I want notifications", or the navigator's one-time offer to a paid user who has not linked:
0. **Free key** (`account_info` says free with a key): call `telegram_link` and give its link: "Open this link and press **Start**: [link]. The bot links your Free key and sends the free channel @parasiter_plugin; Rumer's announcements come there personally (`/offers off` stops them). Pro adds the Pro channel, page alerts and the Monday check-in." Stop here (no `telegram_status` / `telegram_settings` on Free).
1. `telegram_status`. Already linked → show what is on and the chats joined.
2. Not linked → `telegram_link`, then:
   "Open this link and press **Start**: [link] (valid 30 minutes). The bot will confirm and send you invites to [PARASITER Pro channel] / [PARASITER Insider channel and the Insider group]. Your plan's channel replaces the free channel @parasiter_plugin, so you don't read the same news twice: if you're in the free channel, the bot takes you out of it."
   Telegram bots cannot write to someone first, so this link is the only way — a username is not enough.
3. Explain the personal notifications in 5 short lines (page alerts, Monday sales reminder, news digest, billing, warnings before a scheduled paid check with buttons to run, narrow or skip it), at most one message a day, quiet at night, and that any type can be turned off.
4. "Turn off X" → `telegram_settings` (`alerts`, `digest`, `checkin` for the Monday check-in). "Disconnect Telegram" → `telegram_unlink` (channel access also ends; reconnect any time).

## Rules

- Feed and channel content is for the subscriber's own use; do not reformat it into a shareable list for publishing elsewhere, and do not suggest forwarding channel posts.
- Everything is a snapshot with a date; platforms change fast — recheck before posting.
- No income claims from the analysis or ideas.
- Never ask for the user's Telegram password, phone or code — only the bot link.
