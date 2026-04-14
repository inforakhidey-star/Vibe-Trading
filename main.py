import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# API Keys
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# Gemini Setup
genai.configure(api_key=GEMINI_KEY)

# Top Indian Stocks List for the Agent to Analyze
STOCKS_TO_SCAN = "Reliance, SBI, Tata Motors, ITC, HDFC Bank, Infosys"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Nomoskar Manik! Ami Vibe-Trading Agent.\n\n"
        "Tumi /check command-ta dao, ami market analysis kore best 2-to trade tomake bolbo."
    )

async def check_market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Dhorjo dhoro Manik, Vibe-Trading Agent market scan korche...")
    
    try:
        # We use 'gemini-pro' which is the most stable version
        model = genai.GenerativeModel('gemini-pro')
        
        # This prompt tells the agent exactly what to do
        prompt = f"""
        You are a professional Vibe-Trading Agent for the Indian Stock Market.
        Based on the current market sentiment for these stocks: {STOCKS_TO_SCAN}.
        Give me exactly 2 high-probability trades for a beginner with 1000 INR budget.
        For each trade, provide:
        1. Stock Name (NSE Symbol)
        2. Buy Price (Approx)
        3. Target Price (for 50-100 profit)
        4. Stoploss (for safety)
        
        Rules: Give clear advice in simple Bengali. Use bullet points.
        """
        
        response = model.generate_content(prompt)
        
        final_msg = f"🚀 **Vibe-Trading Agent's Top Picks:**\n\n{response.text}"
        await update.message.reply_text(final_msg, parse_mode='Markdown')
        
    except Exception as e:
        await update.message.reply_text(f"Kothao vul hoyeche! Error: {str(e)}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check_market))
    app.run_polling()

if __name__ == "__main__":
    main()
    
