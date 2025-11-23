# 📝 KRaWL> Foundation – Redaktions-Dokumentation

Hey! 👋 Du bist Teil des Redaktionsteams oder verwaltest die Events? Perfekt! Hier erfährst du alles, was du brauchst, um Events zu verwalten, zu moderieren und die Plattform am Laufen zu halten.

## 🎯 Deine Rolle

Als Redakteur:in oder Admin bist du verantwortlich für:
- ✅ Event-Drafts reviewen und freigeben
- 🔍 Qualitätskontrolle der Event-Daten
- 📸 Telegram-Submissions prüfen
- 🗂️ Events organisieren und kategorisieren
- 🚀 Veröffentlichung steuern

## 🚀 Quick Start

### Web-Interface (Coming Soon)

Aktuell gibt es noch kein Web-Interface – aber keine Panik! Die CLI-Tools sind super einfach zu bedienen.

### CLI-Tools nutzen

```bash
# Terminal öffnen und zum Projekt navigieren
cd krawl.foundation

# Virtual Environment aktivieren (nur beim ersten Mal pro Session)
source venv/bin/activate

# Fertig! Jetzt kannst du Events verwalten
```

## 📋 Event-Workflow

### Status-Übersicht

Jedes Event durchläuft drei Phasen:

1. **Draft** (`status: "draft"`): Neu erstellt, noch nicht geprüft
2. **Reviewed** (`status: "reviewed"`): Redaktionell geprüft, aber noch nicht live
3. **Published** (`status: "published"`): Live auf der Website

```
📸 Upload/Scraping → 📝 Draft → 👀 Reviewed → 🚀 Published
```

### 1. Neue Drafts anzeigen

```bash
# Alle Events mit Status "draft" auflisten
./cli/event_scraper.py list | grep draft

# Oder: JSON-Format für mehr Details
./cli/event_scraper.py list --format json | jq 'select(.status == "draft")'
```

**Du erhältst automatisch GitHub Issues**, wenn Drafts länger als 6 Stunden warten!

### 2. Event prüfen

Öffne die Event-Datei mit deinem Lieblings-Editor:

```bash
# Mit Visual Studio Code
code _events/2025-12-15-konzert-example.json

# Oder mit Nano (Terminal-Editor)
nano _events/2025-12-15-konzert-example.json
```

**Was überprüfen?**
- ✅ Datum & Uhrzeit korrekt?
- ✅ Venue-Name richtig geschrieben?
- ✅ Adresse vollständig?
- ✅ Titel aussagekräftig?
- ✅ Beschreibung lesbar (kein OCR-Nonsense)?
- ✅ Kategorien passend?

### 3. Event korrigieren (optional)

Wenn OCR oder Auto-Extraction Fehler gemacht hat:

```json
{
  "title": "Konzert im Galeriehaus",
  "date": "2025-12-15T20:00:00",
  "venue": "Galeriehaus Hof",
  "address": "Hofstraße 1, 12345 Berlin",
  "description": "Live-Musik mit Band XYZ",
  "price": "10€",
  "status": "draft"
}
```

Speichern und fertig! ✨

### 4. Event freigeben

**Einzelnes Event:**

```bash
# Event auf "reviewed" setzen
# (Ändere "draft" zu "reviewed" in der Datei)
nano _events/2025-12-15-konzert-example.json

# Oder direkt auf "published" setzen
# (Ändere "draft" zu "published")
```

**Alle Events auf einmal:**

```bash
# Erst testen: Was würde passieren?
./cli/event_scraper.py bulk --set-field status reviewed --dry-run

# Tatsächlich ausführen
./cli/event_scraper.py bulk --set-field status reviewed
```

### 5. Events veröffentlichen

```bash
# Alle reviewed Events auf published setzen
./cli/event_scraper.py bulk --set-field status published

# (Optional: Erst Dry-Run)
./cli/event_scraper.py bulk --set-field status published --dry-run
```

**Wichtig:** Nach dem Commit wird die Website automatisch aktualisiert! 🚀

```bash
git add _events/
git commit -m "Publish events batch $(date +%Y-%m-%d)"
git push
```

## 📸 Telegram-Submissions

### Wie funktioniert's?

1. User sendet Flyer-Foto an Telegram Bot
2. Bot speichert Foto und startet OCR
3. System erstellt automatisch Event-Draft
4. **Du** bekommst Benachrichtigung (GitHub Issue)
5. **Du** prüfst und korrigierst den Draft
6. **Du** gibst Event frei

### OCR-Qualität

**Gut erkannt:**
- ✅ Datum & Uhrzeit
- ✅ Venue-Namen (meistens)
- ✅ Preise

