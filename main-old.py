import logging
import os
import uuid
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext
from telegram.constants import ParseMode
from logging.handlers import TimedRotatingFileHandler
from credentials import telegram_bot_token, telegram_bot_username, admin_chat_id

# Environment Variables for Security
TOKEN = telegram_bot_token
BOT_USERNAME = telegram_bot_username
ADMIN_CHAT_ID = admin_chat_id

# Mocked Product Data (Consider replacing with database queries)
PRODUCTS = [
    {"id": 1, "name": "Viteza", "price": 100},
    {"id": 2, "name": "Boabe) - Pharaoh Blue", "price": 50},
    {"id": 3, "name": "Vitamina K", "price": 200, "bulk_offer": {"threshold": 7, "discount_percentage": 10}},
    {"id": 4, "name": "Carton", "price": 50},
    {"id": 5, "name": "Cristal MD", "price": 200}
]

carts = {}

# Example structure for storing orders. Each order has a unique ID, user ID, list of product IDs, and status.
orders = {}


def setup_logging(log_dir, log_filename):
    # Ensure log directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Create logger
    app_logger = logging.getLogger()
    app_logger.setLevel(logging.DEBUG)

    # Formatter for log messages
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Ensure log_dir and log_filename are explicitly typed as strings.
    # If they are not hardcoded strings, you might want to ensure their types at runtime.
    log_dir = str(log_dir)
    log_filename = str(log_filename)

    # Now construct the filename with os.path.join, which should not raise type hinting issues.
    filename = os.path.join(log_dir, log_filename)

    # Handler for logging to file with dynamic file naming
    file_handler = TimedRotatingFileHandler(
        filename=filename,
        when='midnight',
        interval=1,
        backupCount=7
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    app_logger.addHandler(file_handler)

    # Handler for logging to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    app_logger.addHandler(console_handler)

    return app_logger  # Return the logger object


admin_user_ids = {5052402745}  # Replace with actual admin Telegram user IDs


def is_admin(user_id):
    return user_id in admin_user_ids


async def update_order_status(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("You are not authorized to use this command.")
        return

    if len(context.args) < 2:
        await update.message.reply_text("Usage: /update_order_status <order_id> <new_status>")
        return

    order_id, new_status = context.args[0], ' '.join(context.args[1:])
    order = orders.get(order_id)

    if order:
        order['status'] = new_status
        # Notify the user
        await context.bot.send_message(chat_id=order['user_id'],
                                       text=f"Your order {order_id} status has been updated to: {new_status}.")
        await update.message.reply_text(f"Order {order_id} status updated to {new_status}.")
    else:
        await update.message.reply_text("Order not found.")


# Command Handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! I'm ShopBot. If you need help, use /help.")


def escape_markdown_v2(text):
    """Escapes characters for Markdown V2."""
    escape_chars = '_*[]()~`>#+-=|{}.!'
    return ''.join(['\\' + c if c in escape_chars else c for c in text])


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Path to the help message file
    help_file_path = 'help_message.txt'

    try:
        # Open and read the help message from the file
        with open(help_file_path, 'r', encoding='utf-8') as file:
            help_text = file.read()

        # Use the escape_markdown_v2 function to escape characters for Markdown V2
        escaped_help_text = escape_markdown_v2(help_text)

        # Send the escaped help message as a reply to the user, specifying Markdown V2 as the parse mode
        await update.message.reply_text(escaped_help_text, parse_mode=ParseMode.MARKDOWN_V2)

    except FileNotFoundError:
        # Handle the case where the help message file does not exist
        await update.message.reply_text("The help message file could not be found.")
    except Exception as e:
        # Handle other possible exceptions
        await update.message.reply_text(f"An error occurred: {str(e)}")


async def browse_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Available Products:\n"
    for product in PRODUCTS:
        message += f"ID: {product['id']}~ {product['name']} - {product['price']}RON\n"

    await update.message.reply_text(message)


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


def handle_response(text: str) -> str:
    text = text.lower()
    if 'hello' in text or 'hi' in text or 'hey' in text or 'hei' in text or 'hola' in text:
        return 'Hey there! If you need help, just type /help.'
    elif 'how are you' in text or 'how’s it going' in text:
        return 'I’m doing great, thanks! How can I assist you today?'
    elif 'bye' in text or 'goodbye' in text:
        return 'Goodbye! If you have more questions later, don’t hesitate to ask.'
    elif 'thank you' in text or 'thanks' in text:
        return 'You’re welcome! Happy to help.'
    elif 'help' in text:
        return ('Sure, what do you need help with? You can browse products with /browse, add items to your cart with '
                '/buy <product_id>, or check your cart with /cart.')
    elif 'what can you do' in text or 'capabilities' in text:
        return ('I can help you browse products, manage your shopping cart, and guide you through the checkout process.'
                'Use /help to see all commands.')
    elif 'price' in text:
        return ('You can find product prices by browsing our catalog with /browse or searching for a specific item with'
                ' /search <keyword>.')
    elif 'order' in text or 'purchase' in text:
        return ('To make a purchase, add products to your cart with /buy <product_id> and then use /checkout to place'
                ' your order.')
    elif 'cart' in text:
        return 'You can view the items in your cart with /cart and remove items with /remove <product_id>.'
    if 'support' in text or 'complaint' in text or 'suport' in text:
        return ('I’m here to help! Please describe your issue, and I’ll do my best to assist. For more complex issues,'
                'you can send an email to 0h5h5@example.com')
    elif 'product' in text:
        return ('You can browse our products with /browse, add items to your cart with /buy <product_id>, or check your'
                ' cart with /cart.')
    elif 'catalog' in text or 'catalogue' in text:
        return ('You can browse our products with /browse, add items to your cart with /buy <product_id>, or check your'
                ' cart with /cart.')
    elif 'checkout' in text or 'order' in text or 'purchase' in text:
        return ('To make a purchase, add products to your cart with /buy <product_id> and then use /checkout to place'
                ' your order.')
    else:
        return ('I do not understand what you wrote. Type /help for assistance or try using a command like /browse to'
                ' see our products.')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

# Additional command and message handlers...


# Utility Functions
# Adds a product to the user's shopping cart
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


# Checkout process initiation
async def checkout(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    cart = carts.pop(user_id, [])
    if not cart:
        await update.message.reply_text("Your cart is empty.")
        return

    # Generate a unique order ID and create an order entry
    order_id = str(uuid.uuid4())

    # Initialize total price and order details
    total_price = 0
    order_details = []

    for item in set(cart):  # Iterate through unique items in cart
        quantity = cart.count(item)
        product = next((p for p in PRODUCTS if p['id'] == item), None)
        if product:
            # Check for bulk offer
            # noinspection PyTypeChecker
            if "bulk_offer" in product and quantity >= int(product["bulk_offer"]["threshold"]):
                # noinspection PyTypeChecker
                discount = int(product["bulk_offer"]["discount_percentage"])
                item_price = product['price'] * quantity * (1 - discount / 100)
                order_details.append(f"- {product['name']} x{quantity} (Bulk offer applied) - {item_price}RON")
            else:
                item_price = product['price'] * quantity
                order_details.append(f"- {product['name']} x{quantity} - {item_price}RON")
            total_price += item_price

    orders[order_id] = {
        "user_id": user_id,
        "products": cart,
        "status": "Processing",
        "total_price": total_price
    }

    # Inform the user
    order_details_str = "\n".join(order_details)
    await update.message.reply_text(f"Checkout successful. Your order ID is {order_id}. Total price: {total_price}RON."
                                    f"Use /track {order_id} to track your order.\n\nOrder details:\n"
                                    f"{order_details_str}")

    # Send a notification to the admin
    admin_message = (f"New order received:\nOrder ID: {order_id}\nUser ID: {user_id}\nProducts:\n{order_details_str}\n"
                     f"Status: Processing\nTotal price: {total_price}RON")
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_message)


async def view_cart(update: Update, context: CallbackContext):
    """Displays the products in the user's cart."""
    user_id = update.effective_user.id  # Correctly extracting user ID from the update object
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
            # noinspection PyTypeChecker
            if "bulk_offer" in product and quantity >= int(product["bulk_offer"]["threshold"]):
                # noinspection PyTypeChecker
                discount = int(product["bulk_offer"]["discount_percentage"])
                discounted_price_per_item = product['price'] * (1 - discount / 100)
                item_total_price = discounted_price_per_item * quantity
                cart_details.append(f"{product['name']} x{quantity} - {discounted_price_per_item}RON each "
                                    f"(Bulk offer applied) - {item_total_price}RON total")
            else:
                item_total_price = product['price'] * quantity
                cart_details.append(f"{product['name']} x{quantity} - {product['price']}RON each - {item_total_price}"
                                    f"RON total")
            total_price += item_total_price

    cart_message = "Your cart contains:\n" + "\n".join(cart_details) + f"\n\nTotal price: {total_price}RON"

    await update.message.reply_text(cart_message + "\n\nUse /checkout to place your order.")


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


async def empty_cart(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    carts[user_id] = []
    await update.message.reply_text("Your cart has been emptied.")


async def track_order(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("Please provide an order ID.")
        # return

    order_id = context.args[0]
    order = orders.get(order_id)

    if order and order['user_id'] == update.effective_user.id:  # Ensure users can only track their own orders
        status = order['status']
        await update.message.reply_text(f"Your order {order_id} is currently {status}.")
    else:
        await update.message.reply_text("Order not found or access denied.")


async def notify_pickup(update: Update, context: CallbackContext):
    # Permission check
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("You are not authorized to use this command.")
        return

    # Check if there are enough arguments
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /notify_pickup <order_id> [latitude,longitude]")
        return

    # Check if there are enough arguments
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /notify_pickup <order_id> <latitude,longitude>")
        return

    order_id_str = context.args[0]
    location_str = context.args[1]

    # Validate order ID (check if it's a valid UUID)
    try:
        order_id = uuid.UUID(order_id_str)
    except ValueError:
        await update.message.reply_text("Invalid order ID. Please provide a valid UUID format order ID.")
        return

    # Validate and parse latitude and longitude
    try:
        latitude, longitude = map(float, location_str.split(','))
        maps_link = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"
    except ValueError:
        await update.message.reply_text("Invalid location format. Please provide in the format <latitude,longitude>.")
        return

    # Attempt to notify the user
    try:
        message = (
            f"Your order ({order_id}) is ready for pickup.\n"
            f"Please pick it up at this location: {maps_link}"
        )
        await update.message.reply_text(message)
        # Notify the admin that the location coords have been sent to the user
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Notification sent to the user for order "
                                                                   f"ID {order_id}.")
    except Exception as e:
        # Notify the admin of the error
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Failed to send notification for order"
                                                                   f" ID {order_id}. Error: {str(e)}")
    else:
        # Default pickup location: Tineretului Park
        latitude, longitude = 44.413381124302326, 26.104192740329374

    # # Fetch order from database
    # order = orders.get(order_id)
    # if not order:
    #     await update.message.reply_text("Order not found.")
    #     return

    # # Send notification to user
    # try:
    #     await context.bot.send_message(chat_id=order['user_id'],
    #                                    text=f"Your order {order_id} is ready for pickup. "
    #                                         f"Please pick it up at this location: "
    #                                         f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}")
    #     await update.message.reply_text(f"Notification sent for order {order_id}.")
    # except Exception as e:
    #     await update.message.reply_text(f"Failed to send notification. Error: {str(e)}")


# Assuming setup_logging has already been called
logger = logging.getLogger(__name__)  # Gets or creates a logger


async def upload_photo(update: Update, context: CallbackContext):
    # Ensure update and update.message are not None
    if update is None or update.message is None:
        logging.error("Update or message is None")
        return  # Optionally send a message to the user

    # Attempt to get the user ID safely
    try:
        user_id = update.effective_user.id
    except AttributeError:
        logging.error("Cannot get user ID")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Error processing request.")
        return

    # Check if the user is an admin
    if not is_admin(user_id):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use "
                                                                              "this feature.")
        return

    # Check if the message contains a photo
    if update.message.photo:
        try:
            photo = update.message.photo[-1]  # Get the highest resolution photo available
            photo_file = await context.bot.get_file(photo.file_id)
            photo_file_id = photo_file.file_id

            # Respond with the file ID of the uploaded photo
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Photo uploaded successfully. File "
                                                                                  f"ID: {photo_file_id}")
        except Exception as e:
            logging.error(f"Error uploading photo: {e}")
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to upload photo. "
                                                                                  "Please try again.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Please send a photo.")


