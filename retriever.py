import json
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDINGS_FILE = "event_embeddings.json"

def load_embeddings():
    with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search(query, top_k=3):
    model = SentenceTransformer(MODEL_NAME)
    q_emb = model.encode(query)
    data = load_embeddings()

    scored = []
    for item in data:
        sim = cosine_similarity(q_emb, item["embedding"])
        scored.append((sim, item["event"]))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]

if __name__ == "__main__":
    q = input("输入检索语句：")
    results = search(q)
    for score, ev in results:
        print(f"[{score:.3f}] {ev['event_type']}: {ev['content']}")