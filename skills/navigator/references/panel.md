# PARASITER panel — the affiliate's working desk (№26, №29, №78)

The user can open the panel at any moment: "menu", "panel", "skills", "all functions", "0". They answer with a **number** and that skill starts at once. Numbers never change between sessions or plans, so the user learns them.

## Principle: offer, never demand

PARASITER does not know how the user wants to work today. Publishing, uploading reports and setup steps are **offers** the user may skip. Never block a skill because setup is open or nothing is published; never write "first publish…" or "you must upload…". A user who only explores the system is a normal user.

## The panel is the user's working desk (№29, №78)

PARASITER is first of all a **working panel**: every tool at hand, any moment — navigator and the day plan are help, not a required route. PARASITER is for affiliates only: one set of **16 skills and 7 agents**, numbered **1…16 without gaps**, fixed. No other roles, no client or agency functions. `client-reports` is shown only as "Analytics: what earns and what to scale" — never as client reports.

## 🏆 Top-10 of the week — pinned at the very top

Rumer's ranked pick of the 10 platforms that hold posts and bring results right now. He sets it in the bot every week (it holds 7 days). It is **the first block of the panel, above the bases**: one line with the date and the first three names — "🏆 Top-10 of the week (DD.MM): 1. X · 2. Y · 3. Z … — say **TOP**" — from `top10_week` (Pro / Insider). **TOP / ТОП / "top 10" / "best platforms this week"** opens the full list at once as a table: `# · Platform · Why (Rumer) · Type · Sign-up · Example`, then one line: "Want posts for these? Say **plan** — today's plan puts them first." `stale: true` → show the last list with "(new Top-10 coming soon)". On the panel page pass it to `dayplan.py` as `top10` ({week_of, stale, items: [{rank, name, why}]}). No list yet, or no server tools → skip the block silently. Free key or no key → the line stays on the panel, locked: "🏆 Top-10 of the week — 🔒 Pro: Rumer's 10 platforms that hold posts right now" — saying **TOP** gives the locked card (`upgrade-showcase.md` §2).

## 📚 Rumer's strategies and 🔁 Repeat this result — right under the Top-10 (№75)

One line on every plan: "📚 Rumer's strategies (8) — say **S** · 🔁 Saw a page in the top? Paste the link and say **repeat this result**". **S / С / "strategies"** opens the library (`strategies.md`); a pasted link with "repeat" runs `repeat-result.md`. On Free both are open (repeat: 1 a week, `repeat_result` counts it).

## Bases and data — first on the panel (№32)

The user's working data opens in one step, **above the skills**, with short codes so they never clash with skill numbers: **Б1…Б5** in Russian / Ukrainian, **B1…B5** in other languages (both always accepted, as are "base", "база", "журнал", "journal", "my platforms"). A code opens the table at once, no questions; then the user filters in words ("only forums", "in Spanish", "new this week", "★ only"). Shown as a table in the chat and on the panel page; never inside a code block. Bases don't count in "Explored".

| Code | Base | Opens with | Plan |
|---|---|---|---|
| Б1 / B1 | **Rumer's platform base** — checked platforms, live example posts, sign-up links; filters type / language / new this week | `platform-finder` Step 2 (`platforms_search`, `feed_latest`); Free key: Free mode A (`free_base`, the 50 snapshot) | Free key: 50 · Pro / Insider: all |
| Б2 / B2 | **My platforms** — the user's own base: priority, state, posts, in the top | `work-log` Mode 7 | Pro |
| Б3 / B3 | **Journal** — pages, sales, traffic, the check queue; today / week / month | `work-log` Mode 4 (report), Mode 5 (queue), Mode 6b (base page to open / download) | Free key: 10 pages (list + checks) · Pro |
| Б4 / B4 | **My offers and links** — the affiliate links library; plus **Rumer's starter programs** by niche (`starter_offers`, every plan, №73) | `work-log` Mode 10; starter programs: `first-post.md` Step 2 | Links library: Pro · starter programs: all |
| Б5 / B5 | **Feed** — new platforms, news, weekly analysis | `platform-feed` | Pro |

A base above the user's plan stays listed, marked "🔒 Pro" with what it would hold for them; choosing it gives the locked card (`upgrade-showcase.md` §2) and what works on their plan (Free key → the 50 snapshot).

