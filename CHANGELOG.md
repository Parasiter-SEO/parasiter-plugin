# Changelog

Each version's section is posted to the news feed and the Telegram channels when it is released. Written for users: what you can do now and what to say to start it.

## 0.40.0 — 2026-11-09

**🏆 Top-10 platforms of the week.** Rumer's ranked pick of the 10 platforms that hold posts and bring results right now — with why, type, sign-up link and a live example — pinned at the very top of the panel and updated every week. Say **TOP** (or "top 10 platforms") to open it; today's plan puts uncovered Top-10 platforms first. Pro and Insider.

## 0.39.0 — 2026-11-09

**Position checks on SerpApi too — start free.**
- **Second option next to DataForSEO:** connect your own **SerpApi** account (free plan: 250 searches a month, enough for a weekly top-10 check of 50–80 pages). /plugin → PARASITER → configure options → **SerpApi API key**. The key goes to secure storage and only to serpapi.com.
- **Connect one or both.** With both, PARASITER asks which to use for each check: SerpApi while your free searches last, DataForSEO for big runs, the top 100, page keywords and the AI-answer check.
- Say *"is my SerpApi connected?"* to see your plan and searches left, then *"check my positions"* as before. Google and Bing positions work on both.
- **Server won't connect with an antivirus on?** Norton Safe Web and similar web / HTTPS protection can block PARASITER. Add `parasiter.affiliatecredo.com` to its exclusions, then `/mcp` → Reconnect. Steps for Norton, Avast, Kaspersky, Bitdefender are in the help (thanks to a beta tester).
- **Windows:** the DataForSEO and SerpApi checks need `python3` — install Python from the Microsoft Store.
- **Fixed:** the update notice could suggest an older version than the one installed. Now the server compares the versions and the notice shows only when a newer one is really out.

## 0.38.0 — 2026-11-08

**Beyond Google: Bing and AI answers.**
- **Bing positions:** say *"check my Bing positions"*. Bing results feed ChatGPT search and Copilot. Your page list shows Bing next to Google ("B 4").
- **AI visibility check:** say *"am I cited in AI answers?"*. For each page's query PARASITER asks Google AI Mode (and, if you want, ChatGPT and Gemini) and tells you: your page is cited, another page of your platform is cited, or not cited. It also lists the other sites these AIs trust for your queries — new platform ideas. Paid from your DataForSEO balance (about $0.0012 per query per engine), cost shown first.
- **AI-ready pages:** the review writer now writes so AI answers can quote you (answer first, facts with dates, named comparison table, real buyer questions). The page audit gives a separate **AI-ready 0–5** line with what to add.
- **Own site:** upload Bing Webmaster Tools → AI Performance exports to your reports to see how often Copilot cites your site.

## 0.37.0 — 2026-11-08

**DataForSEO in the plugin settings.**
- **Your DataForSEO login and password now go into the plugin settings**, not your computer's environment: /plugin → PARASITER → configure options → DataForSEO API login / password. The password is kept in secure storage and sent only to DataForSEO.
- Already set DATAFORSEO_LOGIN / DATAFORSEO_PASSWORD before? Enter them once in the settings; the old variables are no longer read.
- Say *"is my DataForSEO connected?"* to see the status and your balance.

## 0.36.0 — 2026-11-07

**Safer subscriptions and clear updates.**
- **New version? You'll know.** When a new PARASITER version is out, the plan for the day tells you once, with the update steps. Your key and files stay.
- **Key leaked or lost?** Send */newkey* to the bot: a new key comes by email and the old one stops working at once. Then reinstall the plugin and paste the new key.
- **Refunds:** when a refund is made, access ends at once and you get a confirmation email.
- **Beta testers:** your plan for the day reminds you once where to send bugs and ideas (/bug, /idea, /feedback in the bot).

## 0.35.0 — 2026-11-06

**Your publication queue: what to publish next, where and why — from your own numbers.**
- **Say *what should I write next?*** — PARASITER ranks your next pages from your pages, positions, sales, traffic and affiliate links, each with its reason ("#3 on Medium, earns $240 — missing on LinkedIn"):
  - **Fix & push** — pages at #4–20 to push into the top 3, pages with traffic but no sales to audit;
  - **Scale** — topics that rank or earn, missing on your strong platforms;
  - **Expand** — products from your links with no pages yet, best sellers in new content types (A vs B, complaints, pricing);
  - **Explore** — sister products of programs that already pay you, a new platform while you're under 10.
