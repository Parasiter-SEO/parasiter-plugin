# Rumer's 12-point topic filter

Shown to the user as "Topics picked by Rumer's rules", column "Rumer filter score (of 12)".

Score each criterion 0, 1 or 2:

| # | Criterion | 0 | 1 | 2 |
|---|---|---|---|---|
| 1 | **Buying intent** — is the searcher close to purchase? | informational (how to use, what is) | researching the category | review / vs / price / best / legit |
| 2 | **Unresolved doubt** — is there a question the SERP answers poorly? | fully answered | answered, but outdated or thin | open gap (no prices, no comparison, no answer to "is it legit") |
| 3 | **Unique data or experience** — does the author have something others don't? | nothing beyond the product page | own research, checked prices, compared terms | own use, photos, data, a real coupon |
| 4 | **Clear CTA** — is there one obvious commercial action? | none | several competing actions | one action: buy / pick a package / use the coupon |
| 5 | **Platform fit** — does the format suit the platform and are links allowed? | links banned or format off | fits with limits (link in profile, keyword filter) | native format, links allowed |
| 6 | **Update and reuse** — can it be refreshed and rolled out later? | one-off news | can be refreshed | refreshable and rolls out to other platforms in other formats |

| Total | Decision |
|---|---|
| 10–12 | Test first |
| 7–9 | Publish when there is time |
| 4–6 | Reword the topic |
| 0–3 | Do not publish |

This is a filter for ideas, not a ranking prediction.

## Decisions cite rules

The Decision column names the band and, where a rule shaped it, the rule — never "I think". Examples:
- "test first"
- "when there is time — no own data yet (criterion 3: 0); add a price check to raise it"
- "reword: no 'discount' / 'coupon' in the title — the platform's keyword filter"
- "do not publish: informational query — Rumer's commercial-intent rule"
- "experience angle dropped — honesty rule: no personal use"

Rule sources: this filter, the commercial-intent rule (content-type-selector Step 2), the platform's rules (user's platform base, platform analysis), the honesty rules.

## Breakdown on request ("why 9?")

```
#4 Best Testosterone Boosters for Men Over 40 — 9/12 · when there is time
Buying intent        2  "best … for men over 40" — choosing what to buy
Unresolved doubt     2  top pages list products without prices or age-specific picks
Own data             1  research only, no personal use
Clear CTA            2  one pick with a package link
Platform fit         1  link only in the profile on this platform
Update and reuse     1  refreshable; rollout limited
How to raise it: add a checked price/package table (+1 own data) or move it to a platform that allows body links (+1 fit) → 11, test first.
```

## Suggested test mix (30 publications)

| Group | Posts |
|---|---|
| Comparisons and choice | 10 |
| Personal experience / results | 8 |
| Doubts / problems | 6 |
| Prices / packages / tools | 5 |
| General review (control) | 1 |

Spread tests across platforms and formats; don't put 30 similar texts on one domain. Keep one log.

## What to record per publication
URL, platform, date, cluster, country, main query, SERP type; impressions, position, clicks, CTR (where available); affiliate clicks, EPC, conversions, confirmed commissions; indexing and position changes; what was unique (test, table, screenshots, calculator).

Main metric where data exists: revenue per 1000 search impressions
RPM_SERP = (clicks / impressions) × (sales / clicks) × average commission × 1000.
Where third-party platforms hide impressions, compare EPC = confirmed commission / affiliate clicks, and revenue per publication.

Review at 14 / 30 / 60 days: update winners, reposition losers — don't clone them.
