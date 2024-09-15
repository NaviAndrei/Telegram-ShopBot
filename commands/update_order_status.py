from telegram import Update
from telegram.ext import CallbackContext
from utils.is_admin import is_admin

orders = {}


async def update_order_status(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("You are not authorized to use this command.")
        return

    if len(context.args) < 2:
        await update.message.reply_text("Usage: /update_order_status <order_id> <new_status>")
        return

    order_id, new_status = context.args[0], ' '.join(context.args[1:])
    order = orders.get(order_id)

    if order:
        order['status'] = new_status
        # Notify the user
        await context.bot.send_message(chat_id=order['user_id'],
                                       text=f"Your order {order_id} status has been updated to: {new_status}.")
        await update.message.reply_text(f"Order {order_id} status updated to {new_status}.")
    else:
        await update.message.reply_text("Order not found.")