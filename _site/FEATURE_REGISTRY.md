# 🎯 Feature Registry - krawl.foundation

**Single Source of Truth für alle aktiven Features im Event-Scraper.**

---

**Last Updated:** 2025-11-21  
**Maintainer:** feileberlin  
**Purpose:** Verhindert versehentliches Löschen/Überschreiben von Features bei Änderungen

---

⚠️ **WICHTIG:** Bei jeder Feature-Addition/Removal diese Datei aktualisieren!

---

## 📋 Core Features (Aktiv)

### CLI Commands

| Command | Status | File | Description | Added |
|---------|--------|------|-------------|-------|
| `list` | ✅ Active | `cli/event_scraper.py` | Liste alle Events (Tabelle/JSON) | 2025-11-21 |
| `diff` | ✅ Active | `cli/event_scraper.py` | Vergleiche zwei Events, zeige Unterschiede | 2025-11-21 |
| `merge` | ✅ Active | `cli/event_scraper.py` | Merge Events (alle/selektive Felder) | 2025-11-21 |
| `generate` | ✅ Active | `cli/event_scraper.py` | Generiere Lorem-Ipsum Test-Events | 2025-11-21 |
| `bulk` | ✅ Active | `cli/event_scraper.py` | Bulk-Operations mit Dry-Run | 2025-11-21 |
| `scrape` | ⚠️ Placeholder | `cli/event_scraper.py` | Event-Scraping (zu implementieren) | 2025-11-21 |
| `extract` | ✅ Active | `cli/event_scraper.py` | **NEU:** Extrahiere Events aus Social Media Bildern (interaktiv) | 2025-11-21 |

### Event Management

| Feature | Status | File | Description | Added |
|---------|--------|------|-------------|-------|
| JSON Save/Load | ✅ Active | `cli/event_scraper.py:EventManager` | Events als JSON speichern/laden | 2025-11-21 |
| Markdown Save/Load | ✅ Active | `cli/event_scraper.py:EventManager` | Events als Markdown mit Frontmatter | 2025-11-21 |
| Event Comparison | ✅ Active | `cli/event_scraper.py:EventManager.compare_events()` | Diff zwischen zwei Events | 2025-11-21 |
| Selective Merge | ✅ Active | `cli/event_scraper.py:EventManager.merge_events()` | Merge nur spezifischer Felder | 2025-11-21 |
| Event Validation | ✅ Active | `cli/event_scraper.py:EventManager.validate_event()` | Prüfe Pflichtfelder | 2025-11-21 |
| Test Data Generation | ✅ Active | `cli/event_scraper.py:EventManager.generate_test_event()` | Lorem Ipsum Events mit Faker | 2025-11-21 |

### Scraper Framework

| Feature | Status | File | Description | Added |
|---------|--------|------|-------------|-------|
| Base Scraper | ✅ Active | `cli/scrapers/base.py` | Abstract Base Class für alle Scraper | 2025-11-21 |
| HTML Fetching | ✅ Active | `cli/scrapers/base.py:fetch_page()` | HTTP Requests mit Session | 2025-11-21 |
| HTML Parsing | ✅ Active | `cli/scrapers/base.py:parse_html()` | BeautifulSoup Integration | 2025-11-21 |
| Event Normalization | ✅ Active | `cli/scrapers/base.py:normalize_event()` | Standard-Format für Events | 2025-11-21 |
| Date Parsing | ✅ Active | `cli/scrapers/base.py:_parse_date()` | Flexible Datums-Formate | 2025-11-21 |

### Scraper Implementations

| Scraper | Status | File | Source | Added |
|---------|--------|------|--------|-------|
| Example Venue | ✅ Template | `cli/scrapers/example_venue.py` | Template für eigene Scraper | 2025-11-21 |
| GaleriehausHof (Facebook) | ⚠️ Partial | `cli/scrapers/galeriehaus_hof_facebook.py` | Facebook Events (Selenium/Graph API) | 2025-11-21 |
| Punk im Hof (Instagram) | ⚠️ Partial | `cli/scrapers/punk_im_hof_instagram.py` | Instagram Posts (Instaloader/Graph API) | 2025-11-21 |

### Image Extraction (NEW!)

| Feature | Status | File | Description | Added |
|---------|--------|------|-------------|-------|
| Image Stream Extractor | ✅ Active | `cli/image_extractor.py` | Lade Bilder von Social Media | 2025-11-21 |
| Instagram Image Fetch | ✅ Active | `cli/image_extractor.py:fetch_instagram_images()` | Top N Bilder von Instagram | 2025-11-21 |
| Facebook Image Fetch | ⚠️ API Required | `cli/image_extractor.py:fetch_facebook_images()` | Top N Bilder von Facebook (Graph API) | 2025-11-21 |
| OCR Integration | ⚠️ Optional | `cli/image_extractor.py:extract_text_from_image()` | Tesseract OCR für Textextraktion | 2025-11-21 |
| Terminal Image Display | ⚠️ Optional | `cli/image_extractor.py:display_image_in_terminal()` | imgcat/chafa für Bild-Preview | 2025-11-21 |
| Interactive Editor | ✅ Active | `cli/image_extractor.py:interactive_event_editor()` | CLI-Editor für Event-Erstellung aus Bildern | 2025-11-21 |

