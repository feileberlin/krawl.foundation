# CLI Tools - krawl.foundation

Command-line tools für Event-Scraping und Datenmanagement.

## 🚀 Quick Start

```bash
# Installation
pip install -r requirements.txt

# CLI ausführbar machen
chmod +x cli/event_scraper.py

# Hilfe anzeigen
./cli/event_scraper.py

# Oder direkt mit Python
python cli/event_scraper.py
```

## 📋 Kommandoreferenz

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

**Was wird verglichen:**
- Neue Felder (in event2, aber nicht in event1)
- Entfernte Felder (in event1, aber nicht in event2)
- Geänderte Felder mit Alt/Neu-Werten
- Unveränderte Felder

### `merge` - Events zusammenführen

```bash
# Alle Felder mergen
./cli/event_scraper.py merge base.json updates.json -o output.json

# Nur spezifische Felder
./cli/event_scraper.py merge base.json updates.json \
  -f title,date,venue -o output.json
```

**Use Cases:**
- Automatisch gescrapte Daten mit manuell kuratierten zusammenführen
- Einzelne Felder von externen Quellen übernehmen
- Bulk-Updates mit selektivem Merge

### `generate` - Test-Events erzeugen

```bash
# Ein Concert-Event
./cli/event_scraper.py generate

# 10 Events
./cli/event_scraper.py generate --count 10

# Exhibition-Events
./cli/event_scraper.py generate --type exhibition -n 5

# In anderes Verzeichnis
./cli/event_scraper.py generate -n 20 -o tests/fixtures
```

**Generierte Felder:**
- Titel (realistisch mit Faker)
- Datum (zukünftig, nächste 90 Tage)
- Location (deutsche Städte)
- Description (Lorem Ipsum Text)
- Venue, URL, Genre/Typ, Preis

### `bulk` - Massenoperationen

```bash
# Feld in allen Events setzen
./cli/event_scraper.py bulk --set-field status published

# Erst testen (Dry Run)
./cli/event_scraper.py bulk --set-field status draft --dry-run
```

### `scrape` - Events scrapen (TODO)

```bash
# Von URL scrapen
./cli/event_scraper.py scrape https://example.com/events -o new_events.json

# Und direkt mit existierenden vergleichen
./cli/event_scraper.py scrape https://example.com/events -c existing.json
```

## 🔧 Workflows

### Workflow 1: Neue Events von Website scrapen

```bash
# 1. Scrape
./cli/event_scraper.py scrape https://venue.com/events -o scraped.json

# 2. Vergleich mit existierendem Event
./cli/event_scraper.py diff _events/existing-event.json scraped.json

# 3. Selektives Merge (z.B. nur Titel und Datum aktualisieren)
./cli/event_scraper.py merge \
  _events/existing-event.json \
  scraped.json \
  -f title,date \
  -o _events/existing-event.json
```

### Workflow 2: Test-Daten für Development

```bash
# Testdaten generieren
./cli/event_scraper.py generate -n 50 -o tests/fixtures

# Mit verschiedenen Typen
./cli/event_scraper.py generate -n 25 --type concert -o tests/fixtures
./cli/event_scraper.py generate -n 25 --type exhibition -o tests/fixtures
```

### Workflow 3: Bulk-Update aller Events

```bash
# Dry-Run: Sehen was passieren würde
./cli/event_scraper.py bulk --set-field reviewed true --dry-run

# Tatsächlich ausführen
./cli/event_scraper.py bulk --set-field reviewed true

# Status für alle auf draft
./cli/event_scraper.py bulk --set-field status draft
```

## 🎯 Best Practices

### 1. Immer Backups vor Bulk-Operations
```bash
# Events sichern
cp -r _events _events.backup.$(date +%Y%m%d-%H%M%S)

# Oder mit Git
git add _events && git commit -m "backup before bulk operation"
```

### 2. Dry-Run nutzen
```bash
# Erst prüfen
./cli/event_scraper.py bulk --set-field status published --dry-run

# Dann ausführen
./cli/event_scraper.py bulk --set-field status published
```

### 3. Strukturiertes Merge-Workflow
```bash
# 1. Diff checken
./cli/event_scraper.py diff old.json new.json

# 2. Gezielt einzelne Felder mergen
./cli/event_scraper.py merge old.json new.json -f date,venue -o merged.json

# 3. Review
cat merged.json | jq .

# 4. Übernehmen
mv merged.json _events/final-event.json
```

### 4. Event-IDs konsistent halten
- Nutze URL oder eindeutige externe ID als Basis
- Format: `{venue}-{date}-{slug}` (z.B. `berghain-2025-12-01-techno-night`)
- Verhindert Duplikate

### 5. Status-Workflow implementieren
```json
{
  "status": "draft",      // Gerade erstellt/gescraped
  "status": "reviewed",   // Redaktionell geprüft
  "status": "published",  // Live auf Website
  "status": "archived"    // Event ist vorbei
}
```

## 🔮 Geplante Features

- [ ] **Smart Deduplication**: Events automatisch als Duplikat erkennen
- [ ] **Filter in Bulk**: `--filter "status==draft"` für selektive Updates
- [ ] **Diff-Visualisierung**: Colored terminal output für Unterschiede
- [ ] **Import/Export**: CSV, iCal, andere Formate
- [ ] **Validation**: JSON Schema für Event-Struktur
- [ ] **History**: Git-basierte Change-Tracking

## 🐛 Debugging

```bash
# Python im verbose mode
python -v cli/event_scraper.py list

# Mit Debugger
python -m pdb cli/event_scraper.py diff event1.json event2.json

# Output in Datei für Analyse
./cli/event_scraper.py list --format json > debug-output.json
```

## 📚 Weitere Ressourcen

- `/tests/` - Unit Tests und Fixtures
- `/docs/` - Erweiterte Dokumentation
- `.github/workflows/` - GitHub Actions Setup
