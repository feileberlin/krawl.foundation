# 🛠️ KRaWL> Foundation – Entwickler-Dokumentation

Willkommen in der technischen Ecke! 🎉 Hier findest du alles, was du als Entwickler wissen musst, um mit KRaWL> Foundation zu arbeiten, es zu erweitern und zu verbessern.

## 🚀 Quick Start

### Voraussetzungen

- **Ruby** ≥ 3.0 (für Jekyll)
- **Python** ≥ 3.9 (für CLI-Tools)
- **Git** (für Versionskontrolle)

### Installation

```bash
# Repository klonen
git clone https://github.com/feileberlin/krawl.foundation.git
cd krawl.foundation

# Setup-Script ausführen (installiert alles Nötige)
./scripts/setup.sh

# Virtual Environment aktivieren
source venv/bin/activate

# Entwicklungsserver starten
./scripts/dev.sh
```

Fertig! 🎊 Die Website läuft jetzt unter http://localhost:4000

## 📋 Implementierte Features

### ✅ CLI Commands (event_scraper.py)

| Command | Status | Beschreibung |
|---------|--------|--------------|
| `list` | ✅ Funktioniert | Listet alle Events auf (Tabelle oder JSON) |
| `diff` | ✅ Funktioniert | Vergleicht zwei Events und zeigt Unterschiede |
| `merge` | ✅ Funktioniert | Führt Events zusammen (alle oder selektive Felder) |
| `generate` | ✅ Funktioniert | Generiert Lorem-Ipsum Test-Events mit Faker |
| `bulk` | ✅ Funktioniert | Massenoperationen mit Dry-Run Modus |
| `extract` | ✅ Funktioniert | Extrahiert Events aus Social Media Bildern |
| ~~`scrape`~~ | ~~⚠️ Placeholder~~ | ~~Event-Scraping von URLs (noch nicht implementiert)~~ |

### ✅ Scraper Framework

- **Base Scraper** (`cli/scrapers/base.py`): Abstract Base Class mit HTTP, HTML-Parsing, Normalisierung
- **Example Venue** (`cli/scrapers/example_venue.py`): Template für eigene Scraper
- ~~**GaleriehausHof Facebook**~~ (`cli/scrapers/galeriehaus_hof_facebook.py`): ~~⚠️ Teilweise funktionsfähig, benötigt Facebook API~~
- ~~**Punk im Hof Instagram**~~ (`cli/scrapers/punk_im_hof_instagram.py`): ~~⚠️ Teilweise funktionsfähig, benötigt Instagram API~~

### ✅ Image Extraction (image_extractor.py)

| Feature | Status | Beschreibung |
|---------|--------|--------------|
| Instagram Images | ✅ Funktioniert | Lädt Top N Bilder von Instagram (via Instaloader) |
| Local Files | ✅ Funktioniert | Batch-OCR für lokale Bilder |
| Batch OCR | ✅ Funktioniert | Automatische Texterkennung ohne User-Interaktion |
| Smart Parsing | ✅ Funktioniert | Extrahiert automatisch Datum, Uhrzeit, Venue |
| ~~Facebook Images~~ | ~~⚠️ API benötigt~~ | ~~Benötigt Facebook Graph API Token~~ |
| ~~OCR Integration~~ | ~~⚠️ Optional~~ | ~~Tesseract muss manuell installiert werden~~ |
| ~~Terminal Image Display~~ | ~~⚠️ Optional~~ | ~~imgcat/chafa nicht standardmäßig verfügbar~~ |

### ✅ Testing & CI/CD

- **Unit Tests** (`tests/test_event_scraper.py`): pytest-basierte Tests für alle Core-Funktionen
- **GitHub Actions**:
  - `test.yml`: Automatische Tests auf Python 3.9-3.12
  - `scrape-events.yml`: Auto-Scraping (Cron + Manual Trigger)
  - `deploy.yml`: Jekyll Build & GitHub Pages Deploy

## 🏗️ Projekt-Architektur

