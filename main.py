import os
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Token setup
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Nomoskar Manik! /check dile ami SBIN-er live Intraday chart ar prediction pathabo.")

async def check_market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    symbol = "SBIN.NS"
    await update.message.reply_text(f"Dhorjo dhoro Manik, {symbol}-er live chart banachhi...")
    
    try:
        # Data fetch kora (Intraday-r jonno 5 minute interval best)
        data = yf.download(symbol, period="1d", interval="5m")
        
        if data.empty:
            await update.message.reply_text("Market ekhon bondho ba data pawa jachhe na.")
            return

        # Chart Design
        plt.style.use('dark_background') # Trading-er moto dark theme
        plt.figure(figsize=(10, 6))
        plt.plot(data.index, data['Close'], color='#00ff00', linewidth=2)
        plt.fill_between(data.index, data['Close'], color='#00ff00', alpha=0.1)
        plt.title(f"{symbol} Intraday Live View", fontsize=15)
        plt.grid(True, linestyle='--', alpha=0.5)
        
        plt.savefig("chart.png")
        plt.close()
        
        # Simple Intraday Logic
        price = float(data['Close'].iloc[-1])
        msg = (f"📈 *INTRADAY SIGNAL*\n\n"
               f"🏦 *Stock:* {symbol}\n"
               f"💰 *Current Price:* ₹{price:.2f}\n"
               f"🎯 *Target:* ₹{price + 4:.2f}\n"
               f"🛑 *Stoploss:* ₹{price - 3:.2f}\n\n"
               f"💡 *Manik-er jonno Tips:* Intraday-te 3:15 PM-er age trade bondho kore debe!")

        with open("chart.png", "rb") as photo:
            await update.message.reply_photo(photo=photo, caption=msg, parse_mode='Markdown')
            
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check_market))
    app.run_polling()

if __name__ == "__main__":
    main()
    