**Oft fehlerhaft:**
- ⚠️ Lange Beschreibungstexte
- ⚠️ Social Media Handles
- ⚠️ Telefonnummern

💡 **Tipp:** Schau dir immer das Original-Foto an: `.cache/telegram/flyer_*.jpg`

### Telegram-Drafts finden

```bash
# Alle Telegram-Drafts
ls _events/telegram-draft-*.json

# Mit Details
./cli/event_scraper.py list | grep telegram-draft
```

## 🔍 Events suchen & filtern

### Nach Status filtern

```bash
# Alle Draft-Events
./cli/event_scraper.py list --format json | jq 'select(.status == "draft")'

# Alle Published-Events
./cli/event_scraper.py list --format json | jq 'select(.status == "published")'
```

### Nach Datum filtern

```bash
# Events ab heute
./cli/event_scraper.py list --format json | jq 'select(.date >= "2025-11-23")'

# Events im Dezember 2025
./cli/event_scraper.py list --format json | jq 'select(.date | startswith("2025-12"))'
```

### Nach Venue filtern

```bash
# Alle Events im "Galeriehaus Hof"
./cli/event_scraper.py list --format json | jq 'select(.venue == "Galeriehaus Hof")'
```

💡 **Tipp:** `jq` ist ein JSON-Filter-Tool. Wenn nicht installiert: `sudo apt install jq`

## 🗂️ Event-Organisation

### Kategorien

Events sollten passende Kategorien haben:

- `konzert` - Live-Musik, Bands, DJs
- `party` - Clubnächte, Tanzveranstaltungen
- `ausstellung` - Kunst, Galerien
- `festival` - Mehrtägige Events
- `workshop` - Lern-Events
- `lesung` - Literatur, Poetry
- `theater` - Theater, Performance
- `kino` - Filmvorführungen

**Kategorien hinzufügen:**

```json
{
  "categories": ["konzert", "live-musik"]
}
```

### Pflichtfelder

Diese Felder **müssen** ausgefüllt sein:

- ✅ `title` - Event-Titel
- ✅ `date` - Start-Datum & Uhrzeit
- ✅ `venue` - Venue-Name
- ✅ `status` - draft/reviewed/published

**Optional aber empfohlen:**

- `address` - Vollständige Adresse
- `city` - Stadt (Standard: Berlin)
- `description` - Was passiert?
- `price` - Eintritt (z.B. "10€", "Kostenlos", "VVK 15€/AK 20€")
- `url` - Website oder Ticket-Link
- `image` - Flyer-URL

## 🚀 Bulk-Operationen

### Alle Events auf einmal bearbeiten

**Achtung:** Immer erst mit `--dry-run` testen!

```bash
# Beispiel 1: Alle Drafts auf Reviewed setzen
./cli/event_scraper.py bulk --set-field status reviewed --dry-run
./cli/event_scraper.py bulk --set-field status reviewed

# Beispiel 2: Venue-Name korrigieren (für alle Events)
# (Besser: Manuell in einzelnen Dateien ändern)

# Beispiel 3: Alte Events archivieren
# (Filtert nach Datum, dann Status ändern)
```

### Backup vor Bulk-Ops

**Immer ein Backup machen!**

```bash
# Backup erstellen
cp -r _events _events.backup.$(date +%Y%m%d-%H%M%S)

# Später wiederherstellen (falls nötig)
rm -rf _events
mv _events.backup.20251123-143000 _events
```

Oder einfach Git nutzen:

```bash
git add _events/
git commit -m "Before bulk operation"
# ... Bulk-Op durchführen ...
# Falls etwas schief geht:
git reset --hard HEAD
```

## 📊 Dashboard & Statistiken

### Events zählen

```bash
# Anzahl aller Events
ls _events/*.json | wc -l

# Anzahl Draft-Events
grep -l '"status": "draft"' _events/*.json | wc -l

# Anzahl Published-Events
grep -l '"status": "published"' _events/*.json | wc -l
```

### Übersicht

```bash
# Alle Events auflisten (Tabelle)
./cli/event_scraper.py list

# Mit mehr Details
./cli/event_scraper.py list --format json | jq '.'
```

### Dashboard (Web)

Öffne `dashboard.html` im Browser:

```bash
# Lokal
open dashboard.html  # macOS
xdg-open dashboard.html  # Linux

# Oder auf Live-Website
# https://feileberlin.github.io/krawl.foundation/dashboard.html
```

## 🔔 Benachrichtigungen

### GitHub Issues für alte Drafts

Das System erstellt automatisch Issues, wenn Drafts zu lange warten:

