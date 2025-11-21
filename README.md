# 🎪 krawl.foundation

**Event-Scraper CLI mit Diff, Merge und Bulk-Operations für strukturiertes Event-Datenmanagement.**

> Ein KISS-Prinzip Projekt zum Scrapen, Vergleichen und Verwalten von Event-Daten. Von Grund auf neu strukturiert, um aus früheren Erfahrungen (krawl.ist) zu lernen.

## 🎯 Ziele

- **Lernerfreundlich**: Klare Struktur, durchgehend dokumentiert, debugfreundlich
- **CLI-First**: Kommandozeilen-Tool für alle Operationen
- **Datenmanagement**: Events scrapen, vergleichen (diff), selektiv mergen
- **Automatisierung**: GitHub Actions für periodisches Scraping
- **Best Practices**: Moderne Python-Patterns, Testing, CI/CD

## 🚀 Quick Start

```bash
# 1. Repository klonen
git clone https://github.com/feileberlin/krawl.foundation.git
cd krawl.foundation

# 2. Setup ausführen
./scripts/setup.sh

# 3. Virtual Environment aktivieren
source venv/bin/activate

# 4. CLI nutzen
./cli/event_scraper.py --help
```

## 📋 Features

### ✅ Implementiert

- **List**: Alle Events auflisten (Tabelle oder JSON)
- **Diff**: Zwei Events vergleichen, Unterschiede identifizieren
- **Merge**: Events zusammenführen (alle Felder oder selektiv)
- **Generate**: Lorem-Ipsum Test-Events nach Typ generieren
- **Bulk**: Massenoperationen auf alle Events (mit Dry-Run)
- **Testing**: Unit-Tests für alle Core-Funktionen
- **CI/CD**: GitHub Actions für Tests und Auto-Scraping

### 🔮 Geplant

- [ ] **Scraper-Implementierung**: Spezifische Scraper für Venues
- [ ] **Smart Deduplication**: Automatische Duplikat-Erkennung
- [ ] **Filter**: Bulk-Operations mit Filtern
- [ ] **Validation**: JSON Schema für Event-Struktur
- [ ] **Export**: CSV, iCal, andere Formate

## 📚 Dokumentation

- **[CLI Kommandoreferenz](cli/README.md)**: Alle Commands, Workflows, Best Practices
- **[Getting Started](docs/01-GETTING_STARTED.md)**: Detaillierte Einführung
- **[CONTRIBUTING](CONTRIBUTING.md)**: Wie du beitragen kannst

## 🛠️ Projekt-Struktur

```
krawl.foundation/
├── cli/                      # CLI-Tool
│   ├── event_scraper.py      # Haupt-CLI Script
│   └── README.md             # Kommandoreferenz
├── tests/                    # Unit Tests
│   └── test_event_scraper.py
├── _events/                  # Event-Dateien (JSON/Markdown)
├── _data/                    # Zusätzliche Daten
├── scripts/                  # Setup & Dev Scripts
│   └── setup.sh
├── .github/workflows/        # GitHub Actions
│   ├── scrape-events.yml     # Auto-Scraping
│   └── test.yml              # Tests
└── requirements.txt          # Python Dependencies
```

## 🎓 Workflows

### Event scrapen und vergleichen

```bash
# 1. Von URL scrapen (wenn implementiert)
./cli/event_scraper.py scrape https://venue.com/events -o new.json

# 2. Mit existierendem Event vergleichen
./cli/event_scraper.py diff _events/existing.json new.json

# 3. Selektiv mergen (nur bestimmte Felder)
./cli/event_scraper.py merge _events/existing.json new.json \
  -f title,date,venue -o _events/existing.json
```

### Test-Daten generieren

```bash
# 50 Test-Events für Development
./cli/event_scraper.py generate -n 50

# Nach Typ
./cli/event_scraper.py generate --type concert -n 25
./cli/event_scraper.py generate --type exhibition -n 25
```

### Bulk-Update

```bash
# Dry-Run: Was würde passieren?
./cli/event_scraper.py bulk --set-field status published --dry-run

# Tatsächlich ausführen
./cli/event_scraper.py bulk --set-field status published
```

## 🤖 GitHub Actions

### Manual Trigger

1. Gehe zu **Actions** → **Scrape Events**
2. Klicke **Run workflow**
3. Optional: URL eingeben oder Test-Events generieren

### Automatisch

- Jeden Montag um 8:00 Uhr (konfigurierbar in `.github/workflows/scrape-events.yml`)

## 🧪 Testing

```bash
# Alle Tests ausführen
pytest tests/ -v

# Mit Coverage
pytest tests/ --cov=cli --cov-report=term

# Einzelner Test
pytest tests/test_event_scraper.py::TestEventManager::test_compare_events -v
```

## 💡 Best Practices

1. **Backups vor Bulk-Operations**: `git commit` oder Copy
2. **Dry-Run nutzen**: Erst `--dry-run`, dann real
3. **Event-IDs konsistent**: `{venue}-{date}-{slug}` Format
4. **Status-Workflow**: draft → reviewed → published → archived
5. **Dokumentation aktuell halten**: Jede Änderung dokumentieren

## 🤝 Contributing

Siehe [CONTRIBUTING.md](CONTRIBUTING.md) für Guidelines.

## 📄 License

MIT License - siehe [LICENSE](LICENSE)

## 🙏 Acknowledgments

- Inspiration: [krawl.ist](https://github.com/feileberlin/krawl.ist)
- Built with: Python, pytest, faker, BeautifulSoup4
- Hosted on: GitHub Pages