### Testing

| Feature | Status | File | Description | Added |
|---------|--------|------|-------------|-------|
| Unit Tests | ✅ Active | `tests/test_event_scraper.py` | pytest-basierte Tests | 2025-11-21 |
| EventManager Tests | ✅ Active | `tests/test_event_scraper.py:TestEventManager` | Save/Load/Compare/Merge | 2025-11-21 |
| CLI Tests | ✅ Active | `tests/test_event_scraper.py:TestCLI` | Command-Testing | 2025-11-21 |
| Fixtures | ✅ Active | `tests/test_event_scraper.py` | pytest fixtures für Events | 2025-11-21 |

### CI/CD

| Feature | Status | File | Description | Added |
|---------|--------|------|-------------|-------|
| Test Workflow | ✅ Active | `.github/workflows/test.yml` | Multi-Python Tests (3.9-3.12) | 2025-11-21 |
| Scrape Workflow | ✅ Active | `.github/workflows/scrape-events.yml` | Auto-Scraping (Cron + Manual) | 2025-11-21 |
| Coverage Reports | ✅ Active | `.github/workflows/test.yml` | codecov Integration | 2025-11-21 |

---

## 🔮 Planned Features (Roadmap)

| Feature | Priority | Description | Status | Target |
|---------|----------|-------------|--------|--------|
| Smart Deduplication | High | Automatische Duplikat-Erkennung | 📋 Planned | - |
| Filter in Bulk | High | `--filter "status==draft"` für selektive Updates | 📋 Planned | - |
| JSON Schema Validation | Medium | Event-Struktur validieren | 📋 Planned | - |
| CSV Export | Medium | Events als CSV exportieren | 📋 Planned | - |
| iCal Export | Low | Events als .ics für Kalender | 📋 Planned | - |
| Web UI | Low | Optional Flask/FastAPI Interface | 📋 Planned | - |
| Event History | Medium | Git-basierte Change-Tracking | 📋 Planned | - |

---

## 🗂️ File Structure

```
cli/
├── event_scraper.py          # Haupt-CLI (EventManager + Commands)
├── image_extractor.py         # NEW: Image Stream Extraction
└── scrapers/
    ├── __init__.py
    ├── base.py                # Base Scraper Class
    ├── example_venue.py       # Template
    ├── galeriehaus_hof_facebook.py
    └── punk_im_hof_instagram.py

tests/
└── test_event_scraper.py      # Unit Tests

.github/workflows/
├── test.yml                   # CI Tests
└── scrape-events.yml          # Auto-Scraping
```

---

## 📦 Dependencies

### Core
- `requests` - HTTP Client
- `beautifulsoup4` - HTML Parsing
- `lxml` - XML/HTML Parser
- `pyyaml` - YAML Support
- `python-dateutil` - Date Parsing

### Testing
- `pytest` - Test Framework
- `pytest-cov` - Coverage Reports
- `faker` - Test Data Generation
- `black` - Code Formatting

### Optional (für spezifische Features)
- `selenium` - Browser Automation (Facebook Scraping)
- `instaloader` - Instagram Scraping
- `pytesseract` - OCR für Bilder
- `pillow` - Image Processing

---

## 🚨 Critical Components (NICHT LÖSCHEN!)

### Must Keep Files
- `cli/event_scraper.py` - Core CLI
- `cli/scrapers/base.py` - Scraper Framework
- `tests/test_event_scraper.py` - Tests
- `.github/workflows/*.yml` - CI/CD

### Protected Functions
- `EventManager.compare_events()` - Diff Logic
- `EventManager.merge_events()` - Merge mit selective fields
- `EventManager.normalize_event()` - Data Normalization
- `ImageStreamExtractor.interactive_event_editor()` - **NEU:** Interaktiver Editor

---

## 📝 Changelog

### 2025-11-21 - Initial Setup
- ✅ CLI mit 7 Commands (list, diff, merge, generate, bulk, scrape, **extract**)
- ✅ EventManager für JSON/Markdown
- ✅ Scraper Framework mit Base Class
- ✅ Tests mit pytest
- ✅ GitHub Actions (test + scrape)
- ✅ **NEW:** Image Stream Extractor für Social Media
- ✅ **NEW:** Interaktiver Editor (Bild + Text → Event JSON)
- 📋 Scraper Templates für Facebook/Instagram

---

## 🔄 Update-Protocol

**Bei Feature-Änderungen:**

1. ✅ Feature in diesem Dokument aktualisieren
2. ✅ Status ändern (Active/Deprecated/Removed)
3. ✅ Changelog-Eintrag hinzufügen
4. ✅ Tests aktualisieren falls nötig
5. ✅ README.md aktualisieren falls User-facing

**Bei neuen Features:**

1. ✅ Eintrag in entsprechende Tabelle
2. ✅ File-Referenz hinzufügen
3. ✅ Status auf "Active" setzen
4. ✅ Added-Datum eintragen
5. ✅ Changelog-Eintrag

---

**Ende Feature Registry**

*Letzte Überprüfung: 2025-11-21*
