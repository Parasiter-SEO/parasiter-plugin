# Roles — who the user is and what PARASITER gives them

PARASITER has **four full routes**:
- **Affiliate** — the marketer who earns commissions with parasite SEO: baseline and goals, the daily plan, the journal with sales by sub-ID, weekly sales reminders, the check queue.
- **Agency** — SEO and marketing agencies, freelancers and in-house teams who run parasite SEO for clients: a folder per client, onboarding brief, brand and site audit, monthly content plan with client approval, today's plan across clients, positions and traffic to the client (Search Console, GA4 with UTM), monthly white-label reports. Run by `client-workspace`.
- **Site owner** — the owner of a site, shop, service or course who builds parasite pages around it: rankings, traffic with CTAs, dofollow links, paid placements, sales measured on the site. Run by `client-workspace` in own-site mode.
- **Blogger / creator** — free SEO through their own channels: optimized channels, a posting model, findable videos and posts, indexing, tracking in Google, monetization. Run by `creator-channels`.

## The question (Step 0 of the navigator)

Ask once, before the profile questions, in the working language:

> Who are you, and what do you want PARASITER for?
> 1. **Affiliate** — I earn (or want to earn) commissions with parasite SEO pages
> 2. **Agency / SEO or marketing specialist** — I do SEO or marketing for clients (an in-house team works its own company as one client)
> 3. **Blogger / content creator** — I grow my own channels (YouTube, Instagram, TikTok, Pinterest, blog…) without an ad budget
> 4. **Site owner / own product** — I promote my own site: shop, products, services or course
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
| Paid placements for clients: wires, sponsored articles, marketplaces (prnews.io…) — prices, packages, links, how to order | paid-placements (+ placement-scout agent) | Pro |
| Check one platform | platform-analyzer | Pro |
| Pages alive / indexed / ranking per client | platform-monitor | Pro |
| A journal per client: pages, checks, positions, GA4 / platform traffic | work-log (`clients/<slug>/` journal; sales optional) | Pro |
| Keywords, SERP, competitors through their SEO API | niche-analysis | Insider |
| Monthly client report against Month 0, white-label PDF + dashboard | client-reports (Step 4b) | Insider |

