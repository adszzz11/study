---
date: 2026-08-17
tags: [tech]
type: tech-tool-study
status: draft
---

# CodeBurn — Deep Dive

> [[01-getting-started|이전: Getting Started]] · [[../README|목차로 돌아가기]] · [[../05-projects|다음: Projects]]

## 1. Data pipeline

```text
AI coding tools
(JSONL / JSON / SQLite)
        ↓
provider-specific adapters
(discovery → parsing → deduplication)
        ↓
normalized sessions / calls / tools
        ↓
pricing + deterministic classification
        ↓
durable daily cache / aggregation
        ↓
TUI · CLI · Web · Desktop · Menubar · GNOME · JSON/CSV · MCP
```

adapter 계층이 provider 차이를 흡수하기 때문에 상위 surface는 동일한 aggregation 결과를 공유할 수 있다. 반대로 provider schema가 바뀌면 adapter의 discovery, parsing, deduplication이 깨질 수 있다.

## 2. Discovery와 deduplication

| Provider | 저장 형식 | 대표 deduplication 신호 |
|---|---|---|
| Claude Code | project별 JSONL | API message ID |
| Codex | 날짜별 rollout JSONL | cumulative token cross-check |
| Cursor | global `state.vscdb` | conversation + timestamp |
| Gemini CLI | session JSON | session ID |
| OpenCode | SQLite | session + message ID |
| Pi/OMP | JSONL | response ID |

provider별 dedup key가 필요한 이유는 같은 logical call이 cumulative counter, duplicate record, subtask session 등으로 여러 번 나타날 수 있기 때문이다. 단순히 모든 token field를 합하면 과대 계산될 수 있다.

parsed result와 daily aggregate는 기본적으로 `~/.cache/codeburn/`에 저장된다.

```text
~/.cache/codeburn/
├── codex-results.json
├── cursor-results.json
└── daily-cache.json
```

- file `mtime`과 size 등을 invalidation 신호로 쓴다.
- cache는 version field를 가지며 schema bump 시 recompute될 수 있다.
- atomic write로 중간 상태의 손상 위험을 줄인다.
- `CODEBURN_CACHE_DIR`로 위치를 바꿀 수 있다.

## 3. Pricing engine

개념적으로 한 call의 추정 비용은 다음 항목의 합이다.

```text
estimated cost
= input tokens × input rate
+ output tokens × output rate
+ cache-write tokens × cache-write rate
+ cache-read tokens × cache-read rate
+ web-search usage × search rate
```

- LiteLLM model pricing database를 기본으로 사용하고 local cache한다.
- Claude와 GPT 계열 일부에는 hardcoded fallback이 있다.
- model alias와 price override로 unknown model을 보정할 수 있다.
- pricing gap은 추가 source로 보완될 수 있으므로 version별 동작을 확인한다.
- subscription 또는 proxy usage는 API-rate cost와 out-of-pocket을 분리해 볼 수 있다.
- 환율 표시는 Frankfurter data에 의존한다.

### 추정 오차가 커지는 경우

| 상황 | 처리 예시 | 해석 |
|---|---|---|
| Cursor Auto | Sonnet 가격으로 추정 | 실제 model을 모름 |
| Kiro | content length와 Sonnet rate | token과 model 모두 추정 가능 |
| Copilot 일부 format | content length, tool ID prefix | 명시 token 부재 |
| alias 없는 신형 model | fallback/gap-fill 또는 `$0.00` | alias와 changelog 확인 |

따라서 CodeBurn cost는 invoice 대체물이 아니라 attribution과 optimization을 위한 관찰값이다.

## 4. Classification과 metric

task classification은 tool usage pattern과 user-message keyword를 이용한다. 재현 가능하고 LLM 비용이 없다는 장점이 있지만, 동일한 `Bash`나 `Edit`가 실제로 어떤 intent였는지 완전히 이해하지는 못한다.

| Metric | 계산 관점 | 교란 요인 |
|---|---|---|
| Cache hit rate | 전체 input 중 cache read 비중 | provider reporting 방식 |
| Cost per call/edit | cost를 call/edit 수로 나눔 | task 난이도와 call granularity |
| One-shot rate | edit/test/fix retry pattern | 의도적 iteration, test command 의미 |
| Self-correction | 같은 흐름의 수정 행동 | 사람 feedback과 구분 어려움 |
| Yield | session time과 Git commit 상관 | branch, squash, delayed commit, non-code work |

## 5. Optimize를 안전하게 쓰기

```bash
codeburn optimize
codeburn optimize -p week
codeburn optimize --provider claude
codeburn optimize --help
```

finding은 영향도 기반 A–F health grade와 수정 제안을 제공한다. 문서와 version 사이에 “copy-paste fix”와 자동 적용/undo 설명이 다를 수 있으므로 다음 순서를 따른다.

1. `--help`로 현재 version의 mutation 여부를 확인한다.
2. finding이 참조한 config와 session sample을 읽는다.
3. 비용 추정과 실제 workflow 필요성을 분리한다.
4. 변경 전 config를 version control 또는 backup한다.
5. 작은 변경 하나를 적용하고 다음 관찰 기간과 비교한다.

## 6. MCP privacy boundary

```bash
claude mcp add codeburn -- npx -y codeburn mcp
```

stdio MCP server는 두 tool을 노출한다.

| MCP tool | 반환 내용 |
|---|---|
| `get_usage` | provider, model, project, task별 spend와 usage |
| `get_savings` | waste finding, retry tax, routing waste 등 절감 후보 |

project name은 기본 pseudonym 처리되고 `include_project_names: true`를 명시할 때만 실제 이름을 노출한다. 그러나 요약된 usage도 민감할 수 있으므로 MCP client의 log, prompt history, external sync 정책까지 함께 확인한다.

## Sources

- https://codeburn.app/docs/data-locations
- https://codeburn.app/docs/provider-notes
- https://codeburn.app/docs/models
- https://codeburn.app/docs/optimize
- https://codeburn.app/docs/compare
- https://codeburn.app/docs/yield
- https://github.com/getagentseal/codeburn

