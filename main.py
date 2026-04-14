import os
import requests
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# API Keys
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_KEY)

# Top Stocks List
STOCKS = ["RELIANCE", "SBIN", "TATAMOTORS", "ITC", "HDFCBANK", "INFY"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Nomoskar Manik! Ami Vibe-Trading Agent. /top2 trade jante /check likho.")

async def check_market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Market scan korchi... Ami sudhu best 2-to trade khunje ber korbo.")
    
    # Ekhane amra agent-er moto bhabchi
    prompt = f"""
    Act as a Vibe-Trading Agent. I will give you a list of Indian stocks: {STOCKS}.
    Search for their current live price and market trend (Bullish/Bearish).
    Give me ONLY the top 2 best stocks where I can invest 1000 INR to get 50-100 profit.
    Format your answer like this:
    1. Stock Name
    2. Buy Price
    3. Target (Profit)
    4. Stoploss (Safety)
    Language: Simple Bengali.
    """
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash') # Latest model
        response = model.generate_content(prompt)
        
        final_msg = f"🚀 **Vibe-Trading Agent Analysis:**\n\n{response.text}"
        await update.message.reply_text(final_msg, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check_market))
    app.run_polling()

if __name__ == "__main__":
    main()
    
