# How to … (step by step)

Each recipe: what the user says, what happens. Give the user only the recipe they asked for.

## Start for the first time
1. Say "what should I do today?" — the navigator asks language, your role (affiliate, SEO specialist / agency, blogger, course author / own product), then — for affiliates — niche and offers, country, time per day, tools, and the list of pages you already have (imported into your journal and platform base). Saves the profile.
2. It runs `goals`: baseline (how much you work, publish and earn now) → goals → reality check → weekly targets.
3. You get 2–5 tasks for today. "Start with #1?" — each task opens the right skill.

## Add my affiliate links
"Here are my affiliate links" + a list, a table or screenshots of your network's links page → they go into your links library (`parasite-seo-links.csv`), one row per product. Every article then uses your link without asking. "Which products have no pages yet?" → the list of products you sell but haven't written about.

## Add the pages I already have
"Here are my pages" + a file or a pasted list (text, CSV, Excel, any table with links) → `work-log` imports them: platform from each link, dates, offer and program if the table has them, duplicates skipped. Your platform base is built from them. Then "check them" → one bulk alive / index check of the whole list. Missing dates or offers: say them per batch ("these 40 are from September, KetoX on ClickBank").

## See my platforms
"My platforms" → your platform base: each platform with pages, alive, indexed, gone, sales, score and state. "Mark healthboards as dropped", "my account on X is …" updates it. `platform-analyzer` adds its score automatically.

## Mark my main pages, platforms and topics
"Medium and Quora are my main platforms", "these 10 pages are priority", "all keto pages are the topic *keto gummies review*" → priorities (★) and topics in your base. Priority pages are checked first; priority platforms and topics weigh more in the advice.

## Which pages are in the top
"Which of my pages are in the top 10?" → your pages with positions (from checks, a rank tracker or Search Console). "Show only priority pages" filters the list.

## Track positions of my pages
Search Console can't see pages on other people's platforms. Connect your own DataForSEO account (pay per query, cents a month for dozens of pages): create it at dataforseo.com, copy the API login and password, and set them as `DATAFORSEO_LOGIN` / `DATAFORSEO_PASSWORD`. Then "check my positions" → every page with a query or topic is checked in Google, positions and "new in top 10 / up / down / out" go into your journal. Weekly is enough. Using Ubersuggest or another tracker: export the rankings as CSV and upload it — "here are my positions". Trackers follow a whole domain, so on shared platforms (ResearchGate, Medium) make sure the ranking URL is your page; PARASITER skips rows where someone else's page of the same platform ranks. Or just say them ("cortisol on Pressbooks is #8").

## Start the day with my own plan
Say what you plan: "today I add articles on ResearchGate and Pressbooks — give me topics I don't have there; and forum posts on thermaltake on topics where my sites rank". The navigator keeps your plan and fills each part with topics from your base (missing there, strongest first, with the page to learn from). No plan in mind? Say "give me a plan" and it builds one.

## Publish one topic on all my platforms
Wrote a page? Say "roll this topic out" (or "where else should this go?"): you get your platforms that don't have the topic yet, ★ first, and a version for each in its own format — a book chapter, a forum thread, a podcast episode, a Gamma guide — new angle each time, same facts and your links.

## What to write and where
"What should I write next?", "which topics are missing on Medium?" → topic coverage: a table of your topics × platforms and the best gaps, e.g. *glp1 patch review → Medium: #7 and earning on the forum, Medium is your priority platform*. Pick one and it goes to content-type-selector and sales-review-writer (a new angle, never a copy).

## Pick a product or program
"Which program should I promote for [niche]?" → `affiliate-finder` compares programs (commission, cookie, payout, traffic rules). Then "is [product] worth it?" → `niche-analysis` if you have an SEO tool API or exports.

## Find where to publish
"Find platforms for [niche] in [language]" → `platform-finder`. Before the first post on a new one: "analyze [platform]" → `platform-analyzer` (score and verdict). With a key: "what's new?" → `platform-feed`.

## Write and publish a page (full cycle)
1. "What should I write about [product] for [query]?" → `content-type-selector` picks the type and topic.
2. "Write it for [platform]" → `sales-review-writer` (current prices via product-researcher).
3. "Make images" → `post-illustrations`.
4. "Audit it" → `page-audit`; fix until the score is good.
5. Publish it yourself. Keep a copy of the text.
6. Say "published: [URL], [platform], [program], pack [name]" → `work-log` records it; add a sub-ID to the affiliate link if the network supports it. The page is now in the check queue.

## Log a sale
Say "made a sale, $42, ClickBank" (add the page if you know it). → `work-log` records it. If the same sale later arrives in an export, it is counted once.

## Upload sales from an affiliate network
1. In the network, export the transactions / conversions report as CSV (date, order ID, commission, sub-ID, status) for the dates the check queue shows.
2. Upload it and say "import my ClickBank sales". → `work-log` finds the columns, skips duplicates, applies refunds and status changes, shows new sales and commission.
3. Excel works (it is converted). Only a screenshot or PDF: sales are read from it and logged one by one.
4. Weekly: if a program had no import or logged sale for 7 days, the navigator asks for the export.

## Upload traffic
Export per-post stats from the platform (Medium, LinkedIn, Search Console) or a click report from the network, upload, say "import traffic from Medium, 1–21 October". Screenshot: the numbers are logged by hand.

## See what I did and earned
- "What did I do today / yesterday / this week / in September?" → work report: work done, sales, traffic, pages and their status, what needs attention.
- "What earns?" / "which platforms work?" / "how is my keto pack doing?" → effectiveness table by page, platform, offer, program, campaign, content type or month.
- "Is the system paying off?" → by month since the start, against the baseline.

## Sale with no known page
Normal. It counts exactly in program, month and pack totals; page tables show an estimated share. Say "which pages probably sold?" for the estimate.

## Check my pages
"What needs checking?" → check queue (sales to upload, removed pages, not indexed after 14 days, checks and audits due, low audit scores). "Check them" → `platform-monitor` runs the checks and logs results. With a key, checks run on the server automatically.

## Weekly review
First session of the week, or "am I on track?" → `goals` compares plan and fact from the journal, replaces assumptions with your numbers, sets next week.

## Client report
"Make a report for my client for October" → `client-reports`, built from the journal; internal notes kept out unless you want them.

## Get news and notifications in Telegram (Pro, Insider)
Say "connect Telegram" → open the personal link → press Start. The bot sends invites to your plan's channel (and the Insider group). "What's new?" shows the same news in Claude.

## Change language
"Switch to Spanish" — plans and explanations change; pages keep the content language of your target country unless you change it too.

## Get help
"Help", "what can PARASITER do?", "is there a skill for …?" → this help.
