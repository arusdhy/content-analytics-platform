#YouTube Shorts Data Extractor Module

#This is the core data ingestion layer of the system.
import re
import yt_dlp
from datetime import datetime
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
    try:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        upload_date = info.get("upload_date")

        if upload_date:
            upload_date = datetime.strptime(upload_date, "%Y%m%d").strftime("%Y-%m-%d")

        return {
            "title": info.get("title") or "Unknown",
            "views": info.get("view_count") or 0,
            "likes": info.get("like_count") or 0,
            "description": info.get("description") or "",
            "duration_secs": info.get("duration") or 0,
            "author": info.get("uploader") or "Unknown",
            "publish_date": upload_date or None,
        }

    except Exception as e:
        return {"error": f"yt-dlp failed: {str(e)}"}

# STEP 3: MASTER PIPELINE
def extract_youtube_data(url):
# Main function: URL → structured dataset

    video_id = get_video_id(url)

    if not video_id:
        return {"error": "Invalid YouTube URL"}

    metadata = get_video_metadata(url)

    # Attach the extracted video ID
    metadata["video_id"] = video_id

    return metadata