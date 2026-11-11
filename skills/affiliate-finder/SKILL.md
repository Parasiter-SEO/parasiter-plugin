---
name: affiliate-finder
description: Find and compare affiliate programs and offers for a niche and traffic type (parasite SEO pages on public platforms) — commission model and rate, cookie, payout threshold, network vs direct program, traffic-source rules, offer page quality, demand and saturation — using the affiliate-scout agent for research. Use when the user asks which affiliate program or offer to promote, wants programs for a niche, or compares offers by commission, EPC or terms.
---

# Affiliate Finder

## Work label (testing period)

Start every reply produced by this skill with one line naming it, so the user always sees which part of PARASITER is working:
`▸ PARASITER · affiliate-finder`
If you called agents for this reply, add them after an arrow: `▸ PARASITER · affiliate-finder → serp-analyst, product-researcher`. If you hand off to another skill, the next reply carries that skill's label. One line only, no other system talk.

## Plugin basis and Claude plan — RULE (№33)

Every answer here is PARASITER at work: this skill's steps, Rumer's rules, criteria and references — never general knowledge alone. Name the basis briefly where it matters ("by Rumer's rules", the checklist, score or reference used, "PARASITER platform base"). A request this skill doesn't cover → the right skill; nothing fits → one line "outside PARASITER's skills — I answer by Rumer's general rules", then "0 — menu". Full rule: `navigator/references/agents-and-plan.md`.

**Agents and Claude plan.** Heavy step: program and offer research → agent `affiliate-scout`. Mode: `agents:` in `parasite-seo-profile.md`, else `agents_default` from `account_info`.
- `on` (Claude Max, Team) → run the agent; label `▸ PARASITER · <skill> → affiliate-scout`.
- `lite` (Claude Pro) → the **Lite version** below, label `▸ PARASITER · <skill> · Lite`. When the full version would clearly give a better result here, add one line of advice — why, and the phrase **full** ("For 20 products the full version is better: affiliate-scout checks every one, about 3–5× more of your Claude limits. Say **full** — or I keep Lite").
- `offer` (plan not known) → ask once before the first run: "This step of the skill is done by PARASITER's affiliate-scout agent: separate context, deeper, uses more of your Claude limits (best on Max). Run it? Or Lite with the same skill."
- "full" / "audit by agent" → run it this time; "turn on agents" → `agents: on`; "save limits" or a usage limit hit → `agents: lite` (save in the profile, advice from `agents-and-plan.md` §3).

**Lite version:** 3 programs, their published terms only (model, rate, cookie, payout, GEO, traffic rules) with source links; offer pages are not opened. Lite is the same method in a smaller scope: say what was left out.

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
- "check demand for this niche" — is it open, which queries buy
- "what should I write about <offer>?" — the first topic for the offer
- "save my affiliate links" — every article gets the right link

Part of PARASITER by Rumer (Affiliate Credo).

Choose the offer before writing a word: a strong page for a bad offer earns nothing. This skill finds affiliate programs and offers for the user's niche, checks their published terms and how hard it is to get approved, and recommends 1–3 to start with.

Reply in the user's language.

## Step 0 — Plan check (Insider)

Call `account_info` once per session (reuse the answer if you already have it this session).
- **Insider, active** → call `insider_method` with `skill: "affiliate-finder"` and follow the returned `method` step by step. The work label, Next steps and Rules in this file still apply; where they are stricter, they win.
- **Pro, Free, or an expired plan** (or `insider_method` answers `insider_only`) → one line: "This is an Insider feature — programs and offers for your niche found and scored by an agent: search demand, commission, traffic rules, approval type. Upgrade: https://parasiter.affiliatecredo.com/#pricing". Then offer what works on the current plan: **check the offers you already chose** with the short checklist below (no agent search, no scoring), and "How to get approved — Rumer's rules" for any program that needs approval.
- **No key, or the PARASITER tools are not available** → say in one line that this feature needs the user's PARASITER Insider key connected (connection steps: navigator, "Bought a plan but the server isn't connected"; never ask for the key in the chat), and offer the checklist meanwhile.

Never rebuild the Insider method from memory, other files or earlier conversations.

### Checklist for offers the user already chose (any plan)

