---
name: video-seo
description: Make every video and social post findable in Google and in-app search — the package before filming or publishing (search topic and target query, title, first lines of the description, chapters with timestamps, spoken keywords in the first seconds, on-screen text, captions / transcript, tags and hashtags, thumbnail or cover prompt, pinned comment, CTA and links) for YouTube, Shorts, Instagram Reels, TikTok, Facebook Reels, Pinterest and text posts, then a check of the published piece by the video-seo-checker agent and tracking in Google's video and short-video results. Use when the user says "optimize my video", "title and description for my video", "video package for [topic]", "make this Reel / TikTok rank", "check my video", "why doesn't my video show in Google".
---

# Video SEO

## Work label (testing period)

Start every reply produced by this skill with one line naming it:
`▸ PARASITER · video-seo`
If you called agents, add them after an arrow: `▸ PARASITER · video-seo → video-seo-checker`. One line only, no other system talk.

## Show what the next plan opens — RULE (№56)

Free skill. After its result, a Free user (no key or Free key) gets the "🔒 On Pro / Insider this step would also" block with the lines for this skill from `navigator/references/upgrade-showcase.md` §3, made concrete for what was just done; a Pro user gets the one Insider line. At most one block per reply, below the result, never on error or bad-news replies; `upsell: compact` in the profile → one line per session.

## Plugin basis and Claude plan — RULE (№33)

Every answer here is PARASITER at work: this skill's steps, Rumer's rules, criteria and references — never general knowledge alone. Name the basis briefly where it matters ("by Rumer's rules", the checklist, score or reference used, "PARASITER platform base"). A request this skill doesn't cover → the right skill; nothing fits → one line "outside PARASITER's skills — I answer by Rumer's general rules", then "0 — menu". Full rule: `navigator/references/agents-and-plan.md`.

**Agents and Claude plan.** Heavy step: the video check → agent `video-seo-checker`. Mode: `agents:` in `parasite-seo-profile.md`, else `agents_default` from `account_info`.
- `on` (Claude Max, Team) → run the agent; label `▸ PARASITER · <skill> → video-seo-checker`.
- `lite` (Claude Pro) → the **Lite version** below, label `▸ PARASITER · <skill> · Lite`. When the full version would clearly give a better result here, add one line of advice — why, and the phrase **full** ("For 20 products the full version is better: video-seo-checker checks every one, about 3–5× more of your Claude limits. Say **full** — or I keep Lite").
- `offer` (plan not known) → ask once before the first run: "This step of the skill is done by PARASITER's video-seo-checker agent: separate context, deeper, uses more of your Claude limits (best on Max). Run it? Or Lite with the same skill."
- "full" / "audit by agent" → run it this time; "turn on agents" → `agents: on`; "save limits" or a usage limit hit → `agents: lite` (save in the profile, advice from `agents-and-plan.md` §3).

**Lite version:** one video checked by the checklist; other videos listed. Lite is the same method in a smaller scope: say what was left out.

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
- "check my video after publishing: <link>"
- "make the Shorts from this video"
- "make a pin for this video"

Part of PARASITER by Rumer (Affiliate Credo).

**A video ranks when Google and the platform understand what it answers.** They read the title, the description, the spoken words (auto-captions), the text on screen, the chapters and the engagement. A creator who puts the query people search for in those places, and answers it fast, gets into Google's video and "Short videos" blocks for free. This skill writes all of it before the video is made — the cheapest moment to get it right — and checks it after.

Who uses it: creators first (`creator-channels`), and every other role that publishes videos (affiliates on YouTube, agencies and site owners for brand channels).

Reply in the working language; the package itself in the content language of the channel.

## Step 1 — The query

One video, one main query. From the content plan, or ask: topic, channel, audience country. Check the query (`serp-analyst` agent or a quick search): does Google show a video or "Short videos" block for it? Which videos rank, how long, what they miss? Pick the angle that answers the query better or faster. A query with no video block can still win on YouTube and TikTok search — say which goal it serves.

## Step 2 — The package (before filming)

Per platform, from `references/video-package.md`:

**Long video (YouTube)**
- **Title** — the query near the start, plus the promise (result, number, year). Under ~60 characters visible.
- **Hook script (first 15 s)** — say the query and what the viewer gets; this is what auto-captions and viewers judge first.
- **Outline with chapters** — 4–8 sections; each chapter title is a sub-query people search ("How to clean…", "Best budget option"). Timestamps go in the description after editing (starting 0:00).
- **Description** — the first 2 lines carry the query and the answer in brief (shown in search); then what the video covers, chapters, links (hub, offer, affiliate with disclosure), 2–3 related queries in natural sentences, hashtags (2–3).
- **Tags** — a few: the query and close variants (low weight; spelling variants are the main use).
- **Captions** — upload or correct the auto-captions (the spoken words are indexed).
- **Thumbnail** — prompt via `post-illustrations` (Gemini free): one subject, 3–4 words max, readable small, matches the title's promise.
- **Pinned comment** — the main link or the next video, and a question to start comments.
- **Playlist** — which search-topic playlist it goes into.

**Short (YouTube Shorts, Reels, TikTok, Facebook Reels)**
- The query in the **first line of the caption** and **said aloud in the first 2 seconds** and **shown as on-screen text** (all three are read by the platforms' search).
- Caption: 1–2 sentences with the query and a variant, then 3–5 specific hashtags (not generic #fyp lists).
- Cover frame or cover image with the topic in words; vertical 9:16.
- Instagram: alt text with the query; the account's search-engine setting checked in `creator-channels`.
- TikTok: the keyword in the caption, on-screen text and speech; a searchable sound title if using an original sound.
- A link path: "full video on the channel", "link in bio", a pinned comment where allowed.

**Pinterest pin** — title with the query, description in two sentences, the destination link (video or post), board named by search topic.

**Text post** (LinkedIn / Facebook / Medium / blog) — headline with the query, the answer in the first lines, the video embedded or linked, a short summary of the chapters.

Write it all ready to paste, each part in its own block. Mark facts that need checking `[VERIFY: …]`; never invent results, numbers or claims about products.

## Step 3 — After publishing: check

The user sends the URL(s). The **`video-seo-checker` agent** opens the public page and checks every element of the package (title, description first lines, chapters showing, captions, hashtags, links working, cover), whether the video is indexed in Google, and whether it appears for the main query in Google (video results, Short videos block) and in the platform's search. Score 0–100 with `references/video-package.md` (scoring), list fixes in order. Editable things (title, description, chapters, captions, pinned comment) can be fixed after publishing — give the corrected text.

Log the piece in the journal: `work-log add --event published --url … --platform youtube --query "…"`. Not indexed after 7–14 days → `creator-channels` Step 5 (indexing).

## Step 4 — Track

Positions of the creator's videos for their queries in Google, including the video and short-video blocks: `work-log` Mode 9 (DataForSEO, cents, with the user's yes) or manual checks for a few queries. Every 2–4 weeks: which pieces rank, which titles to rework, which topics to make more of.

## Rules

- Write for the viewer first: a title that promises what the video delivers; no clickbait the video doesn't pay off — it kills watch time and rankings.
- No keyword stuffing in titles, descriptions or hashtags; no misleading tags.
- No bought views, likes, comments or followers; no fake engagement.
- Affiliate and sponsor links disclosed as the platform and law require.
- Platform search rules change: describe them "as of [date]" and let the checker confirm.
