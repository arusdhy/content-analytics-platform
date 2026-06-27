# Import the main function that handles YouTube data extraction
# This function pulls metadata (title, views, likes, etc.) and transcript
from app.collectors.youtube_extractor import extract_youtube_data

# YouTube video URL input
# This is the video we want to analyze and extract data from
url = "https://youtube.com/shorts/yxGbYtq1hFU?si=ijQbSeYFnjpIpQFW"

# Call the extractor function
# Step 1: Parses the video ID from the URL
# Step 2: Fetches metadata using YouTube API / pytube
# Step 3: Fetches transcript using transcript API (if available)
# Step 4: Combines everything into a structured dictionary
data = extract_youtube_data(url)

# Print the extracted structured data
print(data)