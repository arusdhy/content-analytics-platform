import psycopg2
from app.utils.config import DB_CONFIG


def save_video(data):
    """
    Saves extracted YouTube video data into PostgreSQL
    """

    try:
        # Connect to database
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # SQL INSERT query (MUST be inside triple quotes)
        query = """
        INSERT INTO videos (
            video_id,
            title,
            views,
            likes,
            comments,
            duration,
            upload_date,
            description
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Execute query with extracted data
        cur.execute(query, (
            data.get("video_id"),
            data.get("title"),
            data.get("views"),
            data.get("likes"),
            0,  # comments placeholder (since not extracted yet)
            data.get("length"),
            data.get("publish_date"),
            data.get("description")
        ))

        # Commit changes
        conn.commit()

        print("Database insert successful!")

    except Exception as e:
        print("Database error:", e)

    finally:
        # Always close connection
        if 'conn' in locals():
            conn.close()