import json
import uuid
from telegram import Update
from telegram.ext import CallbackContext
from credentials import admin_chat_id

with open('utils/PRODUCTS.json', 'r') as file:
    PRODUCTS = json.loads(file.read())

ADMIN_CHAT_ID = admin_chat_id

carts = {}
orders = {}


async def checkout(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    cart = carts.pop(user_id, [])
    if not cart:
        await update.message.reply_text("Your cart is empty.")
        return

    # Generate a unique order ID and create an order entry
    order_id = str(uuid.uuid4())

    # Initialize total price and order details
    total_price = 0
    order_details = []

    for item in set(cart):  # Iterate through unique items in cart
        quantity = cart.count(item)
        product = next((p for p in PRODUCTS if p['id'] == item), None)
        if product:
            # Check for bulk offer
            # noinspection PyTypeChecker
            if "bulk_offer" in product and quantity >= int(product["bulk_offer"]["threshold"]):
                # noinspection PyTypeChecker
                discount = int(product["bulk_offer"]["discount_percentage"])
                item_price = product['price'] * quantity * (1 - discount / 100)
                order_details.append(f"- {product['name']} x{quantity} (Bulk offer applied) - {item_price}RON")
            else:
                item_price = product['price'] * quantity
                order_details.append(f"- {product['name']} x{quantity} - {item_price}RON")
            total_price += item_price

    orders[order_id] = {
        "user_id": user_id,
        "products": cart,
        "status": "Processing",
        "total_price": total_price
    }

    # Inform the user
    order_details_str = "\n".join(order_details)
    await update.message.reply_text(f"Checkout successful. Your order ID is {order_id}. Total price: {total_price}RON."
                                    f"Use /track {order_id} to track your order.\n\nOrder details:\n"
                                    f"{order_details_str}")

    # Send a notification to the admin
    admin_message = (f"New order received:\nOrder ID: {order_id}\nUser ID: {user_id}\nProducts:\n{order_details_str}\n"
                     f"Status: Processing\nTotal price: {total_price}RON")
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_message)
