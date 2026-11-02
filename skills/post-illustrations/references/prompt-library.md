# Prompt library

## Rumer's templates

The author's way: realistic photos of the real products the article is about; infographics carry the facts. Horizontal, 700 px JPG.

**Which generator.** Covers only — infographics are drawn by Claude with code (exact text, $0), the prompts below for them are a fallback when code execution is off.
1. **Gemini — default** (free, [gemini.google.com](https://gemini.google.com)). Write the prompt as plain sentences and name the shape in the text ("wide horizontal 16:9 image"); if it comes out square, the user crops it to 700×394. To keep the real look, the user can attach the merchant's product photo in Gemini and add: "Use the attached photo as the exact reference for the product's shape, colours and label."
2. **DALL·E / ChatGPT — second option**, only for users who already pay for ChatGPT. Same prompt; ask for a landscape (wide) image; attach the product photo the same way. Better than Gemini with a few words of text on the image.
3. Midjourney (add `--ar 16:9`) or Canva Magic Media — only if the user already uses them.

Give the user one prompt in a code block (copy icon) + the [Open Gemini](https://gemini.google.com) link. Add the DALL·E line only when the user said they use ChatGPT.

**Cover — real product, realistic photo**
Gemini (default):
"Create a wide horizontal 16:9 photorealistic photo of [exact product: container shape, color, label colors and text as on the real product], standing on [real setting that fits the use: kitchen counter / gym bench / bathroom shelf / desk]. Natural daylight, shallow depth of field, the label sharp and readable. No people, no added text, no watermark."
DALL·E / ChatGPT (second option): the same text + "Landscape (wide) format."

**Best-of cover — the real products together**
Gemini (default):
"Create a wide horizontal 16:9 photorealistic editorial product photo of [N] products side by side on a clean table: [product 1 look], [product 2 look], [product 3 look]… Labels facing the camera, even soft light. No people, no added text, no watermark."
DALL·E / ChatGPT: the same text + "Landscape (wide) format."

**Key facts / ingredients infographic**
Heading: "[Product] at a glance". 4–6 rows, each: small icon + 2–4 words ("Turmeric 500 mg — joint comfort"). Small real product photo on the right. Clean light background, one accent color, large readable type. Horizontal 16:9.

**Pains → solution**
Two columns: left "The problem" with 3 short pains, right "What [Product] does" with the matching 3 answers, arrows between them. Horizontal 16:9.

**Benefits in theses**
Heading + 4–5 benefit lines, each with an icon, max 6 words per line. Horizontal 16:9.

**Comparison card**
Table: [Product] vs 2–3 competitors × 4–5 rows (price, key ingredient/feature, guarantee, best for), the winner column highlighted. Horizontal 16:9.

**Prices and packages**
3 package columns (1 / 3 / 6), price per unit, "Best value" tag on the best one, "checked [date]" in small type. Horizontal 16:9.

Infographic text is exact and short — Claude renders these with code (the default); the layouts above are what the code draws. Only without code execution turn one into a prompt (Gemini first, DALL·E second) and tell the user to check every letter and number.

## Style blocks (pick one per series, reuse in every prompt)

| Style | Block |
|---|---|
| Clean editorial | "clean editorial product photography, soft daylight, neutral light background, shallow depth of field, realistic, high detail" |
| Flat illustration | "flat vector illustration, bold simple shapes, limited palette of 3 colors, clean lines, no gradients" |
| Lifestyle real | "authentic lifestyle photo, natural home setting, candid, warm natural light, realistic skin and textures, no studio look" |
| Infographic | "clean infographic layout, white background, one accent color, simple icons, clear hierarchy, lots of whitespace" |
| A4 facts sheet | "A4 vertical fact sheet, green and white palette, header band, table section, icon bullets, print-ready look" |

## Generic templates

Written for Gemini (plain sentences, "wide horizontal 16:9" in the text). For DALL·E / ChatGPT use the same text and name the shape ("landscape", "square", "portrait"); for Midjourney add `--ar`.

**Hero / cover (16:9)**
"Create a wide horizontal 16:9 image: [product] [what it is] held in a hand / on a kitchen table, [context of use], [style block]. No text."
Add at the end (Gemini and DALL·E take it as plain words): "No logos other than the product's own, no extra text, no watermark, natural hands."

**Product in use (4:3 or 1:1)**
"person using [product] at [situation], seen from [angle], focus on the product, [style block]"

**Comparison card (16:9)**
"split-screen comparison card, left: [product A] , right: [product B], 'VS' in the middle, [style block], clean background, space for labels" — add labels and numbers in an editor.

**Key facts infographic (4:5 vertical)**
"vertical infographic with 5 sections and simple icons for: [fact 1], [fact 2]…, [infographic style block]" — put exact text in an editor if the generator garbles letters.

**Price / bundle visual (1:1)**
"three product bundles side by side: 1, 3 and 6 units of [product], the 6-unit bundle highlighted, [style block], space for price labels"

**Facebook series (1:1 or 4:5)**
One style block, 5–10 images each on one benefit or tip: "[benefit] illustrated by [scene], [style block], large clear focal point".

## Prompt checklist
- Subject + composition + style block + light + aspect ratio.
- Text on image: short and in quotes, or none.
- "No …" sentences for hands, extra logos, watermarks (written as plain words: there is no separate negative-prompt field).
- Gemini first; DALL·E line only for users who already pay for ChatGPT.
- Same style block across the whole article/series.


## Brand covers and banners (agency role)

**Brand cover — the client's real product in use**
"Realistic photograph of [client product, exact look from the client's photo], used by [the client's audience in a real setting], natural light, colour palette with [brand colour 1] and [brand colour 2] accents in the scene, clean modern composition, no logos, no text overlay, horizontal 16:9, photorealistic."
Gemini by default (DALL·E if the agency pays for ChatGPT). Add the logo and title afterwards in Canva or the client's template — generators distort logos.

**Profile banner (LinkedIn 1584×396, YouTube 2560×1440 safe area 1546×423)**
"Wide minimal banner background for [industry] brand, [brand colour 1] to [brand colour 2] soft gradient, subtle [industry-relevant] shapes on the right, empty space on the left for text, no text, no logos, high resolution."