```
krawl.foundation/
├── cli/                          # CLI-Tools
│   ├── event_scraper.py          # Haupt-CLI (EventManager)
│   ├── image_extractor.py        # Batch OCR für Social Media
│   ├── voice_transcriber.py      # Spracherkennung (VOSK)
│   └── scrapers/
│       ├── base.py               # Abstract Base Class
│       ├── example_venue.py      # Template
│       ├── galeriehaus_hof_facebook.py
│       └── punk_im_hof_instagram.py
├── tests/                        # Unit Tests
│   └── test_event_scraper.py
├── _events/                      # Event-Dateien (JSON/Markdown)
├── _data/                        # Zusätzliche Daten
├── scripts/                      # Setup & Dev Scripts
│   ├── setup.sh
│   ├── telegram_bot.py          # Telegram Bot für Flyer-Upload
│   └── export_chat.py
├── assets/                       # CSS, JS, Bilder
│   ├── css/map.scss             # Map-Styling
│   └── js/map.js                # Map-Interaktionen
├── .github/workflows/            # GitHub Actions
├── _config.yml                   # Jekyll-Konfiguration
├── index.html                    # Startseite
├── map.html                      # Karte
├── dashboard.html                # Dashboard
└── requirements.txt              # Python-Dependencies
```

## 🧪 Testing

### Tests ausführen

```bash
# Alle Tests
pytest tests/ -v

# Mit Coverage
pytest tests/ --cov=cli --cov-report=term

# Einzelner Test
pytest tests/test_event_scraper.py::TestEventManager::test_compare_events -v
```

### Neue Tests hinzufügen

Tests sollten in `tests/test_event_scraper.py` hinzugefügt werden:

```python
def test_new_feature(sample_event):
    """Test für neues Feature"""
    manager = EventManager()
    result = manager.new_feature(sample_event)
    assert result is not None
```

## 🔧 Eigene Scraper entwickeln

### 1. Template kopieren

```bash
cp cli/scrapers/example_venue.py cli/scrapers/mein_venue.py
```

### 2. Anpassen

```python
from cli.scrapers.base import BaseScraper

class MeinVenueScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://meinvenue.de"
    
    def scrape_events(self, url):
        """Scrape Events von Mein Venue"""
        html = self.fetch_page(url)
        soup = self.parse_html(html)
        
        events = []
        for event_elem in soup.select('.event-card'):
            event = {
                'title': event_elem.select_one('.title').text.strip(),
                'date': self._parse_date(event_elem.select_one('.date').text),
                'venue': 'Mein Venue',
                # ... weitere Felder
            }
            events.append(self.normalize_event(event))
        
        return events
```

### 3. Testen

```bash
./cli/event_scraper.py scrape https://meinvenue.de/events
```

Siehe auch: `cli/scrapers/README.md` für ausführliche Dokumentation

## 🤖 GitHub Actions

### Workflows

| Workflow | Trigger | Zweck |
|----------|---------|-------|
| `deploy.yml` | Push to main | Jekyll Build & GitHub Pages Deploy |
| `scrape-events.yml` | Schedule (3am, 3pm UTC) | Auto-Scraping von Instagram/Facebook |
| `telegram-flyer.yml` | Repository Dispatch | Telegram Flyer Processing |
| `notify-pending-drafts.yml` | Schedule (alle 6h) | Erstellt Issues für alte Drafts |

### Manueller Trigger

```bash
# Deployment triggern
gh workflow run deploy.yml

# Scraping mit 5 Test-Events
gh workflow run scrape-events.yml -f event_count=5

# Draft-Benachrichtigung
gh workflow run notify-pending-drafts.yml
```

### Logs anzeigen

```bash
# Letzte Runs
gh run list --workflow=scrape-events.yml

# Logs für Run anzeigen
gh run view <run-id> --log
```

## 🔐 Secrets Management

Secrets werden in `.env` (lokal) und GitHub Secrets (CI/CD) verwaltet:

```bash
# Interaktives Setup
./scripts/setup_secrets.sh

# Oder manuell .env erstellen
cp .env.example .env
nano .env
```

**Benötigte Secrets:**
- `TELEGRAM_TOKEN`: Telegram Bot API (via @BotFather)
- `GITHUB_TOKEN`: GitHub Personal Access Token (Scopes: repo, workflow)

**Optional:**
- `EMAIL_PASSWORD`: Für Email-Benachrichtigungen
- `ONEDRIVE_CLIENT_ID`, `ONEDRIVE_CLIENT_SECRET`: Für Backups

Details: `docs/SECRETS.md`

## 📦 Dependencies

