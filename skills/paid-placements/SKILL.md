---
name: paid-placements
description: Paid publications as part of parasite SEO for site owners and agencies — a base of press-release wires (GlobeNewswire, ACCESS Newswire, EIN Presswire, XPR Media…), sponsored-article marketplaces (prnews.io and similar) and media sites that sell articles, with packages, public prices or how to request a quote, link policy (dofollow / nofollow), distribution, niche restrictions; picks the placements that fit a goal and budget, checks a marketplace catalog with the placement-scout agent, prepares the text, and tracks each placement's links, visits, conversions and return. Use when the user asks "where can I buy an article / press release", "is GlobeNewswire worth it", "which prnews.io sites to buy", "paid platforms", "link building budget", "press release for my site / client", or plans a budget for placements.
---

# Paid Placements

## Work label (testing period)

Start every reply produced by this skill with one line naming it (and the client or site in agency / own-site mode):
`▸ PARASITER · paid-placements · [site or client]`
If you called agents, add them after an arrow: `▸ PARASITER · paid-placements · Acme → placement-scout`. One line only, no other system talk.

## Next steps (end of every reply)

End each reply with one short line of 2–3 options, each with the phrase to say, e.g. `Next: "write the press release" (sales-review-writer brand mode) · "add these 3 placements to the November plan" (client-workspace) · "how did my placements pay off?" (work-log site-roi).` Offer only what the user's plan includes.

Part of PARASITER by Rumer (Affiliate Credo).

**A paid placement is an investment, not exposure.** For a site owner or an agency it buys three things, and each is checked before money is spent: a **page on a strong domain** that can rank for a query (often within days, when the free platforms are slow), a **link to the site** (dofollow where the outlet gives it — link building), and **credibility** (the brand on known media). Typical costs (checked 10/2026): a basic wire release from about $149 (EIN Presswire) to $400–1,200 (Newswire.com, ACCESS Newswire), top wires on request; sponsored articles on marketplaces from a few dollars to $70–175 for a solid site, famous outlets far more. **Wire links are usually nofollow** — wires buy a fast ranking page and credibility; dofollow links come from chosen sites on marketplaces (with the paid-link risk the owner decides on). The base in `references/placements.md` lists the offers; the agent checks what is current.

Who uses it: site owners and agencies first. Affiliates can use it too (paid news pages for reviews), with the publisher's rules on affiliate content checked first.

Reply in the working language; the press release or article itself in the content language.

## Step 1 — Goal and budget

Ask only what the brief (`clients/<slug>/client-brief.md`) doesn't answer:
1. **Goal** of this placement: a page that ranks for a query (which), a dofollow link to a page of the site (which), credibility / news coverage, referral traffic.
2. **Budget** per placement and per month.
3. **Niche and country** — many wires refuse gambling, crypto, CBD, adult, some health and finance claims.
4. **What there is to say** — real news for a press release (launch, new product, study, partnership, event, milestone) or a useful article topic for a sponsored post. No news → a sponsored expert article, not a fake "announcement".

## Step 2 — Shortlist from the base

From `references/placements.md`, filtered by goal, budget, niche and country. For each: what you buy, price (or "price on request" + how to ask), link policy stated and seen, distribution, restrictions, turnaround. Show free and paid options side by side when a free platform can reach the same goal ("Medium + LinkedIn article can rank for this query for $0 — the paid wire adds a dofollow link and news distribution for $X").

**Fresh check** (prices change, link policies change): send the shortlisted services, niche, country, budget, goal and target queries to the **`placement-scout` agent**. It checks the current packages, opens recent published pieces to see the real `rel` of links and whether they are indexed, and whether the outlet's pages rank in the niche. Show its table with the check date.

**Marketplaces** (prnews.io and similar): the agent shortlists 5–10 sites per budget from the public catalog — price, stated traffic, Google News, link rel, an indexed recent article. Pick by the goal: for ranking — outlets whose pages are in the top 10 for the niche's queries; for links — dofollow, indexed, topically close; for credibility — names the audience knows.

## Step 3 — Decide

One table, best first:

```
Placement plan · [site / client] · budget $N
| # | Where | What | Price | Link (stated / seen) | Ranks in niche? | Goal it serves | Why |
Total: $N · expected: [pages that can rank for …, N dofollow links to …] — assumptions, not promises
Skip: [option] — [why: nofollow and no ranking pages / refuses the niche / price for what it gives]
```

Never promise rankings, traffic or that a link stays dofollow; say what was seen and when.

## Step 4 — Prepare the piece

- **Press release:** real news only, `sales-review-writer` brand mode in press-release format: headline with the news, dateline, lead paragraph (who, what, when, why it matters), body with facts and one quote from a real person at the company (approved), boilerplate "About [Brand]", media contact. Links: as many as the wire allows, to the right pages, with UTM; anchors varied (brand, URL, natural phrase).
- **Sponsored article:** an expert article for the outlet's readers (`sales-review-writer` brand mode), the outlet's word count and link limits, the brand disclosed and the publisher's "sponsored / partner" label kept.
- Images: `post-illustrations` (cover in the brand's style, infographic of the facts).
- Check with `page-audit` (brand scale) before sending to the publisher.

## Step 5 — Order and log

The user orders and pays on the service's site — PARASITER never logs in, pays or contacts sales. Give the exact link to the order page or the quote form, and what to fill in. After publishing, log every resulting URL in the site's or client's journal:

```
python3 ../work-log/scripts/worklog.py add clients/acme/parasite-seo-progress.csv --event published --url <published URL> --platform globenewswire --sub-id gn-launch-1125 --link-target https://acme.com/crm --link-rel dofollow --anchor "Acme CRM" --cost 150 --query "acme crm"
```

Wire releases appear on many outlets: log the main release page with the cost, and only the syndicated copies that are indexed or rank (without cost). Monitoring and the check queue take over: is the page live, indexed, is the link still there and still dofollow.

## Step 6 — Did it pay off

After 30 and 60 days: `work-log site-roi --by page` (visits, conversions, revenue against cost) and `backlinks` (live dofollow links, spend per live dofollow link), positions of the placement's pages. Keep buying from outlets whose pages rank or whose links stay; drop those that brought nothing. The verdict goes into the base as a note for the user (`references/placements.md` is the author's; the user's own experience goes into their platform base with `platform-set --score … --note …`).

## Rules

- Real news for press releases; never invented announcements, awards, studies, quotes or numbers.
- Keep the publisher's "sponsored" / "press release" labels; never ask to hide that a placement is paid. Links are what the publisher gives.
- No link schemes: placements are bought for a page that serves readers and a relevant link, not as mass link buying; anchors varied; no buying links on hacked or abused sites. Say once, plainly, that Google's guidelines ask paid links to be `sponsored` / `nofollow` and that dofollow paid links are a risk the owner chooses.
- Prices only from the service or the agent's check, with the date; otherwise "price on request".
- Money is the user's decision: show the total and what it is expected to give, as assumptions.
- Never order, pay, log in or contact sales on the user's behalf.
