---
date: 2026-10-22
tags: [tech]
type: tech-tool-study
status: draft
---

# CLI-Anything cheatsheet

## 빠른 흐름

```bash
# 기존 harness 탐색
pip install cli-anything-hub
cli-hub search <keyword>

# open-source target에서 harness 생성
/cli-anything <target-path-or-repo>

# 생성물 설치와 interface 확인
pip install -e .
<generated-cli> --help
<generated-cli> <command> --json
<generated-cli> repl
```

## Harness checklist

| 항목 | 확인 질문 |
|---|---|
| backend | mock이 아니라 실제 source/API/backend를 호출하는가? |
| commands | GUI menu 복제가 아닌 domain action으로 구성됐는가? |
| output | `--json`의 schema가 success/failure 모두 안정적인가? |
| state | script mode와 stateful REPL의 경계가 명확한가? |
| docs | `--help`와 `SKILL.md`에 example·error handling이 있는가? |
| tests | native artifact 생성, 재오픈, state assertion을 수행하는가? |
| security | input validation, allowlist, least privilege, audit log가 있는가? |

## `/refine` 전 준비

- 빠진 capability를 하나의 command와 acceptance criteria로 좁힌다.
- 실패 command, input, expected JSON, expected artifact를 기록한다.
- generated code의 shell call, path 처리, credential 사용을 review한다.

## 판단 규칙

- API contract가 이미 우수함 → native API + 자체 CLI 우선
- 여러 agent client에서 표준 interface 필요 → MCP wrapper 추가
- Web UI만 대상 → Playwright CLI 검토
- source/API + 반복 domain workflow → CLI-Anything 적합

## Sources

- https://github.com/HKUDS/CLI-Anything
- https://clianything.cc/
- https://modelcontextprotocol.io/specification/2025-11-25/server/tools
