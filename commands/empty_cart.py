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


async def empty_cart(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)  # Store user ID as a string for JSON compatibility
    carts = load_carts()  # Load the current carts from the file

    # Empty the user's cart
    carts[user_id] = []

    # Save the updated carts back to file
    save_carts(carts)

    await update.message.reply_text("Your cart has been emptied.")
