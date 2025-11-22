# Telegram Event Submissions

## Übersicht

krawl.foundation bietet einen **automatisierten Telegram Bot** für einfache Event-Einreichungen via Flyer-Upload.

## 🚀 Quick Start für User

1. **Bot öffnen:** [t.me/krawlfoundation_bot](https://t.me/krawlfoundation_bot) *(Link nach Bot-Setup anpassen)*
2. **Flyer hochladen:** Sende ein Foto vom Event-Flyer
3. **Bestätigung erhalten:** Der Bot bestätigt den Upload
4. **Automatische Verarbeitung:** OCR extrahiert Event-Daten
5. **Review durch Team:** Draft wird geprüft und veröffentlicht

## 📸 Was passiert mit dem Flyer?

### User-Perspektive
```
1. User sendet Foto
   ↓
2. Bot: "📸 Erhalten! Verarbeite..."
   ↓
3. Bot: "✅ Hochgeladen! Du wirst benachrichtigt."
   ↓
4. [Automatische Verarbeitung im Hintergrund]
   ↓
5. Event erscheint auf krawl.foundation
   ↓
6. Optional: User bekommt Benachrichtigung
```

### Technischer Flow
```
1. Telegram Bot empfängt Photo
   ↓
2. Bot cached Foto lokal (.cache/telegram/)
   ↓
3. Bot triggert GitHub Actions (Repository Dispatch)
   ↓
4. GitHub Actions Workflow startet:
   - Download Telegram-Foto
   - OCR-Texterkennung (Tesseract)
   - Event-Daten extrahieren
   - Draft-JSON erstellen
   - Commit zu main branch
   ↓
5. Draft Alerts Workflow triggern
   ↓
6. Moderator reviewed Draft
   ↓
7. Status: draft → reviewed → published
   ↓
8. Jekyll baut Site neu → Event live
```

## 🤖 Bot-Setup (für Admins)

### 1. Telegram Bot erstellen

```bash
# 1. Öffne @BotFather in Telegram
# 2. Sende: /newbot
# 3. Folge Anweisungen (Name, Username)
# 4. Erhalte Token: 123456:ABC-DEF1234ghIkl...

# 5. Konfiguriere Bot
/setdescription - Event-Flyer hochladen für krawl.foundation
/setabouttext - Automatischer Event-Upload Bot
/setuserpic - Logo hochladen
```

### 2. Secrets konfigurieren

```bash
# Lokale Secrets setzen
./scripts/setup_secrets.sh

# Oder manuell .env erstellen
cat > .env << EOF
TELEGRAM_TOKEN=123456:ABC-DEF1234ghIkl...
GITHUB_TOKEN=ghp_...
GITHUB_REPO=feileberlin/krawl.foundation
EOF

chmod 600 .env
```

### 3. Bot starten

```bash
# Option A: Lokal (Development)
python3 scripts/telegram_bot.py

# Option B: Systemd Service (Production)
sudo cp scripts/telegram_bot.service /etc/systemd/system/
sudo systemctl enable telegram_bot
sudo systemctl start telegram_bot
sudo systemctl status telegram_bot

# Option C: Docker
docker build -t krawl-telegram-bot .
docker run -d --env-file .env krawl-telegram-bot

# Option D: Screen Session (Quick & Dirty)
screen -S telegram-bot
python3 scripts/telegram_bot.py
# Ctrl+A, D to detach
```

## 🔐 Sicherheit & Datenschutz

### Datenspeicherung
- **Telegram User ID:** Wird in Draft gespeichert (nur für Moderation)
- **Telegram Username:** Optional gespeichert
- **Foto:** Lokal gecached in `.cache/telegram/` (automatisch gelöscht nach 30 Tagen)
- **OCR-Text:** Im Event-Draft gespeichert

### DSGVO-konform
- Keine dauerhafte Speicherung von Telegram-Userdaten
- User-ID nur temporär für Draft-Zuordnung
- Fotos werden nicht öffentlich veröffentlicht (nur OCR-Text)
- User kann Löschung anfragen: `krawl@feileberlin.de`

## 🛠️ Troubleshooting

### Bot antwortet nicht
```bash
# Check bot status
ps aux | grep telegram_bot

# Check logs
tail -f /var/log/telegram_bot.log

# Restart bot
systemctl restart telegram_bot
```

### GitHub Actions schlagen fehl
```bash
# Check Repository Dispatch permissions
# Settings → Secrets → GITHUB_TOKEN muss 'workflow' Permission haben

# Test Repository Dispatch manuell
gh api repos/feileberlin/krawl.foundation/dispatches \
  -f event_type=telegram_flyer_submission \
  -f client_payload[test]=true
```

### OCR erkennt nichts
- **Problem:** Foto zu unscharf, zu klein, oder schlechte Beleuchtung
- **Lösung:** User bitten, besseres Foto zu senden
- **Tipp:** In Bot-Message Hinweise geben:
  - "Gute Beleuchtung verwenden"
  - "Flyer komplett im Bild"
  - "Nicht zu weit weg fotografieren"

## 📊 Monitoring

### Statistiken anzeigen
```bash
# Anzahl Telegram-Submissions
ls .cache/telegram/ | wc -l

# Drafts von Telegram
jq 'select(.source == "telegram")' _events/*.json | jq -s 'length'

# Letzte 10 Submissions
ls -lt .cache/telegram/ | head -10
```

### Alerts konfigurieren
```yaml
# .github/workflows/notify-pending-drafts.yml
schedule:
  - cron: '0 */6 * * *'  # Alle 6 Stunden prüfen
```

## 🚫 Rate Limiting

Um Spam zu vermeiden:

```python
# In scripts/telegram_bot.py erweitern:
from collections import defaultdict
from datetime import datetime, timedelta

user_uploads = defaultdict(list)
MAX_UPLOADS_PER_HOUR = 5

def check_rate_limit(user_id):
    now = datetime.now()
    hour_ago = now - timedelta(hours=1)
    
    # Clean old uploads
    user_uploads[user_id] = [
        ts for ts in user_uploads[user_id] 
        if ts > hour_ago
    ]
    
    if len(user_uploads[user_id]) >= MAX_UPLOADS_PER_HOUR:
        return False  # Rate limit exceeded
    
    user_uploads[user_id].append(now)
    return True
```

## 📝 Bot-Nachrichten anpassen

Editiere `scripts/telegram_bot.py`:

```python
# /start Message
await update.message.reply_text(
    "👋 Willkommen bei krawl.foundation!\n\n"
    "📸 Sende mir ein Flyer-Foto..."
)

# Erfolgs-Message
await update.message.reply_text(
    "✅ Flyer hochgeladen!\n\n"
    "🤖 Dein Event wird jetzt verarbeitet..."
)
```

## 🔗 Links

- **Bot Code:** `scripts/telegram_bot.py`
- **Workflow:** `.github/workflows/telegram-flyer.yml`
- **OCR Engine:** `cli/image_extractor.py`
- **Secrets Setup:** `scripts/setup_secrets.sh`
- **Telegram Bot API:** https://core.telegram.org/bots/api

---

## 🎤 Voice Message Submissions

### User Flow
```
User → 🎤 Sprachnachricht senden
    ↓
Bot → "Transkribiere..."
    ↓
GitHub Actions → VOSK Spracherkennung
    ↓
Draft JSON mit Transkription
```

### Example Voice Input
"Hallo, ich möchte ein Event eintragen. Konzert am einunddreißigsten Dezember zweitausendfünfundzwanzig um zwanzig Uhr im SO36 Berlin. Eintritt kostet fünfzehn Euro."

### Transcription Result
```json
{
  "_comment": "# Transcription: konzert am 31.12.2025 um 20 uhr im so36 berlin eintritt 15 euro",
  "message_type": "voice",
  "transcription": "konzert am 31.12.2025 um 20 uhr im so36 berlin eintritt 15 euro",
  "needs_review": true
}
```

### VOSK Setup (GitHub Actions)
```yaml
- name: Download VOSK model
  run: |
    wget https://alphacephei.com/vosk/models/vosk-model-small-de-0.15.zip
    unzip -d ~/.cache/vosk/model-de
```

**Models:**
- German: `vosk-model-small-de-0.15` (45 MB)
- English: `vosk-model-small-en-us-0.15` (40 MB)
- Multilingual: `vosk-model-small-multi-0.15` (50 MB)

---

## 💬 Text Message Submissions

### User Flow
```
User → 💬 "Konzert am 31.12. im SO36, 20 Uhr"
    ↓
Bot → "Draft erstellen..."
    ↓
GitHub Actions → Direkt zu Draft (kein OCR/VOSK)
    ↓
Draft JSON mit Original-Text
```

### Example Text Input
```
Party @ Berghain
1. Januar 2026, 23:00
Techno Night mit DJ XYZ
Eintritt: 20€
```

### Draft Result
```json
{
  "_comment": "# Original message: Party @ Berghain, 1. Januar 2026...",
  "message_type": "text",
  "original_text": "Party @ Berghain\n1. Januar 2026, 23:00...",
  "needs_review": true
}
```

---

## 🔄 Processing Comparison

| Input Type | Processing | Duration | Accuracy |
|------------|-----------|----------|----------|
| 📸 Photo | OCR (Tesseract) | ~30s | 70-90% |
| 🎤 Voice | VOSK Transcription | ~20s | 80-95% |
| 💬 Text | Direct | ~5s | 100% |

### Best Practices

**For Users:**
- 📸 **Photo:** Sharp image, good lighting, text visible
- 🎤 **Voice:** Clear speech, mention date/time/venue
- 💬 **Text:** Structured format (date, venue, title, etc.)

**For Moderators:**
All submissions create drafts with `needs_review: true`
- Check `_comment` field for original input
- Verify extracted data (date, venue, title)
- Correct any OCR/transcription errors
- Set `status: published` when ready

