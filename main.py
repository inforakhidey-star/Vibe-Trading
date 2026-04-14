import os
import yfinance as yf
import pandas as pd
import mplfinance as mpf
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Vibe-Trading Active! Manik, /check dile ami pro-chart ar signal pathabo.")

async def check_market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Market scan korchi... Pro-Candle chart toiri hochhe.")
    
    # Bot automatically picks the most active stock
    symbol = "TATAMOTORS.NS" 
    
    try:
        # Data fetch
        df = yf.download(symbol, period="1d", interval="5m", progress=False)
        
        if df.empty:
            await update.message.reply_text("Bazar ekhon bondho, tai data pawa jachhe na.")
            return

        # ERROR FIX: Data cleaning for mplfinance
        df = df.dropna() # Faka gulo muche phela
        # Multi-level index thakle seta ke single level kora
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        # Float-e convert kora jate 'Open' column error na dey
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)

        # Candle Chart with Indicator (Moving Average)
        mpf.plot(df, type='candle', style='charles', 
                 title=f"\nPRO VIEW: {symbol}",
                 ylabel='Price (INR)',
                 mav=(9), # 9-day Moving Average line
                 savefig='pro_chart.png')

        price = float(df['Close'].iloc[-1])
        
        # Intraday Trading Details
        caption = (f"🚀 **BEST INTRADAY PICK: {symbol}**\n\n"
                   f"💰 Current Price: ₹{price:.2f}\n"
                   f"📈 Signal: Indicators check koro (9-SMA line)\n"
                   f"🎯 Target: ₹{price + (price*0.01):.2f}\n"
                   f"🛑 Stoploss: ₹{price - (price*0.005):.2f}\n\n"
                   f"Manik, chart-e candle-gulo jodi liner upore thake, tobe kinte paro.")

        with open("pro_chart.png", "rb") as photo:
            await update.message.reply_photo(photo=photo, caption=caption, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"Ekhono ektu somoshya hochhe: {str(e)}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check_market))
    app.run_polling()

if __name__ == "__main__":
    main()
    
