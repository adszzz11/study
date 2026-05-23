# OpenAI Swarm 심층 스터디

> 교육용 / **deprecated** — 멀티 에이전트 핵심 개념(handoffs) 학습엔 여전히 가치 있음. 프로덕션은 **OpenAI Agents SDK**로.

## 한 줄 정의

**Swarm**(OpenAI 공식)은 **Routines + Handoffs** 두 개념만으로 멀티 에이전트를 설명하는 의도적으로 가벼운 교육용 프레임워크. 후속작 **OpenAI Agents SDK**에 본격 기능 이전됨.

## ⚠️ 첫 메모

> 새 프로젝트는 **OpenAI Agents SDK** (https://github.com/openai/openai-agents-python) 사용. Swarm은 학습/연구용으로만.

## 3줄 요약

1. **Routines**: 에이전트가 실행할 instruction set + tools.
2. **Handoffs**: 한 에이전트가 다른 에이전트로 대화 통제권 이양 (function return으로).
3. **Stateless 클라이언트**: 서버 상태 없이 Chat Completions API만 사용.

## 핵심 키워드

`#openai-swarm` `#handoffs` `#routines` `#educational` `#deprecated` `#multi-agent` `#chat-completions`

## ⚡ Quick Start
```bash
pip install git+https://github.com/openai/swarm.git
```

```python
from swarm import Swarm, Agent

def transfer_to_specialist():
    return specialist   # 다음 에이전트 반환 = handoff

triage = Agent(
    name="Triage",
    instructions="질문 분류 후 전문가에게 위임",
    functions=[transfer_to_specialist],
)
specialist = Agent(name="Specialist", instructions="...")

client = Swarm()
result = client.run(agent=triage, messages=[{"role":"user","content":"..."}])
```

## 📑 목차
| 파일 | 내용 |
|------|------|
| [01-overview.md](01-overview.md) | Routines + Handoffs |
| [02-ecosystem.md](02-ecosystem.md) | Agents SDK 후계 |
| [03-references.md](03-references.md) | 자료 |
| [04-learning/01-handoffs.md](04-learning/01-handoffs.md) | Handoff 패턴 |
| [04-learning/02-context-variables.md](04-learning/02-context-variables.md) | 컨텍스트 변수 |
| [04-learning/03-streaming.md](04-learning/03-streaming.md) | 스트리밍 |
| [04-learning/04-migrate-to-agents-sdk.md](04-learning/04-migrate-to-agents-sdk.md) | Agents SDK로 마이그레이션 |
| [05-projects.md](05-projects.md) | 학습용 예제 |
| [cheatsheet.md](cheatsheet.md) | 빠른 참조 |
