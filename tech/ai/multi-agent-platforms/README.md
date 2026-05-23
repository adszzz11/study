# Multi-Agent Orchestration Platforms 비교 스터디

> "에이전트 1명"이 아니라 "에이전트 팀/조직"을 다루는 카테고리. Paperclip이 부상하면서 다시 관심받는 영역.

## 한 줄 정의

**Multi-Agent Orchestration Platform** = 여러 LLM 에이전트가 **역할을 나누어 협업**하도록 만드는 프레임워크/플랫폼. 단일 슈퍼 에이전트의 한계(컨텍스트 폭주, 도구 라우팅 실수, 비용 통제 부재)를 분업과 거버넌스로 해결한다.

## 3줄 요약

1. **분업 모델**: 한 명이 모든 모자를 쓰지 않고 책임을 분리 (예: PM·Engineer·QA 또는 Mail·PR·System 직원).
2. **오케스트레이션 패턴 4가지**: ① 회사형(Paperclip/Agency Swarm/MetaGPT) ② 크루형(CrewAI) ③ 그래프형(LangGraph) ④ 대화형(AutoGen/OpenAI Swarm).
3. **2026년 트렌드**: LangGraph가 프로덕션 표준으로 부상, Paperclip이 "예산·거버넌스 표준"으로 자리잡는 중.

## 📂 다루는 프로젝트 (8종)

| 폴더 | 프로젝트 | 패턴 | ★ | 언어 | 적합 사용처 |
|------|---------|------|------|------|------------|
| [paperclip/](paperclip/README.md) | **Paperclip** | 회사형 (employee) | 67k | TS+React | "AI 직원 N명 두고 자동화 운영" |
| [crewai/](crewai/README.md) | **CrewAI** | 크루형 (role-based) | 52k | Python | 빠른 프로토타입, 비즈니스 워크플로우 |
| [langgraph/](langgraph/README.md) | **LangGraph** | 그래프형 (stateful) | 33k | Python | 프로덕션 + 복잡 상태/체크포인트 |
| [autogen/](autogen/README.md) | **AutoGen / AG2** | 대화형 (GroupChat) | 58k | Python | 디베이트·합의 도출, Microsoft 생태계 |
| [agency-swarm/](agency-swarm/README.md) | **Agency Swarm** | 회사형 (CEO 메타포) | 4.4k | Python | OpenAI Agents SDK 기반 안정 운영 |
| [openai-swarm/](openai-swarm/README.md) | **OpenAI Swarm** | 핸드오프 (educational) | 22k | Python | 학습용. 실제로는 Agents SDK로 |
| [metagpt/](metagpt/README.md) | **MetaGPT** | SOP형 (software company) | 68k | Python | "한 줄 요구사항 → 코드 회사" |
| [dify/](dify/README.md) | **Dify** | 비주얼 워크플로우 | 142k | Py+TS | 노코드 + RAG + 멀티 에이전트 |

## 🆚 한 페이지 비교 매트릭스

| 축 | Paperclip | CrewAI | LangGraph | AutoGen | Agency Swarm | OpenAI Swarm | MetaGPT | Dify |
|----|-----------|--------|-----------|---------|--------------|--------------|---------|------|
| **추상화 단위** | Company/Agent | Crew/Agent/Task | Graph/Node/State | GroupChat/Agent | Agency/CEO/Agent | Agent/Handoff | Role/SOP | Workflow/Block |
| **유지보수 상태** | Active 🟢 | Active 🟢 | Active 🟢 | 🟡 maintenance | Active 🟢 | 🔴 superseded | Active 🟢 | Active 🟢 |
| **상태/체크포인트** | DB 큐 | Flows로 추가 | ⭐ Native | 약 | conversation | stateless | 약 | 워크플로우 |
| **예산 통제** | ⭐ Native | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | 부분 |
| **에이전트 런타임 자유** | ⭐ 무관 | Python 종속 | Python 종속 | Python 종속 | OpenAI Agents SDK | OpenAI | Python | Python |
| **노코드 UI** | 대시보드 | ✗ | LangSmith | Studio (β) | ✗ | ✗ | ✗ | ⭐ 캔버스 |
| **인간 in-the-loop** | 거버넌스 | 약 | ⭐ Native | 가능 | 가능 | 약 | 약 | 가능 |
| **셋업 부담** | 중 (PG 필요) | ⭐ 가벼움 | 중 | 중 | 가벼움 | ⭐ 가벼움 | 가벼움 | 중 (Docker) |
| **러닝 커브** | 낮음 | ⭐ 낮음 | 높음 | 중 | 낮음 | ⭐ 낮음 | 중 | 낮음 |

