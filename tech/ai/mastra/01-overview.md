---
date: 2026-05-17
tags:
  - tech
  - ai
  - mastra
status: studying
---

# 01. Overview — What & Why

> 이 문서는 "Mastra가 무엇이며, 왜 만들어졌고, 어떤 문제를 푸는가"를 설명합니다.

---

## 1. 기본 정보

| 항목 | 내용 |
|------|------|
| 공식 사이트 | https://mastra.ai |
| GitHub | https://github.com/mastra-ai/mastra |
| 라이선스 | Elastic License 2.0 (오픈소스, 상업적 사용 가능) |
| 첫 릴리스 | 2024년 10월 |
| 1.0 릴리스 | 2026년 1월 |
| GitHub Stars | 22,000+ (1.0 시점) |
| Weekly Downloads | 300,000+ npm (1.0 시점) |
| 개발사 | Gatsby 창립 팀 |
| 주 언어 | TypeScript |
| 기반 | Vercel AI SDK |

---

## 2. What — 한 문장 정의

> **"AI 에이전트와 워크플로우를 TypeScript로 짤 때 필요한 모든 프리미티브를 한 박스에 담아둔, 프로덕션 지향 프레임워크."**

비유하면:

- LangChain (Python) ↔ **Mastra (TypeScript)**
- Next.js가 React에게 한 일을 → Mastra가 Vercel AI SDK에 하고 있음
- "LLM 호출 라이브러리" 가 아니라 **"AI 앱 풀스택 프레임워크"**

---

## 3. Why — 등장 배경

### 풀어야 했던 문제

1. **Python 중심의 에이전트 생태계** — 웹 개발자(특히 TS 백엔드/프론트엔드 풀스택)는 LangChain.js를 쓰거나 직접 OpenAI SDK를 호출해야 했고, 양쪽 모두 production-ready한 구조가 부족.
2. **추상화 파편화** — Vercel AI SDK는 LLM 호출/스트리밍/툴 콜링은 잘 추상화했지만, **Memory · RAG · Workflow · Evals**는 사용자가 직접 짜야 함.
3. **운영 도구 부재** — Eval, Tracing, Studio(시각화)를 매번 LangSmith/LangFuse/Braintrust로 외주.
4. **결정적 vs 비결정적 분리 부재** — "LLM이 알아서 결정"하는 Agent와 "내가 짜둔 그래프대로 실행"하는 Workflow가 한 추상화에 섞여 있었음.

### Mastra가 내놓은 답

| 문제 | Mastra의 해결 방식 |
|------|----------------------|
| Python 의존 | TypeScript-native, Node.js/Bun/Edge 모두 동작 |
| 추상화 파편화 | 6대 프리미티브를 `@mastra/core` 하나에 통합 |
| 운영 도구 | Studio + AI Tracing + Scorers 내장 |
| Agent vs Workflow 혼재 | **명시적으로 분리** — Agent는 LLM이 결정, Workflow는 그래프로 결정 |
| 스키마 락인 | Zod / Valibot / ArkType 모두 지원 (Standard JSON Schema) |

---

## 4. 6대 프리미티브 (한눈에)

```
┌─────────────────────────────────────────────────────────────┐
│                       Mastra Instance                       │
│  (logger, telemetry, storage, agent registry, vector store) │
├─────────────┬─────────────┬─────────────┬─────────────┬─────┤
│   Agents    │  Workflows  │    Tools    │   Memory    │ RAG │
│             │             │             │             │     │
│  LLM 루프    │  결정적     │  외부 호출   │  4계층      │     │
│  reasoning  │  그래프     │  + MCP      │  message/   │     │
│             │  실행 엔진   │             │  working/   │     │
│             │             │             │  semantic/  │     │
│             │             │             │  obs.       │     │
└─────────────┴─────────────┴─────────────┴─────────────┴─────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │   Evals (Scorers)      │
                  │   Tracing (OTEL)       │
                  │   Studio (UI)          │
                  └────────────────────────┘
```

| 프리미티브 | 한 줄 설명 | 패키지 |
|-----------|-----------|--------|
| **Agent** | LLM + 도구를 사용해 open-ended 태스크를 푸는 자율 루프 | `@mastra/core/agent` |
| **Workflow** | 입력/출력 스키마가 정의된 결정적 그래프 (`.then`, `.branch`, `.parallel`) | `@mastra/core/workflows` |
| **Tool** | Zod 스키마 + `execute` 함수로 정의되는 호출 가능한 유닛 | `@mastra/core/tools` |
| **Memory** | 4계층(message history / working / semantic recall / observational) | `@mastra/memory` |
| **RAG** | `MDocument` → chunk → embed → vector store → query | `@mastra/rag` + `@mastra/pg` 등 |
| **Evals (Scorers)** | LLM-judge / rule-based / statistical 평가, sampling rate 기반 비동기 실행 | `@mastra/evals` |

각 프리미티브의 깊이 있는 내용은 다음 문서들에서 다룹니다 — [[03-agents-workflows]], [[04-memory-rag]], [[05-tools-mcp]], [[06-evals-observability]].

---

## 5. 어디에 쓰이고 있나 (Production References)

공식 사이트가 공개한 사례:

- **Replit** — Agent3 (개발 자동화)
- **Sanity** — CMS 컨텐츠 자동화
- **Factorial, SoftBank** — 내부 코파일럿 / 생산성
- **Index, PLAID Japan** — 자연어 데이터 분석 에이전트
- **StarSling** — DevOps 자동화
- **Counsel Health, Cedar** — 의료 도큐멘테이션
- **Medusa, Vetnio, Lua** — 고객 응대 에이전트

> **시사점**: "ChatGPT 클론" 수준이 아닌, **B2B SaaS에 내장된 에이전트**가 주 유스케이스. 따라서 Mastra는 Eval/Tracing/Memory 같은 운영 기능에 무게중심이 있다.

---

## 6. 언제 적합한가 / 부적합한가

### ✅ 적합

- TypeScript/Node.js 백엔드 또는 Next.js 풀스택 프로젝트
- 에이전트를 **제품에 내장**해야 하는 경우 (SDK처럼)
- Workflow와 Agent를 **명확히 분리**하고 싶을 때
- 자체 호스팅 또는 Mastra Cloud 둘 다 고려하는 경우

### ❌ 부적합

- Python 생태계 라이브러리(LlamaIndex 고급 파서, PEFT, Unsloth 등)가 필수일 때
- 단발성 LLM 호출만 필요한 경우 (그냥 OpenAI SDK가 낫다)
- LangGraph 수준의 cyclic graph가 핵심인 경우 — Mastra Workflow는 DAG 기반

---

## 7. 다음 문서

- [[02-architecture]] — 내부 컴포넌트가 어떻게 맞물려 돌아가는지
- [[03-agents-workflows]] — Agent 클래스와 Workflow 그래프 엔진 깊이 학습
