import os
import yfinance as yf
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# API Keys setup
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_KEY)

# Top Indian Stocks to scan automatically
STOCKS_TO_WATCH = ["SBIN.NS", "TATAMOTORS.NS", "RELIANCE.NS", "ITC.NS", "HDFCBANK.NS", "INFY.NS"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Nomoskar Manik! Trading-e zero knowledge thakleo chinta nei.\n\n"
        "Tumi sudhu /check command-ta dao, ami top Indian stocks scan kore ₹1000 investment-er jonno bhalo option khunje debo."
    )

async def check_market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Dhorjo dhoro Manik, ami market scan korchi... Ete 10-15 second somoy lagte pare.")
    
    recommendations = []
    
    for symbol in STOCKS_TO_WATCH:
        try:
            stock = yf.Ticker(symbol)
            df = stock.history(period="5d", interval="1h")
            if df.empty: continue
            
            price = df['Close'].iloc[-1]
            
            # AI logic for each stock
            model = genai.GenerativeModel('gemini-pro')
            prompt = (f"Stock: {symbol}, Current Price: {price}. User wants to invest 1000 INR for 50-100 profit. "
                      f"If this stock looks good to buy today, give clear Target and Stoploss in Bengali. "
                      f"If not good, say 'Wait'. Keep it very simple for a beginner.")
            
            response = model.generate_content(prompt)
            recommendations.append(f"📊 *Stock: {symbol}*\n💰 Price: ₹{price:.2f}\n🤖 Advice: {response.text}\n")
        except:
            continue

    final_msg = "\n---\n".join(recommendations) if recommendations else "Market data ekhon pawa jachhe na. Pore chesta koro."
    await update.message.reply_text(f"🚀 *Aajker Prediction:*\n\n{final_msg}", parse_mode='Markdown')

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check_market))
    app.run_polling()

if __name__ == "__main__":
    main()
    
