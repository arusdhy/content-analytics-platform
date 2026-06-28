# Basic UI setup for Streamlit
import streamlit as st
import requests
import pandas as pd  # added for proper table 'display'

API_BASE_URL = "http://127.0.0.1:8000"
EXTRACT_ENDPOINT = f"{API_BASE_URL}/extract"

# Page setup
st.set_page_config(page_title="YouTube Analytics", layout="wide")

st.title("📊 YouTube Shorts Analytics Platform")
st.write("Paste a YouTube Shorts URL to extract data insights")

st.divider()

# Input box
url = st.text_input("Enter YouTube Shorts URL")

# VALIDATION 
if st.button("Extract Data"):

    if not url:
        st.error("Please enter a valid URL")
        st.stop()
    
    #validating the link to check if it is a youtube link or not
    if not url.startswith(("https://www.youtube.com/", "https://youtube.com/", "https://youtu.be/")):
        st.error("Please enter a valid YouTube URL.")
        st.stop()

    try:
        with st.spinner("Extracting video data..."):

            response = requests.get(
                EXTRACT_ENDPOINT,
                params={"url": url},
                timeout=30
            )

            if response.status_code != 200:
                st.error(f"Backend error: {response.status_code}")
                st.stop()

            try:
                data = response.json()
            except ValueError:
                st.error("Invalid response from backend.")
                st.stop()

    except requests.exceptions.RequestException as e:
        st.error(f"Backend not reachable.\n\n{e}")
        st.stop()


    # Handle API response
    if data.get("status") == "success":

        st.success("Video extracted successfully!")
        video = data["data"]

        views = f"{video.get('views', 0):,}"
        likes = f"{video.get('likes', 0):,}"

        duration = video.get("duration_secs", 0)
        minutes = duration // 60
        seconds = duration % 60
        duration_formatted = f"{minutes}:{seconds:02}"
        if duration == 0:
            duration_formatted = "Unknown"

        st.subheader("📹 Video Overview")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("**Title:**", video.get("title"))
            st.write("**Author:**", video.get("author"))

        with col2:
            st.write("**Views:**", views)
            st.write("**Likes:**", likes)

        with col3:
            st.write("**Duration:**", duration_formatted)
            st.write("**Publish Date:**", video.get("publish_date"))

        st.subheader("📝 Description")
        st.write(video.get("description"))

        st.divider()

        st.subheader("📊 Raw Data Table")

        df = pd.DataFrame([video])

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.error(data.get("message", "Something went wrong"))