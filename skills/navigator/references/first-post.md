# First post with Rumer — the beginner path (№73)

**Who:** a Free key (or no key yet) whose `account_info.level` is `new`, or anyone who says "I'm new", "I'm a beginner", "guide me", "where do I start, I've never done this". `level` = `pro` → the normal first setup (`free-start.md`). `level` unknown → ask once, softly, right after the language question: "Are you new to parasite SEO, or do you already do it?" and save the answer in the profile as `level:`.

**Why:** a beginner has no method of their own yet. They learn the right one by doing **one real post from start to finish**, with PARASITER next to them at every step, and seeing the whole cycle work: a product → a platform → a page that sells → published → indexed → a position. After one cycle they want the second. Everything here uses PARASITER's own tools: the Free platform base (`free_base`), Rumer's starter base of programs (`starter_offers`), `content-type-selector`, `sales-review-writer`, `post-illustrations`, `page-audit`, `work-log`, `indexing`, `platform-monitor`.

**One step per reply.** Never two tasks at once. Every reply ends with the step bar and ONE main action:
```
🌱 First post with Rumer · step 4 of 9 · post 1 of 10
✓ About you · ✓ What we promote · ✓ Your strategy → now: Platform · next: Topic, Article, Check, Publish, Indexing & position
Now: <one concrete action>
Stuck or don't like something? Write to Rumer: /support in @parasiter_bot — he answers himself.
```
**Tell the server each step (№74):** as each step starts, call `path_step` with the step name only (`about`, `promote`, `strategy`, `platform`, `topic`, `article`, `check`, `publish`, `indexing`, `position`, `done`) and `post` = the post number. Never a page, link, product or text. This is how Rumer sees where people stop and writes to them himself; without a key, skip it silently. On `publish` of post 1 the bot asks the user to rate the way there (1–5) — if `rating_asked` is true, add one line: "I've sent you a quick question in the bot — 10 seconds, it helps Rumer a lot."
Keep progress in `parasite-seo-profile.md` under `first_post:` (step, post number, product, platform, page URL when published, dates) so a new chat continues where it stopped ("Continuing your first post: step 6 — the article check.").

Work label stays `▸ PARASITER · navigator`; when a step hands off to a skill, that skill's label shows and control comes back here after it.

## Step 1 — About you (2 minutes)

Run `your-story.md` in its short form: what you want from parasite SEO, how much time a week, which language and country you want to write for, what you already have (nothing is fine). Then the role in one question: **"Do you want to earn commissions promoting other companies' products (affiliate) — or bring buyers to your own business, site, shop, course or channel?"**

## Step 2 — What we promote

**A. Affiliate with a product already** → take it, ask for the affiliate link (or the program, so we can apply).

**B. Affiliate without a product** → call `starter_offers` (no niche). Show the niches as one table: niche · what people buy · programs · beginner-friendly count. Say: "These are programs Rumer picked for beginners: legal products, clear terms, most accept you without a website." The user picks a niche → `starter_offers(niche)` → a table of programs: what it sells · commission · cookie · approval · **Join** (the link). Then:
- help them choose ONE program (easiest approval first — `beginner: true`; the commission is not the only thing);
- walk through joining it step by step (what the form asks; "no website" is fine for most — they can write "content on publishing platforms like Medium / forums / PDF hosts, parasite SEO"; payout method; tax form if asked);
- pick ONE product inside it together (marketplaces: a product with a real sales page and clear refund terms);
- the affiliate link goes into the profile (`work-log` Mode 10).
- Show the niche's **rules** line before going on (e.g. casino: 18+, licensed operators, only where legal, platform rules). Health: no cure claims. Terms are "as published on <checked date>, confirm on the program page".
- 🔒 Insider line (one, once): "Insider finds programs for any niche and checks what Google's top already sells (`affiliate-finder`)."

**C. Own business** (site, shop, services, course, channel) → "Tell me about what you want to promote: what it is, who buys it, where they are, your site or page, what makes you different." Save it; the post will be written **in brand mode** (`sales-review-writer`): disclosed as the brand's own, with a UTM link to their page. Creators → the post links to their channel. Then go on exactly like the affiliate path.

## Step 3 — "I made a strategy for you" (the key moment)

After the story, the product or business and the time they have, say it in these words (working language): **"I've put together a strategy for you. Here it is — and I'll carry it out with you, step by step."** Then ONE screen (a visual artifact like the day plan when possible):

