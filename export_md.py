import json
import os
from datetime import datetime

DATA_FILE = "tracer_data.json"

def main():
    with open(DATA_FILE,"r",encoding="utf-8") as f:
        data = json.load(f)
    md = f"# Consciousness Tracer 导出\n生成：{datetime.now().isoformat()}\n\n"
    for e in sorted(data, key=lambda x:x.get("created_at","")):
        t = e.get("created_at","?")
        tags = " ".join(e.get("tags",[]))
        md += f"### [{t}] {e['event_type']} {tags}\n{e['content']}\n\n"
    with open("export.md","w",encoding="utf-8") as f:
        f.write(md)
    print("✅ export.md 已生成（按需触发）")

if __name__ == "__main__":
    main()