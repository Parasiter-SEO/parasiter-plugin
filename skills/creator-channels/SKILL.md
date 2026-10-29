---
name: creator-channels
description: The free route of PARASITER for bloggers and content creators — no ad budget, their own channels (YouTube, Instagram, TikTok, Facebook, Pinterest, LinkedIn, X, blog, podcast) as parasite SEO. Builds the creator profile, connects and audits every channel for Google and in-app search (name, bio, links, playlists, settings), makes a search-based content plan and a posting model where one idea becomes a video, Shorts / Reels / TikTok, a pin and a text post, gets fresh content indexed (free methods first, a recommended indexer when needed), tracks videos and posts in Google, and turns audience growth into income (media kit, affiliate links, own offers). Use when the role is blogger / creator, or the user says "I'm a creator", "optimize my channels", "audit my YouTube / Instagram / TikTok", "content plan for my channels", "how do I get my videos into Google", "index my video".
---

# Creator Channels

## Work label (testing period)

Start every reply produced by this skill with one line naming it:
`▸ PARASITER · creator-channels`
If you called agents, add them after an arrow: `▸ PARASITER · creator-channels → video-seo-checker, serp-analyst`. One line only, no other system talk.

## Next steps (end of every reply)

End each reply with one short line of 2–3 options, each with the phrase to say, e.g. `Next: "make the video package for [topic]" (video-seo) · "audit my Instagram" · "content plan for 2 weeks".` Offer only what the user's plan includes. Logging and saving are automatic, not offered.

Part of PARASITER by Rumer (Affiliate Credo).

**Ads are expensive; your content can rank for free.** Google now shows creators' content right in the results: YouTube videos and Shorts, and short videos from TikTok, Instagram and Facebook in the "Short videos" block, Pinterest pins in images, creators' posts in "Discussions and forums" and "Perspectives". A creator who makes a lot of content already owns the best parasite SEO platforms — their own channels. The job is to make every piece **findable**: a topic people search for, the words in the right places, a channel that is complete, the content indexed, and a path from the viewer to what the creator earns from.

Say this once, at the start, in two lines, in the working language. No budget is assumed anywhere in this route: every step has a free way; paid tools are named only as options.

## Files

- `parasite-seo-profile.md` — role `creator`, working language, the creator profile (below).
- `creator-channels.md` — every channel: URL, platform, followers, audit score, what to fix, settings checked (written by Step 2).
- `content-plan.md` — the plan and the posting model (Step 3).
- `parasite-seo-progress.csv` — the journal (`work-log`): every published video and post with its main query and platform; checks and positions. Sales and sponsor deals optional.

## Step 1 — The creator profile ("digitize yourself")

In one short message: niche and topics; who they are and why people listen (real experience, results, credentials — facts only); audience (who, country, language); voice and format (talking head, tutorials, reviews, vlogs, shorts); how they earn or want to earn (sponsorships, affiliate links, own product, services, donations); **every channel they have** — links to YouTube, Instagram, TikTok, Facebook, Pinterest, LinkedIn, X, Threads, blog, podcast, newsletter, Linktree-type page — and how much time per week they have. Save into the profile. The profile feeds every text and video package (author intro, voice, CTAs).

## Step 2 — Channel audit and optimization

For every channel, the checklist in `references/channels.md`: findable name (name + niche word), bio with the main topic in searchable words, links (the hub page and the money link), profile photo and banner, playlists / highlights / boards organised by search topic, pinned content, the platform's own search settings (e.g. Instagram's setting that lets public posts appear in search engines for professional accounts, and the account type), consistent handle and description across channels, activity.

