import uuid
from telegram import Update
from telegram.ext import CallbackContext
from credentials import admin_user_ids, admin_chat_id


def is_admin(user_id):
    return user_id in admin_user_ids


async def notify_pickup(update: Update, context: CallbackContext):
    # Permission check
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("You are not authorized to use this command.")
        return

    # Check if there are enough arguments
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /notify_pickup <order_id> [latitude,longitude]")
        return

    # Check if there are enough arguments
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /notify_pickup <order_id> <latitude,longitude>")
        return

    order_id_str = context.args[0]
    location_str = context.args[1]

    # Validate order ID (check if it's a valid UUID)
    try:
        order_id = uuid.UUID(order_id_str)
    except ValueError:
        await update.message.reply_text("Invalid order ID. Please provide a valid UUID format order ID.")
        return

    # Validate and parse latitude and longitude
    try:
        latitude, longitude = map(float, location_str.split(','))
        maps_link = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"
    except ValueError:
        await update.message.reply_text("Invalid location format. Please provide in the format <latitude,longitude>.")
        return

    # Attempt to notify the user
    try:
        message = (
            f"Your order ({order_id}) is ready for pickup.\n"
            f"Please pick it up at this location: {maps_link}"
        )
        await update.message.reply_text(message)
        # Notify the admin that the location coords have been sent to the user
        await context.bot.send_message(chat_id=admin_chat_id, text=f"Notification sent to the user for order "
                                                                   f"ID {order_id}.")
    except Exception as e:
        # Notify the admin of the error
        await context.bot.send_message(chat_id=admin_chat_id, text=f"Failed to send notification for order"
                                                                   f" ID {order_id}. Error: {str(e)}")
    else:
        # Default pickup location: Tineretului Park
        latitude, longitude = 44.413381124302326, 26.104192740329374

    # # Fetch order from database
    # order = orders.get(order_id)
    # if not order:
    #     await update.message.reply_text("Order not found.")
    #     return

    # # Send notification to user
    # try:
    #     await context.bot.send_message(chat_id=order['user_id'],
    #                                    text=f"Your order {order_id} is ready for pickup. "
    #                                         f"Please pick it up at this location: "
    #                                         f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}")
    #     await update.message.reply_text(f"Notification sent for order {order_id}.")
    # except Exception as e:
    #     await update.message.reply_text(f"Failed to send notification. Error: {str(e)}")
