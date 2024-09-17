import json
from telegram import Update
from telegram.ext import CallbackContext

with open('utils/PRODUCTS.json', 'r') as file:
    PRODUCTS = json.loads(file.read())

carts = {}


async def view_cart(update: Update, context: CallbackContext):
    """Displays the products in the user's cart."""
    user_id = update.effective_user.id  # Correctly extracting user ID from the update object
    cart = carts.get(user_id, [])

    if not cart:
        await update.message.reply_text("Your cart is empty.")
        return

    total_price = 0
    cart_details = []

    for item in set(cart):
        quantity = cart.count(item)
        product = next((p for p in PRODUCTS if p['id'] == item), None)
        if product:
            # Check for bulk offer and calculate price accordingly
            # noinspection PyTypeChecker
            if "bulk_offer" in product and quantity >= int(product["bulk_offer"]["threshold"]):
                # noinspection PyTypeChecker
                discount = int(product["bulk_offer"]["discount_percentage"])
                discounted_price_per_item = product['price'] * (1 - discount / 100)
                item_total_price = discounted_price_per_item * quantity
                cart_details.append(f"{product['name']} x{quantity} - {discounted_price_per_item}RON each "
                                    f"(Bulk offer applied) - {item_total_price}RON total")
            else:
                item_total_price = product['price'] * quantity
                cart_details.append(f"{product['name']} x{quantity} - {product['price']}RON each - {item_total_price}"
                                    f"RON total")
            total_price += item_total_price

    cart_message = "Your cart contains:\n" + "\n".join(cart_details) + f"\n\nTotal price: {total_price}RON"

    await update.message.reply_text(cart_message + "\n\nUse /checkout to place your order.")
