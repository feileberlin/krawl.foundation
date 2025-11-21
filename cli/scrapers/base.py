"""
Base Scraper Class - Template für alle Scraper-Implementierungen
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import requests
from bs4 import BeautifulSoup
from datetime import datetime


class BaseScraper(ABC):
    """
    Basis-Klasse für Event-Scraper.
    
    Jeder spezifische Scraper sollte von dieser Klasse erben und
    die scrape() Methode implementieren.
    """
    
    def __init__(self, base_url: str, venue_name: str):
        """
        Initialize scraper.
        
        Args:
            base_url: Base URL of the venue website
            venue_name: Name of the venue
        """
        self.base_url = base_url
        self.venue_name = venue_name
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'krawl.foundation/1.0 (Event Scraper Bot)'
        })
    
    def fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch HTML content from URL.
        
        Args:
            url: URL to fetch
            
        Returns:
            HTML content or None if error
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def parse_html(self, html: str) -> BeautifulSoup:
        """
        Parse HTML content with BeautifulSoup.
        
        Args:
            html: HTML content string
            
        Returns:
            BeautifulSoup object
        """
        return BeautifulSoup(html, 'lxml')
    
    @abstractmethod
    def scrape(self) -> List[Dict[str, Any]]:
        """
        Scrape events from venue.
        
        This method must be implemented by each specific scraper.
        
        Returns:
            List of event dictionaries with standardized fields
        """
        pass
    
    def normalize_event(self, raw_event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize event data to standard format.
        
        Args:
            raw_event: Raw event data from scraping
            
        Returns:
            Normalized event dictionary
        """
        return {
            'title': raw_event.get('title', '').strip(),
            'date': self._parse_date(raw_event.get('date')),
            'venue': self.venue_name,
            'location': raw_event.get('location', '').strip(),
            'description': raw_event.get('description', '').strip(),
            'price': raw_event.get('price', '').strip(),
            'url': raw_event.get('url', '').strip(),
            'genre': raw_event.get('genre', '').strip(),
            'image_url': raw_event.get('image_url', '').strip(),
            'status': 'draft',
            'scraped_at': datetime.now().isoformat(),
            'source': self.base_url
        }
    
    def _parse_date(self, date_str: Optional[str]) -> Optional[str]:
        """
        Parse date string to ISO format.
        
        Args:
            date_str: Date string in various formats
            
        Returns:
            ISO format date string or None
        """
        if not date_str:
            return None
        
        # Common date formats
        formats = [
            '%Y-%m-%d',
            '%d.%m.%Y',
            '%d/%m/%Y',
            '%Y-%m-%d %H:%M:%S',
            '%d.%m.%Y %H:%M',
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str.strip(), fmt)
                return dt.date().isoformat()
            except ValueError:
                continue
        
        return None
    
    def validate_event(self, event: Dict[str, Any]) -> bool:
        """
        Validate that event has required fields.
        
        Args:
            event: Event dictionary
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ['title', 'date', 'venue']
        
        for field in required_fields:
            if not event.get(field):
                return False
        
        return True
