---
name: post-illustrations
description: Plan and write image-generator prompts for parasite SEO and affiliate posts — hero/cover image, product-in-hand, comparison card, key-facts infographic, price/bundle visual, Facebook post series — matched to the content type and platform, in one consistent style. Use when the user needs images, a cover, an infographic or visuals for a review, comparison or post, or when sales-review-writer hands off image ideas.
---

# Post Illustrations

## Work label (testing period)

Start every reply produced by this skill with one line naming it, so the user always sees which part of PARASITER is working:
`▸ PARASITER · post-illustrations`
If you called agents for this reply, add them after an arrow: `▸ PARASITER · post-illustrations → serp-analyst, product-researcher`. If you hand off to another skill, the next reply carries that skill's label. One line only, no other system talk.

Part of PARASITER by Rumer (Affiliate Credo).

The first image often becomes the Google snippet image and decides whether the page looks like a real author's work or another AI retelling. Stock photos say "nobody here". Custom images of the product, the comparison and the key facts say "someone actually did this".

Reply in the user's language; write prompts in English (generators follow English best).

## Step 1 — Inputs

- Article title and content type (single review, best-of, A vs B, experience, complaints, packages).
- Platform (decides count, size and format — see `references/platform-sizes.md`).
- Product name(s) and what they look like (bottle, device, app screen…). If the user has real product photos, use them as the base — real beats generated.
- Style: the user's saved series style if they have one; otherwise propose one from `references/prompt-library.md` and save it for the series.
- Generator they use (Midjourney, ChatGPT/DALL·E, Ideogram, Flux, Gemini, Canva…), so prompts fit its syntax.

## Step 2 — Plan the set

Propose 3–6 images, one line each: purpose + where it goes in the article.
Default set for an article: hero/cover → product in use/in hand → key-facts infographic → comparison card (for comparisons) → price/bundle visual near the main CTA.

## Step 3 — Write prompts

For each image use the matching template from `references/prompt-library.md`. Each prompt: subject, composition, style, lighting/colors, text on image (short, exact, in quotes — or none if the generator garbles text), aspect ratio, negative instructions.

Output:
```
1. Hero (16:9) — goes under the title
Prompt: …
Alt text: …
```

Then tips: which image to generate first, how to keep the style consistent (same style block in every prompt, same seed/reference image where the tool supports it), and to add real numbers/text in an editor rather than in the generator.

## Rules

- No fake people presented as real: no invented doctors, "customers", testimonials or before/after results. A generated person may appear only as an illustration, never labelled as a real user or expert.
- No fake certificates, badges, awards or "clinically proven" seals; no official brand logos used to imitate the merchant.
- Product shown as it really looks; no added features.
- Prices and claims on images only from verified facts, with a date if the image shows a price.
- Mark AI-generated images where the platform requires it.

> Author's note: Rumer's proven prompt templates go into `references/prompt-library.md` (section "Rumer's templates"). Until filled, the generic templates there are used.
