# 🤝 Contributing Guide

Danke für dein Interesse an **krawl.foundation**!

Dieses Projekt ist ausdrücklich **anfängerfreundlich**. Keine Sorge, wenn du noch nie zu Open Source beigetragen hast - wir helfen dir!

---

## 💡 Wie kann ich helfen?

### 1. 🐛 Bugs melden

Hast du einen Fehler gefunden?

1. **Prüfe**: Existiert schon ein [Issue](https://github.com/feileberlin/krawl.foundation/issues)?
2. **Erstelle Issue**: Mit Template "Bug Report"
3. **Beschreibe**:
   - Was hast du gemacht?
   - Was sollte passieren?
   - Was ist stattdessen passiert?
   - Fehlermeldungen (Screenshots helfen!)

### 2. 💡 Features vorschlagen

Idee für ein neues Feature?

1. **Diskussion**: Erstelle [GitHub Discussion](https://github.com/feileberlin/krawl.foundation/discussions)
2. **Beschreibe**:
   - Problem, das gelöst werden soll
   - Deine Lösungsidee
   - Alternativen, die du erwogen hast

### 3. 📝 Dokumentation verbessern

- Tippfehler gefunden?
- Unklare Erklärung?
- Fehlende Beispiele?

→ Pull Request mit Verbesserung!

### 4. 🧪 Testen

- Teste Setup auf deinem System
- Probiere neue Features aus
- Gib Feedback in Discussions

### 5. 💻 Code beitragen

Siehe [Code-Beiträge](#code-beiträge) unten.

---

## 🔧 Development Setup

```bash
# 1. Fork auf GitHub
#    → Klick "Fork" oben rechts

# 2. Clone deinen Fork
git clone https://github.com/DEIN-USERNAME/krawl.foundation.git
cd krawl.foundation

# 3. Upstream hinzufügen
git remote add upstream https://github.com/feileberlin/krawl.foundation.git

# 4. Setup
./scripts/setup.sh

# 5. Branch erstellen
git checkout -b feature/mein-feature
```

---

## 💻 Code-Beiträge

### Workflow

1. **Issue erstellen** (falls noch nicht vorhanden)
2. **Branch erstellen**: `feature/xyz` oder `fix/abc`
3. **Code schreiben** (siehe [Code-Style](#code-style))
4. **Testen** (siehe [Tests](#tests))
5. **Committen** (siehe [Commit-Messages](#commit-messages))
6. **Pull Request** öffnen

### Branch-Namen

```bash
# Features
feature/bookmark-system
feature/search-filter

# Bugfixes
fix/broken-date-parsing
fix/mobile-layout

# Dokumentation
docs/add-api-reference
docs/improve-readme

# Refactoring
refactor/split-css-files
```

### Code-Style

#### Python

```python
# PEP 8 Style Guide
# https://pep8.org/

# Docstrings für Funktionen
def validate_event(event_data):
    """
    Validiert Event-Frontmatter.
    
    Args:
        event_data (dict): Event-Daten aus YAML
    
    Returns:
        bool: True wenn valid, False sonst
    
    Raises:
        ValueError: Bei fehlenden Pflichtfeldern
    """
    pass

# Type Hints (Python 3.9+)
def parse_date(date_str: str) -> datetime:
    pass
```

#### JavaScript

```javascript
// ES6+ Syntax
// JSDoc-Kommentare für Funktionen

/**
 * Filtert Events nach Kategorie.
 * 
 * @param {Array} events - Liste aller Events
 * @param {string} category - Kategorie (z.B. "konzert")
 * @returns {Array} Gefilterte Events
 */
function filterByCategory(events, category) {
    return events.filter(e => e.categories.includes(category));
}

// Moderne Features nutzen
const filteredEvents = events
    .filter(e => e.published)
    .map(e => ({ ...e, formatted_date: formatDate(e.date) }));
```

#### CSS

```css
/* BEM-ähnliche Naming Convention */
.event-card { }
.event-card__title { }
.event-card__meta { }
.event-card--featured { }

/* CSS Custom Properties
:root {
    --color-primary: #667eea;
}

/* Kommentare für Sektionen */
/* ============================================================================
   SECTION NAME
   ============================================================================ */
```

#### YAML

```yaml
# Konsistente Einrückung (2 Spaces)
# Kommentare für nicht-offensichtliche Werte

# Event-Frontmatter
layout: event
title: "Event-Titel"
date: 2025-12-01 20:00    # Format: YYYY-MM-DD HH:MM
published: true           # false = Entwurf
```

### Tests

```bash
# Python-Tests (später)
pytest tests/

# JavaScript-Tests (später)
npm test

# Jekyll-Build testen
bundle exec jekyll build

# Link-Check (später)
./scripts/check-links.sh
```

### Commit-Messages

```bash
# Format: <type>(<scope>): <subject>

# Types:
feat      # Neues Feature
fix       # Bugfix
docs      # Dokumentation
style     # Formatierung (keine Code-Änderung)
refactor  # Code-Refactoring
test      # Tests hinzufügen/ändern
chore     # Build, Dependencies, etc.

# Beispiele:
git commit -m "feat(events): Add bookmark system"
git commit -m "fix(layout): Mobile navigation overflow"
git commit -m "docs: Add federation architecture guide"
git commit -m "refactor(css): Split main.css into modules"

# Multi-Line (für komplexere Commits)
git commit -m "feat(search): Add full-text search

- Implement Lunr.js integration
- Add search UI component
- Update documentation

Closes #42"
```

---

## 📋 Pull Request Checklist

Bevor du einen PR öffnest:

- [ ] Branch ist aktuell mit `main`
- [ ] Code folgt Style-Guide
- [ ] Neue Features sind dokumentiert
- [ ] Jekyll-Build läuft ohne Fehler
- [ ] Commit-Messages sind klar
- [ ] PR-Beschreibung erklärt Änderungen

---

## 🎯 Prioritäten

Aktuell besonders hilfreich:

1. **Dokumentation**: Unklare Stellen verbessern
2. **Testing**: Setup auf verschiedenen OS testen
3. **Accessibility**: A11y-Verbesserungen
4. **Performance**: Optimierungen vorschlagen

---

## 📚 Ressourcen

### Jekyll

- [Jekyll Docs](https://jekyllrb.com/docs/)
- [Liquid Template Language](https://shopify.github.io/liquid/)

### Git & GitHub

- [GitHub Docs](https://docs.github.com/)
- [Git Cheat Sheet](https://training.github.com/downloads/github-git-cheat-sheet/)

### Code Style

- [PEP 8 (Python)](https://pep8.org/)
- [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)

---

## ❓ Fragen?

- **[GitHub Discussions](https://github.com/feileberlin/krawl.foundation/discussions)** - Allgemeine Fragen
- **[Issues](https://github.com/feileberlin/krawl.foundation/issues)** - Bugs & Features

---

**Danke für deinen Beitrag!** 💙
