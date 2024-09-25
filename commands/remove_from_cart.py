<<<<<<< HEAD
import json
from telegram import Update
from telegram.ext import CallbackContext

CARTS_FILE = 'utils/carts.json'


# Load the carts from the file
def load_carts():
    """Load carts from the carts.json file."""
    try:
        with open(CARTS_FILE, 'r') as file:
            return json.loads(file.read())
    except FileNotFoundError:
        return {}


# Save the updated carts to the file
def save_carts(carts):
    """Save carts to the carts.json file."""
    with open(CARTS_FILE, 'w') as file:
        json.dump(carts, file, indent=4)


async def remove_from_cart(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)  # Store user ID as a string for JSON compatibility
    carts = load_carts()  # Load the current carts from the file

    try:
        product_id = int(context.args[0])

        if product_id in carts.get(user_id, []):
            carts[user_id].remove(product_id)
            # Save the updated carts back to file
            save_carts(carts)
            await update.message.reply_text("Product removed from your cart.")
        else:
            await update.message.reply_text("Product not in cart.")
    except IndexError:
        await update.message.reply_text("Please specify the product ID you wish to remove from your cart.")
    except ValueError:
        await update.message.reply_text("Invalid product ID. Please specify a valid number.")
=======
from telegram import Update
from telegram.ext import CallbackContext

carts = {}


async def remove_from_cart(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    try:
        product_id = int(context.args[0])
        if product_id in carts.get(user_id, []):
            carts[user_id].remove(product_id)
            await update.message.reply_text("Product removed from your cart.")
        else:
            await update.message.reply_text("Product not in cart.")
    except IndexError:
        await update.message.reply_text("Please specify the product ID you wish to remove from your cart.")
    except ValueError:
        await update.message.reply_text("Invalid product ID. Please specify a valid number.")
>>>>>>> bd5b9ce1bcd5d4b5aba4265e011c85a738c39520
