---
date: 2026-05-24
tags:
  - tech
  - ai
  - google-adk
  - agent-sample
status: learning
type: tech-concept
---

# Google ADK Deep Search 샘플

> **한 줄 정의**: Google ADK + Gemini로 만든 프로덕션급 리서치 에이전트 샘플 — 협업 플래닝(Human-in-the-Loop) → 자율 실행(검색·비판·합성) 두 단계 워크플로

## 1. What - 개념 정의

`google/adk-samples` 레포의 `python/agents/deep-search`에 들어있는 풀스택 샘플. ADK(Agent Development Kit)와 Gemini를 사용해 "리서치 → 보고서 작성"을 자동화하는 패턴을 보여주며, 별다른 수정 없이 Google Cloud Run 또는 Agent Runtime에 배포 가능하다.

### 주요 용어

| 용어 | 설명 |
|------|------|
| **ADK** | Agent Development Kit — 오픈소스 에이전트 프레임워크 (Python/TypeScript/Go/Java/Kotlin) |
| **Agent Runtime** | Gemini Enterprise Agent Platform의 매니지드 실행 환경 (구 Vertex AI Agent Engine) |
| **Human-in-the-Loop** | 자율 실행 전 사용자가 플랜을 검토·승인하는 게이트 |
| **Iterative Refinement** | Critic 에이전트가 결과 품질을 평가하고, 기준 미달 시 다시 검색·합성을 반복하는 루프 |
| **Tagged Directives** | `[RESEARCH]`, `[DELIVERABLE]`, `[MODIFIED]`, `[NEW]`, `[IMPLIED]` 등 플랜 항목 분류 태그 |

---

## 2. Why - 등장 배경 & 필요성

### 해결하려는 문제

- "딥 리서치"형 에이전트를 직접 만들 때 흔히 빠지는 함정: 플래닝 없이 곧장 LLM에 검색 시키면 산만한 결과, 검증 없이 합성하면 출처 누락/환각
- 멀티 에이전트 워크플로우의 진입 장벽 — planner/researcher/critic/composer 같은 역할 분리를 처음부터 설계하기 어려움
- Cloud 배포 인프라(인증·스케일링·로깅)까지 한 번에 보여주는 풀스택 레퍼런스 부재

### 기존 방식의 한계

- 단일 LLM 호출: 깊이·검증 부족
- LangGraph 기반 직접 구현: 보일러플레이트 + 배포 분리
- 노트북 데모 수준 샘플: 프론트엔드/배포 누락

---

## 3. How - 동작 원리

