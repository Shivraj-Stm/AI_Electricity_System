from langdetect import detect
from googletrans import Translator

translator = Translator()

def detect_language(text: str):
    try:
        return detect(text)
    except:
        return "en"

def translate_text(text: str, target_lang: str):
    try:
        translated = translator.translate(text, dest=target_lang)
        return translated.text
    except:
        return text