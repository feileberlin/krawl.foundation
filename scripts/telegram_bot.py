#!/usr/bin/env python3
"""
Minimalistischer Telegram Bot für krawl.foundation
100% automatisiert - keine User-Interaktion nach Upload

Supported Input Types:
- 📸 Photo: Flyer-Upload → OCR → Event Draft
- 🎤 Voice: Sprachnachricht → VOSK Transkription → Event Draft
- 💬 Text: Direktnachricht → Event Draft

Flow:
1. User sendet Flyer-Foto/Voice/Text
2. Bot lädt es herunter und cached es lokal
3. Bot triggert GitHub Actions Repository Dispatch
4. Bot sendet Bestätigung an User
5. GitHub Actions verarbeitet Input (OCR/VOSK, Draft-Erstellung)
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
        "📸 **Flyer-Foto** → OCR → Event-Draft\n"
        "🎤 **Sprachnachricht** → Transkription → Event-Draft\n"
        "💬 **Text** → Direkt als Event-Draft\n\n"
        "ℹ️ So funktioniert's:\n"
        "1. Du sendest Foto/Voice/Text\n"
        "2. Ich verarbeite es automatisch\n"
        "3. Dein Event wird als Draft angelegt\n"
        "4. Das Team prüft und veröffentlicht es\n\n"
        "🔒 Datenschutz: Deine Daten werden nur zur Event-Erstellung verwendet."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await update.message.reply_text(
        "🤖 krawl.foundation Event Bot\n\n"
        "**Eingabe-Möglichkeiten:**\n\n"
        "📸 **Flyer-Foto:** Sende Bild vom Event-Flyer\n"
        "   → OCR erkennt: Datum, Uhrzeit, Ort, Titel\n\n"
        "🎤 **Sprachnachricht:** Erzähl mir vom Event\n"
        "   → Transkription: \"Konzert am 31.12. im SO36...\"\n\n"
        "💬 **Text:** Schreib Event-Details direkt\n"
        "   → \"Party @ Berghain, 1.1.2026, 23 Uhr, Techno\"\n\n"
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
                    'message_type': 'photo',
                    'telegram_user_id': user.id,
                    'telegram_username': user.username or 'anonymous',
                    'file_id': photo.file_id,
                    'filename': filename,
                    'filepath': str(filepath),
                    'timestamp': timestamp,
                    'caption': update.message.caption or '',
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


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle voice messages - 100% automatisiert
    Voice → VOSK Transkription → Event Draft
    """
    user = update.effective_user
    voice = update.message.voice
    
    logger.info(f"🎤 Voice empfangen von {user.username or user.id} (file_id: {voice.file_id}, duration: {voice.duration}s)")
    
    # Acknowledge receipt
    processing_msg = await update.message.reply_text("🎤 Sprachnachricht erhalten! Transkribiere...")
    
    try:
        # Download voice message
        file = await context.bot.get_file(voice.file_id)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"voice_{user.id}_{timestamp}.ogg"
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
                    'message_type': 'voice',
                    'telegram_user_id': user.id,
                    'telegram_username': user.username or 'anonymous',
                    'file_id': voice.file_id,
                    'filename': filename,
                    'filepath': str(filepath),
                    'timestamp': timestamp,
                    'duration': voice.duration,
                    'mime_type': voice.mime_type,
                }
            }
            
            logger.info(f"🚀 Trigger Repository Dispatch: {dispatch_url}")
            response = requests.post(dispatch_url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 204:
                logger.info("✅ Repository Dispatch erfolgreich")
                await processing_msg.edit_text(
                    "✅ Sprachnachricht hochgeladen!\n\n"
                    "🤖 Dein Event wird jetzt automatisch verarbeitet:\n"
                    "• Sprache → Text Transkription\n"
                    "• Event-Daten extrahieren\n"
                    "• Draft erstellen\n\n"
                    "⏱️ Dauert ca. 30-60 Sekunden.\n"
                    "📧 Du wirst benachrichtigt sobald dein Event live geht!"
                )
            else:
                logger.error(f"❌ Repository Dispatch fehlgeschlagen: {response.status_code} - {response.text}")
                await processing_msg.edit_text(
                    "⚠️ Sprachnachricht gespeichert, aber automatische Verarbeitung fehlgeschlagen.\n"
                    "Das Team wurde benachrichtigt und wird es manuell verarbeiten."
                )
        else:
            logger.warning("⚠️ GITHUB_TOKEN nicht gesetzt - kein Repository Dispatch möglich")
            await processing_msg.edit_text(
                "💾 Sprachnachricht gespeichert!\n\n"
                "⚠️ Automatische Verarbeitung nicht konfiguriert.\n"
                "Das Team wird deine Nachricht manuell verarbeiten."
            )
    
    except Exception as e:
        logger.error(f"❌ Fehler beim Verarbeiten: {e}", exc_info=True)
        await processing_msg.edit_text(
            "❌ Fehler beim Hochladen.\n"
            "Bitte versuche es später erneut oder kontaktiere: krawl@feileberlin.de"
        )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle text messages - 100% automatisiert
    Text → Event Draft (direkt, ohne weitere Verarbeitung)
    """
    user = update.effective_user
    text = update.message.text
    
    # Ignore commands
    if text.startswith('/'):
        return
    
    logger.info(f"💬 Text empfangen von {user.username or user.id}: {text[:50]}...")
    
    # Acknowledge receipt
    processing_msg = await update.message.reply_text("💬 Nachricht erhalten! Erstelle Draft...")
    
    try:
        # Save text message
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"text_{user.id}_{timestamp}.txt"
        filepath = CACHE_DIR / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        
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
                    'message_type': 'text',
                    'telegram_user_id': user.id,
                    'telegram_username': user.username or 'anonymous',
                    'text': text,
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
                    "✅ Text-Nachricht hochgeladen!\n\n"
                    "🤖 Dein Event wird jetzt automatisch verarbeitet:\n"
                    "• Event-Daten extrahieren\n"
                    "• Draft erstellen\n\n"
                    "⏱️ Dauert ca. 10-20 Sekunden.\n"
                    "📧 Du wirst benachrichtigt sobald dein Event live geht!"
                )
            else:
                logger.error(f"❌ Repository Dispatch fehlgeschlagen: {response.status_code} - {response.text}")
                await processing_msg.edit_text(
                    "⚠️ Nachricht gespeichert, aber automatische Verarbeitung fehlgeschlagen.\n"
                    "Das Team wurde benachrichtigt und wird es manuell verarbeiten."
                )
        else:
            logger.warning("⚠️ GITHUB_TOKEN nicht gesetzt - kein Repository Dispatch möglich")
            await processing_msg.edit_text(
                "💾 Nachricht gespeichert!\n\n"
                "⚠️ Automatische Verarbeitung nicht konfiguriert.\n"
                "Das Team wird deine Nachricht manuell verarbeiten."
            )
    
    except Exception as e:
        logger.error(f"❌ Fehler beim Verarbeiten: {e}", exc_info=True)
        await processing_msg.edit_text(
            "❌ Fehler beim Verarbeiten.\n"
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
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))
    application.add_handler(MessageHandler(filters.Document.IMAGE | filters.Document.PDF, handle_document))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    # Start bot
    logger.info("✅ Bot gestartet! Drücke Ctrl+C zum Beenden.")
    logger.info("📸 Photo Handler: Active")
    logger.info("🎤 Voice Handler: Active")
    logger.info("💬 Text Handler: Active")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n👋 Bot beendet")
    except Exception as e:
        logger.error(f"❌ Fataler Fehler: {e}", exc_info=True)
        sys.exit(1)
