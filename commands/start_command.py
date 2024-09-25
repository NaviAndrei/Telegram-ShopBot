<<<<<<< HEAD
from telegram import Update
from telegram.ext import ContextTypes


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! I'm ShopBot. If you need help, use /help.")
=======
from telegram import Update
from telegram.ext import ContextTypes


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! I'm ShopBot. If you need help, use /help.")
>>>>>>> bd5b9ce1bcd5d4b5aba4265e011c85a738c39520
