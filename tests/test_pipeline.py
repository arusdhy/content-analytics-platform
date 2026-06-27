from app.collectors.youtube_extractor import extract_youtube_data
from app.database.video_repository import save_video

def run_pipeline():
    url = input("Paste YouTube Shorts URL: ")

    print("\nExtracting data...\n")

    data = extract_youtube_data(url)

    # STEP 1: check if extraction failed
    if "error" in data:
        print("ERROR:", data["error"])
        return

    print("\nExtraction successful!")
    print("Title:", data["title"])
    print("Views:", data["views"])

    print("\nSaving to database...")

    # STEP 2: save to DB
    save_video(data)

    print("\nSUCCESS: Video saved to database!")

if __name__ == "__main__":
    run_pipeline()