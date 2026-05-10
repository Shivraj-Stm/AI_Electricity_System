import requests
import re
from deep_translator import GoogleTranslator


# ================= TRANSLATION FUNCTION =================
def translate_response(response, lang):

    try:

        # translate only if language is not English
        if lang != "en":

            response = GoogleTranslator(
                source='en',
                target=lang
            ).translate(response)

        return response

    except Exception as e:

        print("Translation Error:", e)

        return response


# ================= MAIN RESPONSE FUNCTION =================
def get_response(intent, acct_id=None, message="", lang="en"):

    # ================= BILL QUERY =================
    if intent == "bill_query":

        try:

            url = f"http://127.0.0.1:8000/user/bill/{acct_id}"

            response = requests.get(url)

            data = response.json()

            reply = (
                f"Current Bill: ₹{data['current_bill']}\n"
                f"Remaining Amount: ₹{round(data['remaining'])}\n"
                f"Last Paid Amount: ₹{round(data['paid'])}"
            )

            return translate_response(reply, lang)

        except Exception as e:

            print("Bill API Error:", e)

            return translate_response(
                "Unable to fetch bill details.",
                lang
            )

 # ================= BILL HISTORY =================
    elif intent == "bill_history":

        # convert message to lowercase
        message = message.lower()

        # ================= NUMBER WORD SUPPORT =================
        number_words = {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6
        }

        # find numeric months
        match = re.search(r'(\d+)', message)

        months = None

        # if digits found
        if match:

            months = int(match.group(1))

        else:

            # check word numbers
            for word, num in number_words.items():

                if word in message:

                    months = num
                    break

        # ================= DEFAULT HISTORY =================
        if not months:

            months = 3

        # ================= CHATBOT LIMIT =================
        if months > 6:

            return translate_response(
                "You can view up to 6 months of bill history in chatbot. "
                "Please check the History page for complete records.",
                lang
            )

        try:

            # ================= HISTORY API =================
            url = f"http://127.0.0.1:8000/user/history/{acct_id}"

            response = requests.get(url)

            data = response.json()

            # take only requested months
            history = data[:months]

            reply = f"Last {months} Months Bill History:\n\n"

            for item in history:

                reply += (
                    f"{item['month']} {item['year']} → "
                    f"{item['units']} units = "
                    f"₹{item['bill']}\n"
                )

            return translate_response(reply, lang)

        except Exception as e:

            print("History API Error:", e)

            return translate_response(
                "Unable to fetch bill history.",
                lang
            )
    # ================= ELECTRICITY SAVING TIPS =================
    elif intent == "savings_tips":

        reply = (
            "Here are some tips to save electricity:\n\n"
            "1. Turn off lights and appliances when not in use.\n"
            "2. Use energy-efficient LED bulbs.\n"
            "3. Unplug chargers and devices when not in use.\n"
            "4. Use natural light during the day.\n"
            "5. Set your thermostat to an energy-saving temperature.\n"
            "6. Use a power strip to easily turn off multiple devices at once.\n"
        )

        return translate_response(reply, lang)

    # ================= HIGH BILL REASON =================
    elif intent == "high_bill_reason":

        reply = (
            "High electricity bills can be caused by several factors, including:\n\n"
            "1. Increased usage: Using more electricity than usual can lead to higher bills.\n"
            "2. Seasonal changes: Certain seasons may require more electricity for heating or cooling.\n"
            "3. Faulty appliances: Malfunctioning appliances can consume more electricity than normal.\n"
            "4. Rate changes: Changes in electricity rates can affect your bill amount.\n"
            "5. Billing errors: Occasionally, billing errors can lead to higher bills.\n"
            "6. Energy inefficiency: Older homes or appliances may be less energy-efficient.\n"
        )

        return translate_response(reply, lang)

    # ================= APPLIANCE QUERY =================
    elif intent == "appliance_query":

        reply = (
            "Air conditioners, heaters, geysers, and refrigerators "
            "usually consume the most electricity in homes."
        )

        return translate_response(reply, lang)

    # ================= THANKS =================
    elif intent == "thanks":

        reply = (
            "You are welcome! If you have any queries, feel free to ask."
        )

        return translate_response(reply, lang)

    # ================= BYE =================
    elif intent == "bye":

        reply = "Goodbye! Have a great day!"

        return translate_response(reply, lang)

    # ================= GREETING =================
    elif intent == "greeting":

        reply = "Hello! How can I help you today?"

        return translate_response(reply, lang)

    # ================= FALLBACK =================
    reply = (
        "Sorry, I didn’t understand your request. Please try again."
    )

    return translate_response(reply, lang)