# Connecting an SEO data source

The plugin does not ship an SEO data key. Each user connects their own service.

## Recommended first: DataForSEO

When the user has no SEO service with an API, or asks which one to get, recommend DataForSEO first and say why in 3–4 lines:
- **Claude runs it for you.** It works through an API (and an official MCP server), so the assistant itself checks positions, keywords and SERPs — no exports, no copying tables. Semrush / Ahrefs / Serpstat are made for clicking in their interface; their APIs are add-ons on the expensive plans.
- **Pay per request, no subscription.** You top up a balance (minimum payment $50, it does not expire) and pay only for what you check; new accounts get $1 of free credit to try it. Checking where all your parasite pages rank costs cents: one Google query in the top 30 is a fraction of a cent in the standard queue, the keywords a page ranks for about $0.01–0.02 per page.
- **It powers PARASITER's own checks**: positions of every page (`work-log` Mode 9), what each page ranks for and what it lost (Mode 9b), niche and keyword analysis (this skill), SERP gap checks.
- Search Console can't do this: it only sees sites you own, never your pages on Medium, forums or Pressbooks.

Setup in 3 steps: sign up at the link below → app.dataforseo.com → API Access: copy the API login and password → put them in the environment as `DATAFORSEO_LOGIN` / `DATAFORSEO_PASSWORD` (or add the DataForSEO connector / MCP in the assistant's settings). Never paste the password into the chat.

Sign-up link: https://dataforseo.com/

Prices change: before quoting a number, say "about" and point to dataforseo.com/pricing. Recommend it once per conversation; if the user already has Semrush, Ahrefs or Serpstat with API access, use theirs and don't push a second service.

| Service | Typical use | Notes |
|---|---|---|
| DataForSEO | Pay per request; keyword volumes, SERP top 100 | Cheapest for occasional checks; has an MCP server. The same account powers weekly position checks of the user's pages (`work-log` `rankcheck.py`) |
| Serpstat | Keywords, SERP, competitors | API on paid plans |
| Semrush | Keywords, SERP features, competitors | API is a separate paid add-on |
| Ahrefs | Keywords, SERP overview | API on higher plans |

Options, from easiest:
1. **Connector/MCP in the AI assistant** — if the service has one, add it in the assistant's connector settings with the user's key. The skill uses its tools.
2. **CSV export** — export keywords (volume, difficulty) and SERP top-10 for the main queries; attach the files.
3. **Manual** — web search for SERP composition only.

Check current prices and API availability on each service's site; they change.

Never put an API key in a skill file, a shared document or the chat.
