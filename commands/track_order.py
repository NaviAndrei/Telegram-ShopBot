from telegram import Update
from telegram.ext import CallbackContext

orders = {}


async def track_order(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("Please provide an order ID.")
        # return

    order_id = context.args[0]
    order = orders.get(order_id)

    if order and order['user_id'] == update.effective_user.id:  # Ensure users can only track their own orders
        status = order['status']
        await update.message.reply_text(f"Your order {order_id} is currently {status}.")
    else:
        await update.message.reply_text("Order not found or access denied.")
