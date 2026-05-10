from langdetect import detect
from deep_translator import GoogleTranslator

SUPPORTED_LANGS = ["en", "hi", "ne"]

def detect_language(text):
    if len(text.strip()) < 3:
        return "en"
    
    try:
        lang = detect(text)
        return lang if lang in SUPPORTED_LANGS else "en"
    except:
        return "en"


def to_english(text, lang):
    if lang == "en":
        return text
    return GoogleTranslator(source=lang, target='en').translate(text)


def from_english(text, lang):
    if lang == "en":
        return text
    return GoogleTranslator(source='en', target=lang).translate(text)