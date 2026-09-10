import os
import sys
import re
import asyncio
import logging

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    CallbackQueryHandler,
    ContextTypes
)

# DATABASE STARTER
from database import tabloyu_olustur

# HANDLERS
from handlers.steam_discounts_write import steam_command
from handlers.password_creator import password_creator_handler
from handlers.chat import ask_ai
from handlers.gold_handler import altin_komutu_handler, build_gold_message, gold_button_callback
from handlers.start_handler import start_komutu_handler, start_buttons_callback

# 1. LOG MASKELEME FİLTRESİ (Token & API Key Gizleyici)
class SensitiveDataFilter(logging.Filter):
    """Loglarda Telegram Bot Token ve API anahtarlarının açık metin görünmesini engeller."""
    def filter(self, record):
        if isinstance(record.msg, str):
            # Telegram Bot Token Maskeleme
            record.msg = re.sub(r'bot\d+:[A-Za-z0-9_-]+', 'bot***TOKEN_MASKED***', record.msg)
            record.msg = re.sub(r'/bot[0-9]+:[^/]+/', '/bot***TOKEN_MASKED***/', record.msg)
            # Gemini / Google API Key Maskeleme
            record.msg = re.sub(r'AIzaSy[A-Za-z0-9_-]{33}', 'AIzaSy***KEY_MASKED***', record.msg)
        return True

# 2. LOGGING SETUP
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Filtreyi tüm log sistemine uygula
sensitive_filter = SensitiveDataFilter()
logging.getLogger().addFilter(sensitive_filter)
logging.getLogger("httpx").addFilter(sensitive_filter)
logging.getLogger("telegram").addFilter(sensitive_filter)

# 3. KÜRESEL HATA YAKALAYICI (Global Error Handler)
async def global_error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Yakalanmayan hataları loglar ve botun çökmesini engeller."""
    logger.error("Hata oluştu!", exc_info=context.error)
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text("⚠️ Bir işlem sırasında beklenmedik bir hata oluştu.")

# Windows Event Loop Fix
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

def main():
    tabloyu_olustur()
    logger.info("🤖 UGAI ÇALIŞIYOR!...")

    app = ApplicationBuilder().token(TOKEN).build()

    # GLOBAL ERROR HANDLER
    app.add_error_handler(global_error_handler)

    # ROUTES
    app.add_handler(CommandHandler("pass", password_creator_handler))
    app.add_handler(CommandHandler("steam", steam_command))
    app.add_handler(CommandHandler("gold", altin_komutu_handler))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), ask_ai))
    app.add_handler(CommandHandler("start", start_komutu_handler))
    app.add_handler(CommandHandler("help", start_komutu_handler))
    app.add_handler(CallbackQueryHandler(start_buttons_callback, pattern="^(get_gold_now|get_steam_now)$"))
    app.add_handler(CallbackQueryHandler(gold_button_callback, pattern="^(sub_gold|unsub_gold)$"))

    app.run_polling()

if __name__ == '__main__':
    main()