import os
import time
import yfinance as yf
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# API Keys setup
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_KEY)

# Ami list-ta ektu choto korlam jate block na hoy
STOCKS_TO_WATCH = ["^NSEI", "SBIN.NS", "TATAMOTORS.NS", "RELIANCE.NS"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Nomoskar Manik! /check command dile ami Nifty ar top stocks scan korbo.")

async def check_market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Market scan korchi... Please 20-30 second dhorjo dhoro.")
    
    recommendations = []
    
    for symbol in STOCKS_TO_WATCH:
        try:
            # Code-ke ektu thamabo jate Yahoo block na kore
            time.sleep(2) 
            
            # Data fetch kora
            data = yf.download(symbol, period="2d", interval="1h", progress=False)
            
            if not data.empty:
                # Latest price ber kora
                price = float(data['Close'].iloc[-1])
                name = "NIFTY 50" if symbol == "^NSEI" else symbol
                
                # Gemini AI Analysis
                model = genai.GenerativeModel('gemini-pro')
                prompt = (f"Market Item: {name}, Current Price: {price}. User wants to invest 1000 INR for 50-100 profit. "
                          f"Give simple Bengali advice: Buy/Wait with Target/Stoploss. Focus on safety.")
                
                response = model.generate_content(prompt)
                recommendations.append(f"📌 *{name}*\n💰 Price: ₹{price:.2f}\n💡 Advice: {response.text}")
            
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            continue

    if recommendations:
        final_msg = "\n\n---\n\n".join(recommendations)
        await update.message.reply_text(f"🚀 *Market Analysis:*\n\n{final_msg}", parse_mode='Markdown')
    else:
        await update.message.reply_text("Yahoo Finance ekhon data block korche. 10 minute pore abar try koro.")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check_market))
    app.run_polling()

if __name__ == "__main__":
    main()
    
