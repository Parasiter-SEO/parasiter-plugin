# PARASITER by Rumer

Parasite SEO inside your AI assistant. Skills and agents that find platforms, pick the content type that sells, write the review, audit the page, and tell you what to do next at your level.

Author: Rumer (Affiliate Credo) — 20 years in SEO, parasite SEO for the last 5.

> **Status: private beta (v0.2.0).** Skills and agents work without a key. The server part (platform database, feed, monitoring) is in development; skills that need it say so and fall back to a live search.

## How it works

1. **Fill in your baseline journal** with `goals`: how many hours you work now, how many pages you publish, on which platforms and offers, and what it earns per day, week or month. These are your starting settings: everything after is calculated from them.
2. **Set your goals** from that starting point: pages, platforms, offers, time and the income you realistically expect, over 1 week to 12 months. The skill compares the goal with your real pace, breaks it into monthly milestones and weekly targets, and marks every number it had to assume.
3. **Ask for today's plan** with `navigator`. It reads your goals, progress and level, checks what changed on your platforms, and gives you 2–5 tasks that fit today's time. You don't pick commands: each task goes to the right skill.
4. **Report what you did** ("added an article: URL", "sent it to indexing", "2 sales"). `work-log` writes it into your work journal at once. Every page in the journal is queued for alive and index checks and a conversion audit, so nothing you published is forgotten. Ask "what did I do this week?" or "report for September" any time.
5. **Weekly review**: the goals skill compares plan and fact from the journal, replaces assumptions with your real numbers, and adjusts the next week.

## Skills

| Skill | What it does |
|---|---|
| `goals` | Baseline journal, goals over 1 week to 12 months, reality check, milestones, weekly targets, progress log, weekly review |
| `navigator` | Entry point: today's plan from your goals, progress, time and level; routes each task |
| `work-log` | Work journal: logs every page and action as you go; reports for a day, week, month or any dates; queue of pages due for alive/index checks and conversion audits |
| `content-type-selector` | Picks the content type and topic that sell before writing |
| `sales-review-writer` | Writes the sales review / comparison for your platform |
| `page-audit` | Audits a page by link or text, 0–100 score, fixes |
| `post-illustrations` | Image plan and generator prompts for your posts |
| `platform-finder` | Finds platforms for your niche; checked database with a key |
| `platform-analyzer` | Breaks down one platform, 0–100 score, verdict |
| `platform-feed` | New platforms and weekly market analysis from Rumer (key required) |
| `platform-monitor` | Alive / indexed / ranking status of your pages; scheduled with a key |
| `niche-analysis` | Keywords and SERPs via your own SEO tool API |
| `affiliate-finder` | Finds and scores affiliate programs (with agent) |
| `client-reports` | Performance analytics and client reports from your data |

## Agents

Skills hold the method; agents do the heavy research and checking in their own context and hand back a table of facts with sources and dates. Agents collect, the skill decides. You never call an agent yourself — the skill sends it.

| Agent | Works for | What it does |
|---|---|---|
| `platform-scout` | `platform-finder` | Searches the SERP and forum/community footprints for a niche, checks each candidate: open registration, fresh indexing, noindex, links, moderation |
| `affiliate-scout` | `affiliate-finder` | Collects published program terms (model, rate, cookie, payout, allowed traffic) and checks the merchant offer page |
| `product-researcher` | `sales-review-writer` | Collects current specs, packages, prices, discounts, shipping and guarantee from the merchant's own pages for the quick facts box |
| `serp-analyst` | `content-type-selector`, `niche-analysis` | Breaks down the top 10 for buyer queries: formats, parasite platforms, SERP features, open buyer questions |
| `page-checker` | `platform-monitor`, `work-log` | Checks lists of your pages: live, noindex, indexed, affiliate link working, position |
| `independent-auditor` | `page-audit` | Reads a page without the context that wrote it, like a doubtful buyer, and flags weak spots and facts to verify |

Call a skill by describing the task ("set my goals for 6 months", "what should I do today", "audit my article") or directly, e.g. `/parasiter:navigator`.

Your files (kept in your project folder): `parasite-seo-profile.md`, `parasite-seo-goals.md`, `parasite-seo-progress.csv`.

## Language

The plugin is written in English and works in any language. On first run the navigator asks which language to work in and saves it in your profile: plans, explanations and your goal files then use it. The pages you publish can be in another language, set by your target country. Change it any time: "switch to Spanish".

## Plans

- **Free, $0** — the plugin without a key.
- **Pro, $19/month** — personal key: platform database, feed and weekly analysis, monitoring, navigator updates; new platforms about 7 days after they are found.
- **Insider, $39/month** — everything in Pro, the full skill set and extra features, new platforms the day they are found, private Telegram group.

Annual billing saves about 20%. First members from the group keep their early price for life. Prices are preliminary.

Updates to the platform feed come as findings appear — several times a week, sometimes less.

## Install (Claude Code)

```
claude plugin marketplace add Parasiter-SEO/parasiter-plugin
claude plugin install parasiter@parasiter
```

Or inside Claude Code: `/plugin marketplace add Parasiter-SEO/parasiter-plugin`, then `/plugin install parasiter@parasiter`.

## Rules built into every skill

No fake reviews, tests, results, credentials, prices or deadlines. Personal experience only when real. Affiliate disclosure and last-checked date on every page. Only platforms where you can legitimately post. No income guarantees: income goals are yours, the system plans actions and tracks results.

## Risks

Google acts against site reputation abuse, platforms change moderation and remove pages, affiliate and payment networks can block traffic sources or niches. Spread pages across platforms, keep copies of every text, monitor.

© Rumer / Affiliate Credo. Licensed for the subscriber's personal use; redistribution of the plugin or server data is not permitted.
