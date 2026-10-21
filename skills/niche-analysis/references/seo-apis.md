# Connecting an SEO data source

The plugin does not ship an SEO data key. Each user connects their own service.

| Service | Typical use | Notes |
|---|---|---|
| DataForSEO | Pay per request; keyword volumes, SERP top 10 | Cheapest for occasional checks; has an MCP server |
| Serpstat | Keywords, SERP, competitors | API on paid plans |
| Semrush | Keywords, SERP features, competitors | API is a separate paid add-on |
| Ahrefs | Keywords, SERP overview | API on higher plans |

Options, from easiest:
1. **Connector/MCP in the AI assistant** — if the service has one, add it in the assistant's connector settings with the user's key. The skill uses its tools.
2. **CSV export** — export keywords (volume, difficulty) and SERP top-10 for the main queries; attach the files.
3. **Manual** — web search for SERP composition only.

Check current prices and API availability on each service's site; they change.

Never put an API key in a skill file, a shared document or the chat.
