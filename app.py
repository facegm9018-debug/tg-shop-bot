import os
import asyncio
import threading
from flask import Flask, request
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message

BOT_TOKEN = os.getenv("BOT_TOKEN")
EPAY_SECRET = os.getenv("EPAY_SECRET")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set")

if not EPAY_SECRET:
    raise ValueError("EPAY_SECRET not set")

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)

dp = Dispatcher()
app = Flask(__name__)


# =======================
# TELEGRAM HANDLERS
# =======================

@dp.message()
async def start_handler(message: Message):
    if message.text == "/start":
        await message.answer(
            "🔥 Добро пожаловать!\n\n"
            "💎 Proxy (10 шт) — 15$\n"
            "🌐 Dolphin Anty (1 месяц) — 40$\n\n"
            "Напишите, что хотите купить."
        )


# =======================
# PAYMENT WEBHOOK
# =======================

@app.route("/payment_notify", methods=["POST"])
def payment_notify():
    data = request.json

    if not data:
        return "No data", 400

    if data.get("api_key") != EPAY_SECRET:
        return "Unauthorized", 403

    if data.get("status") == "paid":
        user_id = data.get("order_id")

        if user_id:
            asyncio.run(
                bot.send_message(
                    chat_id=int(user_id),
                    text="✅ Оплата получена!\n\nСпасибо за покупку 🚀"
                )
            )

    return "OK", 200


@app.route("/")
def home():
    return "Bot is running ✅"


# =======================
# RUN TELEGRAM BOT
# =======================

def start_bot():
    asyncio.run(dp.start_polling(bot))


if __name__ == "__main__":
    threading.Thread(target=start_bot).start()
    app.run(host="0.0.0.0", port=10000)
