# Secrets Management

## Übersicht

krawl.foundation nutzt **lokale `.env` Dateien** + **GitHub Secrets** für sensible Credentials.

## 🔐 Secrets-Architektur

### Lokale Development
```
.env                    # Lokale Secrets (git-ignored)
  ↓
scripts/telegram_bot.py  # Liest .env via python-dotenv
cli/image_extractor.py   # Liest .env für API-Zugriff
```

### GitHub Actions
```
GitHub Secrets          # Verschlüsselt in Repository Settings
  ↓
.github/workflows/*.yml # Zugriff via ${{ secrets.NAME }}
```

## 🚀 Quick Setup

### Option A: Interaktives Script (Empfohlen)

```bash
./scripts/setup_secrets.sh
```

**Features:**
- ✅ Erkennt existierende `.env` automatisch
- ✅ Zeigt maskierte Token-Vorschau
- ✅ Fragt bei jedem Token: "Neu setzen? (y/N)"
- ✅ Merged alte + neue Werte (nur geänderte überschreiben)
- ✅ Optionaler Sync zu GitHub Secrets via `gh` CLI
- ✅ Automatisches Backup (`.env.backup`)
- ✅ Sichere Permissions (`chmod 600`)

### Option B: Manuelle .env Erstellung

```bash
# 1. Template kopieren
cp .env.example .env

# 2. Secrets ausfüllen
nano .env

# 3. Permissions sichern
chmod 600 .env
```

## 📋 Benötigte Secrets

