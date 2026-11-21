# Free start — the first setup and the First look on the Free plan (№67)

> **Beginners (`level: new`) take the "First post with Rumer" path instead (`first-post.md`, №73):** story → what to promote → their strategy → one real post through the whole cycle. This file is for users who already do parasite SEO (`level: pro`).

The Free plan's job: the user starts real work inside PARASITER, gets the first insights from **their own** story and data, and feels where the Free limits end. So on a Free key (and with no key, as far as it goes) the navigator runs the whole first setup for real — it is not a Pro feature. Only the **daily** plan, the session checks and continuous reports stay Pro.

Everything is in the working language. Nothing from the story or the uploads goes to the PARASITER server: files stay in the user's folder.

## 1. What runs on Free during the first setup

| Setup step | Free key | No key |
|---|---|---|
| 1 Language | yes | yes |
| 2 Work environment | yes | yes |
| 3 Your story → verdict (`your-story.md`) | yes | yes |
| 4 Upload base and reports | pages: the first 10 go into the Free journal, the rest are counted; sales and traffic exports: **read once for the First look** (§2) | read once for the First look; nothing is journaled — the Free key opens the journal |
| 5 Goals | yes (`goals` is Free) | yes |
| 6 Offers | from the story; new offers = 🔒 Insider `affiliate-finder` | same |
| 7 Affiliate links | the links on the journal pages; the full links library = 🔒 Pro | the user keeps them for now |
| 8 Indexing | the facts and the free check by hand (site: search); Rumer's indexer comparison and tracking = 🔒 Pro | same |
| 9 Telegram | the free bot: "connect Telegram" links the Free key — the free channel, Rumer's notes and **the free course** (/course) | not needed |
| 10 First topic | yes (`content-type-selector`) | yes |
| 11 First article with images | yes | yes |
| 12 Publish and log | yes (Free journal) | the locked card leads with the Free key |

After step 4 (or right after the verdict, when the user has nothing to upload) comes the **First look** (§2). After step 12: "Setup done" and the **Starter plan** (§3) instead of today's daily plan.

## 2. The First look — insights from the user's own story and data

One reply, one screen. It must contain something the user did not know before, computed from what they gave — never generic advice. Build it from whatever exists:

**A. With data** (pages list, sales or traffic exports, platform stats). Read the files once (the `work-log` import scripts may parse them into a temporary table in the user's folder; on Free nothing is added to the journal beyond the 10 pages). Pick the 3 strongest insights, each with the user's numbers:
- **Where the money comes from** — top platform and top product by sales or commission (or by clicks when there are no sales): "68% of your commission in the last 3 months came from one platform: <X>."
- **Concentration risk** — more than 60% of income or clicks from one platform or one product: "One cleanup on <X> would take most of your income. Rumer's rule: spread to 10 platforms."
- **Clicks without sales** — pages or platforms with traffic but no sales: a conversion problem, not a traffic problem → "audit my page: <link>" (Free).
- **Topics that earn on one platform and are missing on others** — the top 3 gaps from the pages list vs the platforms the user has: the rollout they can do this week.
- **Dead weight** — among the first 10 pages, those that don't open, are removed or have noindex (the free alive check through `platform-monitor` → `page-checker`, ask first, it costs nothing).
- **Pace vs goal** — pages per week now vs Rumer's rule (10 platforms / 100 live posts) and the wanted income from the story.

**B. Starting from zero** (no data): build it from the story and one free look at the market:
- the verdict's main pain, restated as the first thing to fix;
- with the user's yes, **one platform scan** for their product (a Free scan, 3 a week): where reviews rank right now, top 3 in full;
- the 3 best topics for that product from `content-type-selector` (Rumer filter score);
- the gap to Rumer's rule and what the first 2 weeks look like (the entry strategy: niche → queries → offer → 5 topics → 3 platforms → rhythm → check).

**Shape** (keep it this order; a visual artifact like the day plan is welcome when the data is rich):
```
🔎 First look · <the user's name or project>
Where you are: <pages / platforms / programs / income, from the story or the data>
1. <insight with a number> → <what to do, the phrase to say>
2. <insight> → <action>
3. <insight> → <action>
Today: <the one first step>
🔒 With your data, Pro would: <2–3 lines made of this user's numbers — e.g. "track all 37 pages (Free keeps 10) and check them every day", "tie your ClickBank and Digistore24 sales to pages and show EPC by platform", "plan the next pages where you already earn (publication queue)">
Insider: <one line — e.g. "the scale plan from your sales and the offers Google's top sells in your niche"> · Pro <Pro price> · Insider <Insider price> (one payment, lifetime; `account_info.prices`) → <upgrade link, utm_campaign=first-look>
```
Rules: three insights, not ten; numbers from the user's files only (mark story numbers "(from your story)"); no income promises; the 🔒 lines must use this user's numbers, never a generic list. Then call `free_event` with `first_look` (Free key only; show nothing about it) and continue the setup with the next step.

## 3. The Starter plan — after step 12 on Free

Instead of the daily plan (Pro), Free gets one plan for the **first week**, saved as `parasite-seo-starter-plan.md` and shown again on "what should I do today?" until it is done:
- 5–7 tasks built from the First look and the goals (the rollout gaps, the pages to audit, the first topics, one platform scan a week, the page checks of the Free journal), each with the phrase that starts it;
- ticked off from the journal and `tried:`; "what should I do today?" on Free shows the next 2–3 unticked tasks, then one line: "🔒 On Pro this becomes a new plan every morning, built from your journal, goals and page checks — <upgrade link, utm_campaign=starter-plan>";
- when all tasks are done: "Starter plan done" with what moved (pages, indexed, checks), and the locked card of the daily plan (`upgrade-showcase.md` §2).

## 4. Where the Free limits show (honest, at the moment they're met)

Show a limit only when the user actually meets it, in one line, with the Free alternative first: an 11th page (journal full — the `journal_full` event), a sales export to keep in the journal (read once for the First look; continuous imports and reports are Pro), the 4th scan of the week, offers to find (Insider), indexer comparison (Pro), daily plan (Pro). Never block the setup on a limit: mark the step and go on.
