# 🎪 KRaWL> Foundation

**Deine Event-Plattform für Kultur und Nightlife – einfach, offen und für alle! 🎉**

> Ein KISS-Prinzip Projekt zum Entdecken, Sammeln und Verwalten von Events. Mit CLI-Tools für Entwickler, Web-Interface für User und automatischer Scraping-Pipeline für immer aktuelle Events.

## 🎯 Was ist KRaWL> Foundation?

KRaWL> Foundation ist eine **Open Source Event-Plattform**, die:
- 🗺️ **Events auf einer Karte zeigt** (interaktiv, dark mode, responsive)
- 📸 **Telegram Bot** für einfache Event-Submissions (Foto hochladen → fertig!)
- 🤖 **Automatisches Scraping** von Instagram, Facebook & Co.
- 🛠️ **CLI-Tools** für Entwickler (diff, merge, bulk-operations)
- ✨ **Komplett kostenlos & werbefrei**

**Für wen?**
- 🎉 **User**: Events entdecken, einreichen, Favoriten speichern
- 📝 **Redaktion**: Submissions moderieren, Events kuratieren
- 🛠️ **Entwickler**: Scraper bauen, Features entwickeln, beitragen

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

### ✅ Funktioniert

- ✅ **Interaktive Karte**: Dark Mode, responsive, Touch-freundlich
- ✅ **Event-Verwaltung**: List, Diff, Merge, Bulk-Operations
- ✅ **Image Extraction**: OCR für Social Media Flyer (Instagram, lokal)
- ✅ **Test-Daten**: Lorem-Ipsum Generator für Development
- ✅ **Telegram Bot**: Event-Submissions via Foto
- ✅ **Auto-Scraping**: GitHub Actions für Instagram (alle 12h)
- ✅ **Testing**: Unit-Tests mit pytest, CI/CD Pipeline

### ⚠️ Teilweise / In Arbeit

- ~~**Facebook Scraper**~~: ⚠️ Benötigt Facebook API Token
- ~~**Instagram Scraper**~~: ⚠️ Teilweise funktionsfähig
- ~~**URL Scraper**~~: ⚠️ Nur Placeholder, noch nicht implementiert

### 🔮 Geplant

- [ ] **Smart Deduplication**: Automatische Duplikat-Erkennung
- [ ] **Filter-Optionen**: Erweiterte Suche & Filter
- [ ] **JSON Schema**: Event-Struktur validieren
- [ ] **Export**: CSV, iCal für Kalender
- [ ] **Bewertungen**: Community-Feedback zu Events

## 📚 Dokumentation

**Neu organisiert! 🎉** Die Dokumentation ist jetzt auf drei Zielgruppen aufgeteilt:

### 👥 Ich bin...

**🛠️ Entwickler/in**
→ **[ENTWICKLER.md](ENTWICKLER.md)**
- Setup & Installation
- CLI-Tools & Scraper-Framework
- Testing, CI/CD, Debugging

**📝 Redakteur/in oder Admin**
→ **[REDAKTION.md](REDAKTION.md)**
- Event-Moderation & Review
- Telegram-Submissions prüfen
- Content-Management

**🎉 Benutzer/in**
→ **[BENUTZER.md](BENUTZER.md)**
- Karte nutzen & Events entdecken
- Events einreichen via Telegram
- Favoriten & Tipps

### 📦 Weitere Ressourcen

- **[FEATURE_REGISTRY.md](FEATURE_REGISTRY.md)**: Vollständige Feature-Liste mit Status
- **[CONTRIBUTING.md](CONTRIBUTING.md)**: Contribution Guidelines
- **[docs/](docs/)**: Technische Details & Archiv

## 🛠️ Projekt-Struktur

```
KRaWL> Foundation/
├── cli/                        # CLI-Tools
│   ├── event_scraper.py        # Event-Management (list, diff, merge, bulk)
│   ├── image_extractor.py      # OCR & Social Media Extraction
│   ├── voice_transcriber.py    # Spracherkennung (VOSK)
│   └── scrapers/               # Scraper-Framework
├── tests/                      # Unit Tests (pytest)
├── _events/                    # Event-Dateien (JSON/Markdown)
├── assets/                     # CSS, JS, Bilder
│   ├── css/map.scss            # Map-Styling
│   └── js/map.js               # Map-Interaktionen
├── scripts/                    # Setup & Dev Scripts
│   ├── setup.sh                # One-Command Setup
│   └── telegram_bot.py         # Telegram Bot
├── .github/workflows/          # GitHub Actions (CI/CD)
├── index.html                  # Startseite
├── map.html                    # Interaktive Karte
├── dashboard.html              # Admin Dashboard
├── ENTWICKLER.md               # Entwickler-Doku
├── REDAKTION.md                # Redaktions-Doku
└── BENUTZER.md                 # Benutzer-Doku
```

## 🎓 Beispiele

### Für User: Events einreichen

```
1. Öffne Telegram Bot: t.me/krawlfoundation_bot
2. Sende Flyer-Foto
3. Fertig! ✨
```

### Für Redaktion: Events freigeben

```bash
# Drafts anzeigen
./cli/event_scraper.py list | grep draft

# Auf "reviewed" setzen
./cli/event_scraper.py bulk --set-field status reviewed
```

### Für Entwickler: Test-Daten

```bash
# 50 Test-Events generieren
./cli/event_scraper.py generate -n 50

# Events vergleichen
./cli/event_scraper.py diff event1.json event2.json
```

## 🤖 Automatisierung

**GitHub Actions sorgen für immer aktuelle Events:**

- ⏰ **Auto-Scraping**: Alle 12 Stunden (3am & 3pm UTC)
- 📸 **Telegram Processing**: Sofort bei Upload
- 🔔 **Draft Alerts**: Alle 6 Stunden für wartende Drafts
- 🚀 **Deploy**: Automatisch bei Push auf `main`

**Manuell triggern:**
```bash
gh workflow run scrape-events.yml -f event_count=5
```

Details: **[ENTWICKLER.md](ENTWICKLER.md)** → GitHub Actions

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
