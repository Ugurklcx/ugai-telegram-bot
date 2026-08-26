import requests
from datetime import datetime

def get_gram_gold_price():
    url = "https://www.haremaltin.com/ajax/kur_degisim"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://www.haremaltin.com",
        "Referer": "https://www.haremaltin.com/",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    
    # Bugünün tarihini dinamik alalım (Y-M-D)
    bugun = datetime.now().strftime("%Y-%m-%d")
    
    payload = {
        "tarih1": bugun,
        "tarih2": bugun,
        "miktar": "250",
        "kod": "ALTIN",
        "gun_sonu": "1"
    }

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        if response.status_code == 200:
            json_data = response.json()
            kayitlar = json_data.get("data", {}).get("data", [])
            if kayitlar:
                en_guncel = kayitlar[-1]
                return {
                    "alis": en_guncel["alis"],
                    "satis": en_guncel["satis"],
                    "tarih": en_guncel["kayit_tarihi"]
                }
    except Exception as e:
        print("Altın verisi çekilirken hata oluştu:", e)
    
    return None