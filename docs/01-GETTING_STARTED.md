# 🚀 Getting Started Guide

> **Zielgruppe**: Einsteiger  
> **Voraussetzungen**: Keine  
> **Zeitaufwand**: ~15 Minuten

## 📋 Übersicht

Dieser Guide führt dich Schritt für Schritt durch:
1. Lokale Installation
2. Erstes Event erstellen
3. Development-Server starten
4. Auf GitHub Pages deployen

---

## 1️⃣ Lokale Installation

### Voraussetzungen prüfen

```bash
# Ruby (für Jekyll)
ruby --version
# Sollte >= 3.0 sein

# Python (für Scripts)
python3 --version
# Sollte >= 3.9 sein
```

Falls nicht installiert:
- **Ruby**: [ruby-lang.org/de](https://www.ruby-lang.org/de/downloads/)
- **Python**: [python.org/downloads](https://www.python.org/downloads/)

### Repository klonen

```bash
# Via HTTPS
git clone https://github.com/feileberlin/krawl.foundation.git
cd krawl.foundation

# ODER via SSH
git clone git@github.com:feileberlin/krawl.foundation.git
cd krawl.foundation
```

### Setup ausführen

```bash
# Dependencies installieren
chmod +x scripts/setup.sh
./scripts/setup.sh

# Bei Problemen: Verbose-Output
./scripts/setup.sh --verbose
```

Was macht `setup.sh`?
- ✅ Installiert Jekyll & Plugins (Ruby)
- ✅ Erstellt Python Virtual Environment
- ✅ Installiert Python-Pakete
- ✅ Erstellt fehlende Ordner
- ✅ Macht Scripts ausführbar

---

## 2️⃣ Erstes Event erstellen

### Methode 1: Beispiel-Event kopieren

```bash
# Kopiere Beispiel
cp _events/2025-12-01-beispiel-konzert.md _events/$(date +%Y-%m-%d)-mein-event.md

# Bearbeite mit deinem Editor
code _events/$(date +%Y-%m-%d)-mein-event.md
# oder: nano, vim, etc.
```

### Methode 2: Von Grund auf

Erstelle Datei: `_events/2025-12-15-weihnachtsmarkt.md`

```yaml
---
layout: event
title: "Weihnachtsmarkt am Rathaus"
date: 2025-12-15 14:00
published: true

categories:
  - festival
  - familie

location:
  name: "Rathausplatz"
  address: "Am Rathaus 1"
  city: "Berlin"

price: "Kostenlos"
---

Traditioneller Weihnachtsmarkt mit:
- Glühwein & Bratwurst
- Kunsthandwerk
- Live-Musik

Für die ganze Familie!
```

### Frontmatter-Felder erklärt

| Feld | Pflicht? | Beschreibung | Beispiel |
|------|----------|--------------|----------|
| `layout` | ✅ | Template | `event` |
| `title` | ✅ | Event-Name | `"Konzert im Park"` |
| `date` | ✅ | Start | `2025-12-01 20:00` |
| `published` | ✅ | Veröffentlicht? | `true` / `false` |
| `categories` | ❌ | Tags | `[konzert, live-musik]` |
| `location` | ❌ | Ort | `name`, `address`, `city` |
| `price` | ❌ | Eintritt | `"10€"` oder `"Kostenlos"` |
| `url` | ❌ | Website | `"https://..."` |

Vollständige Liste: [02-DATA_MODEL.md](02-DATA_MODEL.md)

---

## 3️⃣ Development-Server starten

```bash
# Server starten
./scripts/dev.sh

# ODER ohne Live-Reload
./scripts/dev.sh --no-live-reload
```

**Server-URL**: http://localhost:4000

### Was passiert?

1. Jekyll baut die Website aus Markdown
2. Browser öffnen → http://localhost:4000
3. Datei speichern → Automatischer Rebuild
4. Browser aktualisiert sich automatisch (Live-Reload)

### Server beenden

Drücke `Ctrl+C` im Terminal

---

## 4️⃣ Auf GitHub Pages deployen

### Schritt 1: Repository pushen

```bash
# Status prüfen
git status

# Änderungen stagen
git add _events/
git add _config.yml  # Falls angepasst

# Committen
git commit -m "Add first event: Mein Event"

# Pushen
git push origin main
```

### Schritt 2: GitHub Pages aktivieren

1. Gehe zu: **https://github.com/USERNAME/krawl.foundation/settings/pages**
2. **Source**: Wähle "GitHub Actions" (NICHT "Deploy from branch")
3. Speichern

### Schritt 3: Warten

- GitHub Actions Workflow startet automatisch
- Check Status: **Actions**-Tab im Repository
- Build dauert ~2-3 Minuten

### Schritt 4: Website öffnen

Deine Website ist live unter:

```
https://USERNAME.github.io/krawl.foundation/
```

---

## 🎯 Nächste Schritte

### Anpassen

1. **Projekt-Info** editieren: `_config.yml`
   ```yaml
   title: "Meine Events"
   description: "Event-Plattform für ..."
   ```

2. **Theme ändern**: `_config.yml`
   ```yaml
   theme:
     active: "default"  # oder "dark", "minimal"
   ```

3. **About-Seite** erstellen: `about.md`

### Mehr Events hinzufügen

```bash
# Neues Event
touch _events/$(date +%Y-%m-%d)-neues-event.md

# Commit & Push
git add _events/
git commit -m "Add event: Neues Event"
git push
```

### Features aktivieren

In `_config.yml`:

```yaml
features:
  bookmarks: true   # Merkliste
  search: true      # Suche
  filters: true     # Filter
  rss: true         # RSS-Feed
```

---

## 🐛 Troubleshooting

### Jekyll baut nicht

```bash
# Check Ruby/Bundler
bundle install

# Verbose-Output
bundle exec jekyll build --verbose
```

### Port 4000 belegt

```bash
# Anderen Port nutzen
bundle exec jekyll serve --port 4001
```

### GitHub Pages deployed nicht

1. Check Actions-Tab für Fehler
2. Prüfe: Settings > Pages > Source = "GitHub Actions"
3. Force Re-Deploy:
   ```bash
   git commit --allow-empty -m "Trigger rebuild"
   git push
   ```

---

## 📚 Weitere Ressourcen

- **[Datenmodell](02-DATA_MODEL.md)** - Alle Event-Felder
- **[Architektur](03-ARCHITECTURE.md)** - Wie Jekyll funktioniert
- **[Debugging](04-DEBUGGING.md)** - Fehlersuche

---

**Fragen?** → [GitHub Discussions](https://github.com/feileberlin/krawl.foundation/discussions)
