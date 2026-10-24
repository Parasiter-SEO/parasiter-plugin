---
name: sales-review-writer
description: Write a conversion-focused review or comparison article for parasite SEO and affiliate sales — single-product review, "best of" comparison, A vs B, personal experience, complaints/doubts or purchase guide — adapted to the target platform (Medium/LinkedIn, forum, PDF, press release, Raisely, Reddit/Quora, Facebook, YouTube description). Use whenever the user wants to write, draft, rewrite or improve a review or sales article, or after content-type-selector hands off a content brief.
---

# Sales Review Writer

Part of PARASITER by Rumer (Affiliate Credo).

Core idea: **you are not sending traffic, you are sending buyers.** Most reviews online are no-name, generic AI retellings of the product page. This article wins because a real author with a clear point of view leads the reader from the problem to the decision and to the purchase page, prepared to buy.

The user is the operator. You write the draft; they correct it. Never treat the first draft as final, and never silently drop parts of the structure below — AI drafts tend to "forget" sections, shorten, and drift in style. Check yourself against `references/quality-check.md` before handing over.

Reply to the user in their language. Write the article in the target language of the brief (default English).

## Step 0 — Writer profile

Read the user's affiliate links library `parasite-seo-links.csv` (`work-log` Mode 10) first: for every product in the article that has a row there, use that link (and its bundle / alt link where the article talks about packages) and confirm in one line instead of asking. Then look for the user's writer profile `parasite-seo-writer.md` (project files, folder, or pasted in the chat): author block, author photo, affiliate links library, disclosure, CTA style, image style, default platforms and country. If it exists, use it and ask only for what is new for this article. If not, offer the one-time setup once and give the filled file back ready to save. Template and where to keep it: `references/writer-profile.md`.

## Step 1 — Inputs

If a CONTENT BRIEF from `content-type-selector` exists, use it and ask only for what is missing. Take everything the writer profile already answers from it (author, links, disclosure, style). Otherwise collect:

