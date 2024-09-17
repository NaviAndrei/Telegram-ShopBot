import logging
from telegram import Update
from telegram.ext import ContextTypes
from utils.is_admin import is_admin


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