- **Plan by numbers:** reply "1, 3, 5" and they go into your plan for the day you choose; the day plan takes new pages from the queue in your time.
- **It updates itself:** after every upload of pages, sales or positions the queue is rebuilt; a page you publish and log marks its item done. *What did the queue bring?* shows earning pages, top 10 and commission per group — and what earns weighs more next time.
- **Your mix:** 70% scaling what works, 20% new products and formats, 10% experiments. Say *more experiments* or *only what works* to change it.

## 0.34.0 — 2026-11-05

**Your base is yours — export it any time, keep it when a plan ends.**
- **Export my base:** say *export my base* — one zip with every PARASITER file as it is (journal, sales, platforms, links, profile, goals), an Excel workbook and a README on how to bring it back. Works on any plan, even without a key.
- **Nothing is lost when a plan ends.** Your files live in your own folder, never on the PARASITER server. Renew within 30 days and the same key continues with your settings; later, a new key works with the same files.
- **Change plan without a new key:** Insider → Pro or Pro → Insider with the same email keeps your key, files and settings; only the channels change.

## 0.33.0 — 2026-11-04

**A shorter checkout.**
- Your Claude plan is no longer asked on the payment page: the navigator asks it once at the first start, and says it's not a purchase — it only picks the work mode for your Claude limits (Lite on Pro, agents on Max).
- The payment page lists the agents by name, as short as the skills.

## 0.32.0 — 2026-11-04

**PARASITER works by your Claude plan: Lite on Pro, agents on Max.**
- **Every answer is PARASITER at work:** a skill with Rumer's rules, criteria and references, and the label shows it — `▸ PARASITER · <skill> · Lite` or `▸ PARASITER · <skill> → <agent>`. The reply names what it stands on: Rumer's rules, the checklist, the platform base.
- **Your Claude plan sets the depth.** On **Claude Pro**, heavy steps run in **Lite**: the same skills in a smaller scope, so your limits last. On **Max / Team**, the skills' agents run at once.
- **Advice instead of commands:** when the full version would give a better result, PARASITER says why in one line and gives the phrase — **full**. An independent audit of an article written in the chat is always offered.
- **Change it any time:** "I'm on Max now" in Claude, or `/plan` in @parasiter_bot. "save limits" → Lite, "turn on agents" → agents always. Hit the usage limit? PARASITER switches to Lite by itself.

## 0.31.0 — 2026-11-04

**Articles ready to post, bases one tap away.**
- **Every article is a finished product:** formatted in the chat **and a Word `.docx`** with the same headings, tables, lists and links, plus the JPG images and the cover prompt — all in one delivery. Every product name links to the product: PARASITER asks for your affiliate links before writing. No `.md` / `.txt` files and no Markdown unless you ask. Presentations get the same, split by slides.
- **Bases and data first on the panel:** **Б1 / B1** Rumer's platform base (Free key: 50 platforms) · **Б2** my platforms · **Б3** journal · **Б4** my offers and links · **Б5** feed. Type the code, "base" or "journal" — the table opens at once; filter in words.

## 0.30.0 — 2026-11-04

**A working desk per role, honest indexing, images as real files.**
- **Your role's desk:** "menu" / **0** shows your role's skills under its own numbers (affiliate: 16 skills, 7 agents); no client reports on the affiliate desk — there it is "Analytics: what earns and what to scale". Other roles' functions: *"all functions"*.
- **Indexing without myths:** no free tricks — links and social posts don't get parasite pages indexed. The only free way is your own site in Google Search Console. Otherwise indexing services: regular ones (results in days, Rumer's comparison with prices) and instant ones (one to a few minutes, about $0.50 a link — the tools are kept secret, but you can find them yourself).
- **Paid placements:** agencies and wires work by contract and mostly with companies; each service shows its work format (one-off · package · contract). XPR Media: big packages for long periods. Without a company — start with prnews.io or Collaborator.
- **Images:** infographics come as separate JPG files exactly 700 px wide, named in order (`01-quick-facts.jpg`…). For the cover — paste a **screenshot** of the product photo into Gemini (no saving). A table of generators with their free and paid terms: Gemini, ChatGPT, Canva, Midjourney.

## 0.29.0 — 2026-11-03

