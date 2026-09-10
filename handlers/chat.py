import os
import json
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from groq import AsyncGroq, RateLimitError, APIError
from telegram import Update
from telegram.ext import ContextTypes

# Hava durumu fonksiyonunu ve şemasını servisimizden çekiyoruz
from services.weather_service import hava_durumu, WEATHER_TOOL

# 1. .env dosyasının yolunu bulup yüklüyoruz
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY bulunamadı! Lütfen .env dosyanı kontrol et.")

# 2. Doğrudan Resmi AsyncGroq İstemcisi
client = AsyncGroq(api_key=api_key)

# Groq Aktif Modeller Listesi (Tam Path İsimleri)
MODEL_CANDIDATES = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "openai/gpt-oss-120b",
    "qwen/qwen3-32b"
]
async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_text = update.message.text

    # Telegram'da "yazıyor..." göstergesi (Ağ hatasında akışı bozmasın)
    try:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    except Exception as e:
        print(f"⚠️ Chat action gönderilemedi (Ağ zaman aşımı): {e}")

    messages = [
        {"role": "system", "content": "Sen samimi, zeki ve pratik bir asistansın. Türkçe yanıtlar ver."},
        {"role": "user", "content": user_text}
    ]

    answer = None

    # Modelleri sırayla dener
    for model_name in MODEL_CANDIDATES:
        try:
            print(f"🔄 Groq deneniyor: {model_name}")
            
            # 1. İlk İstek: Kullanıcı mesajını ve Tool şemasını gönderiyoruz
            response = await client.chat.completions.create(
                model=model_name,
                messages=messages,
                tools=[WEATHER_TOOL],
                tool_choice="auto",
                timeout=15
            )
            
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            # 2. Model bir fonksiyon çalıştırmak istedi mi?
            if tool_calls:
                # Modelin yanıtını geçmişe ekliyoruz
                messages.append(response_message)

                for tool_call in tool_calls:
                    if tool_call.function.name == "hava_durumu":
                        # Modelin gönderdiği parametreleri çözümlüyoruz
                        args = json.loads(tool_call.function.arguments)
                        sehir = args.get("şehir")
                        
                        # Asenkron OpenWeather fonksiyonumuzu çağırıyoruz
                        api_result = await hava_durumu(sehir)

                        # Fonksiyon sonucunu "tool" rolüyle geçmişe besliyoruz
                        messages.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": "hava_durumu",
                            "content": api_result,
                        })

                # 3. İkinci İstek: Canlı veriyi kullanarak nihai cevabı ürettiriyoruz
                second_response = await client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    timeout=15
                )
                answer = second_response.choices[0].message.content
            else:
                answer = response_message.content

            print(f"✅ Başarılı model: {model_name}")
            break  # Yanıt başarılı alındıysa döngüden çık

        except RateLimitError:
            print(f"⚠️ Groq limit uyarısı ({model_name}), sonraki model deneniyor...")
            await asyncio.sleep(1)
            continue

        except APIError as e:
            print(f"❌ Groq API Hatası ({model_name}): {e}")
            continue

        except Exception as e:
            print(f"❌ Beklenmeyen hata ({model_name}): {e}")
            continue

    if not answer:
        answer = "Üzgünüm, şu an yanıt üretemiyorum. Lütfen biraz sonra tekrar dene."

    # Telegram'a yanıtı gönder
    await update.message.reply_text(answer)