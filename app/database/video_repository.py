# Database layer for YouTube video data
# Responsible for inserting extracted video data into PostgreSQL
import psycopg2
from app.utils.config import DB_CONFIG
from app.utils.logger import logger

# CHECK IF VIDEO EXISTS
def get_video_by_id(video_id):

    conn = None
    cur = None

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("SELECT * FROM videos WHERE video_id = %s", (video_id,))
        row = cur.fetchone()

        return row

    except Exception as e:
        logger.error(f"DB fetch error: {e}")
        return None

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# INSERT NEW VIDEO
def save_video(data):

    conn = None
    cur = None

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        query = """
        INSERT INTO videos (
            video_id, title, views, likes,
            duration, upload_date, uploader, description
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

    except Exception as e:
        logger.error(f"DB insert error: {e}")
        raise

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# UPDATE VIDEO
def update_video(data):

    conn = None
    cur = None

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        query = """
        UPDATE videos
        SET title=%s, views=%s, likes=%s,
            duration=%s, upload_date=%s,
            uploader=%s, description=%s
        WHERE video_id=%s
        """

        cur.execute(query, (
            data.get("title"),
            int(data.get("views") or 0),
            int(data.get("likes") or 0),
            int(data.get("duration_secs") or 0),
            data.get("publish_date"),
            data.get("author"),
            data.get("description"),
            data.get("video_id"),
        ))

        conn.commit()

    except Exception as e:
        logger.error(f"DB update error: {e}")
        raise

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()