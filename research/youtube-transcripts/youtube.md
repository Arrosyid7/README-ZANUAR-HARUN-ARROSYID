# YouTube Transcripts

Transcripts organized by author/channel, generated via `scripts/fetch_youtube.py`.

## Structure

```
youtube-transcripts/
  <author-slug>/
    <date>_<video-title-slug>.md
```

Each file contains:
- Video title, channel handle, video ID, URL, published date
- Description
- Full transcript (from captions, where available)

## Generating

```bash
pip install google-api-python-client youtube-transcript-api --break-system-packages
export YOUTUBE_API_KEY="your_key"
python scripts/fetch_youtube.py
```

This folder is currently empty — populate it by running the script above.
