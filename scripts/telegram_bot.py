#!/usr/bin/env python3
"""
Minimalistischer Telegram Bot für krawl.foundation
100% automatisiert - keine User-Interaktion nach Upload

Flow:
1. User sendet Flyer-Foto
2. Bot lädt es herunter und cached es lokal
3. Bot triggert GitHub Actions Repository Dispatch
4. Bot sendet Bestätigung an User
5. GitHub Actions verarbeitet Flyer (OCR, Draft-Erstellung)
6. User wird später benachrichtigt wenn Event live geht
"""

import os
import sys
import asyncio
import logging
from pathlib import Path
from datetime import datetime

try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
    from dotenv import load_dotenv
    import requests
except ImportError:
    print("❌ Fehlende Dependencies!")
    print("Installation: pip install python-telegram-bot python-dotenv requests")
    sys.exit(1)

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment
PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / '.env')

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPO = os.getenv('GITHUB_REPO', 'feileberlin/krawl.foundation')
CACHE_DIR = PROJECT_ROOT / '.cache' / 'telegram'

if not TELEGRAM_TOKEN:
    logger.error("❌ TELEGRAM_TOKEN nicht gesetzt! Führe ./scripts/setup_secrets.sh aus")
    sys.exit(1)

if not GITHUB_TOKEN:
    logger.warning("⚠️  GITHUB_TOKEN nicht gesetzt - Repository Dispatch wird fehlschlagen")

# Ensure cache directory exists
CACHE_DIR.mkdir(parents=True, exist_ok=True)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text(
        "👋 Willkommen bei krawl.foundation!\n\n"
        "📸 Sende mir ein Flyer-Foto, und ich erstelle automatisch einen Event-Entwurf.\n\n"
        "ℹ️ So funktioniert's:\n"
        "1. Du sendest das Foto\n"
        "2. Ich verarbeite es automatisch\n"
        "3. Dein Event wird als Draft angelegt\n"
        "4. Das Team prüft und veröffentlicht es\n\n"
        "🔒 Datenschutz: Deine Daten werden nur zur Event-Erstellung verwendet."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await update.message.reply_text(
        "🤖 krawl.foundation Event Bot\n\n"
        "📸 Sende einfach ein Flyer-Foto!\n\n"
        "Der Bot erkennt automatisch:\n"
        "• Datum & Uhrzeit\n"
        "• Ort/Venue\n"
        "• Event-Titel\n"
        "• Beschreibung\n\n"
        "⏱️ Verarbeitung dauert ca. 30-60 Sekunden.\n"
        "✅ Du bekommst eine Bestätigung sobald der Draft erstellt wurde.\n\n"
        "❓ Fragen? Schreib an: krawl@feileberlin.de"
    )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle photo uploads - 100% automatisiert
    Keine User-Interaktion, nur Upload → Trigger → Bestätigung
    """
    user = update.effective_user
    photo = update.message.photo[-1]  # Highest resolution
    
    logger.info(f"📸 Photo empfangen von {user.username or user.id} (file_id: {photo.file_id})")
    
    # Acknowledge receipt
    processing_msg = await update.message.reply_text("📸 Flyer erhalten! Verarbeite...")
    
    try:
        # Download photo
        file = await context.bot.get_file(photo.file_id)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"flyer_{user.id}_{timestamp}.jpg"
        filepath = CACHE_DIR / filename
        
        await file.download_to_drive(filepath)
        logger.info(f"💾 Gespeichert: {filepath}")
        
        # Trigger GitHub Actions Repository Dispatch
        if GITHUB_TOKEN:
            dispatch_url = f"https://api.github.com/repos/{GITHUB_REPO}/dispatches"
            headers = {
                'Accept': 'application/vnd.github.v3+json',
                'Authorization': f'Bearer {GITHUB_TOKEN}',
            }
            payload = {
                'event_type': 'telegram_flyer_submission',
                'client_payload': {
                    'telegram_user_id': user.id,
                    'telegram_username': user.username or 'anonymous',
                    'file_id': photo.file_id,
                    'filename': filename,
                    'filepath': str(filepath),
                    'timestamp': timestamp,
                }
            }
            
            logger.info(f"🚀 Trigger Repository Dispatch: {dispatch_url}")
            response = requests.post(dispatch_url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 204:
                logger.info("✅ Repository Dispatch erfolgreich")
                await processing_msg.edit_text(
                    "✅ Flyer hochgeladen!\n\n"
                    "🤖 Dein Event wird jetzt automatisch verarbeitet:\n"
                    "• OCR-Texterkennung\n"
                    "• Event-Daten extrahieren\n"
                    "• Draft erstellen\n\n"
                    "⏱️ Dauert ca. 30-60 Sekunden.\n"
                    "📧 Du wirst benachrichtigt sobald dein Event live geht!"
                )
            else:
                logger.error(f"❌ Repository Dispatch fehlgeschlagen: {response.status_code} - {response.text}")
                await processing_msg.edit_text(
                    "⚠️ Flyer gespeichert, aber automatische Verarbeitung fehlgeschlagen.\n"
                    "Das Team wurde benachrichtigt und wird es manuell verarbeiten."
                )
        else:
            # No GitHub Token - manual processing
            logger.warning("⚠️ GITHUB_TOKEN nicht gesetzt - kein Repository Dispatch möglich")
            await processing_msg.edit_text(
                "💾 Flyer gespeichert!\n\n"
                "⚠️ Automatische Verarbeitung nicht konfiguriert.\n"
                "Das Team wird deinen Flyer manuell verarbeiten."
            )
    
    except Exception as e:
        logger.error(f"❌ Fehler beim Verarbeiten: {e}", exc_info=True)
        await processing_msg.edit_text(
            "❌ Fehler beim Hochladen.\n"
            "Bitte versuche es später erneut oder kontaktiere: krawl@feileberlin.de"
        )


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle documents (PDFs, etc.) - same as photos"""
    await update.message.reply_text(
        "📄 Dokument empfangen!\n\n"
        "💡 Tipp: Sende Flyer am besten als **Foto** (nicht als Datei), "
        "dann kann ich sie besser verarbeiten.\n\n"
        "Falls es ein PDF ist, verarbeite ich es trotzdem - dauert nur etwas länger."
    )
    # TODO: Handle PDFs with pdf2image + OCR


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages - provide guidance"""
    await update.message.reply_text(
        "📝 Text empfangen.\n\n"
        "💡 Dieser Bot verarbeitet **Flyer-Fotos**.\n"
        "Sende einfach ein Foto vom Event-Flyer, und ich erstelle automatisch einen Draft.\n\n"
        "ℹ️ Für Fragen: /help"
    )


def main():
    """Start the bot"""
    if not TELEGRAM_TOKEN:
        logger.error("❌ TELEGRAM_TOKEN fehlt!")
        return
    
    logger.info("🤖 Starte krawl.foundation Telegram Bot...")
    logger.info(f"📁 Cache Dir: {CACHE_DIR}")
    logger.info(f"🔐 GitHub Repo: {GITHUB_REPO}")
    
    # Create application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.Document.IMAGE | filters.Document.PDF, handle_document))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    # Start bot
    logger.info("✅ Bot gestartet! Drücke Ctrl+C zum Beenden.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n👋 Bot beendet")
    except Exception as e:
        logger.error(f"❌ Fataler Fehler: {e}", exc_info=True)
        sys.exit(1)
