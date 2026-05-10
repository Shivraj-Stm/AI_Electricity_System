from datetime import datetime


def get_greeting():
    hour = datetime.now().hour

    if 5 <= hour < 12:
        return "Good Morning"
    elif 12 <= hour < 17:
        return "Good Afternoon"
    elif 17 <= hour < 21:
        return "Good Evening"
    else:
        return "Hello"


def generate_response(name: str, message: str):
    greeting = get_greeting()
    message_lower = message.lower()

    # Greeting message
    if message_lower in ["hi", "hello", "hey"]:
        return f"{greeting} {name}, how can I help you?"

    # Bill related
    elif "bill" in message_lower:
        return "Please provide your Account ID to check your bill."

    # Usage related
    elif "usage" in message_lower:
        return "Do you want monthly, yearly or seasonal usage?"

    # Default fallback
    else:
        return "I didn't understand that. Please rephrase."