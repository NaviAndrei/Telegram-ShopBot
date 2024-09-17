import json
import os

from telegram import Update
from telegram.ext import ContextTypes

# Load product data from JSON file
with open(os.path.join(os.path.dirname(__file__), '..', 'utils', 'PRODUCTS.json'), 'r') as file:
    PRODUCTS = json.load(file)


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        search_query = ' '.join(context.args).lower()
        matching_products = [product for product in PRODUCTS if search_query in product['name'].lower()]

        if matching_products:
            message = "Search Results:\n"
            for product in matching_products:
                message += f"ID: {product['id']}~ {product['name']} - {product['price']}RON\n"
        else:
            message = "No products found matching your search."
    else:
        message = "Please provide a search query."

    await update.message.reply_text(message)
