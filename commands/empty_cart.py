from telegram import Update
from telegram.ext import CallbackContext

carts = {}


async def empty_cart(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    carts[user_id] = []
    await update.message.reply_text("Your cart has been emptied.")
