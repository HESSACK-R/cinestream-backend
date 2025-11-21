# cinestream/backend/telegram_bot/bot.py
import asyncio
from django.conf import settings
from telegram import Bot
from telegram.constants import ParseMode

# Lire les variables d’environnement depuis settings.py
TELEGRAM_TOKEN = settings.TELEGRAM_BOT_TOKEN
ADMIN_CHAT_ID = settings.TELEGRAM_CHAT_ID


def get_bot():
    """Retourne le bot Telegram ou None si token invalide."""
    if not TELEGRAM_TOKEN:
        print("⚠️ TELEGRAM_TOKEN manquant dans settings.py")
        return None
    return Bot(token=TELEGRAM_TOKEN)


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
        loop = asyncio.get_event_loop()
        loop.create_task(send_telegram_notification_async(chat_id, message))
    except Exception as e:
        print(f"⚠️ Erreur envoi sync ({chat_id}) : {e}")


def notify_admin(message):
    if not ADMIN_CHAT_ID:
        print("⚠️ ADMIN_CHAT_ID manquant dans settings.py")
        return

    print("\n📡 [SYSTEM] Envoi de notification à l’admin…")
    send_telegram_notification(ADMIN_CHAT_ID, message)
