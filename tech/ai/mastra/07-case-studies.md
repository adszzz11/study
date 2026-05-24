---
date: 2026-05-24
tags:
  - tech
  - mastra
  - case-study
  - production
parent: "[[README]]"
---

# Mastra Case Studies — 프로덕션 활용 사례

> [[README|목차로 돌아가기]] | [[06-evals-observability|이전: Evals & Observability]] | [[99-references|다음: References]]

이 노트는 Mastra를 **실제 프로덕션에서 잘 쓰고 있는 회사들의 기술 디테일**을 정리한다. 단순 도입 목록이 아니라, 각 팀이 (1) 어떤 문제를 풀었고, (2) Mastra의 어떤 프리미티브를 어떻게 조합했는지, (3) 무엇을 배웠고 무엇을 피하라 권하는지 중심으로 본다.

---

## 1. Replit Agent 3 — 메타 에이전트 & 컨테이너 네이티브

> Replit이 사용자 요청을 받아 **Mastra 에이전트를 동적으로 만들어 주는** 메타 에이전트 시스템

### 문제

- "Agents & Automations" 기능에서 사용자가 자연어로 원하는 워크플로를 묘사하면, 에이전트가 자동으로 **Mastra 코드를 생성**해 새 에이전트를 띄워야 함
- 서버 장애나 장시간 실행(최대 **200분**)에도 워크플로가 끝까지 가야 함

### Mastra 사용 패턴

| 요소 | 활용 |
|------|------|
| **Agents/Workflows** | Agent 3가 사용자 요청을 받아 다른 Agent + Workflow 코드 자체를 생성 |
| **컨테이너 네이티브** | 각 사용자 = Docker sandbox + Postgres + storage (일 수천 개) |
| **MCP docs 서버** | Replit 인프라와 자연스럽게 매칭 |
| **Inngest durable execution** | 서버 중간에 죽어도 워크플로 완료 보장 |
| **Composable tools** | Tool이 Agent를 호출하고 Agent가 Tool을 호출 — 메타 에이전트 패턴 가능 |

### 핵심 메커니즘

- **Self-testing 루프**: Playwright로 생성된 코드 실행 → 에러 잡기 → 수정 → 재실행 — "3x 빠르고 10x 비용 효율적"
- **이벤트 기반 실행**: Mastra의 워크플로 엔진이 내부적으로 이벤트 시스템 위에서 동작 (대부분의 개발자는 의식하지 않아도 됨)

### 수치로 본 효과

| 지표 | 값 |
|------|-----|
| 자율성 | **90%** |
| 워크플로 성공률 (Inngest 전후) | 80% → **96%** |
| 자율 실행 최대 길이 | 200분 |
| 일일 컨테이너 수 | 수천 개 |
| 자체 테스트 효율 | 3x 속도, 10x 비용 |

### 가져갈 인사이트

- **메타 에이전트 패턴**: 사용자에게 빈 에이전트를 주는 대신, "당신의 에이전트를 만들어주는 에이전트"가 더 강력
- Mastra의 워크플로 영속성을 외부 시스템(Inngest)과 조합하면 신뢰성이 한 단계 점프 (80→96%)

---

## 2. Sanity Content Agent — CMS 스키마를 이해하는 에이전트

> CMS 안에서 "스키마 그래프"를 기반으로 콘텐츠를 만들고 수정하는 에이전트

### 문제

- 일반 챗봇은 Sanity의 콘텐츠 모델·참조 관계를 이해 못 함 → 생성된 콘텐츠가 스키마 위반
- 35개 툴을 단일 에이전트에 몰아넣자 의사결정 품질 저하

### Mastra 사용 패턴

| 요소 | 활용 |
|------|------|
| **WebSocket 스트리밍** | CMS UI 안에서 실시간 응답 |
| **Runtime Context** | 세션 데이터·권한 전달 |
| **stream method에 tool 직접 전달** | 응답하면서 동시에 툴 사용 |
| **멀티 에이전트** | mutation 같은 discrete 작업에만 서브에이전트 분리 |
| **Temporal + Redis 캐시** | "스키마 그래프"를 백그라운드로 계산·캐시 |

