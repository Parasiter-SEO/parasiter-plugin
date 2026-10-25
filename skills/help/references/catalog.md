# PARASITER catalog

<!-- Maintainer: update this file, how-to.md and faq.md whenever a skill, agent, server tool, plan or file changes. The help skill answers only from these files. -->

PARASITER by Rumer — parasite SEO inside the user's AI assistant, built for affiliate marketers: review pages on trusted platforms → affiliate link → commission. The full system is for affiliate marketers at any stage (want to start, already working, professional, veteran). On first run the navigator asks the role; SEO specialists / agencies, bloggers and course authors / own-product owners get only the tools that fit them, with no goals or daily plan (see "Roles" below). Skills hold the method; agents do research and checks in their own context and hand back facts with sources. The user never calls agents; skills send them. Version 0.16 (private beta).

## The workflow in 5 steps

1. **Plan** — `navigator` (today's plan) and `goals` (baseline, goals, weekly review).
2. **Find** — `affiliate-finder` (what to promote), `niche-analysis` (keywords and SERPs), `platform-finder` / `platform-feed` (where to publish), `platform-analyzer` (is this platform worth it).
3. **Write** — `content-type-selector` (what to write), `sales-review-writer` (the article), `post-illustrations` (images), `page-audit` (check before publishing).
4. **Publish and log** — the user publishes; `work-log` records the page and queues checks; `platform-monitor` checks alive / indexed.
5. **Measure** — `work-log` (sales, traffic, reports, what earns), `client-reports` (client-facing reports), back to `goals` for the weekly review.

## Skills

| Skill | Plan | What it does | Say, for example | Needs the server? |
|---|---|---|---|---|
| `navigator` | Pro | Entry point. First setup: language, role, a few questions (niche, programs, country, time, tools — recommends DataForSEO if you have no SEO API), then asks you to upload what you have: pages, affiliate links, sales reports (with export steps for your networks), traffic reports. Beginners skip the uploads. Reads goals and the journal, gives 2–5 tasks for today and routes each to the right skill. | "What should I do today?", "Where do I start?" | No (with a key it also reads monitoring and the feed) |
| `goals` | Free | Starting point from your uploaded reports plus a few questions (time, pace, team, income in your words), goals for 1 week to 12 months with Rumer's rule (10 platforms / 100 live posts) as the minimum, reality check with *possible* income, monthly milestones incl. posts in the top 3, weekly targets, daily quota, weekly plan-vs-fact review. A from-zero path for beginners. | "Set my goals for 6 months", "Am I on track?" | No |
| `work-log` | Pro | Journal of work, traffic and sales, and your inventory: imports the pages you already have (any list of links) and builds your own platform base from them. Topics, priorities (★) and top-10 positions (automatic weekly checks with your DataForSEO account); topic coverage across platforms with what to write where. Logs every page and action as it happens, keeps the source .docx you worked on with its page and lists what to republish after a removal or cleanup, every sale (by hand or from a network export), platform views and affiliate clicks. Reports for any day, week, month or dates; effectiveness by page, platform, offer, program, campaign (pack), content type, month; check queue; weekly reminder to upload sales. | "Here are my pages" + file, "My platforms", "What should I write next?", "Which pages are in the top?", "Published: URL", "Made a sale, $42 ClickBank", "Here's my Impact export", "What did I do and earn this week?", "What earns?", "What needs checking?" | No |
| `content-type-selector` | Free | Chooses what to write before writing: commercial-intent topics only (best, review, vs, results, legit, complaints, price, alternatives), found through buyer needs and live search. Rumer's formats first: best-of lists of 10–15, personal experience / my results, A vs B, expert review. SERP check of every candidate. | "What should I write about [product]?" | No |
| `sales-review-writer` | Free | Writes the conversion review or comparison (1,500+ words) after 3–4 questions: facts box for the main product (price, quality, my rating x/10, special offers, link), author, TOC, pains → facts → life after → prices → comparison and honest alternatives, CTAs, images, disclosure. Then rolls the topic out to your other platforms and offers to save your worked .docx with the page. | "Write a review of X for Medium" | No |
| `page-audit` | Free | Audits a page by link or text with two scores — Rumer's rules and copywriting — and their average, critical / medium issues, ready-to-paste fixes; always flags a missing cover photo (the snippet image). Uses the independent-auditor agent for a fresh read. | "Audit my article: URL", "Why no sales?" | No |
| `post-illustrations` | Free | Images that carry the facts of the text: a realistic cover photo of the real product (DALL·E by default) and 3–5 infographics (facts, pains → solution, benefits, comparison, prices). Horizontal JPG ~700 px; hosting by link where the platform asks for a URL. | "Make images for this review" | No |
| `platform-finder` | Pro | Finds platforms where affiliate review pages are published and indexed now — Rumer's checked base first, then a live scan of "[product] review" for many affiliate products in the top 10 (paid, on your DataForSEO account, cost shown first). Free and paid platforms always separate; abused sites skipped. | "Where can I publish about VPNs in Spanish?" | Database: Pro |
| `platform-analyzer` | Pro | Breaks down one platform: are affiliate reviews in the top 10 there now (the main check), fresh-page indexing, registration, moderation, free or paid; 0–100 score. Reviews in the top 10 now = publish now; lifespan is only a stability label (2+ weeks = stable). | "Should I post on X?" | No |
| `platform-feed` | Pro | Rumer's news feed: new platforms, plugin updates, ideas, weekly market analysis, polls — turned into actions for the user's niche. Connects Telegram: plan channel, Insider group, personal notifications. | "What's new?", "Connect Telegram" | Pro (Insider: same-day platforms, Insider channel and group) |
| `platform-monitor` | Pro | Alive / removed, noindex, affiliate link (free, daily on the server with a key); index and positions on your own SEO account (paid, only with your yes). Removed pages and platform cleanups go straight to the republish list with your saved sources. | "Are my pages alive?", "Check my links" | Scheduled: Pro. Manual: no |
| `niche-analysis` | Insider | Commercial keywords and their volumes, an entry score from the top 20 (heavy domains vs platforms like yours — one of ours in the top 20 means a chance), competitor parasite pages and their gaps; a test page with the tracker decides. Through your SEO API (paid, cost shown first) or exports. | "Is this niche worth it?", "Find keywords for X" | Needs the user's own SEO API key or exports |
| `affiliate-finder` | Insider | Niche first (nutra, gambling, crypto, gaming, software and more), then programs from networks and direct merchants, sorted by how popular the offer is in search; commission 15%+; traffic rules, payout, legality — via the affiliate-scout agent. | "Which program should I promote for keto?" | No |
| `client-reports` | Insider | For affiliates: the review of your asset and a scale plan — which products, platforms and content types took off and earn, where to add pages and angles, what to stop. For agencies: a client report. | "What took off and where do I scale?", "Report for my client" (agency) | No |
| `help` | Free | This help: what the plugin does and how to use it. | "What can PARASITER do?", "How do I …?" | No |

## Roles

Set once by the navigator ("who are you and what for?"), saved as `role` in the profile, changeable any time. Full table: `navigator/references/roles.md`.

| Role | Gets |
|---|---|
| Affiliate (parasite SEO) | Everything: goals, daily plan, journal with sales, all 15 skills by plan |
| SEO specialist / agency | content-type-selector, page-audit, post-illustrations, platform-finder, platform-feed, platform-analyzer, platform-monitor, work-log (pages and checks), niche-analysis, client-reports |
| Blogger / content creator | content-type-selector, sales-review-writer, page-audit, post-illustrations, work-log, affiliate-finder, niche-analysis |
| Course author / own product | content-type-selector, page-audit, post-illustrations, platform-finder, platform-feed, platform-analyzer, platform-monitor, work-log (pages and checks); own product never presented as an independent review |
| Other / just looking | Overview, then the closest role |

Roles 2–4: no goals and no daily plan. A skill outside the role is not offered; name the closest one in the role. `help` is open to everyone.

## Agents

| Agent | Sent by | Does |
|---|---|---|
| `platform-scout` | platform-finder | Probes "[product] review" searches and lists the platforms where affiliate reviews rank now, free vs paid, with a quick check of the free ones |
| `affiliate-scout` | affiliate-finder | Program terms with sources and dates, offer page check |
| `product-researcher` | sales-review-writer | Current specs, packages, prices, discounts, guarantee from the merchant's pages |
| `serp-analyst` | content-type-selector, niche-analysis | What ranks for buyer queries, which platforms are in the top 10, unanswered buyer doubts |
| `page-checker` | platform-monitor, work-log | Checks lists of pages: live, noindex, indexed, affiliate link, position |
| `independent-auditor` | page-audit | Reads a page without the writing context, like a doubtful buyer; gives the same two scores |

## Server tools (Pro / Insider key)

`account_info` (plan, limits, Telegram linked) · `platforms_search` (checked platform database) · `feed_latest`, `analysis_latest` (platforms and weekly analysis) · `news_latest`, `news_seen` (news feed) · `telegram_link`, `telegram_status`, `telegram_settings`, `telegram_unlink` (Telegram) · `monitor_track`, `monitor_status` (scheduled page checks) · `paid_check_schedule`, `paid_check_pending`, `paid_check_report` (scheduled paid checks on your own SEO API, warned in Telegram before each run). Skills say when they need one and fall back to live search or manual checks without a key. The server is in beta.

## The user's files

Kept in the user's project folder, written by the skills:

| File | Written by | Holds |
|---|---|---|
| `parasite-seo-profile.md` | navigator | working language, role, niche, offers, country and content language, tools, author profile |
| `parasite-seo-goals.md` | goals | baseline, goals, milestones, this week's targets, reviews |
| `parasite-seo-progress.csv` | work-log | pages, checks, audits, traffic, imports, other work — one row per fact |
| `parasite-seo-sales.csv` | work-log | one row per sale, manual or imported |
| `parasite-seo-links.csv` | work-log | your affiliate links library: program, product, link, alternative links, commission |
| `parasite-seo-platforms.csv` | work-log, platform-analyzer | your platform base: domain, type, language, links, account, score, state; built from your pages |
| `parasite-seo-sources/` | work-log | the .docx / texts you worked on, each linked to its published page, for republishing |
| `platforms-scan.csv` | platform-finder | the latest live scan: platforms with affiliate reviews, free / paid |

## Telegram (Pro and Insider only)

| Chat | Who | What |
|---|---|---|
| PARASITER Pro channel | Pro and Insider | news, updates, ideas, polls, platform cleanups seen across subscribers; new platforms ~7 days after found |
| PARASITER Insider channel | Insider | everything the same day, plus Insider-only posts |
| Insider group | Insider | discussion with Rumer and members, polls, questions |
| PARASITER bot | Pro and Insider | linking, invites, personal notifications: one daily summary of your pages that got worse, Monday sales reminder, news digest, billing, warnings before a scheduled paid check (run / only ★ / skip / change) |

Free: no server and no Telegram chats; the public channel @rumerparasiteseo is open to everyone.

## What PARASITER does not do

- Does not publish or post anything itself: it prepares pages, the user publishes.
- Does not create accounts, buy links or work with hacked sites, hidden upload forms or fake reviews.
- Does not log in to affiliate networks: the user exports reports and uploads them.
- Does not promise income or rankings; income in plans is "possible income" at your own numbers.
- Never runs a paid check (index, positions, scans on your SEO API) without your yes and the cost shown first.
