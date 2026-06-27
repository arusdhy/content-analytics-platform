from urllib.parse import urlparse, parse_qs

def get_video_id(url):
    query = urlparse(url).query
    return parse_qs(query).get("v", [None])[0]