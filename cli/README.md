# CLI Tools - KRaWL> Foundation

Command-line tools für Event-Scraping, OCR und Datenmanagement.

## 🚀 Quick Start

```bash
# Installation
pip install -r requirements.txt
sudo apt-get install tesseract-ocr tesseract-ocr-deu  # Für OCR

# CLI ausführbar machen
chmod +x cli/event_scraper.py
chmod +x cli/image_extractor.py

# Hilfe anzeigen
./cli/event_scraper.py --help
./cli/image_extractor.py --help
```

## 📋 event_scraper.py - Event Management

### `list` - Events auflisten

```bash
# Als Tabelle
./cli/event_scraper.py list

# Als JSON
./cli/event_scraper.py list --format json
```

### `diff` - Events vergleichen

```bash
# Text-Ausgabe
./cli/event_scraper.py diff event1.json event2.json

# JSON-Ausgabe
./cli/event_scraper.py diff event1.json event2.json --format json
```

### `merge` - Events zusammenführen

```bash
# Alle Felder mergen
./cli/event_scraper.py merge base.json updates.json -o output.json

# Nur spezifische Felder
./cli/event_scraper.py merge base.json updates.json \
  -f title,date,venue -o output.json
```

### `generate` - Test-Events erzeugen

```bash
# 10 Events
./cli/event_scraper.py generate --count 10

# In anderes Verzeichnis
./cli/event_scraper.py generate -n 20 -o tests/fixtures
```

### `bulk` - Massenoperationen

```bash
# Feld in allen Events setzen
./cli/event_scraper.py bulk --set-field status published

# Erst testen (Dry Run)
./cli/event_scraper.py bulk --set-field status draft --dry-run
```

## 🔍 image_extractor.py - Batch OCR Processing

**Neu in Version 2.0:** Vollautomatische Batch-OCR ohne User-Interaktion.

### Local Files - Batch OCR

```bash
# Single file
./cli/image_extractor.py local flyer.jpg --ocr --output-dir _events

# Entire directory (non-recursive)
./cli/image_extractor.py local /path/to/flyers/ --ocr -o _events

# Recursive scan
./cli/image_extractor.py local /path/to/flyers/ --ocr -r -o _events

# Save all results to single JSON
./cli/image_extractor.py local .cache/telegram/ \
  --ocr \
  --output-json results.json \
  --output-dir _events
```

### Instagram - Batch OCR

```bash
# Latest 5 posts with OCR
./cli/image_extractor.py instagram punkinhof --count 5 --ocr

# More posts
./cli/image_extractor.py instagram punkinhof -n 10 --ocr -o _events
```

### Facebook - Batch OCR

```bash
# Requires FB_TOKEN
./cli/image_extractor.py facebook GaleriehausHof \
  --fb-token YOUR_TOKEN \
  --count 5 \
  --ocr \
  -o _events
```

## 🔧 Workflows

### Workflow 1: Telegram Flyer Processing

```bash
# Simuliere Telegram-Upload (lokal)
cp flyer.jpg .cache/telegram/

# Batch OCR
./cli/image_extractor.py local .cache/telegram/ \
  --ocr \
  --output-json telegram_events.json \
  -o _events

# Review Drafts
cat telegram_events.json | jq .

# Approve Draft
./cli/event_scraper.py bulk --set-field status reviewed
```

### Workflow 2: Instagram Scraping Pipeline

```bash
# 1. Extract mit OCR
./cli/image_extractor.py instagram punkinhof -n 10 --ocr -o _events

# 2. Liste neue Drafts
./cli/event_scraper.py list --format json | jq 'select(.status == "draft")'

# 3. Bulk-Review
./cli/event_scraper.py bulk --set-field status reviewed
```

### Workflow 3: Bulk-Update aller Events

```bash
# Dry-Run: Sehen was passieren würde
./cli/event_scraper.py bulk --set-field reviewed true --dry-run

# Tatsächlich ausführen
./cli/event_scraper.py bulk --set-field reviewed true
```

## 🆕 Änderungen in Version 2.0

### ✅ Neu
- **Batch OCR:** Vollautomatische Verarbeitung ohne User-Interaktion
- **Smart Parsing:** Automatische Extraktion von Datum, Uhrzeit, Venue
- **Telegram Integration:** Direkter Support für Telegram Bot Uploads
- **JSON Output:** `--output-json` für strukturierte Batch-Results

### ❌ Entfernt
- **Interaktiver Editor:** Keine User-Prompts mehr (war: `interactive_event_editor()`)
- **Terminal Image Viewer:** Keine imgcat/chafa Integration mehr
- **Manual Input:** Keine Feld-für-Feld Eingabe mehr

### 🔄 Migrationsguide

**Alt (Version 1.0):**
```bash
# Interaktiver Modus (deprecated)
./cli/image_extractor.py local flyer.jpg --ocr
# → Prompted für jeden Event-Feld
```

**Neu (Version 2.0):**
```bash
# Batch-Modus (automatisch)
./cli/image_extractor.py local flyer.jpg --ocr -o _events
# → Automatische OCR + Parsing
# → Direkt als Draft gespeichert
```

## 🎯 Best Practices

### 1. Immer Backups vor Bulk-Operations
```bash
cp -r _events _events.backup.$(date +%Y%m%d-%H%M%S)
```

### 2. OCR-Qualität verbessern
- Scharfes Foto
- Gute Beleuchtung
- Text nicht zu klein

### 3. Status-Workflow
```json
{
  "status": "draft",      // Gerade erstellt/gescraped
  "status": "reviewed",   // Redaktionell geprüft
  "status": "published"   // Live auf Website
}
```

## 📚 Weitere Ressourcen

- `/tests/` - Unit Tests und Fixtures
- `/docs/` - Erweiterte Dokumentation
- `.github/workflows/` - GitHub Actions Setup
- `docs/TELEGRAM_SUBMISSIONS.md` - Telegram Bot Setup
- `docs/SECRETS.md` - Secrets Management
- `docs/WORKFLOWS.md` - GitHub Actions Workflows