### 핵심 아키텍처 결정 (실험 결과)

**시도 1**: 단일 에이전트에 35개 툴 몰아넣기 → 의사결정 노이즈

**시도 2**: 기능별 서브에이전트로 쪼개기 → **"서브에이전트가 컨텍스트를 너무 잃음"**

**최종**: 대부분을 단일 메인 에이전트로 되돌리고, **mutation 같은 discrete 작업만 서브에이전트**로 분리. Bulk operation은 Temporal로 병렬 처리하되, **사용자가 검토할 수 있는 staging bundle** 단계를 끼움.

### 핵심 기능

1. 콘텐츠 관계 탐색 (참조 그래프 따라가기)
2. **스키마 유효한** 문서 생성 (필드 타입·참조까지 정확)
3. 이미지 변환 (제품 색상 변형, 시장별 비주얼, 브랜드 가이드라인)
4. 콘텐츠 갭 식별 (외부 소스 조사 → 기존 콘텐츠와 교차)

### 가져갈 인사이트

- **"무조건 서브에이전트로 쪼개기" 함정 주의** — 컨텍스트 손실로 오히려 품질이 떨어짐
- **discrete task만 서브에이전트**, 나머지는 단일 에이전트
- 도메인 메타데이터(스키마 그래프)는 **외부 캐시(Redis)에 미리 계산**해두면 에이전트 응답 빨라짐

---

## 3. Factorial — 권한을 자동으로 존중하는 HR 에이전트

> 수백 개의 granular permission이 있는 HR 플랫폼에서 에이전트가 권한 시스템을 우회하지 않게 만든 사례

### 문제

- 고객사 사용자가 ChatGPT 같은 외부 LLM에 민감한 HR 데이터를 붙여넣는 일이 빈번 → 데이터 노출 위험
- 에이전트 자체에 별도 권한 시스템을 만들면 **사용자 권한과의 drift**가 발생

### Mastra 사용 패턴

| 요소 | 활용 |
|------|------|
| TypeScript 네이티브 | 기존 Factorial 백엔드와 동일 스택 |
| **Memory** | 대화 간 컨텍스트 유지 |
| **Workflows** | LLM 라우팅 분기 |
| Provider Integrations | LLM 프로바이더 추상화 |
| CopilotKit `useCoAgent` | 실시간 UI 상태 공유 |
| Braintrust | 평가·관찰성 (Mastra 외부 도구) |

### 핵심 디자인 결정

**"에이전트는 프론트엔드와 동일한 GraphQL API를 호출한다"** — 별도 권한 레이어 없음. 에이전트가 다른 클라이언트 앱처럼 취급되므로 권한 시스템이 자동으로 적용됨. 사용자 권한과 AI 권한 사이에 drift가 발생할 수 없는 구조.

### 프롬프트·툴 전략

- **Dynamic schema discovery → Deterministic tools**: 에이전트가 동적으로 쿼리를 구성하지 않고, 비즈니스 개념 단위의 deterministic tool을 호출 (예: `getEmployeeAbsences(employeeId, dateRange)`)
- **TSV vs JSON**: 토큰 사용량 30-40% 감소 + recall 향상 (구조화된 표 데이터)
- **할루시네이션 방지**: 모를 때는 "I don't know, please ask a human"
- **컨텍스트 재사용**: 후속 질문에서 이전 대화·결과 자동 활용

### 가져갈 인사이트

- **권한은 코드가 아니라 API 경계에서 풀어라** — 에이전트를 또 하나의 클라이언트로 취급하면 권한 시스템 재구현이 불필요
- **TSV** 같은 토큰 효율적인 포맷은 비용·정확도 양쪽에 이득
- 의도적 "I don't know" 응답이 신뢰도를 만든다

