import requests
import json
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class DiscordNotifier:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send_notification(self, posts: List[Dict[str, str]], updated_posts: List[Dict[str, str]] = None):
        """Send Discord notification for new or updated posts."""
        if not self.webhook_url:
            logger.warning("Discord webhook URL not configured")
            return

        if not posts:
            return

        try:
            # Create embed for each post
            embeds = []
            for post in posts:
                # Determine if this is an updated post by checking for update keywords
                title = post['title']
                is_updated = any(keyword.upper() in title.upper()
                               for keyword in ['UPDATED', 'COMPLETED', 'EXTENDED', 'REVISED', 'AMENDED'])

                embed = {
                    "title": f"[{post['date']}] {title}",
                    "url": post['url'],
                    "color": 0xFFA500 if is_updated else 0x00ff00,  # Orange for updates, Green for new
                    "footer": {
                        "text": "MapleSEA Updates Watcher"
                    }
                }

                if is_updated:
                    embed["description"] = "📝 *This post has been updated*"

                embeds.append(embed)

            # Discord has a limit of 10 embeds per message
            for i in range(0, len(embeds), 10):
                embed_batch = embeds[i:i+10]

                # Count new vs updated posts in this batch
                new_count = sum(1 for embed in embed_batch if embed['color'] == 0x00ff00)
                updated_count = len(embed_batch) - new_count

                # Create appropriate message content
                content_parts = ["@everyone"]
                if new_count > 0:
                    content_parts.append(f"🍁 **{new_count} New MapleSEA Update{'s' if new_count > 1 else ''}!**")
                if updated_count > 0:
                    content_parts.append(f"📝 **{updated_count} Updated Post{'s' if updated_count > 1 else ''}!**")

                payload = {
                    "content": " ".join(content_parts),
                    "embeds": embed_batch,
                    "allowed_mentions": {
                        "parse": ["everyone"]
                    }
                }

                response = requests.post(
                    self.webhook_url,
                    json=payload,
                    headers={'Content-Type': 'application/json'},
                    timeout=30
                )

                if response.status_code == 204:
                    logger.info(f"Successfully sent Discord notification for {len(embed_batch)} post(s)")
                else:
                    logger.error(f"Failed to send Discord notification: {response.status_code} - {response.text}")

        except requests.RequestException as e:
            logger.error(f"Error sending Discord notification: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in Discord notification: {e}")

    def test_webhook(self):
        """Test if the Discord webhook is working."""
        if not self.webhook_url:
            logger.error("Discord webhook URL not configured")
            return False

        try:
            test_payload = {
                "content": "🧪 **MapleSEA Updates Watcher Test** 🧪",
                "embeds": [{
                    "title": "Test Notification",
                    "description": "This is a test notification from your MapleSEA updates watcher.",
                    "color": 0x0099ff,
                    "footer": {
                        "text": "If you see this, the webhook is working correctly!"
                    }
                }]
            }

            response = requests.post(
                self.webhook_url,
                json=test_payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )

            if response.status_code == 204:
                logger.info("Discord webhook test successful!")
                return True
            else:
                logger.error(f"Discord webhook test failed: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            logger.error(f"Error testing Discord webhook: {e}")
            return False