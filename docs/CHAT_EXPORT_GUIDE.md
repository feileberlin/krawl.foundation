# 💬 Chat-Verlauf Exportieren & Archivieren

Guide für das Speichern des gesamten GitHub Copilot Chat-Verlaufs.

## 🎯 Warum Chat exportieren?

- 📚 **Nachschlagewerk** für Entscheidungen und Diskussionen
- 📄 **Dokumentation** des Entwicklungsprozesses
- 🔍 **Durchsuchbar** als PDF/A
- 💾 **Archivierung** für langfristige Aufbewahrung

---

## 🚀 Quick Start

### Methode 1: VS Code Export (Empfohlen)

```bash
# 1. In VS Code Copilot Chat:
#    - Rechtsklick im Chat → "Export Chat"
#    - Speichern als: copilot-chat-2025-11-21.md

# 2. Konvertieren zu PDF/A
python scripts/export_chat.py copilot-chat-2025-11-21.md \
  -o docs/sessions/session-2025-11-21.pdf \
  --title "krawl.foundation Development Session" \
  --author "feileberlin" \
  --date "2025-11-21"

# 3. Fertig! PDF ist archiviert.
```

### Methode 2: Clipboard Export

```bash
# 1. In Chat: Ctrl+A → Ctrl+C (alles kopieren)

# 2. Export from clipboard
python scripts/export_chat.py --from-clipboard \
  -o docs/sessions/chat-$(date +%Y-%m-%d).pdf \
  --title "Development Session"

# 3. Fertig!
```

---

## 📦 Installation

```bash
# Dependencies installieren
pip install markdown reportlab pypdf beautifulsoup4 lxml pyperclip

# Oder via requirements.txt (wenn vorhanden)
pip install -r requirements-export.txt
```

---

## 🛠️ Usage

### Basic

```bash
# Markdown → PDF
python scripts/export_chat.py chat.md

# Output: chat-history.pdf
```

### Mit Optionen

```bash
python scripts/export_chat.py input.md \
  --output archive/session-001.pdf \
  --title "Feature Implementation Session" \
  --author "feileberlin" \
  --date "2025-11-21" \
  --format pdfa
```

### Verschiedene Formate

```bash
# PDF/A (archival, empfohlen)
python scripts/export_chat.py chat.md --format pdfa

# Standard PDF
python scripts/export_chat.py chat.md --format pdf

# HTML (web-lesbar)
python scripts/export_chat.py chat.md --format html

# Markdown (unverändert)
python scripts/export_chat.py chat.md --format markdown
```

---

## 📁 Empfohlene Struktur

```
docs/
├── sessions/
│   ├── 2025-11-21-initial-setup.pdf
│   ├── 2025-11-22-scraper-implementation.pdf
│   ├── 2025-11-23-dashboard-creation.pdf
│   └── README.md
├── decisions/
│   ├── architecture.md
│   ├── tech-stack.md
│   └── roadmap.md
└── CHAT_EXPORT_GUIDE.md
```

**Naming Convention:**
```
YYYY-MM-DD-kurze-beschreibung.pdf
```

**Beispiele:**
- `2025-11-21-initial-setup.pdf`
- `2025-11-22-instagram-scraper.pdf`
- `2025-12-01-feature-discussion.pdf`

---

## 🔄 Automatisierung

### Daily Export Script

```bash
#!/bin/bash
# scripts/daily_export.sh

DATE=$(date +%Y-%m-%d)
OUTPUT="docs/sessions/session-$DATE.pdf"

# Aus Clipboard (nach manuellem Copy)
python scripts/export_chat.py --from-clipboard \
  -o "$OUTPUT" \
  --title "Development Session $DATE" \
  --author "feileberlin" \
  --date "$DATE"

# Git commit
git add "$OUTPUT"
git commit -m "docs: Chat export $DATE"
git push
```

### Git Hook (bei jedem Push)

```bash
# .git/hooks/pre-push

#!/bin/bash
echo "💬 Export Chat History? [y/N]"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    DATE=$(date +%Y-%m-%d-%H%M)
    python scripts/export_chat.py --from-clipboard \
      -o "docs/sessions/auto-$DATE.pdf" \
      --title "Auto Export $DATE"
    
    git add docs/sessions/
    git commit --amend --no-edit
fi
```

---

## 📊 PDF/A Format

**Was ist PDF/A?**
- **Archival Format** - standardisiert für Langzeitarchivierung
- **Self-contained** - alle Fonts/Ressourcen eingebettet
- **Durchsuchbar** - Text extrahierbar
- **Validiert** - garantierte Lesbarkeit in Zukunft

**Full PDF/A Compliance mit Ghostscript:**

```bash
# Ghostscript installieren
sudo apt install ghostscript  # Ubuntu/Debian
brew install ghostscript       # macOS

# Konvertierung
gs -dPDFA=1 \
   -dBATCH -dNOPAUSE \
   -sProcessColorModel=DeviceRGB \
   -sDEVICE=pdfwrite \
   -sPDFACompatibilityPolicy=1 \
   -sOutputFile=output-PDFA.pdf \
   input.pdf

# Validierung
gs -dNODISPLAY -dPDFAValidate -sOutputFile=- input-PDFA.pdf
```

