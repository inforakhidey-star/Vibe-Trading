import os
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Token setup
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Nomoskar Manik! /check dile ami live chart ar prediction pathabo.")

async def check_market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    symbol = "SBIN.NS" # Amra default SBI check korbo
    await update.message.reply_text(f"Dhorjo dhoro, {symbol}-er live chart banachhi...")
    
    try:
        # 1. Data neoa
        data = yf.download(symbol, period="1d", interval="5m")
        
        # 2. Chart toiri kora (Matplotlib use kore)
        plt.figure(figsize=(10, 5))
        plt.plot(data['Close'], label='Price', color='blue')
        plt.title(f"{symbol} Live Chart")
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.grid(True)
        plt.savefig("chart.png") # Photo save holo
        plt.close()
        
        # 3. Prediction Text
        price = data['Close'].iloc[-1]
        msg = (f"📊 *Stock:* {symbol}\n"
               f"💰 *Live Price:* ₹{price:.2f}\n"
               f"🚀 *Advice:* Intraday Buy koro ₹1000 invest kore.\n"
               f"🎯 *Target:* ₹{price+5:.2f}\n"
               f"🛑 *Stoploss:* ₹{price-3:.2f}")

        # 4. Telegram-e Photo pathano
        with open("chart.png", "rb") as photo:
            await update.message.reply_photo(photo=photo, caption=msg, parse_mode='Markdown')
            
    except Exception as e:
        await update.message.reply_text("Chart toiri korte ektu somoshya holo. Pore chesta koro.")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check_market))
    app.run_polling()

if __name__ == "__main__":
    main()
