# Indexing methods and checks (checked 2026-10-30)

## What Google says

- Google finds pages mainly through links from pages it already crawls. Crawling "can take a few days to a few weeks"; asking again for the same URL does not make it faster [23].
- The Indexing API is only for job postings and livestream videos, needs Search Console ownership (so it can't be used for pages on someone else's platform), runs spam checks on every submission, and abuse can get access revoked. Since 16 Oct 2026: 200 publish requests per project per day, no form to ask for more [24][25][26]. Don't recommend it for parasite pages.
- Many pages "crawled / discovered – currently not indexed" on one site is a quality signal for that site, not a bug to fix page by page (Mueller, Jul 2026) [30].

## Free ways for pages the user doesn't own

| Way | Google | Notes |
|---|---|---|
| **Link from a page Google already indexed** (the user's indexed parasite pages, profile / hub, own site) | yes | The main way Google finds URLs. Strongest free option. A link from the user's own site can be added, the host page re-requested in Search Console, and the link removed once the target is indexed [20]. |
| **Links inside the platform** (older indexed posts there, profile, collections, tags, related posts) | yes | Same logic; costs nothing on the platform you already use. |
| **X / Twitter post** with the URL | maybe | Practitioners rate it highly, no test data [20]. |
| Reddit / community answer (where self-links are allowed), Pinterest pin, LinkedIn, Quora, YouTube description | discovery only | Mostly nofollow; helps Google find the URL, not proven to get it indexed [20]. |
| Google Sites / Blogger page linking to it | if that page itself gets indexed | No test evidence it is faster [20]. |
| RSS feeds and aggregators | weak, unproven | No 2025–26 evidence. |
| Ping services | **no** for Google | Google shut its sitemap ping at the end of 2023 [21]. Don't recommend. |
| IndexNow | **no** for Google | Bing, Yandex, Naver, Seznam only, and only for domains where you can put the key file [22]. |

## Own site only

Search Console URL Inspection → Request indexing (capped per day; use for the few pages that matter), the sitemap (for many URLs), IndexNow for Bing and others, internal links from the home page or a hub page.

## Before paying: blockers

1. `noindex` in meta robots or the `X-Robots-Tag` header — no indexer can help. Reported on Medium for posts from new or low-distribution accounts (author's observation, not confirmed by Medium) [31].
2. robots.txt disallow.
3. Canonical pointing to another URL (common on imported or syndicated posts).
4. Login wall, 4xx / 5xx, soft 404.
5. Thin or duplicate text — duplication across sites is one of Google's site reputation abuse review factors [32]; thin pages end up "crawled, not indexed" [30].
6. The platform: cleanup waves or "stopped indexing new posts" in the platform base. Site reputation abuse is enforced by manual action on sections of host sites; since 30 Aug 2026 those actions no longer affect rankings for users in the EEA, but still do elsewhere [32][33]. No credible source confirms a full deindex of Medium, LinkedIn, Google Sites, Reddit or Pressbooks; ignore unsourced "50% deindexed" claims.
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
