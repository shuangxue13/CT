from datetime import datetime
from models import ConsciousnessEvent
from logger import log_event

if __name__ == "__main__":
    # 构造一条真实的意识事件
    event = ConsciousnessEvent(
        timestamp=datetime.now(),
        event_type="INSIGHT",
        content="意识到时间是最高的杠杆，拒绝低价值实习",
        intensity=9,
        context="复盘今日求职策略",
        source="human",
        action_taken="拒绝140元/天的驻场实习",
        result="内心清明，能量提升"
    )

    # 调用logger存盘
    log_event(event)
    print("🎉 Tracer 第一条数据已落地！")