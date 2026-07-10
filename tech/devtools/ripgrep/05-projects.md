---
date: 2026-06-10
tags:
  - tech
  - devtools
  - ripgrep
  - projects
type: tech-tool-study
parent: "[[README]]"
---

# ripgrep - 실전 프로젝트

> [[04-learning/02-deep-dive|이전: Deep Dive]] | [[README|목차로 돌아가기]] | [[cheatsheet|다음: 치트시트]]

## 프로젝트 1: Monorepo Dependency Audit

### 목표

- deprecated API, old package, 금지된 import 사용처를 빠르게 찾는다.
- 언어별 file type filter로 noise를 줄인다.

```bash
rg -n "deprecated_api|old_package" -tjs -tts -tpy
rg -n "from old_package|import old_package" -tpy
rg -n "OldComponent" -g 'src/**/*.{ts,tsx}'
```

### 산출물

| 산출물 | 설명 |
|---|---|
| 후보 파일 목록 | `rg -l` 결과 |
| 영향 범위 | package/module별 count |
| migration plan | replace 전후 test 범위 |

## 프로젝트 2: Secret Pre-check

### 목표

- commit 전 obvious secret pattern을 빠르게 탐지한다.
- hidden file도 포함하되 dependency directory는 제외한다.

```bash
rg -n "(AKIA|BEGIN PRIVATE KEY|password\\s*=)" --hidden -g '!node_modules'
rg -n "(api_key|secret|token)\\s*[:=]" --hidden -g '!dist' -g '!build'
```

### 주의

- `rg`는 secret scanner가 아니라 fast pre-check다.
- entropy 기반 탐지, allowlist, history scan은 별도 도구와 병행한다.
- CI에서는 false positive를 줄이기 위해 path와 pattern을 구체화한다.

## 프로젝트 3: AI Coding Agent Context Retrieval

### 목표

- issue keyword, symbol name, error message를 `rg`로 검색한다.
- 주변 context를 LLM에 제공해 수정 범위를 좁힌다.

```bash
rg -n --context 3 "NullPointerException|payment timeout" src tests
rg -n --column "PaymentService|PaymentRetryPolicy" src tests
rg --json -n --column "PaymentRetryPolicy" src
```

### Workflow

| 단계 | 명령 | 목적 |
|---|---|---|
| Keyword search | `rg -n --context 3 "<error>"` | 문제 주변 context 확보 |
| Symbol search | `rg -n --column "<symbol>"` | 정의/사용처 확인 |
| File list | `rg -l "<symbol>"` | edit 후보 축소 |
| Structured output | `rg --json "<symbol>"` | agent pipeline 연결 |

관련: [[../../ai/codex/README|Codex tool-study]], [[../../ai/agent-orchestration/cli-agents|CLI agents]]

## 프로젝트 4: Migration 작업

### 목표

- replace 전에 영향 범위를 눈으로 확인한다.
- `xargs sed` 같은 destructive command는 검토 이후에만 사용한다.

```bash
# 먼저 context 확인
rg -n --context 2 "OldComponent"

# 파일 목록 추출
rg -l "OldComponent"

# 변경 후 검증
rg -n "OldComponent"
```

### Checklist

- [ ] `rg -n --context 2`로 실제 사용 맥락 확인
- [ ] generated/vendor file 제외 여부 확인
- [ ] test file과 production file을 분리해서 영향 범위 파악
- [ ] replace 후 `rg`로 잔여 사용처 확인
- [ ] 관련 테스트 실행

## 프로젝트 5: Search Debugging Playbook

### 목표

- "왜 이 파일이 검색되지 않지?"를 재현 가능하게 진단한다.

```bash
rg --debug "needle"
rg --hidden "needle"
rg -uuu "needle"
rg --files | rg "expected-file"
```

| 증상 | 확인 |
|---|---|
| 파일이 안 잡힘 | `.gitignore`, `.ignore`, `.rgignore` |
| hidden file 누락 | `--hidden` |
| binary로 판단됨 | `-a` 또는 `-uuu` |
| type filter가 이상함 | `rg --type-list` |
| glob이 너무 좁음 | `-g` pattern 단순화 |

## Best Practices

- 검색 root를 좁힌다: `rg PATTERN src tests`
- file type을 명시한다: `-tpy`, `-tjs`, `-trs`
- migration 전에는 `--context`로 사람 검토를 먼저 한다.
- automation에는 `--json`, `-l`, `-o`, `-n --column`을 쓴다.
- agent workflow에서는 exact lexical search를 첫 단계로 둔다.

