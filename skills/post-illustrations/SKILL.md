---
name: post-illustrations
description: Plan and write image-generator prompts for parasite SEO and affiliate posts — hero/cover image, product-in-hand, comparison card, key-facts infographic, price/bundle visual, Facebook post series — matched to the content type and platform, in one consistent style — for agencies in the client's brand style (logo, colours, fonts, real product photos). Images cost $0: infographics are drawn by Claude in the chat; the cover is the real product photo or one ready prompt for free Gemini (ChatGPT / DALL·E only for users who already pay for it). Use when the user needs images, a cover, an infographic or visuals for a review, comparison or post, or when sales-review-writer hands off image ideas.
---

# Post Illustrations

## Work label (testing period)

Start every reply produced by this skill with one line naming it, so the user always sees which part of PARASITER is working:
`▸ PARASITER · post-illustrations`
If you called agents for this reply, add them after an arrow: `▸ PARASITER · post-illustrations → serp-analyst, product-researcher`. If you hand off to another skill, the next reply carries that skill's label. One line only, no other system talk.

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
- "write the text" — the article itself
- "check the first screen" — audit before publishing

Part of PARASITER by Rumer (Affiliate Credo).

**Images accompany the text and make it easier to take in.** They are not decoration and not text pasted into a picture: a useful image shows what the paragraph next to it is about — facts, the headline idea, ingredients or features, benefits in short theses, a comparison, the prices — as an infographic. "A person holding a bottle" helps nobody. An article without images is not finished; a missing cover photo is a problem because the first image often becomes the Google snippet image.

Two kinds of images, every article:
1. **Cover photo** — a realistic photo of the real product being discussed (the user's own photo first; otherwise the merchant's real product shot as the reference, or a realistic generated photo of that exact product). Right under the title.
2. **Infographics** — 3–5 cards that carry the facts of the section they sit in: key facts / ingredients, pains → solution, benefits in theses, comparison table, prices and packages, verdict. Short text only (headings, theses, numbers), never paragraphs. `sales-review-writer` renders these with code as JPG when it can; otherwise this skill writes prompts for them.

Every image: **horizontal, full article width, JPG ~700 px wide** (700×394), light. Sizes and hosting by link: `references/platform-sizes.md`.

Reply in the user's language; write prompts in English (generators follow English best).

## Step 1 — Inputs

- Article title, content type and the sections (what each image will sit next to).
- Platform (count, and whether images go by upload or by link).
- Product name(s) and the real product photos: the user's own, or the merchant's product shot (link from `product-researcher`) — used as the cover and to describe the real look exactly. A generated cover only if no real photo fits — Gemini by default (below).
- **Agency role:** the client's brand kit from `clients/<slug>/client-brief.md` (logo, colours, fonts, real product photos, approved claims). Every infographic uses the client's colours and fonts; the logo only where the client allows it; real product photos first.

## How we work with images (say it once, short)

Images cost the user nothing. Explain it **once** per user (first article, or when they ask about images), in one line in the working language, then save `images_explained: yes` in `parasite-seo-profile.md` and don't repeat it:

> "How we work with images: infographics I draw myself, the cover is made free in Gemini from my prompt — 30 seconds."

1. **Infographics** (key facts, pains → solution, comparison, prices, verdict) — Claude draws them with code right in the chat: JPG ~700 px, exact text and numbers, $0. The only requirement is code execution turned on in Claude (Settings → Capabilities). Without it, say so once and give infographic prompts meanwhile.
2. **Cover** (a realistic photo of the product), in this order:
   1. the **real product photo** — the user's own, or the merchant's product shot (the link comes from `product-researcher` in `sales-review-writer`; otherwise ask the user for the product page);
   2. if a generated cover is needed — **one** ready prompt in a code block (it has the copy icon) and the link **[Open Gemini](https://gemini.google.com)**: the user makes it there for free (about 20 images a day on a free Google account; Google's limits change) and saves it.
3. **DALL·E / ChatGPT** — only as the alternative for users who already pay for ChatGPT. Never the default, never a reason to buy anything.

### Where to make the cover

| Tool | Cost | When |
|---|---|---|
| **Gemini** (gemini.google.com) — default | free, ~20 images a day | every user, every article |
| ChatGPT (DALL·E / image generation) | paid ChatGPT plan for regular use | only if the user already pays for it; good with text on images |
| Midjourney, Canva (Magic Media + templates) | paid / free tier | only if the user or the agency already uses them (Canva for finishing covers with a client's logo and fonts) |

The same prompt works in all of them. Name Gemini first; mention the others only if the user asks or already has them.

## Step 2 — Plan the set

One line per image: what it shows + the section it goes next to. Default: cover photo (real product) → key facts / ingredients infographic → pains → solution or benefits in theses → comparison card → prices and packages card near the main CTA → verdict card (best-of: ranking card with #1 marked).

## Step 3 — Write prompts

- **Cover / product photos** — the real photo first; otherwise one prompt for Gemini (default; the same prompt works in ChatGPT / DALL·E): the exact product as it really looks (shape, color, label described from the real photo), real setting, natural light, horizontal 16:9, no added text, no people unless the user wants them.
- **Infographics** — prefer rendering with code (exact text, exact numbers). If prompts are needed: clean horizontal infographic, a heading + 3–6 short theses or a small table, large readable type, the product photo as a small element; give the exact text in quotes and tell the user to check and fix the lettering in an editor (generators garble text).

Output:
```
1. Cover photo (700×394) — under the title
Real photo: <merchant product image URL> — or, if none fits:
```
then the prompt in its own code block (copy icon) and the link [Open Gemini](https://gemini.google.com). Infographics 2–6: drawn in the chat as JPG (one line each in the plan, no prompt needed).
No alt text. Then one line on how to keep the style the same across the article (same style block, same reference photo).

## Rules

- No fake people presented as real: no invented doctors, "customers", testimonials or before/after results. A generated person may appear only as an illustration, never labelled as a real user or expert.
- No fake certificates, badges, awards or "clinically proven" seals; no official brand logos used to imitate the merchant.
- Product shown as it really looks; no added features.
- Prices and claims on images only from verified facts, with a date if the image shows a price.
- Mark AI-generated images where the platform requires it.

- No decorative images without information ("person holding a bottle"); every image carries the facts of its section.
