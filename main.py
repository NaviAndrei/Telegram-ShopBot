import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from commands.start_command import start_command
from commands.help_command import help_command
from commands.browse_command import browse_command
from commands.search_command import search_command
from commands.add_to_cart import add_to_cart
from commands.checkout import checkout
from commands.view_cart import view_cart
from commands.remove_from_cart import remove_from_cart
from commands.track_order import track_order
from commands.empty_cart import empty_cart
from commands.send_chat_id import send_chat_id
from commands.update_order_status import update_order_status
from commands.notify_pickup import notify_pickup
from commands.send_order_photo import send_order_photo
from commands.help_admin_command import help_admin_command
from commands.upload_photo import upload_photo
from handlers.handle_message import handle_message
from utils.logging_setup import setup_logging

# Environment Variables for Security
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Logging Configuration
setup_logging('logs', 'TelegramBot_Debug.log')


def main():
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
    application.add_handler(CommandHandler("track_order", track_order))
    application.add_handler(CommandHandler("empty_cart", empty_cart))
    application.add_handler(CommandHandler("send_chat_id", send_chat_id))
    application.add_handler(CommandHandler("update_order_status", update_order_status))
    application.add_handler(CommandHandler("notify_pickup", notify_pickup))
    application.add_handler(CommandHandler("send_order_photo", send_order_photo))
    application.add_handler(CommandHandler("help_admin", help_admin_command))
    application.add_handler(CommandHandler("upload_photo", upload_photo))

    # Adding message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()


if __name__ == '__main__':
    main()