### The panel — 16 skills · 7 agents
| # | Skill | What it does | Plan |
|---|---|---|---|
| **Plan** | | | |
| 1 | navigator | today's plan from your goals | Pro |
| 2 | goals | baseline, goals, weekly review | Free |
| **Find** | | | |
| 3 | affiliate-finder | offers and programs for a niche | Insider |
| 4 | niche-analysis | keywords, demand, can you enter | Free: 3 keywords · Insider |
| 5 | platform-finder | find platforms: menu of 7 groups → categories (incl. finance, coupons, gaming) (Rumer's patterns) · where reviews rank now | Free key / Pro |
| 6 | platform-analyzer | score one platform 0–100 | Pro |
| 7 | platform-feed | Rumer's feed, news, Telegram | Free: Telegram + free channel · Pro |
| **Write** | | | |
| 8 | content-type-selector | what to write: topics by Rumer's rules · forum cluster | Free |
| 9 | sales-review-writer | the article, 1500+ words | Free |
| 10 | post-illustrations | infographics + cover prompt | Free |
| 11 | page-audit | check a page by link or text | Free |
| **Publish and journal** | | | |
| 12 | work-log | journal of pages, sales, traffic | Free key: 10 pages · Pro |
| 13 | indexing | get pages into Google | Free: SpeedyIndex start · Pro |
| 14 | platform-monitor | are my pages alive | Pro |
| **Analytics** | | | |
| 15 | client-reports | analytics: what earns, what to scale | Insider |
| **Help** | | | |
| 16 | help | how anything works | Free |

Agents: platform-scout → 5 · affiliate-scout → 3 · product-researcher → 9 · serp-analyst → 8, 4 · page-checker → 14, 12 · independent-auditor → 11 · index-checker → 13

### "All functions"
"All functions" / "все функции" shows the same 16 skills and 7 agents — the affiliate panel is the whole of PARASITER (№78). Hidden skills (`roles.md`) are never listed.

### Cost marks on Claude Pro (№76)
On Claude Pro (`claude_plan: pro`) every skill row and base gets a mark after the plan: 🟢 ready / light, 🟡 cheap check, 🔴 heavy (`agents-and-plan.md` §7). Bases Б1–Б5 are 🟢. Skills: 🟢 navigator, goals, platform-feed, content-type-selector (Lite), sales-review-writer, post-illustrations, page-audit (self-check), work-log, client-reports, help; 🟡 platform-monitor, indexing (script check; index / positions on the user's SEO account); 🔴 affiliate-finder, niche-analysis, platform-analyzer, platform-finder is 🟢 from Rumer's base and 🔴 for a live search — show "🟢 base · 🔴 live". Legend under the panel (one line), on the visual page as `"cost"` per tile. Max / Team: no marks.

### How each row is shown
`N · name — what it does · plan · [🟢/🟡/🔴 on Claude Pro] · ✓ tried DD.MM / ○ not yet` — under the 🏆 Top-10 line and the "Bases and data" row (Б1…Б5), which always come first.
- The plan is marked against the user's plan (`account_info`): above their plan → "🔒 Pro" / "🔒 Insider", still listed, never hidden, in its usual place. Choosing it gives the locked card (`upgrade-showcase.md` §2) and the alternative on their plan.
- Above the panel, one line of progress counted on the panel: **"Explored: 9 of 16 skills · 5 of 7 agents"**; under it, the last 3 tried ("last: page-audit 03.11 · goals 02.11 · platform-finder 02.11").
- Under the panel: "Reply with a number. **0** — this menu any time." Below Insider, then the unlock line (№56): "🔒 N of M functions are locked on your plan. **Insider opens all 16 + 7 agents** (<Insider price>) · Pro opens 13 (<Pro price>) — prices from `account_info.prices` — <upgrade link>" (Pro user: the 3 Insider functions + /upgrade). N counts the locked rows of the panel.

## Starting a skill by number
- "5" (or "5 VigRX Plus", "12 https://…") starts that skill at once with what was given. Nothing given → the skill asks one short question or offers a quick demo on the user's own data; no data yet → a short example on a sample product, marked as a sample.
- The user's plan decides what runs; a skill above the plan answers with the locked card (`upgrade-showcase.md` §2) + what works on their plan.

## Tried — the path the user has walked
Every skill, on its first real run in a session, adds one line under `tried:` in `parasite-seo-profile.md`: `- <skill> · YYYY-MM-DD · <what was done, 3–6 words>` (keep the latest per skill; agents the same, marked `agent`). The panel and the progress line come from this list. Old profiles without `tried:` → build it once from the journal and the files that exist (goals file, journal rows, audits) and say "marked from your files".

## Jumping and coming back
- Any request in the middle of the day plan, the setup or another skill ("audit this page", "find offers") goes straight to the right skill. **Never** answer "let's finish the setup first".
- What was in progress is put on pause in the profile: `paused: <what> · <where it stopped> · YYYY-MM-DD` (day plan task N, setup step N, article draft on <topic>).
- After the jump's task is done, the Next steps block starts with **"1 — back to <paused thing>"** and ends with **"0 — menu"**. "Back" / "1" resumes exactly where it stopped; a new jump keeps the older pause under it (at most 3).

## Exploring mode
"I want to explore / try all the skills / learn the system" → `mode: explore` in the profile.
- No plan from goals, no reminders about publishing, reports or being behind.
- Show the panel, then offer the next untried skill (in panel order, skipping ones above the plan): one line what it does + "try it on <your product / a sample>?". After each, mark it tried and offer the next one or "0 — menu".
- The setup checklist is not shown as a footer in this mode; "where am I in setup?" still shows it.
- Leave with "let's work by plan" / "plan for today" → `mode: work`.

## On the visual page
The panel goes on the dashboard too — the "Bases and data" tiles first (`"bases"` in the JSON: code, name, what, plan), then the skills (`scripts/dayplan.py`, `"panel"` in the JSON — or `"kind": "panel"` for a page with only the panel, `parasiter-panel.html`): tiles by section, number, name, what, plan, ✓/○, and a copy button for the number. Locked tiles (`"locked": true`) show 🔒 and an **Unlock** button; pass `"upgrade": {"url": <upgrade link with utm_campaign=panel>, "text": <the unlock line>}` so the page shows the unlock banner and the buttons open the pricing page. The page cannot start a skill in Claude by itself: the button copies the number, the user pastes it in the chat.
