# ============================================================================
# Ruby Dependencies für Jekyll
# ============================================================================
# Diese Datei definiert alle Ruby-Gems (Pakete), die das Projekt benötigt.
# 
# Installation: bundle install
# Update: bundle update
# Dokumentation: https://bundler.io/
# ============================================================================

source "https://rubygems.org"

# ----------------------------------------------------------------------------
# JEKYLL (Core)
# ----------------------------------------------------------------------------
# Jekyll ist der Static Site Generator

gem "jekyll", "~> 4.3"  # Version 4.3.x (stabil)

# ----------------------------------------------------------------------------
# JEKYLL PLUGINS
# ----------------------------------------------------------------------------
# Diese Plugins sind von GitHub Pages offiziell unterstützt:
# https://pages.github.com/versions/

group :jekyll_plugins do
  gem "jekyll-feed", "~> 0.17"       # RSS Feed Generator
  gem "jekyll-sitemap", "~> 1.4"     # Sitemap.xml
  gem "jekyll-seo-tag", "~> 2.8"     # SEO Meta-Tags
end

# ----------------------------------------------------------------------------
# DEVELOPMENT TOOLS (nur lokal)
# ----------------------------------------------------------------------------
# Diese Gems sind NUR für lokale Entwicklung nötig

group :development do
  gem "webrick", "~> 1.8"            # HTTP Server (Ruby >= 3.0 benötigt das)
  
  # Optional: Schnellere Builds
  # gem "jekyll-watch", "~> 2.2"     # File-Watcher
  # gem "listen", "~> 3.8"           # Für Live-Reload
end

# ----------------------------------------------------------------------------
# PLATFORM-SPEZIFISCH
# ----------------------------------------------------------------------------

# Windows-Support (automatisch geladen auf Windows)
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

# macOS File-Watching Performance
gem "wdm", "~> 0.1", :platforms => [:mingw, :x64_mingw, :mswin]

# ----------------------------------------------------------------------------
# LOCK RUBY VERSION (optional)
# ----------------------------------------------------------------------------
# Erzwingt eine bestimmte Ruby-Version (verhindert Kompatibilitätsprobleme)

# ruby "~> 3.2.0"  # Auskommentiert = beliebige Version >= 3.0
