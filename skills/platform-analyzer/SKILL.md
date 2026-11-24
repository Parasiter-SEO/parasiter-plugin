---
name: platform-analyzer
description: Break down one parasite SEO platform before investing time in it — affiliate reviews ranking in the top 10 there, registration, indexing of fresh pages, noindex, moderation and keyword filters, account warm-up, content limits, free or paid, stability — and give a 0–100 score with a verdict on what to publish there and Rumer's class (proven, Web 2.0, Web 3.0); for a Web 3.0 platform researches how people publish there. Use when the user asks "should I post on X", "is X still working", "analyze this platform/forum", or before the first post on a new platform, or asks "how do people publish on X?", "is this Web 2.0 / Web 3.0?".
---

# Platform Analyzer

## Work label (testing period)

Start every reply produced by this skill with one line naming it, so the user always sees which part of PARASITER is working:
`▸ PARASITER · platform-analyzer`
If you called agents for this reply, add them after an arrow: `▸ PARASITER · platform-analyzer → serp-analyst, product-researcher`. If you hand off to another skill, the next reply carries that skill's label. One line only, no other system talk.

## Show what the next plan opens — RULE (№56)

Pro skill. On Free or with no key, Step 0 answers with the **locked card** from `navigator/references/upgrade-showcase.md` §2 (what it would do for this user now, Insider = all 16 skills / Pro = 13, one payment for lifetime access, prices from `account_info.prices`, the upgrade link), then the Free alternative. Pro user: Insider-only parts of this skill are shown as 🔒 Insider where they come up, one line each.

## Plugin basis and Claude plan — RULE (№33)

Every answer here is PARASITER at work: this skill's steps, Rumer's rules, criteria and references — never general knowledge alone. Name the basis briefly where it matters ("by Rumer's rules", the checklist, score or reference used, "PARASITER platform base"). A request this skill doesn't cover → the right skill; nothing fits → one line "outside PARASITER's skills — I answer by Rumer's general rules", then "0 — menu". Full rule: `navigator/references/agents-and-plan.md`.

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
- **Mark tried:** on this skill's first real run in the session, add or update its line under `tried:` in `parasite-seo-profile.md` (`- <skill> · YYYY-MM-DD · <what, 3–6 words>`; agents too, marked `agent`). **Usage stats (№78):** at the same moment call `usage_event` with the skill name (and once more with `agent` when an agent runs; `mode` lite or full) — names only, never a page, product, query or text; skip it when the profile says `usage_stats: off`, the key is missing, or the server tools are unavailable. When the user seems lost or asks what else there is, add: "All PARASITER functions: say **help**."

