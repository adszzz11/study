---
date: 2026-06-10
tags:
  - tech
  - devtools
  - ripgrep
  - cheatsheet
type: tech-tool-study
parent: "[[README]]"
---

# ripgrep - 치트시트

> [[05-projects|이전: 프로젝트]] | [[README|목차로 돌아가기]]

## 설치

```bash
brew install ripgrep
cargo install ripgrep
rg --version
```

## 기본 검색

| 명령 | 설명 |
|---|---|
| `rg "TODO"` | 현재 디렉터리 recursive search |
| `rg -n "TODO"` | line number 출력 |
| `rg -i "error"` | 대소문자 무시 |
| `rg "foo\|bar"` | regex OR |
| `rg "foo" src tests` | path 제한 |

## 출력 제어

| 명령 | 설명 |
|---|---|
| `rg -l "foo"` | match가 있는 파일명만 |
| `rg -o "foo[0-9]+"` | match 부분만 |
| `rg -n --column "foo"` | line/column 출력 |
| `rg --context 2 "foo"` | 앞뒤 2줄 context |
| `rg --stats "foo"` | 검색 통계 |
| `rg --json "foo"` | JSON event stream |

## File Type / Glob

```bash
rg -tpy "import requests"
rg -tjs "console.log"
rg -Tmd "TODO"
rg --type-list

rg "password" -g '*.env'
rg "OldComponent" -g 'src/**/*.{ts,tsx}'
rg "needle" -g '!node_modules'
```

## Ignore / Hidden / Binary

| 명령 | 설명 |
|---|---|
| `rg "foo"` | `.gitignore`, hidden, binary skip |
| `rg --hidden "foo"` | hidden 포함 |
| `rg -a "foo"` | binary를 text처럼 검색 |
| `rg -u "foo"` | ignore 완화 |
| `rg -uuu "foo"` | 자동 필터 최대 해제 |
| `rg --debug "foo"` | skip reason 디버깅 |

## Regex / PCRE2

```bash
# 기본 regex engine
rg 'user_[0-9]+'
rg '\b[A-Z][A-Za-z0-9_]+\b'

# PCRE2 opt-in
rg -P '(?<=token=)[A-Za-z0-9._-]+'
rg --auto-hybrid-regex '(?<=token=)[A-Za-z0-9._-]+'
```

## 실전 패턴

### TODO/FIXME

```bash
rg -n "TODO|FIXME|HACK"
```

### Deprecated API

```bash
rg -n "deprecated_api|old_package" -tjs -tts -tpy
```

### Secret Pre-check

```bash
rg -n "(AKIA|BEGIN PRIVATE KEY|password\\s*=)" --hidden -g '!node_modules'
```

### Migration 후보 확인

```bash
rg -n --context 2 "OldComponent"
rg -l "OldComponent"
```

### Agent용 structured retrieval

```bash
rg --json -n --column "PaymentRetryPolicy" src tests
```

## 자주 헷갈리는 선택

| 상황 | 추천 |
|---|---|
| 일반 repo 검색 | `rg` |
| Git tracked file만 | `git grep` |
| 최소 서버/portable script | `grep` |
| archive/PDF/TUI 검색 | `ugrep` |
| lookbehind/backreference | `rg -P` |

## 관련 노트

- [[../../ai/codex/README|Codex tool-study]]
- [[../../ai/agent-orchestration/cli-agents|CLI agents]]
- [[../../ai/llm-wiki-study/README|LLM Wiki study]]

