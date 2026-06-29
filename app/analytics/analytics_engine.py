#Analytics Brain Engine

#Datbase reader functions, libraries
import pandas as pd
import numpy as np
import psycopg2
#Title analysis
import re
from collections import Counter


#Database connection function
def load_videos_from_db():
    conn = psycopg2.connect(
        dbname="content_db",
        user="postgres",
        password="password3",
        host="localhost",
        port="5432"
    )

    query = """
    SELECT title, views, likes, description, duration, upload_date
    FROM videos;
    """

    df = pd.read_sql(query, conn)
    conn.close()
    
    # Rename columns to match expected names
    df = df.rename(columns={
        "duration": "duration_secs",
        "upload_date": "publish_date"
    })

    return df
#Clean data
def clean_data(df):
    df = df.dropna()

    df["views"] = pd.to_numeric(df["views"], errors="coerce")
    df["likes"] = pd.to_numeric(df["likes"], errors="coerce")
    df["duration_secs"] = pd.to_numeric(df["duration_secs"], errors="coerce")

    df = df.dropna()

    return df

#Create engagement metrics
def add_engagement_metrics(df):
    df["like_rate"] = df["likes"] / df["views"]

    df["like_rate"] = df["like_rate"].replace([np.inf, -np.inf], 0)

    return df

#Title length
def title_length_stats(df):
    df["title_length"] = df["title"].apply(lambda x: len(str(x).split()))
    return df

#Common words
def get_top_keywords(df, top_n=5):
    words = []

    for title in df["title"]:
        title = str(title).lower()
        title = re.sub(r"[^a-zA-Z0-9 ]", "", title)
        words.extend(title.split())

    common = Counter(words).most_common(top_n)

    return [word for word, _ in common]

#Duration insights
def duration_insights(df):
    avg_duration = df["duration_secs"].mean()

    best_range = df[
        (df["duration_secs"] >= avg_duration - 10) &
        (df["duration_secs"] <= avg_duration + 10)
    ]

    return {
        "avg_duration": round(avg_duration, 2),
        "best_duration_range": [
            int(best_range["duration_secs"].min()),
            int(best_range["duration_secs"].max())
        ]
    }


#Time-based insights
def time_insights(df):
    df["publish_date"] = pd.to_datetime(df["publish_date"])

    df["day_of_week"] = df["publish_date"].dt.day_name()

    best_days = df.groupby("day_of_week")["views"].mean().sort_values(ascending=False)

    return {
        "best_upload_days": list(best_days.head(3).index)
    }

#Ranking insights
def ranking_insights(df):
    top_videos = df.sort_values(by="views", ascending=False).head(5)

    return {
        "top_videos": top_videos["title"].tolist()
    }


#Main function to run all analytics, insights function
def generate_insights():
    df = load_videos_from_db()
    df = clean_data(df)

    df = add_engagement_metrics(df)
    df = title_length_stats(df)

    keyword_data = get_top_keywords(df)
    duration_data = duration_insights(df)
    time_data = time_insights(df)
    ranking_data = ranking_insights(df)

    insights = {
        "best_like_rate": round(df["like_rate"].max(), 4),
        "average_views": int(df["views"].mean()),
        "average_likes": int(df["likes"].mean()),
        "top_title_keywords": keyword_data,
        "avg_title_length": round(df["title_length"].mean(), 2),
        **duration_data,
        **time_data,
        **ranking_data
    }

    return insights