---
date: 2026-08-17
tags: [tech]
type: tech-tool-study
status: draft
---

# CodeBurn — Cheatsheet

> [[05-projects|이전: Projects]] · [[README|목차로 돌아가기]]

## 설치와 확인

```bash
# one-off
npx codeburn

# global install
npm install -g codeburn
codeburn --version
codeburn status

# macOS
brew tap getagentseal/codeburn
brew install codeburn
```

안전한 runtime baseline: **Node.js 22.13+**.

## 핵심 명령

| 목적 | 명령 |
|---|---|
| interactive dashboard | `codeburn` |
| local web dashboard | `codeburn web` |
| compact total | `codeburn status` |
| JSON status | `codeburn status --format json` |
| CSV export | `codeburn export` |
| JSON export | `codeburn export -f json` |
| model table | `codeburn models` |
| model/task breakdown | `codeburn models --by-task` |
| model comparison | `codeburn compare` |
| waste scan | `codeburn optimize` |
| Git delivery proxy | `codeburn yield` |
| stdio MCP server | `codeburn mcp` |

## Filter와 period

```bash
codeburn compare -p today
codeburn compare -p week
codeburn optimize -p week
codeburn optimize --provider claude
codeburn models --provider claude
codeburn models --task feature
codeburn models --top 10
codeburn yield -p 30days
codeburn export --project myapp
codeburn export --provider cursor -f json
```

period 이름은 command별 지원 범위가 다를 수 있으므로 `--help`를 확인한다.

## Output

| Command | 대표 format | 기본값 |
|---|---|---|
| `report`, `today`, `month` | `tui`, `json` | `tui` |
| `status` | `terminal`, `menubar-json`, `json` | `terminal` |
| `export` | `csv`, `json` | `csv` |
| `models` | table, Markdown | table |

```bash
codeburn status --format menubar-json --period today
codeburn models --format markdown
```

## MCP

```bash
claude mcp add codeburn -- npx -y codeburn mcp
```

| Tool | 용도 |
|---|---|
| `get_usage` | spend/usage를 tool, model, project, task별 조회 |
| `get_savings` | waste, retry tax, routing waste 분석 |

- project name은 기본 pseudonym 처리된다.
- 실제 이름은 `include_project_names: true`를 명시할 때만 요청한다.

## Data와 cache

```text
Claude  ~/.claude/projects/.../*.jsonl
Codex   ~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl
Cursor  .../Cursor/User/globalStorage/state.vscdb
Cache   ~/.cache/codeburn/
```

custom cache location:

```bash
CODEBURN_CACHE_DIR=/safe/local/path codeburn status
```

## 결과 해석

| 보이는 값 | 의미 | 주의 |
|---|---|---|
| Cost | local token × price table | invoice가 아님 |
| Cache hit | cache-read input 비중 | provider reporting 차이 |
| One-shot | retry 없는 edit 비율 | 품질 점수가 아님 |
| Optimize grade | 관찰된 waste impact 집계 | 자동 삭제 근거가 아님 |
| Yield | session과 Git commit의 시간 상관 | business value가 아님 |

## Troubleshooting

```bash
node --version
codeburn --version
codeburn --help
codeburn status --format json
codeburn optimize --help
```

- provider가 누락되면 [[03-references|Data Locations와 Provider Notes]]에서 실제 path를 확인한다.
- cost가 `$0.00`이거나 이상하면 model alias, pricing cache, changelog를 확인한다.
- 날짜가 어긋나면 timezone과 reporting period를 확인한다.
- 합계가 이상하면 open issue를 검색하고 원본 session sample로 교차 검증한다.

## Sources

- https://codeburn.app/docs/installation
- https://codeburn.app/docs/status-export
- https://codeburn.app/docs/models
- https://codeburn.app/docs/compare
- https://codeburn.app/docs/optimize
- https://codeburn.app/docs/yield
- https://codeburn.app/docs/data-locations
- https://github.com/getagentseal/codeburn
