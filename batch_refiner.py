import json
import os
from datetime import datetime

DATA_FILE = "tracer_data.json"

def load():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def refine(ev):
    r = dict(ev)
    r["created_at"] = datetime.now().isoformat(timespec="seconds")
    c = r.get("content", "")
    r["content"] = c.strip()[:120]
    for k in ("action_taken", "result"):
        if r.get(k) == "":
            r[k] = None
    return r

if __name__ == "__main__":
    data = load()
    if not data:
        print("❌ 无数据")
        exit()

    refined_all = []
    print("=== 批量人工过目（y=存 n=跳 e=编辑）===")
    for i, ev in enumerate(data, 1):
        r = refine(ev)
        print(f"\n#{i}")
        for k in ["event_type","content","intensity","context","action_taken","result"]:
            print(f"  {k}: {r.get(k)}")
        ans = input("  处理：").strip().lower()
        if ans == "y":
            refined_all.append(r)
        elif ans == "e":
            r["content"] = input("  新 content：")
            refined_all.append(r)

    if refined_all:
        save(refined_all)
        print(f"✅ 批量入库 {len(refined_all)} 条")
    else:
        print("❎ 未存")