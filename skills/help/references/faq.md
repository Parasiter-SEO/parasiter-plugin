# FAQ

## Who is it for?
Built for affiliate marketers who earn with parasite SEO, at any stage — they get the full system. SEO specialists and agencies, bloggers and course authors / own-product owners can use it with a smaller toolset that fits their work, without goals and the daily plan. The navigator asks once ("who are you and what for?"); say "I'm an affiliate now" (or another role) to change it.

## Plans and key
<!-- Maintainer: keep this split identical to the pricing block on the site. -->
- **Free, $0** — plugin without a key, 6 skills: goals, content-type-selector, sales-review-writer, page-audit, post-illustrations, help.
- **Pro, $19/month** — 12 skills: Free + navigator, platform-finder, platform-analyzer, platform-feed, platform-monitor, work-log. Personal key: checked platform database, feed and weekly market analysis, scheduled monitoring, navigator updates; new platforms about 7 days after they are found.
- **Insider, $39/month** — all 15 skills: Pro + niche-analysis, affiliate-finder, client-reports; extra features, new platforms the day they are found, PARASITER Insider channel and the private Insider group.
- Pro includes the PARASITER Pro channel and personal notifications from the bot. Telegram is for paid plans only.
- Annual billing about 20% less. Prices are preliminary — current terms on the official site.
- The key is personal: one key, one person. It stops working when the subscription ends; skills keep working without server data.
- Platform feed updates come as findings appear — several times a week, sometimes less. No daily promise.

## How many platforms and posts do I need?
Rumer's rule: the minimum working base is about **10 platforms and at least 100 live posts**. Below that, one platform cleanup or Google update can take most of your income, and there is too little data to see what sells. It is the minimum goal, not the ceiling; `goals` builds your plan toward it first. Sales start with posts in the top 3: in Rumer's own work, earning begins at 10–15 posts in the top 3 (about $20–50 a day for him), and his 20 platforms with ~400 posts bring about $6,000 a month. That is his experience, not a forecast — your niche, offers and country change it a lot.

## Do I need a paid SEO tool for positions?
No subscription. Search Console only sees your own sites, so for parasite pages PARASITER checks Google through your own DataForSEO account (recommended first: Claude runs it itself, pay per request, minimum top-up $50 that doesn't expire): dozens of pages cost cents. Semrush, Ahrefs, Serpstat or Ubersuggest work too — connect them or upload their exports.

## Will PARASITER spend my money without asking?
No. Every paid check (index, positions, page keywords, platform scans, niche volumes on your SEO API) is named first — which pages, how many, the rough cost — and runs only after your yes, every time. A scheduled weekly check exists only if you set it up; on the day the bot warns you in Telegram with buttons: run as planned, only ★ pages, skip this time, change. No answer = it runs as planned; if the warning didn't reach you, it doesn't run. Free checks (page alive, noindex, link in place) run without asking.

## I'm just starting — no pages, no sales
That's a normal start. The navigator skips the reports, helps you pick a niche and one offer, and `goals` gives you a ladder: first posts and platforms → 15–20 indexed posts → first top-10 positions and clicks → toward 10 platforms / 100 posts and first sales. Possible income is calculated after your first clicks and sales; zero sales in the first 4–8 weeks is normal.

## What platforms does PARASITER look for?
Ones where review pages of affiliate products are published and indexed **right now** (top 10 in Google) — proven parasite platforms. It doesn't hunt for untested sites with no affiliate posts. Whether links there are followed or indexed doesn't matter; the page being indexed does. A platform in the top now goes to work now, even if it may not last; pages living 2+ weeks mark it as stable. Free platforms (you post yourself) and paid ones (news sites, PR wires) are always shown separately.

## Saving my reviews
After you publish a text you worked on yourself, say "save this .docx with the page": it is kept in `parasite-seo-sources/` linked to the page. If the page or the whole platform is removed, "which of my pages were on X?" lists them with their sources to republish. Plain AI drafts are not worth saving — quicker to write again.

## Telegram
- **How to connect**: say "connect Telegram" in Claude, open the personal link, press Start. A username is not enough: Telegram bots cannot write to someone first.
- **Notifications**: one daily summary of your pages that got worse, Monday reminder to upload sales, news digest, billing, warnings before a scheduled paid check. Platform-wide news (new platforms, cleanups) comes in the channel only, never twice. Quiet at night. Turn any off: "turn off news notifications" in Claude, or /stop in the bot.
- **Plan ends**: access to the channels and group ends with it and comes back on renewal.
- The bot never asks for a password, phone number or login code.
- Do not forward channel posts outside: they are for subscribers.

## Where is my data?
- Profile, goals, journal and sales files are in the user's own project folder. PARASITER does not upload them anywhere.
- Sales exports often contain customer data; the import keeps only date, program, product, sub-ID, order ID, amount, commission, currency and status.
- With a key, only what monitoring needs (page URL, main query, platform) goes to the PARASITER server. Linking Telegram stores your Telegram ID with your key. Sales and the journal never go to the server or to Telegram.

## Why can't every sale be tied to a page?
Networks often show no sub-ID or referrer, buyers come back later, and many pages promote the same offer. UTM tags don't help: they go to the merchant's analytics, which the affiliate doesn't see. PARASITER counts every sale exactly by program, month and pack; per-page numbers add an estimated share, always labelled. A sub-ID per page (or per platform / pack), separate Amazon tracking IDs and network click reports make it more precise.

## Which AI does it work with?
Built for Claude (Claude Code plugin; install with `/plugin marketplace add Parasiter-SEO/parasiter-plugin` then `/plugin install parasiter@parasiter`). Other assistants are not supported yet.

## Updates
New versions come through the same marketplace: update the plugin in Claude Code. The feed and platform database update on the server without reinstalling.

## Connecting the key
Claude Code asks for the key when you enable the plugin. In Claude desktop and claude.ai, add a custom connector with the personal URL from your welcome email. Details: how-to, "Connect your key".

## Languages
Works in any language. The working language (plans, explanations) is set on first run; the content language of pages follows the target country. "Switch to …" changes it.

## Levels?
There are none. The plan follows your role, goals, journal and the time you have today. Ask to explain any term, or ask for smaller or bigger tasks, any time.

## Terms (explain in one line when asked)
- **Offer** — a product an affiliate program pays you to sell.
- **Parasite SEO** — publishing your page on a big trusted site so it ranks faster than a new site would.
- **Indexing** — Google has added the page to its search database. No index, no traffic.
- **noindex** — a tag that tells Google not to show the page. A platform that adds it is useless for search traffic.
- **nofollow / ugc** — the link passes no SEO weight, but readers still click and buy. For parasite SEO it doesn't matter: what matters is that the page itself is indexed.
- **Top 3** — where sales start: Rumer counts posts in the top 3 as a milestone.
- **EPC** — earnings per click on your affiliate link.
- **SERP** — the Google results page.

## Rules built in
No fake reviews, tests, results, credentials, prices or deadlines. Personal experience only when real. Affiliate disclosure and last-checked date on every page. Only platforms where the user can legitimately post. No income guarantees: income goals are the user's; the system plans actions and tracks results.

## Risks
Google acts against site reputation abuse; platforms change moderation and remove pages; affiliate and payment networks can block traffic sources or niches. Spread pages across platforms, keep a copy of every text, monitor, check each program's traffic rules.

## Something doesn't work
Describe what happened; Claude tries the step again. If it still fails — Insider: the private Telegram group; others: the author via the official site.

## Can I share the plugin?
No: licensed for the subscriber's personal use; redistribution of the plugin or server data is not permitted.
