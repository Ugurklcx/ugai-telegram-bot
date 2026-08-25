import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError, APIError
from telegram import Update
from telegram.ext import CallbackContext

# 1. .env dosyasının yolunu bulup yüklüyoruz
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(f"❌ GROQ_API_KEY bulunamadı! Lütfen .env dosyanı kontrol et.")

# 2. OpenAI istemcisini Groq sunucularına yönlendiriyoruz
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

async def ask_ai(update: Update, context: CallbackContext):
    user_text = update.message.text
    retries = 3

    # Telegram'da "yazıyor..." göstergesi
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    answer = None

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Hızlı ve çok güçlü açık kaynak model
                messages=[
                    {"role": "system", "content": "Sen samimi, zeki ve pratik bir asistansın. Türkçe yanıtlar ver."},
                    {"role": "user", "content": user_text}
                ],
                timeout=15
            )
            answer = response.choices[0].message.content
            break  # Yanıt başarılıysa döngüden çık
            
        except RateLimitError:
            print(f"⚠️ Groq limit uyarısı, {attempt + 1}. deneme bekleniyor...")
            await asyncio.sleep(2)
            
        except APIError as e:
            print(f"❌ Groq API Hatası: {e}")
            break
        except Exception as e:
            print(f"❌ Beklenmeyen hata: {e}")
            break

    if not answer:
        answer = "Üzgünüm, şu an yanıt üretemiyorum. Lütfen biraz sonra tekrar dene."

    # Telegram'a yanıtı at
    await update.message.reply_text(answer)