from telegram import Update
from telegram.ext import CallbackContext


async def send_chat_id(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Your chat ID is {chat_id}")
