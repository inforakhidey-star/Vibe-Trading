import os
import yfinance as yf
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# API Keys setup
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_KEY)

# Top Indian Stocks
STOCKS_TO_WATCH = ["SBIN.NS", "TATAMOTORS.NS", "RELIANCE.NS", "ITC.NS", "HDFCBANK.NS", "INFY.NS"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Nomoskar Manik! Trading-e zero knowledge thakleo chinta nei.\n\n"
        "Tumi sudhu /check command-ta dao, ami top Indian stocks scan kore ₹1000 investment-er jonno bhalo option khunje debo."
    )

async def check_market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Dhorjo dhoro Manik, ami live market scan korchi...")
    
    recommendations = []
    
    for symbol in STOCKS_TO_WATCH:
        try:
            # Data fetch optimization
            stock = yf.download(symbol, period="5d", interval="1h", progress=False)
            if stock.empty:
                continue
            
            price = float(stock['Close'].iloc[-1])
            
            # AI Decision Logic
            model = genai.GenerativeModel('gemini-pro')
            prompt = (f"Stock: {symbol}, Current Price: {price}. User wants to invest 1000 INR for 50-100 profit. "
                      f"Give clear advice: Buy (if good) or Wait (if bad). "
                      f"If Buy, give Target and Stoploss in simple Bengali. Keep it very short.")
            
            response = model.generate_content(prompt)
            recommendations.append(f"📊 *Stock: {symbol}*\n💰 Current Price: ₹{price:.2f}\n🤖 AI Advice: {response.text}\n")
        except Exception as e:
            print(f"Error for {symbol}: {e}")
            continue

    if recommendations:
        final_msg = "\n---\n".join(recommendations)
        await update.message.reply_text(f"🚀 *Aajker Prediction:*\n\n{final_msg}", parse_mode='Markdown')
    else:
        # Jodi asholei data na pay, tokhon ei message asbe
        await update.message.reply_text("Market data fetch korte somoshya hochhe. Ektu pore /check command-ta abar dao.")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check_market))
    app.run_polling()

if __name__ == "__main__":
    main()
    
