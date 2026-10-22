# Sales and traffic exports

Every affiliate network and most platforms let the user export a report. The user downloads it, uploads it to the conversation, and `import-sales` / `import-traffic` read it. Menus change often: describe what to look for, and if the user cannot find it, ask for a screenshot of their dashboard and point to the button on it.

## What to export (any network)

- **Report type**: transactions / conversions / actions / orders / commissions — one row per sale, not a daily total.
- **Columns to include** (turn on in the report settings if hidden): date, order or transaction ID, commission (payout, earnings), sale amount, **sub-ID / tracking ID**, status, product.
- **Date range**: from the day after the last import (the check queue prints it) to today. Overlaps are fine — duplicates are skipped by order ID.
- **Format**: CSV. Excel is fine too: save as CSV or convert with the xlsx skill.
- **Customer data**: names and emails are not needed. The import keeps only the journal's columns.

If a network only has daily totals by sub-ID, log them as `stats` rows per page (`add --event stats --url … --aff-clicks … --sales … --revenue …`).

## Where the sub-ID goes

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

| Source | What to export | Matching |
|---|---|---|
| Medium, Substack, LinkedIn articles, blog platforms | per-post stats: URL + views/reads for a period | page URL |
| Forums, Reddit, Quora | views shown on the post; usually a screenshot → log by hand | page URL |
| Search Console (own pages) | Performance → Pages, export: clicks, impressions | page URL (`--map views=Impressions`, clicks go in `clicks` via `add` if needed) |
| Network click / hop reports | clicks by sub-ID | sub-ID |

Always run with `--from` and `--to` set to the report's date range, so the same period is never counted twice.
