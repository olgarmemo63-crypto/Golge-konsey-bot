import os
from google import genai
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

async def cevap_ver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        mesaj = update.message.text

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=mesaj
        )

        await update.message.reply_text(response.text)

    except Exception as e:
        await update.message.reply_text(f"Hata oluştu:\n{e}")

app = Application.builder().token(TELEGRAM_TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, cevap_ver)
)

print("🤖 Gölge Konsey Bot aktif!")

app.run_polling()
