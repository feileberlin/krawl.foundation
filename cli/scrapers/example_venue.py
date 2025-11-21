"""
Example Venue Scraper - Template für eigene Scraper

Dieser Scraper dient als Vorlage. Kopiere diese Datei und passe sie an
die Struktur der Ziel-Website an.
"""

from typing import Any, Dict, List

from .base import BaseScraper


class ExampleVenueScraper(BaseScraper):
    """
    Scraper für Example Venue.

    Website-Struktur:
    - Events-Seite: https://example.com/events
    - Event-Container: <div class="event">
    - Titel: <h2 class="event-title">
    - Datum: <span class="event-date">
    - Etc.
    """

    def __init__(self):
        super().__init__(base_url="https://example.com", venue_name="Example Venue")
        self.events_page = f"{self.base_url}/events"

    def scrape(self) -> List[Dict[str, Any]]:
        """
        Scrape events from Example Venue website.

        Returns:
            List of normalized event dictionaries
        """
        # 1. Fetch events page
        html = self.fetch_page(self.events_page)
        if not html:
            return []

        # 2. Parse HTML
        soup = self.parse_html(html)

        # 3. Find all event containers
        event_containers = soup.find_all("div", class_="event")

        events = []
        for container in event_containers:
            try:
                # 4. Extract event data
                raw_event = self._extract_event_data(container)

                # 5. Normalize event
                normalized = self.normalize_event(raw_event)

                # 6. Validate event
                if self.validate_event(normalized):
                    events.append(normalized)
                else:
                    print(
                        f"⚠️  Skipped invalid event: {raw_event.get('title', 'Unknown')}"
                    )

            except Exception as e:
                print(f"Error parsing event: {e}")
                continue

        return events

    def _extract_event_data(self, container) -> Dict[str, Any]:
        """
        Extract raw event data from HTML container.

        Args:
            container: BeautifulSoup element containing event

        Returns:
            Dictionary with raw event data
        """
        # Find elements (adjust selectors to match actual website)
        title_elem = container.find("h2", class_="event-title")
        date_elem = container.find("span", class_="event-date")
        location_elem = container.find("span", class_="event-location")
        description_elem = container.find("p", class_="event-description")
        price_elem = container.find("span", class_="event-price")
        url_elem = container.find("a", class_="event-link")
        genre_elem = container.find("span", class_="event-genre")
        image_elem = container.find("img", class_="event-image")

        return {
            "title": title_elem.get_text() if title_elem else "",
            "date": date_elem.get_text() if date_elem else "",
            "location": location_elem.get_text() if location_elem else "",
            "description": description_elem.get_text() if description_elem else "",
            "price": price_elem.get_text() if price_elem else "",
            "url": url_elem.get("href") if url_elem else "",
            "genre": genre_elem.get_text() if genre_elem else "",
            "image_url": image_elem.get("src") if image_elem else "",
        }


# Usage Example:
if __name__ == "__main__":
    scraper = ExampleVenueScraper()
    events = scraper.scrape()

    print(f"Scraped {len(events)} events from {scraper.venue_name}")

    for event in events:
        print(f"  - {event['title']} ({event['date']})")
