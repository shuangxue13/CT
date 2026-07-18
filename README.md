Consciousness Tracer

A minimal structured event logger for self-reflection and leverage analysis.

Records thoughts / emotions / actions as typed events via Pydantic, persisted to JSON.

Stack

Python 3.10+

Pydantic (data validation)

Local JSON storage (no DB required)

Quick Start

Clone & enter

git clone https://github.com/shuangxue13/CT.git

cd CT

Create env (Windows)

python -m venv tracer-env

tracer-env\Scripts\activate

Install deps

pip install pydantic

Run

python main.py

Output: tracer_data.json with your first ConsciousnessEvent.

Structure

models.py   -> ConsciousnessEvent schema (Pydantic)

logger.py   -> append event -> tracer_data.json

main.py     -> demo entrypoint

START_HERE.txt -> standard startup workflow

Event Schema

field: event_type | type: str | meaning: THOUGHT / EMOTION / ACTION / INSIGHT

field: content    | type: str | meaning: free-text description

field: intensity  | type: int | meaning: 1-10

field: context    | type: str | meaning: scene / situation

field: action_taken | type: str? | meaning: what you did

field: result     | type: str? | meaning: outcome

Roadmap

Vector embedding + semantic retrieval (RAG)

Daily / weekly reflection aggregator

Optional LLM summarization

External brain · Week 1 MVP