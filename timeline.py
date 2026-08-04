import json
import os

DATA_FILE = "tracer_data.json"

def main():
    if not os.path.exists(DATA_FILE):
        print("❌ 无仓库")
        return
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    # 按时间排
    evs = [e for e in data if "created_at" in e]
    evs.sort(key=lambda x: x["created_at"])
    for e in evs:
        print(f"[{e['created_at']}] {e['event_type']}: {e['content'][:40]}...")
    if not evs:
        print("（尚无带时间事件，先用 refiner 入库）")

if __name__ == "__main__":
    main()