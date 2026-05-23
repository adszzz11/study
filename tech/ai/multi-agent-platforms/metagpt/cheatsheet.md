# MetaGPT Cheat Sheet

## 🚀 설치
```bash
pip install --upgrade metagpt
metagpt --init-config       # ~/.metagpt/config2.yaml 생성
```

## ⚙️ 설정 (~/.metagpt/config2.yaml)
```yaml
llm:
  api_type: "openai"   # 또는 "anthropic", "ollama"
  api_key: "sk-..."
  model: "gpt-4o"

repair_llm_output: true
```

## 🎬 CLI
```bash
metagpt "요구사항 텍스트"               # 새 프로젝트
metagpt --inc --project-path PATH "..." # 점진 개발
metagpt --use_docker "..."              # 격리 실행
metagpt --debug "..."                   # 상세 로그
metagpt --max-auto-summarize-code 0    # 코드 요약 안 함
```

## 🐍 Python API
```python
from metagpt.roles import ProductManager, Architect, Engineer
from metagpt.team import Team

async def main():
    team = Team()
    team.hire([ProductManager(), Architect(), Engineer()])
    team.invest(3.0)
    team.run_project("...")
    await team.run(n_round=5)
```

## 🤖 Data Interpreter
```python
from metagpt.roles.di.data_interpreter import DataInterpreter
await DataInterpreter().run("data/x.csv 분석")
```

## 🎭 Custom Role
```python
from metagpt.roles import Role
from metagpt.actions import Action

class MyRole(Role):
    name: str = "X"
    profile: str = "..."
    def __init__(self, **kw):
        super().__init__(**kw)
        self.set_actions([MyAction])
        self._watch([SomeOtherAction])
```

## 📂 결과물
```
workspace/<project>/
├── docs/prd.md
├── docs/system_design.json
├── docs/task.md
├── src/
└── tests/
```

## 🔗 빠른 링크
- 공식: https://github.com/geekan/MetaGPT
- Docs: https://docs.deepwisdom.ai
- 본 study: `study/tech/ai/multi-agent-platforms/metagpt/`
