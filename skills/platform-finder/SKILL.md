---
name: platform-finder
description: Find platforms where a parasite SEO page can be published and rank — forums, communities, Q&A, article and profile platforms, document hosts, site builders, event and fundraising pages — filtered by niche, language, link rules, indexing speed and moderation. Use when the user asks where to publish, wants new platforms, forums or communities for a niche, or a list of platforms that work now.
---

# Platform Finder

## Work label (testing period)

Start every reply produced by this skill with one line naming it, so the user always sees which part of PARASITER is working:
`▸ PARASITER · platform-finder`
If you called agents for this reply, add them after an arrow: `▸ PARASITER · platform-finder → serp-analyst, product-researcher`. If you hand off to another skill, the next reply carries that skill's label. One line only, no other system talk.

## Next steps (end of every reply)

The user must always know what to type next. End every reply with a short numbered block — ready phrases, not skill names:

**What's next? Reply with a number or the phrase:**
1. "<ready phrase>" — <what happens after it, a few words>
2. "<ready phrase>" — <what happens>

- 2–3 options that fit what just happened, the recommended next step first. "1", "yes", "ok", "go" means option 1. Any free wording of the same wish works too ("give me the offers").
- Each option is a complete phrase in the user's working language that they can copy, plus what it does. Never show skill or agent names here: the work label at the top already names the part that is working.
- Offer only what the user's plan includes (`account_info`, once per session). A Pro or Insider feature on a lower plan appears at most once as the last option, marked "(Insider)" or "(Pro)" with one line on what it gives.
- **During first setup** (a step in the profile's `setup:` is still open — not `done`, `skipped` or `not needed`): option 1 is the current setup step, and the setup footer from `navigator` ("First setup checklist") goes under the options — step N of 12, what is done, now, next.
- Things that need no decision (logging, monitoring, saving to the base) are done automatically, not offered.
- **0 — menu (№26):** the last option is always "**0** — menu of all functions". If something is paused (`paused:` in the profile: a day-plan task, a setup step, a draft), option 1 is "**back** to <it>". Never make an option a condition ("first publish…") — every option is an offer.
- **Mark tried:** on this skill's first real run in the session, add or update its line under `tried:` in `parasite-seo-profile.md` (`- <skill> · YYYY-MM-DD · <what, 3–6 words>`; agents too, marked `agent`). When the user seems lost or asks what else there is, add: "All PARASITER functions: say **help**."

Options that usually fit after this part (adapt to the user's products and words):
- After a candidate list, option 1 is always the choice itself: "1, 3" — take these platforms (see Step 5)
- "analyze <platform>" — score one before posting
- "what should I write there?"
- "add it to my platforms"

Part of PARASITER by Rumer (Affiliate Credo).

Platforms live days to months: they get spammed, cleaned up, noindexed or close registration. A list is only worth something if it is **fresh and checked**.

**What we look for:** not new, untested platforms, but the ones where **affiliate review pages are published and indexed right now**. If review pages of affiliate products rank on a domain today, it is a proven parasite platform: anyone can post there and Google keeps the pages. A platform with no affiliate posts on it is not a lead, however promising it looks. Whether links on it are indexed or followed does not matter — what matters is that **the pages themselves are indexed**.

**Free and paid are always separate.** Free: platforms where users post themselves (Facebook, Reddit, Quora, forums, article and document platforms, site builders, podcasts, Gamma…). Paid: news and media sites (all of them are paid — sponsored posts, "partner content", press releases), PR wires, paid placements. Every list shows them in separate tables.

**The user picks the platforms, not PARASITER.** A goal says *how many* platforms (for example 2 in the first week, 10 by the end), never *which*. This skill shows candidates, may star the ones it recommends with the reason, and the user chooses by number. Never say "post here" about a platform the user has not chosen.

**Never shown:** stop types and blacklisted sites (`references/exclusions.md`, the live list comes from the server), platforms whose example pages are removed, and the author's own posts as examples (filtered by the server). The author's private platforms are never named, not even as "skipped".

Reply in the user's language.

## Step 0 — Plan check (Pro)

**Step 0 — Plan check.** Call `account_info` once per session (reuse it if already called).
- **Pro or Insider, active** → proceed to Step 1.
- **Free with a key** (`plan: free` and the tools `free_base` / `free_scout` are there) → **Free mode** below, not Steps 1–5.
- **No key, or an expired paid key** → one line: "Platforms come with a free key: a base of 50 checked platforms and 3 platform scans a week for your product. Get it by email (no card): https://parasiter.affiliatecredo.com/free.html — then reinstall the plugin and paste the key when it asks." Then offer what works right now (the ready Google queries to run yourself ("<product> review", "<product> forum") and what to look for on each result — say "give me the search queries"; or score a platform you already found by hand with the checklist from the analyzer), and stop. An expired Pro / Insider key gets the same line plus the renewal link from `account_info`.

## Free mode (Free plan with a key)

Free gets two things from the server. Both are real value, and both show clearly what Pro adds — never hide that line, never push harder than one line.

**A. "Show the free platform base" / "where can I publish?" without a product** → `free_base` (filters `type`, `language`, `query` from the user's words).
```
Free platform base · snapshot of N checked platforms (of M in Pro)
Each status is as of its check date — check a platform yourself before you invest in it.
| # | Platform | Type | Language | Status | Checked | Sign-up |
```
- No example posts on Free (the server sends none — never invent them). Mark platforms already in the user's base "yours".
- Under the table, one line: "Pro: the whole checked base with live example posts on every platform, new platforms every week (Insider the same day) and what is alive today — https://parasiter.affiliatecredo.com/#pricing".
- Then the choice as in Step 5 ("Which ones do we take? Reply with numbers") and save the chosen ones the same way. The analyzer checklist works on any of them.

**B. "Where do reviews of <product> rank?" / "find platforms for <product>"** → a scan with the `platform-scout` agent (web search, no DataForSEO, nothing paid):
1. **One product per scan.** If the user named several, ask which one first (or take the first and say so).
2. Call `free_scout(action="start", product=…)` **before** the agent. `allowed: false` → do not scan; say how many scans the week has, that they open again on Monday, and what Pro gives (one line), then offer the free base (A). `allowed: true` → say "Scan N of 3 this week" in one line.
3. Run `platform-scout` for that one product with the exclusions (`exclusions_get` works on the Free key), the live check and the sign-up lookup as usual; pass example URLs through `examples_filter`; send dead domains with `dead_report`.
4. **Show the top 3 platforms in full** (live posts first, by the number of products with reviews there and the best position) in the Step 5 format. **The rest only as a count:** "+N more platforms found for <product> — the full list, more example posts and the checked base are in Pro: https://parasiter.affiliatecredo.com/#pricing". Never name the others, not even in later replies of the same session; if the user asks for them, say they are in Pro.
5. The choice and saving as in Step 5 (only the 3 shown).

`free_scout(action="status")` answers "how many scans do I have left?". Other Pro tools return `paid_plan_only` on a Free key: say in one line it is Pro and continue with what Free has.

## Exclusions and the private filter (every step)

- **Exclusions.** With a PARASITER key, call `exclusions_get` once per session and save the answer as `exclusions.json` (pass it to `platformscan.py --exclusions exclusions.json`). Without a key or if the tool fails, use `references/exclusions.md` (the script always reads it). Apply the same list to the author's base, to web-search results and to `platform-scout`'s results: a match is never shown or checked, only counted as "skipped by stop / black list: N". Domains in `dead` are skipped before any paid scan or check. The user's own exclusions (profile) go in with `--exclude domain[/path],…`.
- **PDFs are allowed** as normal findings (type "document / PDF", the PDF's host is the platform), except abuse: PDFs in other organisations' upload folders and PDFs on S3.
- **Example posts** shown to the user must pass `examples_filter` when a key is connected (the server hides posts by the author — his accounts, topics, products). If a platform has no example left, show it without one: "example: find your own with \"[product] review\"". Without a key, show the examples as found.
- **Dead platforms found by a scan** (`platforms-scan-dead.txt`) are sent with `dead_report(domains)` when a key is connected — domain and date only, nothing about the user. Do it automatically and mention it in one line.

## Agency role — brand-safe platforms for a client

For a client the question is the same — where do pages rank now — with three changes:
- **Probe the client's niche, not affiliate products:** "best [category]", "[category] review", "[competitor] alternatives", "[competitor] vs", "how to choose [category]" for the client's target queries, plus "[competitor] review" for 5–10 competitors (`platformscan.py` with those terms and `--suffix ""` / your own suffixes, `--base clients/<slug>/parasite-seo-progress.csv` so the client's platforms are marked). Platforms where the category's pages rank are the client's candidates.
- **Brand-safe filter:** keep platforms whose rules allow declared brand or company content (LinkedIn, Medium, YouTube, Gamma, podcast hosts, document hosts, industry communities with brand accounts, Reddit / Quora only where the community allows brand participation). Drop or mark "not for brands" places full of spam, adult or gambling neighbours, or whose rules forbid promotion. Mark each row brand-safe yes / with conditions / no.
- **The client's own profiles first** (from `brand-presence`): a platform where the brand already has a complete profile is the cheapest place to start.
Read and write the client's platform base (`clients/<slug>/parasite-seo-progress.csv` → `parasite-seo-platforms.csv`). Paid placements (news sites, PR wires) go to the client as an option with a known price only — the client decides on paid media.

## Site owner role — links matter

For an affiliate a link's rel doesn't matter (only the page's indexing does). For a site owner it does: every candidate platform is marked **dofollow / nofollow / ugc / sponsored** for links to their site (check a recent post's link in the page source), and dofollow platforms with indexed pages come first for link building. Probe the site's category like the agency mode above. Paid platforms (news sites, press-release wires, sponsored-article marketplaces) go to `paid-placements`, which keeps their prices, packages and how to order.

## Step 1 — Filters

Ask only what is missing:
- Niche and the user's products (from the links library) or the products to probe.
- Language and country.
- Free only, paid only, or both.
- Read the user's base (`work-log` `platforms`): platforms already in it are marked "yours" with their state; `dropped` and `dead` are skipped unless asked.

## Step 2 — The author's base first (Pro / Insider)

If `platforms_search` is available, call it with the filters. These are platforms Rumer checked by hand; he adds them every Monday and often in between, several a day. Pro sees them ~7 days after they are added, Insider the same day. Each row carries `examples` (live posts, best position first, already filtered) and `signup_url`. Drop rows that match the exclusions, then show them post-first in the Step 5 format and keep the server's notes as written.

If the server is not connected, say once: "Checked platforms from Rumer come with a Pro key. Meanwhile we can run a live scan." and go to Step 3.

## Step 3 — Live scan: where reviews of affiliate products are published now

**The live scan is paid** (the user's DataForSEO balance) — always say so before running it, with the number of products and the rough cost, and run it only after a yes (`work-log` Rules: paid checks).

1. **Products to probe** — `references/products-seed.md`: the user's own products first, then the current top of the marketplaces in their niche (ClickBank, Digistore24, BuyGoods…), the seed list only as a fallback. 20–50 names is a good scan.
2. **Scan** — every affiliate review page has the same two words: *[product name] review*. Search them and collect every result that is not the product's own site or a store:
   ```
   python3 scripts/platformscan.py products.txt --country us --dry-run   # the cost first (top 10 by default)
   python3 scripts/platformscan.py products.txt --country us --base parasite-seo-progress.csv
   ```
   **With a PARASITER key** run it in two steps so the author's posts never reach the user:
   ```
   python3 scripts/platformscan.py products.txt --country us --exclusions exclusions.json --collect-only
   # examples_filter(urls from platforms-scan.examples.txt) → save {"allowed": [...]} as allowed.json
   python3 scripts/platformscan.py --from-raw platforms-scan.raw.json --allowed allowed.json --exclusions exclusions.json --base parasite-seo-progress.csv
   ```
   After the paid search everything is free: excluded and known-dead domains are dropped and counted; up to 3 example pages per platform are **opened live** (404/410, "page removed" text, redirect to the home or login page, empty page, noindex meta or X-Robots-Tag = removed) and a platform passes only if at least one example is alive; a sign-up link is looked up (home page, /register, /signup, /join, /user/register, /create-account…) and opened to check it works, otherwise "sign-up link not found" + the home page.
   Output: the summary line **"found N platforms · live M · removed K · skipped by stop / black list L"**, then **Free / Paid / To check** tables post-first: `Post · Product · Pos. · Platform · Type · Free/Paid · Sign-up` (best post first, 1–2 more under it); then "in Google, but the pages are removed: …" (never in the working list) and platforms that could not be verified automatically. Saved as `platforms-scan.csv`, dead domains in `platforms-scan-dead.txt` (send with `dead_report`). `--suffix reviews` / `complaints` for other probes; `--device mobile` for the mobile SERP; `--self-test` checks the script offline.
3. **Without an API** — the same probe with web search or the `platform-scout` agent (free, but far fewer results and no positions), with the same exclusions, live check and sign-up lookup; or give the user the queries to run in Google (incognito, target country).
4. **Similar to what works** — the author's archive of platforms that ranked in 2025–2026 (on the server) shows which kinds of places are worth it: the scan's "To check" domains of the same kind (document hosts, community projects, notebooks, podcast hosts, site builders) come first.

A platform with review pages of **many different products** is the strongest lead: it is where everyone posts and Google keeps it.

## Step 4 — Quick check of the top candidates (free)

The scan already opened the examples and looked for the sign-up page. For the top 5–10 "free" and "to check" platforms add (details in `platform-analyzer`):
- Can a new user register and post the same kind of page (the sign-up link opens; invite, phone or paid plan?)
- Are fresh posts indexed (check one recent one)?
- Moderation and signs of cleanup (several removed examples, login wall, noindex)?

A platform with no live example is never a candidate. Mark uncertain ones "test".

## Step 5 — Candidates: the user chooses

Show **5–10 candidates** when there are that many (free and paid in separate tables), numbered, post-first:

```
Platform candidates · [niche] · [country] · checked [date]
Found N · live M · removed K · skipped by stop / black list L
Free
| # | Post (live example) | Product | Pos. | Platform | Type | Free/Paid | Score | Indexing | Moderation | Pros / risks | Sign-up |
Paid
| # | Post | Product | Pos. | Platform | Type | Price / how to buy (if known) | Sign-up / contact |
Already in your base: [platforms from the user's base that fit, with their state and priority]
```
- **Score** = the `platform-analyzer` score 0–100 if there is one (server or the user's base), otherwise "not checked". Indexing speed and moderation from the server, the analyzer or the quick check; "unknown" when not checked. Pros / risks in a few words each.
- **Sign-up** = the checked sign-up link, or "sign-up link not found" + the home page.
- **Post** = a live, filtered example; if none is left after the filter: "example: find your own with \"[product] review\"".
- You may star recommended ones: "★ I'd start with #1 and #3 — [why, one line each]". A star is advice, not a decision; never drop the others or pick for the user, even when a goal says how many platforms are needed this week ("your goal this week: 2 platforms — pick any 2").
- Paid ones only with what is known about the price; never guess a price.
- **Few candidates** (fewer than 5): say exactly how many were found and why (for example: the author's base is still empty on your plan, no DataForSEO key, the niche is narrow) and how to get more — a live DataForSEO scan with more products, the feed (on Pro new platforms arrive ~7 days after the author adds them, on Insider the same day), other probes (`--suffix reviews`, `complaints`). Never narrow the list silently.

End the list with: **"Which ones do we take? Reply with numbers (e.g. 1, 3)"** — this is option 1 of the Next steps block.

**Saving the choice.** When the user replies with numbers, save each chosen platform in their platform base as a priority platform (work-log): `platform-set --platform <slug> --domain <domain> --type <type> --state testing --priority high --note "chosen <date> from candidates; sign-up: <link or not found>"` (add `--score NN` when known; for a platform already in the base keep its state and only set `--priority high`). Not-chosen candidates are not written. Confirm in one line ("Saved as your priority platforms: …") — the navigator builds the day plan only from chosen platforms. Then offer `platform-analyzer` on the first chosen one, or writing the first post there.

## Rules

- **Legal products and content only.** PARASITER works only with legal products and content. Don't write, plan, find platforms for or log pages that promote pirated software, films, books or courses, file-upload / download or "free download" schemes, cracks and keygens, counterfeit or illegal goods, or content that breaks the target platform's rules or the law of the target country. Say so in one line, without lecturing, and offer a legal alternative (the official product or a legal affiliate offer). This rule is part of the PARASITER offer the user accepted.
- Only platforms where the user can legitimately create an account and post, or buy a placement. Reviews found in other organisations' upload folders or forms (university and government sites, `wp-content/uploads`, contact-form files) are hacked or abused sites: the scan skips them and they are never suggested — they are not platforms, they are abuse, and they burn domains and offers.
- Spread across platforms; never rely on one.
- Every list is a snapshot: write the check date on it.
- Reference: the author's archive of domains that ranked in 2025–2026 lives on the server (history, not live status).
