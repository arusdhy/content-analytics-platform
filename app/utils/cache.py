# Simple in-memory cache for extracted videos
# MVP version (later upgrade to Redis)

VIDEO_CACHE = {}


def get_cached_video(video_id):
    return VIDEO_CACHE.get(video_id)


def set_cached_video(video_id, data):
    VIDEO_CACHE[video_id] = {
        "data": data,
        "timestamp": datetime.now()
    }


def is_cached(video_id):
    return video_id in VIDEO_CACHE