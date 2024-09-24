import json
from telegram import Update
from telegram.ext import CallbackContext

# Path to the products and carts
CARTS_FILE = 'utils/carts.json'
PRODUCTS_FILE = 'utils/PRODUCTS.json'

# Load the products
with open(PRODUCTS_FILE, 'r') as file:
    PRODUCTS = json.loads(file.read())

def load_carts():
    """Load carts from the carts.json file."""
    try:
        with open(CARTS_FILE, 'r') as file:
            return json.loads(file.read())
    except FileNotFoundError:
        return {}

async def view_cart(update: Update, context: CallbackContext):
    """Displays the products in the user's cart."""
    user_id = str(update.effective_user.id)  # Convert user_id to string to match the JSON format

    # Load the cart
    carts = load_carts()
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
            if "bulk_offer" in product and quantity >= int(product["bulk_offer"]["threshold"]):
                discount = int(product["bulk_offer"]["discount_percentage"])
                discounted_price_per_item = product['price'] * (1 - discount / 100)
                item_total_price = discounted_price_per_item * quantity
                cart_details.append(f"{product['name']} x{quantity} - {discounted_price_per_item:.2f} RON each "
                                    f"(Bulk offer applied) - {item_total_price:.2f} RON total")
            else:
                item_total_price = product['price'] * quantity
                cart_details.append(f"{product['name']} x{quantity} - {product['price']} RON each - {item_total_price}"
                                    f" RON total")
            total_price += item_total_price

    cart_message = "Your cart contains:\n" + "\n".join(cart_details) + f"\n\nTotal price: {total_price:.2f} RON"

    await update.message.reply_text(cart_message + "\n\nUse /checkout to place your order.")
