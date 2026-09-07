# 🤖 UGAI - Telegram AI & Utility Assistant

> 🚧 **Status:** Active Development (Work in Progress)

Bu proje aktif olarak geliştirilmeye devam eden, içerisinde yapay zeka sohbet modelleri, finansal veri takibi ve sistem araçlarını barındıran çok yönlü bir Telegram botudur.

### 🚀 Mevcut Modüller & Özellikler
* 🧠 **Groq LLM Entegrasyonu:** Asenkron çalışabilen, yedekli (fallback) yapay zeka sohbet motoru.
* 📊 **Canlı Altın Takibi:** Harem Altın verileri üzerinden anlık kur sorgulama ve günlük abonelik mekanizması.
* 🎮 **Steam Fırsatları:** Mağaza üzerindeki indirimli oyunları otomatik listeleme ve kartlı bilgilendirme.
* 🔐 **Güvenli Şifre Üreteci:** Karmaşık ve rastgele parola üretme komutu (`/pass`).
* ☁️ **Hava Durumu Servisi:** OpenWeatherMap API entegrasyonu.

---

## 🛠️ Kurulum ve Çalıştırma

1. **Repoyu klonlayın:**
   ```bash
    git clone https://github.com/Ugurklcx/ugai-telegram-bot.git
    cd ugai-telegram-bot

2. **Bağımlılıkları yükleyin:**
   pip install -r requirements.txt

3. **API Gereklilikleri**
   .env_example dosyasının adını .env olarak değiştiriniz ve kendi API kodlarınızı giriniz.
   
   Terminal:
   cp .env_example .env

4. **Başlatma**
    main.py üzerinden botu başlatınız.

*Yeni özellikler ve mimari güncellemeler düzenli olarak eklenmektedir.*