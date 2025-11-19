# cinestream/backend/telegram_bot/bot.py
import os
import asyncio
from telegram import Bot
from telegram.constants import ParseMode

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))

bot = Bot(token=TELEGRAM_TOKEN)

async def send_telegram_notification_async(chat_id, message):
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
        print(f"✅ Message Telegram envoyé à {chat_id}")
    except Exception as e:
        print(f"⚠️ Erreur Telegram ({chat_id}) : {e}")

def send_telegram_notification(chat_id, message):
    try:
        asyncio.run(send_telegram_notification_async(chat_id, message))
    except Exception as e:
        print(f"⚠️ Erreur envoi sync ({chat_id}) : {e}")

def notify_admin(message):
    print("\n📡 Envoi de notification Telegram...")
    send_telegram_notification(ADMIN_CHAT_ID, message)
