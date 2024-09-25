<<<<<<< HEAD
import json
import logging
from telegram import Update
from telegram.ext import CallbackContext
import os

# Paths to products and carts
PRODUCTS_FILE = 'utils/PRODUCTS.json'
CARTS_FILE = 'utils/carts.json'

# Load the products
try:
    with open(PRODUCTS_FILE, 'r') as file:
        PRODUCTS = json.loads(file.read())
except FileNotFoundError:
    PRODUCTS = {}  # Fallback if products file is not found
    logging.error(f"Products file '{PRODUCTS_FILE}' not found. Using empty product list.")


def load_carts():
    """Load carts from the carts.json file."""
    try:
        if os.path.exists(CARTS_FILE) and os.path.getsize(CARTS_FILE) > 0:
            with open(CARTS_FILE, 'r') as file:
                return json.loads(file.read())
        else:
            logging.warning(f"Carts file '{CARTS_FILE}' is missing or empty. Returning empty carts.")
            return {}
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from carts file: {e}. Returning empty carts.")
        return {}


def save_carts(carts):
    """Save carts to the carts.json file."""
    try:
        with open(CARTS_FILE, 'w') as file:
            json.dump(carts, file, indent=4)
        logging.info(f"Carts successfully saved to '{CARTS_FILE}'.")
    except Exception as e:
        logging.error(f"Failed to save carts: {e}")


async def add_to_cart(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)  # Ensure user ID is stored as a string (for JSON compatibility)
    logging.info(f"add_to_cart called by user {user_id}")

    # Load current carts
    carts = load_carts()

    # Ensure user cart exists
    if user_id not in carts:
        carts[user_id] = []

    try:
        # Ensure at least a product ID is provided
        if len(context.args) == 0:
            await update.message.reply_text("Please specify the product ID you wish to add to your cart.")
            return

        # Extract product ID and optional quantity from the command arguments
        product_id = int(context.args[0])  # Parse product ID
        quantity = int(context.args[1]) if len(context.args) > 1 else 1  # Default quantity is 1 if not specified

        # Validate product ID exists in PRODUCTS dictionary
        if isinstance(PRODUCTS, list):
            # Assuming PRODUCTS is a list of dictionaries or IDs
            product_ids = [prod.get('id', None) if isinstance(prod, dict) else prod for prod in PRODUCTS]
        else:
            # PRODUCTS is expected to be a dictionary with product IDs as keys
            product_ids = list(PRODUCTS.keys())

        if product_id not in product_ids:
            await update.message.reply_text(f"Invalid product ID: {product_id}. Please select a valid product.")
            return

        # Validate the quantity is a positive integer
        if quantity < 1:
            await update.message.reply_text("Invalid quantity. Please specify a positive number.")
            return

        logging.info(f"Product ID: {product_id}, Quantity: {quantity}")

        # Add the product to the cart for the user
        carts[user_id].extend([product_id] * quantity)  # Add 'quantity' number of the product to the user's cart
        logging.info(f"Cart after addition: {carts[user_id]}")

        # Save the updated carts back to the carts.json file
        save_carts(carts)

        # Respond appropriately based on the quantity added
        if quantity == 1:
            await update.message.reply_text("Product added to your cart.")
        else:
            await update.message.reply_text(f"{quantity} items of the product added to your cart.")

    except (IndexError, ValueError) as e:
        # Handle both IndexError (no arguments provided) and ValueError (non-integer input)
        logging.error(f"Input error: {e}")
        await update.message.reply_text("Invalid input. Please specify a valid product ID and an optional quantity.")
    except Exception as e:
        logging.error(f"Error in add_to_cart: {e}")
        await update.message.reply_text("An error occurred while adding the product to your cart. Please try again.")
=======
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
>>>>>>> bd5b9ce1bcd5d4b5aba4265e011c85a738c39520
