from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

# ========== Import ML + Rule-based =============
from app.chatbot.intent_classifier import predict_intent
from app.chatbot.response_generator import get_response
from app.chatbot.fallback import keyword_fallback

router = APIRouter()
user_context = {}

# ================= REQUEST MODEL =================
class ChatRequest(BaseModel):
    username: str
    message: str
    acct_id: str


# ================= GREETING =================
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


# ================= WELCOME =================
@router.get("/chat/welcome/{name}")
def welcome(name: str):
    greeting = get_greeting()
    return {
        "response": f"{greeting} {name}, how can I help you?"
    }


# ================= MAIN CHAT =================
@router.post("/chat")
def chat(request: ChatRequest):

    message = request.message.strip()
    acct_id = request.acct_id

    # ================= CONTEXT CHECK =================

    if acct_id in user_context:

        last_intent = user_context[acct_id]

        # if user sends only number after bill history query
        if message.isdigit() and last_intent == "bill_history":

            months = int(message)

            return {
                "reply": f"Showing last {months} months bill history."
            }

    # ================= STEP 1: INTENT DETECTION =================

    intent, confidence = predict_intent(message)

    # store current intent
    user_context[acct_id] = intent

    print("Intent:", intent, "Confidence:", confidence)

    # ================= STEP 2: RESPONSE =================

    if confidence > 0.6:

        reply = get_response(intent, acct_id,message)

    else:

        reply = keyword_fallback(message)

    return {"reply": reply}