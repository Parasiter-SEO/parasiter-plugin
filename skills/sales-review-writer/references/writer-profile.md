# Writer profile — fill once, reuse in every article

The profile holds everything that does not change from article to article, so the skill asks only for what is new (product, link, deal, platform). File name: `parasite-seo-writer.md`, kept where the assistant can read it in every chat:

- **Claude.ai:** a Project (e.g. "PARASITER") — add the file to the Project's files; start article chats inside that Project.
- **Claude Code / Cowork:** the user's project folder, next to `parasite-seo-profile.md`.
- **Other assistants:** custom instructions / knowledge files of the assistant.

## How the skill uses it

1. Before Step 1, look for `parasite-seo-writer.md` (project files, folder, or pasted in the chat).
2. Found → use it silently; ask only for the article-specific inputs. Say in one line which author and style it uses.
3. Not found → offer the one-time setup ("2 minutes, then every article starts faster"), ask the questions below in one message, and return the filled file as a copy-ready block with a line on where to save it. If the user wants to skip, ask only the author minimum (name, role, why trust).
4. When the user adds a product link or changes a rule during work, offer to add it to the profile.

## Template

```markdown
# Writer profile (PARASITER)
Updated: YYYY-MM-DD

## Author (used in every author block)
- Name / pen name: …
- Role / position: … (e.g. "SEO specialist, 20 years in SEO and affiliate marketing")
- Why trust me: … (real experience, numbers, projects — facts only)
- What I usually do for an article: … (compare packages and terms, study complaints, test when I really have the product)
- Hands-on experience with products: only when stated per article
- Author photo: [link or file name] (real photo, used as the author image)
- Short bio for forums (1–2 lines): …

## Default publishing
- Main platforms: …
- Countries / content language: …
- Tone: expert blog / friendly forum / neutral press — default: …

## Affiliate links library
| Product | Affiliate link | Best landing (order / bundle page) | Network | Notes |
|---|---|---|---|---|

## Disclosure (pasted at the end of every article)
"…"

## CTA style
- Button texts I like: …
- Words to avoid: …

## Images
- Style: (e.g. graphite background, blue + cyan accents, clean cards) or "match the platform"
- Brand mark / watermark: none / …
- Generator I use for photo-like images: ChatGPT / Gemini / Midjourney / …

## My rules (added over time)
- …
```

Never store passwords, API keys or payment details in the profile.
