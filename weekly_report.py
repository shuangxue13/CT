import json
import os
from datetime import datetime, timedelta

DATA_FILE = "tracer_data.json"

def week_bound():
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    return monday, monday + timedelta(days=6)

def main():
    if not os.path.exists(DATA_FILE):
        print("❌ 无仓库")
        return
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    start, end = week_bound()
    weeks = [e for e in data if "created_at" in e and start.isoformat()[:10] <= e["created_at"][:10] <= end.isoformat()[:10]]
    insights = [e for e in weeks if e["event_type"] in ("INSIGHT","INSIGHT_AUTO")]
    print(f"=== 周报 {start.date()} ~ {end.date()} ===")
    print(f"事件总数: {len(weeks)} | 洞察数: {len(insights)}")
    for e in insights:
        print(f"· [{e.get('tags',[])}] {e['content'][:60]}")
    print("==============================")
    if input("生成此周报并入库？(y/n)：").lower()=="y":
        report = {
            "event_type":"WEEKLY_REPORT",
            "content": f"Week {start.date()} items={len(weeks)} insights={len(insights)}",
            "intensity":None,
            "context":"auto_weekly",
            "action_taken":None,
            "result":None,
            "tags":["#周报"],
            "created_at":datetime.now().isoformat(timespec="seconds")
        }
        data.append(report)
        with open(DATA_FILE,"w",encoding="utf-8") as f:
            json.dump(data,f,indent=2,ensure_ascii=False)
        print("✅ 周报已入库（人工确认）")

if __name__ == "__main__":
    main()