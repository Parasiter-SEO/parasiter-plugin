---
name: video-seo
description: Make every video and social post findable in Google and in-app search — the package before filming or publishing (search topic and target query, title, first lines of the description, chapters with timestamps, spoken keywords in the first seconds, on-screen text, captions / transcript, tags and hashtags, thumbnail or cover prompt, pinned comment, CTA and links) for YouTube, Shorts, Instagram Reels, TikTok, Facebook Reels, Pinterest and text posts, then a check of the published piece by the video-seo-checker agent and tracking in Google's video and short-video results. Use when the user says "optimize my video", "title and description for my video", "video package for [topic]", "make this Reel / TikTok rank", "check my video", "why doesn't my video show in Google".
---

# Video SEO

## Work label (testing period)

Start every reply produced by this skill with one line naming it:
`▸ PARASITER · video-seo`
If you called agents, add them after an arrow: `▸ PARASITER · video-seo → video-seo-checker`. One line only, no other system talk.

## Next steps (end of every reply)

End each reply with one short line of 2–3 options, each with the phrase to say, e.g. `Next: "check my video after publishing: URL" · "make the Shorts from this video" · "pin for this video" (post-illustrations).` Logging is automatic, not offered.

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
