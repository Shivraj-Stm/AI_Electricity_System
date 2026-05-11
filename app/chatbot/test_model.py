from sentence_transformers import SentenceTransformer

model = None

def get_model():
    global model

    if model is None:
        model = SentenceTransformer(
            'paraphrase-MiniLM-L3-v2',
            device='cpu'
        )

        print("Model Loaded Successfully")

    return model