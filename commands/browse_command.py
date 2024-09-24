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
        message += f"{product['id']}: {product['name']} - {product['price']} RON\n"
    await update.message.reply_text(message)
