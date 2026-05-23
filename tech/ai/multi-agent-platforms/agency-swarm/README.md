# Agency Swarm 심층 스터디

> CEO + 전문직 직원 메타포로 안정적인 멀티 에이전트 — OpenAI Agents SDK 기반

## 한 줄 정의

**Agency Swarm**(VRSEN 제작)은 "Agency"라는 회사 구조 안에 **CEO + 직원**을 두고, `>` 연산자로 **명시적 통신 흐름**을 정의하는 Python 프레임워크. OpenAI Agents SDK 위에서 type-safe하게 동작.

## 3줄 요약

1. **Agency = CEO + 직원들**의 명시적 조직도.
2. **`ceo > dev`** — `>` 연산자로 통신 방향 통제 (역방향은 X).
3. **Pydantic 기반 type-safe tool** — 프로덕션 신뢰성.

## 핵심 키워드

`#agency-swarm` `#ceo-pattern` `#openai-agents-sdk` `#pydantic` `#multi-agent` `#vrsen` `#python` `#mit`

## ⚡ Quick Start

```bash
pip install -U agency-swarm
```

```python
from agency_swarm import Agent, Agency

ceo = Agent(name="CEO", description="사용자와 대화, 위임", 
            instructions="agents/ceo/instructions.md")
dev = Agent(name="Developer", description="코드 작성",
            instructions="agents/dev/instructions.md", tools=[CodeTool])

agency = Agency([
    ceo,            # 사용자 진입점
    [ceo, dev],     # ceo → dev 통신 허용
])

agency.run_demo()   # CLI 데모
```

## 📑 목차
| 파일 | 내용 |
|------|------|
| [01-overview.md](01-overview.md) | Agency/CEO 모델 |
| [02-ecosystem.md](02-ecosystem.md) | CrewAI/AutoGen와 차이 |
| [03-references.md](03-references.md) | 공식·튜토리얼 |
| [04-learning/01-agency-structure.md](04-learning/01-agency-structure.md) | Agency 구조 |
| [04-learning/02-communication-flows.md](04-learning/02-communication-flows.md) | `>` 연산자 |
| [04-learning/03-tools-pydantic.md](04-learning/03-tools-pydantic.md) | Pydantic 도구 |
| [04-learning/04-multi-llm-litellm.md](04-learning/04-multi-llm-litellm.md) | Claude/Gemini 라우팅 |
| [05-projects.md](05-projects.md) | 실전 |
| [cheatsheet.md](cheatsheet.md) | 빠른 참조 |