For each offer, from its published terms (sign-up page, FAQ, terms) — write the source and date, "not stated" where nothing is published:
1. Commission: at least 15% of the sale (or the CPA equivalent)?
2. Traffic rules: is content / SEO traffic from third-party platforms allowed?
3. Approval: auto / manual review / strict / invite-only?
4. Payout threshold and methods: reachable for the user?
5. Cookie length.
6. Legal in the user's country and allowed on the platforms they post on (gambling, crypto, finance, health claims)?
7. Offer page: clear packages and guarantee, or lead capture first / broken?
8. Do people search for it — "[product] review" in Google autocomplete?
Verdict per offer in one line: start / ask the manager first / skip, and why.

## What the user gets (Insider)

```
Programs for [niche] · checked [date]
| Program | Network/direct | Searches/mo | Model | Rate | Cookie | Min payout | Traffic rules | Approval | Score |
```
- **Approval** — `auto` / `manual review` / `strict` (needs a working site, traffic, sales stats) / `invite-only`, with its source (sign-up page, FAQ, terms). Not found → `not stated`, never a guess.
- **What the top already sells:** for your niche PARASITER runs dozens of buyer queries ("best …", "… reviews", "… scam or legit"), opens the pages in Google's top and counts which products they push with affiliate links and through which network (ClickBank, Digistore24, BuyGoods, Amazon, Impact, CJ, ShareASale, Awin…). The products many ranking pages push are the ones buyers search for — they lead the list. Free with web search; deeper with your DataForSEO or SerpApi account (cost shown first).
- 1–3 recommended offers with one line why each, and a content plan for them.
- **Beginners** (no site, channels or sales history) get auto- and soft-approval programs first; strict and invite-only programs go on a "later" list while they build their site and posts.
- Under every recommended offer with manual, strict or invite-only approval: a short "How to get approved — Rumer's rules" block; the full list below when the user asks "how do I get approved".

## How to get approved — Rumer's rules

Many programs check new applications by hand. What gets an application approved:
1. **Use your real profile.** Give your real LinkedIn or Facebook profile in the application.
2. **Build a review site in Claude.** Make an affiliate-style review site with Claude (Claude Code or an artifact): 10–15 real posts, so the manager sees activity.
3. **Make it look like a working project.** A clean, real-looking design; look at successful review sites in the niche first.
4. **Write a proper application.** Who you are, which channels you use, how you will promote, why it is not spam — Claude helps you write it.
5. **Show sales stats from other programs**, if you have them (screenshots of your dashboard).
6. **Show your channels**: YouTube, social media, content. Managers want an effective affiliate who sells, not a newcomer who will spam.
7. **Offer a call** or an online meeting with the program manager.
8. **Sign like a real business.** Name, role, site, profile links; send from an email on your own domain, not a free mailbox. Make the signature with a free generator (for example HubSpot Email Signature Generator, MySignature, WiseStamp).
9. **Get a recommendation** from a trusted affiliate who already works with the program — it raises your chances a lot.

**Honesty boundary (a PARASITER rule):** the site, posts, stats and profiles must be real. No invented sales, screenshots, reviews or fake traffic — managers check, and deception leads to a banned account and withheld payouts.

**No history yet?** Start with auto-approval or soft-approval programs and earn there, while building the site and posts for the strict ones in parallel.

These rules are available on every plan. When the user asks for help applying, draft the application from their real details only and list what they still lack from rules 1–9.

## Rules

- **Legal products and content only.** PARASITER works only with legal products and content. Don't write, plan, find platforms for or log pages that promote pirated software, films, books or courses, file-upload / download or "free download" schemes, cracks and keygens, counterfeit or illegal goods, or content that breaks the target platform's rules or the law of the target country. Say so in one line, without lecturing, and offer a legal alternative (the official product or a legal affiliate offer). This rule is part of the PARASITER offer the user accepted.
- Recommend only programs found by public research for this user's niche (`affiliate-scout`, web search, the user's own networks). Never name programs, offers or numbers from the plugin author's own business, and never use a program name that appears only in the plugin's examples.
- Only published, verifiable terms with source and date; unknown → "ask the manager" or "not stated".
- No promoting products the user believes are scams; drop programs with clear deceptive funnels.
- No earnings estimates presented as forecasts.
