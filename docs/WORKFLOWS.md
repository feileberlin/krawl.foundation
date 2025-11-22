# GitHub Actions Workflows

## Übersicht

krawl.foundation nutzt **4 Haupt-Workflows** für Automation:

| Workflow | Trigger | Zweck | Intervall |
|----------|---------|-------|-----------|
| **deploy.yml** | Push to main | Jekyll Build & GitHub Pages Deploy | On push |
| **scrape-events.yml** | Schedule | Instagram/Facebook Scraping | 3am & 3pm UTC |
| **telegram-flyer.yml** | Repository Dispatch | Telegram Flyer Processing | On upload |
| **notify-pending-drafts.yml** | Schedule + Workflow Call | Draft Alert Issues | Every 6 hours |

## 📋 Workflow Details

### 1. deploy.yml - Site Deployment
**Pfad:** `.github/workflows/deploy.yml`  
**Trigger:** Push to `main` branch, Manual  
**Dauer:** ~2-3 Minuten

**Was passiert:**
1. Checkout Repository
2. Setup Ruby + Install Jekyll
3. Build Jekyll Site (`_site/`)
4. Upload Artifact
5. Deploy to GitHub Pages

**Manueller Trigger:**
```bash
gh workflow run deploy.yml
```

**Überwachung:**
```bash
gh run list --workflow=deploy.yml
gh run view <run-id>
```

---

### 2. scrape-events.yml - Event Bot
**Pfad:** `.github/workflows/scrape-events.yml`  
**Trigger:** Schedule (3am & 3pm UTC), Manual  
**Dauer:** ~5-10 Minuten

**Was passiert:**
1. Setup Python + Dependencies
2. Run Tests (`pytest`)
3. Scrape Instagram (@punkinhof)
4. Scrape Facebook (GaleriehausHof)
5. Set Events to `draft` status
6. Commit neue Events
7. Trigger `notify-pending-drafts.yml`

**Schedule:**
```yaml
schedule:
  - cron: '0 3,15 * * *'  # 03:00 & 15:00 UTC (4/5am & 4/5pm Berlin)
```

**Manueller Trigger:**
```bash
# Mit Test-Events
gh workflow run scrape-events.yml -f event_count=5

# Mit Custom URL
gh workflow run scrape-events.yml -f source_url=https://example.com/events
```

**Dependencies:**
- `instaloader` - Instagram Scraping
- `requests` - HTTP Requests
- `pytesseract` - OCR (falls aktiviert)

**Output:**
- Neue JSON-Dateien in `_events/`
- Status: `"status": "draft"`
- Commit: `🤖 Auto-scrape: New draft events`

---

### 3. telegram-flyer.yml - Telegram Processing
**Pfad:** `.github/workflows/telegram-flyer.yml`  
**Trigger:** Repository Dispatch (event_type: `telegram_flyer_submission`)  
**Dauer:** ~1-2 Minuten

**Was passiert:**
1. Setup Python + Tesseract OCR
2. Download Telegram Photo via Bot API
3. Run OCR (`image_extractor.py batch mode`)
4. Parse Event-Daten (Datum, Venue, Titel)
5. Create Event Draft JSON
6. Commit Draft to `_events/`
7. Trigger `notify-pending-drafts.yml`

**Trigger via Bot:**
```python
# In scripts/telegram_bot.py
requests.post(
    f"https://api.github.com/repos/{REPO}/dispatches",
    json={
        "event_type": "telegram_flyer_submission",
        "client_payload": {
            "telegram_user_id": user.id,
            "file_id": photo.file_id,
            "filename": "flyer_123_20251122.jpg"
        }
    },
    headers={"Authorization": f"Bearer {GITHUB_TOKEN}"}
)
```

**Output:**
- `_events/telegram-draft-YYYYMMDD_HHMMSS.json`
- `.cache/telegram/flyer_*.jpg`
- Commit: `📸 New event draft from Telegram`

---

