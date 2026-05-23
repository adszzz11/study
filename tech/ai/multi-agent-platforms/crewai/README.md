# CrewAI 심층 스터디

> 역할 기반 AI 에이전트 크루를 가장 빠르게 만드는 방법 — 20줄로 시작.

## 한 줄 정의

**CrewAI**는 **역할 기반 자율 에이전트들이 협업**하도록 만드는 Python 프레임워크. `Agent`(역할 가진 행위자) + `Task`(작업 단위) + `Crew`(팀)의 세 추상화로, 비즈니스 워크플로우를 직관적으로 모델링한다.

## 3줄 요약

1. **3개 추상화로 충분**: Agent / Task / Crew만 알면 즉시 협업 시스템 구축.
2. **LangChain 독립**: 자체 코어, 더 빠르고 가볍게 동작.
3. **52k★, 가장 인기**: 멀티 에이전트 프로토타이핑의 사실상 표준. CrewAI Flows + AMP Suite로 프로덕션까지 확장.

## 핵심 키워드

`#multi-agent` `#role-based` `#python` `#crew` `#flows` `#sequential` `#hierarchical` `#mit` `#prototyping`

## ⚡ Quick Start

```bash
uv pip install crewai 'crewai[tools]'
```

```python
from crewai import Agent, Task, Crew, Process

researcher = Agent(role="리서처", goal="기술 동향 조사",
                   backstory="AI 트렌드 전문가", verbose=True)
writer = Agent(role="작가", goal="한국어 요약 작성",
               backstory="기술 글 잘 쓰는 작가", verbose=True)

t1 = Task(description="LangGraph 최신 동향 조사", agent=researcher,
          expected_output="bullet 5개")
t2 = Task(description="t1 결과를 한국어 1page 요약", agent=writer,
          expected_output="markdown")

crew = Crew(agents=[researcher, writer], tasks=[t1, t2],
            process=Process.sequential)
result = crew.kickoff()
print(result)
```

## 📑 전체 목차

| 파일 | 내용 |
|------|------|
| [01-overview.md](01-overview.md) | Agent/Task/Crew 모델, Process 타입, Flows |
| [02-ecosystem.md](02-ecosystem.md) | LangGraph/Agency Swarm/AutoGen과의 차이 |
| [03-references.md](03-references.md) | 공식·튜토리얼 |
| [04-learning/01-agents-tasks-crews.md](04-learning/01-agents-tasks-crews.md) | 3대 추상화 패턴 |
| [04-learning/02-processes.md](04-learning/02-processes.md) | Sequential vs Hierarchical |
| [04-learning/03-tools-and-memory.md](04-learning/03-tools-and-memory.md) | tools, RAG, 메모리 |
| [04-learning/04-flows-production.md](04-learning/04-flows-production.md) | CrewAI Flows로 프로덕션 |
| [05-projects.md](05-projects.md) | 실전 프로젝트 |
| [cheatsheet.md](cheatsheet.md) | 빠른 참조 |

## 🗓️ 학습 플랜

| Day | 목표 |
|-----|------|
| 1 | 01-overview, Quick Start 돌려보기 |
| 2 | Agent/Task/Crew 패턴 익히기 |
| 3 | Hierarchical 프로세스로 매니저 에이전트 만들기 |
| 4 | Tools/Memory 붙이기 |
| 5 | Flows로 이벤트 드리븐 시스템 |
| 6+ | 실전 프로젝트 1개 |