## 🧭 의사결정 플로우

```
질문 1: "내가 작성·운영할 것이 코드인가 시스템인가?"
   ├─ 코드 — 프로덕션 에이전트 시스템을 직접 작성
   │     └─ 질문 2A: 상태 복잡도?
   │         ├─ 단순/선형 → CrewAI (20줄로 시작)
   │         ├─ 그래프/조건 → LangGraph (체크포인트·HITL)
   │         └─ 대화/합의 → AutoGen/AG2
   │
   └─ 시스템 — 여러 에이전트를 "운영"하는 환경 구축
         └─ 질문 2B: 거버넌스/예산이 중요한가?
             ├─ 매우 — Paperclip (회사 메타포 + 예산 hard-stop)
             ├─ 적당 — Agency Swarm (CEO+직원 + Python으로 코딩)
             └─ 노코드 우선 — Dify (캔버스)
```

## 🎯 사용자 케이스(맥미니 자치 운영)에 매핑

| 컴포넌트 | 추천 | 이유 |
|----------|------|------|
| **관제탑/예산/거버넌스** | **Paperclip** | 직원별 예산 hard-stop, 다양한 런타임 통합 |
| **대화형 비서 (chief)** | Hermes Agent (별도 카테고리) | Paperclip 직원으로 등록 |
| **도메인 자동화 직원들** | Hermes 인스턴스 또는 CrewAI 마이크로 크루 | CrewAI는 작은 협업이 자연스러움 |
| **시스템 관리 (sysadmin)** | Bash/Python 어댑터 + Paperclip | LLM 없이도 직원으로 채용 가능 |
| **시각 대시보드** | Paperclip 내장 + Dify (선택) | |
| **장기 기억** | Letta (별도 카테고리) | 모든 직원이 공유 메모리 참조 |

## 📚 학습 순서 추천

| 일차 | 학습 |
|------|------|
| Day 1 | 본 README + paperclip/01-overview |
| Day 2-3 | Paperclip full study + CrewAI overview |
| Day 4 | LangGraph (프로덕션 패턴 이해) |
| Day 5 | Agency Swarm vs MetaGPT 비교 (회사형 패턴 깊이) |
| Day 6 | AutoGen, OpenAI Swarm 빠르게 훑기 |
| Day 7 | Dify hands-on (비주얼 워크플로우 체험) |
| Day 8+ | 실전: Paperclip을 맥미니에 띄우고 직원 1명 등록 |

## 🔗 인접 학습

- [[study/tech/ai/openclaw-study]] — 메신저 게이트웨이형 (다른 카테고리, 직원으로 채용 가능)
- [[study/tech/ai/agent-orchestration]] — CLI 에이전트 오케스트레이션 (Claude Squad 등, 다른 카테고리)
- [[study/tech/ai/langchain-crewai]] — 기존 vault 자료 보강 참고
- [[study/tech/ai/mastra]] — TS 기반 AI 프레임워크

## ⚠️ 카테고리 함정

1. **AutoGen은 v0.2/v0.4 분기**가 있음. 본가 microsoft/autogen은 maintenance 모드. ag2ai/ag2로 fork가 활동 — 둘 다 다룰 것.
2. **OpenAI Swarm은 superseded** 됨. 새로 쓰는 코드는 OpenAI Agents SDK로 가야 함. Swarm 자료는 학습용으로만.
3. **LangChain vs LangGraph 혼동**: LangGraph는 LangChain Inc 작품이지만 독립 사용 가능. LangChain의 AgentExecutor는 legacy로 deprecated 중.
4. **CrewAI vs Agency Swarm 헷갈림**: 둘 다 역할 기반이지만 CrewAI는 process(sequential/hierarchical) 선택, Agency Swarm은 명시적 통신 채널(`>` 연산자).

Sources:
- [awesome-agent-orchestrators](https://github.com/andyrewlee/awesome-agent-orchestrators)
- [awesome-ai-agents-2026](https://github.com/Zijian-Ni/awesome-ai-agents-2026)
- [appintent: 11 Best Agentic Orchestration Platforms 2026](https://www.appintent.com/software/ai/agentic-orchestration/)
- [openagents.org: Open Source AI Agent Frameworks Compared 2026](https://openagents.org/blog/posts/2026-02-23-open-source-ai-agent-frameworks-compared)
