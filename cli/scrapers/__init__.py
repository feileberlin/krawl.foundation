"""
Event Scraper Implementations

Dieser Ordner enthält spezifische Scraper-Implementierungen für verschiedene Venues.
Jeder Scraper sollte von BaseScraper erben und die scrape() Methode implementieren.
"""

from .base import BaseScraper

__all__ = ["BaseScraper"]
