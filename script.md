# Scripts: Collection Workflow

## 1. YouTube — `fetch_youtube.py`

Uses YouTube Data API v3 (channel + search endpoints) + `youtube-transcript-api`
for captions.

```bash
pip install google-api-python-client youtube-transcript-api --break-system-packages
export YOUTUBE_API_KEY="your_key"
python fetch_youtube.py
```

Output: `research/youtube-transcripts/<author_slug>/<date>_<title-slug>.md`
(metadata + description + full transcript per video).

Note: some channels disable captions — script writes a placeholder note
when no transcript is available; fall back to manual notes in `research/other/`.

## 2. LinkedIn — `fetch_linkedin_posts.py` (URL-based)

No public API for reading other users' posts, so this fetches specific
post URLs you've already collected (e.g. by browsing each creator's profile
and copying post links).

```bash
pip install requests beautifulsoup4 --break-system-packages
```

1. Open `scripts/post_urls.txt` and add post URLs under each `# author-slug` header.
2. Run:
   ```bash
   python scripts/fetch_linkedin_posts.py
   ```
3. Output: `research/linkedin-posts/<author-slug>/<post-id>.md`

**Important**: LinkedIn frequently blocks unauthenticated requests or only
serves limited Open Graph metadata (title/description), not full post text.
When that happens, the script writes a stub file flagging "Fetch failed" or
"No description extracted" — open the URL manually in a browser and paste
the post content into the `## Content` section. This script is a time-saver
for organizing/labeling, not a full scraper.

## 3. Repo structure

```
research/
  sources.md                 <- expert list, links, annotations
  linkedin-posts/
    <author-slug>/
      <date>-<slug>.md
  youtube-transcripts/
    <author-slug>/
      <date>_<title-slug>.md
  other/
    <misc files: podcast notes, screenshots, PDFs>
```

## 4. Suggested cadence

Run `fetch_youtube.py` weekly (cron or GitHub Actions) to keep transcripts
current. Commit outputs directly — they're markdown, diff-friendly.
