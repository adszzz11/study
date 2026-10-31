---
date: 2026-06-23
tags:
  - tech
  - ai
  - notebooklm
  - deep-dive
  - architecture
type: tech-tool-study
parent: "[[../README]]"
---

# NotebookLM 연동 가능성 - 심화

> [[01-getting-started|이전: 시작하기]] | [[../README|목차로 돌아가기]] | [[../05-projects|다음: 프로젝트]]

---

## 1. 핵심 설계 판단

NotebookLM을 시스템에 붙일 때 가장 먼저 구분해야 하는 질문은 다음이다.

| 질문 | NotebookLM 적합 | API RAG 적합 |
|------|------|------|
| 사람이 research UI에서 탐색하는가? | 높음 | 중간 |
| backend가 자동으로 답변을 생성/저장해야 하는가? | 낮음 | 높음 |
| source-grounded citation UX가 중요한가? | 높음 | 높음 |
| Audio/Video Overview가 필요한가? | 높음 | 낮음 |
| 권한, logging, eval, CI가 중요한가? | 중간 | 높음 |

결론:

- **NotebookLM은 사용자-facing research workspace**로 본다.
- **Gemini API/Agent Search/OpenAI File Search는 developer-facing backend**로 본다.

## 2. Drive 기반 semi-automation 상세

### 권장 흐름

```text
Batch job
  -> Generate structured source documents
  -> Upload/update Google Drive folder
  -> Human imports Drive files once in NotebookLM
  -> NotebookLM syncs updated source content
  -> Human uses chat, citations, overviews
```

### 문서 작성 규칙

- 문서 제목에 날짜, 시스템 이름, 범위를 넣는다.
- section heading을 질문 가능한 단위로 쪼갠다.
- 표에는 컬럼 설명을 붙인다.
- 이미지에만 핵심 정보가 들어가지 않게 한다.
- append-only log와 latest summary를 분리한다.

예시:

```markdown
# Daily Research Report - 2026-06-23

## Scope

이 문서는 NotebookLM 연동 가능성 검토 결과를 요약한다.

## Decision

공식 공개 NotebookLM API 직접 연동은 사용하지 않는다.
MVP는 Google Drive source sync로 구현한다.

## Evidence

| Evidence | Source | Implication |
|---|---|---|
| Drive files sync after import | NotebookLM source help | semi-automation 가능 |
| Web URL imports text only | NotebookLM source help | report는 text 중심이어야 함 |
```

## 3. Web URL source 설계

Web URL import는 간단하지만, 웹페이지 전체를 crawler처럼 읽는다고 가정하면 안 된다.

| 항목 | 설계 기준 |
|------|------|
| HTML text | 핵심 내용을 본문 text로 제공 |
| Images | alt text나 별도 caption으로 의미 보강 |
| Embedded videos | NotebookLM이 자동으로 video content를 이해한다고 기대하지 않음 |
| Nested pages | 링크된 하위 page는 별도 source로 추가 |
| Paywall/auth | 접근 제한 page는 source로 부적합 |
| PDF URL | PDF source로 처리될 수 있으므로 layout 품질 확인 |

## 4. 대체 RAG 아키텍처

### Gemini API 패턴

```text
App
  -> Upload document to Gemini Files API
  -> Ask question with document context
  -> Request structured answer + citations/quotes
  -> Store response and evaluation metadata
```

적합한 경우:

- Google ecosystem을 유지하고 싶다.
- PDF/document understanding이 중요하다.
- NotebookLM artifacts보다 API control이 중요하다.

### Google Cloud Agent Search 패턴

```text
Enterprise sources
  -> Data store / indexing
  -> Semantic search + generated answers
  -> IAM/access control
  -> App integration
```

적합한 경우:

- 조직 문서가 많다.
- 권한, audit, data governance가 중요하다.
- Cloud 운영 비용과 설계를 감당할 수 있다.

### OpenAI File Search 패턴

```text
App
  -> Vector store
  -> File upload
  -> Responses API with file_search
  -> Answer with retrieved citations
```

적합한 경우:

- 개발자 친화적인 API와 빠른 PoC가 필요하다.
- 기존 backend가 OpenAI Responses API 중심이다.
- NotebookLM UX보다 product integration이 중요하다.

## 5. 보안/프라이버시 체크

| 체크 | 개인 계정 | Workspace/Education | Enterprise |
|------|------|------|------|
| human review/training | feedback 제공 시 내용 사용 가능성 확인 | uploads/queries/responses 비사용 안내 확인 | enterprise privacy 조건 확인 |
| access control | 개인 계정 공유 범위 주의 | 조직 policy 적용 | IAM/VPC-SC 등 검토 |
| source ownership | 개인 Drive 소유 | 조직 Drive 권장 | managed repository 권장 |
| audit/logging | 제한적 | 관리자 설정 의존 | Cloud audit 설계 가능 |

## 6. 피해야 할 설계

- NotebookLM 웹 UI를 browser automation으로 조작해 production integration처럼 사용하는 설계
- 중요한 내용을 이미지나 embedded content에만 넣는 source 설계
- NotebookLM 결과를 backend truth로 저장해야 하는데 수동 copy/paste에 의존하는 설계
- 개인 Google 계정에 민감한 회사 문서를 올리고 privacy 정책을 확인하지 않는 운영
- source limit, file size, sync latency를 측정하지 않고 대규모 rollout하는 방식

## 관련 노트

- [[study/tech/ai/model-context-protocol-mcp]] - tool/API 연결을 표준화해야 할 때 참고
- [[study/tech/ai/litellm]] - 여러 LLM/RAG backend를 routing해야 할 때 참고
- [[study/tech/ai/ai-ecosystem]] - NotebookLM과 programmable RAG의 역할 분류
