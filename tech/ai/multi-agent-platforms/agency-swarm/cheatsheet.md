# Agency Swarm Cheat Sheet

## 🚀 설치
```bash
pip install -U agency-swarm
```

## 🧩 기본 패턴
```python
from agency_swarm import Agent, Agency
from agency_swarm.tools import BaseTool
from pydantic import Field

class MyTool(BaseTool):
    arg: str = Field(..., description="...")
    def run(self):
        return ...

class CEO(Agent):
    def __init__(self):
        super().__init__(name="CEO",
            instructions="./instructions.md",
            tools=[MyTool])

agency = Agency([CEO(), [CEO(), Dev()]])
agency.run_demo()       # CLI
agency.demo_gradio()    # 웹 UI
```

## 📂 폴더 구조
```
agency/
├── agency.py
├── agency_manifesto.md
└── agents/
    └── ceo/
        ├── ceo.py
        ├── instructions.md
        └── tools/
            └── MyTool.py
```

## 🔁 통신 흐름
```python
[A]              # 사용자 ↔ A
[A, B]           # A → B
[A, B], [B, A]   # 양방향
```

## 🔧 자주 쓰는 옵션
```python
Agent(
    name=, description=, instructions=,
    tools=[],
    files_folder="./files",      # RAG
    schemas_folder="./schemas",  # OpenAPI 자동 도구
    model="claude-opus",
    temperature=0.3,
    max_prompt_tokens=10000,
)
```

## 🌉 Multi-LLM
```bash
litellm --model anthropic/claude-opus-4-7 --port 4000
```
```python
import openai
openai.base_url = "http://localhost:4000/v1"
```

## 🔗 빠른 링크
- 공식: https://github.com/VRSEN/agency-swarm
- Docs: https://vrsen.github.io/agency-swarm/
- 본 study: `study/tech/ai/multi-agent-platforms/agency-swarm/`
