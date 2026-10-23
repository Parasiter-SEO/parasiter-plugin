---
name: platform-finder
description: Find platforms where a parasite SEO page can be published and rank — forums, communities, Q&A, article and profile platforms, document hosts, site builders, event and fundraising pages — filtered by niche, language, link rules, indexing speed and moderation. Use when the user asks where to publish, wants new platforms, forums or communities for a niche, or a list of platforms that work now.
---

# Platform Finder

Part of PARASITER by Rumer (Affiliate Credo).

Platforms live days to months: they get spammed, cleaned up, noindexed or close registration. A list is only worth something if it is **fresh and checked**. This skill combines the author's database (server, Pro) with a live search the user can run with you.

Reply in the user's language.

## Step 1 — Filters

Ask only what is missing:
- Niche / offer and target query (or the keyword list from niche-analysis).
- Language and country.
- Platform types wanted: forum/community, Q&A, article/blog, profile, document/PDF/flipbook, site builder, events/fundraising, audio/video, paid press release.
- Must-haves: live links required? dofollow needed or nofollow is fine? free or paid OK? max moderation?
- Platforms to exclude (already used, already banned).

## Step 2 — Database first (Pro)

If the server tool `platforms_search` is available, call it with the filters. It returns platforms with status, last check date, indexing speed, link type, moderation, notes and the plan delay (Pro gets new platforms ~7 days after they are found, Insider the same day). Show them as a table and keep the server's notes as written — do not strip or rewrite markers in the response.

If the server is not connected, say once: "Fresh checked platforms come with a Pro key. Meanwhile we can search live." and go to Step 3.

## Step 3 — Live search

For a broad search, delegate to the `platform-scout` agent. Otherwise use web search yourself; without web search, give the user the exact queries to run in Google (target country, incognito, mobile and desktop).

1. **SERP-first (best signal):** search the target queries with buyer modifiers ("[product] reviews", "[product] vs", "[product] complaints", "best [category]"). Note every non-brand domain in the top 20, the "Discussions and forums" block, videos, PDFs. A platform already ranking for your niche is the strongest lead.
2. **Footprints:** find forgotten but still indexed forums and communities with the patterns in `references/footprints.md` + niche words. AI and footprints make old XenForo/ProBoards/phpBB boards easy to find — so do competitors; speed matters.
3. **Competitor trail:** open competitors' parasite pages for the same product; the domains they use are candidates.

## Step 4 — Quick filter

For each candidate check fast (details in platform-analyzer):
- Can a new user register and post? (old-accounts-only = skip for users without aged accounts)
- Is a fresh post indexed? (`site:domain` + recent posts; noindex meta/header)
- Are links allowed and live?
- Any sign of mass cleanup (empty threads, "removed", login wall)?

Drop dead ones. Mark uncertain ones "test".

## Step 5 — Output

```
Platforms for [niche] · [language] · checked [date]
| Platform | Type | Register | Indexing | Links | Moderation | Status | Next step |
```
Then: top 3 to start with and why (one line each), and "run platform-analyzer on #1 before posting".

## Rules

- Only platforms where the user can legitimately create an account and post. Never suggest hacked sites, hidden or unprotected upload forms on organisations' sites, injection into someone else's files, or impersonating an organisation — these are not platforms, they are abuse, and they burn domains and offers.
- Spread across platforms; never rely on one.
- Every list is a snapshot: write the check date on it.
- Reference: the author's archive of domains that ranked in 2025–2026 lives on the server (history, not live status).
