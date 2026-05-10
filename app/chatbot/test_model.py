from sentence_transformers import SentenceTransformer

model = None

def get_model():
    global model

    if model is None:
        model = SentenceTransformer(
            'paraphrase-multilingual-MiniLM-L12-v2'
        )

    return model

print("Model Loaded Successfully")