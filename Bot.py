import os
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY = os.getenv("GEMINI_API_KEY")

URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

async def cevap_ver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mesaj = update.message.text

    veri = {
        "contents": [
            {
                "parts": [
                    {
                        "text": mesaj
                    }
                ]
            }
        ]
    }

    try:
        r = requests.post(URL, json=veri, timeout=30)
        r.raise_for_status()

        cevap = r.json()["candidates"][0]["content"]["parts"][0]["text"]

        await update.message.reply_text(cevap)

    except Exception as e:
        await update.message.reply_text(f"Hata:\n{e}")

app = Application.builder().token(TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, cevap_ver)
)

print("Bot çalışıyor...")

app.run_polling()
