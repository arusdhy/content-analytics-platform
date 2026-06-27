# Basic UI setup for Streamlit
import streamlit as st
import requests
import pandas as pd  # added for proper table 'display'

# Page setup
st.set_page_config(page_title="YouTube Analytics", layout="wide")

st.title("📊 YouTube Shorts Analytics Platform")
st.write("Paste a YouTube Shorts URL to extract data insights")

# Input box
url = st.text_input("Enter YouTube Shorts URL")

# Button click
if st.button("Extract Data"):

    if not url:
        st.error("Please enter a valid URL")
        st.stop()

    try:
        with st.spinner("Extracting video data..."):

            # FIX: store API endpoint separately (cleaner + reusable)
            API_URL = "http://127.0.0.1:8000/extract"

            response = requests.get(
                API_URL,
                params={"url": url},
                timeout=30
            )

            # FIX: check HTTP status BEFORE parsing JSON
            if response.status_code != 200:
                st.error(f"Backend error: {response.status_code}")
                st.stop()

            # FIX: safely parse JSON (prevents crash if backend fails)
            try:
                data = response.json()
            except:
                st.error("Invalid response from backend.")
                st.stop()

        # Handle API response
        if data.get("status") == "success":

            st.success("Video extracted successfully!")
            video = data["data"]

            # Display results
            st.subheader("Video Details")

            st.write("**Title:**", video.get("title"))
            st.write("**Views:**", video.get("views"))
            st.write("**Likes:**", video.get("likes"))
            st.write("**Description:**", video.get("description"))
            st.write("**Duration:**", video.get("length"))
            st.write("**Author:**", video.get("author"))
            st.write("**Publish Date:**", video.get("publish_date"))

            st.subheader("Transcript")

            if video.get("transcript"):
                st.write(video["transcript"])
            else:
                st.warning("No transcript available")

            # TABLE format
            st.subheader("📊 Data Table View")

            # FIX: better dataframe rendering (cleaner + safer)
            st.dataframe(pd.DataFrame([video]))

        else:
            st.error(data.get("message", "Something went wrong"))

    except requests.exceptions.RequestException:
        st.error("Backend not reachable. Is FastAPI running?")