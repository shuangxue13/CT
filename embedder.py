import numpy as np
from sentence_transformers import SentenceTransformer
import json
import os

MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDINGS_FILE = "event_embeddings.json"

def load_events():
    if not os.path.exists("tracer_data.json"):
        return []
    with open("tracer_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def generate_embeddings(events):
    model = SentenceTransformer(MODEL_NAME)
    texts = [f"{e['event_type']}: {e['content']} (context: {e['context']})" for e in events]
    return model.encode(texts)

def save_embeddings(events, embeddings):
    """保存向量 + 原始事件"""
    data = [
        {
            "event": event,
            "embedding": emb.tolist()   # ← numpy → python list
        }
        for event, emb in zip(events, embeddings)
    ]
    with open(EMBEDDINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    events = load_events()
    if not events:
        print("❌ 没有 tracer_data.json，先 python main.py")
    else:
        embs = generate_embeddings(events)
        save_embeddings(events, embs)
        print(f"✅ 生成 {len(embs)} 条向量 -> {EMBEDDINGS_FILE}")