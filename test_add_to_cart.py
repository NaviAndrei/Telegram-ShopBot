import asyncio


# Mock the Update and CallbackContext objects from the Telegram Bot API
class MockUpdate:
    def __init__(self, user_id, command_args):
        self.effective_user = MockUser(user_id)
        self.message = MockMessage(command_args)


class MockUser:
    def __init__(self, user_id):
        self.id = user_id


class MockMessage:
    def __init__(self, command_args):
        self.text = '/buy ' + ' '.join(command_args)
        self.chat_id = 12345  # Example chat ID

    async def reply_text(self, text):
        print(f"Reply: {text}")


class MockCallbackContext:
    def __init__(self, args):
        self.args = args


# Mock PRODUCTS and carts for testing
PRODUCTS = [{'id': 1, 'name': 'Test Product', 'price': 10}]
carts = {}  # User carts


# The add_to_cart function to be tested
async def add_to_cart(update, context):
    # Function logic here...
    user_id = update.effective_user.id
    try:
        # Extract product ID and optional quantity from the command arguments
        product_id = int(context.args[0])
        quantity = int(context.args[1]) if len(context.args) > 1 else 1  # Default quantity is 1 if not specified

        # Validate the product ID
        product = next((product for product in PRODUCTS if product['id'] == product_id), None)
        if not product:
            await update.message.reply_text("Product not found.")
            return

        # Validate the quantity
        if quantity < 1:
            await update.message.reply_text("Invalid quantity. Please specify a positive number.")
            return

        # Initialize the user's cart if it doesn't exist
        carts.setdefault(user_id, [])
        # Add the product to the cart, considering the quantity
        for _ in range(quantity):
            carts[user_id].append(product_id)

        # Respond appropriately based on the quantity added
        if quantity == 1:
            await update.message.reply_text("Product added to your cart.")
        else:
            await update.message.reply_text(f"{quantity} items of the product added to your cart.")

    except IndexError:
        await update.message.reply_text("Please specify the product ID you wish to add to your cart.")
    except ValueError:
        await update.message.reply_text("Invalid input. Please specify a valid product ID and an optional quantity.")
    pass


# Test function
async def test_add_to_cart():
    user_id = 6863259501  # Example user ID
    product_id = '1'
    quantity = '2'
    update = MockUpdate(user_id, [product_id, quantity])
    context = MockCallbackContext([product_id, quantity])

    await add_to_cart(update, context)

    # Verify the cart contains the correct items
    assert user_id in carts, "User cart not created."
    assert carts[user_id].count(int(product_id)) == int(quantity), "Incorrect quantity in cart."


# Run the test

if __name__ == '__main__':
    asyncio.run(test_add_to_cart())
