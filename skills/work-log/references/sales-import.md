# Sales and traffic exports

Every affiliate network and most platforms let the user export a report. The user downloads it, uploads it to the conversation, and `import-sales` / `import-traffic` read it. Menus change often: describe what to look for, and if the user cannot find it, ask for a screenshot of their dashboard and point to the button on it.

## What to export (any network)

- **Report type**: transactions / conversions / actions / orders / commissions — one row per sale, not a daily total.
- **Columns to include** (turn on in the report settings if hidden): date, order or transaction ID, commission (payout, earnings), sale amount, **sub-ID / tracking ID**, status, product.
- **Date range**: from the day after the last import (the check queue prints it) to today. Overlaps are fine — duplicates are skipped by order ID.
- **Format**: CSV. Excel is fine too: save as CSV or convert with the xlsx skill.
- **Customer data**: names and emails are not needed. The import keeps only the journal's columns.

## Where the export is in each network

Give the user only the steps for the programs they named. Menus move: these are the usual places, not exact clicks. If the button is not there, ask for a screenshot of their dashboard and point to it. If the network is not listed, use the generic path at the end.

| Network / platform | Sales export (one row per sale) | Click export (for traffic) |
|---|---|---|
| ClickBank | Reporting → Transactions (or Analytics → Transactions) → date range → Download / CSV | Reporting → Analytics, group by TID or by "Hop" → export |
| Digistore24 | Reports → Transactions → filter by date → Export (CSV or Excel) | Reports → Clicks / Affiliate statistics → export |
| BuyGoods, MaxWeb, other nutra networks | Reports → Conversions / Sales → date range → Export CSV | Reports → Clicks → group by sub-ID or by referrer → export |
| Everflow networks (FanFuel and many direct nutra programs) | Reporting → Conversions → date range → add columns Sub1–Sub5 and Referer → Export CSV | Reporting → Clicks (or Variance) → group by Sub1 or Referer → Export |
| Post Affiliate Pro (many direct merchants) | Commissions (Transactions) → date filter → Export to CSV; turn on columns Data1–Data5, Channel, Referrer URL if offered | Reports → Raw clicks / Traffic → group by Referrer → Export |
| Impact | Reports → Action Listing (or "Performance by Action") → date range → Download CSV | Reports → Clicks / Performance by Sub ID → Download |
| CJ | Reports → Commission Detail (or Transaction Detail) → date range → Download CSV | Reports → Performance by Link / by SID → Download |
| ShareASale | Reports → Transaction Detail → date range → Download | Reports → Traffic / Click Report by Afftrack → Download |
| Awin | Reports → Transactions → date range → Export CSV | Reports → Performance over time / Clicks by Clickref → Export |
| Rakuten | Reports → Signature Orders Report (includes `u1`) → Download | Reports → Signature Activity by Member ID → Download |
| PartnerStack, Tapfiliate, Rewardful, FirstPromoter (SaaS) | Rewards / Commissions / Conversions → Export CSV | Usually clicks per link in the dashboard → export or screenshot |
| Amazon Associates | Reports → Download Reports → Orders and Earnings for the date range (CSV), one file per tracking ID set | Same report: clicks per tracking ID |
| Any other network | Look for "Reports", "Statistics" or "Commissions" → the report with one line per sale → date range → Export / Download / CSV | The click or traffic report, grouped by sub-ID or referrer |

Ask for both files when the network has them: sales tell what earned, clicks tell which platform sent the buyers. A click report grouped by **referrer** (Post Affiliate Pro, Everflow `referer`) gives clicks per platform even with no sub-ID — the best substitute for sub-IDs.

If a network only has daily totals by sub-ID, log them as `stats` rows per page (`add --event stats --url … --aff-clicks … --sales … --revenue …`).

## Where the sub-ID goes (when the network supports it)

A sub-ID is optional. Without it every sale still counts by program and campaign, and per-page numbers are estimated. Many programs, merchant-direct offers and coupon sales never pass one.

