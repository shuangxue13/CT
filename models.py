from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ConsciousnessEvent(BaseModel):
    id: Optional[int] = None
    timestamp: datetime = datetime.now()
    event_type: str      # THOUGHT / EMOTION / ACTION / INSIGHT
    content: str         # 具体描述
    intensity: int       # 1-10
    context: str         # 场景
    source: str = "human"
    action_taken: Optional[str] = None
    result: Optional[str] = None