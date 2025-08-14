from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Message
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
import asyncio
from datetime import datetime, timedelta
import os
from keep_alive import keep_alive

# Ambil dari environment variable Railway
TOKEN = os.environ.get("7710185509:AAFlgVIfajRTHkfo6VQbg1Uh-DAaA4lVlp4")
ADMIN_ID = int(os.environ.get("6141653876", 0))

channel_links = {
    "vip": "https://t.me/+t8dheeuon3Q5ZGNl",
    "inews": "https://t.me/+WqSrSVNTJlJjMGJl",
    "tradergp": "https://t.me/rynfxtrader"
}

usage_tracker = {}

BASE_VIDEO_PATH = os.path.join(os.path.dirname(__file__), "videos")

async def send_video_safe(context, chat_id, filename, delay=5):
    filepath = os.path.join(BASE_VIDEO_PATH, filename)
    if os.path.exists(filepath):
        with open(filepath, "rb") as video_file:
            msg_video: Message = await context.bot.send_video(chat_id=chat_id, video=video_file)
            await asyncio.sleep(delay)
            await msg_video.delete()
    else:
        await context.bot.send_message(chat_id=chat_id, text=f"❌ File '{filename}' tidak ditemukan!")

async def bot_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    now = datetime.now()
    usage = usage_tracker.get(user_id, {"count": 0, "reset": now + timedelta(hours=1)})

    if now >= usage["reset"]:
        usage = {"count": 0, "reset": now + timedelta(hours=1)}

    if usage["count"] >= 3:
        sisa = usage["reset"] - now
        msg = await update.message.reply_text(f"⚠️ Waktu kamu habis. Coba lagi dalam {sisa.seconds // 60} menit.")
        await asyncio.sleep(3)
        await msg.delete()
        await update.message.delete()
        return

    usage["count"] += 1
    usage_tracker[user_id] = usage

    keyboard = [
        [InlineKeyboardButton("VIP 🔥", callback_data="vip")],
        [InlineKeyboardButton("iNews 💯", callback_data="inews")],
        [InlineKeyboardButton("Trader GP 📈", callback_data="tradergp")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    notif = await update.message.reply_text("🔐 Menu Utama...")
    msg = await update.message.reply_text("Pilihan 🤖", reply_markup=reply_markup)
    await asyncio.sleep(2)
    await notif.delete()
    await update.message.delete()

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    channel = channel_links.get(query.data)
    if channel:
        keyboard = [[InlineKeyboardButton("🔗 Masuk Sekarang", url=channel)]]
        rep = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text("🔐 Klik tombol berikut untuk masuk:", reply_markup=rep)
        await asyncio.sleep(2)
        await query.message.delete()

async def secret_word_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    user_id = update.effective_user.id
    now = datetime.now()
    usage = usage_tracker.get(user_id, {"count": 0, "reset": now + timedelta(hours=1)})

    if now >= usage["reset"]:
        usage = {"count": 0, "reset": now + timedelta(hours=1)}

        keyboard = [
            [InlineKeyboardButton("📁 Rahasia 1", callback_data="vip")],
            [InlineKeyboardButton("📁 Rahasia 2", callback_data="inews")],
            [InlineKeyboardButton("📁 Rahasia 3", callback_data="tradergp")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        msg_menu = await update.message.reply_text("🕵️ MENU RAHASIA 🕵️", reply_markup=reply_markup)
        await send_video_safe(context, update.effective_chat.id, "model.mp4", delay=5)

        await asyncio.sleep(4)
        await msg_menu.delete()
        await update.message.delete()
        return
    
    if text.startswith("video "):
        if user_id != ADMIN_ID:
            msg = await update.message.reply_text("⛔️ Fitur ini hanya untuk admin.")
            await asyncio.sleep(3)
            await msg.delete()
            await update.message.delete()
            return

        nama = text.replace("video ", "").strip()
        filename = f"{nama}.mp4"
        await send_video_safe(context, user_id, filename, delay=8)
        await update.message.delete()
        return

    if text in ["keren:1122", "bagus:1122", "baik:1122"]:
        usage_tracker[user_id] = {"count": 0, "reset": now + timedelta(hours=1)}
        keyboard = [
            [InlineKeyboardButton("VIP 🔥", callback_data="vip")],
            [InlineKeyboardButton("iNews 💯", callback_data="inews")],
            [InlineKeyboardButton("Trader GP 📈", callback_data="tradergp")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        msg = await update.message.reply_text("🤖 Menu rahasia aktif kembali!", reply_markup=reply_markup)
        await asyncio.sleep(3)
        await msg.delete()
        await update.message.delete()
        return

    if text == "mantap":
        markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("🚀Mantap", url="https://t.me/+_XcdDWYZDQhhZTA1")]]
        )
        msg = await update.message.reply_text("🔓Aktif kembali:", reply_markup=markup)
        await asyncio.sleep(3)
        await msg.delete()
        await update.message.delete()
        return

    if text == "botstart":
        keyboard = [
            [InlineKeyboardButton("VIP 🔥", callback_data="vip")],
            [InlineKeyboardButton("iNews 💯", callback_data="inews")],
            [InlineKeyboardButton("Trader GP 📈", callback_data="tradergp")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        notif = await update.message.reply_text("🕒 Akses cepat melalui kata 'wak'...")
        msg = await update.message.reply_text("🤖 Menu Utama 🤖", reply_markup=reply_markup)
        await asyncio.sleep(3)
        await notif.delete()
        await msg.delete()
        await update.message.delete()
        return

    msg = await update.message.reply_text("❓ Ketik /botstart untuk menampilkan menu.")
    await asyncio.sleep(5)
    await msg.delete()
    await update.message.delete()

def main():
    keep_alive()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("botstart", bot_start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, secret_word_check))
    print("🤖 BOT AKTIF...")
    app.run_polling()

if __name__ == "__main__":
    main()
  
