import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from groq import AsyncGroq, RateLimitError, APIError
from telegram import Update
from telegram.ext import ContextTypes

# 1. .env dosyasının yolunu bulup yüklüyoruz
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY bulunamadı! Lütfen .env dosyanı kontrol et.")

# 2. Doğrudan Resmi AsyncGroq İstemcisi
client = AsyncGroq(api_key=api_key)

# Denediğimiz aktif Groq model adayları listesi
MODEL_CANDIDATES = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant"
]

async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_text = update.message.text

    # Telegram'da "yazıyor..." göstergesi
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    answer = None

    # Modelleri sırayla dener, çalışan ilk modeli bulduğunda cevabı alır
    for model_name in MODEL_CANDIDATES:
        try:
            print(f"🔄 Groq deneniyor: {model_name}")
            response = await client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "Sen samimi, zeki ve pratik bir asistansın. Türkçe yanıtlar ver."},
                    {"role": "user", "content": user_text}
                ],
                timeout=15
            )
            answer = response.choices[0].message.content
            print(f"✅ Başarılı model: {model_name}")
            break  # Yanıt başarılı alındıysa döngüden çık

        except RateLimitError:
            print(f"⚠️ Groq limit uyarısı ({model_name}), sonraki model deneniyor...")
            await asyncio.sleep(1)
            continue

        except APIError as e:
            # Eğer 404 (model not found) veya 400 (decommissioned) verirse sıradakine geç
            print(f"❌ Groq API Hatası ({model_name}): {e}")
            continue

        except Exception as e:
            print(f"❌ Beklenmeyen hata ({model_name}): {e}")
            continue

    if not answer:
        answer = "Üzgünüm, şu an yanıt üretemiyorum. Lütfen biraz sonra tekrar dene."

    # Telegram'a yanıtı gönder
    await update.message.reply_text(answer)