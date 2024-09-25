from telegram import Update
from telegram.ext import ContextTypes, CallbackContext
from utils.handle_response import BOT_USERNAME, handle_response
from commands.product_navigation import handle_product_callback, handle_navigation_callback  # Import both callback handlers

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming text messages"""
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot: ', response)
    await update.message.reply_text(response)


async def handle_callback(update: Update, context: CallbackContext):
    """Handle callback queries from inline buttons"""
    query = update.callback_query
    await query.answer()  # Acknowledge the callback query to avoid 'loading' state on the client

    # Determine if the callback data is related to products or navigation
    callback_data = query.data

    if callback_data.startswith("product_"):
        # This is a product selection callback
        await handle_product_callback(update, context)
    elif callback_data.startswith("navigate_"):
        # This is a navigation (pagination) callback
        await handle_navigation_callback(update, context)
    else:
        # Handle any other potential callback queries if needed
        await query.edit_message_text(text="Invalid callback query.")