---

## 4. Cedar — 멀티 에이전트 온보딩 코파일럿

> 튜토리얼 영상·popover 대신, 실제 사용자 워크스페이스 위에서 단계별로 자동 셋업해주는 코파일럿

### 문제

- 일반 온보딩은 "이걸 클릭하세요" 영상·팝업으로 끝남
- 사용자가 실제 자기 데이터로 첫 작업을 끝낼 때까지 가지 못함

### "Agent Army" 아키텍처

```
              ┌─────────────────────┐
              │   Supervisor Agent  │
              │  (orchestration)    │
              └──────────┬──────────┘
                         │ delegate
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
   Chat Agent     UI Instruction    DOM Expert
  (Q&A 대응)       Agent (가이드)    Agent (페이지 상태)
                                          │
                                          ▼
                                 Element-Pinpointing
                                 Agent (클릭 대상)
```

Supervisor가 작업을 위임 → 각 전문 에이전트가 응답 → Supervisor가 결과 조립 → 다음 단계 또는 사용자에게 결과 전달.

### Mastra 사용 패턴

| 요소 | 활용 |
|------|------|
| **Streaming** | 실시간 응답 |
| **Agent orchestration** | Supervisor의 위임/조립 패턴 |
| **Modular workflow construction** | 각 전문 에이전트가 독립적인 워크플로 |

### 가져갈 인사이트

- **"orchestration layer" 패턴**: 워크플로를 직접 짜는 게 아니라 supervisor 에이전트에게 위임 (= LLM이 라우터 역할)
- 사용자의 DOM 상태 같은 **휘발성·동적 컨텍스트**는 전용 에이전트(DOM expert)로 분리하면 메인 에이전트가 단순해짐

---

## 5. WorkOS — GTM 자동화 + MCP 조합

> Sales / GTM 팀의 prospect 데이터 처리 자동화

### 사례 1: Prospect 정제 에이전트

- **입력**: 잡다한 비정형 prospect 데이터
- **처리**: 회사·인물 식별 → enrichment → 정제된 테이블 출력
- **MCP 활용**: Cargo(enrichment provider)를 MCP 서버로 연결 → 에이전트가 자율적으로 enrichment tool 선택

### 사례 2: 컨퍼런스 발표자 스크래핑

- 컨퍼런스 사이트 URL → 발표자 정보 추출 → target persona 필터 → 정형화

### Mastra 사용 패턴

| 요소 | 활용 |
|------|------|
| **MCP Integration** | 외부 enrichment provider(Cargo) 자율 호출 |
| **Playground** | 워크플로 변형 테스트·데모 |
| **Mastra Cloud** | 간편 배포 |

### 가져갈 인사이트

- **MCP를 enrichment 레이어로**: 외부 데이터 소스를 MCP 서버로 노출하면 에이전트가 자율적으로 선택 — "어떤 tool을 호출할지" 결정을 LLM에게 맡길 수 있음
- Mastra를 **기존 도구 위의 custom abstraction layer**로 활용 (vendor-specific 코드 격리)

---

## 6. 11x Alice — AI SDR (일 5만 건 이메일)

> 자율 lead 소싱·리서치·이메일 개인화 SDR 에이전트

### 문제

- 단순 캠페인 생성 도구에서 **진짜 자율 SDR**로 진화 필요
- 사람 SDR 수준 (2% 회신율) 달성

### 아키텍처 실험

| 시도 | 결과 |
|------|------|
| ReAct 패턴 | 부적합 |
| Workflow 기반 | 부적합 |
| **Hierarchical Multi-Agent** | ✅ 채택 |

특화 서브에이전트들이 lead sourcing / research / personalization 각각을 담당. **3개월** 만에 처음부터 재구축 완료.

### 수치

- **5만+** AI 이메일/일
- **수백만** lead·메시지 처리
- 회신율 **2%** (사람 SDR 수준)

### 가져갈 인사이트

