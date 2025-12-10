import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
MAPLESEA_URLS = [
    "https://www.maplesea.com/updates",
    "https://www.maplesea.com/notices",
    "https://www.maplesea.com/announcements",
    "https://www.maplesea.com/news",
    "https://www.maplesea.com/events"
]
DISCORD_WEBHOOK_URLS = [
    os.getenv("DISCORD_WEBHOOK_URL"),
    os.getenv("DISCORD_WEBHOOK_URL_2")
]
# Filter out None values in case second webhook is not configured
DISCORD_WEBHOOK_URLS = [url for url in DISCORD_WEBHOOK_URLS if url]
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "30"))
SEEN_POSTS_FILE = "seen_posts.json"