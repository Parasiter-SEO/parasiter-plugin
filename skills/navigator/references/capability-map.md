# PARASITER capability map

The user must always know every skill and agent PARASITER has and not forget them. This map is the fixed, approved format — keep its sections, columns and order; translate it into the user's working language at runtime (skill names and plan names stay as they are).

## When to show it

1. **First run** — once, right after the language and role questions (setup step 1), before the work environment block.
2. **Start of every new session** — as a reminder of what the system can do, after today's plan (navigator Step 3); during first setup, after the setup footer. Also on request any time ("map", "show all functions"). If the user says "don't show the map", save `capability_map: on-request` in the profile and from then on end the first reply of a session with one line instead: "All PARASITER functions: say **map**".
3. **In `help`** on "what can PARASITER do?", "show all skills", "capability map".

## Rules for showing it

- **Role:** each role sees only the rows of its set ("Rows per role" below); sections with no rows for the role are dropped. Role 1 (affiliate) sees the approved affiliate map; the agency, site-owner and creator rows only if asked. "Other" sees the full map.
- **Plan:** every row shows its plan. A skill above the user's plan (from `account_info`; no key = Free without a key, `plan: free` = Free with a key) stays in the map with the plan marked, e.g. "Insider — not on your plan", never hidden.
- **Panel numbers:** every skill row starts with its number in the user's role table in `panel.md` (first column "#"); affiliates don't see client-report rows — `client-reports` is "Analytics: what earns and what to scale"; under the map: "Reply with a number to start it · **0** — the panel with what you've tried".
- "How to start" is a ready phrase in the working language, adapted to the user's products and platforms when known ("What should I write about [their product]?").
- No other text around it: the title "PARASITER capability map", the sections, the agents, one closing line "Say any phrase from the third column — or just describe what you want."

## The map

**1. Plan**
| Skill | What it does | How to start | Plan |
|---|---|---|---|
| navigator | entry point: first setup, today's plan, leads you through the other skills | "Where do I start?", "What do we do today?" | Pro |
| goals | starting point, goals, Rumer's rule, weekly review | "Set my goals for 3 months", "Am I on track?" | Free |
| client-workspace | agencies and site owners: clients or your own site, brief, Month 0, monthly content plan with approval, today's plan across clients | "New client: Acme", "What do we do today for clients?" | Pro |
| creator-channels | creators: profile and channels, channel audit, search-based content plan, one idea → many pieces, media kit | "I'm a creator", "Audit my YouTube" | Free |

**2. Find**
| Skill | What it does | How to start | Plan |
|---|---|---|---|
| affiliate-finder | niche → programs, sorted by popularity in search, commission 15%+, approval type + Rumer's approval rules (on Pro: check offers you already chose) | "Which program should I take for nutra?" | Insider |
| niche-analysis | commercial queries, volumes, entry score from the top 20 | "Is this niche worth entering?" | Insider |
| platform-finder | where reviews rank in the top 10 now, free and paid separately; new platforms by category with Rumer's patterns — where affiliates post and clean ones with no competitors | "Where should I publish about joint supplements?", "Find new flipbooks" | Free key: 50-platform base + 3 scans a week · Pro: full |
| platform-analyzer | breakdown of one platform, score 0–100 | "Should I post on X?" | Pro |
| platform-feed | Rumer's feed: platforms, analysis, news, Telegram | "What's new?", "Connect Telegram" | Pro |
| brand-presence | agencies and site owners: site audit, brand profiles on socials and platforms, content audit | "Brand audit for Acme" | Insider |
| paid-placements | agencies and site owners: press-release wires and sponsored articles — prices, links, how to order | "Where can I buy an article for my site?" | Pro |

**3. Write**
| Skill | What it does | How to start | Plan |
|---|---|---|---|
| content-type-selector | what to write: topics picked by Rumer's rules — every topic scored by the 12-point filter ("Rumer filter score (of 12)"), best-of lists first | "What should I write about [product]?" | Free |
| sales-review-writer | 1,500+ word article by the rules + rollout to your other platforms | "Write a review for Medium" | Free |
| post-illustrations | infographics drawn by Claude + a free Gemini cover prompt | "Make images for the article" | Free |
| page-audit | two scores: Rumer's rules and copywriting | "Audit my article: link" | Free |
| video-seo | creators: title, description, chapters, keywords, captions, cover for every video and post; check after publishing | "Optimize my video" | Free |

**4. Publish and journal**
| Skill | What it does | How to start | Plan |
|---|---|---|---|
| work-log | journal of pages, sales, traffic, sources, republishing | "Published: link", "Here are my sales" | Pro |
| indexing | getting pages into Google: your own site + Search Console, Rumer's top indexers, a clean list for your indexer (you send it), stats by service | "Index these pages", "Which indexer should I use?" | Pro |
| platform-monitor | are your pages alive, platform cleanups, what to republish | "Are my pages alive?" | Pro |

**5. Measure**
| Skill | What it does | How to start | Plan |
|---|---|---|---|
| client-reports | what took off and the scale plan (agencies — the client report) | "What took off this month?" | Insider |
| help | help on the whole system | "What can PARASITER do?" | Free |

**Agents** (skills call them; you don't start them):
- platform-scout — probes "[product] review", finds platforms with reviews (for platform-finder)
- affiliate-scout — program terms with sources (for affiliate-finder)
- product-researcher — prices, deals, guarantee, product photos, competitors (for sales-review-writer)
- serp-analyst — breakdown of the results page and intent (for content-type-selector and niche-analysis)
- page-checker — checks lists of pages (for platform-monitor and work-log)
- independent-auditor — a fresh look at the article, like a doubtful buyer (for page-audit)
- index-checker — what blocks indexing and the clean list to send (for indexing)
- brand-auditor — the brand's profiles and site pages (for brand-presence and client-workspace)
- placement-scout — checks paid offers and marketplace sites (for paid-placements)
- video-seo-checker — what search can read on a channel or video (for video-seo and creator-channels)

## Rows per role

| Role | Rows | Agents |
|---|---|---|
| 1. Affiliate | navigator, goals, affiliate-finder, niche-analysis, platform-finder, platform-analyzer, platform-feed, content-type-selector, sales-review-writer, post-illustrations, page-audit, work-log, indexing, platform-monitor, client-reports, help | platform-scout, affiliate-scout, product-researcher, serp-analyst, page-checker, independent-auditor, index-checker |
| 2. Agency | client-workspace, brand-presence, niche-analysis, platform-finder, platform-analyzer, platform-feed, paid-placements, content-type-selector, sales-review-writer (brand mode), post-illustrations, page-audit, work-log, indexing, platform-monitor, client-reports, help | platform-scout, product-researcher, serp-analyst, page-checker, independent-auditor, index-checker, brand-auditor, placement-scout |
| 3. Creator | creator-channels, affiliate-finder, niche-analysis, content-type-selector, sales-review-writer, post-illustrations, page-audit, video-seo, work-log, platform-monitor, help | affiliate-scout, product-researcher, serp-analyst, page-checker, independent-auditor, video-seo-checker |
| 4. Site owner | client-workspace (own-site mode), brand-presence, niche-analysis, platform-finder, platform-analyzer, platform-feed, paid-placements, content-type-selector, sales-review-writer (brand mode), post-illustrations, page-audit, work-log, indexing, platform-monitor, client-reports, help | platform-scout, product-researcher, serp-analyst, page-checker, independent-auditor, index-checker, brand-auditor, placement-scout |
| 5. Other | the full map | all |

Keep this file in step with `help/references/catalog.md` and `roles.md` whenever a skill, agent or plan changes.
