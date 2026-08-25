import os
import aiohttp

async def hava_durumu(sehir: str) -> str:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={sehir}&appid={api_key}&units=metric&lang=tr"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as response:
                res = await response.json()
                if res.get("cod") == 200:
                    return f"🌤 {sehir.capitalize()}: {res['main']['temp']}°C, {res['weather'][0]['description']}"
                return "Şehir bulunamadı."
    except Exception:
        return "Hava durumu alınamadı."