- **Intervall:** Alle 6 Stunden
- **Threshold:** Drafts älter als 6 Stunden
- **Label:** `draft-pending`

**Issue enthält:**
- Anzahl wartender Drafts
- Titel, Venue, Datum jedes Events
- Alter (z.B. "8 hours")
- Dateiname für schnellen Zugriff

**Was tun?**
1. Issue öffnen
2. Events prüfen
3. Events freigeben
4. Issue schließen (automatisch beim nächsten Run)

### Eigene Benachrichtigungen

**GitHub Watch aktivieren:**
1. Repository öffnen
2. "Watch" → "All Activity"
3. Du bekommst Emails bei neuen Issues

**Oder:** Telegram-Bot konfigurieren für direktes Feedback an User

## 🛠️ Troubleshooting

### "Event wird nicht auf Website angezeigt"

**Checkliste:**
- ✅ Status auf `"published"` gesetzt?
- ✅ Datum in der Zukunft? (Vergangene Events werden evtl. versteckt)
- ✅ Datei committed und gepusht?
- ✅ GitHub Actions erfolgreich? (Check Actions-Tab)

```bash
# Status prüfen
jq '.status' _events/dein-event.json

# Datum prüfen
jq '.date' _events/dein-event.json

# Git Status
git status

# Pushen falls nötig
git add _events/dein-event.json
git commit -m "Publish event: Dein Event"
git push
```

### "OCR hat Nonsense erkannt"

**Lösung:** Manuell korrigieren

```bash
# Datei öffnen
nano _events/telegram-draft-*.json

# Felder korrigieren
# Speichern: Ctrl+O, Enter, Ctrl+X
```

**OCR verbessern:**
- User bitten, bessere Fotos zu machen (scharf, gut ausgeleuchtet)
- Tesseract-Sprache konfigurieren (in `cli/image_extractor.py`)

### "Bulk-Operation lief schief"

**Rollback mit Git:**

```bash
# Letzten Commit rückgängig machen
git reset --hard HEAD~1

# Oder: Spezifischen Commit wiederherstellen
git log --oneline  # Commit-ID finden
git reset --hard <commit-id>
```

**Oder: Aus Backup wiederherstellen:**

```bash
rm -rf _events
mv _events.backup.20251123-143000 _events
```

## 📚 Cheat Sheet

### Häufigste Befehle

```bash
# Virtual Environment aktivieren
source venv/bin/activate

# Drafts anzeigen
./cli/event_scraper.py list | grep draft

# Alle Drafts auf Reviewed setzen
./cli/event_scraper.py bulk --set-field status reviewed

# Alle Reviewed Events auf Published setzen
./cli/event_scraper.py bulk --set-field status published

# Änderungen speichern
git add _events/
git commit -m "Review and publish events"
git push
```

### Nützliche Git-Commands

```bash
# Was wurde geändert?
git status
git diff _events/

# Änderungen committen
git add _events/
git commit -m "Update events"

# Hochladen
git push

# Rückgängig machen (vor Push)
git reset --hard HEAD
```

## 🎓 Tipps & Best Practices

### 1. Regelmäßig checken

- ⏰ Mindestens 2x täglich Drafts prüfen
- 📧 GitHub-Benachrichtigungen aktivieren
- 🔔 Telegram-Bot für sofortige Alerts nutzen

### 2. Qualität vor Quantität

- ✅ Lieber ein Event gründlich prüfen als zehn schnell durchwinken
- 🔍 OCR-Fehler korrigieren (verbessert Nutzererlebnis)
- 📝 Beschreibungen lesbar machen

### 3. Konsistente Formatierung

- 📅 Datum immer: `YYYY-MM-DDTHH:MM:SS`
- 💶 Preis einheitlich: "10€", "Kostenlos", "VVK 15€ / AK 20€"
- 🏛️ Venue-Namen konsistent (nicht mal "SO36", mal "SO 36", mal "so36")

### 4. Backups

- 💾 Vor Bulk-Ops immer Backup erstellen
- 📦 Regelmäßig kompletten `_events/` Ordner sichern
- ☁️ Git ist dein Freund – regelmäßig committen!

## 📞 Hilfe & Support

**Probleme?**
- 📖 Diese Doku nochmal durchlesen
- 🐛 Issue auf GitHub öffnen: https://github.com/feileberlin/krawl.foundation/issues
- 💬 Im Team nachfragen

**Feature-Wünsche?**
- Schreib sie auf! Wir sammeln Feedback.

---

**Happy Reviewing! 🎉**

*Letzte Aktualisierung: November 2025*