**Every function under a number — jump anywhere, come back.**
- Say **"menu"** or **0** any time: all 21 skills under fixed numbers by section, ✓ tried / ○ not yet, and "Explored: N of 21 skills · M of 10 agents". Reply with a number to start that skill at once.
- **Jump and return:** ask for an audit or offers in the middle of anything — it runs right away; your plan, setup step or draft waits, and **1 — back** takes you there.
- **No pressure:** publishing, reports and setup steps are offers you can skip; "behind" only shows when you work by goals you set.
- **Exploring mode:** "I want to try all the skills" walks you through the untried ones on short examples; "plan for today" switches back.
- The panel as a page (or an artifact) with a copy button for each number.

## 0.28.0 — 2026-11-03

**Your day plan as a page, articles ready to copy.**
- **Plan for today looks like a dashboard:** goal and week progress, task cards with time, what each task moves, a phrase to copy and a "done" checkbox. An artifact in the Claude app; in Claude Code `plan-today.html` in your PARASITER folder opens in the browser. In the chat — a short clean list, no more code block. Say *"plan for today"*. *"Am I on track?"* — the weekly review the same way.
- **Articles come right in the chat:** press the copy button under the reply and paste into the platform's editor — headings, lists, tables and links keep their look. No file by default; say *"file"* for a Word copy. Markdown / BBCode platforms also get the source in a code block, presentations get the text by slides. Long articles come in parts.

## 0.27.1 — 2026-11-03

- The Free key opens **50 checked platforms** (was announced as 100): a hand-picked snapshot, each with its check date and sign-up link.

## 0.27.0 — 2026-11-03

**Free key: platforms on the Free plan.**
- **Get a free key by email, no card:** parasiter.affiliatecredo.com/free.html. Paste it when the plugin asks for "PARASITER key (Free, Pro or Insider)" (reinstall the plugin if it was installed without a key).
- **50 checked platforms:** say *"show the free platform base"* — type, language, status, check date and sign-up link for each. It is a snapshot: check a platform before you invest in it.
- **3 platform scans a week:** say *"where do reviews of <product> rank?"* — one product per scan, the top 3 platforms in full with live example posts. *"How many scans do I have left?"* shows the week.
- **Pro adds** the whole checked base with live example posts, new platforms every week, what is alive today, cleanup alerts, the journal and the daily plan.

## 0.26.1 — 2026-11-02

**One way to install: Claude Code.**
- Install with two commands in Claude Code: `/plugin marketplace add Parasiter-SEO/parasiter-plugin`, then `/plugin install parasiter@parasiter`.
- Pro or Insider: paste your key when the plugin asks for "PARASITER key (Pro or Insider)". Free: leave it empty.
- Check with *"my PARASITER plan"*. Shows Free? Reinstall the plugin and paste the key when asked.

## 0.26.0 — 2026-11-02

**You choose the platforms; PARASITER shows only what works.**
- **Candidates, not orders:** a goal says how many platforms, never which. You get 5–10 candidates with live example posts, sign-up links and risks, a ★ on the ones worth starting with, and pick by number ("1, 3"). Your daily plan uses only the platforms you chose.
- **Cleaner platform lists:** a stop list (YouTube, S3 files, Q&A sites) and a blacklist of platforms that stopped accepting posts are skipped in every scan; PDFs on normal hosts are back as findings.
- **Example posts checked live:** every platform shows a real post first (best position on top), opened and checked before it's listed. Platforms whose posts are all removed are listed apart and skipped in everyone's next scans, so you don't pay to scan them again.
- **Direct sign-up links** instead of bare domains.
- **Images at $0:** infographics drawn by Claude in the chat, the cover from a real product photo or one free Gemini prompt (ChatGPT / DALL·E only if you already pay for it). Explained once.
- **Capability map** at the first start and every session: every skill and agent for your role, what to say, and its plan. Say *"map"*.
- **Indexing from day one:** set up right after you upload your pages; pages out of Google become your first task.
- **Topics picked by Rumer's rules:** every topic carries its "Rumer filter score (of 12)"; ask *"why 9?"* for the breakdown.
- **Write in batches, publish later:** after an article the first option is the next topic, not an audit — the writer already checked it ("Check by Rumer's rules: N/100"). Say *"I published"* with one or many links: they are logged, checked, sent to indexing as one list and queued (index in 3–7 days, positions in 14). Unpublished articles show up as one line in your daily plan.
- **The right file for each platform:** Markdown only where the platform reads it; visual editors get formatted text and a doc; presentations get a slide-by-slide doc.
- **Plan check:** Pro and Insider features check your plan first and offer what works on yours. Insider skills load their method from the server with an Insider key; on Pro, *"check my offers"* checks the offers you already chose.
- **Affiliate approval:** the offers table has an Approval column (auto / manual / strict / invite-only, with source); say *"how do I get approved?"* for Rumer's 9 rules. Beginners start with auto-approval programs.
- **Help:** installing from the Claude website, connecting your key with a hidden header, and why to keep your own connector on.

