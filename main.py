import schedule
import time
import logging
import sys
import os
from datetime import datetime
from scraper import MapleSEAScraper
from storage import PostStorage
from discord_notifier import DiscordNotifier
from config import MAPLESEA_UPDATES_URL, DISCORD_WEBHOOK_URL, CHECK_INTERVAL_MINUTES, SEEN_POSTS_FILE

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('watcher.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class UpdatesWatcher:
    def __init__(self):
        self.scraper = MapleSEAScraper(MAPLESEA_UPDATES_URL)
        self.storage = PostStorage(SEEN_POSTS_FILE)
        self.notifier = DiscordNotifier(DISCORD_WEBHOOK_URL)

    def check_for_updates(self):
        """Check for new updates and send notifications if found."""
        logger.info("Checking for updates...")

        try:
            # Get current updates from the website
            current_updates = self.scraper.get_updates()

            if not current_updates:
                logger.warning("No updates found or error occurred while scraping")
                return

            # Filter out already seen posts
            new_posts = self.storage.get_new_posts(current_updates)

            if new_posts:
                logger.info(f"Found {len(new_posts)} new post(s):")
                for post in new_posts:
                    logger.info(f"  - [{post['date']}] {post['title']}")

                # Send Discord notification
                self.notifier.send_notification(new_posts)
            else:
                logger.info("No new updates found")

        except Exception as e:
            logger.error(f"Error during update check: {e}")

    def initialize_storage(self):
        """Initialize storage with current posts to avoid spam on first run."""
        logger.info("Initializing storage with current posts...")
        current_updates = self.scraper.get_updates()
        if current_updates:
            self.storage.mark_posts_as_seen(current_updates)
            logger.info(f"Marked {len(current_updates)} existing posts as seen")

    def test_webhook(self):
        """Test the Discord webhook."""
        logger.info("Testing Discord webhook...")
        return self.notifier.test_webhook()

    def run_once(self):
        """Run a single check for updates."""
        self.check_for_updates()

    def run_scheduler(self):
        """Run the scheduled watcher."""
        if not DISCORD_WEBHOOK_URL:
            logger.error("Discord webhook URL not configured! Please set DISCORD_WEBHOOK_URL in your .env file or GitHub secret")
            return

        logger.info(f"Starting MapleSEA updates watcher (checking every {CHECK_INTERVAL_MINUTES} minutes)")

        # For GitHub Actions, we just run once per workflow execution
        if os.getenv('GITHUB_ACTIONS'):
            logger.info("Running in GitHub Actions mode - single check")
            self.check_for_updates()
            return

        # For local execution, use scheduler
        # Schedule the update check
        schedule.every(CHECK_INTERVAL_MINUTES).minutes.do(self.check_for_updates)

        # Run an initial check
        self.check_for_updates()

        # Keep the script running
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute if any scheduled job needs to run
        except KeyboardInterrupt:
            logger.info("Watcher stopped by user")

def main():
    watcher = UpdatesWatcher()

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "init":
            watcher.initialize_storage()
        elif command == "test":
            watcher.test_webhook()
        elif command == "check":
            watcher.run_once()
        elif command == "run":
            watcher.run_scheduler()
        else:
            print("Usage: python main.py [init|test|check|run]")
            print("  init  - Initialize storage with current posts")
            print("  test  - Test Discord webhook")
            print("  check - Run a single check for updates")
            print("  run   - Start the scheduled watcher")
    else:
        watcher.run_scheduler()

if __name__ == "__main__":
    main()