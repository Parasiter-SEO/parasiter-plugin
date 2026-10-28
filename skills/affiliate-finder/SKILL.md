---
name: affiliate-finder
description: Find and compare affiliate programs and offers for a niche and traffic type (parasite SEO pages on public platforms) — commission model and rate, cookie, payout threshold, network vs direct program, traffic-source rules, offer page quality, demand and saturation — using the affiliate-scout agent for research. Use when the user asks which affiliate program or offer to promote, wants programs for a niche, or compares offers by commission, EPC or terms.
---

# Affiliate Finder

## Work label (testing period)

Start every reply produced by this skill with one line naming it, so the user always sees which part of PARASITER is working:
`▸ PARASITER · affiliate-finder`
If you called agents for this reply, add them after an arrow: `▸ PARASITER · affiliate-finder → serp-analyst, product-researcher`. If you hand off to another skill, the next reply carries that skill's label. One line only, no other system talk.

## Next steps (end of every reply)

The user should always see where to go next without asking. End each reply with one short line of 2–3 options that fit what just happened, each with the phrase to say, e.g. `Next: `niche-analysis` (is the niche open) · `content-type-selector` (first topic for the offer) · save your affiliate links to the profile.` Offer only what their plan includes; a Pro/Insider feature on Free is named once with its plan in brackets. When the user seems lost or asks what else there is, add: "All PARASITER functions: say **help**." Things that need no decision (logging, monitoring, saving to the base) are done automatically, not offered.

Part of PARASITER by Rumer (Affiliate Credo).

Choose the offer before writing a word: a strong page for a bad offer earns nothing. The author's filter: **the offer is popular in search, the commission is at least 15%, and the program accepts traffic from public platforms.** Networks and direct programs are both fine.

Reply in the user's language.

## Step 1 — Niche first

If the user has no niche yet (beginner), show the niches and let them pick one — every niche is open to them; don't choose for them. Niches the author works with, then others that suit parasite SEO:

| Niche | Typical offers | Notes |
|---|---|---|
| **Nutra / supplements** | weight loss, men's health, joints, sleep, sports nutrition | the author's main niche; direct programs pay 30–50% |
| **Casino / gambling / betting** | casinos, sportsbooks, sweepstakes | high RevShare or CPA; legal only in some countries, many platforms ban these links — check GEO and the platform's rules first |
| **Crypto** | exchanges, wallets, trading bots, prop firms | recurring RevShare; platforms and Google are strict — check rules |
| **Roblox and gaming** | gift cards, game keys, gaming gear and accounts services | the audience is often under 18: only legitimate offers, never "free Robux" or gambling-style offers |
| **Software / SaaS / AI tools** | VPN, hosting, AI writers, antivirus, SEO tools | recurring commissions, low refunds |
| Others worth checking | dating, personal finance and loans, e-commerce and Amazon, online courses, pets, home and garden, travel | |

Then the inputs: country / language, offers the user already runs, networks they belong to.

## Step 2 — Research

Delegate the search to the `affiliate-scout` agent (or do it yourself with web search): networks and direct programs for the niche, their published terms, and the merchant offer pages. Collect only published terms with the source link and date.

## Step 3 — Evaluate

**Search popularity comes first** — it is what the author looks at. For every candidate offer measure how often people search the product itself: "[product] review(s)", "[product] reviews complaints", "[product] vs …", "buy / coupon / discount [product]", "does [product] work". Popular in search = buyers already looking = a parasite page can catch them.
- With the user's SEO API (DataForSEO recommended): monthly volume for these queries in the user's country. It is a paid call: name the number of offers and queries and the rough cost, and wait for a yes (`work-log` Rules: paid checks).
- Without an API: free signals only — Google autocomplete for "[product] r…", Google Trends, "People also ask", how many review pages and videos exist — and mark the result "rough, no volumes".

Then the filters:
- **Commission at least 15%** of the sale (RevShare or CPA counted as a share of the average order). Below 15% → skip unless the user insists.
- **Traffic rules** — content/SEO traffic from third-party platforms allowed? Unclear → "ask the manager".
- **Payout** — threshold reachable; payment record.
- **Country / legality** — for gambling, crypto, finance and supplements with medical claims: legal in the target country, allowed on the target platforms.
Saturation, offer page quality and cookie are noted in the table but don't decide on their own.

## Step 4 — Output

```
Programs for [niche] · checked [date]
| Program | Network/direct | Searches/mo | Model | Rate | Cookie | Min payout | Traffic rules | Score |
```
Sort by search popularity. Recommend 1–3, one line why each ("~2,400 searches/mo for reviews, 40%, direct"). Suggest the content plan: high-commission lesser-known product → best-of comparison where it can be placed high **only if it genuinely fits**; known product with demand → single review + A vs B + packages page.

## Rules

- Recommend only programs found by public research for this user's niche (`affiliate-scout`, web search, the user's own networks). Never name programs, offers or numbers from the plugin author's own business, and never use a program name that appears only in the plugin's examples.

- Only published, verifiable terms with source and date; unknown → "ask the manager".
- No promoting products the user believes are scams; drop programs with clear deceptive funnels.
- No earnings estimates presented as forecasts.
