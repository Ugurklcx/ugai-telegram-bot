from telegram import Update
from telegram.ext import ContextTypes
from services.steam_service import get_steam_tr_deals
import logging

logger = logging.getLogger(__name__)

async def steam_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1. İstek butondan mı yoksa yazılı komuttan mı geldi kontrol et
    target_message = update.message if update.message else update.callback_query.message

    indirimler = await get_steam_tr_deals()

    if not indirimler:
        await target_message.reply_text("❌ Şu an herhangi bir Steam indirimi bulunamadı.")
        return

    await target_message.reply_text("⏳ Steam fırsatları getiriliyor, lütfen bekleyin...")
    
    for mesaj in indirimler:
        caption_text = (
            f"<b>{mesaj['name']}</b>\n"
            f"Orijinal Fiyat: {mesaj['original_price']}\n"
            f"İndirimli Fiyat: {mesaj['final_price']}\n\n"
            f"İndirim: {mesaj['discount']}\n"
            f"👉 <a href='{mesaj['url']}'>Steam Sayfasına Git</a>"
        )
        
        image_url = mesaj.get("image_url")

        # Görsel URL'si geçerli mi kontrol edip göndermeyi dene
        if image_url:
            try:
                await target_message.reply_photo(
                    photo=image_url,
                    caption=caption_text,
                    parse_mode="HTML"
                )
                continue
            except Exception as e:
                logger.warning(f"Görsel gönderilemedi, metin olarak atılıyor: {e}")

        # Görsel yoksa veya yüklenirken Hata (BadRequest) verirse yedek mesaj
        await target_message.reply_text(
            text=caption_text,
            parse_mode="HTML",
            disable_web_page_preview=False
        )