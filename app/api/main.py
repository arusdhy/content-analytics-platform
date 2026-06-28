# FastAPI entry point for YouTube Content Analytics Platform
# Handles API requests, triggers extraction, and saves data to PostgreSQL
from fastapi import FastAPI
from app.collectors.youtube_extractor import extract_youtube_data
from app.database.video_repository import save_video, get_video_by_id
from app.utils.logger import logger
import pandas as pd


app = FastAPI()

#Endpoint: Takes YouTube URL, Extracts video data, Saves to PostgreSQL, Returns structured response.

@app.post("/extract")
def extract_video(url: str):

    logger.info(f"Incoming request: {url}")

    try:
        # STEP 1: Extract data from YouTube
        data = extract_youtube_data(url)

        # Handle extraction error
        if "error" in data:
            return {
                "status": "error",
                "message": data["error"],
                "data": None
            }

        video_id = data["video_id"]

        # STEP 2: Check if video already exists in DB
        existing = get_video_by_id(video_id)

        if existing:
            logger.info(f"DB hit: {video_id}")

            return {
                "status": "exists",
                "message": "Video already in database",
                "data": data
            }

    # STEP 3: Save NEW video to database
        try:
            save_video(data)
            logger.info(f"Saved new video: {video_id}")

        except Exception as e:
            logger.error(f"DB insert failed for {video_id}: {e}")

            return {
                "status": "error",
                "message": "Database insert failed",
                "data": None
            }

        # STEP 4: Return success response
        return {
            "status": "new",
            "message": "Video extracted and saved",
            "data": data
        }

    except Exception as e:
        # FIX: global safety net
        logger.error(f"Unexpected API error: {e}")
        return {
            "status": "error",
            "message": "Internal server error",
            "data": None
        }

#FEATURE: EXPORT FULL DATASET FROM DATABASE
@app.get("/export_all")
def export_all_videos():

    try:
        logger.info("Export request received")

        import psycopg2
        import pandas as pd
        from app.utils.config import DB_CONFIG

        # 🔥 SAME STYLE AS YOUR REPOSITORY (consistent architecture)
        conn = psycopg2.connect(**DB_CONFIG)

        df = pd.read_sql("SELECT * FROM videos", conn)

        conn.close()

        return {
            "status": "success",
            "data": df.to_dict(orient="records")
        }

    except Exception as e:
        logger.error(f"Export failed: {e}")

        return {
            "status": "error",
            "message": str(e),
            "data": []
        }