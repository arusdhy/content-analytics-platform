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