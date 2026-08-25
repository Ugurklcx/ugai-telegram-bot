import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Proje dizinini dinamik olarak bulup .env dosyasını nokta atışı yüklüyoruz
BASE_DIR = Path(__file__).resolve().parent.parent  # 6-Telegram_bot_project klasörünü bulur
load_dotenv(dotenv_path=BASE_DIR / ".env")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4o-mini",  # Hızlı ve ucuz alternatif (veya "gpt-4o")
    messages=[
        {"role": "system", "content": "Sen yardımcı ve pratik bir asistansın."},
        {"role": "user", "content": "Merhaba, bana basit bir selam ver."}
    ],
    temperature=0.7,
    max_tokens=500
)

# Yanıtı alma
answer = response.choices[0].message.content
print(answer)