import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

async def cevap_ver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mesaj = update.message.text
    cevap = model.generate_content(mesaj)
    await update.message.reply_text(cevap.text)

app = Application.builder().token(TELEGRAM_TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, cevap_ver)
)

print("Bot aktif!")

app.run_polling()
