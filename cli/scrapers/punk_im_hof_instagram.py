"""
Instagram Scraper für Punk im Hof (@punkinhof)

WICHTIG: Instagram-Scraping Einschränkungen:
- Erfordert Login für viele Inhalte
- Instagram Basic Display API (eingeschränkt)
- Instagram Graph API (nur für Business-Accounts)
- Rate Limits sehr strikt
- Robots.txt beachten

Empfohlene Alternativen:
1. Instagram Graph API (falls Business-Account)
2. RSS-Bridge oder Bibliogram (Drittanbieter-Proxies)
3. Instaloader (Python-Library, aber Login nötig)
4. Manuelle Erfassung
"""

import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add parent directory to path for standalone execution
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from scrapers.base import BaseScraper
else:
    from .base import BaseScraper

import time


class PunkImHofInstagramScraper(BaseScraper):
    """
    Scraper für Instagram @punkinhof.

    Bietet mehrere Ansätze:
    1. Instaloader (empfohlen für Instagram)
    2. Instagram Graph API (Business-Accounts)
    3. Manuelle Erfassung
    """

    def __init__(self):
        super().__init__(
            base_url="https://www.instagram.com/punkinhof", venue_name="Punk im Hof"
        )
        self.use_instaloader = False

        # Prüfe ob instaloader verfügbar
        try:
            import instaloader

            self.use_instaloader = True
            print("✓ Instaloader verfügbar")
        except ImportError:
            print("⚠️  Instaloader nicht installiert")
            print("   Installation: pip install instaloader")

    def scrape(self) -> List[Dict[str, Any]]:
        """
        Scrape events from Instagram profile.

        Returns:
            List of normalized event dictionaries
        """
        if self.use_instaloader:
            try:
                return self._scrape_with_instaloader()
            except Exception as e:
                print(f"Instaloader-Fehler: {e}")
                return self._scrape_fallback()
        else:
            return self._scrape_fallback()

    def _scrape_with_instaloader(self) -> List[Dict[str, Any]]:
        """
        Scrape using Instaloader library.

        HINWEIS: Kann Login erfordern für vollständigen Zugriff.
        """
        import instaloader

        L = instaloader.Instaloader()

        # Optional: Login (auskommentiert, da nicht immer nötig)
        # L.login(username, password)

        events = []

        try:
            profile = instaloader.Profile.from_username(L.context, "punkinhof")

            print(f"📸 Lade Posts von @punkinhof...")
            print(f"   Follower: {profile.followers}")
            print(f"   Posts: {profile.mediacount}")

            # Durchsuche die letzten Posts nach Event-Keywords
            post_count = 0
            for post in profile.get_posts():
                if post_count >= 20:  # Nur letzte 20 Posts
                    break

                post_count += 1

                # Extrahiere Event-Info aus Caption
                caption = post.caption or ""

                # Suche nach Event-Keywords
                if self._is_event_post(caption):
                    raw_event = self._extract_event_from_caption(caption, post)
                    if raw_event:
                        normalized = self.normalize_event(raw_event)
                        if self.validate_event(normalized):
                            events.append(normalized)
                            print(f"   ✓ Event gefunden: {normalized['title'][:50]}...")

                time.sleep(1)  # Rate limiting

            print(f"\n✓ {len(events)} Events extrahiert aus {post_count} Posts")

        except Exception as e:
            print(f"Fehler beim Laden von Instagram-Profil: {e}")
            print("Tipp: Login könnte erforderlich sein für vollständigen Zugriff")

        return events

    def _is_event_post(self, caption: str) -> bool:
        """Check if post is about an event."""
        event_keywords = [
            "konzert",
            "concert",
            "live",
            "show",
            "gig",
            "veranstaltung",
            "event",
            "auftritt",
            "datum",
            "einlass",
            "uhr",
            "uhr",
            "📅",
            "🎵",
            "🎸",
            "🎤",
            "🎶",
        ]

        caption_lower = caption.lower()
        return any(keyword in caption_lower for keyword in event_keywords)

    def _extract_event_from_caption(
        self, caption: str, post
    ) -> Optional[Dict[str, Any]]:
        """
        Extract event data from Instagram caption.

        Versucht Titel, Datum, etc. aus dem Text zu parsen.
        """
        lines = caption.split("\n")

        # Erste Zeile oft der Titel
        title = lines[0] if lines else "Event @ Punk im Hof"
        title = title.replace("#", "").strip()

        # Versuche Datum zu finden (sehr simpel)
        date = None
        date_patterns = [
            r"\d{1,2}\.\d{1,2}\.\d{2,4}",  # DD.MM.YYYY
            r"\d{1,2}/\d{1,2}/\d{2,4}",  # DD/MM/YYYY
        ]

        for line in lines:
            for pattern in date_patterns:
                match = re.search(pattern, line)
                if match:
                    date = match.group(0)
                    break
            if date:
                break

        # Post-URL
        url = f"https://www.instagram.com/p/{post.shortcode}/"

        return {
            "title": title,
            "date": date
            or post.date_local.strftime("%Y-%m-%d"),  # Fallback: Post-Datum
            "description": caption[:200],  # Erste 200 Zeichen
            "url": url,
            "location": "Berlin",
            "image_url": post.url,
        }

    def scrape_with_graph_api(
        self, access_token: str, instagram_business_id: str
    ) -> List[Dict[str, Any]]:
        """
        Alternative: Scrape via Instagram Graph API.

        Voraussetzungen:
        - Business oder Creator Account
        - Facebook Page verbunden
        - Access Token mit instagram_basic Permission

        Args:
            access_token: Instagram/Facebook API Access Token
            instagram_business_id: Instagram Business Account ID

        Returns:
            List of events
        """
        import requests

        api_url = f"https://graph.facebook.com/v18.0/{instagram_business_id}/media"

        params = {
            "access_token": access_token,
            "fields": "id,caption,media_type,media_url,permalink,timestamp",
        }

        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()
            data = response.json()

            events = []
            for media in data.get("data", []):
                caption = media.get("caption", "")

                if self._is_event_post(caption):
                    raw_event = {
                        "title": caption.split("\n")[0][:100],
                        "date": media.get("timestamp", "")[:10],
                        "description": caption[:200],
                        "url": media.get("permalink", ""),
                        "location": "Berlin",
                        "image_url": media.get("media_url", ""),
                    }

                    normalized = self.normalize_event(raw_event)
                    if self.validate_event(normalized):
                        events.append(normalized)

            return events

        except Exception as e:
            print(f"Graph API Fehler: {e}")
            return []

    def _scrape_fallback(self) -> List[Dict[str, Any]]:
        """
        Fallback: Zeige Anleitung für manuelle Erfassung.
        """
        print("\n" + "=" * 60)
        print("📸 Instagram Events Scraping - Alternativen")
        print("=" * 60)
        print("\n🔧 Option 1: Instaloader installieren (empfohlen)")
        print("   pip install instaloader")
        print("   Scrapet Posts und extrahiert Event-Infos aus Captions")
        print()
        print("🔑 Option 2: Instagram Graph API")
        print("   Voraussetzungen:")
        print("   - Business oder Creator Account")
        print("   - Mit Facebook Page verbunden")
        print("   - Access Token mit instagram_basic Permission")
        print("   Anleitung: https://developers.facebook.com/docs/instagram-api")
        print()
        print("🌐 Option 3: RSS-Bridge")
        print("   https://github.com/RSS-Bridge/rss-bridge")
        print("   Proxy für Instagram-Feeds ohne API")
        print()
        print("✍️  Option 4: Manuelle Erfassung (pragmatisch)")
        print("   1. Öffne: https://www.instagram.com/punkinhof/")
        print("   2. Kopiere Event-Posts manuell")
        print("   3. Nutze: ./cli/event_scraper.py generate --count 1")
        print("   4. Editiere: _events/test-*.json mit echten Daten")
        print()
        print("💡 Tipp: Frag Venue ob sie Events auf eigener Website haben!")
        print("=" * 60 + "\n")

        return []


# Standalone Usage
if __name__ == "__main__":
    scraper = PunkImHofInstagramScraper()

    print("Instagram Scraper für Punk im Hof (@punkinhof)")
    print("-" * 60)

    # Versuche zu scrapen
    events = scraper.scrape()

    if events:
        print(f"\n✓ {len(events)} Events gefunden:\n")
        for event in events:
            print(f"  📅 {event['date']}: {event['title']}")
            print(f"     {event['url']}")
    else:
        print("\n⚠️  Keine Events gefunden")
        print("Siehe Ausgabe oben für Alternativen.")
