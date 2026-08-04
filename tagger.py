import json
import os
from datetime import datetime

DATA_FILE = "tracer_data.json"
PRESET = ["#杠杆", "#情绪", "#代码", "#洞察", "#实习", "#废话"]

def load():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def ensure_tags(ev):
    if "tags" not in ev:
        ev["tags"] = []
    if "created_at" not in ev:
        ev["created_at"] = datetime.now().isoformat(timespec="seconds")
    return ev

if __name__ == "__main__":
    data = load()
    updated = []
    print("=== A. 事件打标（人工过目）===")
    for i, ev in enumerate(data, 1):
        ev = ensure_tags(ev)
        print(f"\n#{i} [{ev['created_at']}]")
        print(f"  {ev['event_type']}: {ev['content'][:50]}")
        print(f"  现有标签: {ev['tags']}")
        print(f"  预设: {PRESET}")
        t = input("  输入标签（逗号,#可，回车不变）：").strip()
        if t:
            tags = [x.strip() for x in t.replace("#", "").split(",") if x.strip()]
            ev["tags"] = list(set(ev["tags"] + ["#"+tag for tag in tags]))
        updated.append(ev)
    save(updated)
    print("✅ 全部事件已打标")