## 0.25.0 — 2026-11-01

**You always know what to do next.**
- **First setup with a progress bar:** 12 fixed steps, from language to your first published page. Every reply shows "step N of 12", what is done and the one thing to do now. Progress is saved — a new chat or a break picks up at the same step. Say *"skip"* to leave a step for later, *"where am I?"* to see the list.
- **Ready phrases at the end of every reply:** numbered options you can copy, or just answer "1". No more internal names to guess.
- **Plan-aware suggestions:** features outside your plan are marked (Pro) or (Insider) instead of being offered as the next step.

## 0.24.0 — 2026-11-01

**Your pages stay yours.** The PARASITER server no longer receives or stores your page addresses.
- **Page checks run in your own Claude:** say *"are my pages alive?"*, or *"check my pages every morning"* (or every Monday) to set it on your own schedule. The check queue still plans them for you; results go to your journal.
- **Telegram gets counts only:** "40 checked · 2 removed · 1 noindex" — the list stays in your project. Platform cleanups are still spotted across subscribers, from platform domains and counts only, without names, kept 7 days.
- **Nothing to set up:** pages are no longer sent to the server when you log them; addresses stored by earlier versions were deleted.
- **Legal products and content only:** PARASITER doesn't write, plan or log pages for pirated files, file-upload or "free download" schemes, cracks or illegal goods, and offers a legal alternative.
- Privacy policy and offer updated: what the server keeps, for how long (settings are deleted 30 days after a subscription ends), and how to ask for deletion.

## 0.23.1 — 2026-11-01

- Help: step-by-step Monday check-in and the full list of bot commands.

## 0.23.0 — 2026-11-01

**Monday check-in** (Pro and Insider, Telegram linked) — every Monday at 10:00 Kyiv the PARASITER bot asks for last week's numbers, so your journal and goals stay true.
- **What to bring:** sales from your affiliate networks (export, Excel or screenshot), traffic from your platforms' stats and the network click report, and your UTM / GA4 / Search Console data if you use them.
- **Then say *"weekly check-in"* in your PARASITER project:** everything is logged, sales are tied to pages, and you see what earned, what grew and what dropped against your goals.
- **Position check:** one tap shows how to check how your keywords and posts moved — on your own SEO API, with the pages and cost shown before anything is spent, or every week on a schedule.
- **Buttons:** Done · Remind me at 19:00 · Position check · Skip this week · Turn off. `/checkin on|off` in the bot, or *"turn off Monday check-ins"* in Claude. A week you already logged gets no reminder. Your data stays in Claude: the bot never asks for exports or keys.
- **Help knows it:** say *"help: Monday check-in"* or *"bot commands"* for the steps and every command of the bot.

## 0.22.1 — 2026-10-30

- **Indexing is advice and tracking; you send.** PARASITER no longer sends pages to indexers or asks for indexer keys. You get the clean list for each of your services and send it yourself — to one indexer or several.
- **Mix indexers freely:** say *"sent to SpeedyIndex and Rapid"* — the page is logged with both, and *"my indexing stats"* shows every mix as its own line next to each single service.
- The agent is now `index-checker`: it checks what blocks indexing and whether pages are already in Google, and returns the list worth paying for.

## 0.22.0 — 2026-10-30

**Indexing** (`indexing`, Pro) — a page that isn't in Google can't rank. Say *"index this page"*, *"which indexer should I use?"* or *"my indexing stats"*.
- **The best indexers for parasite SEO, compared:** Rapid URL Indexer, SpeedyIndex, Indexceptional, IndexMeNow, Omega Indexer, GIGA Indexer and newcomers — price per URL, what happens to URLs that don't get indexed, 2026 test results, API, Telegram bot. Rumer's picks first; dead and weak services marked.
- **Set it once:** your indexer, and when to send — every new page right after you log it, or only pages still out after a few days.
- **No money wasted:** before sending, every page is checked for what blocks indexing (noindex, canonical, robots.txt, login wall, a platform that stopped indexing). Blocked pages are fixed or moved, not paid for.
- **Free ways first:** links from your own indexed pages and profile, inside the platform, socials; Search Console and IndexNow only for your own site.
- **Sent for you:** the new `index-runner` agent sends pages to SpeedyIndex by API with your key; for other services you get a clean list and where to paste it. The price is shown before anything is sent.
- **Every submission counted:** logged with the service and price, rechecked 4 days later, resent via another service only after the refund window. *"My indexing stats"*: per service — sent, indexed, rate, days, cost per indexed page; per platform — which ones index on their own, so you stop paying there.
- Pro now has 17 skills; the full system 21 skills and 10 agents.

