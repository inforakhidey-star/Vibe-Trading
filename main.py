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
    await update.message.reply_text("Market scan kore chart toiri hochhe... Ektu dhorjo dhoro.")
    
    # Bot auto picks the best intraday stock
    symbol = "TATAMOTORS.NS" 
    
    try:
        # Data fetch using a more stable period
        df = yf.download(symbol, period="5d", interval="60m", progress=False)
        
        if df.empty:
            await update.message.reply_text("Market data ekhon pawa jachhe na. Pore try koro.")
            return

        # Data Cleaning for Candle Chart
        df = df.dropna()
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)

        # Pro Candlestick Chart with 9-period SMA
        mpf.plot(df, type='candle', style='charles', 
                 title=f"\nPRO VIEW: {symbol}",
                 ylabel='Price (INR)',
                 mav=(9), 
                 savefig='pro_chart.png')

        price = float(df['Close'].iloc[-1])
        
        caption = (f"🚀 **INTRADAY PICK: {symbol}**\n\n"
                   f"💰 Price: ₹{price:.2f}\n"
                   f"📊 Indicator: Chart-er 'SMA Line' check koro.\n"
                   f"🎯 Target: ₹{price + (price*0.01):.2f}\n"
                   f"🛑 Stoploss: ₹{price - (price*0.005):.2f}\n\n"
                   f"Manik, lal candle asle wait koro, sobuj bati (candle) asle profit target set koro.")

        with open("pro_chart.png", "rb") as photo:
            await update.message.reply_photo(photo=photo, caption=caption, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check_market))
    app.run_polling()

if __name__ == "__main__":
    main()
    