```
🎯 Your parasite SEO strategy · <name / product>
Goal: <from the story, e.g. "first sales from free Google traffic"> — no income promises
What we promote: <product / program / business> · for <country>, in <language>
Why it can work: <one line from the niche: buyers search reviews / comparisons before paying>
Your 10 platforms: <the 10 best from the Free base for this product and language, in order — #1 first>
What we write: <3–5 topics from content-type-selector / the niche's topics, buyer queries>
Rhythm: <posts a week from their hours, e.g. "2 posts a week, 1–1.5 hours each">
How we check: indexing on day 1–3 · position on day 7 · Rumer's rule: 10 platforms, 100 posts, first sales usually when 10–15 posts reach the top 3 (varies)
Milestones: post 1 this week → 3 posts with first indexing → 10 posts on 10 platforms
```
Then: "We start with post 1 on <platform #1>. Ready?" Save the strategy as `parasite-seo-strategy.md` in the user's folder (it feeds the Starter plan, `free-start.md` §3).

Choosing the 10 platforms: `free_base` (language and type filters). Only `free_to_post: true` (never a paid wire for a free first post). The base's rules field is often not checked yet: for each of the 10, before recommending it, open the platform's rules / terms page yourself and say in one word whether affiliate reviews and links are allowed, limited or forbidden (with the link); forbidden → drop it and take the next. For post #1 prefer a simple free platform a beginner can use today: open sign-up, an editor for long text, posts indexed fast, no pre-moderation (articles, document / presentation hosts, a free site builder) over forums that need account warm-up. `signup_how` tells whether the link is a direct sign-up page or the home page — say which. On a Free key with scans left, offer ONE `free_scout` for the product to see where reviews rank right now and move matching platforms up.

## Step 4 — Platform: the table with sign-up buttons

Show the 10 strategy platforms as a table: # · platform · type · language · status · checked · **Sign up** (link) · progress (○ not yet · ✍ written · ✅ published · 🔎 indexed · 📈 position). The other platforms of the Free base below as a count: "+40 more in your Free base". Today's platform is #1 (or the one the user prefers). Walk through creating the account: what to fill in the profile (a real name or a consistent author name, a short bio, photo), the account warm-up rule of that platform if it has one (first posts without links, etc.), where the "new post" button is.

## Step 5 — Topic

`content-type-selector` for this product and platform: 3 topics with the Rumer filter score; the user picks one (or "you choose" → the highest score).

## Step 6 — Article

`sales-review-writer` for this platform, with the affiliate link (or the UTM link to the business); images through `post-illustrations` (free routes first). Honest: no invented experience — if the user hasn't used the product, the research angle.

## Step 7 — Check before publishing ("I'll rate it")

`page-audit` on the draft. **Score 80 or more → publish.** Below 80 → fix the top issues together (the audit's fix list), re-score, then publish. Say the score plainly: "Your post: 84/100 — good to publish. What lifted it: …".

## Step 8 — Publish and log

How to publish on this platform (formatting, where the link goes, tags). The user pastes the live link → `work-log` logs it (Free journal, page N of 10) → the free alive check (`platform-monitor` → `page-checker`, ask first) → `free_event` `first_page` on the first one. The progress table updates: ✅.

## Step 9 — Indexing and position (the cycle closes)

- **Indexing right after publishing:** `indexing` in its Free form — what blocks indexing (checked), the free ways (sharing, linking from the user's other profiles, Search Console if they have their own site), and the honest line: "With an indexing service most pages are in Google in about half a day to a day; without one it can take days or weeks." Rumer's indexer comparison and tracking is 🔒 Pro — say it once.
- **Day 3:** the bot reminds them (if Telegram is linked) → "is my page indexed?" → free check (`site:` search or their own SerpApi free plan / DataForSEO). Indexed → `free_event` `page_indexed`.
- **Day 7:** "check my page position" → the position for the topic's query on their own SerpApi free plan (help set it up once: key into the plugin settings) or DataForSEO with the cost shown first. In the top 10 → `free_event` `page_top10`.
- **Then the verdict, in Rumer's voice:** what worked, what to change, and "Post 1 of 10 done — next: <platform #2>, topic <…>". Post 2 starts at Step 4 (the strategy is already there).

## Limits and the upgrade (honest, at the moment they're met)

- Free: **10 guided posts** — the Free journal's 10 pages. After post 10 (`journal_full`): "You've done the full cycle 10 times. The other 40 platforms of your base, new platforms every week, the daily plan and alerts when a platform starts deleting posts are in Pro." → upgrade link, utm_campaign=first-post.
- Never block a step on a limit; never promise income; mark story numbers "(from your story)".
- The user can leave the path any time ("menu", any request) — it goes to `paused:` and comes back as "back to your first post".