## 0.21.0 — 2026-10-29

- **Your base of posts, open and in Excel.** Say *"open my base"*: a dashboard page with every post you logged — totals (posts, ★, platforms, alive, indexed, top 10, need attention, sales), the status of your posts on each platform, and a table you can search, filter by platform, status, topic and offer, show only ★ or only top-10 pages, and sort by any column. Light and dark, works on a phone.
- **Download it any time.** *"My posts in Excel"* or the **Download Excel** button gives a workbook with Summary, Posts (one row per page as it stands today), Platforms, Sales, Links and your full Journal: filters on, links clickable, dates and numbers as real values. **CSV of this view** saves exactly the rows you filtered. Labels in English, Russian, Ukrainian, Spanish and Portuguese.

## 0.20.0 — 2026-10-29

**PARASITER for creators** — a free route for bloggers and content creators with no ad budget. Ads are expensive; your content can rank in Google for free. Say *"I'm a creator"*.
- **Your channels as parasite SEO** (`creator-channels`): creator profile, every channel connected (YouTube, Instagram, TikTok, Facebook, Pinterest, LinkedIn, X, blog, podcast), an audit of each for Google and in-app search with ready texts (name line, bio, About, playlists) and the settings to turn on — e.g. Instagram's "appear in search engine results" for professional accounts.
- **Content plan from search** and the posting model: one idea → long video, 3–5 shorts, pins, a text post with the video embedded — sized to your time.
- **Video SEO** (`video-seo`): before filming — query, title, hook, chapters (Google Key moments), description, spoken and on-screen keywords, captions, hashtags, cover prompt, pinned comment; after publishing — a check by the new `video-seo-checker` agent: what's missing, indexed or not, does it show in Google's video and Short videos results.
- **Indexing:** free ways first (links from crawled pages, your hub, Search Console and IndexNow for your own site); a low-cost indexer only if you choose it, tested on a few URLs first.
- **Tracking and income:** positions in Google incl. video blocks, monthly review, a media kit for sponsors from your real numbers, disclosed affiliate links.
- Free plan now has 8 skills (creator-channels and video-seo added).

## 0.19.0 — 2026-10-29

**PARASITER for site owners** — a full route for owners of a site, shop, services or course who build parasite pages around their own site. Say *"I promote my own site"*.
- **A workspace for your site** (`client-workspace`, own-site mode): brief about what the site sells, Search Console and GA4, UTM on every link, Month 0, a monthly content **and link** plan, today's plan. No client approvals, no white-label.
- **Links tracked.** Log the link each page gives your site — target page, dofollow / nofollow, anchor, cost: *"my backlinks"* shows links live, dofollow per target page, anchors (warns when one money anchor dominates) and spend per live dofollow link. Platforms are marked by the link rel they give.
- **Sales closed on the site.** GA4 exports with Key events and Purchase revenue (by Session source and Session manual ad content) are imported per page and platform; *"how did my pages pay off?"* gives visits, conversions, conversion rate, revenue, spend and return. `--medium parasite` counts only our traffic.
- **Site and landing pages audited** by Rumer's content rules before links point to them (`brand-presence`, `page-audit`).
- **Paid placements** (`paid-placements`, new agent `placement-scout`), for site owners and agencies: a base of press-release wires (EIN Presswire, ACCESS Newswire, GlobeNewswire, XPR Media, Newswire.com, PR Newswire, Business Wire) and sponsored-article marketplaces (prnews.io, Collaborator, Adsy, WhitePress) with prices or how to request a quote, link policy, distribution and niche limits; a plan for your goal and budget, a fresh check and a marketplace shortlist, the release or article written, logged with its cost, and judged by return after 30 and 60 days. Honest about links: wire links are usually nofollow; dofollow comes from chosen marketplace sites.
- Site owner monthly report: revenue from our pages, conversions, spend and return, live dofollow links, target queries in the top 10 vs Month 0.

## 0.18.0 — 2026-10-29

