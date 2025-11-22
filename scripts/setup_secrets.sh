#!/bin/bash

# Smart Secrets Management Script für krawl.foundation
# Setzt Secrets nur dann neu, wenn ausdrücklich erwünscht

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"
ENV_EXAMPLE="$PROJECT_ROOT/.env.example"
ENV_BACKUP="$PROJECT_ROOT/.env.backup"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔐 krawl.foundation Secrets Management${NC}"
echo "================================================"
echo ""

# Check if .env exists
if [ -f "$ENV_FILE" ]; then
    echo -e "${YELLOW}⚠️  .env Datei existiert bereits${NC}"
    echo ""
    
    # Show masked preview of existing tokens
    echo "Aktuelle Secrets (maskiert):"
    while IFS='=' read -r key value; do
        # Skip comments and empty lines
        [[ "$key" =~ ^#.*$ ]] || [[ -z "$key" ]] && continue
        
        # Mask the value (show first 4 and last 4 chars)
        if [ ${#value} -gt 12 ]; then
            masked="${value:0:4}...${value: -4}"
        else
            masked="***"
        fi
        echo "  $key=$masked"
    done < "$ENV_FILE"
    echo ""
    
    read -p "Möchtest du die Secrets neu konfigurieren? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${GREEN}✅ Behalte bestehende .env Datei${NC}"
        echo ""
        
        # Ask about GitHub Secrets sync
        if command -v gh &> /dev/null; then
            read -p "Möchtest du die lokalen Secrets zu GitHub Secrets synchronisieren? (y/N): " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                sync_to_github_secrets
            fi
        fi
        exit 0
    fi
    
    # Backup existing .env
    echo -e "${YELLOW}Erstelle Backup: .env.backup${NC}"
    cp "$ENV_FILE" "$ENV_BACKUP"
fi

# Load existing values if available
declare -A EXISTING_SECRETS
if [ -f "$ENV_FILE" ]; then
    while IFS='=' read -r key value; do
        [[ "$key" =~ ^#.*$ ]] || [[ -z "$key" ]] && continue
        EXISTING_SECRETS[$key]=$value
    done < "$ENV_FILE"
fi

# Function to prompt for secret with optional existing value
prompt_secret() {
    local key=$1
    local description=$2
    local example=$3
    
    echo ""
    echo -e "${GREEN}$key${NC}"
    echo "$description"
    echo -e "${YELLOW}Beispiel: $example${NC}"
    
    # Show existing value if available
    if [ -n "${EXISTING_SECRETS[$key]}" ]; then
        local existing="${EXISTING_SECRETS[$key]}"
        if [ ${#existing} -gt 12 ]; then
            local masked="${existing:0:4}...${existing: -4}"
        else
            local masked="***"
        fi
        echo -e "Aktueller Wert: $masked"
        read -p "Neu setzen? (y/N): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "$key=${EXISTING_SECRETS[$key]}"
            return
        fi
    fi
    
    read -p "Wert eingeben: " -r value
    
    # Use existing value if empty input
    if [ -z "$value" ] && [ -n "${EXISTING_SECRETS[$key]}" ]; then
        value="${EXISTING_SECRETS[$key]}"
        echo -e "${YELLOW}Verwende bestehenden Wert${NC}"
    fi
    
    echo "$key=$value"
}

# Function to sync secrets to GitHub
sync_to_github_secrets() {
    echo ""
    echo -e "${GREEN}🔄 Synchronisiere zu GitHub Secrets...${NC}"
    
    if ! command -v gh &> /dev/null; then
        echo -e "${RED}❌ gh CLI nicht installiert. Überspringe GitHub Sync.${NC}"
        return
    fi
    
    # Check if authenticated
    if ! gh auth status &> /dev/null; then
        echo -e "${RED}❌ Nicht bei GitHub authentifiziert. Führe 'gh auth login' aus.${NC}"
        return
    fi
    
    local synced=0
    local failed=0
    
    while IFS='=' read -r key value; do
        [[ "$key" =~ ^#.*$ ]] || [[ -z "$key" ]] && continue
        
        echo -n "  Setze $key... "
        if echo "$value" | gh secret set "$key" 2>/dev/null; then
            echo -e "${GREEN}✓${NC}"
            ((synced++))
        else
            echo -e "${RED}✗${NC}"
            ((failed++))
        fi
    done < "$ENV_FILE"
    
    echo ""
    echo -e "${GREEN}✅ $synced Secrets synchronisiert${NC}"
    [ $failed -gt 0 ] && echo -e "${RED}❌ $failed Secrets fehlgeschlagen${NC}"
}

# Create new .env file
echo ""
echo "Konfiguriere Secrets..."
echo "======================"

{
    echo "# krawl.foundation Secrets"
    echo "# Generiert am $(date '+%Y-%m-%d %H:%M:%S')"
    echo "# NIEMALS in Git committen!"
    echo ""
    
    prompt_secret "TELEGRAM_TOKEN" \
        "Bot-Token von @BotFather" \
        "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
    
    echo ""
    
    prompt_secret "GITHUB_TOKEN" \
        "Personal Access Token mit 'repo' und 'workflow' Rechten" \
        "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    
    echo ""
    
    prompt_secret "EMAIL_PASSWORD" \
        "App-Passwort für Event-Email-Benachrichtigungen (optional)" \
        "abcd efgh ijkl mnop"
    
    echo ""
    echo "# Optional: OneDrive Integration für Backup"
    
    prompt_secret "ONEDRIVE_CLIENT_ID" \
        "Azure App Client ID (optional)" \
        "12345678-1234-1234-1234-123456789abc"
    
    echo ""
    
    prompt_secret "ONEDRIVE_CLIENT_SECRET" \
        "Azure App Client Secret (optional)" \
        "ABC~1234567890abcdefghijklmnopqrst"
    
} > "$ENV_FILE"

# Secure permissions
chmod 600 "$ENV_FILE"

echo ""
echo -e "${GREEN}✅ .env Datei erstellt und gesichert (chmod 600)${NC}"

# Ask about GitHub Secrets sync
if command -v gh &> /dev/null; then
    echo ""
    read -p "Möchtest du die Secrets zu GitHub Secrets synchronisieren? (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sync_to_github_secrets
    fi
else
    echo ""
    echo -e "${YELLOW}💡 Tipp: Installiere gh CLI für automatischen Sync zu GitHub Secrets${NC}"
    echo "   https://cli.github.com/"
fi

echo ""
echo -e "${GREEN}🎉 Setup abgeschlossen!${NC}"
echo ""
echo "Nächste Schritte:"
echo "  1. Telegram Bot starten: python scripts/telegram_bot.py"
echo "  2. GitHub Actions konfigurieren: .github/workflows/telegram-flyer.yml"
echo "  3. Bot-Link teilen: https://t.me/YOUR_BOT_NAME"
