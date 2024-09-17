import logging
from telegram import Update
from telegram.ext import CallbackContext
from utils.is_admin import is_admin

orders = {}


async def send_order_photo(update: Update, context: CallbackContext):
    # Ensure update and update.message are not None
    if update is None or update.message is None:
        logging.error("Update or message is None")
        return  # Optionally send a message to the user

    try:
        user_id = update.effective_user.id

        if not is_admin(user_id):
            await update.message.reply_text("You are not authorized to use this command.")
            return

        if len(context.args) < 2:
            await update.message.reply_text("Usage: /send_order_photo <order_id> <photo_file_id_or_url> [caption]")
            return

        order_id = context.args[0]
        photo_source = context.args[1]
        caption = ' '.join(context.args[2:]) if len(context.args) > 2 else 'Your order is ready for pickup!'

        order = orders.get(order_id)
        if order:
            try:
                if photo_source.startswith("http"):
                    await context.bot.send_photo(chat_id=order['user_id'], photo=photo_source, caption=caption)
                else:
                    await context.bot.send_photo(chat_id=order['user_id'], photo=photo_source, caption=caption)
                await update.message.reply_text(f"Photo sent for order {order_id}.")
            except Exception as e:
                logging.error(f"Failed to send photo for order {order_id}: {e}")
                await update.message.reply_text(f"Failed to send photo for order {order_id}. Please try again.")
        else:
            await update.message.reply_text("Order not found.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        await update.message.reply_text("An unexpected error occurred. Please try again.")