**PARASITER for agencies** — a full route for SEO and marketing agencies, freelancers and in-house teams running parasite SEO for clients. Say *"I'm an agency"*.
- **A desk for every client** (`client-workspace`). Say *"New client: Acme"*: two short messages make the brief — business, target queries, where the traffic goes (site, YouTube, LinkedIn, socials), voice and limits, KPIs — plus a ready message to the client with the open questions and the access steps for Search Console and GA4. Each client has its own folder, journal, plan and reports; nothing mixes.
- **Month 0.** Search Console for the last 3 months (brand queries separately), positions for the target queries and the brand audit are recorded before work starts, so every report shows growth from day one.
- **Brand and site audit** (`brand-presence`, new agent `brand-auditor`). Say *"brand audit for Acme"*: which profiles the brand has on LinkedIn, YouTube, Medium, Reddit, Quora, X, Facebook, Instagram, Pinterest, TikTok and directories — complete, consistent, active — a quick site audit (indexing, landing pages, titles, speed, tracking, trust) and what the brand already publishes. You get a plan of profiles to open or fix and topics nobody covers.
- **Monthly content plan with client approval.** *"Content plan for Acme, November"*: topics × platforms × format × dates × UTM links; only approved rows go to production.
- **Today's plan across all clients.** *"What do we do today for clients?"*: due pieces, waiting approvals, broken pages, report dates.
- **Brand mode** in the writer: expert guides, honest comparisons, case studies, LinkedIn / Medium articles, YouTube descriptions, press releases and profile bios — disclosed as the brand's, with UTM links. Page audit scores client pages on a brand scale (disclosure, voice, UTM, design in the client's style); 75+ goes to the client.
- **Images:** infographics in the client's colours drawn by Claude for free; for the cover one prompt and a choice where to make it — Gemini free by default, or ChatGPT, Midjourney, Canva.
- **Traffic to the client:** every link carries UTM (`utm_medium=parasite`); GA4 exports credit visits per platform, and per page through the page's sub-ID (= `utm_content`). Search Console shows the client's own site and its brand queries.
- **Monthly white-label report** against Month 0: positions, visits from our pages, brand-query clicks, delivered vs plan, next month's plan — PDF + dashboard in the agency's name.
- Platform finder for clients: probes the client's category and competitors, marks brand-safe platforms, starts from the brand's own profiles.
- The client's own landing pages are tracked with their target queries, so the client's site positions are in every report from Month 0.
- Reports in the agency's colour with its wordmark (`accent`, `logo_text`).
- NDA clients: `Server monitoring: off` in the brief keeps their pages off the PARASITER server.
- Plans: the agency route runs on Pro (plain monthly report, manual brand checklist); Insider adds the brand audit agent and the white-label client report.
- Course authors / own-product owners can now write about their product in brand mode (disclosed as theirs).

## 0.17.1 — 2026-10-28
- Every page you log or import goes on daily server monitoring automatically (Pro / Insider) — no need to ask.
- Every skill ends its reply with 2–3 next steps and what to say; "help" shows all functions.
- client-reports: pages without data show "—", not $0; commission by program and month per currency; reversed orders excluded.

## 0.17.0 — 2026-10-28
- client-reports: every report now also comes as a designed document — PDF (A4) and a private page with KPI tiles, charts, findings, next actions and a pages table (`scripts/visual_report.py`).
- help: support via @parasiter_bot; public channel @parasiter_plugin.

## 0.16.2 — 2026-10-28

- **Plugin + connector explained.** The navigator now tells a paying user whose server isn't connected that PARASITER has two parts (plugin and connector), and gives the steps for Claude Code and for the Claude app. Help (how-to) explains the same.

## 0.16.0 — 2026-10-25

- **Rumer's rule in your goals:** the minimum working base is about 10 platforms and 100 live posts. If your goal is below it, the plan says so and climbs toward it first; the daily plan shows where you are ("6/10 platforms, 48/100 posts · top 3: 4/15"). Posts in the top 3 are tracked as a milestone: that is where sales start.
- **Where reviews rank now.** Say *"where can I publish about [niche]?"*: a scan of "[product] review" for many affiliate products shows the platforms where review pages are in the top 10 today, free and paid separately. Paid scans and checks always show the cost first and run only after your yes.
- **Your reviews are kept.** Save the .docx you worked on with its page; if a page or a whole platform is cleaned up, *"which of my pages were on X?"* lists them with their sources to republish. Cleanups seen across subscribers are posted in the channel.
- **Two scores in every audit:** Rumer's rules and copywriting. Articles now open with a facts box (price, quality, my rating, special offers, link) and a real cover photo.
- **What took off and where to scale:** the monthly review shows which products, platforms and content types earn and plans more pages for them.
- **Possible income, not promises.** Goal tables show "possible income" at your own numbers. Your goals start from your real data: what your reports show, plus your own word on what you earn, since reports rarely cover everything.

