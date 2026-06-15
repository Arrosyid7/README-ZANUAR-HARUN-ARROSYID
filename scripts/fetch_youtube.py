"""
Fetch latest videos + transcripts for each expert's YouTube channel.

Requirements:
    pip install google-api-python-client youtube-transcript-api --break-system-packages

Setup:
    - Get a YouTube Data API v3 key: https://console.cloud.google.com/apis/credentials
    - export YOUTUBE_API_KEY="your_key_here"

Usage:
    python fetch_youtube.py
"""

import os
import json
import re
from pathlib import Path
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

API_KEY = os.environ.get("YOUTUBE_API_KEY")
MAX_VIDEOS_PER_CHANNEL = 5

# channel handles (resolve to channel IDs via the API's "forHandle" param)
CHANNELS = {
    "simon_hoiberg": "@SimonHoiberg",
    "microconf": "@MicroConf",
    "jonathan_rintala": "@JonathanRintala",
    "dan_martell": "@DanMartell",
    "saastr": "@SaaStr",
    "founderpath": "@NathanLatka",
    "josh_braun": "@JoshBraun",
    "alex_hormozi": "@AlexHormozi",
}

OUT_DIR = Path(__file__).resolve().parent.parent / "research" / "youtube-transcripts"


def slugify(text):
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[\s_]+", "-", text)


def get_channel_id(youtube, handle):
    resp = youtube.channels().list(part="id", forHandle=handle).execute()
    items = resp.get("items", [])
    return items[0]["id"] if items else None


def get_latest_videos(youtube, channel_id, max_results=MAX_VIDEOS_PER_CHANNEL):
    resp = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        order="date",
        maxResults=max_results,
        type="video",
    ).execute()
    return resp.get("items", [])


def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi().fetch(video_id)
        return "\n".join(snippet.text for snippet in transcript)
    except Exception as e:
        return f"[No transcript available: {e}]"


def main():
    if not API_KEY:
        raise SystemExit("Set YOUTUBE_API_KEY environment variable first.")

    youtube = build("youtube", "v3", developerKey=API_KEY)

    for author_slug, handle in CHANNELS.items():
        print(f"Fetching: {handle}")
        channel_id = get_channel_id(youtube, handle)
        if not channel_id:
            print(f"  Could not resolve channel ID for {handle}")
            continue

        videos = get_latest_videos(youtube, channel_id)
        author_dir = OUT_DIR / author_slug
        author_dir.mkdir(parents=True, exist_ok=True)

        for video in videos:
            video_id = video["id"]["videoId"]
            title = video["snippet"]["title"]
            published = video["snippet"]["publishedAt"]
            description = video["snippet"]["description"]

            transcript_text = get_transcript(video_id)

            out_file = author_dir / f"{published[:10]}_{slugify(title)[:60]}.md"
            content = (
                f"# {title}\n\n"
                f"- Channel: {handle}\n"
                f"- Video ID: {video_id}\n"
                f"- URL: https://www.youtube.com/watch?v={video_id}\n"
                f"- Published: {published}\n\n"
                f"## Description\n\n{description}\n\n"
                f"## Transcript\n\n{transcript_text}\n"
            )
            out_file.write_text(content, encoding="utf-8")
            print(f"  Saved: {out_file.name}")


if __name__ == "__main__":
    main()
