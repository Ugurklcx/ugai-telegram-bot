from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from handlers.gold_handler import altin_komutu_handler
from handlers.steam_discounts_write import steam_command

async def start_komutu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kullanici_adi = update.effective_user.first_name
    
    text = (
        f"👋 *Merhaba {kullanici_adi}, UGAI Bot'a Hoş Geldin!*\n\n"
        f"Senin için finansal verileri, sistem araçlarını ve oyun fırsatlarını takip eden kişisel asistanınım.\n\n"
        f"📌 *Kullanabileceğin Komutlar:*\n"
        f"🔹 `/gold` - Anlık gram altın fiyatını getirir.\n"
        f"🔹 `/pass` - Rastgele ve güçlü bir şifre üretir.\n"
        f"🔹 `/steam` - Steam'deki güncel indirimleri ve fırsatları listeler.\n"
        f"🔹 `/abone_ol` - Her sabah 09:00'da otomatik altın fiyat bildirimi almanı sağlar."
    )
    
    keyboard = [
        [
            InlineKeyboardButton("📊 Canlı Altın", callback_data="get_gold_now"),
            InlineKeyboardButton("🎮 Steam İndirimleri", callback_data="get_steam_now")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# MAIN.PY'NİN BULAMADIĞI EKSİK FONKSİYON:
async def start_buttons_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
  query = update.callback_query
  await query.answer()  # Yükleme simgesini kapatır

  if query.data == "get_gold_now":
    # Altın komutunu tetikler
    await altin_komutu_handler(update, context)

  elif query.data == "get_steam_now":
    # Doğrudan Steam servisini tetikleyen handler'ı çağırıyoruz
    await steam_command(update, context)