Options that usually fit after this part (adapt to the user's products and words):
- "what sells there?" — the topic for this platform
- "write the first test post"
- "find more platforms like it"

Part of PARASITER by Rumer (Affiliate Credo).

A platform is worth it when **review pages of affiliate products already rank there in the Google top 10 and fresh pages get indexed.** How long it will live doesn't decide anything: if it is in the top now, it goes to work now — even if it lives a day. A platform whose affiliate pages have lived 2+ weeks counts as **stable**. Whether links on it are indexed or followed doesn't matter — the page itself being indexed does. Every verdict says whether the platform is **free** (users post) or **paid** (news, PR, sponsored).

Reply in the user's language.

## Step 0 — Plan check (Pro)

**Step 0 — Plan check.** Call `account_info` once per session (reuse it if already called). Pro or Insider, active → proceed. Free, expired or no key → the locked card (№56, `navigator/references/upgrade-showcase.md` §2) built on: "This is a Pro feature — one platform scored 0–100: affiliate reviews in the top 10 now (checked live), indexing of fresh pages, registration, moderation, free or paid. Upgrade: https://parasiter.affiliatecredo.com/?utm_source=plugin&utm_medium=upgrade&utm_campaign=platform-analyzer#pricing", then offer the Free alternative for this skill (a short manual checklist to run yourself: search `site:<domain> review`, open 2–3 results, check they are live, indexed and not noindexed — say "how do I check a platform myself?"), and stop.

## Step 1 — Inputs

Platform domain (or a URL of a post on it), the niche/offer, language, and whether the user already has an account (age, activity).

## Step 2 — Exclusions and server data (Pro)

First check the platform against the exclusions: `exclusions_get` with a key, else `../platform-finder/references/exclusions.md` (match: host equals or ends with the domain; a path in the entry must prefix the URL path). A stop type or blacklisted site: say so with the reason, score nothing, and offer to find other platforms. A domain in `dead`: say it was found dead on [date] and analyze only if the user insists (then check live — it may have come back).

If `platform_get` is available, call it: last status, history (when it ranked, cleanups), the author's notes, indexing speed, `signup_url` and `examples` (live posts, already filtered). Use it as the starting point and say how fresh it is. Without the server, do the checks below live.

## Step 3 — Checks

Use web search / fetch where available; otherwise give the user each check as a short instruction. Details and how to read results: `references/checks.md`.

1. **Registration** — open for new users? Captcha, app, phone, invite, paid plan, old accounts only? Give the **sign-up link**: `signup_url` from the server, or find it (sign-up / register / create account link on the home page, else /register, /signup, /join, /user/register, /create-account) and open it to confirm the form loads; else "sign-up link not found" + the home page.
2. **Fresh indexing** — are posts from the last 1–2 weeks indexed (`site:` + recent)? How fast?
3. **noindex** — meta robots and X-Robots-Tag on new posts/profiles; some platforms noindex new accounts only.
4. **Affiliate reviews ranking there (the main check)** — search `site:domain review` and "[product] review" for a few affiliate products: are review pages on this domain in the Google top 10, in "Discussions and forums" or AI Overview? None → the platform is not proven, however good it looks — **unless** it passes the other checks (open sign-up, fresh pages indexed, no noindex, live topic): then it is a **Web 2.0 candidate by Rumer** (nobody posts there yet, the user can be its discoverer), verdict "test 1–3 posts as your Web 2.0" instead of "skip". **Open each review page found (up to 3, free): it counts only if it is alive** — 404 / 410, "page removed" text, redirect to the home or login page, an empty page or noindex (meta robots / X-Robots-Tag) = removed, however high Google still shows it. All found pages removed → verdict "skip — pages are being removed". Pages shown to the user as examples go through the local private filter first (with a key: `private_hashes` + platform-finder's `scripts/privfilter.py`, nothing is sent); the author's posts are never shown.
5. **Link to the offer** — possible anywhere (body, profile, signature, description)? Outbound warning page? Link only after N posts? Link indexing and nofollow don't matter.
6. **Moderation** — pre-moderation, keyword blacklists (platforms block typical affiliate words), automatic AI spam removal, cleanup waves, bans.
7. **Account needs** — warm-up (XenForo forums, Medium, LinkedIn need aged/active accounts), points systems, first-post limits.
8. **Content format** — length/character limits, images, tables, editor (BBCode), title uniqueness.
9. **Stability label** (not a reason to skip) — how long affiliate pages on it have lived: 2+ weeks = stable, less or unknown = new, pages being removed now = unstable.
10. **Fit** — does the platform's audience and format suit the content type and offer?

## Step 4 — Score

Score with `references/scoring.md` (0–100) and show:

```
[Platform] · score NN/100 · checked [date]
Free / Paid · Affiliate reviews in top 10 (live): … | Indexing: … | Stability: stable / new / unstable | Link: …
Class (by Rumer): proven / Web 2.0 🔒 candidate / Web 3.0 — one line why
Live example: [<product or title>, <date>](<post URL>) · pos. N   |   Sign-up: [<domain>/register](<sign-up URL>) (or "sign-up link not found" + [home](<home URL>))
Rules: [terms](<official rules URL>) — only when the card cites the platform's rules (moderation, links, affiliate posts)
Verdict: [publish now / test 1–3 posts / skip] — affiliate reviews in the top 10 now = publish now
Best content type here: …
How to post: [account, title, link placement, tone]
```

**Clickable links (№84, same rule as `platform-finder`):** every post, sign-up, rules and home page on the card is a clickable markdown link with the full `https://` URL (Cyrillic and special characters percent-encoded), never a bare domain or a URL to copy. No checked sign-up URL → the engine's standard path as a link marked "(not checked)"; never invent one. The same goes for the Web 3.0 mode below: official docs and ranking example pages as links.

**Lean card first (№85, same rule as `platform-finder`):** the card opens with the five facts — live post with its date, newest affiliate post date, LIVE + INDEXABLE, working sign-up, and the section link (where such posts sit and who else posts). Free checks first; paid calls (DataForSEO domain strength, positions) only after the platform passes the live check. A platform with no affiliate posts but working sign-up and indexed threads is a **candidate — "try it, you'll be first"**, not a fail.

Write the result into the user's platform base: `work-log` `platform-set --platform <slug> --domain … --type … --links … --score NN --state testing|active|dropped --class proven|web2|web3` and a journal row `add --event platform --platform <slug> --score NN --note "verdict: …"`.

## Rumer's class — RULE (№67)

Every verdict names the class by Rumer's definitions (`../help/references/rumer-concepts.md`; his own terms, not the usual "Web 2.0" / "Web3" — say so the first time):
- **proven** — affiliate reviews rank there now (check 4 found live ones).
- **Web 2.0 🔒 candidate** — no affiliate posts yet, but sign-up, indexing and topic pass. Add the privacy line: "If it works, keep it as your own Web 2.0: don't name it in public groups, screenshots or videos, don't link your profiles to it, post naturally from one account." When check 4 later finds other people's affiliate posts on a platform the user keeps as `web2`, say "your Web 2.0 has been found by others — it is a proven platform now" and offer `--class proven`.
- **Web 3.0** — its pages rank in the top for everyone to see, but there is no visible sign-up or post form: publishing goes through the service's own tools and few people know the process.

## Web 3.0 mode — "how do people publish on <domain>?"

For a Web 3.0 platform (or when the user asks how pages get onto a service), research the route instead of scoring registration and moderation:
1. **What the ranking pages are** — open 2–3 live examples: what kind of page (static page, document, listing, profile, project page), what URL shape, whose account they sit under.
2. **The legitimate route** — from the service's own documentation and public guides only: how a person opens their own account, creates a public page of that kind, makes it public, and whether the service's terms allow promotional or affiliate content. Give it as steps with links to the official docs, plus cost (free tier or paid) and what it takes technically.
3. **Indexing** — are such pages indexed, how fast, and do new ones rank (fresh examples)?
4. **Risks** — the service's terms (accounts used for spam get closed), Google's site reputation abuse policy and spam rules, how the service handles abuse reports. A route that needs someone else's account, access controls bypassed or other organisations' storage is abuse: say so and stop.
5. **Verdict** — "Web 3.0 · route found: <easy / technical / paid>" with the first test (one useful page, disclosure, check indexing in 3–7 days), or "route not found — skip". Mark it as **Creative SEO** work: a method few people use, a test before any scale.
Domains in the stop list or blacklist are not researched (Step 2 still applies first).

## Rules

- State what was checked live and what is assumed or from history.
- Recommend testing with 1–3 posts before scaling; never mass-post from one account.
- Respect platform rules; if links or the format are not allowed, say so instead of suggesting tricks to hide them.
- Remind: keep a copy of every text; platforms delete without notice.
