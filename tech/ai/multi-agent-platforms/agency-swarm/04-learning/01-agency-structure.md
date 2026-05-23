# 4-1. Agency 구조

## 📁 표준 프로젝트 레이아웃

```
my_agency/
├── agency.py               # 메인 entry
├── agency_manifesto.md     # 회사 미션·톤
└── agents/
    ├── ceo/
    │   ├── ceo.py
    │   ├── instructions.md
    │   └── tools/
    │       └── DelegateTool.py
    ├── developer/
    │   ├── developer.py
    │   ├── instructions.md
    │   └── tools/
    │       ├── CreateFileTool.py
    │       └── RunTestsTool.py
    └── va/
        ├── va.py
        └── instructions.md
```

## 🤖 Agent 클래스
```python
# agents/developer/developer.py
from agency_swarm import Agent
from .tools.CreateFileTool import CreateFileTool
from .tools.RunTestsTool import RunTestsTool

class Developer(Agent):
    def __init__(self):
        super().__init__(
            name="Developer",
            description="파이썬 코드 작성 + 테스트",
            instructions="./instructions.md",
            tools=[CreateFileTool, RunTestsTool],
            files_folder="./files",
            schemas_folder="./schemas",
            temperature=0.3,
            max_prompt_tokens=10000,
        )
```

## 🏢 Agency 조립
```python
# agency.py
from agency_swarm import Agency
from agents.ceo.ceo import CEO
from agents.developer.developer import Developer
from agents.va.va import VA

agency = Agency(
    [
        CEO(),                # 사용자 진입
        [CEO(), Developer()], # CEO → Dev
        [CEO(), VA()],        # CEO → VA
        [Developer(), VA()],  # Dev → VA (보조 작업)
    ],
    shared_instructions="./agency_manifesto.md",
    temperature=0.3,
    max_prompt_tokens=10000,
)

if __name__ == "__main__":
    agency.demo_gradio()   # 또는 .run_demo() (CLI)
```

## ✅ 체크포인트
- [ ] 폴더 구조대로 3-agent 구성
- [ ] agency_manifesto.md 작성
- [ ] CEO만 사용자와 대화
- [ ] CEO가 Developer에게 위임 동작

## 🔗 다음 → [02-communication-flows.md](02-communication-flows.md)
