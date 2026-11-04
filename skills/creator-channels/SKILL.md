---
name: creator-channels
description: The free route of PARASITER for bloggers and content creators — no ad budget, their own channels (YouTube, Instagram, TikTok, Facebook, Pinterest, LinkedIn, X, blog, podcast) as parasite SEO. Builds the creator profile, connects and audits every channel for Google and in-app search (name, bio, links, playlists, settings), makes a search-based content plan and a posting model where one idea becomes a video, Shorts / Reels / TikTok, a pin and a text post, gets fresh content indexed (free methods first, a recommended indexer when needed), tracks videos and posts in Google, and turns audience growth into income (media kit, affiliate links, own offers). Use when the role is blogger / creator, or the user says "I'm a creator", "optimize my channels", "audit my YouTube / Instagram / TikTok", "content plan for my channels", "how do I get my videos into Google", "index my video".
---

# Creator Channels

## Work label (testing period)

Start every reply produced by this skill with one line naming it:
`▸ PARASITER · creator-channels`
If you called agents, add them after an arrow: `▸ PARASITER · creator-channels → video-seo-checker, serp-analyst`. One line only, no other system talk.

## Plugin basis and Claude plan — RULE (№33)

Every answer here is PARASITER at work: this skill's steps, Rumer's rules, criteria and references — never general knowledge alone. Name the basis briefly where it matters ("by Rumer's rules", the checklist, score or reference used, "PARASITER platform base"). A request this skill doesn't cover → the right skill; nothing fits → one line "outside PARASITER's skills — I answer by Rumer's general rules", then "0 — menu". Full rule: `navigator/references/agents-and-plan.md`.

**Agents and Claude plan.** Heavy step: the channel and video checks → agent `video-seo-checker`. Mode: `agents:` in `parasite-seo-profile.md`, else `agents_default` from `account_info`.
- `on` (Claude Max, Team) → run the agent; label `▸ PARASITER · <skill> → video-seo-checker`.
- `lite` (Claude Pro) → the **Lite version** below, label `▸ PARASITER · <skill> · Lite`. When the full version would clearly give a better result here, add one line of advice — why, and the phrase **full** ("For 20 products the full version is better: video-seo-checker checks every one, about 3–5× more of your Claude limits. Say **full** — or I keep Lite").
- `offer` (plan not known) → ask once before the first run: "This step of the skill is done by PARASITER's video-seo-checker agent: separate context, deeper, uses more of your Claude limits (best on Max). Run it? Or Lite with the same skill."
- "full" / "audit by agent" → run it this time; "turn on agents" → `agents: on`; "save limits" or a usage limit hit → `agents: lite` (save in the profile, advice from `agents-and-plan.md` §3).

**Lite version:** one channel or video checked by the checklist; the rest listed. Lite is the same method in a smaller scope: say what was left out.

## Next steps (end of every reply)

The user must always know what to type next. End every reply with a short numbered block — ready phrases, not skill names:

**What's next? Reply with a number or the phrase:**
1. "<ready phrase>" — <what happens after it, a few words>
2. "<ready phrase>" — <what happens>

- 2–3 options that fit what just happened, the recommended next step first. "1", "yes", "ok", "go" means option 1. Any free wording of the same wish works too ("give me the offers").
- Each option is a complete phrase in the user's working language that they can copy, plus what it does. Never show skill or agent names here: the work label at the top already names the part that is working.
- Offer only what the user's plan includes (`account_info`, once per session). A Pro or Insider feature on a lower plan appears at most once as the last option, marked "(Insider)" or "(Pro)" with one line on what it gives.
- **During first setup** (a step in the profile's `setup:` is still open — not `done`, `skipped` or `not needed`): option 1 is the current setup step, and the setup footer from `navigator` ("First setup checklist") goes under the options — step N of 12, what is done, now, next.
- Things that need no decision (logging, monitoring, saving to the base) are done automatically, not offered.
- **0 — menu (№26):** the last option is always "**0** — menu of all functions". If something is paused (`paused:` in the profile: a day-plan task, a setup step, a draft), option 1 is "**back** to <it>". Never make an option a condition ("first publish…") — every option is an offer.
- **Mark tried:** on this skill's first real run in the session, add or update its line under `tried:` in `parasite-seo-profile.md` (`- <skill> · YYYY-MM-DD · <what, 3–6 words>`; agents too, marked `agent`). When the user seems lost or asks what else there is, add: "All PARASITER functions: say **help**."

Options that usually fit after this part (adapt to the user's products and words):
- "make the video package for <topic>"
- "audit my <channel>"
- "content plan for 2 weeks"

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

**Hub:** the creator needs one page Google can index that links every channel and the money links — their own site or blog, or at least a Linktree-type page, Medium / Substack profile, or a Gamma page. New videos are also embedded or linked there: an indexed page linking fresh content helps it get found.

## Step 3 — Search-based content plan and the posting model

1. **Topics from search, not guesses.** For the niche: what people search on Google, YouTube, TikTok and Pinterest — "how to…", "best…", "… vs …", "… review", "… for beginners", problems and questions. `content-type-selector` (buyer-doubt topics when the creator sells or reviews), `serp-analyst` agent for which queries show videos or short videos in Google right now (a query with a video block is the easiest win). Search volumes through the user's SEO API only if they have one; free signals otherwise (autocomplete, "People also ask", YouTube and TikTok search suggestions).
2. **The posting model — one idea, many pieces** (`references/posting-model.md`): long video (YouTube) → 3–5 Shorts / Reels / TikToks from its best moments → 1–2 pins → a text post (LinkedIn / Facebook / Medium / blog) with the video embedded → a community answer (Reddit / Quora) where the rules allow linking to one's own content. Each piece optimised for its platform's search with `video-seo`.
3. **Plan:** 2–4 weeks, one row per piece: date, topic, target query, platform, format, status (`idea → scripted → filmed → published → indexed → ranking`). Sized to the time the creator has; consistency beats volume.

## Step 4 — Make each piece findable

Every video or post goes through `video-seo`: the package before filming or publishing (title, description, chapters, on-screen text, spoken keywords, captions, hashtags, thumbnail / cover prompt, pinned comment, CTA), then the check after publishing by `video-seo-checker`. Text posts and blog articles: `sales-review-writer` in brand mode (the creator's own voice and channels) when the post reviews or sells; otherwise the platform format in `references/channels.md`. Images: `post-illustrations` (covers and pins, free in Gemini).

## Step 5 — Get it indexed

Fresh content that Google hasn't found can't rank. `references/indexing.md`: no free tricks (links and shares don't get pieces indexed); the only free way is the creator's own site in Search Console; then one recommended low-cost indexer for URLs that stay unindexed after 7–14 days — with its price per URL named, and only with the user's yes. Log `submitted` in the journal.

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
