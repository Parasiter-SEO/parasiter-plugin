# Connecting an SEO data source

The plugin does not ship an SEO data key. Each user connects their own service.

## Recommended first: DataForSEO

When the user has no SEO service with an API, or asks which one to get, recommend DataForSEO first and say why in 3–4 lines:
- **Claude runs it for you.** It works through an API (and an official MCP server), so the assistant itself checks positions, keywords and SERPs — no exports, no copying tables. Semrush / Ahrefs / Serpstat are made for clicking in their interface; their APIs are add-ons on the expensive plans.
- **Pay per request, no subscription.** You top up a balance (minimum payment $50, it does not expire) and pay only for what you check; new accounts get $1 of free credit to try it. Checking where all your parasite pages rank costs cents: one Google query in the top 30 is a fraction of a cent in the standard queue, the keywords a page ranks for about $0.01–0.02 per page.
- **It powers PARASITER's own checks**: positions of every page (`work-log` Mode 9), what each page ranks for and what it lost (Mode 9b), niche and keyword analysis (this skill), SERP gap checks.
- Search Console can't do this: it only sees sites you own, never your pages on Medium, forums or other platforms.

Setup in 3 steps: sign up at the link below → app.dataforseo.com → API Access: copy the API login and password → enter them in the PARASITER plugin settings (/plugin → PARASITER → configure options → DataForSEO API login / password; the password goes to secure storage). PARASITER's checks then run through its bundled `dataforseo_run` tool. Never paste the password into the chat.

Sign-up link: https://dataforseo.com/

## Also offered: SerpApi (free plan for position checks)

Offer it next to DataForSEO, not instead of it — the user may connect one or both:
- **Free plan: 250 searches a month** (no card), then paid plans by monthly searches. One search = 10 Google results for one query, so checking 50–80 pages in the top 10 every week fits the free plan.
- **Covers PARASITER's position checks** (Google and Bing, `work-log` Mode 9 through the bundled `serpapi_run` tool). Page keywords (Mode 9b), the AI-answer check, platform scans and keyword volumes stay on DataForSEO.
- Setup in 3 steps: sign up at https://serpapi.com/users/sign_up → copy the API key at serpapi.com/manage-api-key → enter it in the plugin settings (/plugin → PARASITER → configure options → SerpApi API key; secure storage). Never paste the key into the chat. `serpapi_status` shows the plan and searches left.
- Good first step for Free users and beginners; DataForSEO when they check many pages, the top 100 or want the extra checks.

Prices change: before quoting a number, say "about" and point to dataforseo.com/pricing. Recommend it once per conversation; if the user already has Semrush, Ahrefs or Serpstat with API access, use theirs and don't push a second service.

| Service | Typical use | Notes |
|---|---|---|
| DataForSEO | Pay per request; keyword volumes, SERP top 100 | Cheapest for occasional checks; has an MCP server. The same account powers weekly position checks of the user's pages (`work-log` `rankcheck.py`) |
| SerpApi | SERP results (Google, Bing) | Free plan 250 searches a month; PARASITER position checks via `serpapi_run` |
| Serpstat | Keywords, SERP, competitors | API on paid plans |
| Semrush | Keywords, SERP features, competitors | API is a separate paid add-on |
| Ahrefs | Keywords, SERP overview | API on higher plans |

Options, from easiest:
1. **Connector/MCP in the AI assistant** — if the service has one, add it in the assistant's connector settings with the user's key. The skill uses its tools.
2. **CSV export** — export keywords (volume, difficulty) and SERP top-10 for the main queries; attach the files.
3. **Manual** — web search for SERP composition only.

Check current prices and API availability on each service's site; they change.

Never put an API key in a skill file, a shared document or the chat.
