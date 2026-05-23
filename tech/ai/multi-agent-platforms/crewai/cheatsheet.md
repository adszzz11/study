# CrewAI Cheat Sheet

## 🚀 설치
```bash
uv pip install crewai 'crewai[tools]'
```

## 🧩 기본 패턴
```python
from crewai import Agent, Task, Crew, Process

a = Agent(role=, goal=, backstory=, tools=[], llm=, allow_delegation=False)
t = Task(description=, expected_output=, agent=a, context=[])
crew = Crew(agents=[...], tasks=[...], process=Process.sequential, memory=True)
result = crew.kickoff(inputs={"key": "value"})
```

## 🌊 Flow 패턴
```python
from crewai.flow.flow import Flow, listen, start, router

class MyFlow(Flow[StateModel]):
    @start()
    def begin(self): ...
    @listen(begin)
    def next(self): ...
    @router(next)
    def branch(self): return "path_a"
    @listen("path_a")
    def path_a(self): ...
```

## 🛠️ 내장 도구
```python
from crewai_tools import (
  SerperDevTool, WebsiteSearchTool, FileReadTool, FileWriterTool,
  GithubSearchTool, PDFSearchTool, YoutubeChannelSearchTool,
  MCPServerAdapter,
)
```

## 🔧 CLI
```bash
crewai create crew my-project       # 새 프로젝트
crewai run                          # 현재 크루 실행
crewai install                      # 의존성 동기화
crewai test                         # 테스트
crewai deploy                       # AMP 배포
```

## 🔑 환경변수
```bash
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
SERPER_API_KEY=             # SerperDevTool
CREWAI_AMP_KEY=             # AMP 트레이싱
```

## 📂 프로젝트 구조 (crewai create)
```
my-project/
├── src/my_project/
│   ├── crew.py
│   ├── main.py
│   ├── config/
│   │   ├── agents.yaml
│   │   └── tasks.yaml
│   └── tools/
└── pyproject.toml
```

## 🔗 빠른 링크
- 공식: https://docs.crewai.com
- GitHub: https://github.com/crewAIInc/crewAI
- 본 study: `study/tech/ai/multi-agent-platforms/crewai/`
