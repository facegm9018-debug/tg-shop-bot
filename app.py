import os
from flask import Flask, request
from aiogram import Bot
import asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")
EPAY_SECRET = os.getenv("EPAY_SECRET")

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
