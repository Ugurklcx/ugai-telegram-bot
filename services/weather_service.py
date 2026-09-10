import os
import aiohttp

async def hava_durumu(şehir: str) -> str:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Hava durumu servisi şu an aktif değil."

    url = f"http://api.openweathermap.org/data/2.5/weather?q={şehir}&appid={api_key}&units=metric&lang=tr"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as response:
                res = await response.json()
                if res.get("cod") == 200:
                    temp = res['main']['temp']
                    desc = res['weather'][0]['description']
                    return f"{şehir.capitalize()}: {temp}°C, {desc}"
                return "Şehir bulunamadı."
    except Exception:
        return "Hava durumu bilgisi alınamadı."

# Groq'a Tanıtacağımız Tool Şeması
WEATHER_TOOL = {
    "type": "function",
    "function": {
        "name": "hava_durumu",
        "description": "Belirtilen şehrin anlık hava durumunu ve sıcaklığını getirir.",
        "parameters": {
            "type": "object",
            "properties": {
                "şehir": {
                    "type": "string",
                    "description": "Hava durumu öğrenilmek istenen şehir (Örn: Istanbul, Ankara)"
                }
            },
            "required": ["şehir"],
        },
    },
}