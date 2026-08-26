from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.gold_services_tr import get_gram_gold_price
from database import set_subscription, get_active_subscribers


# 1. Yardımcı Fonksiyon: Sadece mesaj ve buton nesnesini üretir (Telegram Callback Değildir)
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
    
    # Kullanıcının abonelik durumuna göre dinamik buton
    aktif_aboneler = get_active_subscribers()
    if user_id in aktif_aboneler:
        keyboard = [[InlineKeyboardButton("❌ Abonelikten Çık", callback_data="unsub_gold")]]
    else:
        keyboard = [[InlineKeyboardButton("🔔 Her Sabah 09:00'da Bildirim Al", callback_data="sub_gold")]]
        
    return text, InlineKeyboardMarkup(keyboard)


# 2. Komut Handler'ı: Telegram'ın çağırdığı asıl async fonksiyon (/gold için)
async def altin_komutu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user:
        return
        
    user_id = user.id
    text, reply_markup = build_gold_message(user_id)
    
    # Normal mesaj (/gold yazıldıysa)
    if update.message:
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)
        
    # Butona basılarak tetiklendiyse (Inline buton)
    elif update.callback_query and update.callback_query.message:
        await update.callback_query.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)


# 3. Başlangıç Menüsü Buton Tıklamaları
async def start_buttons_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return
        
    await query.answer()
    
    if query.data == "get_gold_now":
        await altin_komutu_handler(update, context)
        
    elif query.data == "get_steam_now":
        if query.message:
            await query.message.reply_text("🎮 *Steam indirimleri yükleniyor...*", parse_mode="Markdown")


# 4. Abonelik İşlemleri Buton Tıklamaları (Abone Ol / Çık)
async def gold_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query or not query.from_user:
        return
        
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
            text="🔴 *Aboneliğin iptal edildi.* Dilediğin zaman `/gold` ile tekrar katılabilirsin.",
            parse_mode="Markdown"
        )