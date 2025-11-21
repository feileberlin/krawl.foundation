#!/bin/bash
# =============================================================================
# Setup Script für krawl.foundation - Event Scraper CLI
# =============================================================================

set -e  # Exit on error

echo "🚀 Setting up krawl.foundation..."
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Found: Python $python_version"

if ! python3 -c 'import sys; assert sys.version_info >= (3, 8)' 2>/dev/null; then
    echo "❌ Error: Python 3.8 or higher required"
    exit 1
fi
echo "   ✓ Python version OK"
echo ""

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "🔨 Creating virtual environment..."
    python3 -m venv venv
    echo "   ✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "   ✓ Activated"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip > /dev/null
echo "   ✓ pip upgraded"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt
echo "   ✓ Dependencies installed"
echo ""

# Create necessary directories
echo "📁 Creating directory structure..."
mkdir -p _events
mkdir -p _data
mkdir -p tests/fixtures
mkdir -p .github/workflows
echo "   ✓ Directories created"
echo ""

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x scripts/*.sh
chmod +x cli/event_scraper.py
echo "   ✓ Scripts are executable"
echo ""

# Run tests
echo "🧪 Running tests..."
if pytest tests/ -v; then
    echo "   ✓ All tests passed"
else
    echo "   ⚠️  Some tests failed (non-critical for setup)"
fi
echo ""

# Success
echo "✅ Setup complete!"
echo ""
echo "📚 Next steps:"
echo "   1. Activate virtual environment: source venv/bin/activate"
echo "   2. Run CLI help: ./cli/event_scraper.py"
echo "   3. Generate test events: ./cli/event_scraper.py generate -n 5"
echo "   4. Read documentation: cat cli/README.md"
echo ""
echo "🎉 Happy scraping!"
