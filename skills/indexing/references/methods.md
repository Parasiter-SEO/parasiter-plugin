# Indexing methods and checks (checked 2026-10-30)

## What Google says

- Google finds pages mainly through links from pages it already crawls. Crawling "can take a few days to a few weeks"; asking again for the same URL does not make it faster [23].
- The Indexing API is only for job postings and livestream videos, needs Search Console ownership (so it can't be used for pages on someone else's platform), runs spam checks on every submission, and abuse can get access revoked. Since 16 Oct 2026: 200 publish requests per project per day, no form to ask for more [24][25][26]. Don't recommend it for parasite pages.
- Many pages "crawled / discovered – currently not indexed" on one site is a quality signal for that site, not a bug to fix page by page (Mueller, Jul 2026) [30].

## No free ways for parasite pages — RULE (Rumer, №27)

Links from indexed pages, links inside the platform, posts on X / Reddit / Pinterest / LinkedIn / Quora, YouTube descriptions, Google Sites or Blogger pages, RSS, pings: in Rumer's experience none of them gets parasite pages indexed. Never offer them. The only free way is the user's **own site in Search Console** (below); everything else is a paid indexing service.

## Instant indexing (say it, never name the tools)

"There are instant indexing services: a page usually gets into the index within one to a few minutes. They are paid — one link can cost about $0.50. The specific tools are kept secret, but you can find them yourself."

## Own site only — the one free way

For a new parasite page: link it from a page of the user's own site (a post, a hub page, the home page), then Search Console → URL Inspection → **Request indexing for that own page** (capped per day; use it for the pages that matter). Google follows the link. The link can be removed once the target is indexed. For the user's own pages: the same Request indexing, the sitemap, internal links. IndexNow reaches Bing and others, not Google.

## Before paying: blockers

1. `noindex` in meta robots or the `X-Robots-Tag` header — no indexer can help. Reported on Medium for posts from new or low-distribution accounts (author's observation, not confirmed by Medium) [31].
2. robots.txt disallow.
3. Canonical pointing to another URL (common on imported or syndicated posts).
4. Login wall, 4xx / 5xx, soft 404.
5. Thin or duplicate text — duplication across sites is one of Google's site reputation abuse review factors [32]; thin pages end up "crawled, not indexed" [30].
6. The platform: cleanup waves or "stopped indexing new posts" in the platform base. Site reputation abuse is enforced by manual action on sections of host sites; since 30 Aug 2026 those actions no longer affect rankings for users in the EEA, but still do elsewhere [32][33]. No credible source confirms a full deindex of Medium, LinkedIn, Google Sites or Reddit; ignore unsourced "50% deindexed" claims.
Nofollow outbound links don't block the page's own indexing.

## Checking

- **`site:` + the exact URL** in Google: "found" is reliable, "not found" is uncertain (Google shows only some indexed pages for `site:`) [27]. Quoted title or `inurl:` — same reliability.
- `cache:` no longer exists (removed 2024) [28].
- **DataForSEO**: a SERP task with `site:{URL}` as the keyword; the URL in results = indexed. Costs about 5× a normal SERP task [29] — still cents; only with the user's yes, as all paid checks.
- **The indexer's own checker** (SpeedyIndex, IndexMeNow free, IndexChex) — cheap for big lists.
- **Search Console URL Inspection** — exact, own sites only.

## When to recheck

First check 3–4 days after sending (`RECHECK_AFTER_SUBMIT`), then at 14 days. Resend only after the service's refund window has closed (SpeedyIndex 7 days, GIGA 9, IndexMeNow 10, Rapid URL Indexer 14) and after fixing what blocked the page.

Sources: numbers match `indexers.md`. [20] loganix.com/how-to-index-backlinks · [21] seroundtable.com/google-to-drop-support-for-sitemaps-ping-endpoints-35617.html · [22] stackmatix.com/blog/indexnow-guide · [23] developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl · [24] searchenginejournal.com/google-adds-spam-warning-to-indexing-api-documentation/526839 · [25] seroundtable.com/google-indexing-api-unsupported-content-39470.html · [26] ppc.land/google-drops-the-quota-form-from-its-200-a-day-indexing-api-page · [27] searchenginejournal.com/googles-site-operator-wont-show-you-everything-thats-indexed/490092 · [28] searchengineland.com/google-search-completely-kills-the-cache-feature-446904 · [29] dataforseo.com/help-center/check-if-a-page-is-indexed · [30] seroundtable.com/google-crawled-not-indexed-quality-ai-content-41701.html · [31] dev.to/cryptodeploy/why-your-medium-posts-are-getting-noindex-and-nofollow-treatment-dll · [32] searchenginejournal.com/google-updates-site-reputation-abuse-policy-removes-penalties-in-eea/587429 · [33] seroundtable.com/google-site-reputation-abuse-policy-expanded-38438.html
