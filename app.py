import os
import asyncio
from flask import Flask, request
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

# Получаем переменные окружения из Render
BOT_TOKEN = os.getenv("BOT_TOKEN")
EPAY_SECRET = os.getenv("EPAY_SECRET")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set in environment variables")

if not EPAY_SECRET:
    raise ValueError("EPAY_SECRET not set in environment variables")

# Создаем бота (новый способ для aiogram 3.7+)
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)

app = Flask(__name__)

# Проверка, что сервис работает
@app.route("/")
def home():
    return "Bot is running ✅"

# Webhook от E-PAY
@app.route("/payment_notify", methods=["POST"])
def payment_notify():
    data = request.json

    if not data:
        return "No data", 400

    # Проверка API-ключа
    if data.get("api_key") != EPAY_SECRET:
        return "Unauthorized", 403

    # Проверяем статус оплаты
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


# Для локального запуска (не обязательно для Render)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
