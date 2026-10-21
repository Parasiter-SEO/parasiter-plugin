# Planning math

All formulas use the user's own numbers first: the baseline journal, then the progress log. When a number is missing, use the starting assumption below, mark it **assumption** in the goal file, and replace it with the measured value after two weeks of progress data.

## 0. Numbers from the baseline

| Number | From the baseline |
|---|---|
| Hours per page | the user's own "one page takes ~X h"; if not given: weekly hours ÷ pages per week (counts upkeep too, so it is a safe upper value) |
| Survival rate | live pages now ÷ pages built so far |
| Clicks per live page per day | if clicks are tracked: clicks per day ÷ live pages; if only income and EPC: income per day ÷ EPC ÷ live pages |
| EPC | network stats; else income ÷ clicks if both known |
| Share of time on new pages | 0 live pages → 70–100%; 20+ live pages → about 50%; 100+ → about 40% (assumption: the rest is refreshes, moves, monitoring) |

**Change from today**: show the goal as a multiple of the baseline (pages per week, hours, live pages, income). A goal above ~2× the current pace with the same hours is flagged in the reality check: either pace improves (templates, batching, a VA) or the plan needs more time.

Existing live pages count toward the goal: pages alive at the end = baseline live pages × survival + new pages × survival.

## 1. Capacity: pages the user can build

```
hours in horizon   = hours per day × days per week × weeks
hours for new pages = hours in horizon × share of time on new pages
pages buildable    = hours for new pages ÷ hours per page
```

Starting assumptions, only when the baseline has no pace (a beginner with no pages yet); replace with measured pace:

| Level | Hours per page (research, writing, images, publishing, check) | Share of time on new pages |
|---|---|---|
| Beginner | 2–3 | 70% (the rest is learning and checks) |
| Intermediate | 1–1.5 | 50% (the rest is index checks, refreshes, moving pages) |
| Advanced | 0.5–1 with batching and templates | 40% (the rest is monitoring, testing, reports) |

Measured pace = pages published in the last 2 weeks ÷ hours worked (ask the user for hours once a week, or use their stated hours per day).

## 2. Survival: pages still alive at the end

Platforms clean up, add noindex or delete accounts. Starting assumption: **40–70% of pages alive after 60 days**, lower for forums and open communities, higher for blog platforms the user controls. Use the middle (55%) until the progress log has 60-day data, then use the user's own rate per platform.

```
pages alive at the end ≈ pages built × survival rate
```

Pages that die are not lost work if the text is saved: reposting is part of the plan (weekly target "pages moved off dead platforms").

## 3. Income chain

Work backwards from the user's expectation:

```
income per day      = monthly target ÷ 30
clicks per day      = income per day ÷ EPC
live pages needed   = clicks per day ÷ clicks per live page per day
pages to build      = (live pages needed − baseline live pages × survival rate) ÷ survival rate
```

EPC and clicks per page differ by niche, offer, country and platform by more than ten times, so there is **no default EPC or clicks per page**. In order of preference:

1. The user's own data (affiliate network EPC, platform or Search Console clicks).
2. The user's estimate from past projects, marked assumption.
3. No data: ask the user to choose a cautious and an optimistic pair (for example EPC $0.30 / $1.00 and clicks per page 0.5 / 2 per day), show the chain for both, mark both as assumptions, and make month 1's milestone "measure real clicks and EPC from the first 20 pages". Recalculate at the first weekly review that has data.

Example only, not a benchmark: target $1,500/month → $50/day → at EPC $0.60, 83 clicks/day → at 1 click per live page per day, 83 live pages → at 55% survival, ~150 pages to build.

## 4. Gap and the three options

```
gap = pages to build (from goals or income chain, whichever is larger) − pages buildable
```

If the gap is positive, show how each option closes it and let the user choose:

- **More time**: extra hours per week = gap × hours per page ÷ share of time on new pages ÷ weeks.
- **Longer horizon**: extra weeks = gap × hours per page ÷ (hours for new pages per week).
- **Lower target**: what the current time allows (pages buildable, and the income chain run forwards from it).

Team or VA in the business model adds their hours to capacity; ask for their hours and pace separately.

## 5. Breaking down

- Monthly milestones grow, not flat: beginners ~50% of the average monthly pace in month 1, ~120% later. Intermediate and advanced start at the average.
- Platforms: at least 3 by the end of month 1 for everyone, so no single platform carries more than ~40% of live pages.
- Weekly targets = milestone delta ÷ weeks in the month, rounded up to whole pages.
- Daily quota = weekly target ÷ working days; leftovers go to the first days of the week.
- Each week reserves time for refreshes and moving pages once the user has 20+ live pages: about 1 refresh per 10 live pages per week (assumption).

## 6. Pace at the weekly review

```
pace per week   = pages published in the last 2 weeks ÷ 2
projected built = pages built so far + pace per week × weeks left
projected alive = projected built × measured survival rate
```

On track: projected values ≥ 95% of the goal. Behind: below 95%; offer the three options. Ahead: suggest adding a platform or an offer rather than raising the income goal on the user's behalf.
