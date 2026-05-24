---
date: 2026-05-17
tags:
  - tech
  - tool
  - ai
  - agent-framework
  - typescript
status: studying
type: tech-tool-study
---

# Mastra — TypeScript AI Agent Framework

> **한 줄 소개**: Gatsby 팀이 만든 오픈소스 TypeScript 에이전트 프레임워크. Agents · Workflows · Memory · RAG · Tools · Evals 6개 프리미티브를 Vercel AI SDK 위에서 통합 제공.

---

## 학습 경로 (Learning Path)

이 폴더는 **아키텍처 학습** 관점으로 구성되어 있습니다. 위에서 아래로 읽으면 됩니다.

| 단계 | 파일 | 내용 | 누구를 위한가 |
|------|------|------|----------------|
| 0 | [[README]] | 전체 맵 / 학습 로드맵 | 모두 |
| 1 | [[01-overview]] | What/Why, 등장 배경, 6대 프리미티브 | 입문자 |
| 2 | [[02-architecture]] | 전체 아키텍처 다이어그램, 실행 흐름 | 중급자 |
| 3 | [[03-agents-workflows]] | Agent 클래스 · Workflow 그래프 엔진 (코드 심화) | 실무 적용 |
| 4 | [[04-memory-rag]] | Memory 4계층 + RAG 파이프라인 | 실무 적용 |
| 5 | [[05-tools-mcp]] | createTool, MCP Client/Server, 통합 패턴 | 실무 적용 |
| 6 | [[06-evals-observability]] | Scorers, AI Tracing, OTEL | 운영 |
| 7 | [[07-case-studies]] | 프로덕션 사례 (Replit·Sanity·Factorial·Cedar·WorkOS·11x) | 실무 적용 |
| 8 | [[cheatsheet]] | 핵심 API 빠른 참조 | 모두 |
| 9 | [[99-references]] | 공식 문서, GitHub, 튜토리얼 링크 | 모두 |

---

## TL;DR — 30초 요약

- **무엇인가**: LangChain의 TypeScript 진영판. Next.js처럼 "프레임워크 + 스튜디오 + 호스팅"이 한 세트.
- **왜 쓰나**: Vercel AI SDK 위에 *프로덕션에 필요한* 6대 프리미티브(에이전트/워크플로우/메모리/RAG/툴/평가)를 표준 API로 묶어둠. Zod 스키마가 곧 모델에게 보여줄 description이 된다.
- **핵심 차별점**:
	1. **TypeScript-native** — 백엔드/프론트엔드 같은 코드베이스
	2. **그래프 기반 결정적 Workflow** — Agent의 비결정성과 분리
	3. **Studio + AI Tracing 내장** — 별도 LangSmith 없이도 디버깅 가능
	4. **Standard JSON Schema** — Zod / Valibot / ArkType 모두 지원
- **언제 안 쓰나**: 파이썬 생태계가 필수일 때(LlamaIndex, LangGraph), 단순 챗봇 1개만 만들 때.

---

## 학습 체크리스트

### 아키텍처 이해
- [ ] 6대 프리미티브(Agent, Workflow, Tool, Memory, RAG, Evals)가 각각 무엇인지 설명할 수 있다
- [ ] Agent와 Workflow를 언제 각각 써야 하는지 구분할 수 있다
- [ ] `Mastra` 인스턴스가 왜 필요한지(공유 리소스) 설명할 수 있다

### 핵심 코드 패턴
- [ ] `new Agent({...})` 와 `createTool({...})` 의 시그니처를 안다
- [ ] `createWorkflow().then().branch().commit()` 체이닝을 이해한다
- [ ] `Memory` 의 `resourceId` / `threadId` 스코핑 규칙을 안다
- [ ] `MDocument.fromText().chunk()` → embed → `PgVector.upsert()` 흐름을 안다

### 운영
- [ ] Scorer를 agent에 붙여 sampling rate 기반으로 평가하는 방법을 안다
- [ ] OTEL Exporter / Bridge의 차이를 안다

---

## 관련 노트

- [[../langchain-crewai/01-overview|LangChain·CrewAI 비교]]
- [[../ai-ecosystem/|AI 에이전트 생태계 전반]]
- [[../claude/|Claude Agent SDK]]
