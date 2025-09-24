import json
import os
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class PostStorage:
    def __init__(self, storage_file: str):
        self.storage_file = storage_file
        self.seen_posts: Dict[str, str] = self._load_seen_posts()

    def _load_seen_posts(self) -> Dict[str, str]:
        """Load previously seen posts from storage file."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('seen_posts', {})
            except (json.JSONDecodeError, FileNotFoundError) as e:
                logger.warning(f"Error loading seen posts: {e}, starting fresh")
        return {}

    def _save_seen_posts(self):
        """Save seen posts to storage file."""
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'seen_posts': self.seen_posts
                }, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving seen posts: {e}")

    def get_new_posts(self, current_posts: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Filter posts and return new ones or ones with updated titles."""
        new_posts = []
        updated_posts = []

        for post in current_posts:
            # Use date + URL as unique identifier (more stable than title)
            post_key = f"{post['date']}_{post['url']}"
            current_title = post['title']

            if post_key not in self.seen_posts:
                # Completely new post
                new_posts.append(post)
                self.seen_posts[post_key] = current_title
                logger.debug(f"New post: [{post['date']}] {current_title}")
            elif self.seen_posts[post_key] != current_title:
                # Existing post with updated title
                old_title = self.seen_posts[post_key]
                updated_posts.append(post)
                self.seen_posts[post_key] = current_title
                logger.debug(f"Updated post: [{post['date']}] {old_title} -> {current_title}")

        all_new_or_updated = new_posts + updated_posts

        if all_new_or_updated:
            self._save_seen_posts()
            if new_posts:
                logger.info(f"Found {len(new_posts)} new posts")
            if updated_posts:
                logger.info(f"Found {len(updated_posts)} updated posts")
        else:
            logger.info("No new or updated posts found")

        return all_new_or_updated

    def mark_posts_as_seen(self, posts: List[Dict[str, str]]):
        """Manually mark posts as seen (useful for initialization)."""
        for post in posts:
            post_key = f"{post['date']}_{post['url']}"
            self.seen_posts[post_key] = post['title']

        self._save_seen_posts()
        logger.info(f"Marked {len(posts)} posts as seen")