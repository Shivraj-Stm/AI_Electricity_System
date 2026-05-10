from language_utils import detect_language, to_english
from roman_language_handler import convert_roman_text
from preprocessing import preprocess
from intent_classifier import predict_intent
from response_generator import get_response


def chatbot_response(user_text, acct_id=None):

    #   Handle Roman Nepali / Roman Hindi
    converted_text, detected_lang = convert_roman_text(user_text)

    # ================= LANGUAGE HANDLING =================
    if detected_lang:

        lang = detected_lang
        text_en = converted_text

    else:

        #  Detect language automatically
        lang = detect_language(user_text)

        # Convert user text to English
        text_en = to_english(user_text, lang)

    # ================= NLP PIPELINE =================
    processed = preprocess(text_en)
    print("Original User Input:", user_text)
    print("Detected Language:", lang)
    print("Converted English Text:", text_en)

    #  Predict intent
    intent, score = predict_intent(processed)

    print(f"Intent: {intent}")
    print(f"Confidence Score: {score}")
     
    if score < 0.40:
        intent = "fallback"

    # ================= RESPONSE GENERATION =================
    response = get_response(
        intent=intent,
        acct_id=acct_id,
        message=text_en,
        lang=lang
    )

    return response