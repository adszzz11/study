# Part 1. Agency Swarm 개요

## 📌 핵심: "Agency 메타포"

```
Agency (회사)
   │
   ├─ CEO (사용자 1차 진입점)
   │
   └─ 직원들 (Developer, VA, Researcher, ...)
       └─ 각자 instructions.md + tools.py + files/
```

CrewAI의 "Crew"가 평등한 동료라면, Agency Swarm은 **명확한 위계** (CEO > 직원).

## 🔁 통신 흐름 정의

```python
agency = Agency([
    ceo,                  # 사용자 ↔ CEO
    [ceo, dev],           # CEO → Developer
    [ceo, va],            # CEO → VA
    [dev, qa],            # Developer → QA (단방향)
])
```

리스트 형식이 통신 방향 = **`A > B`** (A가 B를 호출 가능, 역방향은 명시 안 하면 불가).

## 🧩 Agent 구조 (폴더 기반)

```
agents/
└── developer/
    ├── instructions.md     # 시스템 프롬프트
    ├── tools.py            # Pydantic Tool 정의
    ├── files/              # 참조 파일 (RAG)
    └── schemas/            # OpenAPI 스키마 (외부 API)
```

이 폴더 구조 자체가 신호 — 직원 1명 = 모듈 1개.

## 🔧 OpenAI Agents SDK 기반

- 내부적으로 OpenAI Agents SDK + Responses API 사용
- LiteLLM 통해 Claude/Gemini 등 다른 모델도 OK
- thread/conversation persistence 1급

## ⚖️ 장단점

### ✅ 장점
- **명시적 통신 흐름** — 실수로 잘못 위임 ✗
- **폴더 기반 모듈화** — 직원 추가가 코드 추가가 아니라 폴더 추가
- **Pydantic type-safe tool** — 런타임 에러 ↓
- **CEO 중심 사용자 경험** — 챗봇처럼 자연스러움
- **OpenAI Agents SDK 위라 안정**

### ❌ 단점
- **OpenAI 결제 + Assistants API** — 사용량·지연·비용
- **상태/체크포인트 약함** (LangGraph만큼 강하지 않음)
- 4.4k★ — 비교적 작은 생태계
- Python 3.12+ 요구
- 노코드 빌더 없음

## 🎯 적합도

| 상황 | 적합 |
|------|------|
| 챗봇형 멀티 에이전트 (CEO가 응대) | ⭐⭐⭐⭐⭐ |
| 명확한 위임 흐름이 있는 조직 | ⭐⭐⭐⭐⭐ |
| Type-safe 프로덕션 | ⭐⭐⭐⭐ |
| 그래프/상태 머신 필요 | ⭐⭐ (LangGraph) |
| OpenAI 외 모델 위주 | ⭐⭐⭐ (LiteLLM 필요) |

## 🔗 다음 → [02-ecosystem.md](02-ecosystem.md)
