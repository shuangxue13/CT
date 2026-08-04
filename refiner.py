import json
import os
from datetime import datetime

DATA_FILE = "tracer_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def refine(event):
    """整理提炼：补时间、清空值、缩内容、保标签"""
    refined = dict(event)

    # 补时间戳
    refined["created_at"] = datetime.now().isoformat(timespec="seconds")

    # 提炼 content（去首尾空格，截太长）
    c = refined.get("content", "")
    refined["content"] = c.strip()[:120]

    # 空值转 None 明示
    for k in ("action_taken", "result"):
        if refined.get(k) == "":
            refined[k] = None

    # ✅ Day 5：确保每个事件都有 tags 字段
    if "tags" not in refined or not isinstance(refined["tags"], list):
        refined["tags"] = []

    return refined

def show(refined):
    print("\n——— 拟存入仓库（请人工过目）———")
    for k in ["event_type", "content", "intensity", "context", "action_taken", "result", "created_at"]:
        v = refined.get(k)
        print(f"{k}: {v}")
    print("——————————————")

if __name__ == "__main__":
    data = load_data()
    if not data:
        print("❌ 仓库为空，先记事件")
        exit()

    # 取最后一条做示例（你可改索引）
    raw = data[-1]
    refined = refine(raw)
    show(refined)

    ans = input("\n确认保存？(y=存 / n=弃 / e=编辑)：").strip().lower()
    if ans == "y":
        data.append(refined)
        save_data(data)
        print("✅ 已提炼入库")
    elif ans == "e":
        refined["content"] = input("新 content：")
        data.append(refined)
        save_data(data)
        print("✅ 编辑后入库")
    else:
        print("❎ 取消，未入库")