---
name: platform-finder
description: Find platforms where a parasite SEO page can be published and rank — forums, communities, Q&A, article and profile platforms, document hosts, flipbooks, podcasts, site builders, event, job and fundraising pages — filtered by niche, language, link rules, indexing speed and moderation; and search NEW platforms by category with Rumer's patterns (two-level menu of 6 groups and 27 categories, platforms where affiliates already post and clean ones with no competitors yet). Use when the user asks where to publish, wants new platforms, forums or communities for a niche, a list of platforms that work now, "find new platforms", "find forums / flipbooks / job sites / podcasts…", or "platforms with no competitors".
---

# Platform Finder

## Work label (testing period)

Start every reply produced by this skill with one line naming it, so the user always sees which part of PARASITER is working:
`▸ PARASITER · platform-finder`
If you called agents for this reply, add them after an arrow: `▸ PARASITER · platform-finder → serp-analyst, product-researcher`. If you hand off to another skill, the next reply carries that skill's label. One line only, no other system talk.

## Show what the next plan opens — RULE (№56)

No key or Free key: every result in Free mode, the category menu (groups 1–6 marked 🔒 Pro) and the locked pattern search follow `navigator/references/upgrade-showcase.md` — the locked card when a Pro part is opened, and under each Free result the "On Pro / Insider" block (full base with example posts, no weekly limit, 27 patterns, 0–100 scores, Top-10; Insider — same-day platforms). Pro user: one Insider line.

## Plugin basis and Claude plan — RULE (№33)

Every answer here is PARASITER at work: this skill's steps, Rumer's rules, criteria and references — never general knowledge alone. Name the basis briefly where it matters ("by Rumer's rules", the checklist, score or reference used, "PARASITER platform base"). A request this skill doesn't cover → the right skill; nothing fits → one line "outside PARASITER's skills — I answer by Rumer's general rules", then "0 — menu". Full rule: `navigator/references/agents-and-plan.md`.

**Agents and Claude plan.** Heavy step: the live platform search for the user's products → agent `platform-scout`. Mode: `agents:` in `parasite-seo-profile.md`, else `agents_default` from `account_info`.
- `on` (Claude Max, Team) → run the agent; label `▸ PARASITER · <skill> → platform-scout`.
- `lite` (Claude Pro) → the **Lite version** below, label `▸ PARASITER · <skill> · Lite`. When the full version would clearly give a better result here, add one line of advice — why, and the phrase **full** ("For 20 products the full version is better: platform-scout checks every one, about 3–5× more of your Claude limits. Say **full** — or I keep Lite").
- `offer` (plan not known) → ask once before the first run: "This step of the skill is done by PARASITER's platform-scout agent: separate context, deeper, uses more of your Claude limits (best on Max). Run it? Or Lite with the same skill."
- "full" / "audit by agent" → run it this time; "turn on agents" → `agents: on`; "save limits" or a usage limit hit → `agents: lite` (save in the profile, advice from `agents-and-plan.md` §3).

**Lite version:** up to 5 products (the result still shows the full list of what was found and the search source line, Step 5): the checked base (`platforms_search`; Free key: `free_base`) plus one "[product] review" search each, no live sign-up / indexing check of every platform. A Free key still calls `free_scout` start before any search, Lite or full. Lite is the same method in a smaller scope: say what was left out.

## Next steps (end of every reply)

The user must always know what to type next. End every reply with a short numbered block — ready phrases, not skill names:

**What's next? Reply with a number or the phrase:**
1. "<ready phrase>" — <what happens after it, a few words>
2. "<ready phrase>" — <what happens>

