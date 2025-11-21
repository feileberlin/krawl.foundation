# Event Scrapers

Spezifische Scraper-Implementierungen für verschiedene Venues.

## 🏗️ Architektur

Alle Scraper erben von `BaseScraper` und implementieren die `scrape()` Methode.

```python
from cli.scrapers.base import BaseScraper

class MyVenueScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            base_url='https://myvenue.com',
            venue_name='My Venue'
        )
    
    def scrape(self):
        # Implementierung hier
        pass
```

## 📝 Neuen Scraper erstellen

### 1. Template kopieren

```bash
cp cli/scrapers/example_venue.py cli/scrapers/mein_venue.py
```

### 2. Basis-Informationen anpassen

```python
class MeinVenueScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            base_url='https://meinvenue.de',
            venue_name='Mein Venue'
        )
        self.events_page = f'{self.base_url}/veranstaltungen'
```

### 3. HTML-Selektoren identifizieren

Öffne die Events-Seite im Browser:

```bash
# Chrome DevTools
Rechtsklick → Untersuchen → Element auswählen

# Suche nach:
# - Container für Events (z.B. <div class="event">)
# - Titel-Element (z.B. <h2 class="title">)
# - Datum-Element (z.B. <time class="date">)
# - Etc.
```

### 4. `_extract_event_data()` anpassen

```python
def _extract_event_data(self, container) -> Dict[str, Any]:
    # Anpassen an tatsächliche HTML-Struktur
    title_elem = container.find('h2', class_='event-title')
    date_elem = container.find('time', {'datetime': True})
    
    return {
        'title': title_elem.get_text() if title_elem else '',
        'date': date_elem.get('datetime') if date_elem else '',
        # ...
    }
```

### 5. Testen

```bash
# Direkt ausführen
python cli/scrapers/mein_venue.py

# Oder über CLI (wenn integriert)
./cli/event_scraper.py scrape --venue mein_venue
```

## 🛠️ BaseScraper API

### Methoden

#### `fetch_page(url: str) -> Optional[str]`
Lädt HTML von URL.

```python
html = self.fetch_page('https://example.com/events')
```

#### `parse_html(html: str) -> BeautifulSoup`
Parst HTML zu BeautifulSoup-Objekt.

```python
soup = self.parse_html(html)
events = soup.find_all('div', class_='event')
```

#### `normalize_event(raw_event: Dict) -> Dict`
Normalisiert Event-Daten zu Standard-Format.

```python
raw = {'title': 'Concert', 'date': '15.12.2025'}
normalized = self.normalize_event(raw)
# {'title': 'Concert', 'date': '2025-12-15', ...}
```

#### `validate_event(event: Dict) -> bool`
Prüft ob Event alle Pflichtfelder hat.

```python
if self.validate_event(event):
    events.append(event)
```

## 📋 Standard Event-Format

```json
{
  "title": "Event Titel",
  "date": "2025-12-15",
  "venue": "Venue Name",
  "location": "Berlin",
  "description": "Event Beschreibung",
  "price": "15€",
  "url": "https://venue.com/event/123",
  "genre": "Rock",
  "image_url": "https://venue.com/images/event.jpg",
  "status": "draft",
  "scraped_at": "2025-11-21T10:00:00",
  "source": "https://venue.com"
}
```

### Pflichtfelder
- `title`
- `date`
- `venue`

### Optionale Felder
Alle anderen Felder sind optional, sollten aber gefüllt werden wenn verfügbar.

## 🎯 Best Practices

### 1. Fehlerbehandlung

```python
def scrape(self):
    try:
        html = self.fetch_page(self.events_page)
        if not html:
            return []
        
        # ... parsing ...
        
    except Exception as e:
        print(f"Error scraping {self.venue_name}: {e}")
        return []
```

### 2. Robuste Selektoren

```python
# Mehrere Fallbacks
title = (
    container.find('h2', class_='event-title') or
    container.find('h3', class_='title') or
    container.find('a', class_='event-link')
)
```

### 3. Daten-Cleaning

```python
title = title_elem.get_text().strip()
title = ' '.join(title.split())  # Normalize whitespace
```

### 4. Rate Limiting

```python
import time

for page in range(1, 10):
    html = self.fetch_page(f'{self.base_url}/events?page={page}')
    # ... parse ...
    time.sleep(1)  # 1 Sekunde Pause
```

### 5. User Agent

```python
self.session.headers.update({
    'User-Agent': 'krawl.foundation/1.0 (Contact: mail@example.com)'
})
```

## 🧪 Testing

### Unit Test für Scraper

```python
# tests/test_mein_venue_scraper.py
import pytest
from cli.scrapers.mein_venue import MeinVenueScraper

def test_scraper():
    scraper = MeinVenueScraper()
    events = scraper.scrape()
    
    assert len(events) > 0
    assert all(scraper.validate_event(e) for e in events)
```

### Mock HTML für Tests

```python
def test_extract_event_data():
    html = '''
    <div class="event">
        <h2 class="title">Test Event</h2>
        <time datetime="2025-12-15">15. Dez 2025</time>
    </div>
    '''
    
    scraper = MeinVenueScraper()
    soup = scraper.parse_html(html)
    container = soup.find('div', class_='event')
    
    event = scraper._extract_event_data(container)
    assert event['title'] == 'Test Event'
```

## 🔍 Debugging

```python
# Verbose logging
def scrape(self):
    print(f"Fetching: {self.events_page}")
    html = self.fetch_page(self.events_page)
    
    print(f"Found {len(containers)} event containers")
    
    for i, container in enumerate(containers):
        print(f"Processing event {i+1}...")
        # ...
```

## 🚀 Integration in CLI

```python
# In cli/event_scraper.py
from cli.scrapers.mein_venue import MeinVenueScraper

def cmd_scrape(self, args):
    if args.venue == 'mein_venue':
        scraper = MeinVenueScraper()
        events = scraper.scrape()
        # ...
```

## 📚 Weitere Ressourcen

- [BeautifulSoup Docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Docs](https://requests.readthedocs.io/)
- [CSS Selectors Reference](https://www.w3schools.com/cssref/css_selectors.php)
- [Web Scraping Ethics](https://towardsdatascience.com/ethics-in-web-scraping-b96b18136f01)
