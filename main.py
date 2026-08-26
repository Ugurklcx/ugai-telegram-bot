import os
import sys
import asyncio

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler

#DATABASE STARTER
from database.db import tabloyu_olustur

#HANDLERS
from handlers.steam_discounts_write import steam_command
from handlers.password_creator import password_creator_handler
from handlers.chat import ask_ai
from handlers.gold_handler import altin_komutu_handler, build_gold_message
from handlers.start_handler import start_komutu_handler, start_buttons_callback
from handlers.gold_handler import gold_button_callback

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

def main():
    tabloyu_olustur()
    print("🤖 UGAI ÇALIŞIYOR!...")

    app = ApplicationBuilder().token(TOKEN).build()

    #ROUTES
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