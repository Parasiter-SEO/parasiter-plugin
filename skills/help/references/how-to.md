# How to … (step by step)

Each recipe: what the user says, what happens. Give the user only the recipe they asked for.

## Start for the first time
1. Say "what should I do today?" — the navigator asks the language and your role, then a few short questions: niche and offers, affiliate programs, country and page language, hours, tools (no SEO API yet → it recommends DataForSEO).
2. Then it asks you to upload what you have: live pages (any list of links), affiliate links, sales reports from each program (with the export steps for the networks you named) and any traffic data (network clicks by referrer, Google Analytics, Gamma or Medium stats…). Nothing is required; the more real data, the more real the plan. Just starting? Uploads are skipped.
3. `goals` shows your starting point from these numbers, asks your hours, pace and income in your words, then sets goals with Rumer's rule (10 platforms / 100 live posts) as the minimum.
4. You get 2–5 tasks for today. "Start with #1?" — each task opens the right skill.

## Upload my traffic
"Here is my traffic report" + a file or screenshot: network click reports (by referrer or sub-ID), Google Analytics (source / medium, UTM, landing pages), Search Console, Gamma analytics, Medium / LinkedIn stats, podcast plays, shortener clicks. Traffic is credited to the page when the page is known, to the platform when only the referring site is known. "How do I export clicks from [network]?" → the steps for that network.

## Add my affiliate links
"Here are my affiliate links" + a list, a table or screenshots of your network's links page → they go into your links library (`parasite-seo-links.csv`), one row per product. Every article then uses your link without asking. "Which products have no pages yet?" → the list of products you sell but haven't written about.

## Add the pages I already have
"Here are my pages" + a file or a pasted list (text, CSV, Excel, any table with links) → `work-log` imports them: platform from each link, dates, offer and program if the table has them, duplicates skipped. Your platform base is built from them. Dates are not needed. Then the free check (page alive, noindex, link) runs on all of them; index and positions are paid on your SEO account, so you choose which pages — ★, earning, the newest pack — after seeing the cost. Missing offers: say them per batch ("these 40 are KetoX on ClickBank").

## See my platforms
"My platforms" → your platform base: each platform with pages, alive, indexed, gone, sales, score and state. "Mark healthboards as dropped", "my account on X is …" updates it. `platform-analyzer` adds its score automatically.

## Mark my main pages, platforms and topics
"Medium and Quora are my main platforms", "these 10 pages are priority", "all keto pages are the topic *keto gummies review*" → priorities (★) and topics in your base. Priority pages are checked first; priority platforms and topics weigh more in the advice.

## Which pages are in the top
"Which of my pages are in the top 10?" → your pages with positions (from checks, a rank tracker or Search Console). "Show only priority pages" filters the list.

## Track positions of my pages
Search Console can't see pages on other people's platforms. Connect your own DataForSEO account (pay per query, cents a month for dozens of pages): create it at dataforseo.com, copy the API login and password, and set them as `DATAFORSEO_LOGIN` / `DATAFORSEO_PASSWORD`. Then "check my positions" → you choose which pages (★, earning, new, all) and see the cost; after your yes they are checked in Google (top 10–30), positions and "new in top 10 / up / down / out" go into your journal. Weekly is enough; "check ★ pages every Monday" sets a scheduled check with a Telegram warning before each run. Using Ubersuggest or another tracker: export the rankings as CSV and upload it — "here are my positions". Trackers follow a whole domain, so on shared platforms (ResearchGate, Medium) make sure the ranking URL is your page; PARASITER skips rows where someone else's page of the same platform ranks. Or just say them ("cortisol on Pressbooks is #8").

## Start the day with my own plan
Say what you plan: "today I add articles on ResearchGate and Pressbooks — give me topics I don't have there; and forum posts on thermaltake on topics where my sites rank". The navigator keeps your plan and fills each part with topics from your base (missing there, strongest first, with the page to learn from). No plan in mind? Say "give me a plan" and it builds one.

## Publish one topic on all my platforms
Wrote a page? Say "roll this topic out" (or "where else should this go?"): you get your platforms that don't have the topic yet, ★ first, and a version for each in its own format — a book chapter, a forum thread, a podcast episode, a Gamma guide — new angle each time, same facts and your links.

## What to write and where
"What should I write next?", "which topics are missing on Medium?" → topic coverage: a table of your topics × platforms and the best gaps, e.g. *glp1 patch review → Medium: #7 and earning on the forum, Medium is your priority platform*. Pick one and it goes to content-type-selector and sales-review-writer (a new angle, never a copy).

## Pick a product or program
"Which program should I promote?" → `affiliate-finder`: pick a niche (nutra, gambling, crypto, gaming, software…), get programs from networks and direct merchants sorted by how popular the offer is in search, 15%+ commission, traffic rules checked. Then "is [product] worth it?" → `niche-analysis`: volumes and an entry score for the top 20 (is one of our kind of platforms there?).

## Find where to publish
"Where can I publish about [niche]?" → `platform-finder`: Rumer's checked platforms first (with a key), then a live scan of "[product] review" for 20–50 affiliate products — where reviews rank in the top 10 now. The scan is paid (your DataForSEO), cost shown first. Free and paid platforms are listed separately. Before the first post: "analyze [platform]" → `platform-analyzer`.

