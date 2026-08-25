import random
import string
from telegram import Update
from telegram.ext import ContextTypes

async def password_creator_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/sifre komutu tetiklendiğinde çalışan handler"""
    
    total = []
    password = []
    
    for i in range(4):
        letter_count = random.randint(1, 4)
        number_count = 5 - letter_count

        for _ in range(letter_count):
            harf = random.choice(string.ascii_letters)
            total.append(harf)

        for _ in range(number_count):
            number = random.randint(0, 9)
            total.append(str(number))

        punctuation = random.choice(["!", "?", "@", "#", "$", "%", "&"])
        random_location = random.randint(0, len(total) - 1)
        total[random_location] = str(punctuation)

        if len(total) == 5:
            random.shuffle(total)
            password.append("".join(total))
            password.append("-")
            total.clear()

    if password:
        password.pop()  # Son eklenen fazladan '-' karakterini kaldırır
        
    final_password = "".join(password)
    
    # Yanıt gönderme (Markdown modunda özel karakter çakışmalarını önlemek için standart Markdown kullandım)
    await update.message.reply_text(
        f"🔐 *Senin için özel şifre üretildi:*\n\n`{final_password}`", 
        parse_mode="Markdown"
    )