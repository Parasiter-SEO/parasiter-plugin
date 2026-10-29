# PARASITER by Rumer

Parasite SEO inside your AI assistant for **affiliate marketers** and **agencies**: you publish pages on platforms Google already trusts — affiliates earn the commission, agencies send the client's buyers to the client's site. Skills and agents find platforms, pick the content type that sells, write the review, audit the page, track every sale, and tell you what to do next.

**Who it's for:** two full routes — **affiliate marketers** who earn with parasite SEO, at any stage, and **agencies** (SEO and marketing agencies, freelancers, in-house teams) running parasite SEO for clients.

On first run the navigator asks who you are and what for. Agencies get their own route; bloggers and course authors (own product) get only the tools that fit their work, without goals and the daily plan:

| Role | Tools |
|---|---|
| Affiliate (parasite SEO) | Goals, daily plan, journal with sales, every affiliate skill |
| Agency (SEO / marketing, freelancers, in-house) | A folder per client, onboarding brief, brand and site audit, monthly content plan with client approval, brand-mode texts, images in the client's style, audits, brand-safe platforms, monitoring, positions, GA4 + Search Console traffic, monthly white-label reports |
| Blogger / content creator | content types, sales reviews, page audit, images, journal, affiliate programs, niche analysis |
| Course author / own product | content types, page audit, images, platform finder / feed / analyzer / monitor, journal of pages |

Author: Rumer (Affiliate Credo) — 20 years in SEO, parasite SEO for the last 5.

> **Status: private beta (v0.18.0).** Skills and agents work without a key. The server part (platform database, feed, monitoring) is in development; skills that need it say so and fall back to a live search.

## How it works

0. **Basic setup: your pages, platforms and affiliate links.** Upload your affiliate links for every product you sell (a list, a table or screenshots), so every article gets the right link and you see which products have no pages yet. Already have pages? Upload the list (any file or pasted links). `work-log` puts every page in your journal, builds your own platform base from them, and one bulk check shows which are alive and indexed.
1. **Fill in your baseline journal** with `goals`: how many hours you work now, how many pages you publish, on which platforms and offers, and what it earns per day, week or month. These are your starting settings: everything after is calculated from them.
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
| `work-log` | Journal of work, traffic and sales, and your inventory: imports pages you already have and builds your own platform base; topics, priorities, top-10 positions and what to write where; logs every page, action and sale; imports network and platform exports; ties sales to pages by sub-ID; reports for any day, week or month; effectiveness by page, platform, offer, program, content type; check queue and weekly sales upload reminder |
| `content-type-selector` | Picks the content type and topic that sell before writing |
| `sales-review-writer` | Writes the sales review / comparison for your platform |
| `page-audit` | Audits a page by link or text, 0–100 score, fixes |
| `post-illustrations` | Image plan and generator prompts for your posts |
| `platform-finder` | Finds platforms for your niche; checked database with a key |
| `platform-analyzer` | Breaks down one platform, 0–100 score, verdict |
| `platform-feed` | News from Rumer: new platforms, plugin updates, ideas, weekly market analysis, polls; connects Telegram (key required) |
| `platform-monitor` | Alive / indexed / ranking status of your pages; scheduled with a key |
| `niche-analysis` | Keywords and SERPs via your own SEO tool API |
| `affiliate-finder` | Finds and scores affiliate programs (with agent) |
| `client-reports` | Performance analytics and client reports from your data |
| `client-workspace` | Agencies: clients, onboarding brief, Search Console / GA4 access, UTM, Month 0 baseline, content plan with approval, today's plan across clients, monthly report cycle |
| `brand-presence` | Agencies: client site quick audit, brand profiles on socials and platforms, content audit, profiles plan (with agent) |
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
| `independent-auditor` | `page-audit` | Reads a page without the context that wrote it, like a doubtful buyer, and flags weak spots and facts to verify |

Call a skill by describing the task ("set my goals for 6 months", "what should I do today", "audit my article") or directly, e.g. `/parasiter:navigator`.

Your files (kept in your project folder): `parasite-seo-profile.md`, `parasite-seo-goals.md`, `parasite-seo-progress.csv` (work and traffic journal), `parasite-seo-sales.csv` (sales), `parasite-seo-platforms.csv` (your platform base), `parasite-seo-links.csv` (your affiliate links).

## Language

The plugin is written in English and works in any language. On first run the navigator asks which language to work in and saves it in your profile: plans, explanations and your goal files then use it. The pages you publish can be in another language, set by your target country. Change it any time: "switch to Spanish".

## Plans

- **Free, $0** — the plugin without a key.
- **Pro, $19/month** — personal key: platform database, feed and weekly analysis, monitoring, navigator updates; new platforms about 7 days after they are found. **PARASITER Pro** Telegram channel and personal notifications from the bot.
- **Insider, $39/month** — everything in Pro, the full skill set and extra features, new platforms the day they are found. **PARASITER Insider** Telegram channel (platforms a week earlier, extra posts) and the private Insider group (discussion, polls).

Annual billing saves about 20%. First members from the group keep their early price for life. Prices are preliminary.

Updates to the platform feed come as findings appear — several times a week, sometimes less.

## News and Telegram (Pro and Insider)

Every new platform, plugin update, idea, market analysis and poll from Rumer appears in three places at once: in Claude at the start of your session ("what's new?"), in the Telegram channel of your plan, and — for Insider — in the private group. To link Telegram, say **"connect Telegram"** in Claude: you get a personal link, press Start in the bot, and it sends your channel invites. The bot also sends personal notifications — pages that died, a Monday reminder to upload sales, a daily news digest, billing — at most one a day, any type can be turned off. What changed in each version: `CHANGELOG.md`.

## Install (Claude Code)

```
claude plugin marketplace add Parasiter-SEO/parasiter-plugin
claude plugin install parasiter@parasiter
```

Or inside Claude Code: `/plugin marketplace add Parasiter-SEO/parasiter-plugin`, then `/plugin install parasiter@parasiter`.

Agency route: Pro; brand and site audit, white-label client reports: Insider.

## Rules built into every skill

No fake reviews, tests, results, credentials, prices or deadlines. Personal experience only when real. Affiliate disclosure (client pages: brand disclosure) and last-checked date on every page. Only platforms where you can legitimately post. No income guarantees: income goals are yours, the system plans actions and tracks results.

## Risks

Google acts against site reputation abuse, platforms change moderation and remove pages, affiliate and payment networks can block traffic sources or niches. Spread pages across platforms, keep copies of every text, monitor.

© Rumer / Affiliate Credo. Licensed for the subscriber's personal use; redistribution of the plugin or server data is not permitted.

## Privacy

Privacy policy: https://parasiter.affiliatecredo.com/privacy-en.html