- **First setup asks for your real numbers.** After a few short questions (niche, programs, country, time, tools) the navigator asks you to upload what you have: live pages, affiliate links, sales reports from every program and any traffic data. For each program you name you get the steps to export the report from its dashboard. Your goals start from these numbers, not from guesses.
- **Traffic from anywhere.** Network click reports by referrer, Google Analytics (source / medium, UTM, landing pages), Gamma analytics, podcast plays, shortener clicks — by page when the page is known, by platform when it isn't. Say *"here is my traffic report"*.

## 0.15.0 — 2026-10-25

- **You always see which part of PARASITER is working.** Every reply starts with a short label: the skill, and the agents it called (for example `▸ PARASITER · sales-review-writer → product-researcher`).

## 0.14.0 — 2026-10-25

- **Your key now connects the plugin to the PARASITER server.** Checked platform database and feed (Insider the day a platform is found, Pro a week later), news and weekly analysis, daily checks of your pages (up, removed, noindex) with alerts in Telegram. Claude Code asks for the key when you enable the plugin; in Claude desktop and claude.ai add the personal connector URL from your welcome email. Say *"my PARASITER plan"* to check.

## 0.13.0 — 2026-10-24

- **One topic → all your platforms.** After every new article the system shows which of your platforms don't have the topic yet and makes a version for each in its own format: book chapter, forum thread, podcast episode, Gamma guide, community post. New angle each time, never a copy. Say *"roll this topic out"*.

## 0.12.0 — 2026-10-24

- **What each page ranks for — and what it lost.** Say *"which queries do my pages rank for?"* or *"what did my keto page lose?"*: every page gets its Google queries with volume, position and estimated traffic, plus the queries it lost and when. Shows which pages really bring visitors and what dropped before a sales dip.

## 0.11.2 — 2026-10-24

- **AI Overview and SERP blocks.** Position checks now see your pages cited in Google's AI Overview, "Discussions and forums", images and videos, not only the organic list.
- Mobile or desktop check, top 30 by default (cheaper; that is where traffic is).

## 0.11.1 — 2026-10-24

- **Sales with the referring site.** Network exports that show where the buyer came from (Everflow / FanFuel `referer`) now credit the estimated share to your pages on that platform. Repeat-customer offers are merged with the main offer and marked.
- **Several currencies** (EUR from one network, USD from another) are reported side by side, never mixed.

## 0.11.0 — 2026-10-24

