from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Don’t hardcode, use env variable on Render
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

app = Flask(__name__)

telegram_app = Application.builder().token(BOT_TOKEN).build()

# Bot command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Received /start from:", update.effective_user.first_name)
    await update.message.reply_text("👋 Hello! I'm running via webhook on Render!")

# Bot command: /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ℹ️ Use /start to test me.")

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("help", help_command))

# This route is called by Telegram when a new message arrives
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    await telegram_app.process_update(update)
    return "ok"

# Setup webhook when Flask starts
@app.route("/setup-webhook", methods=["GET"])
def setup_webhook():
    telegram_app.bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")
    return "✅ Webhook has been set!"

# Optional health check route
@app.route("/", methods=["GET"])
def index():
    return "🤖 Telegram bot is alive!"

if __name__ == "__main__":
    print("🌐 Visit /setup-webhook to register your Telegram webhook.")
    app.run(port=5000)
