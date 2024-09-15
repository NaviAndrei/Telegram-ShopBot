import logging
from telegram import Update
from telegram.ext import CallbackContext
from utils.is_admin import is_admin


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
