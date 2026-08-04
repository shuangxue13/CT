import json
import numpy as np
import os

EMBEDDINGS_FILE = "event_embeddings.json"

def load_embeddings():
    if not os.path.exists(EMBEDDINGS_FILE):
        return []
    with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def cosine(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def retrieve(query_vec, data, top_k=2):
    scored = []
    for item in data:
        sim = cosine(query_vec, item["embedding"])
        scored.append((sim, item["event"]))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [ev for _, ev in scored[:top_k]]

def template_insight(events):
    if len(events) < 2:
        return "样本不足，无法生成洞察。"
    a, b = events[0], events[1]
    return (
        f"你在「{a['context']}」经历 {a['event_type']}：「{a['content']}」；"
        f"而在「{b['context']}」获得 {b['event_type']}：「{b['content']}」。"
        f"暗示：情绪常是信号，洞察是其转化后的杠杆。"
    )

if __name__ == "__main__":
    data = load_embeddings()
    if not data:
        print("❌ 先 embedder.py")
        exit()
    query_vec = data[0]["embedding"]
    tops = retrieve(query_vec, data)
    print("\n——— 召回事件 ———")
    for ev in tops:
        print(f"{ev['event_type']}: {ev['content']}")

    auto_insight = template_insight(tops)
    print("\n——— Auto-Inight ———")
    print(auto_insight)

    from datetime import datetime
    ai_event = {
        "event_type": "INSIGHT_AUTO",
        "content": auto_insight,
        "intensity": 5,
        "context": "machine_reflect",
        "action_taken": None,
        "result": None,
        "created_at": datetime.now().isoformat(timespec="seconds")
    }

    ans = input("\n将此 Insight 送 refiner 人工过目？(y/n)：")
    if ans.lower() == "y":
        from refiner import refine, show
        rf = refine(ai_event)
        show(rf)
        if input("确认入库？(y/n)：").lower() == "y":
            raw = load()
            raw.append(rf)
            save(raw)
            print("✅ Insight 经人工提炼入库")