---
name: platform-finder
description: Find platforms where a parasite SEO page can be published and rank — forums, communities, Q&A, article and profile platforms, document hosts, site builders, event and fundraising pages — filtered by niche, language, link rules, indexing speed and moderation. Use when the user asks where to publish, wants new platforms, forums or communities for a niche, or a list of platforms that work now.
---

# Platform Finder

## Work label (testing period)

Start every reply produced by this skill with one line naming it, so the user always sees which part of PARASITER is working:
`▸ PARASITER · platform-finder`
If you called agents for this reply, add them after an arrow: `▸ PARASITER · platform-finder → serp-analyst, product-researcher`. If you hand off to another skill, the next reply carries that skill's label. One line only, no other system talk.

Part of PARASITER by Rumer (Affiliate Credo).

Platforms live days to months: they get spammed, cleaned up, noindexed or close registration. A list is only worth something if it is **fresh and checked**.

**What we look for:** not new, untested platforms, but the ones where **affiliate review pages are published and indexed right now**. If review pages of affiliate products rank on a domain today, it is a proven parasite platform: anyone can post there and Google keeps the pages. A platform with no affiliate posts on it is not a lead, however promising it looks. Whether links on it are indexed or followed does not matter — what matters is that **the pages themselves are indexed**.

**Free and paid are always separate.** Free: platforms where users post themselves (Facebook, Reddit, Quora, forums, article and document platforms, site builders, podcasts, Gamma, Pressbooks, ResearchGate…). Paid: news and media sites (all of them are paid — sponsored posts, "partner content", press releases), PR wires, paid placements. Every list shows them in separate tables.

Reply in the user's language.

## Step 1 — Filters

Ask only what is missing:
- Niche and the user's products (from the links library) or the products to probe.
- Language and country.
- Free only, paid only, or both.
- Read the user's base (`work-log` `platforms`): platforms already in it are marked "yours" with their state; `dropped` and `dead` are skipped unless asked.

## Step 2 — The author's base first (Pro / Insider)

If `platforms_search` is available, call it with the filters. These are platforms Rumer checked by hand; he adds them every Monday and often in between, several a day. Pro sees them ~7 days after they are added, Insider the same day. Show them as a table (free and paid separately) and keep the server's notes as written.

If the server is not connected, say once: "Checked platforms from Rumer come with a Pro key. Meanwhile we can run a live scan." and go to Step 3.

## Step 3 — Live scan: where reviews of affiliate products are published now

**The live scan is paid** (the user's DataForSEO balance) — always say so before running it, with the number of products and the rough cost, and run it only after a yes (`work-log` Rules: paid checks).

1. **Products to probe** — `references/products-seed.md`: the user's own products first, then the current top of the marketplaces in their niche (ClickBank, Digistore24, BuyGoods…), the seed list only as a fallback. 20–50 names is a good scan.
2. **Scan** — every affiliate review page has the same two words: *[product name] review*. Search them and collect every result that is not the product's own site or a store:
   ```
   python3 scripts/platformscan.py products.txt --country us --dry-run   # the cost first (top 10 by default)
   python3 scripts/platformscan.py products.txt --country us --base parasite-seo-progress.csv
   ```
   Output: platforms grouped as **Free / Paid / To check**, each with how many different products have review pages there, the best position, the SERP blocks (Discussions and forums, AI Overview, videos), whether it is already the user's, and example pages. Saved as `platforms-scan.csv`. `--suffix reviews` / `complaints` for other probes; `--device mobile` for the mobile SERP.
3. **Without an API** — the same probe with web search (free, but far fewer results and no positions), or give the user the queries to run in Google (incognito, target country).
4. **Similar to what works** — the author's archive of platforms that ranked in 2025–2026 (on the server) shows which kinds of places are worth it: the scan's "To check" domains of the same kind (document hosts, community projects, notebooks, podcast hosts, site builders) come first.

A platform with review pages of **many different products** is the strongest lead: it is where everyone posts and Google keeps it.

## Step 4 — Quick check of the top candidates (free)

For the top 5–10 "free" and "to check" platforms (details in `platform-analyzer`):
- Can a new user register and post the same kind of page?
- Are fresh posts indexed (the scan already shows pages in Google; check one recent one)?
- Any sign of cleanup (removed pages, login wall, noindex)?

Drop dead ones. Mark uncertain ones "test".

## Step 5 — Output

```
Platforms with affiliate reviews · [niche] · [country] · checked [date]
Free
| Platform | Type | Products with reviews | Best pos. | SERP blocks | Yours | Next step |
Paid
| Platform | Type | Products with reviews | Best pos. | Price / how to buy (if known) | Next step |
```
Then: top 3 free platforms to start with and why (one line each), and "run platform-analyzer on #1 before posting". Paid ones only with what is known about the price; never guess a price.

## Rules

- Only platforms where the user can legitimately create an account and post, or buy a placement. Reviews found in other organisations' upload folders or forms (university and government sites, `wp-content/uploads`, contact-form files) are hacked or abused sites: the scan skips them and they are never suggested — they are not platforms, they are abuse, and they burn domains and offers.
- Spread across platforms; never rely on one.
- Every list is a snapshot: write the check date on it.
- Reference: the author's archive of domains that ranked in 2025–2026 lives on the server (history, not live status).
