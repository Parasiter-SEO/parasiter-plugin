# Roles — who the user is and what PARASITER gives them

PARASITER has **two full routes**:
- **Affiliate** — the marketer who earns commissions with parasite SEO: baseline and goals, the daily plan, the journal with sales by sub-ID, weekly sales reminders, the check queue.
- **Agency** — SEO and marketing agencies, freelancers and in-house teams who run parasite SEO for clients: a folder per client, onboarding brief, brand and site audit, monthly content plan with client approval, today's plan across clients, positions and traffic to the client (Search Console, GA4 with UTM), monthly white-label reports. Run by `client-workspace`.

Bloggers and course authors / own-product owners get the tools from the set that honestly fit their work, with no goals and no daily plan — those are tuned for affiliate income and would give wrong numbers.

## The question (Step 0 of the navigator)

Ask once, before the profile questions, in the working language:

> Who are you, and what do you want PARASITER for?
> 1. **Affiliate** — I earn (or want to earn) commissions with parasite SEO pages
> 2. **Agency / SEO or marketing specialist** — I do SEO or marketing for clients (an in-house team works its own company as one client)
> 3. **Blogger / content creator** — I run my own blog, channel or newsletter
> 4. **Course author / own product** — I want traffic to my own course, product or service
> 5. **Something else / just looking**

If the user already said it in their first message ("I'm an affiliate", "I'm a blogger"), don't ask — confirm in one line and go on. Save the answer as `role` in `parasite-seo-profile.md`. The user can change it any time ("I'm actually an affiliate now").

## 1. Affiliate — parasite SEO (the main route)

Starting out or years in the game, no levels are assigned: the baseline (pages, sales, time) and the goals shape the plan. Everyone needs the same thing: a structure for the work and KPIs. So the route is always: profile → `goals` (baseline, goals) → today's plan (Step 3 of the navigator).

**Tools:** every affiliate skill, by plan (see `help/references/faq.md`).

## 2. Agency — SEO and marketing agencies, freelancers, in-house teams (full route)

Uses: getting client brands and pages into the top of Google, AI Overviews and "Discussions and forums" through trusted platforms, sending visitors to the client's site and channels, proving it every month with a report. Agency KPIs are rankings, traffic to the client and delivered work — never affiliate commission.

**Plans:** the route runs on Pro (clients, brief, content plan, production, journals, monitoring, positions, a plain monthly report from the journal). Insider adds the full brand and site audit with the agent, the white-label client report against Month 0 and niche analysis. On Pro, `client-workspace` uses the manual profile checklist and the plain report instead (its Step 2 and Step 6 say how).

Route: agency profile → new client onboarding → baseline (brand-presence + Search Console Month 0 + positions) → monthly content plan with client approval → production → publish and log per client → monthly report. Run by `client-workspace`; the daily question "what do we do today?" goes to its Step 4 (today's plan across clients), not to the affiliate daily plan.

| Need | Skill | Plan |
|---|---|---|
| Clients, onboarding, brief, access (GSC / GA4), UTM, content plan, today's plan across clients | client-workspace | Pro |
| Site quick audit, brand profiles on socials and platforms, content audit, profiles plan | brand-presence (+ brand-auditor agent) | Insider |
| What content type fits the query and platform | content-type-selector | Free |
| Brand texts: expert articles, guides, comparisons, LinkedIn / Medium / YouTube / press release, profile bios — disclosed as the brand's | sales-review-writer (brand mode) | Free |
| Images in the client's brand style: infographics by Claude, cover prompt with a choice of generator | post-illustrations | Free |
| Audit a page before the client sees it and after publishing | page-audit (agency scale) | Free |
| Fresh checked platforms, brand-safe | platform-feed, platform-finder (agency filter) | Pro |
| Check one platform | platform-analyzer | Pro |
| Pages alive / indexed / ranking per client | platform-monitor | Pro |
| A journal per client: pages, checks, positions, GA4 / platform traffic | work-log (`clients/<slug>/` journal; sales optional) | Pro |
| Keywords, SERP, competitors through their SEO API | niche-analysis | Insider |
| Monthly client report against Month 0, white-label PDF + dashboard | client-reports (Step 4b) | Insider |

**Not offered:** goals (income goals and Rumer's rule as an income plan), affiliate-finder, affiliate sales import as the main metric. If the client is an affiliate business itself, the agency can still log sales in the client's journal.

**Rule:** a client's product is never presented as an independent review, test or ranking. Pages say who is behind them — the brand, its expert, or "prepared with [Brand]". Profiles are the brand's real, declared accounts.

## 3. Blogger / content creator

Uses: monetizing their own blog, channel or newsletter with affiliate links, and better reviews.

| Need | Skill | Plan |
|---|---|---|
| What to write about a product | content-type-selector | Free |
| The review or comparison itself | sales-review-writer | Free |
| Audit a post | page-audit | Free |
| Images for posts | post-illustrations | Free |
| Log posts and sales | work-log | Pro |
| Find an affiliate program | affiliate-finder | Insider |
| Keywords and SERP via their API | niche-analysis | Insider |

**Not offered:** goals and the daily plan, the platform skills (finder, analyzer, feed, monitor), client-reports.

If the blogger wants to earn by publishing pages on other platforms, that is role 1: say so in one line and offer to switch.

## 4. Course author / own product or service

Uses: bringing buyers to their own course, product or service through pages on trusted platforms.

| Need | Skill | Plan |
|---|---|---|
| What content type fits the query | content-type-selector | Free |
| Audit a page | page-audit | Free |
| Images for posts | post-illustrations | Free |
| Find platforms | platform-finder (+ platform-feed) | Pro |
| Check one platform | platform-analyzer | Pro |
| Are the pages alive / indexed | platform-monitor | Pro |
| Log pages and checks | work-log (pages and checks) | Pro |
| Texts about their own product, disclosed as theirs | sales-review-writer (brand mode) | Free |

**Not offered:** goals and the daily plan, affiliate-finder, niche-analysis, client-reports, the review mode of sales-review-writer.

**Rule:** the user's own product is never presented as an independent review, test or "best of" ranking. Pages say who the author is and that it is their product.

## 5. Something else / just looking

Give the 5-step overview from `help` in a few lines, say who it is built for, and ask whether they are an affiliate. If not, offer the closest role above.

## How to talk to the agency role

- First run: one line — "PARASITER for agencies: one folder per client, brand audit, content plan with client approval, positions and traffic to the client, monthly white-label reports." — then hand over to `client-workspace` Step 0 (agency profile) and Step 1 (first client).
- Every session: read `clients/` — which clients exist, which is active — then `client-workspace` Step 4 when the user asks what to do today.

## How to talk to roles 3–4

- One line, once: "PARASITER is built for affiliates who earn with parasite SEO. For [role] you get these tools:" — then the table for the role, as a short list, and "What do you want to do first?"
- Route each request to the role's skills. A request for a skill outside the role: say it is built for affiliate work and is not part of their toolset; name the closest skill they do have.
- No daily plan and no goals for these roles. "What should I do today?" → show their toolset and ask which task.
- The plan still decides what works: a role's Pro or Insider skill needs that plan.
