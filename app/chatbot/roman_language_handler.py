# ================= ROMAN NEPALI MAP =================
ROMAN_NEPALI_MAP = {

    "mero bill deu": "show my bill",
    "mero bijuli bill deu": "show my electricity bill",
    "mero 3 mahina ko bill deu": "show 3 month bill history",
    "mero 6 mahina ko bill deu": "show 6 month bill history",
    "mero bill itihas dekhau": "show bill history"
}


# ================= ROMAN HINDI MAP =================
ROMAN_HINDI_MAP = {

    "mera bill dikhao": "show my bill",
    "mera bijli bill dikhao": "show my electricity bill",
    "mera 3 mahine ka bill dikhao": "show 3 month bill history",
    "mera 6 mahine ka bill dikhao": "show 6 month bill history",
    "mera bill itihaas dikhao": "show bill history"
}


# ================= ROMAN LANGUAGE DETECTION =================
def convert_roman_text(text):

    text_lower = text.lower().strip()

    # ================= NEPALI =================
    for key, value in ROMAN_NEPALI_MAP.items():

        if key in text_lower:

            return value, "ne"

    # ================= HINDI =================
    for key, value in ROMAN_HINDI_MAP.items():

        if key in text_lower:

            return value, "hi"

    # ================= DEFAULT =================
    return text, None