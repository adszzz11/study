---
date: 2026-06-20
tags:
  - tech
  - ai
  - notebooklm
  - learning
type: tech-tool-study
parent: "[[../README]]"
---

# NotebookLM - 심화

> [[01-getting-started|이전: 시작하기]] | [[../README|목차로 돌아가기]]

---

## 1. 심화 목표

NotebookLM을 단순 요약 도구가 아니라 **source QA + artifact generation + research workflow**로 다룬다.

- citation 품질을 평가하는 prompt pattern 만들기
- Studio outputs를 output type별로 검수하기
- Deep/Fast Research로 가져온 sources를 curator 관점에서 정리하기
- CLI/API 자동화 필요성을 판단하고 대안을 설계하기

## 2. Citation 품질 평가

| 평가 항목 | 좋은 상태 | 위험 신호 |
|----------|-----------|-----------|
| Coverage | 핵심 주장 대부분에 citation 있음 | 중요한 숫자/날짜/정책에 citation 없음 |
| Specificity | source의 특정 위치와 연결 | source 전체만 뭉뚱그려 언급 |
| Relevance | citation이 claim을 직접 뒷받침 | citation 문맥이 다른 주장 |
| Conflict handling | source 간 충돌을 명시 | 최신/구버전 문서를 섞어 단정 |
| Unknown handling | source 밖 정보는 모른다고 말함 | source에 없는 배경지식을 섞음 |

```text
"아래 답변을 citation auditor처럼 검토해줘.
각 claim을 direct support / weak support / unsupported / contradicted 로 분류하고,
unsupported claim은 다시 확인해야 할 source query를 제안해줘."
```

## 3. Studio output 검수

### Audio Overview

Audio Overview는 AI hosts가 source 핵심 주제를 deep-dive discussion 형식으로 설명하는 output이다. Deep Dive, Brief, Critique, Debate 같은 format을 고를 수 있다.

| 검수 질문 | 이유 |
|-----------|------|
| 진행자가 source 밖의 비유나 평가를 사실처럼 말하지 않는가? | audio는 듣기 쉬운 대신 근거 추적이 약해질 수 있음 |
| 중요한 caveat가 빠지지 않았는가? | 요약 과정에서 한계가 누락되기 쉬움 |
| 용어를 일관되게 쓰는가? | source-grounded learning에서 용어 drift 방지 |

### Video Overview

Video Overview는 source를 narration/visual 중심 video로 바꾼다. Explainer, Brief, Cinematic format, visual style, steering prompt를 활용할 수 있다.

```text
Steering prompt 예시:
"이 video overview는 엔지니어 onboarding용이다.
기능 홍보보다 limits, data policy, CLI/API 부재, 검증 workflow를 강조해줘."
```

### Flashcards / Quizzes

- 정답이 source에 직접 근거하는지 확인한다.
- 애매한 문항은 "복수 정답 가능" 여부를 점검한다.
- 숫자/limit/plan은 최신 문서 확인이 필요하므로 카드에 "verify latest" 표시를 둔다.

## 4. Deep Research / Fast Research

NotebookLM 안의 research 기능은 web/Drive sources를 찾아 notebook에 가져오는 흐름으로 이해한다. Deep Research는 여러 웹사이트를 browse해 report와 sources를 만든 뒤 import하는 agentic feature다.

| 단계 | 작업 | 산출물 |
|------|------|--------|
| Query design | 좁은 research question 작성 | 검색 query와 scope |
| Source discovery | web/Drive 후보 탐색 | source candidate list |
| Import | notebook sources로 추가 | curated source set |
| Report review | generated report 검토 | claim/citation audit |
| Prune | 중복/약한 source 제거 | 신뢰도 높은 notebook |

```text
Research query 예시:
"NotebookLM official CLI or API availability, Gemini CLI distinction, and enterprise data handling as of June 2026"
```

## 5. CLI/API 대체 아키텍처

NotebookLM 전용 공식 CLI/API가 필요한 상황이라면 현재는 대체 설계를 검토하는 편이 안정적이다.

```text
Local docs
  -> extraction/parsing
  -> chunking + metadata
  -> vector/search index
  -> Gemini/OpenAI/Claude model
  -> CLI/MCP interface
  -> markdown report with citations
```

| 구성요소 | 선택지 | 메모 |
|----------|--------|------|
| CLI agent | Gemini CLI, Codex, Claude Code | local file/shell workflow |
| Model API | Google AI Studio, Vertex AI, OpenAI, Anthropic | 보안/비용/모델 선택 |
| RAG framework | LangChain, LlamaIndex, custom scripts | chunking, retrieval, citations |
| Integration | MCP | tool/resource/prompt 노출 |
| Storage | local files, SQLite, Postgres, vector DB | 권한과 audit 고려 |

## 6. Prompt patterns

```text
"sources만 근거로 답해줘. source에 없는 내용은 'source에 없음'이라고 표시해줘."
```

```text
"답변을 claim 단위 표로 분해하고, 각 claim마다 citation, confidence, 검증 필요 여부를 붙여줘."
```

```text
"공식 문서와 비공식 글의 주장을 분리해줘.
공식 문서에만 근거한 결론을 먼저 쓰고, 나머지는 참고 의견으로 표시해줘."
```

```text
"CLI/API 관련 언급만 추출해줘.
NotebookLM 자체 기능, Gemini CLI, 비공식 자동화 가능성을 구분해서 표로 정리해줘."
```

## 7. 도입 리스크

| 리스크 | 대응 |
|--------|------|
| Hallucinated artifact | citations audit, source-only prompt, human review |
| Stale limits | 공식 Help/plan 문서 링크를 notes에 함께 보존 |
| Data leakage | Workspace policy, sharing setting, source 권한 점검 |
| Automation gap | Gemini CLI/custom RAG/MCP로 별도 workflow 설계 |
| Source sprawl | notebook별 source owner, freshness, pruning rule 운영 |

---

## 관련 노트

- [[study/tech/ai/model-context-protocol-mcp]] - NotebookLM-like CLI workflow의 integration layer
- [[study/tech/ai/litellm]] - custom RAG의 provider routing/gateway
- [[study/tech/ai/agent-orchestration/cli-agents]] - Gemini CLI, Codex, Claude Code 등 terminal agents 비교
