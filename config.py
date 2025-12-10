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
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "30"))
SEEN_POSTS_FILE = "seen_posts.json"