### TELEGRAM_TOKEN
**Wozu:** Telegram Bot API-Zugriff  
**Wo holen:** [@BotFather](https://t.me/BotFather) → `/newbot`  
**Format:** `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`  
**Benötigt für:**
- `scripts/telegram_bot.py`
- `.github/workflows/telegram-flyer.yml`

```bash
# Erstellen:
# 1. Öffne @BotFather in Telegram
# 2. Sende: /newbot
# 3. Folge Anweisungen
# 4. Kopiere Token
```

### GITHUB_TOKEN
**Wozu:** Repository Dispatch, GitHub API  
**Wo holen:** [GitHub Settings → Developer Settings → Personal Access Tokens](https://github.com/settings/tokens)  
**Format:** `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`  
**Permissions:** `repo`, `workflow`  
**Benötigt für:**
- `scripts/telegram_bot.py` (Repository Dispatch)
- GitHub Actions (Auto-Commit, Issues, etc.)

```bash
# Erstellen:
# 1. GitHub → Settings → Developer Settings
# 2. Personal Access Tokens → Tokens (classic)
# 3. Generate new token
# 4. Scopes: [x] repo, [x] workflow
# 5. Generate token → Kopieren
```

### EMAIL_PASSWORD (Optional)
**Wozu:** Email-Benachrichtigungen für neue Events  
**Wo holen:** Gmail App-Passwort, Outlook App-Passwort  
**Format:** `abcd efgh ijkl mnop`  
**Benötigt für:**
- Email-Notifications (falls aktiviert)

```bash
# Gmail App-Passwort erstellen:
# 1. Google Account → Sicherheit
# 2. 2-Faktor-Authentifizierung aktivieren
# 3. App-Passwörter → Neue App → Name: krawl
# 4. Passwort generieren → Kopieren
```

### ONEDRIVE_CLIENT_ID / ONEDRIVE_CLIENT_SECRET (Optional)
**Wozu:** Backup von Events zu OneDrive  
**Wo holen:** [Azure Portal](https://portal.azure.com) → App Registrations  
**Benötigt für:**
- Optional: Automatische Backups

## 🔄 Sync: Lokal ↔ GitHub Secrets

### Lokal → GitHub (via gh CLI)

```bash
# Alle Secrets syncen
./scripts/setup_secrets.sh
# Wähle: "Möchtest du die Secrets zu GitHub Secrets synchronisieren? (y/N): y"

# Oder manuell einzeln
gh secret set TELEGRAM_TOKEN < <(grep TELEGRAM_TOKEN .env | cut -d= -f2)
gh secret set GITHUB_TOKEN < <(grep GITHUB_TOKEN .env | cut -d= -f2)
```

### GitHub → Lokal (manuell)

```bash
# GitHub Secrets NICHT automatisch lesbar (Security!)
# Nur manuell über GitHub UI → Settings → Secrets
```

## 🛡️ Security Best Practices

### 1. Nie in Git committen!
```bash
# .gitignore bereits konfiguriert:
.env
.env.*
.env.backup
```

### 2. Restricted Permissions
```bash
chmod 600 .env     # Nur Owner kann lesen/schreiben
chmod 700 scripts/ # Scripts nur für Owner ausführbar
```

### 3. Token Rotation
```bash
# Tokens regelmäßig neu generieren (alle 6-12 Monate)
./scripts/setup_secrets.sh  # Alte Tokens überschreiben
```

### 4. Separate Tokens für Dev/Prod
```bash
# Development
.env              # Lokaler Bot, Test-Repo

# Production
GitHub Secrets    # Production Bot, Live-Repo
```

## 🔍 Secrets prüfen

### Lokal
```bash
# Maskierte Anzeige
grep -o '^[^=]*' .env | while read key; do
  value=$(grep "^${key}=" .env | cut -d= -f2)
  echo "$key=${value:0:4}...${value: -4}"
done

# Oder via Script
./scripts/setup_secrets.sh
# Wähle: "Möchtest du die Secrets neu konfigurieren? (y/N): N"
```

### GitHub
```bash
# Liste aller Secrets
gh secret list

# Einzelnes Secret (nur Metadaten, nicht Wert!)
gh secret view TELEGRAM_TOKEN
```

## 🚨 Secret Leaks vermeiden

### 1. Pre-Commit Hook
```bash
# .git/hooks/pre-commit
#!/bin/bash
if git diff --cached --name-only | grep -q '^.env$'; then
  echo "❌ FEHLER: .env darf nicht committed werden!"
  exit 1
fi
```

### 2. GitHub Secret Scanning
- Automatisch aktiviert für Public Repos
- Warnt bei versehentlich committeten Tokens

### 3. .env-Beispiel nutzen
```bash
# Niemals echte Tokens in .env.example!
# Nur Platzhalter
TELEGRAM_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
```

## 🔄 Token Widerruf / Kompromittierung

### Telegram Token kompromittiert
```bash
# 1. Neuen Token generieren
# @BotFather → /token

# 2. Alten Token widerrufen
# @BotFather → /revoke

# 3. Neuen Token setzen
./scripts/setup_secrets.sh
# TELEGRAM_TOKEN neu eingeben
```

### GitHub Token kompromittiert
```bash
# 1. Token löschen
# GitHub → Settings → Developer Settings → Tokens → Delete

# 2. Neuen Token generieren
# Generate new token

# 3. Secrets aktualisieren
./scripts/setup_secrets.sh
gh secret set GITHUB_TOKEN
```

## 📝 Beispiel .env

```bash
# krawl.foundation Secrets
# Generiert am 2025-11-22 15:30:00
# NIEMALS in Git committen!

TELEGRAM_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
EMAIL_PASSWORD=abcd efgh ijkl mnop

# Optional: OneDrive Integration
ONEDRIVE_CLIENT_ID=12345678-1234-1234-1234-123456789abc
ONEDRIVE_CLIENT_SECRET=ABC~1234567890abcdefghijklmnopqrst
```

## 🔗 Links

- **Setup-Script:** `scripts/setup_secrets.sh`
- **Template:** `.env.example`
- **GitHub Tokens:** https://github.com/settings/tokens
- **Telegram BotFather:** https://t.me/BotFather
- **gh CLI:** https://cli.github.com/
