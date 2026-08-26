from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.gold_services_tr import get_gram_gold_price
from database import set_subscription, get_active_subscribers


async def start_buttons_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    # 1. KRİTİK NOKTA: Telegram'a tıklamayı aldığımızı bildiriyoruz (Yükleme simgesi durur)
    await query.answer()
    
    # 2. Hangi butona basıldığını kontrol ediyoruz
    if query.data == "get_gold_now":
        # Altın komutu handler'ını çağırıyoruz
        await altin_komutu_handler(update, context)
        
    elif query.data == "get_steam_now":
        # Steam verisini getiren fonksiyonunu çağırabilirsin
        await query.message.reply_text("🎮 *Steam indirimleri yükleniyor...*", parse_mode="Markdown")

# 1. Gold Mesajı Oluşturucu (Kullanıcının abonelik durumuna göre buton üretir)
def build_gold_message(user_id: int):
    data = get_gram_gold_price()
    if not data:
        return "⚠️ *Altın verisi şu an alınamıyor.*", None
    
    tarih_str = datetime.now().strftime("%d.%m.%Y")
    
    text = (
        f"📊 *GÜNCEL ALTIN FİYATLARI*\n\n"
        f"🗓 *Tarih:* `{tarih_str}`\n"
        f"💰 *Satış Fiyatı:* `{data['satis']} TL`\n"
        f"📥 *Alış Fiyatı:* `{data['alis']} TL`\n"
    )
    
    # Kullanıcı zaten abone mi kontrol et
    aktif_aboneler = get_active_subscribers()
    if user_id in aktif_aboneler:
        keyboard = [[InlineKeyboardButton("❌ Abonelikten Çık", callback_data="unsub_gold")]]
    else:
        keyboard = [[InlineKeyboardButton("🔔 Her Sabah 09:00'da Bildirim Al (Abone Ol)", callback_data="sub_gold")]]
        
    return text, InlineKeyboardMarkup(keyboard)

# 2. /gold Komut Handler'ı
async def altin_komutu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text, reply_markup = build_gold_message(user_id)
    
    # 1. Eğer normal komut yazıldıysa (/gold) -> update.message doludur
    if update.message:
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)
        
    # 2. Eğer butona basıldıysa ("Canlı Altın" butonu) -> update.callback_query doludur
    elif update.callback_query:
        await update.callback_query.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)

# 3. Buton Tıklama Handler'ı (Abone Ol / Çık)
async def gold_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    
    if query.data == "sub_gold":
        set_subscription(user_id, True)
        await query.edit_message_text(
            text="✅ *Başarıyla abone oldun!* Her sabah 09:00'da güncel gram altın fiyatı cebine gelecek.",
            parse_mode="Markdown"
        )
    elif query.data == "unsub_gold":
        set_subscription(user_id, False)
        await query.edit_message_text(
            text="🔴 *Aboneliğin iptal edildi.* Dilediğin zaman `/gold` veya `/abone_ol` ile tekrar katılabilirsin.",
            parse_mode="Markdown"
        )