---

## 🔍 Durchsuchen

### PDF Text Extraction

```bash
# PDF Text extrahieren
pdftotext session.pdf session.txt

# Suche in PDF
grep -i "instagram" session.txt

# Alle PDFs durchsuchen
find docs/sessions/ -name "*.pdf" -exec pdftotext {} - \; | grep -i "scraper"
```

### Python Search

```python
from pypdf import PdfReader

def search_in_pdf(pdf_path, query):
    reader = PdfReader(pdf_path)
    results = []
    
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if query.lower() in text.lower():
            results.append((i+1, text))
    
    return results

# Usage
results = search_in_pdf("session.pdf", "instagram")
for page_num, text in results:
    print(f"Found on page {page_num}")
```

---

## 🎨 Styling & Customization

### Custom CSS (für HTML Export)

```python
# In export_chat.py, modify html_to_pdf() style section:

custom_style = """
<style>
    body {
        font-family: 'Georgia', serif;
        background: #f9f9f9;
        color: #333;
    }
    pre {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 8px;
    }
</style>
"""
```

### PDF Watermark

```python
from reportlab.pdfgen import canvas

def add_watermark(input_pdf, output_pdf, text):
    # Add "CONFIDENTIAL" or "DRAFT" watermark
    # Implementation...
```

---

## 📚 Weitere Exportmöglichkeiten

### 1. **Notion Export**

```bash
# Markdown zu Notion
# Via Notion API oder Import-Feature
```

### 2. **Obsidian Vault**

```bash
# Markdown zu Obsidian
cp chat-export.md ~/Obsidian/krawl-foundation/sessions/$(date +%Y-%m-%d).md
```

### 3. **Confluence/Wiki**

```bash
# HTML Export
python scripts/export_chat.py chat.md --format html

# Upload to Confluence via API
curl -X POST "https://wiki.example.com/rest/api/content" \
  -H "Authorization: Bearer $TOKEN" \
  -d @output.html
```

### 4. **GitHub Gist**

```bash
# Als Private Gist
gh gist create chat-export.md --desc "Dev Session 2025-11-21"
```

---

## 🐛 Troubleshooting

### "markdown module not found"

```bash
pip install markdown
```

### "reportlab not found"

```bash
pip install reportlab
```

### "Clipboard access failed"

```bash
# Linux: xclip/xsel installieren
sudo apt install xclip

# macOS: sollte funktionieren
# Windows: WSL hat ggf. Probleme mit Clipboard
```

### "PDF is empty"

- Prüfe Input: `cat chat.md | head -50`
- Prüfe Encoding: Datei sollte UTF-8 sein
- Prüfe Markdown-Syntax

### "Ghostscript error"

```bash
# Ghostscript version prüfen
gs --version  # sollte >= 9.50 sein

# Permissions
chmod 644 input.pdf
```

---

## 📖 Beispiel-Session

**Input (chat-export.md):**
```markdown
# Chat Session 2025-11-21

## User
Ich möchte einen Event-Scraper bauen.

## Assistant
Gerne! Lass uns einen CLI-basierten Scraper erstellen...

## User
Wie funktioniert der Diff?

## Assistant
Der Diff-Command vergleicht zwei Events...
```

**Command:**
```bash
python scripts/export_chat.py chat-export.md \
  -o archive/session-2025-11-21.pdf \
  --title "Event Scraper Development" \
  --author "feileberlin" \
  --format pdfa
```

**Output:**
```
✅ Loaded 15234 chars from chat-export.md
✅ PDF created: archive/session-2025-11-21.pdf
✅ PDF/A created: archive/session-2025-11-21-PDFA.pdf
✅ Export completed!
```

---

## 💡 Best Practices

1. **Regelmäßig exportieren** - Nach jeder Session
2. **Sinnvolle Namen** - Datum + Kurzbeschreibung
3. **Git committen** - Versionshistorie
4. **Metadaten pflegen** - Title, Author, Keywords
5. **PDF/A nutzen** - Für Langzeitarchivierung
6. **Sessions-Verzeichnis** - Zentraler Ort für alle Exports
7. **README.md** in sessions/ - Index aller Sessions

---

## 📋 Session Index (Beispiel)

**`docs/sessions/README.md`:**
```markdown
# Chat Session Archive

| Date | Topic | File | Tags |
|------|-------|------|------|
| 2025-11-21 | Initial Setup | session-2025-11-21.pdf | setup, cli, architecture |
| 2025-11-22 | Scraper Implementation | session-2025-11-22.pdf | scraper, instagram, facebook |
| 2025-11-23 | Dashboard Creation | session-2025-11-23.pdf | dashboard, yaml, github-pages |

## Search Index

- **CLI Commands**: 2025-11-21, 2025-11-22
- **Instagram Scraper**: 2025-11-22
- **YAML Features**: 2025-11-23
```

---

## 🔗 Weitere Infos

- [ReportLab Documentation](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [PDF/A Standard](https://en.wikipedia.org/wiki/PDF/A)
- [Python Markdown](https://python-markdown.github.io/)

---

**Last Updated:** 2025-11-21
