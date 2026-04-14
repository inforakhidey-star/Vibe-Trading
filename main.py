import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# API Keys setup
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# Gemini Setup - Version specify kore deya holo
genai.configure(api_key=GEMINI_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Nomoskar Manik! Ami Vibe-Trading Agent.\n\n"
        "Tumi sudhu /check command-ta dao, ami market analysis kore best 2-to trade bolbo."
    )

async def check_market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Vibe-Trading Agent market scan korche... Ektu dhorjo dhoro.")
    
    try:
        # Latest Stable Model: gemini-1.5-flash
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = """
        You are a professional Vibe-Trading Agent. 
        Scan the Indian stock market sentiment right now.
        Pick exactly 2 stocks for a 1000 INR investment with 50-100 INR profit target.
        Give the output in this format in Bengali:
        1. Stock Name (NSE Symbol)
        2. Current Price (Approx)
        3. Target & Stoploss
        4. Why this stock? (Reason)
        Keep it simple for a beginner.
        """
        
        response = model.generate_content(prompt)
        
        final_msg = f"🚀 **Vibe-Trading Agent's Picks:**\n\n{response.text}"
        await update.message.reply_text(final_msg, parse_mode='Markdown')
        
    except Exception as e:
        # Jodi 1.5-flash o na pay, tobe gemini-1.0-pro try korbe automatically
        try:
            model = genai.GenerativeModel('gemini-1.0-pro')
            response = model.generate_content(prompt)
            await update.message.reply_text(f"🚀 **Vibe-Trading Agent's Picks:**\n\n{response.text}", parse_mode='Markdown')
        except Exception as e2:
            await update.message.reply_text(f"Error: {str(e2)}. API settings-e somoshya achhe.")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check_market))
    app.run_polling()

if __name__ == "__main__":
    main()
    
