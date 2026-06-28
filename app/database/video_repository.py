# Handles database operations for YouTube video data
# Responsible for inserting extracted video data into PostgreSQL
import psycopg2
from app.utils.config import DB_CONFIG
from app.utils.logger import logger

def save_video(data):

    #Inserts YouTube video data into PostgreSQL database
    conn = None
    cur = None

    video_id = data.get("video_id")

    try:
        logger.info(f"Connecting to DB for video_id: {video_id}")

        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        query = """
        INSERT INTO videos (
            video_id,
            title,
            views,
            likes,
            duration,
            upload_date,
            uploader,
            description
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cur.execute(query, (
            data.get("video_id"),
            data.get("title"),
            int(data.get("views") or 0),
            int(data.get("likes") or 0),
            int(data.get("duration_secs") or 0),
            data.get("publish_date"),
            data.get("author"),
            data.get("description"),
        ))

        conn.commit()
        logger.info(f"DB insert successful for video_id: {video_id}")


    except Exception as e:
        if conn:
            conn.rollback()

        logger.error(f"DB insert failed for {video_id}: {str(e)}")
        raise Exception(f"Database insert failed: {str(e)}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        logger.info(f"DB connection closed for video_id: {video_id}")