# PARASITER panel — every skill under a fixed number (№26)

The user can open the panel at any moment: "menu", "panel", "skills", "all functions", "0". They answer with a **number** and that skill starts at once. Numbers never change between sessions, plans or roles, so the user learns them.

## Principle: offer, never demand

PARASITER does not know how the user wants to work today. Publishing, uploading reports and setup steps are **offers** the user may skip. Never block a skill because setup is open or nothing is published; never write "first publish…" or "you must upload…". A user who only explores the system is a normal user.

## The panel (show it in the working language, in this order)

| # | Skill | What it does (3–5 words) | Plan |
|---|---|---|---|
| **Plan** | | | |
| 1 | navigator | today's plan from your goals | Pro |
| 2 | goals | baseline, goals, weekly review | Free |
| **Find** | | | |
| 3 | affiliate-finder | offers and programs for a niche | Insider |
| 4 | niche-analysis | keywords, demand, can you enter | Insider |
| 5 | platform-finder | where reviews rank now | Free key / Pro |
| 6 | platform-analyzer | score one platform 0–100 | Pro |
| 7 | platform-feed | Rumer's feed, news, Telegram | Pro |
| 8 | paid-placements | news sites, PR wires, prices | Pro |
| **Write** | | | |
| 9 | content-type-selector | what to write: topics by Rumer's rules | Free |
| 10 | sales-review-writer | the article, 1500+ words | Free |
| 11 | post-illustrations | infographics + cover prompt | Free |
| 12 | page-audit | check a page by link or text | Free |
| **Channels and brand** | | | |
| 13 | creator-channels | your channels as Google traffic | Free |
| 14 | video-seo | a video made findable | Free |
| 15 | brand-presence | brand profiles and site audit | Insider |
| 16 | client-workspace | clients or your own site | Pro |
| **Publish and journal** | | | |
| 17 | work-log | journal of pages, sales, traffic | Pro |
| 18 | indexing | get pages into Google | Pro |
| 19 | platform-monitor | are my pages alive | Pro |
| **Measure** | | | |
| 20 | client-reports | what earns, what to scale | Insider |
| **Help** | | | |
| 21 | help | how anything works | Free |

**Agents** (a skill calls them; the user can ask for one by name, it runs through its skill):
platform-scout → 5 · affiliate-scout → 3 · product-researcher → 10 · serp-analyst → 9, 4 · page-checker → 19, 17 · independent-auditor → 12 · index-checker → 18 · brand-auditor → 15 · placement-scout → 8 · video-seo-checker → 14

### How each row is shown
`N · name — what it does · plan · ✓ tried DD.MM / ○ not yet`
- The plan is marked against the user's plan (`account_info`): above their plan → "(Pro)" / "(Insider)", still listed, never hidden. Choosing it gives the one-line upgrade note and the alternative on their plan.
- Role filter: affiliates see all rows; other roles see their rows first and the rest under "Also available".
- Above the panel, one line of progress: **"Explored: 8 of 21 skills · 4 of 10 agents"**; under it, the last 3 tried ("last: page-audit 03.11 · goals 02.11 · platform-finder 02.11").
- Under the panel: "Reply with a number. **0** — this menu any time."

## Starting a skill by number
- "5" (or "5 VigRX Plus", "12 https://…") starts that skill at once with what was given. Nothing given → the skill asks one short question or offers a quick demo on the user's own data; no data yet → a short example on a sample product, marked as a sample.
- The user's plan decides what runs; a skill above the plan answers with its upgrade line + what works on their plan.

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
The panel goes on the dashboard too (`scripts/dayplan.py`, `"panel"` in the JSON — or `"kind": "panel"` for a page with only the panel, `parasiter-panel.html`): tiles by section, number, name, what, plan, ✓/○, and a copy button for the number. The page cannot start a skill in Claude by itself: the button copies the number, the user pastes it in the chat.