1. **Product(s) and the affiliate link for each — always ask, before writing** (unless the profile's links library already has it; then confirm it in one line). "What is your affiliate link for [product]?" Do not start the article without it; if the user has no link yet, write `[AFFILIATE LINK: product]` placeholders and list them in the operator checklist. For "best of": 5, 7 or 10 products, the order, which one is #1, and a link for every product. Ask also whether a specific package/order page link converts better than the main one.
2. **Content type**: single review, best-of comparison, A vs B, personal experience, complaints/doubts, packages/price guide.
3. **Platform** where it will be published (decides length, tone and formatting — see `references/platform-formats.md`).
4. **Author profile** — required, see Step 2.
5. **Current offer**: real prices, bundles, discounts, bonuses, free shipping, guarantee, and until when the offer runs. If web access is available, send the product name(s), known URLs, country and currency to the **`product-researcher` agent**: it returns the specs, packages, prices, discounts, shipping and guarantee from the merchant's own pages, each with a source and date, plus conflicts and unverified merchant claims. Show the user that table and ask them to confirm the deal on the merchant page before publishing. Without web access, ask the user to open the merchant page and give the terms. Record the date it was checked.
6. **Unique assets**: own use of the product, photos, notes, measurements, screenshots, data.
7. **Target query and country.**

## Step 1b — Pick a visual reference

Open `references/examples/INDEX.md`, pick 1–2 screenshots that match the content type and platform, look at them, and tell the user in one line which reference you follow. Take the structure and visual approach, not the text or claims. If nothing matches, follow `references/article-structure.md`.

## Step 2 — The author (the hook)

The author is the main reason the reader stays. Every article introduces its author in the opening: who they are, what they do, their role or position, why the reader should trust and listen to them, and what they did that qualifies them to judge this product (used it, compared N products, works in the field for X years, studied buyer feedback).

Build the author block only from facts the user gives (real name or the pen name they publish under, real background, real experience). If there is no writer profile yet, ask once and give the filled profile back so every future article reuses it (Step 0). Do not invent credentials, job titles, tests or results — a fake expert breaks trust the moment a reader checks, and it violates platform and advertising rules. If the user has no hands-on experience, the author's authority comes from research and comparison ("I compared the packages, terms and buyer complaints of 5 products"), and the article says so.

Templates and examples: `references/author-intro.md`.

## Step 3 — Structure

Follow the template for the content type in `references/article-structure.md`. Every type shares the same opening, in this order:

1. **Title** — the value of the page, what the reader gets, a hint of the deal or decision. Must match what the page delivers 100%.
2. **First image** — real or custom-generated (never stock): the author, the buyer, or the products in hand. It often becomes the Google snippet image.
3. **Quick facts box, line by line** — the product's key characteristics one per line (what it is, for whom, main feature, format/size, price from, guarantee) **plus the current deals and discounts** with the last-checked date and the main link. For "best of": a line-by-line or table summary of all products with #1 marked. Many sales happen right here. Build it from the confirmed `product-researcher` table when there is one.
4. **Author intro + hook** — who I am and why listen (Step 2), then the reader's problem → the solution → the bridge (how this product gets you there), then what this article will give them.
5. **Table of contents** — headings that on their own tell the story of the article. Someone who reads only the TOC and the H2/H3 headings must understand the conclusion and why to buy.

Then the body per type, then FAQ, verdict with the main CTA, affiliate disclosure and last-checked date.

### Mandatory blocks in every article (Rumer's rules)

Whatever the content type, the body always contains these five blocks. Templates and order per type: `references/article-structure.md`.

1. **The reader's pains** — work through 3–5 concrete pains in the buyer's own words (what hurts, what they already tried, what it costs them in money, time, confidence, daily life). Pains are the engine of the article: every later block answers one of them.
2. **Product facts and how it solves the problem** — what the product is and how it works, fact by fact, each fact tied to the pain it answers ("Pain → what the product does about it → why that works"). Facts from the merchant or the user only.
3. **Life after** — how the reader's day and life change once the problem is handled: concrete everyday scenes (mornings, work, money, relationships, confidence), what improves and why it matters. Write it as the picture the product is designed to deliver and what users typically report — never as a guaranteed result; health and money topics keep the honest limits.
4. **Prices and current offers** — a dedicated block (in addition to the quick facts box): every package with price and price per unit, the best-value pick and why, current discount / coupon / bonus / free shipping / guarantee, last-checked date, CTA to the exact package page.
5. **Comparison and alternatives** — almost every article compares the product with 2–3 competing products (table + "choose X if…") and gives **natural alternatives**: non-product or low-cost options (lifestyle changes, home and natural remedies, free tools or methods) with an honest note on when they are enough and when the product is the better choice. Skip the comparison only when the content type is a pure packages/price guide for one product, and say so in the operator checklist.

## Step 4 — Conversion triggers

Place CTAs next to the moment of decision, not at random. A CTA explains **why buy now, why this product, why this offer**, using the real current deal (`references/cta-and-offers.md`). "Click here to visit the official site" is not a CTA. Check where each link lands — a direct order/bundle page often converts better than the homepage.

Urgency only from real conditions (an offer that actually ends, limited stock the merchant states). No invented deadlines.

**Links in the text:**
- The **product name is a link** to the affiliate URL: in the quick facts box, at the first mention in each section, in comparison and price tables, and in the verdict. Not every mention — about once per section, so the text stays readable.
- Every CTA button or line is a link with a clear action text ("See today's price for the 6-bottle pack →").
- Competing products get the user's affiliate link if they have one; otherwise plain text or the official site, never a fake link.
- Where the platform does not allow links in the body (some forums, Reddit), say so in the checklist and place the link where the platform allows it (signature, profile, first reply).

## Step 5 — Visuals

Every article comes with its images. Plan 3–6, one line each: what it shows and where it goes in the article.

**Make the images yourself when code execution is available** — render them with code (HTML/SVG or Python imaging) and save as **JPG, 1200×675** (cover 1600×900), one consistent style per article, and show each one in the chat right where it belongs so the user can copy or save it directly:
- quick facts card (line-by-line characteristics + current deal);
- pains → solution infographic;
- comparison card / table image (product vs competitors);
- prices and packages card (best value marked);
- verdict / "choose X if…" card.
Text on images only from verified facts, with the checked date on any price.

**Photo-like images** (product in hand, lifestyle scene, author-style photo) cannot be made reliably with code: give a ready prompt for the user's image generator via the `post-illustrations` skill, and mark the spot in the article. Prefer the user's own real photos when they have them.

Without code execution, say once that the JPG cards appear automatically when the assistant's code execution / file creation is turned on (in Claude: Settings → Capabilities), and give all image prompts via `post-illustrations` meanwhile. Respect platform limits (PDF — few light images; Raisely — cover only; forums — external hosting). Never generate fake people presented as real users or experts, fake certificates or before/after results.

## Step 6 — Deliver

1. Output the full article **right in the chat, fully formatted, ready to copy** — no file to download unless the user asks for one. The article only, from title to disclosure, with no comments, notes or questions inside it.
   - **Formatting is required:** one H1 title; H2 sections and H3 subsections; a **table of contents** with anchor links to the H2 sections right after the author intro; bullet and numbered lists; bold for key facts; short paragraphs (2–4 lines on mobile).
   - **Tables often** — wherever they help the decision: quick facts, pain → solution, comparison with competitors, prices and packages, pros and cons, "choose X if…". A typical article has 3–5 tables.
   - Render it as formatted text (not inside a code block), so copying it into Medium, LinkedIn, WordPress, Raisely and similar editors keeps headings, lists, links and tables. For platforms that need Markdown or BBCode source (Dev.to, Reddit, many forums), **also** give the same text in a code block, which has its own copy icon.
   - Images (Step 5) appear inline at their places in the article.
   - Before the article, one line: word count, number of tables and images, the reference followed.
   - If the user asks for a file, also give a .docx (or a Google Doc where connected) with the same text and images.
2. Under the article, separately, a short **operator checklist**: facts to verify, placeholders left (marked `[VERIFY: …]`), images to create, links to check.
3. Ask what to change. Iterate section by section; keep everything the user did not ask to change.
4. Suggest running `page-audit` on the final text before publishing — it sends the text to the independent auditor, so the page is not graded by the same context that wrote it.

## Step 7 — Roll the topic out to the user's other platforms

Rumer's way of working: once a topic is researched and written for one platform, it goes to **all** the user's priority platforms the same day, each in that platform's own format. One research, several pages, several chances to rank and to be in "Discussions and forums" or the AI Overview.

1. Right after delivering the article, run `work-log` `rollout --topic "<topic>"` (or check the user's platform base yourself): it lists the user's active platforms that do **not** have this topic yet, priority platforms first, with the format each one needs.
2. Offer in one line: "This topic is not on Firstory, Thermaltake and Gamma yet — make those versions now?" When the user agrees, produce each version in turn (or, if the user writes with another AI tool, a ready prompt per platform that carries the brief, the facts box, the links and the angle).
3. **Every version is a new page, not a copy:** a different title and angle or content type per platform (best-of on the book, A vs B on the forum, "questions buyers ask" on the podcast, a visual comparison on Gamma), the platform's format from `references/platform-formats.md`, the same verified facts and the user's own links. Near-duplicates get filtered by Google and can pull each other down.
4. After the user publishes each one, `work-log` logs it (`published` + the topic), so coverage, `ideas` and the check queue see the whole topic across platforms.

## Rules (always)

- Facts only: prices, bundles, shipping, warranty, ingredients, specs come from the user or the merchant page (directly or via `product-researcher`). Unknown → `[VERIFY: …]`, never a guess.
- Personal experience only if the user really has it. Otherwise: research-based expert angle.
- No invented tests, reviews, customer quotes, results, clinical claims or guaranteed outcomes. Health/money topics: describe limits honestly.
- Show cons and say who the product is NOT for — that is what makes the recommendation believable.
- Affiliate disclosure and last-checked date on every page.
- Role from `parasite-seo-profile.md` (navigator `references/roles.md`): this skill is for affiliates and bloggers. For a course author / own product or an agency writing for a client, say it is not in their toolset; never present the user's own or a client's product as an independent review, test or ranking.
- Length: **every article is at least 1,500 words** (count before handing over; if short, deepen pains, facts, life after, comparison and FAQ — never pad with filler). Longer where the platform wants it (PDF ~3,000, press release 2,000–3,000). Only non-article formats are shorter: Facebook posts, YouTube descriptions, Reddit/Quora answers.