### 2단계 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│ Phase 1: Collaborative Planning (Human-in-the-Loop)     │
│                                                         │
│  User ──topic──▶ Planner ──tagged plan──▶ User approval │
│                  (Gemini)   [RESEARCH][DELIVERABLE]...  │
└─────────────────────────────────────────────────────────┘
                          │ approved
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Phase 2: Autonomous Execution                           │
│                                                         │
│   Outline ─▶ Researcher ─▶ web search                   │
│              │                                          │
│              ▼                                          │
│            Critic ──not OK──▶ refine query ──┐          │
│              │                               │          │
│              │ OK                            └──────────┘│
│              ▼                                          │
│           Composer ─▶ Report w/ inline citations        │
└─────────────────────────────────────────────────────────┘
```

### 동작 흐름

1. 사용자가 리서치 주제 입력
2. **Planner 에이전트**가 다단계 플랜 초안 생성 (tagged directives 포함)
3. 사용자가 플랜 수정·승인 → 자율 실행 단계로 진입
4. 플랜을 구조화된 outline으로 변환
5. **Researcher 에이전트**가 web search 함수 호출 → 결과 수집
6. **Critic 에이전트**가 품질 평가 → 기준 미달이면 쿼리 재작성 후 5번 반복
7. **Composer 에이전트**가 인라인 출처 인용이 포함된 최종 리포트 작성

### 핵심 메커니즘

- **멀티 에이전트 역할 분리**: planner / researcher / critic / composer — ADK가 sub-agent 패턴을 제공
- **품질 기반 종료 조건**: Critic의 평가가 임계치를 넘을 때까지 루프 (max iterations로 무한루프 방지)
- **태그 기반 플랜 트래킹**: `[MODIFIED]`/`[NEW]` 태그로 사용자가 수정한 부분을 UI에서 시각화
- **Frontend-Backend 동기화**: 백엔드 에이전트 이름을 React UI 컴포넌트 트리와 일치시켜 진행 상황 타임라인 표시

---

## 4. 실무 적용

### 셋업

요구 사항: Python 3.10+, Node.js, `uv` 패키지 매니저, Google Cloud SDK (Vertex AI API 활성화), API 키 (AI Studio 또는 Vertex AI)

**권장 경로 — Google Agents CLI 사용**:

```bash
uvx google-agents-cli setup
agents-cli create my-deep-search-agent -a adk@deep-search
```

이 명령으로 CI/CD 포함 프로덕션 스캐폴딩이 자동 생성된다.

### 디렉토리 구조

```
deep-search/
├── app/                 # 백엔드 (ADK + FastAPI)
│   ├── agent.py         # 에이전트 정의 (수정 포인트)
│   └── config.py        # ResearchConfiguration
├── frontend/            # React + Vite + Tailwind + Shadcn UI
├── .env.example
├── Makefile
├── pyproject.toml
└── uv.lock
```

### 커스터마이즈 포인트

- `app/agent.py`: 에이전트 로직, 프롬프트, 서브에이전트 추가/수정
- `app/config.py`: `ResearchConfiguration`으로 max iterations, 품질 임계치 등 조정
- 프론트엔드: 에이전트 이름이 UI 타임라인과 매칭되므로 같이 업데이트 필요

### Best Practices

- **Critic의 평가 기준을 구체적으로 작성**: "정확한가" 같은 모호한 기준은 LLM이 너무 관대하게 통과시킴
- **Max iterations 고정**: 무한 정제 루프는 비용 폭증의 주범
- **출처 인용 강제**: Composer 프롬프트에 "각 주장에 출처 URL 인라인 포함" 명시

### Anti-patterns (주의사항)

- 플랜 승인 단계를 생략하면 자율 실행이 엉뚱한 방향으로 폭주
- 동일한 모델로 Researcher와 Critic을 돌리면 평가가 의미 없어짐 — Critic은 다른 모델/프롬프트로 분리
- ADK 외 자체 로직을 너무 많이 끼우면 ADK가 제공하는 trace·observability 이점을 잃음

---

## 5. 비교 분석

### vs 대안 접근

| 비교 항목 | ADK deep-search | LangGraph 기반 자체 구현 | OpenAI Assistants + Tools |
|-----------|----------------|------------------------|--------------------------|
| **장점** | 풀스택 샘플, GCP 배포 자동화 | 가장 유연, 벤더 중립 | 매니지드, 간단 |
| **단점** | Google 생태계 락인 | 보일러플레이트, 배포 별도 | 멀티 에이전트·HITL 직접 구현 필요 |
| **적합한 상황** | GCP/Gemini 사용 중, 빠른 PoC | 멀티 클라우드, 커스텀 워크플로 | 단일 에이전트 빠른 출시 |

### 선택 기준

- GCP/Gemini 인프라가 이미 있고 빠르게 PoC → ADK 샘플 채택
- 멀티 클라우드 또는 모델 중립 필요 → LangGraph 또는 ICM 같은 폴더 기반 접근
- 마케팅·세일즈용 단순 봇 → OpenAI Assistants

---

## 6. 학습 체크리스트

### 이해도 점검

- [ ] 2단계 워크플로(플래닝 vs 자율 실행)의 분리 이유를 설명할 수 있다
- [ ] planner/researcher/critic/composer 각 역할의 책임을 구분할 수 있다
- [ ] HITL 게이트가 비용/품질 측면에서 왜 중요한지 설명할 수 있다
- [ ] ADK의 어떤 컴포넌트(Agent/Tool/Session/Runner)가 어떻게 쓰이는지 코드에서 확인할 수 있다

### 추가 학습

- [ ] ADK 공식 문서 [adk.dev](https://adk.dev) 핵심 컨셉 정리
- [ ] `app/agent.py` 코드 직접 읽고 sub-agent 정의 패턴 추출
- [ ] Agent Engine 배포 후 trace·observability 기능 체험

---

## 7. References

- [GitHub: deep-search 샘플](https://github.com/google/adk-samples/tree/main/python/agents/deep-search)
- [adk-samples 레포 (Python 30+ 에이전트)](https://github.com/google/adk-samples)
- [ADK 공식 문서](https://adk.dev)
- [Agent Starter Pack](https://github.com/GoogleCloudPlatform/agent-starter-pack)
- 관련 노트: [[agent-garden]] · [[ai-ecosystem/01-overview]]
