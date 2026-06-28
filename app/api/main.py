# FastAPI entry point for YouTube Content Analytics Platform
# Handles API requests, triggers extraction, and saves data to PostgreSQL
from fastapi import FastAPI
from app.collectors.youtube_extractor import extract_youtube_data #calling a function from youtube_extractor.py file
from app.database.video_repository import save_video

app = FastAPI()

#Endpoint: Takes YouTube URL, Extracts video data, Saves to PostgreSQL, Returns structured response.
@app.get("/extract") 
def extract_video(url: str):

    try: 
        data = extract_youtube_data(url)

        # Handle extraction failure
        if "error" in data:
            return {
                "status": "error",
                "message": data["error"]
            }

        #DB INSERT
        try:
            save_video(data)
        except Exception as db_error:
            return {
                "status": "error",
                "message": f"Database error: {str(db_error)}",
                "data": data
            }

        return {
            "status": "success",
            "message": "Video successfully added",
            "data": data
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Server error: {str(e)}"
        }