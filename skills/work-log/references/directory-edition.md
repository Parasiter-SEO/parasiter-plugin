# Position checks in the directory edition

Read this when the session has **no `dataforseo_run` / `serpapi_run` tools** (PARASITER installed from the Claude directory). In that edition the plugin connects the official hosted MCP servers of DataForSEO and SerpApi with the user's own credentials from the plugin settings (`dataforseo_token`, `serpapi_key`). Their tools appear under the servers `parasiter-dataforseo` and `parasiter-serpapi`; tool names are set by DataForSEO and SerpApi (for example SerpApi `search`, DataForSEO's SERP organic live tool such as `serp_organic_live_advanced`, its Labs ranked-keywords tool). Use what the session lists.

The rules of Mode 9 stay the same: the user's own account, which pages, the cost or the number of searches before the run, and a yes before every paid call.

## Positions (Google or Bing) — both accounts

1. **Which queries.** Run `rankcheck.py <journal> --dry-run` with the usual filters (free, plain python3): it lists the queries and the pages they cover. For SerpApi add `--provider serpapi` to see the search count.
2. **Cost and yes.** Show the number of queries and the cost: DataForSEO live SERP ≈ $0.002 per query per 10 results; SerpApi 1 search per query per 10 results (free plan 250 a month). Wait for a yes.
3. **Run.** One call per query on the chosen server: Google (or Bing), the user's country and language, the same depth (default top 10, top 30 only when asked). Read the organic results and find each of the user's pages for that query (same URL, ignoring `http/https`, `www`, a trailing slash and tracking parameters). Note AI Overview / Discussions citations of the page when the result shows them.
4. **Into the journal.** Write a CSV in the user's folder, `ranks-YYYY-MM-DD.csv`, columns `url,query,position` (empty position = not in the checked depth), and import it: `worklog.py import-ranks ranks-YYYY-MM-DD.csv` (`--date` if not today). The journal, reports and the publication queue then work exactly as after a scripted check.
5. **Report** as in Mode 9: up, down, out of the top, cited in AI blocks — and what to do next.

Never put the credentials into arguments, files or the chat: the servers already have them from the plugin settings. Not set up → give the setup in 3 lines (`niche-analysis/references/seo-apis.md`; in this edition DataForSEO takes one **API token** = Base64 of `login:password`, see the option's description).

## Page keywords, AI-answer check, platform scans

Small runs work the same way through the DataForSEO server's own tools (Labs ranked keywords for a page URL, AI-answer / LLM tools, SERP for `"<product> review"`): show the cost, get a yes, call one item at a time, read the result, log what matters (`worklog.py tag`, `platform-set`). For **big batch runs** (hundreds of queries, task queue with `--collect`, the full `platformscan` with live checks and sign-up links) tell the user in one line that the full edition from GitHub (https://github.com/Parasiter-SEO/parasiter-plugin) runs them as one script, and keep going in this edition if they prefer.
