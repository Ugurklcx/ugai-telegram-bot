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
from telegram.request import HTTPXRequest

# DATABASE STARTER
from database import tabloyu_olustur

# HANDLERS
from handlers.steam_discounts_write import steam_command
from handlers.password_creator import password_creator_handler
from handlers.chat import ask_ai
from handlers.gold_handler import altin_komutu_handler, build_gold_message, gold_button_callback
from handlers.start_handler import start_komutu_handler, start_buttons_callback


# 1. LOGGING CONFIGURATION
class SensitiveDataFormatter(logging.Formatter):
    """Ekrana veya dosyaya basılan NİHAİ log metnindeki tüm token ve key'leri temizler."""
    
    def format(self, record):
        original_msg = super().format(record)
        
        clean_msg = re.sub(r'bot\d+:[A-Za-z0-9_-]+', 'bot***TOKEN_MASKED***', original_msg)
        clean_msg = re.sub(r'/bot[0-9]+:[^/]+/', '/bot***TOKEN_MASKED***/', clean_msg)
        clean_msg = re.sub(r'AIzaSy[A-Za-z0-9_-]{33}', 'AIzaSy***KEY_MASKED***', clean_msg)
        
        return clean_msg


handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(SensitiveDataFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logger = logging.getLogger()
logger.setLevel(logging.INFO)

for h in logger.handlers[:]:
    logger.removeHandler(h)
logger.addHandler(handler)


# 2. GLOBAL ERROR HANDLER
async def global_error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Yakalanmayan hataları loglar ve botun çökmesini engeller."""
    logger.error("Hata oluştu!", exc_info=context.error)
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text("⚠️ Bir işlem sırasında beklenmedik bir hata oluştu.")


if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")


def main():
    if not TOKEN:
        raise ValueError("❌ TELEGRAM_TOKEN bulunamadı! .env dosyasını kontrol et.")

    tabloyu_olustur()
    logger.info("🤖 UGAI ÇALIŞIYOR!...")

    # Timeout sürelerini artırarak HTTPX isteği oluşturuyoruz
    request_config = HTTPXRequest(
        connect_timeout=20.0,
        read_timeout=20.0
    )

    # Uygulamayı timeout ayarları ve token ile tek seferde inşa ediyoruz
    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .request(request_config)
        .build()
    )

    # GLOBAL ERROR HANDLER
    app.add_error_handler(global_error_handler)

    # ROUTES
    app.add_handler(CommandHandler("pass", password_creator_handler))
    app.add_handler(CommandHandler("steam", steam_command))
    app.add_handler(CommandHandler("gold", altin_komutu_handler))
    app.add_handler(CommandHandler("start", start_komutu_handler))
    app.add_handler(CommandHandler("help", start_komutu_handler))
    
    # Callback Handlers
    app.add_handler(CallbackQueryHandler(start_buttons_callback, pattern="^(get_gold_now|get_steam_now)$"))
    app.add_handler(CallbackQueryHandler(gold_button_callback, pattern="^(sub_gold|unsub_gold)$"))

    # AI Chat Handler (Tüm metinleri yakaladığı için en sonda durmalı)
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), ask_ai))

    app.run_polling()

if __name__ == '__main__':
    main()