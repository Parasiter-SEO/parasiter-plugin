# Search footprints

Combine a footprint with niche words ("car forum", "fitness", "gardening", the product category). Run in the target country. Add `-site:` for domains already used.

## Forum engines

| Engine | URL / text footprints |
|---|---|
| XenForo | `inurl:"index.php?threads/"`, `inurl:/threads/ "Log in or Register"`, `"Forum software by XenForo"` |
| ProBoards | `site:proboards.com [niche]`, `inurl:/board/ [niche]` |
| Freeforums | `site:freeforums.net [niche]` |
| phpBB | `inurl:viewtopic.php [niche]`, `"Powered by phpBB"` |
| vBulletin | `inurl:showthread.php [niche]`, `inurl:forumdisplay.php` |
| wpForo / bbPress | `inurl:/community/ [niche]`, `inurl:/forums/topic/ [niche]` |
| Invision (IPS) | `inurl:"index.php?/topic/"`, `inurl:/forum/ "Invision Community"` |
| Discourse | `inurl:/t/ [niche] "Discourse"` |

## Profiles that index

Some forum and community profiles index and show in "Discussions and forums"; sometimes the bio allows text and a link:
- `inurl:member.php?u= [niche]`, `inurl:member.php?action=profile`
- `inurl:/members/ [niche]`, `inurl:/profile/ [niche] forum`
Many are empty profiles — test before investing.

## Communities on big domains

- `site:[bigbrand].com inurl:community`, `inurl:discussions`, `inurl:forum`
- Old company communities (support forums, product communities) often keep ranking old posts.

## Open publishing

- `"write a story" OR "publish your article" [niche]`
- `"create your page" fundraising`, `"create event" free [city/niche]`
- Document/flipbook hosts: `"upload your PDF" flipbook`, `"publish document" free`

## Checking what ranks

- `[product] reviews` / `[product] vs [competitor]` / `[product] complaints` → collect non-brand domains in the top 20.
- `site:domain.com [product]` → does this platform already rank pages for the niche?
- `site:domain.com` sorted by recent (Tools → past week) → are fresh posts indexed?
