# PARASITER by Rumer

<a href="https://parasiter.affiliatecredo.com"><img src="https://github.com/user-attachments/assets/7ba859b4-2529-4700-b21e-196fd15c83a3" alt="PARASITER by Rumer — parasite SEO workflow in one place: platforms, pages that sell, sales journal and page checks" width="100%"></a>

**A complete system for managing your parasite SEO work inside Claude Code** — all the skills and AI agents you need for every stage, plus connections to your own SEO tools (DataForSEO, SerpApi, Semrush, Ahrefs, Serpstat and others). Planning, platforms, content that sells, your sales journal and page checks in one place.

[Website](https://parasiter.affiliatecredo.com) · [Watch the 3-minute demo](https://www.youtube.com/watch?v=8pxC6Ml6kVI) · [Plans: Free, Pro, Insider](https://parasiter.affiliatecredo.com/#pricing) · [What's new](CHANGELOG.md)

**Install in Claude Code (two commands):**

```
/plugin marketplace add Parasiter-SEO/parasiter-plugin
/plugin install parasiter@parasiter
```

Free works without a key. Pro and Insider: paste the key from your welcome email when the plugin asks.

⭐ **If PARASITER saves you time, star this repo** — it helps other SEOs find it. Questions, ideas and your results: [Discussions](https://github.com/Parasiter-SEO/parasiter-plugin/discussions) · bugs: [Issues](https://github.com/Parasiter-SEO/parasiter-plugin/issues) or `/bug` in [@parasiter_bot](https://t.me/parasiter_bot).

## What it does

For **affiliate marketers**, **creators**, **site owners** and **agencies**: you publish pages on platforms Google already trusts — affiliates earn the commission, site owners and agencies send buyers (and links, where platforms allow) to the site. Skills and agents find platforms where reviews rank right now, pick the content type that sells, write and audit the page, track every page and sale, and tell you what to do next.

- **Your own mentor:** tell your parasite SEO story in your own words (typed or dictated) — PARASITER builds your profile from it, tells you what it will do for each of your problems and plans every day around them
- **Plan:** goals from your own baseline and a daily plan that fits the time you have
- **Platforms:** where affiliate reviews rank today, with a live example post and a sign-up link for each
- **Content:** buyer topics picked by Rumer's rules, reviews and comparisons written for each platform, images
- **Journal:** every page, sale and click in one place — which pages, platforms and offers really earn
- **Control:** alive / indexed / ranking checks and a queue of what to fix, refresh or republish
- **Beyond Google:** Bing positions and whether Google AI Mode, ChatGPT and Gemini cite your pages; every page written and audited to be AI-ready
- **Updates:** new platforms, Rumer's weekly market analysis and news in Claude and Telegram

**Who it's for:** four full routes — **bloggers and creators** growing their own channels for free, **site owners** building parasite pages around their own site, and **affiliate marketers** who earn with parasite SEO, at any stage, and **agencies** (SEO and marketing agencies, freelancers, in-house teams) running parasite SEO for clients.

On first run the navigator asks who you are and what for. Agencies, site owners and creators get their own routes; others and course authors (own product) get only the tools that fit their work, without goals and the daily plan:

| Role | Tools |
|---|---|
| Affiliate (parasite SEO) | Goals, daily plan, journal with sales, every affiliate skill |
| Agency (SEO / marketing, freelancers, in-house) | A folder per client, onboarding brief, brand and site audit, monthly content plan with client approval, brand-mode texts, images in the client's style, audits, brand-safe platforms, monitoring, positions, GA4 + Search Console traffic, monthly white-label reports |
| Blogger / content creator | Free route: channel audit and optimization, search-based content plan, one idea → many pieces, video SEO packages and checks, indexing, tracking in Google, media kit |
| Site owner (own site, shop, services, course) | A workspace for the site, site and landing-page audits, content and link plan, brand-mode texts, platforms with link rules, paid placements (wires, sponsored articles), backlinks and site results — visits, conversions, revenue vs spend |

Author: Rumer (Affiliate Credo) — 20 years in SEO, parasite SEO for the last 5.

> **Privacy:** the PARASITER server never receives your page URLs, journal, sales, affiliate links or texts — they stay in your Claude project. Page checks run in your own Claude. **Legal products and content only.**

> **Status: beta (v0.38.0).** Skills and agents work without a key; the server (platform database, feed, Telegram, page checks) is live for Pro and Insider.

## How it works

0. **Basic setup: your pages, platforms and affiliate links.** Upload your affiliate links for every product you sell (a list, a table or screenshots), so every article gets the right link and you see which products have no pages yet. Already have pages? Upload the list (any file or pasted links). `work-log` puts every page in your journal, builds your own platform base from them, and one bulk check shows which are alive and indexed.
1. **Tell your story, then fill in what's missing in your baseline journal** with `goals` (the story usually answers most of it): how many hours you work now, how many pages you publish, on which platforms and offers, and what it earns per day, week or month. These are your starting settings: everything after is calculated from them.
2. **Set your goals** from that starting point: pages, platforms, offers, time and the income you realistically expect, over 1 week to 12 months. The skill compares the goal with your real pace, breaks it into monthly milestones and weekly targets, and marks every number it had to assume.
3. **Ask for today's plan** with `navigator`. It reads your goals, progress and time, checks what changed on your platforms, and gives you 2–5 tasks that fit today's time. You don't pick commands: each task goes to the right skill.
4. **Report what you did and what you sold** ("added an article: URL", "sent it to indexing", "made a sale, $42"). `work-log` writes it into your journal at once. Every page is queued for alive and index checks and a conversion audit, so nothing you published is forgotten.
5. **Upload your sales and traffic exports** once a week (ClickBank, Impact, CJ, Amazon, platform stats). Sales are tied to pages by sub-ID, so you see which pages, platforms, offers and content types actually earn: EPC, conversion, commission per page. If you forget, the system asks. Ask "what did I do and earn this week?" or "report for September" any time.
6. **Weekly review**: the goals skill compares plan and fact from the journal, replaces assumptions with your real numbers, and adjusts the next week.

## Skills

| Skill | What it does |
|---|---|
| `goals` | Baseline journal, goals over 1 week to 12 months, reality check, milestones, weekly targets, progress log, weekly review |
| `navigator` | Entry point: asks your role and offers the tools for it; for affiliates, today's plan from your goals, progress and time; routes each task |
| `work-log` | Journal of work, traffic and sales, and your inventory: imports pages you already have and builds your own platform base; topics, priorities, top-10 positions and what to write where; logs every page, action and sale; imports network and platform exports; ties sales to pages by sub-ID; reports for any day, week or month; effectiveness by page, platform, offer, program, content type; check queue and weekly sales upload reminder; your whole base as a dashboard page and an Excel file |
| `content-type-selector` | Picks the content type and topic that sell before writing |
| `sales-review-writer` | Writes the sales review / comparison for your platform |
| `page-audit` | Audits a page by link or text, 0–100 score, fixes |
| `post-illustrations` | Image plan and generator prompts for your posts |
| `platform-finder` | Finds platforms for your niche; checked database with a key |
| `platform-analyzer` | Breaks down one platform, 0–100 score, verdict |
| `platform-feed` | News from Rumer: new platforms, plugin updates, ideas, weekly market analysis, polls; connects Telegram (key required) |
| `platform-monitor` | Alive / indexed / ranking status of your pages; scheduled with a key |
| `indexing` | Gets your pages into Google: blocker check (with agent), free ways, Rumer's comparison of the top indexers and which to use or mix, the clean list to send, logs and rechecks every submission, indexing stats per service, mix and platform |
| `niche-analysis` | Keywords and SERPs via your own SEO tool API |
| `affiliate-finder` | Finds and scores affiliate programs (with agent) |
| `client-reports` | Performance analytics and client reports from your data |
| `client-workspace` | Agencies: clients, onboarding brief, Search Console / GA4 access, UTM, Month 0 baseline, content plan with approval, today's plan across clients, monthly report cycle |
| `brand-presence` | Agencies: client site quick audit, brand profiles on socials and platforms, content audit, profiles plan (with agent) |
| `paid-placements` | Paid publications: wires and sponsored-article marketplaces with prices, link policy, how to order; plan for a budget; did it pay off (with agent) |
| `creator-channels` | Creators: profile, channel audit and optimization, search-based content plan and posting model, indexing, tracking in Google, media kit (free) |
| `video-seo` | The package for every video and post (title, description, chapters, spoken and on-screen keywords, captions, hashtags, cover) and a check after publishing (free) |
| `help` | Built-in help: what each skill does, how to do any task step by step, plans, files, privacy. Ask "what can PARASITER do?" or "how do I …?" |

## Agents

Skills hold the method; agents do the heavy research and checking in their own context and hand back a table of facts with sources and dates. Agents collect, the skill decides. You never call an agent yourself — the skill sends it.

| Agent | Works for | What it does |
|---|---|---|
| `platform-scout` | `platform-finder` | Searches the SERP and forum/community footprints for a niche, checks each candidate: open registration, fresh indexing, noindex, links, moderation |
| `affiliate-scout` | `affiliate-finder` | Collects published program terms (model, rate, cookie, payout, allowed traffic) and checks the merchant offer page |
| `product-researcher` | `sales-review-writer` | Collects current specs, packages, prices, discounts, shipping and guarantee from the merchant's own pages for the quick facts box |
| `serp-analyst` | `content-type-selector`, `niche-analysis` | Breaks down the top 10 for buyer queries: formats, parasite platforms, SERP features, open buyer questions |
| `page-checker` | `platform-monitor`, `work-log` | Checks lists of your pages: live, noindex, indexed, affiliate link working, position |
| `brand-auditor` | `brand-presence`, `client-workspace` | Finds and opens a client brand's profiles and key site pages: exist, complete, consistent, last activity, links; site quick checks; what the brand publishes |
| `placement-scout` | `paid-placements` | Checks paid offers and link policy on published pieces; shortlists marketplace sites for a niche and budget |
| `video-seo-checker` | `video-seo`, `creator-channels` | Checks a channel or a published video / post: what search reads, indexed, appears for its query in Google's video and short-video results |
| `index-checker` | `indexing` | Checks pages for what blocks indexing and whether they are already indexed; returns the clean list to send |
| `independent-auditor` | `page-audit` | Reads a page without the context that wrote it, like a doubtful buyer, and flags weak spots and facts to verify |

Call a skill by describing the task ("set my goals for 6 months", "what should I do today", "audit my article") or directly, e.g. `/parasiter:navigator`.

Your files (kept in your project folder): `parasite-seo-profile.md`, `parasite-seo-goals.md`, `parasite-seo-progress.csv` (work and traffic journal), `parasite-seo-sales.csv` (sales), `parasite-seo-platforms.csv` (your platform base), `parasite-seo-links.csv` (your affiliate links); `parasite-seo-base.xlsx` / `.html` (your base to view and download, rebuilt on request).

## Language

The plugin is written in English and works in any language. On first run the navigator asks which language to work in and saves it in your profile: plans, explanations and your goal files then use it. The pages you publish can be in another language, set by your target country. Change it any time: "switch to Spanish".

## Plans

- **Free, $0** — the plugin without a key: topics, articles, images, page audit, goals, help. **Free key** (by email, no card — [parasiter.affiliatecredo.com/free.html](https://parasiter.affiliatecredo.com/free.html)): a snapshot of 50 checked platforms, 3 platform scans a week for your product and the Free journal for 10 pages with alive, index and position checks.
- **Pro, $19/month** — personal key: platform database, feed and weekly analysis, Telegram alerts, navigator updates; new platforms about 7 days after they are found. **PARASITER Pro** Telegram channel and personal notifications from the bot.
- **Insider, $39/month** — everything in Pro, the full skill set and extra features, new platforms the day they are found. **PARASITER Insider** Telegram channel (platforms a week earlier, extra posts) and the private Insider group (discussion, polls).

Annual billing saves about 20%. First members from the group keep their early price for life. Prices are preliminary.

Updates to the platform feed come as findings appear — several times a week, sometimes less.

## News and Telegram (Pro and Insider)

Every new platform, plugin update, idea, market analysis and poll from Rumer appears in three places at once: in Claude at the start of your session ("what's new?"), in the Telegram channel of your plan, and — for Insider — in the private group. To link Telegram, say **"connect Telegram"** in Claude: you get a personal link, press Start in the bot, and it sends your channel invites. The bot also sends personal notifications — pages that died, a Monday reminder to upload sales, a daily news digest, billing — at most one a day, any type can be turned off. What changed in each version: `CHANGELOG.md`.

## Install

PARASITER runs in Claude Code (needs a paid Claude plan that includes Claude Code).

Windows: the DataForSEO and SerpApi checks need the `python3` command — install Python from the Microsoft Store (python.org's installer adds only `python` and `py`). Antivirus with web / HTTPS protection (Norton Safe Web, Avast, Kaspersky, Bitdefender…): add `parasiter.affiliatecredo.com` to its exclusions, or the PARASITER server won't connect.

1. Open Claude Code and type two commands:

```
/plugin marketplace add Parasiter-SEO/parasiter-plugin
/plugin install parasiter@parasiter
```

2. During install the plugin asks for **"PARASITER key (Free, Pro or Insider)"**. Pro / Insider: paste the key from your welcome email (it starts with `psr_`). Free: leave it empty.
3. Check: say "my PARASITER plan". It shows your plan and its end date.

Need to change the key later? Reinstall the plugin and paste the key when asked. Never paste the key into a chat.

Agency and site owner routes: Pro (incl. paid placements); brand and site audit, client and site owner reports: Insider.

## Rules built into every skill

No fake reviews, tests, results, credentials, prices or deadlines. Personal experience only when real. Affiliate disclosure (client pages: brand disclosure) and last-checked date on every page. Only platforms where you can legitimately post. No income guarantees: income goals are yours, the system plans actions and tracks results.

## Risks

Google acts against site reputation abuse, platforms change moderation and remove pages, affiliate and payment networks can block traffic sources or niches. Spread pages across platforms, keep copies of every text, monitor.

© Rumer / Affiliate Credo. Licensed for the subscriber's personal use; redistribution of the plugin or server data is not permitted.

## Privacy and external services

**Stays on your machine / in your Claude project:** your journal, pages and their URLs, sales, affiliate links, texts, client files and your writer profile (name or pen name you give, background). PARASITER never uploads them.

**Sent off-platform, and only these:**

| Service | When | What is sent |
|---|---|---|
| PARASITER server (`parasiter.affiliatecredo.com`, the declared MCP connector) | Only with a key | Your key; account data from payment (email, plan, term, Telegram link if you connect it); platform search queries; bare platform domains your scan found dead (no URLs, nothing about you); weekly page-health counts per platform domain (how many removed or noindexed — no URLs, no sales); the schedule of your paid checks as you describe it ("24 starred pages") |
| DataForSEO API (`api.dataforseo.com`) — **your own account** | Only if you enter your DataForSEO API login and password in the plugin settings (the password is kept in secure storage) and say yes to a check (cost shown first). Runs through the bundled local `parasiter-dataforseo` server | Search queries, keywords and the page URLs being checked; billed to your DataForSEO balance. Credentials never go to the PARASITER server |
| SerpApi (`serpapi.com`) — **your own account** | Only if you enter your SerpApi API key in the plugin settings (kept in secure storage) and say yes to a position check, platform scan or new-platform search (searches shown first). Runs through the bundled local `parasiter-serpapi` server | Search queries; uses your SerpApi searches (free plan 250 a month). The key never goes to the PARASITER server |
| Public web pages | Platform and page checks | Plain HTTP requests to the platforms and your published pages to see if they are live, indexed (noindex) and keep your link |
| Other SEO tools (Semrush, Ahrefs, Serpstat, Google Search Console, GA4) | Only through connectors you add yourself | Whatever that connector sends under its own terms |

**Retention on the PARASITER server:** account data for the life of the subscription and as required for payment records; encrypted backups for 14 days. Details and deletion requests: privacy policy below.

Privacy policy: https://parasiter.affiliatecredo.com/privacy-en.html