Send the channel URLs, niche and target topics to the **`video-seo-checker` agent** for a fresh read of what is public (what the profile shows, the last 10 uploads' titles and descriptions, whether the channel or its videos appear in Google for its name and topics). Score each channel 0–100 with the checklist, list fixes in order of impact, and give the rewritten texts ready to paste (name line, bio, About, playlist titles). Save to `creator-channels.md`.

**Hub:** the creator needs one page Google can index that links every channel and the money links — their own site or blog, or at least a Linktree-type page, Medium / Substack profile, or a Pressbooks / Gamma page. New videos are also embedded or linked there: an indexed page linking fresh content helps it get found.

## Step 3 — Search-based content plan and the posting model

1. **Topics from search, not guesses.** For the niche: what people search on Google, YouTube, TikTok and Pinterest — "how to…", "best…", "… vs …", "… review", "… for beginners", problems and questions. `content-type-selector` (buyer-doubt topics when the creator sells or reviews), `serp-analyst` agent for which queries show videos or short videos in Google right now (a query with a video block is the easiest win). Search volumes through the user's SEO API only if they have one; free signals otherwise (autocomplete, "People also ask", YouTube and TikTok search suggestions).
2. **The posting model — one idea, many pieces** (`references/posting-model.md`): long video (YouTube) → 3–5 Shorts / Reels / TikToks from its best moments → 1–2 pins → a text post (LinkedIn / Facebook / Medium / blog) with the video embedded → a community answer (Reddit / Quora) where the rules allow linking to one's own content. Each piece optimised for its platform's search with `video-seo`.
3. **Plan:** 2–4 weeks, one row per piece: date, topic, target query, platform, format, status (`idea → scripted → filmed → published → indexed → ranking`). Sized to the time the creator has; consistency beats volume.

## Step 4 — Make each piece findable

Every video or post goes through `video-seo`: the package before filming or publishing (title, description, chapters, on-screen text, spoken keywords, captions, hashtags, thumbnail / cover prompt, pinned comment, CTA), then the check after publishing by `video-seo-checker`. Text posts and blog articles: `sales-review-writer` in brand mode (the creator's own voice and channels) when the post reviews or sells; otherwise the platform format in `references/channels.md`. Images: `post-illustrations` (covers and pins, free in Gemini).

## Step 5 — Get it indexed

Fresh content that Google hasn't found can't rank. `references/indexing.md`: free ways first (the hub page linking the new piece, sharing to crawled platforms, the creator's own site sitemap and Search Console, IndexNow for Bing), then one recommended low-cost indexer for URLs that stay unindexed after 7–14 days — with its price per URL named, and only with the user's yes. Log `submitted` in the journal.

## Step 6 — Track the top and the growth

- Log every published piece in the journal (`work-log`): URL, platform, main query (`--query`), sub-ID if it carries a link. Checks: alive and indexed (free), positions in Google including video and short-video blocks (`work-log` Mode 9 on the user's DataForSEO account — cents, only with the user's yes; or manual checks for a few queries).
- Monthly: followers and views per channel (the creator reads them from each app's analytics or uploads the exports — `work-log import-traffic`), which pieces rank in Google, which queries bring people, what to make more of.

## Step 7 — Turn growth into income

- **Media kit** for sponsors from real numbers: audience, views, engagement, top pieces, which ones rank in Google (a sponsor gets search traffic for months, not a 48-hour post) — written by Claude, figures only from the creator's analytics.
- **Affiliate links** in descriptions and pinned comments (`affiliate-finder` on Insider, `parasite-seo-links.csv`), disclosed as the platform requires.
- **Own offer** (course, product, service) → the CTA in every piece; when it grows into a site, the site owner route.

## Rules

- Free first, always: every step has a $0 way; paid tools only as named options with prices, never assumed.
- No fake engagement: no bought views, followers, likes or comments, no engagement pods sold as growth, no fake reviews. They break platform rules and kill reach.
- Facts about the creator only from the creator; numbers in media kits only from their analytics.
- Paid checks (positions, indexers) only with the user's yes and the cost shown.
- Platforms change their search and settings often: say "as of [date]" on settings and limits, and let `video-seo-checker` confirm what is live.
