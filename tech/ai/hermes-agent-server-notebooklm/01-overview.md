---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Hermes Agent Server와 NotebookLM — Overview

> [[README|목차로 돌아가기]] · [[02-ecosystem|다음: Ecosystem]]

## What

이 노트에서 Hermes Agent Server는 Nous Research의 `hermes-agent` API Server를 뜻한다. Hermes는 terminal, file, web search, memory, skills를 가진 agent를 OpenAI-compatible HTTP endpoint로 노출한다.

NotebookLM은 추가한 source를 중심으로 답하고 요약·질문·quiz·Audio/Studio 산출물을 만드는 학습 도구다. 둘을 직접적인 memory 동기화 대상으로 보지 않고, **Hermes의 연구 산출물을 NotebookLM이 읽는 source로 발행**하는 구조로 연결한다.

## Why

| 문제 | 분리된 역할로 푸는 방법 |
|---|---|
| 세션에서 얻은 정보가 다음 학습에 재사용되지 않음 | Hermes가 Study Note 초안을 만든다. |
| agent memory에 원문과 추론이 뒤섞임 | operational memory에는 현재 작업 사실만, 학습 기록에는 provenance를 남긴다. |
| 요약을 믿기 어렵고 재검증이 어려움 | 주장·근거·원문 URL·확신도·open question을 분리한다. |
| 문서를 고쳐도 NotebookLM source가 낡음 | Drive의 Google Doc을 연결해 auto-sync를 사용한다. |

`MEMORY.md`와 `USER.md`는 각각 약 2,200자와 약 1,375자로 의도적으로 작다. 따라서 장기 지식 base가 아니라 “지금 agent가 일을 잘 하기 위해 필요한” curated memory로 취급한다.

## 핵심 특징

### 1. 사람 검토가 들어가는 publishing boundary

Hermes가 만든 초안은 곧바로 permanent memory나 NotebookLM source가 되지 않는다. claim과 source URL을 확인하고, agent의 해석과 source가 말한 사실을 나눈 뒤 승인해 발행한다.

```text
Raw research → Draft → Verify → Human approval → Google Doc → NotebookLM
```

### 2. 주제별 living Google Doc

문서 하나를 주제 하나에 대응시킨다. 문서 상단에는 최소한 다음을 둔다.

```markdown
Updated: 2026-09-20
Scope: RAG evaluation fundamentals
Source URLs: <원문 링크 목록>
Confidence: high / medium / low
Open questions: 아직 검증하지 못한 질문
```

Google Docs/Drive source는 원본 변경을 NotebookLM에 자동 동기화할 수 있다. 단, source 접근 권한을 잃거나 원본을 삭제하면 notebook에서도 사용할 수 없게 된다.

### 3. provenance를 보존하는 note schema

| 필드 | 목적 |
|---|---|
| Claim | 내가 기억하고 싶은 검증 가능한 주장 |
| Evidence | 그 주장을 뒷받침하는 source 사실 또는 인용 요약 |
| Source URL | 원문으로 되돌아가는 링크 |
| Hermes interpretation | agent의 연결·추론·가설임을 표시 |
| Confidence | 재검증 우선순위를 정함 |
| Question / mistake | 복습과 다음 조사로 연결 |

### 4. 보안 경계

Hermes API Server는 terminal 권한을 가진 agent를 노출할 수 있다. 기본 loopback binding, Bearer key, 최소 범위 CORS를 적용하고 public endpoint로 직접 노출하지 않는다. Google Drive publishing credential도 least privilege와 승인 단계를 전제로 설계한다.

> [!WARNING]
> NotebookLM Google Docs import에서는 footnote와 comments가 source 본문으로 들어오지 않는다. 핵심 근거나 인용 맥락은 문서 본문에 작성한다.

## 권장 아키텍처

```text
Hermes API Server
  ├─ session / research / tools
  ├─ curated internal memory
  └─ optional external memory provider
                │
                ▼
       reviewed Study Note (Markdown)
                │
                ▼
   Google Drive: topic-specific Google Doc
                │
                ▼
NotebookLM: source-grounded Q&A and review
```

Hermes의 external memory provider는 agent가 세션 사이의 사실을 recall하는 계층이다. NotebookLM은 이 memory provider의 대체재가 아니라, 사람이 source와 함께 학습하는 published knowledge layer다.

## Sources

- https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/api-server.md
- https://hermes-agent.nousresearch.com/docs/user-guide/features/memory
- https://support.google.com/gemininotebook/answer/16215270?co=GENIE.Platform%3DDesktop&hl=en-6