**Not offered:** goals (income goals and Rumer's rule as an income plan), affiliate-finder, affiliate sales import as the main metric. If the client is an affiliate business itself, the agency can still log sales in the client's journal.

**Rule:** a client's product is never presented as an independent review, test or ranking. Pages say who is behind them — the brand, its expert, or "prepared with [Brand]". Profiles are the brand's real, declared accounts.

## 3. Blogger / content creator (full route, free)

Uses: no ad budget — free SEO through their own channels. Their YouTube videos and Shorts, Reels, TikToks, Facebook posts, pins and blog posts can rank in Google (video results, the "Short videos" block, images, "Discussions and forums") and in each app's search. The route makes every channel and every piece findable, turns one idea into many pieces, gets fresh content indexed, tracks it in Google, and turns audience growth into income (sponsors with a media kit, affiliate links, own offer). The message to the creator: ads are expensive — your content can rank for free.

Route: run by `creator-channels` — creator profile ("digitize yourself") and every channel connected → channel audit and optimization (`video-seo-checker` agent) → search-based content plan and the posting model (one idea → long video, shorts, pins, text post) → each piece through `video-seo` (package before, check after) → indexing (free first) → tracking in Google → monetization.

| Need | Skill | Plan |
|---|---|---|
| Creator profile, channels, audit and optimization, content plan, posting model, indexing, media kit | creator-channels (+ video-seo-checker agent) | Free |
| Video and post package: title, description, chapters, spoken and on-screen keywords, captions, hashtags, cover, CTA; check after publishing | video-seo (+ video-seo-checker agent) | Free |
| What to make about a product or a buyer question | content-type-selector | Free |
| Reviews and text posts in the creator's voice, with disclosed links | sales-review-writer (review mode for products they review, brand mode for their own offer) | Free |
| Thumbnails, covers, pins | post-illustrations | Free |
| Audit a post or a blog article | page-audit | Free |
| Journal of pieces, positions in Google incl. video blocks, channel stats | work-log | Pro |
| Pieces alive / indexed | platform-monitor | Pro |
| Affiliate programs for their niche | affiliate-finder | Insider |
| Keywords and SERP through their API | niche-analysis | Insider |

**Not offered:** goals as affiliate income planning (a creator's goals are audience and pieces that rank — set in `creator-channels`), client-workspace. If the creator starts publishing review pages on other platforms for commissions, that is role 1; if they build a site around their offer, role 4 — say so in one line and offer to switch.

## 4. Site owner — own site, shop, services, course (full route)

Uses: the site is the centre. Many pages on trusted platforms around it rank for the site's queries (sooner than the site itself can), send buyers to the site with clear calls to action, and — where the platform allows — give the site **dofollow links** (link building). Bought articles and press releases on media sites are part of the investment. The goal is not visits but **sales and leads on the site**, measured end to end: page → visit (UTM) → order / lead → revenue against spend.

Route: run by `client-workspace` in **own-site mode** — the user's site is the one "client" (`clients/<site-slug>/`), no client approvals, no white-label. Onboarding brief → baseline (site audit + Search Console Month 0 + positions of the site's target queries) → monthly content and link plan (free platforms + paid placements) → production → publish and log with link target, rel, anchor and cost → monthly results: positions, visits, conversions and revenue from our pages, links live, spend and return.

| Need | Skill | Plan |
|---|---|---|
| The site's workspace: brief, Search Console / GA4, UTM, Month 0, monthly content and link plan, today's plan | client-workspace (own-site mode) | Pro |
| Site audit (indexing, landing pages, titles, speed, tracking, trust), profiles on socials and platforms, content audit | brand-presence (+ brand-auditor agent) | Insider |
| Landing pages checked by Rumer's content rules (first screen, offer, CTA, trust) | page-audit (brand scale) | Free |
| What content type fits the query and platform | content-type-selector | Free |
| Texts about their own product or service, disclosed as theirs, with CTAs to the site | sales-review-writer (brand mode) | Free |
| Images in the site's style | post-illustrations | Free |
| Free platforms, with link rules (dofollow / nofollow) marked | platform-finder, platform-feed, platform-analyzer | Pro |
| Paid placements: press-release wires, sponsored articles on media sites, marketplaces — prices, packages, dofollow, how to order | paid-placements (+ placement-scout agent) | Pro |
| Journal: pages, links given to the site (target, rel, anchor, cost), traffic, conversions and revenue from GA4 or the shop | work-log (`backlinks`, `site-roi`) | Pro |
| Pages alive / indexed / ranking, links still in place | platform-monitor | Pro |
| Keywords, SERP, competitors through their SEO API | niche-analysis | Insider |
| Monthly results report against Month 0 | client-reports (Step 4c) | Insider |

**Not offered:** goals as affiliate income planning, affiliate-finder, the review mode of sales-review-writer.

**Rule:** the user's own product is never presented as an independent review, test or "best of" ranking. Pages say who is behind them and that it is their product. Paid articles carry the label the publisher requires ("sponsored", "partner content"); links on paid pages are whatever the publisher gives — never ask a publisher to hide that a placement is paid.

## 5. Something else / just looking

Give the 5-step overview from `help` in a few lines, say who it is built for, and ask whether they are an affiliate. If not, offer the closest role above.

## How to talk to the agency role

- First run: one line — "PARASITER for agencies: one folder per client, brand audit, content plan with client approval, positions and traffic to the client, monthly white-label reports." — then hand over to `client-workspace` Step 0 (agency profile) and Step 1 (first client).
- Every session: read `clients/` — which clients exist, which is active — then `client-workspace` Step 4 when the user asks what to do today.

## How to talk to the site owner

- First run: one line — "PARASITER for your site: pages on trusted platforms that rank for your queries, send buyers to your site and give it links; paid placements when they pay off; sales measured on your site." — then `client-workspace` in own-site mode: Step 1 (brief about the site), Step 2 (Month 0).
- Every session: `client-workspace` Step 4 for today's plan.

## How to talk to the creator

- First run: two lines — "Ads are expensive; your content can rank in Google for free. PARASITER makes your channels and every video findable, turns one idea into many pieces and tracks them in Google." — then `creator-channels` Step 1 (profile and channels).
- "What should I do today?" → the next pieces from the creator's content plan (`creator-channels` Step 3), sized to their time.
- A request outside the role: name the closest skill they have.
- The plan still decides what works: a role's Pro or Insider skill needs that plan.
