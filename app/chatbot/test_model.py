from sentence_transformers import SentenceTransformer

model = None

def get_model():
    global model

    if model is None:
        model = SentenceTransformer(
            'paraphrase-MiniLM-L3-v2',
            device='cpu'
        )

    return model

print("Model Loaded Successfully")