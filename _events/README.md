# 📅 Events Collection

Dieser Ordner enthält alle **Event-Markdown-Dateien**.

## 📂 Was gehört hier rein?

- Jedes Event = 1 Markdown-Datei (`.md`)
- Dateiname: `YYYY-MM-DD-event-titel.md`
- Wird von Jekyll in HTML umgewandelt

## 📝 Event-Format (Frontmatter)

Jede Event-Datei beginnt mit **Frontmatter** (YAML zwischen `---`):

```yaml
---
layout: event              # Pflicht: Layout-Template
title: "Event-Titel"       # Pflicht: Angezeigter Titel
date: 2025-11-21 20:00     # Pflicht: Start-Datum/Zeit (YYYY-MM-DD HH:MM)
end_date: 2025-11-21 23:00 # Optional: End-Zeit
published: true            # Pflicht: false = Entwurf, true = veröffentlicht

# Kategorisierung
categories:                # Tags/Kategorien (mehrere möglich)
  - konzert
  - live-musik

# Ort
location:                  # Optional: Freier Text
  name: "Kulturzentrum"
  address: "Musterstraße 42, 12345 Stadt"
  city: "Berlin"

coordinates:               # Optional: GPS (für Karte)
  lat: 52.5200
  lng: 13.4050

# Veranstalter
organizer: "Veranstalter Name"  # Optional
contact: "info@example.com"     # Optional

# Links
url: "https://example.com"      # Optional: Event-Website
ticket_url: "https://tickets.example.com"  # Optional: Ticket-Link

# Preise
price: "10€"                    # Optional: Freier Text
price_reduced: "5€"             # Optional: Ermäßigt

# Metadaten
featured: false                 # Optional: Hervorgehoben auf Startseite
sold_out: false                 # Optional: Ausverkauft
cancelled: false                # Optional: Abgesagt

# Quelle (für Scraping)
source: "manual"                # manual, scraped, api
source_url: ""                  # URL der Original-Quelle
---

Hier kommt die **Event-Beschreibung** in Markdown.

## Programm

- 20:00 Einlass
- 21:00 Band 1
- 22:00 Hauptact

## Über die Künstler

Beschreibung...
```

## 📋 Beispiel: Minimales Event

Datei: `_events/2025-12-01-konzert-im-club.md`

```yaml
---
layout: event
title: "Konzert im Club"
date: 2025-12-01 21:00
published: true
categories:
  - konzert
location:
  name: "Club Berlin"
  address: "Hauptstraße 1, 10115 Berlin"
price: "15€"
---

Tolle Band spielt ihre größten Hits!
```

## 🔍 Dateistruktur-Konventionen

### Dateiname

```
YYYY-MM-DD-kurzbeschreibung.md

Beispiele:
✅ 2025-11-21-jazz-night.md
✅ 2025-12-24-weihnachtskonzert.md
❌ jazz-night.md (fehlt Datum)
❌ 2025-11-21 jazz night.md (Leerzeichen)
```

### Kategorien

Einheitliche Kategorien nutzen (Kleinbuchstaben, Bindestriche):

```yaml
# ✅ Gut
categories:
  - konzert
  - live-musik
  - elektronisch

# ❌ Vermeiden
categories:
  - Konzert       # Großbuchstaben
  - Live Musik    # Leerzeichen
```

## 🎯 Status-Workflow

1. **Entwurf**: `published: false`
   - Event wird lokal angezeigt (mit `show_drafts: true`)
   - NICHT auf GitHub Pages veröffentlicht

2. **Veröffentlicht**: `published: true`
   - Event ist live auf der Website

3. **Abgesagt**: `cancelled: true`
   - Event wird durchgestrichen angezeigt

4. **Ausverkauft**: `sold_out: true`
   - Badge "Ausverkauft" wird angezeigt

## 🔄 Event erstellen (manuell)

```bash
# 1. Neue Datei erstellen
touch _events/$(date +%Y-%m-%d)-mein-event.md

# 2. Frontmatter einfügen (siehe oben)

# 3. Lokal testen
./scripts/dev.sh

# 4. Auf http://localhost:4000 prüfen

# 5. Committen & Pushen
git add _events/
git commit -m "Add event: Mein Event"
git push
```

## 🤖 Automatisierung (später)

In Phase 3 kommt:
- **Event-Scraper** (Python): Lädt Events von Websites
- **Event-Generator** (Python): Erstellt Test-Events
- **Validierung** (Python): Prüft Frontmatter-Format

## 📚 Weitere Infos

- **[Datenmodell](../docs/02-DATA_MODEL.md)** - Alle Felder erklärt
- **[Jekyll Collections](https://jekyllrb.com/docs/collections/)** - Offizielle Docs
- **[YAML Syntax](https://yaml.org/spec/1.2/spec.html)** - Frontmatter-Format

## ❓ Häufige Fragen

**Q: Warum Markdown statt Datenbank?**  
A: Git-Versionierung, einfache Bearbeitung, keine Server nötig.

**Q: Wie lösche ich ein Event?**  
A: Datei löschen oder `published: false` setzen.

**Q: Können Events mehrere Termine haben?**  
A: Ja, siehe [Recurring Events](../docs/08-RECURRING_EVENTS.md) (v2.0+)

---

**Stand:** November 2025 | [Zurück zur Hauptdokumentation](../README.md)
