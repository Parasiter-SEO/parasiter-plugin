# Your story — the first step of "About you" (№63)

Setup step 3 for affiliates. Instead of a questionnaire, the user tells their parasite SEO story in their own words — typed or dictated — and PARASITER takes everything it needs from it: the profile, the starting point for goals, the pains to solve first. Then it gives a short verdict: what PARASITER will do for this person and what they can reach with it. A questionnaire stays one tap away for those who prefer it.

Everything is in the working language. The story never leaves the user's folder: it is not sent to the PARASITER server.

## 1. The invitation (one message)

> **Tell me your story — 2–5 minutes, your own words.** Type it or dictate it, as long or short as you like. Rough numbers are fine, so is "I'm just starting". From this I build your profile, your starting point and your plan, so I won't ask the same things again.
>
> What to cover (any order, skip what doesn't apply):
> • **What you do now** — how you work with parasite SEO today, how many hours a week, alone or with a team
> • **Where and what** — platforms you post on, niches and offers, programs or networks, countries and languages
> • **What works** — platforms, page types or products that bring clicks or sales
> • **What doesn't** — what gets deleted, doesn't get indexed, doesn't sell
> • **Money** — roughly what parasite SEO brings you now per month, and what you'd like it to bring
> • **How you see parasite SEO** — a side income, a main business, a test; where you want to grow (more niches, own site, clients, a team)
> • **What gets in your way most** — indexing, finding platforms, bans and cleanups, writing, choosing offers, tracking sales, time
> • **What you need most from PARASITER right now**
>
> 🎙 **Voice:** in Claude Code use your computer's dictation — Windows: **Win + H**, Mac: press **Fn** twice (or Control twice). In the Claude app, use the microphone.
> Prefer short questions instead? Say **"ask me questions"**.

"ask me questions" / "questions" → Message A in the navigator, then `goals` Mode 1, as before. The story step is `done` either way.

## 2. Taking the story in

Read the whole story (several messages are fine; wait for "that's it" or a clear end before answering). Then:

1. **Fill what it answers** — without asking again:
   - profile (`parasite-seo-profile.md`): niches, offers, programs, country and content language, hours, tools, level;
   - baseline facts for `goals` Mode 1: hours, pages per week, live pages and platforms, content types, income now — every number marked **(from your story)** so the user can correct it;
   - wanted income, direction of growth (side income / business / clients / own site / team) → `goals` Mode 2 inputs, kept as the user's words.
2. **Save the story** as `parasite-seo-story.md` (format in §5): the user's words, tidied but not rewritten, plus the extracted lines.
3. **Ask only the gaps** that the next steps really need, in one message, 2–4 questions at most (most often: target country / content language, programs, which SEO tools they have). Never re-ask what the story said, even vaguely: confirm it instead ("You said around $300 a month — right?").

## 3. The verdict — right after the story (setup step 3)

Give it **in the same reply as the gap questions, above them**, before any upload request. Why here: the user has just spent effort telling their story, and the first value must come back at once; uploads and goals (steps 4–5) take longer and can wait for a later session. At step 12 ("Setup done") the summary of what the user now has comes as before.

Format — 8–12 lines, the user's own words where possible, no theory:

```
Here's what I heard
• [2–3 lines: where you are now — hours, platforms, niche, what works, what doesn't]

What PARASITER does for you
• [your pain, in your words] → [the function and what changes] (say "[phrase to start it]")
• [pain] → [function] …   (3–5 lines: only functions that answer what the user said, most painful first)

Where this can take you
• [2–3 lines: how your work changes — e.g. "every page tracked, you see which platforms and offers actually sell",
  "new platforms with no competitors every week instead of the same spammed ones",
  "pages that died are noticed in a day, not after sales stop"]

Your first step: [one concrete action for today]
```

Rules for the verdict:
- **No money.** No income forecasts, no "you will earn", no promise of rankings. Speak about how the work changes: faster, measured, fewer dead pages, more platforms, clearer decisions. The user's own wanted income is theirs; the goals skill shows the math later.
- Every "PARASITER does" line maps one thing the user said to one real function of their plan. A function their plan doesn't open is marked 🔒 Pro / 🔒 Insider with one line on what it does (№56 rule), never sold harder than that; on Free say what works today.
- Map pains to functions with this table (use the user's words, not these):

| The user says | PARASITER answers with |
|---|---|
| pages don't get indexed | `indexing`: what blocks indexing, the free way, Rumer's indexer comparison, clean lists, results counted |
| can't find platforms / platforms get spammed / always the same platforms | `platform-finder`: the checked base and pattern search — clean platforms with no competitors, where affiliates post now and when |
| pages get deleted / cleanups / bans | `platform-monitor`: alive, indexed, still ranking; alerts; republish queue |
| don't know what to write / pages don't sell | `content-type-selector` + `sales-review-writer`: the content type that sells for each query, the article for the platform |
| don't know which offer / program | `affiliate-finder` (Insider: the offers Google's top already sells) |
| don't know what earns / no tracking | `work-log`: every page and sale in one journal, sub-IDs, reports by page, platform, offer |
| no time / no system / chaos | navigator + `goals`: the daily plan built from goals and the journal |
| want to grow: more niches | `niche-analysis` (with an SEO API) |
| want clients / agency | `client-workspace` (role: agency) |
| own site / blog / YouTube | `client-workspace` own-site mode / `creator-channels` |
| images take time / cost money | `post-illustrations`: $0 images |

- **First step** = the step that answers the biggest pain and moves setup on: often step 4 (upload the base) or, when starting from zero, the first offer (`affiliate-finder`).
- After the verdict and the gap questions, setup continues with step 4 as usual (Message B), skipping whatever the story already answered.

## 4. Later sessions

- The navigator reads `parasite-seo-story.md` with the profile. The pains in it raise matching tasks in today's plan (said "indexing is my problem" → indexing checks and the clean list come first while pages wait for Google). The goals' "what you want" lines stay in the user's words.
- **Once a month** (first session of the month): one line — "Has your story changed? Tell me what's new: what started working, what stopped, what you want now." The answer is added as a dated "Update" section; the profile and baseline corrections follow the same rules (the baseline itself is never edited, corrections are dated lines).
- "my story" / "what did I tell you" → show the file in short. "change my story" → add an update.

## 5. File format — `parasite-seo-story.md`

```
# My parasite SEO story
Told: 2026-11-14 · way: dictated / typed

## In my words
[the story, tidied for typos and filler words, nothing added, nothing removed that carries meaning]

## What PARASITER took from it
- now: [hours / week, alone or team, platforms, niches, programs, live pages]
- works: […]
- doesn't work: […]
- income now: [as said, or "not said"] · wanted: [as said, or "not said"]
- sees parasite SEO as: […] · wants to grow into: […]
- biggest pains: [1. …, 2. …, 3. …]
- needs most from PARASITER: […]

## Verdict given
[the verdict, as shown]

## Updates
### 2026-12-01
[…]
```

Income and anything personal stay in this file in the user's folder only. Never send the story, its numbers or its pains to the PARASITER server, a URL, or any tool outside the user's machine.
