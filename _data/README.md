# 📊 Data Directory

Dieser Ordner enthält **strukturierte Daten** in CSV/YAML-Format.

## 📂 Was gehört hier rein?

- **CSV-Dateien**: Tabellarische Daten (editierbar in Excel/LibreOffice)
- **YAML-Dateien**: Konfigurationsdaten
- **JSON-Dateien**: API-Responses, komplexe Strukturen (optional)

## 🎯 Warum nicht in _config.yml?

- `_config.yml`: Globale Jekyll-Einstellungen
- `_data/`: Domain-spezifische Daten (Venues, Sources, etc.)

## 📋 Geplante Dateien

### venues.csv

Liste aller Veranstaltungsorte (für Autocomplete, Icons):

```csv
id,name,address,city,lat,lng,icon,website
club-berlin,Club Berlin,"Hauptstraße 1",Berlin,52.5200,13.4050,music,https://club-berlin.de
kulturzentrum,Kulturzentrum,"Kulturweg 5",Berlin,52.5100,13.4100,theater,https://kultur.example
```

**Felder:**
- `id`: Eindeutige ID (für Referenzierung)
- `name`: Anzeigename
- `address`: Straße + Hausnummer
- `city`: Stadt
- `lat`, `lng`: GPS-Koordinaten (Dezimalgrad)
- `icon`: Icon-Typ (music, theater, cinema, festival, ...)
- `website`: URL (optional)

### sources.csv

Event-Scraping-Quellen (für Automation):

```csv
id,name,url,type,selector,enabled
facebook-events,Facebook Events,https://facebook.com/events,facebook,#events,true
website-scraper,Venue Website,https://example.com/events,html,.event-item,false
```

**Felder:**
- `id`: Eindeutige ID
- `name`: Anzeigename
- `url`: Start-URL für Scraping
- `type`: Scraper-Typ (facebook, html, ical, json)
- `selector`: CSS-Selector oder API-Endpoint
- `enabled`: Aktiv? (true/false)

### categories.yml

Event-Kategorien mit Icons & Farben:

```yaml
konzert:
  label: "Konzert"
  icon: "🎵"
  color: "#FF6B6B"
  
theater:
  label: "Theater"
  icon: "🎭"
  color: "#4ECDC4"
  
kino:
  label: "Kino"
  icon: "🎬"
  color: "#95E1D3"
```

## 🔍 Zugriff in Liquid-Templates

```liquid
{% for venue in site.data.venues %}
  <option value="{{ venue.id }}">{{ venue.name }}</option>
{% endfor %}

{% assign category_info = site.data.categories[event.categories[0]] %}
<span style="color: {{ category_info.color }}">
  {{ category_info.icon }} {{ category_info.label }}
</span>
```

## 📊 CSV vs. YAML vs. JSON

| Format | Vorteile | Nachteile | Verwendung |
|--------|----------|-----------|------------|
| **CSV** | Excel-editierbar, kompakt | Keine Hierarchien | Flache Listen (Venues, Sources) |
| **YAML** | Hierarchien, lesbar | Syntax-sensitiv | Konfigurationen (Categories) |
| **JSON** | Standardformat, APIs | Weniger lesbar | API-Responses, komplexe Daten |

## 🎯 Best Practices

### CSV-Dateien

```csv
# ✅ Gut: Konsistente Spalten, keine Leerzeilen
id,name,city
1,Club Berlin,Berlin
2,Kulturhaus,München

# ❌ Schlecht: Inkonsistente Struktur
id,name
1,Club Berlin,Berlin  # Extra-Spalte
2,Kulturhaus          # Fehlende Spalte
```

### YAML-Dateien

```yaml
# ✅ Gut: Konsistente Einrückung (2 Spaces)
categories:
  konzert:
    label: "Konzert"
    icon: "🎵"

# ❌ Schlecht: Tabs, inkonsistent
categories:
	konzert:
	  label: "Konzert"
```

## 🔧 Tools

### CSV bearbeiten

- **Excel / LibreOffice Calc**: Tabellenansicht
- **VS Code**: CSV-Erweiterung (z.B. Rainbow CSV)
- **Python**: `pandas` für komplexe Bearbeitungen

### YAML validieren

```bash
# Online: https://yamllint.com

# Python
python -c "import yaml; yaml.safe_load(open('_data/categories.yml'))"
```

## 🚀 Kommende Features (Phase 2+)

- **organizers.csv**: Veranstalter-CRM
- **locations.csv**: GPS-Locations für Karte
- **filters.yml**: Dynamische Filter-Konfiguration
- **federation.yml**: ActivityPub-Konfiguration (v2.0)

## 📚 Weitere Infos

- **[Datenmodell](../docs/02-DATA_MODEL.md)** - Vollständige Schemas
- **[Jekyll Data Files](https://jekyllrb.com/docs/datafiles/)** - Offizielle Docs
- **[CSV Spec](https://tools.ietf.org/html/rfc4180)** - RFC 4180

---

**Stand:** November 2025 | [Zurück zur Hauptdokumentation](../README.md)