### 4. notify-pending-drafts.yml - Draft Alerts
**Pfad:** `.github/workflows/notify-pending-drafts.yml`  
**Trigger:** Schedule (every 6h), Workflow Call, Manual  
**Dauer:** ~30 Sekunden

**Was passiert:**
1. Scan `_events/*.json` für `status: draft`
2. Check `created_at` timestamp
3. Filter Drafts älter als Threshold (default: 6 Stunden)
4. Close alte Alert-Issues
5. Create neue GitHub Issue mit Draft-Liste

**Schedule:**
```yaml
schedule:
  - cron: '0 */6 * * *'  # Alle 6 Stunden
```

**Manueller Trigger:**
```bash
# Default threshold (6h)
gh workflow run notify-pending-drafts.yml

# Custom threshold (12h)
gh workflow run notify-pending-drafts.yml -f threshold_hours=12
```

**Output:**
- GitHub Issue mit Label `draft-pending`
- Enthält: Titel, Venue, Datum, Alter, Filename
- Auto-Assignee: Repository Owner

**Issue-Beispiel:**
```markdown
## ⚠️ 3 Draft Events Pending

### 🎫 Konzert im Galeriehaus
- Venue: Galeriehaus Hof
- Date: 2025-12-15
- File: `2025-12-15-konzert-galeriehaus.json`
- Age: **8 hours** ⏰

[...]

## Actions
```bash
./cli/event_scraper.py bulk --set-field status reviewed
```
```

---

## 🔄 Workflow-Abhängigkeiten

```
Push to main
    ↓
deploy.yml ────────────────────→ Site deployed

Schedule (3am/3pm)
    ↓
scrape-events.yml
    ↓
    ├─ Instagram/Facebook scraping
    ├─ Create drafts
    ├─ Commit
    └─ Trigger ──→ notify-pending-drafts.yml
                        ↓
                        Create Issue

Telegram Upload
    ↓
telegram_bot.py ─→ Repository Dispatch
                        ↓
                  telegram-flyer.yml
                        ↓
                        ├─ Download photo
                        ├─ OCR
                        ├─ Create draft
                        ├─ Commit
                        └─ Trigger ──→ notify-pending-drafts.yml

Schedule (every 6h)
    ↓
notify-pending-drafts.yml
    ↓
    Check old drafts → Create Issue
```

## 🛠️ Workflow-Management

### Alle Workflows auflisten
```bash
gh workflow list
```

### Workflow-Runs anzeigen
```bash
gh run list --workflow=scrape-events.yml --limit 10
```

### Workflow manuell starten
```bash
gh workflow run <workflow-name>
```

### Workflow deaktivieren
```bash
gh workflow disable <workflow-name>
```

### Logs anzeigen
```bash
gh run view <run-id> --log
```

## 🚨 Troubleshooting

### Workflow schlägt fehl
```bash
# 1. Logs prüfen
gh run view --log

# 2. Workflow re-run
gh run rerun <run-id>

# 3. Failed Jobs anzeigen
gh run view <run-id> --log-failed
```

### Secrets fehlen
```bash
# GitHub Secrets prüfen
gh secret list

# Secret setzen
gh secret set TELEGRAM_TOKEN
```

### Workflow nicht getriggert
```bash
# Cron-Schedule prüfen
# Online-Tool: https://crontab.guru/

# Manuell triggern
gh workflow run <workflow-name>
```

## 📊 Monitoring

### Workflow-Status Dashboard
```bash
gh run list --limit 20
```

### Success Rate
```bash
gh run list --workflow=deploy.yml --limit 100 \
  | grep -c "completed success"
```

### Letzte Failures
```bash
gh run list --status=failure --limit 10
```

## 🔐 Permissions

Workflows benötigen folgende Permissions:

```yaml
permissions:
  contents: write     # Commit, Push
  issues: write       # Create/Close Issues
  workflows: write    # Trigger andere Workflows
```

## 🔗 Links

- **Workflows:** `.github/workflows/`
- **GitHub Actions Docs:** https://docs.github.com/en/actions
- **Cron Schedule Tester:** https://crontab.guru/
- **Repository Dispatch:** https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event