- **Your affiliate links library.** Part of the first setup: upload your links for every product (a list, a table or screenshots of your network's link page). Articles use the right link without asking, and *"which products have no pages yet?"* shows what to write next. Say *"here are my affiliate links"*.

## 0.10.0 — 2026-10-24

- **Your plan for the day, filled with ideas.** Tell the navigator what you want to do today — "articles on Medium and a document platform, topics I don't have there; forum posts on topics where my sites rank" — and get topics for each part from your own base: missing there, strongest first, with the page to learn from. New platforms work too. No plan? Say *"give me a plan"*.
- **Your own sites as a source.** Register them in the platform base; topics where they rank in the top 10 become ideas for parasite platforms.
- Position checks retry automatically and can download already-paid results for free.

## 0.9.0 — 2026-10-24

- **Positions from any rank tracker.** Upload a CSV export from Ubersuggest, SE Ranking, ProRankTracker or any other tracker: positions are matched to your pages by URL or keyword. Rows where another page of the same platform ranks are skipped.
- **Positions of all your pages, automatically.** Connect your own DataForSEO account (cents a month) and say *"check my positions"*: every page is checked in Google by its query, positions go into your journal with what changed — new in the top 10, up, down, out. Coverage advice and the page list update from it.

## 0.8.1 — 2026-10-23

- **Your platform order.** Say *"Medium is my #2 platform"*: the order leads the advice. *"What topics are missing on my top platforms?"* lists, per platform, the topics you wrote elsewhere but skipped there.

## 0.8.0 — 2026-10-23

- **What to write and where.** Your topics × platforms in one table, and the best gaps: a topic that is in the top 10 or earning on one platform but missing on your strong ones. Say *"what should I write next?"* or *"which topics are missing on Medium?"*
- **Top positions.** Checks record the page's position; see which pages are in the top 10, per page and per platform. Say *"which of my pages are in the top?"*
- **Priorities.** Mark your main pages, topics and platforms (★): they are checked first and weigh more in the advice. Say *"Medium is my main platform"*.
- **Topics.** Pages on the same subject are grouped across platforms; name them once, in batches.

## 0.7.0 — 2026-10-23

- **Bring the pages you already have.** Upload or paste your published pages — a list of links, CSV, Excel, any table. Each page goes into your journal with its platform, date, offer and program when the table has them; duplicates are skipped. Say *"here are my pages"*.
- **Your own platform base.** Built from your pages automatically: every platform with pages, alive, indexed, gone, sales, score and state (active, testing, paused, dropped, dead). Say *"my platforms"*. Platform analysis writes its score into it, and platform search marks the ones you already use.
- **One bulk check for imported pages** instead of hundreds of separate reminders.

## 0.6.4 — 2026-10-23

- **Writer profile.** Fill it once (author block, photo, your affiliate links, disclosure, CTA and image style), save it in your Claude Project, and every article only asks what is new: product, link, deal, platform. Say *"set up my writer profile"* to start.

## 0.6.3 — 2026-10-23

- **Your link everywhere it sells.** Before writing, Claude asks for your affiliate link for every product, links the product name in the facts box, each section, the tables and the verdict, and builds the CTAs on it.
- **Images come with the article.** Quick facts, pain → solution, comparison and price cards are drawn as JPG right in the chat; for photo-like images you get a ready prompt for your image generator.
- **Ready to paste.** Fully formatted in the chat: headings, table of contents, lists and 3–5 tables. Copy it straight into Medium, LinkedIn or WordPress; a Markdown/BBCode copy for forums and Reddit.

## 0.6.2 — 2026-10-23

- **Stronger sales articles.** Every review now works through the reader's pains, shows how the product solves each one, paints the "life after", has a dedicated prices and current offers block, and compares the product with competitors and natural alternatives. Minimum 1,500 words.
- **Copy in one go.** The finished article comes on screen as one clean block, ready to paste into the platform; the checklist comes separately. Ask for a .docx if you want a file.

## 0.6.1 — 2026-10-23

- **No more levels.** Beginner / intermediate / advanced are gone. Your plan follows your role, goals, journal and today's time. Ask Claude to explain any term or to make tasks smaller or bigger, any time.

## 0.6.0 — 2026-10-23

- **Choose who you are.** On first run the navigator asks: affiliate, SEO specialist / agency, blogger, course author / own product, or just looking. Affiliates (want to start, already working, professional, veteran) get the full system. Other roles get only the tools that fit their work, without goals and the daily plan. Say *"I'm an affiliate now"* to change your role.

## 0.5.0 — 2026-10-22

- **News feed and Telegram.** New platforms, plugin updates, ideas, market analysis and polls from Rumer now appear in Claude at the start of your session and in Telegram: the PARASITER Pro channel, the PARASITER Insider channel and the private Insider group. Say *"what's new?"* or *"connect Telegram"*. *(Needs the server, in beta.)*
- **Personal notifications** from the PARASITER bot for Pro and Insider: pages that died, a Monday reminder to upload sales, a daily news digest, billing. At most one a day; any type can be turned off.

## 0.4.0 — 2026-10-22

- **Built-in help.** Ask *"what can PARASITER do?"*, *"how do I log a sale?"*, *"is there a skill for …?"* — Claude answers from the plugin's own catalog, how-to recipes and FAQ.

## 0.3.0 — 2026-10-22

- **Sales and traffic in the journal.** Log a sale in one line (*"made a sale, $42, ClickBank"*) or upload a network export — columns are found automatically, duplicates skipped, refunds and status changes applied.
- **Sales without a page count.** Every sale counts exactly by program, month and campaign (pack); page tables add an estimated share.
- **What earns.** Effectiveness by page, platform, offer, program, campaign, content type or month: EPC, conversion, commission per page and per 1,000 views.
- **Weekly sales reminder** for programs with no sales uploaded for 7 days.

## 0.2.0 — 2026-10-22

- **Work journal (`work-log`).** Every page and action is logged as you go; reports for today, yesterday, a week, a month or any dates.
- **Check queue.** Each logged page is checked alive and indexed on day 2, 7, 14 and then every two weeks, and audited for conversion at publishing and at 14/30/60 days.

## 0.1.0 — 2026-10-21

- First private beta: 13 skills and 6 agents — navigator, goals, content-type-selector, sales-review-writer, page-audit, post-illustrations, platform-finder, platform-analyzer, platform-feed, platform-monitor, niche-analysis, affiliate-finder, client-reports.
