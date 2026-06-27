#Basic FastAPI setup
from fastapi import FastAPI
from app.collectors.youtube_extractor import extract_youtube_data
from app.database.video_repository import save_video

app = FastAPI()

@app.get("/extract")
def extract_video(url: str):

    data = extract_youtube_data(url)

    if "error" in data:
        return {
            "status": "error",
            "message": data["error"]
        }

    save_video(data)

    return {
        "status": "success",
        "data": data
    }