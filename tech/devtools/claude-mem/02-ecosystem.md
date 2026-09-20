---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude-Mem Ecosystem

> [[01-overview|이전: Overview]] | [[README|목차]] | [[03-references|다음: References]]

## Positioning

Claude-Mem은 model 자체의 context window도, source-of-truth documentation도 아니다. Coding activity를 관찰해 session 사이에 이어 주는 별도 memory layer다.

```text
Repository docs / ADR / issue   → 사람이 검토하는 장기 source of truth
Built-in auto memory            → Claude가 선별한 간결한 Markdown memory
Claude-Mem                      → tool activity 기반 observation timeline + retrieval
Current context window          → 지금 추론에 직접 쓰는 제한된 working memory
```

## Comparison

| 기준 | Claude-Mem | Claude Code auto memory | 수동 `CLAUDE.md`/ADR/note | 일반 vector RAG |
|---|---|---|---|---|
| 주된 입력 | hook이 capture한 prompt/tool/session | Claude가 선별한 memory | 사람이 작성한 규칙·결정 | ingest한 문서 chunk |
| 저장 형식 | SQLite entities + optional Chroma | 유형별 Markdown note, `MEMORY.md` index | Markdown/document | vector DB + metadata |
| 자동성 | 높음 | 높음 | 낮음 | ingest pipeline에 따라 다름 |
| 시간적 맥락 | session/observation timeline | 선별 note 중심 | 작성 방식에 의존 | 보통 약함 |
| 검색 | FTS5, semantic, MCP, API | session 시작 시 index 일부 load | file/search | semantic/hybrid search |
| 설명 가능성 | observation과 source file metadata | Markdown을 직접 읽을 수 있음 | 가장 높음 | chunk/citation 품질에 의존 |
| 주요 위험 | 과잉 capture, provider 전송, summary 오류 | 선별 과정의 누락 | 갱신 누락과 작성 비용 | stale index, chunking 오류 |

Claude Code built-in auto memory는 `user`, `feedback`, `project`, `reference` 유형의 선별된 Markdown note를 만들고, session 시작 시 `MEMORY.md`의 처음 200줄 또는 25KB를 읽는다. Claude-Mem은 훨씬 넓은 coding activity를 observation으로 남기고 필요할 때 세부 기록을 검색한다는 점이 다르다.

## Complementary Use

함께 사용할 때는 역할을 겹치게 두지 않는 편이 낫다.

| 정보 | 권장 위치 |
|---|---|
| 반드시 지켜야 할 build/test command | tracked `CLAUDE.md` 또는 project docs |
| 합의된 architecture decision | ADR, issue, design doc |
| 사용자 선호와 반복 feedback | built-in auto memory |
| 어제 조사한 원인과 실패한 실험 | Claude-Mem observation/summary |
| 오래된 session의 특정 변경 맥락 | Claude-Mem MCP search |

Claude-Mem의 summary를 repository 사실의 최종 근거로 삼지 않는다. 중요한 결정은 검토 가능한 tracked document로 승격한다.

## Host And Provider Ecosystem

Worker 중심 구조는 Claude Code뿐 아니라 Cursor, OpenCode, Codex CLI, Grok Bot, OpenClaw 같은 host로 확장될 수 있다. 다만 host마다 hook lifecycle과 지원 범위가 같다고 가정하면 안 된다.

Compression provider는 데이터 경계를 바꾼다.

| Provider 유형 | 운영 질문 |
|---|---|
| Anthropic plan/API | plan 사용량과 code 전송 policy가 허용되는가? |
| Gemini/OpenRouter | API key 관리와 제3자 retention 조건을 검토했는가? |
| CMEM Pro | hosted observer와 Cloud Sync의 upload 범위를 이해했는가? |
| Host observer | local loopback을 쓰는 host integration의 제약은 무엇인가? |

## Decision Guide

### Claude-Mem을 추가한다

- session이 길고 병렬이며 동일 문제를 반복 조사한다.
- activity timeline과 검색 가능한 history가 실질적 비용을 줄인다.
- provider/data-flow review, backup, version pinning을 운영할 수 있다.

### Built-in memory만 사용한다

- 선별된 preference와 project fact만 있으면 충분하다.
- 설치할 background worker와 별도 DB를 최소화하고 싶다.
- 모든 tool activity를 capture할 이유가 없다.

### Tracked documentation을 우선한다

- 팀 전체가 검토·versioning해야 하는 규칙과 결정이다.
- 특정 agent plugin이 없어도 보존돼야 한다.
- auditability와 정확성이 자동 요약보다 중요하다.

## Sources

- https://github.com/thedotmack/claude-mem
- https://github.com/thedotmack/claude-mem/blob/main/docs/public/configuration.mdx
- https://github.com/thedotmack/claude-mem/blob/main/docs/public/usage/search-tools.mdx
- https://github.com/thedotmack/claude-mem/blob/main/docs/public/architecture/worker-service.mdx
- https://code.claude.com/docs/en/memory
