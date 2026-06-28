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
    
    # Validate YouTube URL
    if not url.startswith(("https://www.youtube.com/", "https://youtube.com/", "https://youtu.be/")):
        st.error("Please enter a valid YouTube URL.")
        st.stop()

    try:
        with st.spinner("Extracting video data..."):
            # CALL BACKEND (ENDPOINT)
            response = requests.post(  #backend POST
                EXTRACT_ENDPOINT,
                params={"url": url},
                timeout=30
            )

            if response.status_code != 200:
                st.error(f"Backend error: {response.status_code}")
                st.stop()

            try:
                data = response.json()
            except Exception:
                st.error("Invalid JSON response from backend")
                st.stop()

    except requests.exceptions.RequestException as e:
        st.error(f"Backend not reachable.\n\n{e}")
        st.stop()


    # Handle API response
    if data.get("status") == "new":

        st.success("Video extracted and saved!")

    elif data.get("status") == "exists":

        st.warning("Video already exists in database")

    elif data.get("status") == "error":

        st.error(data.get("message", "Unknown error"))

    video = data.get("data")

    if video:

        st.json(video)

        df = pd.DataFrame([video])
        st.dataframe(df)

        #CSV DOWNLOAD FEATURE
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download CSV (This Video)",
            data=csv,
            file_name="youtube_video_data.csv",
            mime="text/csv"
        )
#DOWNLOAD FULL DATASET FROM DATABASE
st.divider()
st.subheader("📦 Export Full Dataset (Database)")

if st.button("Download ALL Stored Videos CSV"):

    try:
        with st.spinner("Fetching full dataset from database..."):

            response = requests.get(f"{API_BASE_URL}/export_all", timeout=30)

            if response.status_code != 200:
                st.error(f"Backend error: {response.status_code}")
                st.stop()

            data = response.json()

            if data.get("status") != "success":
                st.error("Failed to fetch dataset")
                st.stop()

            records = data.get("data", [])

            if not records:
                st.warning("No data found in database")
                st.stop()

            # Convert to DataFrame
            df = pd.DataFrame(records)

            st.success(f"Exported {len(df)} videos from database")

            st.dataframe(df)

            # Convert to CSV
            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="📥 Download FULL CSV (All Videos)",
                data=csv,
                file_name="youtube_full_dataset.csv",
                mime="text/csv"
            )

    except requests.exceptions.RequestException as e:
        st.error(f"Backend not reachable:\n{e}")