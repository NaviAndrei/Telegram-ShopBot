from credentials import telegram_bot_username

BOT_USERNAME = telegram_bot_username


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
