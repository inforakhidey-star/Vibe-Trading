import os
import yfinance as yf
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# API Keys setup
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Nomoskar Manik! Ami ready. /predict [Stock Name] likhe pathao. Example: /predict TATAMOTORS.NS")

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Stock-er naam dao (Example: /predict SBIN.NS)")
        return
    symbol = context.args[0].upper()
    await update.message.reply_text(f"Dhorjo dhoro Manik, ami {symbol} analysis korchi...")
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period="5d", interval="1h")
        price = df['Close'].iloc[-1]
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Stock: {symbol}, Current Price: {price}. User wants to invest 1000 INR for 50-100 profit. Give clear Buy/Sell advice with Target and Stoploss in simple Bengali language."
        response = model.generate_content(prompt)
        await update.message.reply_text(f"📊 *{symbol} Analysis*\n💰 Current Price: ₹{price:.2f}\n\n🤖 *AI Advice:* \n{response.text}", parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"Error: Symbol-ta thik achhe to? (NSE stock hole .NS lagao)")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("predict", predict))
    app.run_polling()

if __name__ == "__main__":
    main()
  
