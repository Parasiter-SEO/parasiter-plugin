---
name: brand-presence
description: Audit a client brand's presence before and during parasite SEO work — a quick audit of the client's site (indexing, titles, landing pages for the target queries, speed, tracking), the brand's profiles on social networks and trusted platforms (LinkedIn, YouTube, Medium, Reddit, Quora, X, Facebook, Instagram, Pinterest, TikTok, industry directories) — do they exist, are they complete and consistent, do they link to the site — and a content audit of what the brand already publishes, then a plan of profiles to open or fix and topics for the content plan. Uses the brand-auditor agent. Use when the user (agency role) says "audit the client", "brand audit", "check their profiles", "which profiles should they have", "audit their site", "audit their social content", or at client onboarding.
---

# Brand Presence

## Work label (testing period)

Start every reply produced by this skill with one line naming it and the client:
`▸ PARASITER · brand-presence · [client]`
If you called agents, add them after an arrow: `▸ PARASITER · brand-presence · Acme → brand-auditor`. One line only, no other system talk.

## Plugin basis and Claude plan — RULE (№33)

Every answer here is PARASITER at work: this skill's steps, Rumer's rules, criteria and references — never general knowledge alone. Name the basis briefly where it matters ("by Rumer's rules", the checklist, score or reference used, "PARASITER platform base"). A request this skill doesn't cover → the right skill; nothing fits → one line "outside PARASITER's skills — I answer by Rumer's general rules", then "0 — menu". Full rule: `navigator/references/agents-and-plan.md`.

**Agents and Claude plan.** Heavy step: the brand audit → agent `brand-auditor`. Mode: `agents:` in `parasite-seo-profile.md`, else `agents_default` from `account_info`.
- `on` (Claude Max, Team) → run the agent; label `▸ PARASITER · <skill> → brand-auditor`.
- `lite` (Claude Pro) → the **Lite version** below, label `▸ PARASITER · <skill> · Lite`. When the full version would clearly give a better result here, add one line of advice — why, and the phrase **full** ("For 20 products the full version is better: brand-auditor checks every one, about 3–5× more of your Claude limits. Say **full** — or I keep Lite").
- `offer` (plan not known) → ask once before the first run: "This step of the skill is done by PARASITER's brand-auditor agent: separate context, deeper, uses more of your Claude limits (best on Max). Run it? Or Lite with the same skill."
- "full" / "audit by agent" → run it this time; "turn on agents" → `agents: on`; "save limits" or a usage limit hit → `agents: lite` (save in the profile, advice from `agents-and-plan.md` §3).

**Lite version:** 2–3 key profiles checked by the checklist; the rest listed as not checked. Lite is the same method in a smaller scope: say what was left out.

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
- "add these profiles to <client>'s plan" — tasks for the month
- "write the LinkedIn About for <client>"
- "audit <client>'s top landing page"

Part of PARASITER by Rumer (Affiliate Credo).

**Parasite pages work better for a brand that is visibly real.** When a reader meets the brand on Medium or Reddit, clicks through and finds a complete LinkedIn page, a YouTube channel and a site that loads fast and answers the query, they trust the page they came from. When they find nothing, or a dead profile from 2021, the page loses them. Search engines and AI answers also read the brand's footprint across platforms. This skill finds what is missing and turns it into work.

For the agency and site owner roles (navigator `references/roles.md`); for a site owner the "client" is their own site. Reply in the working language; the client-facing summary in the client's language. Read `clients/<slug>/client-brief.md` first; if it is missing, run `client-workspace` onboarding first (at least Message A).

## Step 1 — What to audit

Ask only what the brief doesn't answer: the site URL, the list of known profiles (or "find them"), the 5–15 target queries, the country. Then send the **`brand-auditor` agent** the brand name and spellings, site URL, known profile URLs, target queries, country and language, and the checklist `references/profiles.md`. It searches for the profiles that exist, opens each one and the site's key pages, and returns facts with links.

## Step 2 — Site quick audit (free, no crawler)

From the agent's facts and `references/site-audit.md`:
1. **Can Google read it:** robots.txt, sitemap, noindex on key pages, canonical, HTTPS, the site's `site:` count against the pages it should have.
2. **Landing pages for traffic:** for each target query and for each destination in the brief — is there a page that answers it, does it load on mobile, is there one clear action (buy, book, form)? Pages where our parasite links will land matter most.
3. **Titles and descriptions** of those pages: match the query, unique, not cut.
4. **Speed:** PageSpeed Insights for the main landing page (mobile score, LCP) — link the report.
5. **Tracking:** GA4 tag present, key events the client tracks (form, purchase); without them, the monthly report can show visits but not leads — say so now.
6. **Trust basics:** contacts, about page, real address or company details, reviews widget only if real.

Then the **landing pages our links will point to** go through `page-audit` (brand scale): first screen, offer, CTA, trust, images — Rumer's content rules applied to the site itself. A parasite page can't sell through a landing page that doesn't.

This is a quick audit for the parasite SEO work, not a full technical SEO audit. For a full crawl suggest Screaming Frog or the client's SEO tool; say it once.

## Step 3 — Profiles: present, complete, consistent

Per platform in `references/profiles.md`, one row: exists (URL) · complete (name, logo, bio, link to the site, contact) · consistent (same name, logo and one-line description as everywhere) · active (last post date) · fit for parasite work (can it host articles or long posts that rank: LinkedIn articles, Medium, YouTube descriptions, Reddit / Quora answers where the community allows declared brand accounts).

Score each platform **0–3** (0 missing, 1 exists but empty or broken, 2 complete, 3 complete and active) and show a short table. Platforms that matter for the client's audience come first (B2B → LinkedIn, YouTube, Medium, industry directories; B2C → Instagram, Facebook, TikTok, Pinterest, YouTube, Reddit).

## Step 4 — Content audit

For the 3–5 most active profiles and the site's blog: what the brand publishes (topics, formats, frequency, last 90 days), what gets engagement (views, comments, reactions where public), which target queries no content covers, and what can be reused as parasite pages (a webinar → a LinkedIn article and a Medium guide; a YouTube video → a document guide with the video embedded). Only what is visible on the profiles; never guess the client's private stats.

## Step 5 — Plan and save

Write `clients/<slug>/brand-presence.md`:

```
Brand presence · Acme · 2026-11-01
Score: site [n]/6 checks passed · profiles [sum]/[max]
Site — critical: … · fix: …
Profiles to open: Quora (brand), Medium (publication) …
Profiles to fix: LinkedIn — no link to the site, old logo; YouTube — empty About …
Reuse: webinar Oct 12 → LinkedIn article + Medium guide …
Topics nobody covers yet: [queries]
```

Then offer, in one line: add the profile tasks and the topics to the client's content plan (`client-workspace` Step 3). For profile texts (bio, About, first posts) use `sales-review-writer` brand mode; for covers and banners `post-illustrations` with the brand kit.

Re-run every 3 months, or before a report when profiles were opened: the before/after table goes into the client report.

## Rules

- Only real, declared brand accounts. Never suggest fake personal accounts, bought followers, reviews, likes or engagement, and never accounts on platforms whose rules forbid brand accounts.
- Facts from what the agent opened, with links and the date. A profile not found is "not found", not "doesn't exist" — ask the client.
- Never ask for or store passwords; the client gives access through each platform's own roles (LinkedIn page admin, YouTube manager, Business Manager).
- Health, finance and other regulated niches: profile texts follow the client's approved claims only.
