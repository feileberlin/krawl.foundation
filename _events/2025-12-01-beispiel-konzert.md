---
# ============================================================================
# BEISPIEL-EVENT - Vollständig dokumentiert
# ============================================================================
# Dieses Event zeigt ALLE verfügbaren Frontmatter-Felder.
# Kopiere diese Datei für neue Events.
#
# Dateiname-Format: YYYY-MM-DD-event-titel.md
# ============================================================================

layout: event              # Pflicht: Layout-Template
title: "Konzert im Kulturzentrum"
date: 2025-12-01 20:00     # Pflicht: Start (YYYY-MM-DD HH:MM)
end_date: 2025-12-01 23:30 # Optional: End-Zeit
published: true            # Pflicht: false = Entwurf, true = Live

# ----------------------------------------------------------------------------
# KATEGORISIERUNG
# ----------------------------------------------------------------------------
categories:                # Optional: Tags (mehrere möglich)
  - konzert
  - live-musik
  - indie-rock

# ----------------------------------------------------------------------------
# LOCATION (Ort)
# ----------------------------------------------------------------------------
location:
  name: "Kulturzentrum Berlin"
  address: "Kulturstraße 42"
  city: "Berlin"
  postal_code: "10115"

# GPS-Koordinaten (für Karte)
coordinates:
  lat: 52.5200
  lng: 13.4050

# ----------------------------------------------------------------------------
# VERANSTALTER & KONTAKT
# ----------------------------------------------------------------------------
organizer: "Kulturverein Berlin e.V."
contact: "info@kulturzentrum-berlin.de"
phone: "+49 30 12345678"

# ----------------------------------------------------------------------------
# LINKS
# ----------------------------------------------------------------------------
url: "https://kulturzentrum-berlin.de/events/konzert-2025-12-01"
ticket_url: "https://tickets.example.com/event/12345"
facebook_event: "https://facebook.com/events/12345"

# ----------------------------------------------------------------------------
# PREISE
# ----------------------------------------------------------------------------
price: "15€"               # Freier Text
price_reduced: "10€"       # Ermäßigt (Studenten, etc.)
price_note: "VVK: 12€"     # Zusätzliche Info

# ----------------------------------------------------------------------------
# STATUS & FLAGS
# ----------------------------------------------------------------------------
featured: true             # Hervorgehoben auf Startseite
sold_out: false            # Ausverkauft?
cancelled: false           # Abgesagt?
age_restriction: "18+"     # Altersbeschränkung (optional)

# ----------------------------------------------------------------------------
# METADATEN (Scraping, Import)
# ----------------------------------------------------------------------------
source: "manual"           # manual, scraped, api, ical
source_url: ""             # Original-URL (bei Scraping)
import_date: 2025-11-21    # Wann importiert? (optional)

# ----------------------------------------------------------------------------
# BILD (später, Phase 3)
# ----------------------------------------------------------------------------
# image: "/assets/images/events/2025-12-01-konzert.jpg"
# image_alt: "Band auf der Bühne"

---

<!-- ============================================================================
     EVENT BESCHREIBUNG (Markdown)
     ============================================================================
     Alles nach den --- wird als Event-Content angezeigt.
     Du kannst Markdown-Formatierung nutzen.
============================================================================ -->

Die Indie-Rock-Band **The Example Band** kommt nach Berlin!

Erlebt eine unvergessliche Nacht mit den besten Hits der letzten Jahre und brandneuen Songs aus dem kommenden Album "Future Sounds".

## 🎵 Line-Up

- **20:00** - Einlass & Warm-Up DJ
- **21:00** - Support Act: Local Heroes
- **22:00** - The Example Band (Main Act)
- **23:30** - Ende

## 🎤 Über die Band

The Example Band wurde 2018 gegründet und hat sich schnell einen Namen in der Indie-Szene gemacht. Ihr Debütalbum "First Steps" erreichte Platz 5 in den deutschen Indie-Charts.

### Bandmitglieder

- Alex Müller - Vocals, Gitarre
- Sarah Schmidt - Bass
- Tom Wagner - Drums

## 🎫 Tickets

- **Online**: [tickets.example.com](https://tickets.example.com/event/12345)
- **VVK**: 12€ (bis 30.11.)
- **Abendkasse**: 15€
- **Ermäßigt**: 10€ (Schüler, Studenten, Rentner)

> ⚠️ **Hinweis**: Tickets sind streng limitiert. Vorverkauf wird empfohlen!

## 📍 Anfahrt

**Kulturzentrum Berlin**  
Kulturstraße 42  
10115 Berlin

**Öffentliche Verkehrsmittel:**
- U-Bahn: U6 bis Naturkundemuseum (5 Min. Fußweg)
- S-Bahn: S1, S2, S25 bis Nordbahnhof (7 Min. Fußweg)
- Bus: 120, 142, 245

**Parken:**  
Parkhaus Kulturplatz (2 Min. Fußweg)

## ℹ️ Wichtige Infos

- Einlass ab 18 Jahren
- Garderobe vorhanden (1€)
- Bargeldlose Zahlung möglich
- Rauchen nur im Außenbereich

## 📸 Fotos & Social Media

Teile deine Erlebnisse mit:
- Instagram: [@kulturzentrum_berlin](https://instagram.com/kulturzentrum_berlin)
- Facebook: [Kulturzentrum Berlin](https://facebook.com/kulturzentrum)
- Hashtag: #ExampleBandBerlin

---

**Veranstalter:** Kulturverein Berlin e.V.  
**Kontakt:** info@kulturzentrum-berlin.de  
**Telefon:** +49 30 12345678
