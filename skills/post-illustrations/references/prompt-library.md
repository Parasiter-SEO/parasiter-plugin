# Prompt library

## Rumer's templates

The author's way: DALL·E, realistic photos, the real products the article is about; infographics carry the facts. Horizontal, 700 px JPG.

**Cover — real product, realistic photo (DALL·E)**
"Realistic photograph of [exact product: container shape, color, label colors and text as on the real product], standing on [real setting that fits the use: kitchen counter / gym bench / bathroom shelf / desk], natural daylight, shallow depth of field, sharp label, no people, no text overlay, horizontal 16:9, photorealistic, high detail."

**Best-of cover — the real products together**
"Realistic photograph of [N] supplement products side by side on a clean table: [product 1 look], [product 2 look], [product 3 look]… labels facing the camera, even soft light, editorial product photography, no people, no added text, horizontal 16:9, photorealistic."

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

Infographic text is exact and short — render with code where possible; from a generator, check every letter and number.

## Style blocks (pick one per series, reuse in every prompt)

| Style | Block |
|---|---|
| Clean editorial | "clean editorial product photography, soft daylight, neutral light background, shallow depth of field, realistic, high detail" |
| Flat illustration | "flat vector illustration, bold simple shapes, limited palette of 3 colors, clean lines, no gradients" |
| Lifestyle real | "authentic lifestyle photo, natural home setting, candid, warm natural light, realistic skin and textures, no studio look" |
| Infographic | "clean infographic layout, white background, one accent color, simple icons, clear hierarchy, lots of whitespace" |
| A4 facts sheet | "A4 vertical fact sheet, green and white palette, header band, table section, icon bullets, print-ready look" |

## Generic templates

**Hero / cover (16:9)**
"[product] [what it is] held in a hand / on a kitchen table, [context of use], [style block], 16:9, no text"
Negative: "no logos other than the product's own, no extra text, no watermark, no distorted hands".

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
- Negative instructions for hands, extra logos, watermarks.
- Same style block across the whole article/series.
