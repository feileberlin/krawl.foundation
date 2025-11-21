#!/usr/bin/env bash
# ============================================================================
# DEVELOPMENT SERVER - krawl.foundation
# ============================================================================
# Startet Jekyll Development-Server mit Live-Reload.
#
# Usage:
#   ./scripts/dev.sh [--no-live-reload]
#
# Features:
#   - Automatischer Rebuild bei Änderungen
#   - Live-Reload im Browser
#   - Zeigt Drafts (published: false)
#   - Zeigt zukünftige Events
# ============================================================================

set -e

# Farben
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Parse Arguments
LIVE_RELOAD=true
if [[ "${1:-}" == "--no-live-reload" ]]; then
    LIVE_RELOAD=false
fi

# ============================================================================
# MAIN
# ============================================================================

echo ""
echo "🚀 Starte Development-Server..."
echo ""

# Check if Jekyll is installed
if ! command -v jekyll >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Jekyll nicht gefunden. Führe Setup aus:${NC}"
    echo "   ./scripts/setup.sh"
    exit 1
fi

# Build options
BUILD_OPTS=(
    "--incremental"      # Nur geänderte Dateien
    "--drafts"           # Zeige Entwürfe
    "--future"           # Zeige zukünftige Posts
)

if [ "$LIVE_RELOAD" = true ]; then
    BUILD_OPTS+=("--livereload")
fi

echo -e "${BLUE}ℹ️  Server-URL:${NC} http://localhost:4000"
echo -e "${BLUE}ℹ️  Beenden:${NC} Ctrl+C"
echo ""

# Start Jekyll
bundle exec jekyll serve "${BUILD_OPTS[@]}"
