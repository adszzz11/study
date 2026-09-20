---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Hermes Agent Server와 NotebookLM — Ecosystem

> [[01-overview|이전: Overview]] · [[README|목차로 돌아가기]] · [[03-references|다음: References]]

## 선택지 비교

| 방식 | 적합한 경우 | 자동화 | 핵심 한계 |
|---|---|---:|---|
| Hermes → Google Docs → NotebookLM | 개인 학습·리서치, 기본 권장 | 중간 | NotebookLM 질의 결과를 Hermes가 공식 API로 회수하는 흐름은 아님 |
| Hermes → Markdown/PDF upload | 일회성 snapshot, 개인 파일 중심 | 낮음 | 재업로드와 version 관리가 필요 |
| Hermes → NotebookLM Enterprise API | 조직 단위, Cloud/IAM 운영 가능 | 높음 | Preview, Enterprise 라이선스·권한·지역 설계 필요 |
| Hermes + external memory provider | agent가 장기 사실을 recall해야 함 | 높음 | 사람이 읽는 학습 노트 경험은 별도로 필요 |
| Custom RAG + vector DB + MCP | agent↔knowledge 양방향 API가 필수 | 높음 | indexing, permission, observability를 직접 운영 |
| 비공식 `notebooklm-py`류 | 개인 실험·CLI 편의 | 중간 | 브라우저 세션·비공식 내부 동작 의존, production 부적합 |

## 계층별 책임

| 계층 | 대표 도구 | 책임 | 저장하면 안 되는 것 |
|---|---|---|---|
| Agent working memory | Hermes `MEMORY.md`, `USER.md` | 현재 task와 사용자 선호 | 긴 원문, 검증 전 추측, 대형 연구 archive |
| Agent long-term retrieval | Mem0, Hindsight, Supermemory 등 | 세션 간 fact retrieval | 검토되지 않은 원문 혼합 corpus |
| Published learning layer | Google Docs + NotebookLM | 사람의 질문, 복습, source-grounded synthesis | secret, raw credential, 승인 전 조사 초안 |
| Bidirectional knowledge system | RAG + vector DB + MCP | programmatic retrieval/write | ownership·permission이 불명확한 문서 |

## Google Docs 경로를 기본으로 삼는 이유

NotebookLM은 Google Docs, Markdown, PDF, DOCX, TXT, CSV, Slides, Sheets, Web URL, YouTube를 source로 지원한다. 그중 Google Drive의 Google Doc은 living note를 갱신할 때 auto-sync가 가능하므로 재업로드 부담이 작다.

Free 기준 안내된 한도는 source당 최대 50만 단어 또는 업로드 파일 200MB, notebook당 50개 source다. 큰 원문 모음 하나를 무조건 넣기보다 주제와 질문 경계를 기준으로 source를 나눈다.

> [!NOTE]
> Drive auto-sync는 편의 기능이지 version control이 아니다. 문서의 `Updated`, 변경 요약, source URL을 남겨 NotebookLM 답변의 근거가 어느 revision인지 사람이 판단할 수 있게 한다.

## Enterprise API를 택할 때

Gemini Notebook Enterprise에는 `notebooks.create`, `sources.batchCreate` 같은 API가 있으며 raw text, Google Docs/Slides, web URL, YouTube source를 넣을 수 있다. 이는 consumer NotebookLM을 Hermes가 호출하는 API와 구분해야 한다. Enterprise API는 Preview 상태와 별도 Cloud/IAM 운영을 전제로 한다.

## MCP가 들어갈 자리

Hermes는 MCP로 외부 tool server를 연결하고 server별 tool surface를 제한할 수 있다. 따라서 다음의 adapter 구조가 자연스럽다.

```text
Hermes ──MCP──> Drive publisher (create draft / update approved Doc)
       └─MCP──> internal documents or custom RAG (read-only first)
```

초기에는 `create_draft`, `preview_diff`, `publish_approved`를 분리해 write를 명시적으로 승인한다. 검색 결과나 외부 문서도 prompt injection source가 될 수 있으므로, publishing tool이 임의의 지시를 실행하지 않도록 입력 schema와 대상 folder를 좁힌다.

## Sources

- https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers
- https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp
- https://support.google.com/gemininotebook/answer/16215270?co=GENIE.Platform%3DDesktop&hl=en-6
- https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks
- https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks-sources
