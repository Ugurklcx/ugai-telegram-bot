import os
import sys
import asyncio

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

#DATABASE STARTER
from database.db import tabloyu_olustur

#HANDLERS
from handlers.steam_discounts_write import steam_command
from handlers.password_creator import password_creator_handler
from handlers.chat import ask_ai

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
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), ask_ai))

    app.run_polling()

if __name__ == '__main__':
    main()