# Exclusions — stop types and blacklist (local copy)

The live list is on the PARASITER server (`exclusions_get`) and is extended by the author; it also returns the `dead` platforms (marked dead by the author, or found dead in any user's scan in the last 30 days). **With a key, always use the server list** (save its answer as `exclusions.json` and pass it to `platformscan.py --exclusions exclusions.json`). This file is the fallback when there is no key or the server is unreachable; the scan always merges it with the server list.

Match rule: the page's host equals the domain or ends with `.domain`; if the entry has a path, the URL path must start with it. `*` is a wildcard inside a host; `type:<type>` matches the platform type the scan detects.

Results that match are **not checked live and never shown** — only counted in the scan summary ("skipped by stop / black list: N"). The user may add their own exclusions in their profile; pass them with `--exclude domain[/path],…`.

## Stop types — never shown

| Match | Reason |
|---|---|
| `youtube.com` | Video platform — not a page we publish a review on |
| `youtu.be` | YouTube short links |
| `s3.amazonaws.com` | Amazon S3 file storage — files in storage buckets, not a platform (PDFs on S3 included) |
| `*.s3.amazonaws.com` | Amazon S3 buckets |
| `*.s3.*.amazonaws.com` | Amazon S3 regional buckets |
| `*.s3-*.amazonaws.com` | Amazon S3 regional buckets (old naming) |
| `quora.com` | Q&A — not used for parasite pages |
| `type:q&a` | Any question-and-answer platform |
| `answers.com` | Q&A |
| `justanswer.com` | Q&A |
| `answers.yahoo.com` | Q&A |
| `stackexchange.com` | Q&A |
| `stackoverflow.com` | Q&A |
| `ask.fm` | Q&A |

**PDFs are allowed.** A PDF is a normal finding: type "document / PDF", the PDF's host is the platform. The only PDFs excluded are abuse: PDFs in other organisations' upload folders (`wp-content/uploads`, contact-form and upload-plugin files, `uploads` on `.edu` / `.gov` sites) and PDFs on S3 (stop type above). The scan skips those as "abuse".

## Blacklist — sites that don't work for us

| Match | Reason |
|---|---|
| `fitness.com/forum` | Forum no longer keeps affiliate posts |
| `force11.org` | Event pages — has not accepted new ones for a long time |
| `community.synology.com` | The forum deleted SEO posts long ago |
| `blogspot.com` | Whole domain excluded |
| `vocal.media` | Does not let us publish |
| `tudocelular.com` | Does not accept new registrations |
| `galaxus.ch/forum` | Forum posts removed |