### Core

```
requests          # HTTP Client
beautifulsoup4    # HTML Parsing
lxml              # XML/HTML Parser
pyyaml            # YAML Support
python-dateutil   # Date Parsing
```

### Testing

```
pytest            # Test Framework
pytest-cov        # Coverage Reports
faker             # Test Data Generation
black             # Code Formatting
```

### Optional

```
selenium          # Browser Automation (für Facebook)
instaloader       # Instagram Scraping
pytesseract       # OCR (benötigt tesseract-ocr)
pillow            # Image Processing
vosk              # Speech Recognition
```

## 🎯 Best Practices

### 1. Code-Style

- **Black** für Formatierung: `black cli/ tests/`
- **Type Hints** verwenden: `def func(param: str) -> dict:`
- **Docstrings** für alle Funktionen
- **Klare Variablennamen**: `event_data` statt `d`

### 2. Error Handling

```python
try:
    event = manager.load_event(path)
except FileNotFoundError:
    logger.error(f"Event nicht gefunden: {path}")
    return None
except json.JSONDecodeError:
    logger.error(f"Ungültiges JSON: {path}")
    return None
```

### 3. Logging

```python
import logging

logger = logging.getLogger(__name__)
logger.info("Event erfolgreich gespeichert")
logger.warning("Pflichtfeld 'date' fehlt")
logger.error("Fehler beim Laden der Datei")
```

### 4. Git Workflow

```bash
# Feature Branch erstellen
git checkout -b feature/neue-funktion

# Commits mit aussagekräftigen Messages
git commit -m "Add: Neue Scraper-Funktion für Venue X"

# Tests laufen lassen
pytest tests/

# Pull Request erstellen
gh pr create --title "Add Venue X Scraper"
```

## 🚀 Deployment

### Lokales Testing

```bash
# Jekyll Build
bundle exec jekyll build

# Server starten
bundle exec jekyll serve --livereload
```

### GitHub Pages

Automatischer Deploy bei Push auf `main`:
1. GitHub Actions baut Jekyll
2. Deploy nach GitHub Pages
3. Website live unter https://feileberlin.github.io/krawl.foundation/

Custom Domain einrichten: `docs/01-GETTING_STARTED.md`

## 🐛 Debugging

### Häufige Probleme

**Jekyll baut nicht:**
```bash
bundle install
bundle exec jekyll build --verbose
```

**Python-Tests schlagen fehl:**
```bash
source venv/bin/activate
pip install -r requirements.txt
pytest tests/ -v
```

**Port 4000 belegt:**
```bash
bundle exec jekyll serve --port 4001
```

**GitHub Actions schlagen fehl:**
```bash
# Logs prüfen
gh run view --log

# Workflow neu starten
gh run rerun <run-id>
```

### Logging aktivieren

```bash
# Jekyll Verbose
bundle exec jekyll serve --verbose

# Python Debug
./cli/event_scraper.py list --verbose

# GitHub Actions Logs
gh run view <run-id> --log-failed
```

## 🔮 Roadmap & TODOs

### Geplante Features

- [ ] **Smart Deduplication**: Automatische Duplikat-Erkennung
- [ ] **Filter für Bulk-Ops**: `--filter "status==draft"`
- [ ] **JSON Schema Validation**: Event-Struktur validieren
- [ ] **CSV Export**: Events als CSV exportieren
- [ ] **iCal Export**: Events als .ics für Kalender
- [ ] **Web UI**: Optional Flask/FastAPI Interface
- [ ] **Event History**: Git-basierte Change-Tracking

### Offene Issues

Siehe: https://github.com/feileberlin/krawl.foundation/issues

## 📚 Weitere Ressourcen

- **Jekyll Dokumentation**: https://jekyllrb.com/docs/
- **pytest Dokumentation**: https://docs.pytest.org/
- **BeautifulSoup Docs**: https://www.crummy.com/software/BeautifulSoup/
- **GitHub Actions**: https://docs.github.com/en/actions

## 🤝 Contributing

Contributions sind willkommen! 🎉

1. Fork das Repository
2. Feature Branch erstellen
3. Tests hinzufügen
4. Pull Request erstellen

Siehe auch: `CONTRIBUTING.md`

---

**Happy Coding! 🚀**

*Letzte Aktualisierung: November 2025*
