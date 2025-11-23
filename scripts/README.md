# 🤖 Scripts Directory

Dieser Ordner enthält **Automation- und Development-Scripts**.

## 📁 Struktur

```
scripts/
├── README.md          # Diese Datei
├── setup.sh           # Projekt-Setup (Dependencies installieren)
├── dev.sh             # Development-Server starten
├── add_todo.sh        # ⭐ Schnelle TODO-Erfassung
└── (weitere später)
```

---

## ⭐ Quick Start: TODO Management

### `add_todo.sh` - Schnellste TODO-Erfassung

**One-Liner:**
```bash
./scripts/add_todo.sh high "Wichtige Aufgabe"
```

**Mit Optionen:**
```bash
./scripts/add_todo.sh medium "Tests schreiben" \
  --command "pytest tests/" \
  --file "tests/test_new.py"
```

**Alias einrichten:**
```bash
echo 'alias todo="./scripts/add_todo.sh"' >> ~/.bashrc
source ~/.bashrc

# Dann:
todo high "Neue Aufgabe"
todo done "Erledigte Aufgabe"
```

**Priority Levels:**
- `high` / `h` / `1` → 🔴 High Priority
- `medium` / `m` / `2` → 🟡 Medium Priority
- `low` / `l` / `3` → 🔵 Low Priority
- `nice` / `n` / `4` → Nice to Have
- `done` / `d` / `✓` → Mark as completed

**Optionen:**
- `--command <cmd>` / `-c` → Shell-Kommando
- `--file <path>` / `-f` → Zugehörige Datei
- `--note <text>` / `-n` → Zusätzliche Notiz
- `--url <link>` / `-u` → Relevanter Link

**Beispiele:**

```bash
# Einfach
./scripts/add_todo.sh high "GitHub Actions aktivieren"

# Mit Command
./scripts/add_todo.sh medium "Tests laufen" -c "pytest tests/"

# Mit File + Note
./scripts/add_todo.sh low "Scraper erweitern" \
  -f "cli/scrapers/berghain.py" \
  -n "API Token benötigt"

# Mit URL
./scripts/add_todo.sh high "Token erstellen" \
  -u "https://developers.facebook.com/apps"

# TODO complete
./scripts/add_todo.sh done "CLI implementiert" -f "cli/event_scraper.py"

# Full Example
./scripts/add_todo.sh high "Instagram testen" \
  -c "./cli/event_scraper.py extract instagram punkinhof -n 5" \
  -f "cli/scrapers/punk_im_hof_instagram.py" \
  -n "Instaloader installieren"
```

**Features:**
- ✅ Interactive Git Commit
- ✅ Auto-Push Option
- ✅ Colored Output
- ✅ YAML bleibt strukturiert
- ✅ Metadata Auto-Update
- ✅ Dashboard-Link nach Push

---

## 🎯 Kommende Scripts (nach Phasen)

### Phase 1: Foundation

- ✅ `setup.sh` - Projekt einrichten
- ✅ `dev.sh` - Jekyll-Server starten
- [ ] `validate.py` - _config.yml & Frontmatter prüfen

### Phase 2: Content

- [ ] `new-event.sh` - Interaktiv neues Event erstellen
- [ ] `list-events.py` - Alle Events auflisten
- [ ] `test-event.py` - Event-Generator (Test-Daten)

### Phase 3: Automation

- [ ] `scrape-events.py` - Events von Websites scrapen
- [ ] `import-ical.py` - iCal-Feeds importieren
- [ ] `archive-old.py` - Alte Events archivieren

### Phase 4: Quality

- [ ] `test-all.sh` - Alle Tests ausführen
- [ ] `lint.sh` - Code-Style prüfen
- [ ] `check-links.py` - Broken Links finden

## 📝 Script-Konventionen

### Shebang & Executable

```bash
#!/usr/bin/env bash
# Macht Script ausführbar: chmod +x scripts/setup.sh
```

### Hilfe-Funktion

Jedes Script MUSS `--help` unterstützen:

```bash
#!/usr/bin/env bash

show_help() {
    cat << EOF
Usage: $0 [OPTIONS]

Description:
    Kurzbeschreibung was das Script tut

Options:
    -h, --help      Zeige diese Hilfe
    -v, --verbose   Ausführliche Logs
    
Examples:
    $0                    # Standard-Ausführung
    $0 --verbose          # Mit Debug-Output
EOF
}

# Parse arguments
case "$1" in
    -h|--help) show_help; exit 0 ;;
esac
```

### Fehlerbehandlung

```bash
set -e  # Bei Fehler abbrechen
set -u  # Unset variables = Fehler
set -o pipefail  # Pipe-Fehler erkennen

# Trap für Cleanup
trap 'echo "❌ Fehler in Zeile $LINENO"' ERR
```

### Farbige Ausgabe

```bash
# Farb-Definitionen
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'  # No Color

echo -e "${GREEN}✅ Erfolg${NC}"
echo -e "${RED}❌ Fehler${NC}"
echo -e "${YELLOW}⚠️  Warnung${NC}"
```

## 🐍 Python-Script-Konventionen

### Docstring & Argparse

```python
#!/usr/bin/env python3
"""
Event Validator
===============

Prüft Event-Markdown-Dateien auf Fehler.

Usage:
    python validate.py [--verbose]

Options:
    --verbose    Ausführliche Logs
    --help       Diese Hilfe anzeigen
"""

import argparse

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()
    
    # ...

if __name__ == '__main__':
    main()
```

### Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

logger.info("✅ Script gestartet")
logger.warning("⚠️  Warnung")
logger.error("❌ Fehler")
```

## 🔧 Verwendung

### Setup ausführen

```bash
# Von Projekt-Root
./scripts/setup.sh

# Mit Permissions-Fix
chmod +x scripts/*.sh
./scripts/setup.sh
```

### Python-Scripts

```bash
# Mit virtualenv (empfohlen)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/validate.py --help

# Ohne virtualenv
python3 scripts/validate.py
```

## 🎯 Best Practices

### 1. Idempotenz

Scripts sollen **mehrfach ausführbar** sein ohne Fehler:

```bash
# ✅ Gut: Prüft ob schon existiert
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# ❌ Schlecht: Fehlschlag bei 2. Ausführung
python3 -m venv .venv  # Error: Directory exists
```

### 2. Dry-Run-Modus

```bash
DRY_RUN=false

if [ "$DRY_RUN" = true ]; then
    echo "[DRY RUN] Würde löschen: $file"
else
    rm "$file"
fi
```

### 3. Fortschritts-Anzeige

```bash
total=100
for i in $(seq 1 $total); do
    echo -ne "Fortschritt: $i/$total\r"
    # Arbeit...
done
echo ""  # Newline nach Fortschritt
```

### 4. Exit-Codes

```bash
# 0 = Erfolg
exit 0

# 1 = Allgemeiner Fehler
exit 1

# 2 = Falsche Parameter
exit 2
```

## 🧪 Testing

### Script-Tests (später)

```bash
# test_scripts.sh
#!/usr/bin/env bash

test_setup() {
    ./scripts/setup.sh
    [ -d ".venv" ] || exit 1
    echo "✅ setup.sh funktioniert"
}

test_setup
```

## 📚 Weitere Infos

- **[Bash Style Guide](https://google.github.io/styleguide/shellguide.html)**
- **[Python PEP 8](https://pep8.org/)**
- **[Development Guide](../ENTWICKLER.md)**

---

**Stand:** November 2025 | [Zurück zur Hauptdokumentation](../README.md)
