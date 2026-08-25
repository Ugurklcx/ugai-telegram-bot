from telegram import Update
from telegram.ext import ContextTypes
from services.steam_service import get_steam_tr_deals

async def steam_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    indirimler = await get_steam_tr_deals()

    if not indirimler:
        await update.message.reply_text("❌ Şu an herhangi bir Steam indirimi bulunamadı.")
        return

    await update.message.reply_text("⏳ Steam fırsatları aranıyor, lütfen bekleyin...")
    
    for mesaj in indirimler:
        await update.message.reply_photo(
            photo=mesaj["image_url"],
            caption=(
                f"<b>{mesaj['name']}</b>\n"
                f"Orijinal Fiyat: {mesaj['original_price']}\n"
                f"İndirimli Fiyat: {mesaj['final_price']}\n\n"
                f"İndirim: {mesaj['discount']}\n"
                f"👉 <a href='{mesaj['url']}'>Steam Sayfasına Git</a>"
            ),
            parse_mode="HTML"   
        )