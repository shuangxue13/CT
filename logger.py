import json
from datetime import datetime
from models import ConsciousnessEvent

DATA_FILE = "tracer_data.json"

def log_event(event: ConsciousnessEvent):
    """将意识事件追加写入JSON文件"""
    # 1. 读取已有数据（文件不存在则创建空列表）
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    # 2. 把事件对象转成字典，datetime转成字符串（JSON不认datetime）
    event_dict = event.model_dump()
    event_dict['timestamp'] = event_dict['timestamp'].isoformat()

    # 3. 追加新事件
    data.append(event_dict)

    # 4. 写回文件（ensure_ascii=False 保证中文不乱码）
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ 事件已记录: {event.content[:30]}...")