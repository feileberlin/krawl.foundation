"""
Facebook Events Scraper für GaleriehausHof

WICHTIG: Facebook-Scraping ist komplex und unterliegt Einschränkungen:
- Erfordert Browser-Automation (Selenium) wegen JavaScript
- Rate Limits beachten
- Evtl. Login erforderlich für alle Events
- Robots.txt beachten
- Facebook Graph API als Alternative erwägen

Alternative Ansätze:
1. Facebook Graph API (empfohlen, aber API-Key nötig)
2. Selenium mit geckodriver/chromedriver
3. RSS-Feed falls verfügbar
4. Manuelle Dateneingabe mit generate-Command
"""

from typing import List, Dict, Any, Optional
import sys
from pathlib import Path

# Add parent directory to path for standalone execution
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from scrapers.base import BaseScraper
else:
    from .base import BaseScraper

import time


class GaleriehausHofFacebookScraper(BaseScraper):
    """
    Scraper für Facebook Events von GaleriehausHof.

    Nutzt Selenium für JavaScript-Rendering.
    Falls Selenium nicht verfügbar, gibt Anleitung für manuelle Erfassung.
    """

    def __init__(self):
        super().__init__(
            base_url="https://www.facebook.com/GaleriehausHof",
            venue_name="Galeriehaus Hof",
        )
        self.events_page = f"{self.base_url}/events"
        self.use_selenium = False

        # Prüfe ob Selenium verfügbar
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            self.use_selenium = True
            print("✓ Selenium verfügbar - verwende Browser-Automation")
        except ImportError:
            print("⚠️  Selenium nicht installiert")
            print("   Installation: pip install selenium")
            print("   Plus: geckodriver (Firefox) oder chromedriver (Chrome)")

    def scrape(self) -> List[Dict[str, Any]]:
        """
        Scrape events from Facebook page.

        Returns:
            List of normalized event dictionaries
        """
        if not self.use_selenium:
            return self._scrape_fallback()

        try:
            return self._scrape_with_selenium()
        except Exception as e:
            print(f"Fehler beim Selenium-Scraping: {e}")
            return self._scrape_fallback()

    def _scrape_with_selenium(self) -> List[Dict[str, Any]]:
        """Scrape using Selenium for JavaScript rendering."""
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.firefox.options import Options
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        # Headless Firefox
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = None
        events = []

        try:
            print(f"🌐 Öffne {self.events_page} mit Selenium...")
            driver = webdriver.Firefox(options=options)
            driver.get(self.events_page)

            # Warte auf Event-Container (Selektor muss angepasst werden)
            wait = WebDriverWait(driver, 10)

            # Facebook-Struktur ändert sich oft - diese Selektoren sind Beispiele
            # und müssen wahrscheinlich angepasst werden
            time.sleep(5)  # Initiales Laden

            # Versuche Event-Container zu finden
            event_containers = driver.find_elements(
                By.CSS_SELECTOR, '[role="article"]'
            )  # Oder anderer Selektor

            print(f"   Gefunden: {len(event_containers)} Event-Container")

            for container in event_containers:
                try:
                    raw_event = self._extract_from_selenium_element(container)
                    if raw_event:
                        normalized = self.normalize_event(raw_event)
                        if self.validate_event(normalized):
                            events.append(normalized)
                except Exception as e:
                    print(f"   ⚠️  Fehler bei Event-Extraktion: {e}")
                    continue

        finally:
            if driver:
                driver.quit()

        return events

    def _extract_from_selenium_element(self, element) -> Optional[Dict[str, Any]]:
        """Extract event data from Selenium WebElement."""
        try:
            # Diese Selektoren sind Platzhalter und müssen angepasst werden
            # basierend auf der aktuellen Facebook-Struktur

            title = element.find_element(By.CSS_SELECTOR, 'span[dir="auto"]').text

            # Datum - sehr variabel bei Facebook
            date_text = ""
            try:
                date_elem = element.find_element(By.TAG_NAME, "time")
                date_text = date_elem.get_attribute("datetime")
            except:
                pass

            # Link zum Event
            url = ""
            try:
                link = element.find_element(By.TAG_NAME, "a")
                url = link.get_attribute("href")
            except:
                pass

            return {
                "title": title,
                "date": date_text,
                "url": url,
                "location": "Berlin",  # Muss ggf. aus Beschreibung extrahiert werden
                "description": "",
            }
        except Exception as e:
            return None

    def _scrape_fallback(self) -> List[Dict[str, Any]]:
        """
        Fallback: Zeige Anleitung für manuelle Erfassung oder API-Nutzung.
        """
        print("\n" + "=" * 60)
        print("📘 Facebook Events Scraping - Alternativen")
        print("=" * 60)
        print("\n🔧 Option 1: Selenium installieren")
        print("   pip install selenium")
        print("   Und Firefox geckodriver herunterladen:")
        print("   https://github.com/mozilla/geckodriver/releases")
        print()
        print("🔑 Option 2: Facebook Graph API (empfohlen)")
        print("   1. Facebook App erstellen: https://developers.facebook.com/")
        print("   2. Access Token erhalten")
        print("   3. API nutzen für zuverlässigere Daten")
        print()
        print("✍️  Option 3: Manuelle Erfassung")
        print("   Nutze den generate-Command mit realen Daten:")
        print("   ./cli/event_scraper.py generate --count 1")
        print("   Dann manuell editieren: _events/test-*.json")
        print()
        print("📋 Option 4: CSV/JSON Import")
        print("   Exportiere Events aus Facebook manuell als CSV")
        print("   Konvertiere mit separatem Script")
        print("=" * 60 + "\n")

        return []

    def scrape_with_graph_api(self, access_token: str) -> List[Dict[str, Any]]:
        """
        Alternative: Scrape via Facebook Graph API (stabiler & zuverlässiger).

        Args:
            access_token: Facebook API Access Token

        Returns:
            List of events
        """
        import requests

        # Graph API Endpoint für Events
        # Benötigt Page ID statt Page Name
        page_id = "GaleriehausHof"  # Kann auch numerisch sein

        api_url = f"https://graph.facebook.com/v18.0/{page_id}/events"

        params = {
            "access_token": access_token,
            "fields": "id,name,description,start_time,end_time,place,ticket_uri",
            "time_filter": "upcoming",
        }

        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()
            data = response.json()

            events = []
            for fb_event in data.get("data", []):
                raw_event = {
                    "title": fb_event.get("name", ""),
                    "date": fb_event.get("start_time", ""),
                    "description": fb_event.get("description", ""),
                    "url": f"https://facebook.com/events/{fb_event.get('id')}",
                    "location": fb_event.get("place", {}).get("name", "Berlin"),
                }

                normalized = self.normalize_event(raw_event)
                if self.validate_event(normalized):
                    events.append(normalized)

            return events

        except Exception as e:
            print(f"Graph API Fehler: {e}")
            return []


# Standalone Usage
if __name__ == "__main__":
    scraper = GaleriehausHofFacebookScraper()

    print("Facebook Events Scraper für Galeriehaus Hof")
    print("-" * 60)

    # Versuche zu scrapen
    events = scraper.scrape()

    if events:
        print(f"\n✓ {len(events)} Events gefunden:\n")
        for event in events:
            print(f"  📅 {event['date']}: {event['title']}")
    else:
        print("\n⚠️  Keine Events gefunden oder Selenium nicht verfügbar")
        print("Siehe Ausgabe oben für Alternativen.")
