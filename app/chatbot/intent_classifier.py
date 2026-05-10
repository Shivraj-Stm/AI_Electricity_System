import json
import os
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# ================= LOAD MODEL =================
model = SentenceTransformer(
    'paraphrase-multilingual-MiniLM-L12-v2'
)


# ================= LOAD DATASET =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

dataset_path = os.path.join(BASE_DIR, "intents_dataset.json")

with open(dataset_path, "r", encoding="utf-8") as file:
    data = json.load(file)


# ================= PREPARE TRAINING DATA =================
intent_patterns = {}
intent_embeddings = {}

for intent in data["intents"]:

    tag = intent["tag"]

    patterns = intent["patterns"]

    intent_patterns[tag] = patterns

    embeddings = model.encode(patterns)

    intent_embeddings[tag] = embeddings


# ================= PREDICT INTENT =================
def predict_intent(user_input):

    text = user_input.lower()

    # ================= PRIORITY RULES =================

    history_keywords = [
        "history",
        "itihas",
        "itihaas",
        "mahina",
        "mahine",
        "month",
        "months",
        "previous",
        "old bill",
        "last month",
        "records"
    ]

    for word in history_keywords:

        if word in text:

            return "bill_history", 0.99

    # ================= EMBEDDING PREDICTION =================

    user_embedding = model.encode([user_input])

    best_intent = None
    best_score = -1

    for tag, embeddings in intent_embeddings.items():

        similarities = cosine_similarity(
            user_embedding,
            embeddings
        )

        score = np.max(similarities)

        if score > best_score:

            best_score = score
            best_intent = tag

    # ================= CONFIDENCE THRESHOLD =================
    if best_score < 0.40:

        return "fallback", best_score

    return best_intent, best_score