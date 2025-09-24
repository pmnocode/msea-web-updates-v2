import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
MAPLESEA_UPDATES_URL = "https://www.maplesea.com/updates"
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "30"))
SEEN_POSTS_FILE = "seen_posts.json"