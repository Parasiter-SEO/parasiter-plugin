# PARASITER catalog

<!-- Maintainer: update this file, how-to.md and faq.md whenever a skill, agent, server tool, plan or file changes. The help skill answers only from these files. -->

PARASITER by Rumer — parasite SEO inside the user's AI assistant, built for affiliate marketers: review pages on trusted platforms → affiliate link → commission. The full system is for affiliate marketers at any stage (want to start, already working, professional, veteran). On first run the navigator asks the role; SEO specialists / agencies, bloggers and course authors / own-product owners get only the tools that fit them, with no goals or daily plan (see "Roles" below). Skills hold the method; agents do research and checks in their own context and hand back facts with sources. The user never calls agents; skills send them. Version 0.9 (private beta).

## The workflow in 5 steps

1. **Plan** — `navigator` (today's plan) and `goals` (baseline, goals, weekly review).
2. **Find** — `affiliate-finder` (what to promote), `niche-analysis` (keywords and SERPs), `platform-finder` / `platform-feed` (where to publish), `platform-analyzer` (is this platform worth it).
3. **Write** — `content-type-selector` (what to write), `sales-review-writer` (the article), `post-illustrations` (images), `page-audit` (check before publishing).
4. **Publish and log** — the user publishes; `work-log` records the page and queues checks; `platform-monitor` checks alive / indexed.
5. **Measure** — `work-log` (sales, traffic, reports, what earns), `client-reports` (client-facing reports), back to `goals` for the weekly review.

## Skills

| Skill | Plan | What it does | Say, for example | Needs the server? |
|---|---|---|---|---|
| `navigator` | Pro | Entry point. Asks role, niche, time and language once, reads goals and the journal, checks what changed, gives 2–5 tasks for today and routes each to the right skill. Asks for the week's sales exports on the first session of the week. | "What should I do today?", "Where do I start?" | No (with a key it also reads monitoring and the feed) |
| `goals` | Free | Baseline journal (how much you work, publish and earn now), goals for 1 week to 12 months, reality check, monthly milestones, weekly targets, daily quota, weekly plan-vs-fact review. | "Set my goals for 6 months", "Am I on track?" | No |
| `work-log` | Pro | Journal of work, traffic and sales, and your inventory: imports the pages you already have (any list of links) and builds your own platform base from them. Topics, priorities (★) and top-10 positions (automatic weekly checks with your DataForSEO account); topic coverage across platforms with what to write where. Logs every page and action as it happens, every sale (by hand or from a network export), platform views and affiliate clicks. Reports for any day, week, month or dates; effectiveness by page, platform, offer, program, campaign (pack), content type, month; check queue; weekly reminder to upload sales. | "Here are my pages" + file, "My platforms", "What should I write next?", "Which pages are in the top?", "Published: URL", "Made a sale, $42 ClickBank", "Here's my Impact export", "What did I do and earn this week?", "What earns?", "What needs checking?" | No |
| `content-type-selector` | Free | Chooses what to write before writing: the content type and topic that sells for this product and query (A vs B, experience, doubts, packages and prices, discounts, discussions, tools, research, best-of), from SERP and buyer intent. | "What should I write about [product]?" | No |
| `sales-review-writer` | Free | Writes the conversion review or comparison for the chosen platform: quick facts and current deal at the top, TOC, author intro, structure for the type, CTAs, disclosure. Uses the product-researcher agent for current prices and terms. | "Write a review of X for Medium" | No |
| `page-audit` | Free | Audits a page by link or text: 0–100 score, critical / medium issues, ready-to-paste fixes. Uses the independent-auditor agent for a fresh read. Logs the score in the journal. | "Audit my article: URL", "Why no sales?" | No |
| `post-illustrations` | Free | Image plan and generator prompts in one style: cover, product-in-hand, comparison card, facts infographic, price visual, Facebook series; sizes per platform. | "Make images for this review" | No |
| `platform-finder` | Pro | Finds platforms for a niche and language: forums, communities, Q&A, article, profile, document, site-builder, event pages; filtered by link rules, indexing, moderation. Live search through the platform-scout agent; with a key, the checked platform database first. | "Where can I publish about VPNs in Spanish?" | Database: Pro |
| `platform-analyzer` | Pro | Breaks down one platform: registration, fresh-post indexing, noindex, links, moderation, warm-up, lifespan; 0–100 score and what to publish there. | "Should I post on X?" | No |
| `platform-feed` | Pro | Rumer's news feed: new platforms, plugin updates, ideas, weekly market analysis, polls — turned into actions for the user's niche. Connects Telegram: plan channel, Insider group, personal notifications. | "What's new?", "Connect Telegram" | Pro (Insider: same-day platforms, Insider channel and group) |
| `platform-monitor` | Pro | Alive / removed, indexed / noindex, still ranking, affiliate link working. With a key, scheduled server checks; without, a manual check (page-checker agent for longer lists). Results go into the journal. | "Are my pages alive?", "Check my links" | Scheduled: Pro. Manual: no |
| `niche-analysis` | Insider | Keywords by buyer-modifier cluster, difficulty, SERP make-up, which parasite platforms already rank, competitor pages — through the user's own SEO tool API (DataForSEO, Serpstat, Semrush, Ahrefs) or CSV exports. | "Is this niche worth it?", "Find keywords for X" | Needs the user's own SEO API key or exports |
| `affiliate-finder` | Insider | Finds and scores affiliate programs and offers: model, rate, cookie, payout, GEOs, traffic rules, offer page — via the affiliate-scout agent. | "Which program should I promote for keto?" | No |
| `client-reports` | Insider | Client-facing analytics and reports from the journal and uploaded data: revenue per page, EPC, RPM, winners and losers, 14/30/60-day review, next actions. | "Make a monthly report for my client" | No |
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
| `platform-scout` | platform-finder | SERP and footprint search for platforms, quick live check of each |
| `affiliate-scout` | affiliate-finder | Program terms with sources and dates, offer page check |
| `product-researcher` | sales-review-writer | Current specs, packages, prices, discounts, guarantee from the merchant's pages |
| `serp-analyst` | content-type-selector, niche-analysis | What ranks for buyer queries, which platforms are in the top 10, unanswered buyer doubts |
| `page-checker` | platform-monitor, work-log | Checks lists of pages: live, noindex, indexed, affiliate link, position |
| `independent-auditor` | page-audit | Reads a page without the writing context, like a doubtful buyer |

## Server tools (Pro / Insider key)

`account_info` (plan, limits, Telegram linked) · `platforms_search` (checked platform database) · `feed_latest`, `analysis_latest` (platforms and weekly analysis) · `news_latest`, `news_seen` (news feed) · `telegram_link`, `telegram_status`, `telegram_settings`, `telegram_unlink` (Telegram) · `monitor_track`, `monitor_status` (scheduled page checks). Skills say when they need one and fall back to live search or manual checks without a key. The server is in beta.

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

## Telegram (Pro and Insider only)

| Chat | Who | What |
|---|---|---|
| PARASITER Pro channel | Pro and Insider | news, updates, ideas, polls; new platforms ~7 days after found |
| PARASITER Insider channel | Insider | everything the same day, plus Insider-only posts |
| Insider group | Insider | discussion with Rumer and members, polls, questions |
| PARASITER bot | Pro and Insider | linking, invites, personal notifications: page alerts, Monday sales reminder, news digest, billing |

Free: no server and no Telegram chats; the public channel @rumerparasiteseo is open to everyone.

## What PARASITER does not do

- Does not publish or post anything itself: it prepares pages, the user publishes.
- Does not create accounts, buy links or work with hacked sites, hidden upload forms or fake reviews.
- Does not log in to affiliate networks: the user exports reports and uploads them.
- Does not promise income or rankings; forecasts are labelled as assumptions.
