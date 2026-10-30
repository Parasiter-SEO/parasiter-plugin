# Indexers for parasite pages (checked 2026-10-30)

Prices and rates change. Vendor home pages could not be opened on the check date, so figures come from the vendor's own docs or plugin pages where noted, otherwise from dated reviews and tests (sources at the bottom). Before quoting a price, say "about" and ask the user to confirm it on the vendor's site. Re-check this file when it is older than 3 months.

## What to expect

- **No service can force Google to index a page.** None says how it gets Googlebot to the page. A crawl is not indexing: in one test Google's own tools sent Googlebot to 200 thin pages and none got indexed [3].
- **Independent tests disagree a lot.** The same tools scored 85–99% in one 2026 test [1], 55–78% in another [2], 27–46% in a 2025 analysis [4]. Plan on **roughly 55–90% for decent pages**, not the 90%+ vendors advertise.
- **Refunds are mostly credits, not cash**, after a fixed window. Wait for that window before resending.
- **Bad pages stay out whatever you pay** (thin, duplicate, noindex). Fix the page first.

## Rumer's picks

1. **Rapid URL Indexer** — default pick. Cheap (from ~$0.05 per URL), credits back automatically for URLs not indexed in 14 days, top-two results in both 2026 tests, WordPress plugin, REST API, Make / Zapier. API documentation is not public: the user sends by hand (dashboard / plugin) unless they give Claude the API docs from their account.
2. **SpeedyIndex** — best for automation. You pay only for indexed URLs (tokens back on day 7), Telegram bot, a documented API Claude can run (`index-runner`), its own index checker. Weaker results in one test (55%).
3. **Indexceptional** — highest rates in both 2026 tests (99.4% / 77.5%), but ~$0.25 per credit. For ★ and earning pages, or as the second try when the first service failed.

## Comparison

| Service | Price (about) | Unindexed URLs | Tests: Floate 07/2026 [1] · Onfolio 08–10/2026 [2] | API | Other ways to send | Index checker | Status |
|---|---|---|---|---|---|---|---|
| **Rapid URL Indexer** | from $0.05 / URL (1 credit); Apex mode 3 credits; Bing +1 credit, not refunded [10] | credits back after 14 days [10] | 99% · 75% | REST, 100 req/min (docs not public) [8]; MCP server [11] | dashboard, WordPress plugin [10], Make / Zapier | likely (not confirmed) | alive |
| **SpeedyIndex** | 100 tokens per indexed URL; ~$0.03–0.10 per URL by volume [5][7][8] | pay per indexed, tokens back on day 7 [5][6] | 89.9% · 55% | **documented** — `en.speedyindex.com/api.html`, up to 10,000 URLs per task, drip-feed 2–30 days [5] | Telegram @SpeedyIndexBot, Chrome extension, WP via BotSubmit [9] | yes (Google, Yandex, Bing) [5] | alive |
| **Indexceptional** | from $0.25 / credit, credits don't expire [1][12] | refunds mentioned anecdotally, not published [13] | 99.4% · 77.5% | not published | dashboard, Chrome extension; shows the crawler IPs that visited each URL [2][12] | dashboard tracking | alive |
| **IndexMeNow** | ~€0.47–0.98 / URL by pack (€59 / 60 credits) [2][7] | credit back after 10 days [2][7] | 89.1% · 72.5% | yes, free [7] | dashboard | yes, free [7] | alive |
| **Omega Indexer** | ~$0.04–0.15 / URL; plans from ~$19 / 190 credits; sources disagree [2][7][8] | credits back (terms vary by source) [7][8] | 85.3% · 65% | yes [2][8]; MCP server | dashboard, drip-feed up to 30 days [7] | not published | alive |
| **GIGA Indexer** | ~$0.28–0.48 / link (60 credits $15) [2][14] | refund window 9 days [2] | 81.2% · 67.5% | not published | dashboard | not published | alive |
| **IndexChex** (new) | packs from ~$21.99 [2] | not published | — · 90% (one test) | yes [2] | dashboard | yes [2] | new, little data |
| Links Indexer | freemium, prices not published | — | 11.2% · 22.5% | — | — | — | alive, weak results: don't recommend |

**Unverified or dead (don't recommend):** OneHourIndexing, Indexification, Elite Link Indexer, IndexJump (no 2026 evidence or no updates) [15][16][17][18]; Sinbyte (plugin abandoned 5 years) [19]; Colinkri, TheIndexer (no 2025–26 trace). Other 2026 names (Speed Indexing, IndexBolt, IndexPro, UltraIndexer) appear only on vendor or affiliate pages.

## Where the user sends pages by hand

- Rapid URL Indexer: dashboard → new project → paste URLs (one per line); or the WordPress plugin for their own site.
- SpeedyIndex: Telegram @SpeedyIndexBot → send the list as a message or a .txt file; or the dashboard.
- Indexceptional, IndexMeNow, Omega, GIGA: dashboard → new task / campaign → paste URLs.

Always give the clean list (one URL per line, no tracking parameters unless the page needs them), the count and the price.

## API keys (environment variables)

| Service | Variable | Claude can send by API |
|---|---|---|
| SpeedyIndex | `SPEEDYINDEX_API_KEY` | yes — `index-runner` |
| Rapid URL Indexer | `RAPIDURLINDEXER_API_KEY` | only if the user provides the API docs from their account, or connects its MCP server |
| IndexMeNow | `INDEXMENOW_API_KEY` | only with the docs from their account |
| Omega Indexer | `OMEGA_INDEXER_API_KEY` | only with the docs from their account, or its MCP server |

Never invent an endpoint. No docs → by hand.

## Sources
[1] charlesfloate.com/best-backlink-indexing-tools · [2] onfolio.com/reviewed/best-backlink-indexer · [3] searchlogistics.com/seo/tools/backlink-indexers-test · [4] indexcheckr.com/resources/success-rate-analysis-of-indexing-tools (sells index checking) · [5] en.speedyindex.com/api.html · [6] sostav.ru/blogs/282180/96178 · [7] junia.ai/blog/website-indexing-tools · [8] speedindexing.com/en/alternatives/rapid-url-indexer-alternative (a competitor) · [9] wordpress.org/plugins/botsubmit · [10] wordpress.org/plugins/rapidurlindexer-wp · [11] glama.ai/mcp/servers/rollounden/rapid-indexer-mcp · [12] earnperinstall.com/best-backlink-indexing-tools · [13] fatrank.transistor.fm/504/transcript · [14] indexpro.app/blog/top-10-link-indexing-services-compared-2025-review (sells indexing) · [15] bloggersneed.com/best-website-indexing-services · [16] indiehackers.com (anonymous 2026 test) · [17] fatrank.com/elitelinkindexer-review · [18] plugins.wpmayor.com/plugin/indexjump-submitter · [19] wordpress.org/plugins/sinbyte-indexer

Test notes: Floate paid for his credits, no affiliate links, sample size per tool not stated. Onfolio: 40 URLs per tool, the author is linked to the Indexsy brand. IndexCheckr's per-tool totals don't add up.
