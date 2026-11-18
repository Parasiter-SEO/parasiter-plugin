# Forum cluster — Rumer's method for ranking above competitors on forums (№68)

Rumer's rule, tested on his own work: he looked at a competitor's forum threads, picked the ones that had reached the top, and wrote about 10 of his own threads on those topics. They pushed the old threads out of the top almost at once. Two forces did it:

1. **Freshness.** Google's "Discussions and forums" block and forum results favour live, current discussions. A new thread with a real story beats an old one on the same query.
2. **Several threads per query.** One query, several threads, each with its own angle. Google builds the "Discussions and forums" block from several threads; the more good threads on the query are yours, the more places in the block and in the top can be yours.

**And the threads read like real ones because they are:** a person's own experience — "I tried it, here is what happened, sharing it" — not an ad.

Every skill that writes or plans forum posts points here.

## The steps

### 1. Pick the queries

Commercial queries only (`modifiers-and-serp.md`): "[product] review", "[product] results", "is [product] legit", "[product] vs [alt]", "[product] side effects / complaints", "best [category] for [need]". Good sources:
- topics where the user's other pages already rank or earn (`work-log` coverage) — Rumer's way: "forum posts on topics where my sites rank";
- the user's approved topics (`topics:` in the profile);
- the "Discussions and forums" block itself: queries that show it are the best targets.

3–10 queries per run.

### 2. Read the forum top of each query: the scan

With the user's SerpApi (free searches first) or DataForSEO (cost shown first), run `forumscan` (dry run first, then real after a yes):

```
serpapi_run  forumscan ["<q1>,<q2>,…", "--country", "us", "--depth", "20", "--mine", "parasite-seo-progress.csv", "--dry-run"]
dataforseo_run forumscan [same args]
```

It returns for each query: whether the "Discussions and forums" block is there, which threads sit in it and in the organic top 20, each thread's forum engine, age and comments, which threads are the user's own (`--mine`, the journal), and a verdict:

| Verdict | Meaning | What to do |
|---|---|---|
| **OPEN** | the forum top is old (most threads 180+ days, none under 45) | post the cluster now: fresh threads should push the old ones out |
| **WINDOW** | mixed ages | 3–5 threads with new angles have a real chance |
| **CROWDED** | many threads under 45 days: others post here now | more threads, sharper angles, keep them active with real updates |
| **NO FORUMS** | no forum threads in the block or the top | a forum post is a long shot here: take another query |

No API account → **Lite**: search each query yourself (web search), note the "Discussions and forums" block and the forum threads on the first page with the dates shown, and say the ages are approximate.

### 3. Analyse the competitors' threads that won

For every query, open the threads that sit in the block and the top (up to 5 per query, free) and take apart **why they won**, never what to copy:

| Look at | Note |
|---|---|
| Title | the formula (question / "my results after X weeks" / "X vs Y — honest" / warning), length, words from the query |
| Opening post | who speaks, the first two lines, the problem, the length, photos, numbers, the link (where, how many) |
| Story | timeline, results, what went wrong, who it's for / not for |
| Thread life | replies, the author's own follow-ups, the last reply's date |
| Forum | engine (XenForo, phpBB, Discourse…), section, the forum's rules on links |
| Author | a competitor's affiliate post (link to an offer, same pattern on many forums) or a real user |

Mark the competitor's winners: the same author or pattern across several threads in the top is the competitor whose method to beat. The result is a short table per query: thread · age · why it ranks · what it lacks (no numbers, no downsides, no update, old offer, no answer to a doubt from People also ask).

**Never parody or copy them.** Not their title, not their text, not their story. The user takes the winning *pattern* (angle, format, length, structure) and fills it with their own experience and a gap the competitor left open. A copied thread is a duplicate: Google drops it, the forum deletes it.

### 4. Plan the cluster: several threads per query

For every query that is OPEN, WINDOW or CROWDED, plan **3–5 threads**, each with its **own angle**:

| Angle | Title example |
|---|---|
| My results / my story | "Ikaria juice after 8 weeks — my honest results (with numbers)" |
| A question I answer from experience | "Is Ikaria juice legit? I was skeptical, here's what happened" |
| Comparison from use | "Tried Ikaria and Mitolyn — which one actually worked for me" |
| Mistakes / what I'd do differently | "3 mistakes I made with Ikaria juice (and what I'd change)" |
| For a specific person | "Ikaria juice over 50 — my experience with slow metabolism" |
| Doubts / downsides | "Ikaria juice side effects — what I noticed in the first 2 weeks" |
| Update | "Ikaria juice 3 months later — update on my results" (later, as a new thread or a reply in the first one) |

Rules of the cluster:
- **Every thread is different:** angle, title, opening, structure, length. Never one text spun into five. Google merges near-duplicates and shows one.
- **Different forums first.** Spread the threads over the forums from the scan and from the user's base (their strong forums, XenForo first by Rumer's preference). Two threads on one forum only in different relevant sections, and only when its rules allow.
- **The user's own accounts, one per forum.** The cluster is many threads, never many fake people: no second account to praise your own thread, no staged conversations. The author may come back to their own thread with real updates and answer questions. That keeps it alive.
- **Stagger:** 1–2 threads a day over a week, not all in one hour.
- **Freshness is the lever:** every 2–4 weeks a real update in each thread (new results, a price change, an answer to a question); when a thread ages past 60–90 days and fresh competitors appear, a new thread with a new angle.
- **Platform rules first:** where the forum forbids affiliate links, the link goes where allowed (profile, signature) or the thread goes without it; see the platform's rules in the user's base or `platform-analyzer`.

Show the plan as a table: # · Query · Verdict · Thread title · Angle · Forum · Day · Status (`todo`).

### 5. Write each thread as a personal experience post

`sales-review-writer` writes each thread in **forum experience mode** (`../../sales-review-writer/references/forum-experience-post.md`): an interview first, then a native first-person forum post.

**The experience must be real.** It is the user's own use, or a real person who used the product and agreed to share it (named as "my wife", "a client of mine"…). Without real use, the post is still first person and personal, but true: "I spent a week comparing …", "I asked my doctor / pharmacist …", "I read 200 complaints so you don't have to" — the research angle. Never invented results, weeks of use, weight lost or photos. A made-up story is the fastest way to get a thread deleted, an account banned and a buyer refunding.

### 6. Save the cluster and track it

Save the plan in the profile `parasite-seo-profile.md` under `forum_clusters:` (same convention as `topics:`):

```
forum_clusters:
  - query: "ikaria juice review"
    verdict: OPEN
    scanned: 2026-11-18
    competitor: "forum-x.com author 'mike_b' — 4 threads in the top, 9–14 months old"
    threads:
      - n: 1
        title: "Ikaria juice after 8 weeks — my honest results"
        angle: my-results
        forum: forum-x.com
        status: todo          # todo → written YYYY-MM-DD → published <URL>
```

When the user publishes, `work-log` logs each thread as a page (content type `forum-experience`, sub-ID per thread). **In 5–10 days run `forumscan` again with `--mine`**: which of the user's threads got into the block or the top, which competitor threads they pushed out, which threads need an update or a new angle. Put the recheck into the check queue (Pro) or say the date (Free).

## What to tell the user when they first meet the method

Two lines, in their language: "Rumer's forum cluster: we look at which competitor threads reached the top for your query, then post several fresh threads with your own experience, each from a new angle. Fresh threads push out old ones, and several threads on one query take more places in Google's 'Discussions and forums' block." Then step 1.
