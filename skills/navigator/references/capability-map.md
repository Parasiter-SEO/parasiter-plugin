# PARASITER capability map

The user must always know every skill and agent PARASITER has and not forget them. This map is the fixed, approved format — keep its sections, columns and order; translate it into the user's working language at runtime (skill names and plan names stay as they are).

## When to show it

1. **First run** — once, right after the language question (setup step 1), before the work environment block.
2. **Start of every new session** — as a reminder of what the system can do, after today's plan (navigator Step 3); during first setup, after the setup footer. Also on request any time ("map", "show all functions"). If the user says "don't show the map", save `capability_map: on-request` in the profile and from then on end the first reply of a session with one line instead: "All PARASITER functions: say **map**".
3. **In `help`** on "what can PARASITER do?", "show all skills", "capability map".

## Rules for showing it

- **One map for everyone (№78):** PARASITER is affiliates-only — 16 skills, 7 agents. Hidden skills (`roles.md`) are never shown.
- **Plan:** every row shows its plan. A skill above the user's plan (from `account_info`; no key = Free without a key, `plan: free` = Free with a key) stays in the map with the plan marked "🔒 Pro" / "🔒 Insider", never hidden. Below Insider, the map ends with the unlock line from `upgrade-showcase.md` §1 after the closing line.
- **Panel numbers:** every skill row starts with its number in `panel.md` (first column "#"); `client-reports` is "Analytics: what earns and what to scale"; under the map: "Reply with a number to start it · **0** — the panel with what you've tried".
- "How to start" is a ready phrase in the working language, adapted to the user's products and platforms when known ("What should I write about [their product]?").
- No other text around it: the title "PARASITER capability map", the sections, the agents, one closing line "Say any phrase from the third column — or just describe what you want." (plus the unlock line below Insider, №56).

## The map

**1. Plan**
| Skill | What it does | How to start | Plan |
|---|---|---|---|
| navigator | entry point: first setup, today's plan, leads you through the other skills | "Where do I start?", "What do we do today?" | Pro |
| goals | starting point, goals, Rumer's rule, weekly review | "Set my goals for 3 months", "Am I on track?" | Free |

**2. Find**
| Skill | What it does | How to start | Plan |
|---|---|---|---|
| affiliate-finder | niche → programs, sorted by popularity in search, commission 15%+, approval type + Rumer's approval rules (on Pro: check offers you already chose) | "Which program should I take for nutra?" | Insider |
| niche-analysis | commercial queries, volumes, entry score from the top 20 | "Is this niche worth entering?" | Insider |
| platform-finder | where reviews rank in the top 10 now, free and paid separately; new platforms by category with Rumer's patterns — where affiliates post and clean ones with no competitors; every find classed proven / Web 2.0 🔒 / Web 3.0 (Rumer's terms) | "Where should I publish about joint supplements?", "Find new flipbooks", "Find Web 2.0 platforms" | Free key: 50-platform base + 3 scans a week · Pro: full |
| platform-analyzer | breakdown of one platform, score 0–100 and Rumer's class; Web 3.0 mode: how people publish on a service with no sign-up form | "Should I post on X?", "How do people publish on X?" | Pro |
| platform-feed | Rumer's feed: platforms, analysis, news, Telegram | "What's new?", "Connect Telegram" | Pro |

**3. Write**
| Skill | What it does | How to start | Plan |
|---|---|---|---|
| content-type-selector | what to write: topics picked by Rumer's rules — every topic scored by the 12-point filter ("Rumer filter score (of 12)"), best-of lists first; **forum cluster** — competitor threads in the top and "Discussions and forums" → several fresh experience threads per query | "What should I write about [product]?", "Forum cluster for [query]" | Free |
| sales-review-writer | 1,500+ word article by the rules + rollout to your other platforms | "Write a review for Medium" | Free |
| post-illustrations | infographics drawn by Claude + a free Gemini cover prompt | "Make images for the article" | Free |
| page-audit | two scores: Rumer's rules and copywriting | "Audit my article: link" | Free |

**4. Publish and journal**
| Skill | What it does | How to start | Plan |
|---|---|---|---|
| work-log | journal of pages, sales, traffic, sources, republishing | "Published: link", "Here are my sales" | Free key: 10 pages · Pro |
| indexing | getting pages into Google: your own site + Search Console, Rumer's top indexers, a clean list for your indexer (you send it), stats by service | "Index these pages", "Which indexer should I use?" | Pro |
| platform-monitor | are your pages alive, platform cleanups, what to republish | "Are my pages alive?" | Pro |

**5. Measure**
| Skill | What it does | How to start | Plan |
|---|---|---|---|
| client-reports | what took off and the scale plan | "What took off this month?" | Insider |
| help | help on the whole system | "What can PARASITER do?" | Free |

**Agents** (skills call them; you don't start them):
- platform-scout — probes "[product] review", finds platforms with reviews (for platform-finder)
- affiliate-scout — program terms with sources (for affiliate-finder)
- product-researcher — prices, deals, guarantee, product photos, competitors (for sales-review-writer)
- serp-analyst — breakdown of the results page and intent (for content-type-selector and niche-analysis)
- page-checker — checks lists of pages (for platform-monitor and work-log)
- independent-auditor — a fresh look at the article, like a doubtful buyer (for page-audit)
- index-checker — what blocks indexing and the clean list to send (for indexing)

Keep this file in step with `help/references/catalog.md`, `panel.md` and `roles.md` whenever a skill, agent or plan changes.
