import os
import requests
import pandas as pd
import mplfinance as mpf
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# API Keys
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY = os.getenv("TWELVE_DATA_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Vibe-Trading Active! Manik, ebar /check dilei ami pro-chart pathabo.")

async def check_market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Twelve Data theke market scan korchi... Chart toiri hochhe.")
    
    # Bot top Indian stock auto pick korbe (Reliance sample)
    symbol = "RELIANCE:NSE" 
    
    try:
        # API theke data neoa
        url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=5min&outputsize=50&apikey={API_KEY}"
        response = requests.get(url).json()
        
        if "values" not in response:
            await update.message.reply_text("API Limit ba connection error. Twelve Data key thik achhe to?")
            return

        # Data-ke table format-e ana
        df = pd.DataFrame(response["values"])
        df['datetime'] = pd.to_datetime(df['datetime'])
        df = df.set_index('datetime')
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = df[col].astype(float)
        
        # Column name thik kora mplfinance-er jonno
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        df = df.iloc[::-1] # Purono theke notun-e sajano

        # Candlestick Chart with Moving Average
        mpf.plot(df, type='candle', style='charles', 
                 title=f"PRO VIEW: {symbol}",
                 ylabel='Price (INR)',
                 mav=(9), 
                 savefig='pro_chart.png')

        price = df['Close'].iloc[-1]
        caption = (f"🚀 **INTRADAY PICK: {symbol}**\n\n"
                   f"💰 Price: ₹{price:.2f}\n"
                   f"📈 Signal: RSI & MA Check koro (Lal-Sobuj Candle)\n"
                   f"🎯 Target: ₹{price * 1.01:.2f}\n"
                   f"🛑 Stoploss: ₹{price * 0.995:.2f}\n\n"
                   f"Manik, chart-er bheti-te SMA line-ta track koro.")

        with open("pro_chart.png", "rb") as photo:
            await update.message.reply_photo(photo=photo, caption=caption, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"System Error: {str(e)}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check_market))
    app.run_polling()

if __name__ == "__main__":
    main()
    
