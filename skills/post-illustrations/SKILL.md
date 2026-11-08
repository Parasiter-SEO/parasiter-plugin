---
name: post-illustrations
description: "Plan and write image-generator prompts for parasite SEO and affiliate posts — hero/cover image, product-in-hand, comparison card, key-facts infographic, price/bundle visual, Facebook post series — matched to the content type and platform, in one consistent style — for agencies in the client's brand style (logo, colours, fonts, real product photos). Images cost $0: infographics are drawn by Claude in the chat; the cover is the real product photo or one ready prompt for free Gemini (ChatGPT / DALL·E only for users who already pay for it). Use when the user needs images, a cover, an infographic or visuals for a review, comparison or post, or when sales-review-writer hands off image ideas."
---

# Post Illustrations

## Work label (testing period)

Start every reply produced by this skill with one line naming it, so the user always sees which part of PARASITER is working:
`▸ PARASITER · post-illustrations`
If you called agents for this reply, add them after an arrow: `▸ PARASITER · post-illustrations → serp-analyst, product-researcher`. If you hand off to another skill, the next reply carries that skill's label. One line only, no other system talk.

## Plugin basis and Claude plan — RULE (№33)

Every answer here is PARASITER at work: this skill's steps, Rumer's rules, criteria and references — never general knowledge alone. Name the basis briefly where it matters ("by Rumer's rules", the checklist, score or reference used, "PARASITER platform base"). A request this skill doesn't cover → the right skill; nothing fits → one line "outside PARASITER's skills — I answer by Rumer's general rules", then "0 — menu". Full rule: `navigator/references/agents-and-plan.md`.

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

Every image: **horizontal, full article width, JPG 700 px wide** (700×394), light. Sizes and hosting by link: `references/platform-sizes.md`.

**Infographic files — RULE (№30).** Each infographic is a **separate `.jpg` file, exactly 700 px wide** (cards 700×394; a tall table 700 px wide, height by content), JPEG quality ~85, under ~150 KB, named in article order: `01-quick-facts.jpg`, `02-ingredients.jpg`, `03-which-one-fits.jpg`… Saved in the user's folder under `images/<article-slug>/` and handed over as files (download / open), each also shown in the chat. **Never** a `.md` file with images, never a small PNG preview, never a screenshot of the chat. Before handing over, check every file with code (format JPEG, width = 700) and fix it if not. In the article text mark where each goes: "[Image 2: 02-ingredients.jpg — insert here]".

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
   2. if a generated cover is needed — **one** ready prompt in a code block (it has the copy icon) and the link **[Open Gemini](https://gemini.google.com)**, made free there.
   **The reference photo is a screenshot, not a saved file:** product photos on shops are usually page backgrounds, so saving them is slow or impossible. Say: "Open the product page, take a screenshot of the product photo (Windows: **Win+Shift+S**, Mac: **Cmd+Shift+4**) and paste it straight into Gemini with **Ctrl+V** / **Cmd+V** — no need to save the file. Attach a screenshot of each product, then paste the prompt." Saving the image is the fallback.
3. Other generators — the user chooses from the table below; never a reason to buy anything.

### Where to make the cover

Show this table once (with the check date) so the user can choose; terms change — say "as checked on <date>":

| Tool | Free | Paid | Good for |
|---|---|---|---|
| **Gemini** (gemini.google.com) — default | yes; Google doesn't publish a daily number — the limit is compute-based, resets every 5 hours, with a weekly cap | Google AI Plus $4.99/mo (2× the limit), AI Pro $19.99/mo (4×) | every article; understands a pasted product screenshot as the reference |
| **ChatGPT** (image generation) | about 2–3 images per 24 h | Plus $20/mo — far more | text on images |
| **Canva** (Canva AI / Dream Lab + templates) | up to 20 AI uses a month (shared allowance) | Canva Pro about $15/mo ($144/yr): image generation without a separate cap (fair use) | finishing covers with a logo and fonts (agencies) |
| **Midjourney** | no free plan | Basic $10/mo (~200 fast minutes ≈ 200+ images) | the most "photo" look |

Checked 21–25 Oct 2026 (Gemini: compute-based limits, plans AI Plus / AI Pro; ChatGPT free ~2–3 / 24 h; Canva Free 20 AI uses / month, Pro $144 / yr; Midjourney Basic $10, no free plan). Never quote "20 images a day" for Gemini — Google publishes no such number. The same prompt works in all of them.

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