The parameter name differs by network. Common ones (confirm in the network's own help, they change):

| Network | Sub-ID parameter |
|---|---|
| ClickBank | `tid` in the hoplink |
| Impact | `subId1` (also `subId2`, `subId3`, `sharedid`) |
| CJ | `sid` |
| ShareASale | `afftrack` |
| Awin | `clickref` |
| Rakuten | `u1` |
| Digistore24 | campaign key in the promo link |
| Partner programs on PartnerStack, Tapfiliate, Post Affiliate Pro, Everflow, HasOffers/Tune | usually `sub1` / `aff_sub` / `sub_id` |
| Amazon Associates | no sub-ID: create a separate tracking ID per page or per platform and use it as the `sub_id` |

If the user's link already contains a parameter, keep it and add the sub-ID. Never change the affiliate ID itself.

## Column names the import recognises

| Field | Header names (case and spaces ignored) |
|---|---|
| date | Date, Transaction Date, Transaction Time, Sale Date, Order Date, Action Date, Conversion Date, Event Date, Created At |
| order_id | Order ID, Transaction ID, Receipt, Action ID, Order Number, Conversion ID, Commission ID |
| commission | Commission, Your Commission, Publisher Commission, Payout, Earnings, Your Earnings, Amount Earned, Action Earnings, Reward |
| amount | Sale Amount, Order Amount, Order Value, Amount, Revenue, Sale Value, Item Price |
| sub_id | SubId, SubId1, SID, TID, Tracking ID, Shared ID, aff_sub, Click Ref, Custom ID, afftrack, Campaign Key, Tag, Label |
| status | Status, Action Status, Commission Status, Transaction Type, Txn Type, State |
| offer | Product, Product Name, Offer, Item, Brand, Advertiser, Merchant, Campaign |
| currency | Currency, Currency Code |

Status words: approved / paid / locked / sale / completed → **approved**; pending / open / new / extended → **pending**; reversed / refund / declined / rejected / chargeback / void → **reversed**.

Anything else: `--map field="Header in the file"` (repeatable). Dates are detected as ISO, US (MM/DD/YYYY) or EU (DD.MM.YYYY, DD/MM/YYYY when a day is over 12); force with `--date-format "%d/%m/%Y"`.

## Traffic exports

Anything the user knows about traffic helps: a file, a screenshot, or a number per page or platform. Three levels, all accepted:
- **per page** (page URL or sub-ID) — best, credits the page;
- **per platform** (referrer domain, GA4 source, utm_source, or a whole-platform total with `--platform`) — credits the platform when the page is unknown;
- **no referrer / direct** — counted in totals, tied to nothing.

| Source | What to export | Matching |
|---|---|---|
| Affiliate network click report by referrer (Post Affiliate Pro, Everflow) | clicks grouped by referrer URL or domain for the period | page URL if the referrer is the page, else platform domain |
| Network click / hop reports by sub-ID | clicks by sub-ID | sub-ID |
| Google Analytics 4 — for links that go through the user's own site or landing page, or UTM-tagged links to it | Reports → Acquisition → Traffic acquisition; primary dimension **Session source / medium** (or Session campaign for utm_campaign); add **Landing page** as a secondary dimension; set the dates; Share icon → Download file → CSV. Or Explore → Free form with Session source, Landing page, Sessions | landing page URL, else source → platform |
| Search Console (own pages) | Performance → Pages, export: clicks, impressions | page URL (`--map views=Impressions`) |
| Link shorteners and redirect services (Bitly, geni.us, own redirect domain) | clicks per short link for the period → export or screenshot | log each link's clicks on its page (`add --event traffic --url <page> --aff-clicks N`) |
| Gamma | open the gamma → Share / ⋯ menu → **View analytics**: views and viewers per gamma (paid plan); no CSV → screenshot | page URL; or `--platform gamma` for the account total |
| Medium, Substack, LinkedIn articles, Pressbooks, blog platforms | per-post stats: URL + views/reads for a period (Medium: Stats page; LinkedIn: post analytics) — export or screenshot | page URL |
| ResearchGate, Academia, document hosts (Scribd, Issuu, SlideShare) | Stats / reads per item — usually a screenshot | page URL |
| Podcasts (Audioboom, Spotify for Creators, Firstory) | plays / listens per episode for the period → export or screenshot | page URL |
| YouTube | Studio → Analytics → Advanced mode → content × views → Export (CSV) | video URL |
| Forums, Reddit, Quora | views shown on the post; usually a screenshot → log by hand | page URL |

From a screenshot: read the numbers into a small table first (page or platform, views or clicks, period), show it to the user, then import or `add` it.

Always run with `--from` and `--to` set to the report's date range, so the same period is never counted twice.
