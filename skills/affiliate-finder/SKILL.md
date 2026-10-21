---
name: affiliate-finder
description: Find and compare affiliate programs and offers for a niche and traffic type (parasite SEO pages on public platforms) — commission model and rate, cookie, payout threshold, network vs direct program, traffic-source rules, offer page quality, demand and saturation — using the affiliate-scout agent for research. Use when the user asks which affiliate program or offer to promote, wants programs for a niche, or compares offers by commission, EPC or terms.
---

# Affiliate Finder

Part of PARASITER by Rumer (Affiliate Credo).

Choose the offer before writing a word: a strong page for a bad offer earns nothing. The author's filter is simple — **real demand, strong commission, an offer page that converts, and a program that accepts traffic from public platforms.**

Reply in the user's language.

## Step 1 — Inputs

Niche or product category, country/language, traffic type (parasite pages: forums, Medium, PDFs, press releases…), preferred models (CPA, RevShare, recurring), payout methods, networks the user already belongs to.

## Step 2 — Research

Delegate the search to the `affiliate-scout` agent (or do it yourself with web search): networks and direct programs for the niche, their published terms, and the merchant offer pages. Collect only published terms with the source link and date.

## Step 3 — Evaluate

Score each program with `references/criteria.md`. Key checks:
- **Demand** — the product is actually searched for (niche-analysis or the user's SEO tool).
- **Commission** — rate and model; average order value; upsells that change the real payout.
- **Traffic rules** — does the program allow content/SEO traffic from third-party platforms? Some big networks ban accounts for "low-quality" traffic sources; smaller programs and networks are usually glad of it. Ask the affiliate manager when unclear.
- **Saturation** — products every affiliate pushes (spam-heavy marketplaces, constant refunds, aggressive price cuts) convert worse; prefer less crowded offers with real demand.
- **Offer page** — converts? clear packages, guarantee? Red flags: lead-capture page before the sales page, pop-up forms, price on the page far below what the listing promised.
- **Payout** — threshold reachable with the expected sales; network (one payout across many offers) vs many small direct programs (hard to reach minimums).
- **Cookie and attribution** — longer cookie helps nofollow platforms where readers return later.

## Step 4 — Output

```
Programs for [niche] · checked [date]
| Program | Network/direct | Model | Rate | Cookie | Min payout | Traffic rules | Saturation | Score |
```
Recommend 1–3, one line why each. Suggest the content plan: high-commission lesser-known product → best-of comparison where it can be placed high **only if it genuinely fits**; known product with demand → single review + A vs B + packages page.

## Rules

- Only published, verifiable terms with source and date; unknown → "ask the manager".
- No promoting products the user believes are scams; drop programs with clear deceptive funnels.
- No earnings estimates presented as forecasts.
