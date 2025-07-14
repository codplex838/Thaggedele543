from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# If you're using this only in Termux, you can put the token directly here:
BOT_TOKEN = "7313598031:AAH-nxgICvUa2mNxGni043bq-u4QfXfJXUQ"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Received /start from:", update.effective_user.first_name)
    await update.message.reply_text("👋 Hello! I am alive and running in Termux!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /start to test me.")

if __name__ == "__main__":
    print("🤖 Starting bot...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    print("✅ Bot is now polling... waiting for messages.")
    app.run_polling()