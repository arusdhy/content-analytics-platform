# FastAPI entry point for YouTube Content Analytics Platform
# Handles API requests, triggers extraction, and saves data to PostgreSQL
from fastapi import FastAPI
from app.collectors.youtube_extractor import extract_youtube_data #calling a function from youtube_extractor.py file
from app.database.video_repository import save_video
from app.utils.logger import logger
from app.utils.cache import get_cached_video, set_cached_video


app = FastAPI()

#Endpoint: Takes YouTube URL, Extracts video data, Saves to PostgreSQL, Returns structured response.
@app.get("/extract") 
def extract_video(url: str):

    logger.info(f"Incoming request: {url}")

    try: 
        data = extract_youtube_data(url)#extract data

        # Handle extraction failure
        if "error" in data:
            logger.warning(f"Extraction failed: {data['error']}")
            return {
                "status": "error",
                "message": data["error"]
            }

        video_id = data.get("video_id")

        #CACHE check: If video data is already cached, return it instead of saving to DB
        cached = get_cached_video(video_id)
        if cached:
            logger.info(f"Cache hit for video_id: {video_id}")
            return {
                "status": "success",
                "message": "Loaded from cache",
                "data": cached
            }
        logger.info(f"Cache miss: {video_id}")

        # SAVE TO DB
        try:
            save_video(data)
        except Exception as db_error:
            logger.error(f"DB error: {db_error}")

            return {
                "status": "error",
                "message": f"Database error: {str(db_error)}",
                "data": data
            }

        #STORE IN CACHE only after successful DB insert
        set_cached_video(video_id, data)
        logger.info(f"Success pipeline completed: {video_id}")

        return {
            "status": "success",
            "message": "Video successfully added",
            "data": data
        }

    except Exception as e:
        logger.exception(f"Unhandled error: {e}")
        return {
            "status": "error",
            "message": str(e)
        }