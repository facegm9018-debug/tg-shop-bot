import os
from flask import Flask, request
from aiogram import Bot
import asyncio

BOT_TOKEN = os.getenv("8159888762:AAEO8ZCZ0KiY9b6AIhcqiydgjatXSy7zkq0")
EPAY_SECRET = os.getenv("f7a2c9c697cfed5980fcea22e280c732997b33139fe1ce27a6de1116febfb525")

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

@app.route("/payment_notify", methods=["POST"])
def payment_notify():
    data = request.json

    if not data:
        return "No data", 400

    if data.get("api_key") != EPAY_SECRET:
        return "Unauthorized", 403

    if data.get("status") == "paid":
        user_id = data.get("order_id")

        asyncio.run(bot.send_message(
            chat_id=user_id,
            text="✅ Оплата получена! Спасибо за покупку."
        ))

    return "OK", 200
