import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

# Load product data from JSON file
with open(os.path.join(os.path.dirname(__file__), '..', 'utils', 'PRODUCTS.json'), 'r') as file:
    PRODUCTS = json.load(file)


async def handle_product_callback(update: Update, context: CallbackContext = None):
    """Handles a user's selection of a product"""
    query = update.callback_query
    await query.answer()  # Acknowledge the callback query

    # Extract the product ID from the callback data
    product_id = int(query.data.split("_")[1])

    # Find the selected product
    product = next((prod for prod in PRODUCTS if prod['id'] == product_id), None)

    if product:
        # Display the product details
        product_details = (
            f"Product ID: {product['id']}\n"
            f"Name: {product['name']}\n"
            f"Price: {product['price']} RON\n"
            f"Description: {product.get('description', 'No description available.')}"
        )
        await query.edit_message_text(text=product_details)
    else:
        await query.edit_message_text(text="Product not found.")


async def handle_navigation_callback(update: Update, context: CallbackContext = None):
    """Handles navigation between product pages"""
    query = update.callback_query
    await query.answer()  # Acknowledge the callback query

    # Extract the page number from the callback data
    page_number = int(query.data.split("_")[1])

    # Re-display the product list for the new page
    await show_product_page(query, page_number)


async def show_product_page(query, page_number: int):
    """Displays a list of products with inline buttons for navigation"""
    PRODUCTS_PER_PAGE = 5
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
    await query.edit_message_text("Available Products:", reply_markup=reply_markup)
