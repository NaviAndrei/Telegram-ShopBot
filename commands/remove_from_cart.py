from telegram import Update
from telegram.ext import CallbackContext

carts = {}


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
