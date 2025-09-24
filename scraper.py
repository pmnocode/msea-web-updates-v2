import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MapleSEAScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def get_updates(self) -> List[Dict[str, str]]:
        """Scrape the MapleSEA updates page and return a list of update posts."""
        try:
            response = self.session.get(self.base_url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            updates = []

            # Find all update items in the list
            update_items = soup.find_all('li')

            for item in update_items:
                # Look for items that contain links with the date pattern
                link = item.find('a')
                if link and link.get('href'):
                    text = item.get_text(strip=True)

                    # Match the date pattern [DD.MM]
                    date_match = re.match(r'\[(\d{2}\.\d{2})\]\s*:\s*(.+)', text)
                    if date_match:
                        date = date_match.group(1)
                        title = date_match.group(2).strip()
                        href = link.get('href')

                        # Construct full URL if it's a relative path
                        if href.startswith('/'):
                            full_url = f"https://www.maplesea.com{href}"
                        else:
                            full_url = href

                        updates.append({
                            'date': date,
                            'title': title,
                            'url': full_url,
                            'full_text': text
                        })

            logger.info(f"Found {len(updates)} updates on the page")
            return updates

        except requests.RequestException as e:
            logger.error(f"Error fetching updates: {e}")
            return []
        except Exception as e:
            logger.error(f"Error parsing updates: {e}")
            return []