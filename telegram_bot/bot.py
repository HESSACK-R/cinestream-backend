# cinestream/backend/telegram_bot/bot.py
import asyncio
import os
from telegram import Bot
from telegram.constants import ParseMode

# Charger les variables d’environnement
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

def get_bot():
    """Crée une instance du bot seulement lorsque nécessaire."""
    token = TELEGRAM_TOKEN
    if not token:
        print("⚠️ TELEGRAM_TOKEN manquant dans .env")
        return None
    return Bot(token=token)


async def send_telegram_notification_async(chat_id, message):
    bot = get_bot()
    if not bot:
        return
    
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN_V2,
            disable_web_page_preview=True
        )
        print(f"✅ Message Telegram envoyé à {chat_id}")
    except Exception as e:
        print(f"⚠️ Erreur Telegram ({chat_id}) : {e}")


def send_telegram_notification(chat_id, message):
    try:
        asyncio.run(send_telegram_notification_async(chat_id, message))
    except RuntimeError:
        # Cas : boucle event déjà en cours
        loop = asyncio.get_event_loop()
        loop.create_task(send_telegram_notification_async(chat_id, message))
    except Exception as e:
        print(f"⚠️ Erreur envoi sync ({chat_id}) : {e}")


def notify_admin(message):
    if not ADMIN_CHAT_ID:
        print("⚠️ ADMIN_CHAT_ID introuvable dans .env")
        return

    print("\n📡 [SYSTEM] Envoi de notification à l’admin…")
    send_telegram_notification(ADMIN_CHAT_ID, message)
