import os
import requests
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# API Keys setup
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
ALPHA_KEY = os.getenv("ALPHA_VANTAGE_KEY")

genai.configure(api_key=GEMINI_KEY)

# Top Indian Stocks (Alpha Vantage formatting)
STOCKS = {"SBIN": "BSE:SBIN", "TATA": "BSE:TATAMOTORS", "RELIANCE": "BSE:RELIANCE"}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Nomoskar Manik! Alpha Vantage API ready. /check dile ami scan korbo.")

async def check_market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Market data fetch korchi Alpha Vantage theke...")
    
    recommendations = []
    
    for name, symbol in STOCKS.items():
        try:
            # Alpha Vantage API URL
            url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_KEY}'
            r = requests.get(url)
            data = r.json()
            
            # Extract price from JSON
            price = data.get("Global Quote", {}).get("05. price")
            
            if price:
                model = genai.GenerativeModel('gemini-pro')
                prompt = (f"Stock: {name}, Price: {price}. User wants 50-100 profit on 1000 investment. "
                          f"Give simple Bengali advice: Buy/Wait with Target/Stoploss.")
                
                response = model.generate_content(prompt)
                recommendations.append(f"📌 *{name}*\n💰 Price: ₹{float(price):.2f}\n💡 Advice: {response.text}")
            
        except Exception as e:
            continue

    if recommendations:
        await update.message.reply_text("\n\n---\n\n".join(recommendations), parse_mode='Markdown')
    else:
        await update.message.reply_text("Alpha Vantage thekeo data pawa jachhe na. API limit check koro.")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check_market))
    app.run_polling()

if __name__ == "__main__":
    main()
    
