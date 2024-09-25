<<<<<<< HEAD
import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# Load product data from JSON file
with open(os.path.join(os.path.dirname(__file__), '..', 'utils', 'PRODUCTS.json'), 'r') as file:
    PRODUCTS = json.load(file)

# Number of products per page
PRODUCTS_PER_PAGE = 5


async def browse_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    page_number = 0  # Start at the first page
    await show_product_page(update, page_number)


async def show_product_page(update: Update, page_number: int):
    """Displays a list of products with inline buttons for navigation"""
    start_idx = page_number * PRODUCTS_PER_PAGE
    end_idx = start_idx + PRODUCTS_PER_PAGE
    product_subset = PRODUCTS[start_idx:end_idx]

    # Creating the product buttons
    keyboard = [[InlineKeyboardButton(product['name'], callback_data=f"product_{product['id']}")]
                for product in product_subset]

    # Adding navigation buttons
    navigation_buttons = []
    if page_number > 0:
        navigation_buttons.append(InlineKeyboardButton("Previous", callback_data=f"navigate_{page_number - 1}"))
    if end_idx < len(PRODUCTS):
        navigation_buttons.append(InlineKeyboardButton("Next", callback_data=f"navigate_{page_number + 1}"))

    if navigation_buttons:
        keyboard.append(navigation_buttons)

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Available Products:", reply_markup=reply_markup)
=======
import json
import os
from telegram import Update
from telegram.ext import ContextTypes

# Load product data from JSON file
with open(os.path.join(os.path.dirname(__file__), '..', 'utils', 'PRODUCTS.json'), 'r') as file:
    PRODUCTS = json.load(file)


async def browse_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Available Products:\n"
    for product in PRODUCTS:
        message += f"{product['id']}: {product['name']} - ${product['price']}\n"
    await update.message.reply_text(message)
>>>>>>> bd5b9ce1bcd5d4b5aba4265e011c85a738c39520
