import json
import logging
from telegram import Update
from telegram.ext import CallbackContext

with open('utils/PRODUCTS.json', 'r') as file:
    PRODUCTS = json.loads(file.read())

carts = {}


async def add_to_cart(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    logging.info(f"add_to_cart called by user {user_id}")
    try:
        # Extract product ID and optional quantity from the command arguments
        product_id = int(context.args[0])
        quantity = int(context.args[1]) if len(context.args) > 1 else 1  # Default quantity is 1 if not specified

        # Validate the product ID
        product = next((product for product in PRODUCTS if product['id'] == product_id), None)
        if not product:
            await update.message.reply_text("Product not found.")
            return

        logging.info(f"Product ID: {product_id}, Quantity: {quantity}")
        logging.info(f"Cart before addition: {carts.get(user_id, 'Empty')}")

        # Validate the quantity
        if quantity < 1:
            await update.message.reply_text("Invalid quantity. Please specify a positive number.")
            return

        # Initialize the user's cart if it doesn't exist
        carts.setdefault(user_id, [])
        # Add the product to the cart, considering the quantity
        for _ in range(quantity):
            carts[user_id].append(product_id)

        logging.info(f"Cart after addition: {carts[user_id]}")

        # Respond appropriately based on the quantity added
        if quantity == 1:
            await update.message.reply_text("Product added to your cart.")
        else:
            await update.message.reply_text(f"{quantity} items of the product added to your cart.")

    except IndexError:
        await update.message.reply_text("Please specify the product ID you wish to add to your cart.")
    except ValueError:
        await update.message.reply_text("Invalid input. Please specify a valid product ID and an optional quantity.")
    except Exception as e:
        logging.error(f"Error in add_to_cart: {e}")