- 2–3 options that fit what just happened, the recommended next step first. "1", "yes", "ok", "go" means option 1. Any free wording of the same wish works too ("give me the offers").
- Each option is a complete phrase in the user's working language that they can copy, plus what it does. Never show skill or agent names here: the work label at the top already names the part that is working.
- Offer only what the user's plan includes (`account_info`, once per session). On a lower plan the last option before "0" is always one locked feature of the next plan that fits this step, marked "🔒 Pro" or "🔒 Insider" with what it gives (`navigator/references/upgrade-showcase.md`, №56).
- **During first setup** (a step in the profile's `setup:` is still open — not `done`, `skipped` or `not needed`): option 1 is the current setup step, and the setup footer from `navigator` ("First setup checklist") goes under the options — step N of 12, what is done, now, next.
- Things that need no decision (logging, monitoring, saving to the base) are done automatically, not offered.
- **0 — menu (№26):** the last option is always "**0** — menu of all functions". If something is paused (`paused:` in the profile: a day-plan task, a setup step, a draft), option 1 is "**back** to <it>". Never make an option a condition ("first publish…") — every option is an offer.
- **Mark tried:** on this skill's first real run in the session, add or update its line under `tried:` in `parasite-seo-profile.md` (`- <skill> · YYYY-MM-DD · <what, 3–6 words>`; agents too, marked `agent`). When the user seems lost or asks what else there is, add: "All PARASITER functions: say **help**."

Options that usually fit after this part (adapt to the user's products and words):
- After a candidate list, option 1 is always the choice itself: "1, 3" — take these platforms (see Step 5)
- "find new <category>" — a pattern search in another category (e.g. "find new flipbooks")
- "analyze <platform>" — score one before posting
- "what should I write there?"
- "add it to my platforms"

Part of PARASITER by Rumer (Affiliate Credo).

Platforms live days to months: they get spammed, cleaned up, noindexed or close registration. A list is only worth something if it is **fresh and checked**.

**Start with the category menu.** Any request to find platforms — "find platforms", "find new platforms", "найди площадки", "where can I publish", with or without a product or niche — opens the **Pattern search menu** first (next section): 6 groups → their categories → the search. The menu also has item **7 — where reviews of my product rank now**, which runs Steps 1–5 below (the checked base and the live "[product] review" scan). Skip the menu only when the user already named a category ("find flipbooks" → that category) or asked exactly where reviews of a named product rank now ("where do reviews of X rank" → Steps 1–5). When the navigator sends here for platforms the day plan needs, it also opens the menu. On a Free key or with no key, the menu still shows in full: groups 1–6 marked "🔒 Pro", each category listed (never hidden); choosing one gives the locked card (below, №56) and item 7 works.

**What we look for in Steps 1–5:** not new, untested platforms, but the ones where **affiliate review pages are published and indexed right now**. If review pages of affiliate products rank on a domain today, it is a proven parasite platform: anyone can post there and Google keeps the pages. A platform with no affiliate posts on it is not a lead, however promising it looks. Whether links on it are indexed or followed does not matter — what matters is that **the pages themselves are indexed**.

**Free and paid are always separate.** Free: platforms where users post themselves (Facebook, Reddit, Quora, forums, article and document platforms, site builders, podcasts, Gamma…). Paid: news and media sites (all of them are paid — sponsored posts, "partner content", press releases), PR wires, paid placements. Every list shows them in separate tables.

**The user picks the platforms, not PARASITER.** A goal says *how many* platforms (for example 2 in the first week, 10 by the end), never *which*. This skill shows candidates, may star the ones it recommends with the reason, and the user chooses by number. Never say "post here" about a platform the user has not chosen.

**Never shown:** stop types and blacklisted sites (`references/exclusions.md`, the live list comes from the server), platforms whose example pages are removed, and the author's own posts as examples (filtered by the server). The author's private platforms are never named, not even as "skipped".

Reply in the user's language.

## Step 0 — Plan check (Pro)

**Step 0 — Plan check.** Call `account_info` once per session (reuse it if already called).
- **Pro or Insider, active** → proceed to Step 1.
- **Free with a key** (`plan: free` and the tools `free_base` / `free_scout` are there) → **Free mode** below, not Steps 1–5.
- **No key, or an expired paid key** → one line: "Platforms come with a free key: a base of 50 checked platforms, 3 platform scans a week for your product and a journal for 10 pages with checks. Get it by email (no card): https://parasiter.affiliatecredo.com/free.html — then reinstall the plugin and paste the key when it asks." Then offer what works right now (the ready Google queries to run yourself ("<product> review", "<product> forum") and what to look for on each result — say "give me the search queries"; or score a platform you already found by hand with the checklist from the analyzer), and stop. An expired Pro / Insider key gets the same line plus the renewal link from `account_info`.

## Free mode (Free plan with a key)

Free gets two things from the server. Both are real value, and both show clearly what Pro and Insider add: under every Free result the "🔒 On Pro / Insider" block (№56, `navigator/references/upgrade-showcase.md` §3) — one block per reply, after the result, never instead of it.

**A. "Show the free platform base" / "where can I publish?" without a product** → `free_base` (filters `type`, `language`, `query` from the user's words).
```
Free platform base · snapshot of N checked platforms (of M in Pro)
Each status is as of its check date — check a platform yourself before you invest in it.
| # | Platform | Type | Language | Status | Checked | Sign-up |
```
- No example posts on Free (the server sends none — never invent them). Mark platforms already in the user's base "yours".
- Under the table, one line: "Pro: the whole checked base with live example posts on every platform, new platforms every week (Insider the same day) and what is alive today — https://parasiter.affiliatecredo.com/?utm_source=plugin&utm_medium=upgrade&utm_campaign=platform-finder#pricing".
- Then the choice as in Step 5 ("Which ones do we take? Reply with numbers") and save the chosen ones the same way. The analyzer checklist works on any of them.

**B. "Where do reviews of <product> rank?" / "find platforms for <product>"** → a scan with the `platform-scout` agent (web search, no DataForSEO, nothing paid):
1. **One product per scan.** If the user named several, ask which one first (or take the first and say so).
2. Call `free_scout(action="start", product=…)` **before** the agent. `allowed: false` → do not scan; say how many scans the week has, that they open again on Monday, and what Pro gives (one line), then offer the free base (A). `allowed: true` → say "Scan N of 3 this week" in one line.
3. Run `platform-scout` for that one product with the exclusions (`exclusions_get` works on the Free key), the live check and the sign-up lookup as usual; hide the author's posts locally with `privfilter.py` (see the private filter below). Nothing found is sent anywhere.
4. **Show the top 3 platforms in full** (live posts first, by the number of products with reviews there and the best position) in the Step 5 format. **The rest only as a count:** "+N more platforms found for <product> — the full list, more example posts and the checked base are in Pro: https://parasiter.affiliatecredo.com/?utm_source=plugin&utm_medium=upgrade&utm_campaign=platform-finder#pricing". Never name the others, not even in later replies of the same session; if the user asks for them, say they are in Pro.
5. The choice and saving as in Step 5 (only the 3 shown).

`free_scout(action="status")` answers "how many scans do I have left?". Other Pro tools return `paid_plan_only` on a Free key: the locked card (№56 §2) for that feature, then continue with what Free has.

## Exclusions and the private filter (every step)

- **Exclusions.** With a PARASITER key, call `exclusions_get` once per session and save the answer as `exclusions.json` (pass it to `platformscan.py --exclusions exclusions.json`). Without a key or if the tool fails, use `references/exclusions.md` (the script always reads it). Apply the same list to the author's base, to web-search results and to `platform-scout`'s results: a match is never shown or checked, only counted as "skipped by stop / black list: N". Domains in `dead` are skipped before any paid scan or check. The user's own exclusions (profile) go in with `--exclude domain[/path],…`.
- **PDFs are allowed** as normal findings (type "document / PDF", the PDF's host is the platform), except abuse: PDFs in other organisations' upload folders and PDFs on S3.
- **Your finds stay yours.** Nothing a search finds — URLs, domains, platforms, queries, products — is ever sent to the PARASITER server. New platforms the user picks go only into the user's own base (Step 5). Dead platforms a scan finds stay in the user's own `platforms-scan-dead.txt`; skip them in the user's next scans.
- **Private filter, run locally.** Example posts shown to the user must not be the author's (his accounts, profile paths, topics, platforms). With a key, call `private_hashes` once per session and save the answer as `private-hashes.json`; write the example URLs (one per line, optionally `URL<TAB>product`) to a file and run `python3 scripts/privfilter.py private-hashes.json examples.txt --out allowed.json`; show only the allowed ones. The script only hashes on the user's machine — no URL leaves it. If a platform has no example left, show it without one: "example: find your own with \"[product] review\"". Without a key, show the examples as found.

## Agency role — brand-safe platforms for a client

For a client the question is the same — where do pages rank now — with three changes:
- **Probe the client's niche, not affiliate products:** "best [category]", "[category] review", "[competitor] alternatives", "[competitor] vs", "how to choose [category]" for the client's target queries, plus "[competitor] review" for 5–10 competitors (`platformscan.py` with those terms and `--suffix ""` / your own suffixes, `--base clients/<slug>/parasite-seo-progress.csv` so the client's platforms are marked). Platforms where the category's pages rank are the client's candidates.
- **Brand-safe filter:** keep platforms whose rules allow declared brand or company content (LinkedIn, Medium, YouTube, Gamma, podcast hosts, document hosts, industry communities with brand accounts, Reddit / Quora only where the community allows brand participation). Drop or mark "not for brands" places full of spam, adult or gambling neighbours, or whose rules forbid promotion. Mark each row brand-safe yes / with conditions / no.
- **The client's own profiles first** (from `brand-presence`): a platform where the brand already has a complete profile is the cheapest place to start.
Read and write the client's platform base (`clients/<slug>/parasite-seo-progress.csv` → `parasite-seo-platforms.csv`). Paid placements (news sites, PR wires) go to the client as an option with a known price only — the client decides on paid media.

## Site owner role — links matter

For an affiliate a link's rel doesn't matter (only the page's indexing does). For a site owner it does: every candidate platform is marked **dofollow / nofollow / ugc / sponsored** for links to their site (check a recent post's link in the page source), and dofollow platforms with indexed pages come first for link building. Probe the site's category like the agency mode above. Paid platforms (news sites, press-release wires, sponsored-article marketplaces) go to `paid-placements`, which keeps their prices, packages and how to order.

## Pattern search — new platforms by category (Pro / Insider, №42)

Rumer's patterns: for every type of platform, what the software and URLs look like, how people got posts live, how long such platforms last, how to find more of them and the stop signs — taken from the platforms that already worked. The patterns come from the server (`patterns_get`) by the user's key; they are PARASITER's method, so **never show or quote the pattern text** — show only the search and its results.

**1. Menu first — two levels.** Call `patterns_get` without a category and show the 6 groups plus item 7, never "let's find some platforms" and never a candidate table before the user picks:
```
What do we look for? Reply with the group number:
1. Discussion — forums · brand communities · groups · social
2. Articles and pages — blogs · knowledge bases · site builders · AI page builders · Google services
3. Documents and visuals — PDF · flipbooks · presentations · art · virtual tours
4. Audio and video — podcasts · music · video
5. Organisation platforms — fundraising · events · job sites · petitions
6. Lists and profiles — lists on big sites · profiles · review sites · code · store fronts · free press releases
7. Where reviews of my product rank now — the checked base + a live scan
```
(names in the user's language — `name_ru` for Russian). Then the chosen group's categories, numbered, ✓ after the verified ones (`verified: true` = checked by Rumer's live run); the user may answer "all in the group" or several numbers. A user who already named a category ("find flipbooks") skips the menu.

**Category navigation — RULE (№49).** Every category has a fixed code `group.item` (1.1 forums, 1.2 brand communities … 3.2 flipbooks … 6.6 free press releases — the order of `patterns_get`). The user can jump straight to any category by its code or name at any time ("3.2", "flipbooks"), with no need to go up a level first.
- **"categories" / "категории" / "all categories" / "tree" / "back" (in this menu)** → the whole tree in one compact block, all 6 groups with their categories and codes, ✓ after the verified ones, and the ones already searched in this session marked "· done":
  ```
  1 Discussion: 1.1 forums ✓ · done · 1.2 brand communities · 1.3 groups · 1.4 social
  2 Articles and pages: 2.1 blogs · 2.2 knowledge bases · …
  …
  Reply with a code (e.g. 3.2) or several (2.1, 3.2).
  ```
- **After every category result**, the Next steps start with: **"1 — next category in <group>: <the group's other codes and names, one line>"** · **"2 — all categories (the tree)"** · then the usual choice of platforms by numbers and **0 — menu**. Never make the user climb back to the group list to see what else there is.

**2. One question:** niche or offer, language / country, forum topic if it matters — "or say skip". Then `patterns_get(category)` for every chosen category.

**2a. Volume and source — RULE (№50).** Before the first search of a category, in the same message as the question above or right after it, the user chooses how much to find and with what. Never pick for them and never fall back to Lite silently: a skipped choice means the default below, said in one line.

**Known empty — RULE (№54).** Before offering the sources, check what earlier runs of this category found with each source: the pattern's own test notes from `patterns_get` (`verified`, test results) and the user's `pattern-runs.csv` (written in 5a). If a source already returned **0 platforms** for this category, say it in the same message, before anything runs: "Earlier free live searches in <code name> found nothing (checked <date>). More likely to find: <SerpApi / DataForSEO footprint search, if connected> · or the nearest categories that did return platforms: <2–3 codes and names>." Mark that source "(found 0 before)" in the list below. Run it only if the user still picks it.

First, silently, check both SEO accounts: `serpapi_status` (plan, searches per month, searches left) and `dataforseo_status` (balance). Then:
```
How many platforms do we start with?
1. 10   2. 20   3. 30   4. as many as the search finds
Source (free first):
A. Live search — built-in web search by Rumer's pattern (free, uses Claude limits)
B. SerpApi — footprint search in real Google · plan <Free/…> · <left> of <per month> searches left this month · this batch ≈ N searches
C. DataForSEO — footprint search in Google · balance $<balance> · this batch ~$X
D. Everything — A, then B on the searches left, then C only for what is still missing (~$X at most)
```
- **Free first — RULE (№51).** Order of use: A (free) → SerpApi searches still left this month (free plan or already paid plan) → paid: DataForSEO or more SerpApi (a paid SerpApi plan on the same key). Never spend DataForSEO money while SerpApi searches are left, unless the user picks C. When SerpApi runs out mid-batch, stop and ask: "SerpApi: 0 searches left (resets on <date>). Go on with DataForSEO (~$X), upgrade SerpApi (serpapi.com/pricing, same key), or stop here?".
- **Not connected → ask to connect, each one once per session.** SerpApi missing → "B needs a SerpApi key: free plan 250 searches a month, no card — sign up at https://serpapi.com/users/sign_up → copy the key at serpapi.com/manage-api-key → /plugin → PARASITER → Configure options → SerpApi API key → restart Claude Code." DataForSEO missing → "C needs your DataForSEO login and password — app.dataforseo.com → API Access → /plugin → PARASITER → Configure options." Show only the lines that are missing; the options that work stay in the list. Never ask for a key in the chat.
- A key is set but the status call fails (wrong key, 401, can't reach) → one line with the status message, then go on with what works.
- **Default** when the user skips: `agents: on` (Max, Team) → 10 + A with the agent, plus B when SerpApi has searches left (free); `lite` (Pro) → 10 + A in Lite, plus the one-line **full** advice. The profile's `agents: lite` while `account_info` says `claude_plan: max` → one line "Your profile says Lite, your account says Max — I run full; say **save limits** to keep Lite", and set `agents: on`.
- The size of B and the cost of C are always the `--dry-run` figures, shown before the run; B runs after a yes for that number of searches, C after a yes for that amount.
- **How B and C run:** the pattern's method B footprints become one ready Google query per line (`queries.txt`), then `platformscan` with `--suffix ""` through `serpapi_run` (B) or `dataforseo_run` (C), `--dry-run` first: SerpApi costs 1 search per query per 10 results (keep `--depth 10` unless the user asks for more). Results go through the same exclusions, live check and sign-up lookup as every scan, then 4–5a below.

**3. Search strictly by the pattern** — its Find section (method A: current products + "reviews 2026" + the platform's names or page words in the built-in web search; method B: the footprints in real Google through the user's SerpApi — free while the monthly searches last — or DataForSEO — paid; searches or cost shown first and only after a yes, see 2a). Plan check, mode and agents as everywhere: `on` → agent `platform-scout` in **pattern mode** (pass the category, the pattern and the common rules, the exclusions, the user's base, the chosen volume and source, and the seen-list from 5a); `lite` → up to 5 queries yourself per batch, one category at a time — the link check in 4a still runs in Lite (it is page opens, not searches). The volume chosen in 2a is the target, not a cap on what the search may look at: keep searching (more products, more query variants, deeper pages) until the batch is full of platforms that passed 4a or the source runs dry — then say which.

**3a. Products to search with — RULE (№52).** Method A needs product names, and the same three every time find the same platforms. Build the product list for the user's niche before the first query: the user's own products (links library, profile) → the current hot offers from the server when `hot_offers` is available (Rumer's list) → the current top of the marketplaces in the niche (ClickBank, Digistore24, BuyGoods by gravity) → `references/products-seed.md` as the last fallback. Take 15–30 names. **Rotate:** every batch and every "next 10" uses products not used yet in this session (keep them in the seen-list), never the first names of the list again. The products used go into the search source line of the result ("Products searched: …").

**3b. Show finds as they come — RULE (№53).** The user never waits for a whole batch in silence.
- **First message within 1–2 minutes:** "Searching <category>: N candidates found, checking them now." — then each platform appears **the moment it passes 4a**, as its own short message: the Step 5 row for that one platform with a counter ("3 of 10 · checked"). Use `SendUserMessage` for these when the tool is there.
- **How:** search the candidates first (queries in the main chat or one quick agent run that only collects candidates), then check them in **small parallel agents** — `platform-scout` in check mode with 1–2 candidates each, run in the background — and show each result as soon as its agent returns. In Lite (no agents) check one candidate at a time in the chat and show each as soon as it passes.
- Unchecked candidates are never shown as platforms; one line is enough: "in check: 4 · dropped so far: 2 (sign-up closed, posts removed)".
- No platform passed after 2–3 minutes → say what is going on (candidates, dropped and why), never "the list isn't ready yet".
- "where is the list" / "show what you have" → show every platform that passed so far at once, then keep going.
- After the last one: the full batch table (Step 5 format) once, the dropped count with reasons, and the 5a line.

**4. Two tracks in every result:**
- **Follow** — affiliate posts are already there: the date of the newest one and the wave — **live** (≤14 days) · **fading** (15–60 days: check that sign-up is open, not "old accounts only") · **closed** (>60 days or sign-up closed: not in the working list, one line "old posts still there, no new ones").
- **Clean** — the pattern's good signs, open sign-up, no affiliate posts yet: "clean — no competitors". Give the test plan: register as a normal user → a neutral post on the site's topic → the review 2–3 days later → check indexing. Say the risk plainly: moderation may be absent or manual, the first post shows.

**4a. Open every link before showing it — in every mode, Lite included (plain page fetches, free).** For each candidate:
- **Home** — the platform's root or the forum's index / the section where posts go. Open it: it must load.
- **Sign-up** — the direct register / sign-up / create-account page (look for the link on the home page, else try /register, /signup, /join, /user/register, /create-account, /users/sign_up, /login?register, /member/register). Open it and confirm a sign-up form loads. Not found → "sign-up link not found — use Home".
- **Live example** — each affiliate post you found: 404 / 410, "page not found / removed / deleted", redirect to the home or a login page, an empty page or noindex = **removed**. Show an example **only if it opens and the post is there**; never print a removed example as a link — not in the table, not under "Sources". All examples removed → the platform cleans up: say "posts removed (cleanup on [date checked])", move it to **fading** with "check that new posts stay"; when the home or sign-up is also gone, it is dead — leave it out of the working list. A site that blocks the check → "could not verify — open by hand", never "live".

**5. Output** — one row per platform, the user should be able to act from the row without searching:
```
New platforms · [category] · [niche, language] · checked [date] · by Rumer's pattern · links opened [date]
| # | Platform | Home | Sign-up | Live example (only if it opens) | Software | Topic · language | Affiliates (newest post / clean) | Wave | Indexing | Filters | Verdict |
```
Home and Sign-up are clickable links in every row. The "Live example" cell is a link only for a post that opened; otherwise "none live" or "clean — no posts yet". Under the table no list of example links that were not checked.
Order: follow with a live wave → clean → fading ("check"). Closed ones only as a count line. Same exclusions and the local private filter as in every step; the author's private platforms are never named. ★ up to 3 with the reason; the user chooses by numbers and the choice is saved as in Step 5 (state `testing`). Never register or post for the user.

**5a. Batches — the user reviews and decides what comes next.** Results come in batches of the size chosen in 2a (10 by default); numbering continues across batches (11, 12 …) so picks stay unambiguous.
- Only platforms that passed 4a fill a batch: removed examples, dead homes and closed sign-ups are dropped before showing and do not count toward the 10; say in one line how many were dropped.
- Keep a **seen-list** for the session (platform domains already shown, picked or dropped, plus the user's base): never show a platform twice, across batches or categories.
- Under every batch, before the Next steps, one line:
  "Pick numbers to save (e.g. 2, 5, 7) · **next 10** — live search, free · **next 10 with SerpApi** — ≈N searches, <left> left · **next 10 with DataForSEO** — ~$X · **stop**"
  (the SerpApi and DataForSEO options only when they are configured; SerpApi first while it has searches left; figures from `--dry-run` for that batch and the latest `serpapi_status`). Picks and "next" can come in one reply ("3, 8 — next 10").
- When a source runs dry, say so plainly ("live search found nothing new after N queries") and offer the other source or the next category — never pad the batch with unchecked or closed platforms.
- **Empty batch — RULE (№55).** A batch with 0 platforms never ends with "next 10" on the same source. Say plainly: "<source> found no platforms in <code name> after N queries (products: …)." Then the Next steps: 1 — the next category in the group (codes, one line) · 2 — all categories · 3 — the same category with SerpApi / DataForSEO (searches or cost from `--dry-run`, only if connected; else how to connect, one line) · 0 — menu. Two empty batches in a row on a source → that category is marked "· empty (<source>)" in the tree for the rest of the session and not offered again with that source.
- **Run log.** After every batch, add a line to `pattern-runs.csv` in the user's folder: `date,category,source,queries,products,found,passed` (create it with this header if missing). It feeds the №54 warning next time. Local only, never sent anywhere.

**6. Nothing is sent.** The finds stay with the user: the ones they pick go into their own base (Step 5), the rest stay in this chat. A category whose search found nothing: say that the built-in search showed nothing and offer method B — SerpApi first while it has free searches ("footprint search in Google with your SerpApi — ≈N searches, <left> left this month"), then DataForSEO ("about $X") — instead of calling the category empty.

Free key or no key: `patterns_get` answers `paid_plan_only` — the locked card (№56 §2): "🔒 New platforms by Rumer's patterns — Pro: 27 categories, where affiliates post now and clean platforms with no competitors; Insider gets them the same day they are found: https://parasiter.affiliatecredo.com/?utm_source=plugin&utm_medium=upgrade&utm_campaign=platform-finder#pricing", then what Free has (the base snapshot, one scan). Profile says Pro or Insider but `account_info` shows no key or Free → the navigator's "key isn't connected" warning at the top (№44), never a quiet Free run.

## Step 1 — Filters

Ask only what is missing:
- Niche and the user's products (from the links library) or the products to probe.
- Language and country.
- Free only, paid only, or both.
- Read the user's base (`work-log` `platforms`): platforms already in it are marked "yours" with their state; `dropped` and `dead` are skipped unless asked.

## Step 2 — The author's base first (Pro / Insider)

If `platforms_search` is available, call it with the filters: `type` and `language` from Step 1, and the niche or product words as `query` (matched word by word against the platform and its example posts). If the answer has `query_matched: false`, no checked platform mentions the niche yet: show the base by type and language anyway with one line from `note` (most checked platforms work for any niche) — never report "0 platforms" while `total_in_your_plan` is above 0. These are platforms Rumer checked by hand; he adds them every Monday and often in between, several a day. Pro sees them ~7 days after they are added, Insider the same day. Each row carries `examples` (live posts, best position first, already filtered) and `signup_url`. Drop rows that match the exclusions, then show them post-first in the Step 5 format and keep the server's notes as written.

If the server is not connected, say once: "Checked platforms from Rumer come with a Pro key. Meanwhile we can run a live scan." and go to Step 3.

## Step 3 — Live scan: where reviews of affiliate products are published now

**The live scan uses the user's own SEO account** — SerpApi first while its monthly searches last (`serpapi_run`, script `platformscan`; 1 search per product per 10 results; free plan 250 a month), DataForSEO otherwise or when the user picks it (`dataforseo_run`, paid from the balance). Same script and args below for both: the tool adds the provider and the credentials from the plugin settings (see `work-log` Mode 9; no `serpapi_run` / `dataforseo_run` tool in this session → directory edition, see `work-log/references/directory-edition.md`). Check `serpapi_status` and `dataforseo_status`, say which account, how many searches or roughly what it costs, run `--dry-run` first and run for real only after a yes (`work-log` Rules: paid checks). A scan larger than the SerpApi searches left: offer to split it (the first N products on SerpApi, the rest on DataForSEO) or to wait for the reset date. Neither account connected → the connect lines from 2a, then item 3 below.

**Show finds as they come (№53):** the live check of the found platforms follows 3b of the pattern search — first message within 1–2 minutes, each platform shown as soon as it passes, small parallel check agents, never a silent wait for the whole list.

1. **Products to probe** — `references/products-seed.md`: the user's own products first, then Rumer's hot offers (`hot_offers`, when the server has it), then the current top of the marketplaces in their niche (ClickBank, Digistore24, BuyGoods…), the seed list only as a fallback. 20–50 names is a good scan. Rotate them as in 3a (№52).
2. **Scan** — every affiliate review page has the same two words: *[product name] review*. Search them and collect every result that is not the product's own site or a store:
   ```
   python3 scripts/platformscan.py products.txt --country us --dry-run   # the cost first (top 10 by default)
   python3 scripts/platformscan.py products.txt --country us --base parasite-seo-progress.csv
   ```
   **With a PARASITER key** run it in two steps so the author's posts never reach the user:
   ```
   python3 scripts/platformscan.py products.txt --country us --exclusions exclusions.json --collect-only
   python3 scripts/privfilter.py private-hashes.json platforms-scan.examples.txt --out allowed.json   # local, nothing is sent
   python3 scripts/platformscan.py --from-raw platforms-scan.raw.json --allowed allowed.json --exclusions exclusions.json --base parasite-seo-progress.csv
   ```
   After the paid search everything is free: excluded and known-dead domains are dropped and counted; up to 3 example pages per platform are **opened live** (404/410, "page removed" text, redirect to the home or login page, empty page, noindex meta or X-Robots-Tag = removed) and a platform passes only if at least one example is alive; a sign-up link is looked up (home page, /register, /signup, /join, /user/register, /create-account…) and opened to check it works, otherwise "sign-up link not found" + the home page.
   Output: the summary line **"found N platforms · live M · removed K · skipped by stop / black list L"**, then **Free / Paid / To check** tables post-first: `Post · Product · Pos. · Platform · Type · Free/Paid · Sign-up` (best post first, 1–2 more under it); then "in Google, but the pages are removed: …" (never in the working list) and platforms that could not be verified automatically. Saved as `platforms-scan.csv`, dead domains in `platforms-scan-dead.txt` (kept locally, skipped in the next scans). `--suffix reviews` / `complaints` for other probes; `--device mobile` for the mobile SERP; `--self-test` checks the script offline.
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

Show **every live candidate found — the full list by default** (free and paid in separate tables), numbered, post-first, best first. Never cut the list to 5–10 or to a top N and never hide the rest behind a count (the only exception is the Free key's top 3 in Free mode B). More than ~30 rows: keep the same table, compact (Pros / risks may shrink to a few words), and also save it as `platforms-scan.csv` in the user's folder.

**Search source line — RULE (№48).** Right under the title of every live search result (Lite, full, agent, pattern search, Free scan) say how it was searched, so the user knows whether this is all there is:
- built-in web search: `Search: built-in web search, no SEO API — free, but it sees only part of Google and gives no positions. With your DataForSEO key the live scan reads Google's top 10–30 for every product and usually finds several times more.` + `Probed: N products × "<suffix>"`;
- SerpApi: `Search: SerpApi (your account, <plan>) · Google <country> · top <depth> · N queries · used N searches, <left> left this month`;
- DataForSEO: `Search: DataForSEO API (your account) · Google <country> · top <depth> · N products × "<suffix>" · cost $X`;
- mixed: name both and which part came from which.
After the list, one line on how to get more **in this case** (only what applies): more products, `--depth 20/30`, other suffixes (`reviews`, `complaints`, `reviews 2026`), the full mode instead of Lite, the pattern search ("find new platforms").

**What gives more — upgrade hint (№48), honest and once per session.** Under the "how to get more" line, show only the items the user does not have yet (plan from `account_info`, Claude plan and `agents:` from the profile, DataForSEO from the settings), each with what it really changes. Never promise more than that item changes:
- **Your SerpApi key (free plan)** → Google's real top 10 with positions for the live scan and the footprint search for new platforms, 250 searches a month at no cost: start here.
- **Your DataForSEO key** → the same real Google, pay per request with no monthly cap: for big scans (50+ products, top 30) or when SerpApi's free searches are used up. Cost shown before every run.
- **Claude Max** → the full mode with the platform-scout agent every time instead of Lite: more products per run and a deeper check, without hitting the Claude Pro limit after one big search.
- **PARASITER Insider** → more *ready* platforms: the author's whole checked base the same day he adds it (on Pro ~7 days later), with live example posts and sign-up links — platforms you can use without searching at all. Insider does not change how many platforms the live search finds. Link: https://parasiter.affiliatecredo.com/?utm_source=plugin&utm_medium=upgrade&utm_campaign=platform-finder#pricing
If the user has all three, skip this block. One short line per item; no pressure words, no "limited offer".



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