async def send_order_photo(update: Update, context: CallbackContext):
    # Ensure update and update.message are not None
    if update is None or update.message is None:
        logging.error("Update or message is None")
        return  # Optionally send a message to the user

    try:
        user_id = update.effective_user.id

        if not is_admin(user_id):
            await update.message.reply_text("You are not authorized to use this command.")
            return

        if len(context.args) < 2:
            await update.message.reply_text("Usage: /send_order_photo <order_id> <photo_file_id_or_url> [caption]")
            return

        order_id = context.args[0]
        photo_source = context.args[1]
        caption = ' '.join(context.args[2:]) if len(context.args) > 2 else 'Your order is ready for pickup!'

        order = orders.get(order_id)
        if order:
            try:
                if photo_source.startswith("http"):
                    await context.bot.send_photo(chat_id=order['user_id'], photo=photo_source, caption=caption)
                else:
                    await context.bot.send_photo(chat_id=order['user_id'], photo=photo_source, caption=caption)
                await update.message.reply_text(f"Photo sent for order {order_id}.")
            except Exception as e:
                logging.error(f"Failed to send photo for order {order_id}: {e}")
                await update.message.reply_text(f"Failed to send photo for order {order_id}. Please try again.")
        else:
            await update.message.reply_text("Order not found.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        await update.message.reply_text("An unexpected error occurred. Please try again.")


async def help_admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not is_admin(user_id):
        await update.message.reply_text("You are not authorized to use this command.")
        return

    # Define the path to your admin help message file
    admin_help_file_path = 'Readme.txt'  # This line becomes unreachable if the user is not an admin.

    try:
        with open(admin_help_file_path, 'r') as file:
            admin_help_message = file.read()
        await update.message.reply_text(admin_help_message, parse_mode='Markdown')
    except FileNotFoundError:
        await update.message.reply_text("Admin help file not found.")
    except Exception as e:
        logging.error(f"Error reading admin help file: {e}")
        await update.message.reply_text("An error occurred while reading the admin help file.")


async def send_chat_id(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Your chat ID is {chat_id}")


# Main Function
def main():
    log_directory = "logs"
    log_file_name = "TelegramBot_Debug.log"
    app_logger = setup_logging(log_directory, log_file_name)  # Get the logger object

    application = Application.builder().token(TOKEN).build()

    # Adding command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("browse", browse_command))
    application.add_handler(CommandHandler("search", search_command))
    application.add_handler(CommandHandler("buy", add_to_cart))
    application.add_handler(CommandHandler("checkout", checkout))
    application.add_handler(CommandHandler("cart", view_cart))
    application.add_handler(CommandHandler("remove", remove_from_cart))
    application.add_handler(CommandHandler("track", track_order))
    application.add_handler(CommandHandler('empty_cart', empty_cart))
    application.add_handler(CommandHandler("chat_id", send_chat_id))

    # Admin Only Commands:
    application.add_handler(CommandHandler("update_order_status", update_order_status))
    application.add_handler(CommandHandler("notify_pickup", notify_pickup))
    application.add_handler(CommandHandler("send_order_photo", send_order_photo))
    application.add_handler(CommandHandler("help_admin", help_admin_command))

    # Register the upload_photo function to be called for photo messages from admin users
    photo_handler = MessageHandler(filters.PHOTO & filters.User(user_id=list(admin_user_ids)), upload_photo)
    application.add_handler(photo_handler)

    # Additional handlers...
    # Messages
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    app_logger.info("Starting bot...")
    application.run_polling()


if __name__ == '__main__':
    main()