- "어떤 아키텍처가 좋은가"는 **3가지 실험해서 비교**한 결과로 정해라 (도그마 대신 실험)
- Mastra의 hierarchical multi-agent 패턴은 **명확한 책임 분리가 가능한 도메인** (영업 자동화 같은)에서 잘 작동

---

## 횡단 패턴 — 5개 사례 공통점

### 1. 어떤 Mastra 프리미티브가 가장 많이 쓰였나

| 프리미티브 | 사례 |
|-----------|------|
| **Agents (단일/멀티)** | 전부 |
| **Workflows** | Replit, Factorial, Cedar |
| **Memory** | Factorial, Sanity |
| **Streaming** | Sanity, Cedar |
| **MCP** | WorkOS, Replit (docs 서버) |
| **Tool 동적 생성** | Replit |
| **외부 영속성 (Inngest)** | Replit |
| **외부 캐시 (Redis)** | Sanity |
| **외부 평가 (Braintrust)** | Factorial |

### 2. 반복되는 디자인 결정

- **API 경계에서 권한 풀기** (Factorial) — 에이전트도 그냥 또 하나의 클라이언트
- **Discrete task만 서브에이전트로** (Sanity) — 무조건 분해 X
- **Supervisor 패턴** (Cedar, Replit) — 라우팅을 LLM에게 위임
- **Deterministic tools > Dynamic queries** (Factorial) — 비즈니스 개념 단위 툴
- **외부 영속성·캐시·평가** — Mastra 안에 다 끼우려 하지 말고 검증된 인프라(Inngest/Redis/Braintrust)와 조합

### 3. Anti-pattern (사례에서 직접 학습한 것)

- 무조건 멀티 에이전트로 쪼개기 → 컨텍스트 손실 (Sanity)
- 한 에이전트에 30+개 툴 몰아넣기 → 선택 정확도 저하 (Sanity)
- 에이전트에 별도 권한 시스템 만들기 → drift 위험 (Factorial)
- "I don't know" 없이 자신감 있게 답하기 → 할루시네이션 (Factorial)
- 도그마로 아키텍처 결정 → 11x는 3개 실험 후 결정

---

## 우리 조직에 적용한다면

> 카테고리별 추천 출발점

| 우리 상황 | 참고할 사례 | 첫 액션 |
|----------|------------|---------|
| 사내 도메인 도구 + 권한 시스템 있음 | **Factorial** | 기존 GraphQL/REST API를 그대로 에이전트 클라이언트로 사용 |
| CMS·문서 시스템 | **Sanity** | 스키마 그래프를 외부 캐시에 미리 계산 |
| 사용자 자동화 빌더 | **Replit** | Inngest로 워크플로 영속성 확보 |
| 온보딩·튜토리얼 | **Cedar** | DOM 상태 전용 에이전트 분리 |
| 영업·GTM | **11x, WorkOS** | 3개 아키텍처 실험 후 hierarchical multi-agent |

---

## References

- [Mastra Customers 카테고리](https://mastra.ai/blog/category/case-studies)
- [Replit Agent 3 deep dive](https://mastra.ai/blog/replitagent3)
- [Sanity Content Agent](https://mastra.ai/customers/sanity)
- [Factorial — Permission-respecting agent](https://mastra.ai/blog/factorial-case-study)
- [Cedar — Multi-agent copilots](https://mastra.ai/blog/cedar-case-study)
- [WorkOS — From Evaluating to Teaching](https://mastra.ai/blog/workos-teaching-mastra)
- [11x Alice — Multi-Agent SDR (ZenML LLMOps DB)](https://www.zenml.io/llmops-database/rebuilding-an-ai-sdr-agent-with-multi-agent-architecture-for-enterprise-sales-automation)
- [Mastra Prompting Guide (SurePrompts)](https://sureprompts.com/blog/mastra-prompting-guide)
- 관련 노트: [[03-agents-workflows]] · [[05-tools-mcp]] · [[06-evals-observability]]
