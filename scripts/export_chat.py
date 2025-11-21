gh run list --workflow=auto-export-chat.yml#!/usr/bin/env python3
"""
Chat History to PDF/A Exporter
================================

Exportiert GitHub Copilot Chat-Verlauf als durchsuchbares PDF/A.

PROBLEM: VS Code Copilot Chat hat keine direkte Export-API.

LÖSUNGEN:

1. **Manueller Export (empfohlen):**
   - VS Code: Chat-Fenster → Rechtsklick → "Export Chat"
   - Speichert als Markdown
   - Dieses Script konvertiert MD → PDF/A

2. **Clipboard-Capture:**
   - Chat-Verlauf kopieren (Ctrl+A, Ctrl+C)
   - Script liest Clipboard und konvertiert

3. **Session-Logs (falls aktiviert):**
   - VS Code speichert ggf. Session-Logs
   - Location: ~/.config/Code/logs/

Usage:
    # Von Markdown-Export
    python scripts/export_chat.py chat-export.md -o chat-history.pdf
    
    # Von Clipboard
    python scripts/export_chat.py --from-clipboard -o chat-history.pdf
    
    # Mit Metadaten
    python scripts/export_chat.py chat.md -o output.pdf \
        --title "krawl.foundation Development Session" \
        --author "feileberlin" \
        --date "2025-11-21"

Requires:
    pip install markdown reportlab pypdf pillow
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
import re

def parse_args():
    parser = argparse.ArgumentParser(
        description="Export Chat History to PDF/A",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        'input',
        nargs='?',
        help='Input Markdown file (oder --from-clipboard)'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='chat-history.pdf',
        help='Output PDF file (default: chat-history.pdf)'
    )
    
    parser.add_argument(
        '--from-clipboard',
        action='store_true',
        help='Read from clipboard instead of file'
    )
    
    parser.add_argument(
        '--title',
        default='Chat History',
        help='PDF title metadata'
    )
    
    parser.add_argument(
        '--author',
        default='GitHub Copilot',
        help='PDF author metadata'
    )
    
    parser.add_argument(
        '--date',
        help='Date (ISO format, default: heute)'
    )
    
    parser.add_argument(
        '--format',
        choices=['pdf', 'pdfa', 'markdown', 'html'],
        default='pdfa',
        help='Output format (default: pdfa)'
    )
    
    return parser.parse_args()


def read_input(args):
    """Lese Input (File oder Clipboard)"""
    
    if args.from_clipboard:
        try:
            import pyperclip
            content = pyperclip.paste()
            print("✅ Content from clipboard gelesen")
            return content
        except ImportError:
            print("❌ Error: pyperclip not installed")
            print("   pip install pyperclip")
            sys.exit(1)
    
    elif args.input:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"❌ Error: File not found: {input_path}")
            sys.exit(1)
        
        content = input_path.read_text(encoding='utf-8')
        print(f"✅ Loaded {len(content)} chars from {input_path}")
        return content
    
    else:
        print("❌ Error: Provide input file or --from-clipboard")
        sys.exit(1)


def markdown_to_html(markdown_text):
    """Convert Markdown to HTML"""
    try:
        import markdown
    except ImportError:
        print("❌ Error: markdown not installed")
        print("   pip install markdown")
        sys.exit(1)
    
    # Extensions for better formatting
    html = markdown.markdown(
        markdown_text,
        extensions=[
            'fenced_code',
            'codehilite',
            'tables',
            'toc',
            'nl2br'
        ]
    )
    
    return html


def html_to_pdf(html_content, output_path, metadata):
    """Convert HTML to PDF with ReportLab"""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, PageBreak,
            Preformatted, Table, TableStyle
        )
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_LEFT, TA_CENTER
        from bs4 import BeautifulSoup
    except ImportError as e:
        print(f"❌ Error: Missing dependency: {e}")
        print("   pip install reportlab beautifulsoup4 lxml")
        sys.exit(1)
    
    # Create PDF
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
        title=metadata['title'],
        author=metadata['author'],
        subject=f"Chat History {metadata['date']}"
    )
    
    # Styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#764ba2'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    code_style = ParagraphStyle(
        'Code',
        parent=styles['Code'],
        fontSize=9,
        leftIndent=20,
        backColor=colors.HexColor('#f4f4f4'),
        borderColor=colors.HexColor('#ddd'),
        borderWidth=1,
        borderPadding=10
    )
    
    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Build story
    story = []
    
    # Title page
    story.append(Paragraph(metadata['title'], title_style))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(f"Author: {metadata['author']}", styles['Normal']))
    story.append(Paragraph(f"Date: {metadata['date']}", styles['Normal']))
    story.append(Spacer(1, 1*cm))
    story.append(PageBreak())
    
    # Content
    for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'pre', 'code', 'ul', 'ol']):
        
        if element.name in ['h1', 'h2', 'h3']:
            story.append(Paragraph(element.get_text(), heading_style))
        
        elif element.name == 'pre':
            code_text = element.get_text()
            story.append(Preformatted(code_text, code_style))
            story.append(Spacer(1, 0.3*cm))
        
        elif element.name == 'p':
            text = element.get_text()
            if text.strip():
                story.append(Paragraph(text, styles['Normal']))
                story.append(Spacer(1, 0.2*cm))
        
        elif element.name in ['ul', 'ol']:
            for li in element.find_all('li'):
                text = "• " + li.get_text()
                story.append(Paragraph(text, styles['Normal']))
            story.append(Spacer(1, 0.2*cm))
    
    # Build PDF
    doc.build(story)
    print(f"✅ PDF created: {output_path}")


def convert_to_pdfa(pdf_path):
    """Convert PDF to PDF/A (archival format)"""
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        print("⚠️  Warning: pypdf not installed, skipping PDF/A conversion")
        print("   pip install pypdf")
        return
    
    # Note: Full PDF/A compliance requires Ghostscript
    # This is a simplified approach
    
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    
    for page in reader.pages:
        writer.add_page(page)
    
    # Add PDF/A metadata
    writer.add_metadata({
        '/Title': 'Chat History',
        '/Author': 'GitHub Copilot',
        '/Subject': 'Development Session Chat',
        '/Keywords': 'krawl.foundation, chat, development',
        '/Creator': 'export_chat.py',
    })
    
    # Write
    pdfa_path = pdf_path.replace('.pdf', '-PDFA.pdf')
    with open(pdfa_path, 'wb') as f:
        writer.write(f)
    
    print(f"✅ PDF/A created: {pdfa_path}")
    print("⚠️  Note: For full PDF/A compliance, use Ghostscript:")
    print(f"   gs -dPDFA=1 -sProcessColorModel=DeviceRGB -o {pdfa_path} {pdf_path}")


def main():
    args = parse_args()
    
    print("🚀 Chat History Exporter")
    print("=" * 50)
    
    # Read input
    content = read_input(args)
    
    # Metadata
    metadata = {
        'title': args.title,
        'author': args.author,
        'date': args.date or datetime.now().strftime('%Y-%m-%d')
    }
    
    output_path = Path(args.output)
    
    # Export based on format
    if args.format == 'markdown':
        output_path = output_path.with_suffix('.md')
        output_path.write_text(content, encoding='utf-8')
        print(f"✅ Markdown saved: {output_path}")
    
    elif args.format == 'html':
        html = markdown_to_html(content)
        
        # Full HTML document
        full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{metadata['title']}</title>
    <style>
        body {{ font-family: sans-serif; max-width: 900px; margin: 40px auto; padding: 20px; }}
        pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
        h1, h2 {{ color: #667eea; }}
    </style>
</head>
<body>
    <h1>{metadata['title']}</h1>
    <p><strong>Author:</strong> {metadata['author']}</p>
    <p><strong>Date:</strong> {metadata['date']}</p>
    <hr>
    {html}
</body>
</html>
"""
        output_path = output_path.with_suffix('.html')
        output_path.write_text(full_html, encoding='utf-8')
        print(f"✅ HTML saved: {output_path}")
    
    elif args.format in ['pdf', 'pdfa']:
        html = markdown_to_html(content)
        html_to_pdf(html, output_path, metadata)
        
        if args.format == 'pdfa':
            convert_to_pdfa(output_path)
    
    print("=" * 50)
    print("✅ Export completed!")


if __name__ == '__main__':
    main()
