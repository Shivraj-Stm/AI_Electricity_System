def keyword_fallback(message: str):

    message = message.lower()

    # Greeting
    if "hi" in message or "hello" in message or "hey" in message:
        return "Hello! How can I help you today?"

    # Bill related
    elif "bill" in message or "amount" in message:
        return "You can check your latest bill in the billing section."

    # Usage related
    elif "usage" in message or "consumption" in message or "units" in message:
        return "Your electricity usage details are available in the dashboard."

    # Saving electricity
    elif "save" in message or "reduce" in message:
        return (
            "Here are some tips to save electricity:\n"
            "- Use LED bulbs\n"
            "- Turn off unused appliances\n"
            "- Reduce AC usage\n"
            "- Use energy-efficient devices"
        )

    # Complaint
    elif "complaint" in message or "issue" in message:
        return "Please describe your issue. We will assist you."

    # Default fallback
    return "Sorry, I didn’t understand your request. Please try again."