## Write and publish a page (full cycle)
1. "What should I write about [product] for [query]?" → `content-type-selector` picks the type and topic.
2. "Write it for [platform]" → `sales-review-writer` (current prices via product-researcher).
3. "Make images" → `post-illustrations`.
4. "Audit it" → `page-audit` (two scores: Rumer's rules and copywriting); fix until the score is good.
5. Publish it yourself. Worked on the text? "Save this .docx with the page" — it can be republished if the page is removed.
6. Say "published: [URL], [platform], [program], pack [name]" → `work-log` records it; add a sub-ID to the affiliate link if the network supports it. The page is now in the check queue.

## Log a sale
Say "made a sale, $42, ClickBank" (add the page if you know it). → `work-log` records it. If the same sale later arrives in an export, it is counted once.

## Upload sales from an affiliate network
1. In the network, export the transactions / conversions report as CSV for the dates the check queue shows. Ask "how do I export from [network]?" for the steps (ClickBank, Digistore24, Everflow, Post Affiliate Pro, Impact, CJ, Awin, Amazon…).
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

## What took off and where to scale
"What took off this month?", "where do I scale?" → `client-reports`: the review of your asset (live pages, top 3, what earns) and a scale plan — products that earn get pages on more platforms and new angles, platforms that sell get more posts, what earns nothing in 60 days stops. The navigator puts it into your daily tasks.

## Republish after a removal or a cleanup
"Which of my pages were on Pressbooks?", "republish my removed pages" → the list with status, earnings and your saved source for each, ★ and earning first. Each is rewritten for a new platform (new title and angle, the platform's format), never copied.

## Agencies: work for clients

1. **Start:** "I'm an agency" (or pick it at the role question) → agency profile once: name, logo text, report colours, report language, white-label.
2. **New client:** "New client: Acme" → two short messages (the business; access and data). You get a brief, a ready message to the client with the open questions, and the access steps: Search Console (add your Google account as Restricted user), GA4 (Viewer).
3. **Baseline:** "Brand audit for Acme" → site quick audit, profiles on social networks and platforms, content audit, a plan of profiles to open or fix. Then Month 0: Search Console 3 months (brand queries separately), positions for the target queries.
4. **Content plan:** "Content plan for Acme, November" → topics × platforms × format × dates × UTM links, sent to the client for approval; only approved rows are produced.
5. **Every piece:** content type → text in brand mode (disclosed as the brand's) → images in the client's style (infographics by Claude; cover prompt for Gemini free, or ChatGPT / Midjourney / Canva) → audit on the brand scale (75+ goes to the client) → client approval → you publish → "published for Acme: URL" (monitoring switches on).
6. **Every day:** "What do we do today for clients?" → today's plan across all clients, waiting approvals, broken pages, report dates.
7. **Every month:** "Monthly report for Acme" → upload the GA4 export (traffic acquisition, `utm_medium = parasite`, with Session manual ad content for per-page numbers) and the Search Console export → PDF + dashboard in the agency's name, against Month 0, with next month's plan.

Every client has its own folder (`clients/acme/`); nothing from one client appears in another's plan or report.

## Creators: get your videos and posts into Google for free

1. "I'm a creator" → your profile (niche, who you are, audience, how you earn) and the links to all your channels.
2. "Audit my channels" → each channel checked for Google and in-app search, with ready texts: name line, bio, About, playlist titles, and the settings to turn on.
3. "Content plan for 2 weeks" → topics people search for, and the posting model: one idea → long video, shorts, pins, text post — sized to your time.
4. Before filming: "video package for [topic]" → title, hook, chapters, description, spoken and on-screen keywords, captions, hashtags, cover prompt (free in Gemini), pinned comment.
5. After publishing: "check my video: URL" → what's missing, indexed or not, does it show for the query in Google. Fix the title, description, chapters or captions if needed.
6. Not in Google after 7–14 days → "index my video" → free ways first, a low-cost indexer only if you want it.
7. Every month: which videos rank in Google, what to make more of; "make my media kit" for sponsors.

## Site owners: grow your own site

1. "I promote my own site" → a brief about the site: what it sells, top pages, queries each page should win, what a conversion is.
2. "Audit my site" → site quick audit, profiles, and page audits of the landing pages your links will point to.
3. Month 0: Search Console 3 months, positions of the site's target queries (its landing pages are logged with their queries).
4. "Content and link plan for November" → topics × platforms × link target, rel and anchor × free or paid (price).
5. Paid placements: "where can I buy an article for my site?" → wires and marketplaces with prices and link policy, a plan for your budget, the press release or article written, then "published: URL, cost $149".
6. Every page: CTA to the site with UTM; logged with its link (`--link-target --link-rel --anchor --cost`).
7. Every month: upload GA4 (Session source / medium, Session manual ad content, Sessions, Key events, Purchase revenue) → "how did my pages pay off?" (`site-roi`), "my backlinks" (`backlinks`), and the site owner report.

## Connect your key (Pro, Insider)
PARASITER has two parts, and paid plans need both: the **plugin** (skills and agents: the method, articles, audits, journal; works without a key as Free) and the **connector** (your key: the link to the server). The key comes in the welcome email after payment. It connects the plugin to the PARASITER server: checked platform database and feed, news, weekly analysis, daily page checks, Telegram. Install the plugin first, then connect the key. Lost the steps? The bot sends them again: /setup.
- **Claude Code:** the plugin asks for "PARASITER key" when you enable it; paste the key. To change it later, reconfigure the plugin's options.
- **Claude desktop / claude.ai:** add a custom connector named PARASITER with the personal URL from the email (`https://parasiter.affiliatecredo.com/mcp/<your key>`). The URL contains the key: never share it.
Check: say "my PARASITER plan" → `account_info` shows the plan and until when. Never paste the key into the chat.

## Get news and notifications in Telegram (Pro, Insider)
Say "connect Telegram" → open the personal link → press Start. The bot sends invites to your plan's channel (and the Insider group). "What's new?" shows the same news in Claude.

## Change language
"Switch to Spanish" — plans and explanations change; pages keep the content language of your target country unless you change it too.

## Get help
"Help", "what can PARASITER do?", "is there a skill for …?" → this help.
