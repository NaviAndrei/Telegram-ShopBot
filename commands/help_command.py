<<<<<<< HEAD
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


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
=======
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


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
>>>>>>> bd5b9ce1bcd5d4b5aba4265e011c85a738c39520
