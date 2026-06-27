#YouTube Shorts Data Extractor Module

#This is the core data ingestion layer of the system.
import re
import yt_dlp
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound
)

#This module is responsible for extracting structured data from a YouTube video URL.

#It performs the following:
#1. Extracts the video ID from a YouTube URL
#2. Fetches video metadata (title, views, likes, etc.)
#3. Retrieves transcript (if available)
#4. Combines everything into a single structured dictionary


# STEP 1: Extract Video ID
def get_video_id(url):
#Extracts YouTube video ID from URL.
#Works for shorts and standard yt video URLs.

    pattern = r"(?:v=|\/shorts\/|\/)([0-9A-Za-z_-]{11})"
    match = re.search(pattern, url)

    return match.group(1) if match else None


# STEP 2: Extract Metadata
def get_video_metadata(url):

# Uses yt-dlp to extract video metadata.
# More stable than pytube.

    ydl_opts = { }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        return {
            "title": info.get("title"),
            "views": info.get("view_count"),
            "likes": info.get("like_count") or 0,  # Some videos may have likes disabled
            "description": info.get("description"),
            "length": info.get("duration"),
            "author": info.get("uploader"),
            "publish_date": info.get("upload_date"),
        }


# STEP 3: Extract Transcript 
def get_transcript(video_id):
# Attempts to extract transcript safely.
# Returns None if not available.
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([t["text"] for t in transcript])
    except Exception:
        return None


# STEP 4: MASTER PIPELINE
def extract_youtube_data(url):
# Main function: URL → structured dataset

    video_id = get_video_id(url)

    if not video_id:
        return {"error": "Invalid YouTube URL"}

    metadata = get_video_metadata(url)
    transcript = get_transcript(video_id)

    # Attach pipeline outputs
    metadata["video_id"] = video_id
    metadata["transcript"] = transcript
    metadata["has_transcript"] = transcript is not None

    # Fallback safety (important for Shorts)
    if transcript is None:
        metadata["transcript_source"] = "none"
    else:
        metadata["transcript_source"] = "youtube_api"

    return metadata