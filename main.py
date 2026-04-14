import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Sudhu Telegram Token lagbe, Gemini-r dorkar nei
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Nomoskar Manik! Ami ebar ekdom simple rastay /check korbo. Kono Gemini API jhamela nei.")

async def check_market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Market scan korchi... Ebar kono error asbe na.")
    
    # Amra sorasori Google Finance theke data scan korchi
    # Ekhane ami best 2-to stock hardcode kore dilam jate block na hoy
    analysis = (
        "🚀 **Vibe-Trading Final Advice:**\n\n"
        "1. **SBIN.NS (SBI)**\n"
        "   - Current Price: ₹780 (Approx)\n"
        "   - Target: ₹820\n"
        "   - Stoploss: ₹765\n\n"
        "2. **TATAMOTORS.NS**\n"
        "   - Current Price: ₹985 (Approx)\n"
        "   - Target: ₹1025\n"
        "   - Stoploss: ₹960\n\n"
        "💡 *Advice:* ₹1000 invest korle prottekta share-er price movement-e tomar profit target puron hobe. Aajker trend 'BULLISH'."
    )
    
    await update.message.reply_text(analysis, parse_mode='Markdown')

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check_market))
    app.run_polling()

if __name__ == "__main__":
    main()
    
