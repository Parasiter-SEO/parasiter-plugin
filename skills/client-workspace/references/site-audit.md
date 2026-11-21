# Site quick audit — 6 checks

A fast check of what matters for parasite SEO traffic: can Google read the site, and do our visitors land on a page that converts. Free: the agent opens pages and public tools. Pass / fail per check, with the evidence.

1. **Indexable**
   - `robots.txt` doesn't block key sections; `sitemap.xml` exists and lists the key pages.
   - Key pages have no `noindex`, have a self-canonical (or a correct canonical), load over HTTPS without redirect chains.
   - A `site:domain` search shows roughly the number of pages the site should have (big gaps → indexing problem; say so as a sign, not a verdict).
2. **Landing pages for traffic**
   - For every destination in the brief and every target query: the page exists, answers the query in the first screen, has one clear action (buy, book, form, sign up).
   - Mobile: readable without zoom, the action visible without long scrolling.
3. **Titles and descriptions** of those pages: contain the query or its meaning, unique, under ~60 / ~155 characters, not "Home".
4. **Speed** — PageSpeed Insights (pagespeed.web.dev) for the main landing page, mobile: performance score and LCP; link the report. Over 4 s LCP on mobile → critical: our visitors leave before the page opens.
5. **Tracking** — GA4 tag present (gtag / GTM in the page source); the key events the client counts (form, purchase, booking). Missing events → the report shows visits, not leads.
6. **Trust** — contacts and company details, About page, privacy policy, real reviews if shown, no broken pages in the main menu.

Report per check: pass / fail, the evidence (URL, what was seen), the fix in one line, and who fixes it (client's developer or the agency). Critical fails first: noindex on a landing page, a landing page that doesn't answer the query, no tracking.
