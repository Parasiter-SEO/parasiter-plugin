---
name: brand-presence
description: Audit a client brand's presence before and during parasite SEO work — a quick audit of the client's site (indexing, titles, landing pages for the target queries, speed, tracking), the brand's profiles on social networks and trusted platforms (LinkedIn, YouTube, Medium, Reddit, Quora, X, Facebook, Instagram, Pinterest, TikTok, industry directories) — do they exist, are they complete and consistent, do they link to the site — and a content audit of what the brand already publishes, then a plan of profiles to open or fix and topics for the content plan. Uses the brand-auditor agent. Use when the user (agency role) says "audit the client", "brand audit", "check their profiles", "which profiles should they have", "audit their site", "audit their social content", or at client onboarding.
---

# Brand Presence

## Work label (testing period)

Start every reply produced by this skill with one line naming it and the client:
`▸ PARASITER · brand-presence · [client]`
If you called agents, add them after an arrow: `▸ PARASITER · brand-presence · Acme → brand-auditor`. One line only, no other system talk.

## Next steps (end of every reply)

End each reply with one short line of 2–3 options, each with the phrase to say, e.g. `Next: "add the profiles to Acme's November plan" (client-workspace) · "write the LinkedIn About for Acme" · "audit Acme's top landing page" (page-audit).` Offer only what the user's plan includes. Saving the audit to the client folder is done automatically, not offered.

Part of PARASITER by Rumer (Affiliate Credo).

**Parasite pages work better for a brand that is visibly real.** When a reader meets the brand on Medium or Reddit, clicks through and finds a complete LinkedIn page, a YouTube channel and a site that loads fast and answers the query, they trust the page they came from. When they find nothing, or a dead profile from 2021, the page loses them. Search engines and AI answers also read the brand's footprint across platforms. This skill finds what is missing and turns it into work.

For the agency role (navigator `references/roles.md`). Reply in the working language; the client-facing summary in the client's language. Read `clients/<slug>/client-brief.md` first; if it is missing, run `client-workspace` onboarding first (at least Message A).

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

This is a quick audit for the parasite SEO work, not a full technical SEO audit. For a full crawl suggest Screaming Frog or the client's SEO tool; say it once.

## Step 3 — Profiles: present, complete, consistent

Per platform in `references/profiles.md`, one row: exists (URL) · complete (name, logo, bio, link to the site, contact) · consistent (same name, logo and one-line description as everywhere) · active (last post date) · fit for parasite work (can it host articles or long posts that rank: LinkedIn articles, Medium, YouTube descriptions, Reddit / Quora answers where the community allows declared brand accounts).

Score each platform **0–3** (0 missing, 1 exists but empty or broken, 2 complete, 3 complete and active) and show a short table. Platforms that matter for the client's audience come first (B2B → LinkedIn, YouTube, Medium, industry directories; B2C → Instagram, Facebook, TikTok, Pinterest, YouTube, Reddit).

## Step 4 — Content audit

For the 3–5 most active profiles and the site's blog: what the brand publishes (topics, formats, frequency, last 90 days), what gets engagement (views, comments, reactions where public), which target queries no content covers, and what can be reused as parasite pages (a webinar → a LinkedIn article and a Medium guide; a YouTube video → a Pressbooks chapter with the video embedded). Only what is visible on the profiles; never guess the client's private stats.

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
