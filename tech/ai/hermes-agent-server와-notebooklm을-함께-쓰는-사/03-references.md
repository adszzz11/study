---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Hermes Agent Server와 NotebookLM — References

> [[02-ecosystem|이전: Ecosystem]] · [[README|목차로 돌아가기]] · [[04-learning/01-getting-started|다음: Getting Started]]

## 공식 문서 지도

| 영역 | 자료 | 확인할 내용 |
|---|---|---|
| Hermes | [Hermes Agent repository](https://github.com/NousResearch/hermes-agent) | 설치 방식, release, 전체 기능 지도 |
| Hermes | [API Server](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/api-server.md) | OpenAI-compatible endpoint, binding, auth, CORS |
| Hermes | [Persistent Memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory) | `MEMORY.md`/`USER.md`의 역할과 관리 방식 |
| Hermes | [Memory Providers](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers) | external memory provider 설정과 retrieval 경계 |
| Hermes | [MCP](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp) | MCP server 연결, server별 tool 제한 |
| NotebookLM | [Add or discover sources](https://support.google.com/gemininotebook/answer/16215270?co=GENIE.Platform%3DDesktop&hl=en-6) | 지원 형식, 한도, Drive source 제약 |
| NotebookLM | [Drive auto-sync announcement](https://workspaceupdates.googleblog.com/2026/05/keep-your-sources-up-to-date-with-automatic-Drive-syncing-in-NotebookLM.html) | Drive source 자동 동기화 rollout |
| NotebookLM | [Deep Research and file types](https://blog.google/innovation-and-ai/models-and-research/google-labs/notebooklm-deep-research-file-types/) | source 형식 확장과 research workflow |
| Enterprise | [Notebook API](https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks) | notebook 생성·관리 API, Preview 조건 |
| Enterprise | [Source API](https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks-sources) | `sources.batchCreate`, source type, IAM |

## 읽는 순서

1. Hermes API Server 문서로 network exposure와 auth 경계를 먼저 확인한다.
2. Persistent Memory와 Memory Providers를 읽어 어떤 사실이 agent memory에 남아야 하는지 정한다.
3. NotebookLM source Help에서 import 형식, 한도, Drive 권한 제약을 확인한다.
4. auto-sync 발표와 실제 계정 UI의 사용 가능 여부를 대조한다.
5. 조직 자동화가 필요할 때만 Enterprise API 문서와 IAM 설계를 검토한다.

## 조사 메모

- “NotebookLM API”라는 표현은 consumer NotebookLM과 Gemini Notebook Enterprise API를 혼동하기 쉽다. 구현 전 product와 account 유형을 명시한다.
- Google Docs의 footnote/comments는 NotebookLM import 대상이 아니므로, 학습에 필요한 사실·링크·인용 맥락은 본문에 둔다.
- 문서의 기능·한도·rollout은 바뀔 수 있다. 실제 publishing workflow를 만들기 전 위 공식 문서와 계정에서 재확인한다.

## Sources

- https://github.com/NousResearch/hermes-agent
- https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/api-server.md
- https://hermes-agent.nousresearch.com/docs/user-guide/features/memory
- https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers
- https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp
- https://support.google.com/gemininotebook/answer/16215270?co=GENIE.Platform%3DDesktop&hl=en-6
- https://workspaceupdates.googleblog.com/2026/05/keep-your-sources-up-to-date-with-automatic-Drive-syncing-in-NotebookLM.html
- https://blog.google/innovation-and-ai/models-and-research/google-labs/notebooklm-deep-research-file-types/
- https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks
- https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks-sources
