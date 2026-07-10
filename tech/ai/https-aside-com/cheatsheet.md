---
date: 2026-06-25
tags:
  - tech
  - ai
  - aside
  - cheatsheet
type: tech-tool-study
parent: "[[README]]"
---

# Aside - 치트시트

> [[README|목차로 돌아가기]]

---

## 핵심 요약

| 항목 | 내용 |
|------|------|
| Category | Agentic AI browser |
| Platform | 문서 기준 macOS 15.0+ |
| 핵심 컨텍스트 | 로그인된 웹사이트, 파일, history, saved credentials |
| 기본 mode | `Guard` |
| Developer tools | `aside` CLI, MCP server, REPL |
| Automation | Cron routine, heartbeat routine, event-triggered routine |
| Research mode | Ultrabrowse |

---

## Session mode

| Mode | 쓰임 |
|------|------|
| `Read only` | 조사, 읽기, citation-heavy research |
| `Guard` | 기본값. 제한된 작업 + approval gate |
| `Full access` | 신뢰 가능한 local 작업, 넓은 파일 접근이 필요한 task |

## Permission rule

| Rule | 의미 |
|------|------|
| `Allow` | task 안에서 바로 허용 |
| `Ask` | 실행 전 사용자 승인 |
| `Deny` | 금지 |

---

## Task prompt template

```text
Use <Read only|Guard|Full access> mode.
Work on <site/app/account>.
Goal: <desired outcome>.
Save artifacts to <folder>.
Allowed: <allowed actions>.
Ask before: <payment/post/send/delete/status change/credential unlock/etc>.
Do not: <forbidden actions>.
When done, summarize files created and unresolved blockers.
```

## 좋은 첫 prompt

```text
Use Guard mode. In Rippling, download this month's paystub PDF
to ~/Downloads. If MFA is required, ask me. Do not change any payroll
settings. Tell me the saved filename when done.
```

```text
Use Ultrabrowse to compare three vendors on pricing, SOC2/security docs,
API limits, and enterprise support. Return a citation-heavy markdown table.
Do not sign up for trials or submit contact forms.
```

---

## Developer commands

```bash
# Local web app smoke test
aside "Open localhost:3000 and run a smoke test"

# Start MCP server
aside mcp

# Interactive deterministic browser steps
aside repl
```

---

## Password Manager guardrails

| 정책 | 설명 |
|------|------|
| `Always allow` | 조건이 맞으면 autofill 허용 |
| `While unlocked` | unlock 상태에서만 허용 |
| `Never` | agent autofill 금지 |

기억할 점:

- Raw password는 AI agent에 노출되지 않는다.
- Credential은 autofill payload로 웹사이트에 입력된다.
- URL과 access policy를 확인한다.
- Payment, message send, destructive action은 별도 approval을 둔다.

---

## Memory / privacy

| 설정 | 선택지 |
|------|--------|
| Memory retention | `Never forget`, `30 days`, `90 days` |
| Privacy 확인 | browsing history, cookies, analytics sharing, Safe Browsing |
| 파일 접근 | readable/writable roots를 task별로 제한 |

---

## 언제 무엇을 쓰나

| 목표 | 추천 |
|------|------|
| 웹 조사 | `Read only` + Ultrabrowse |
| portal에서 파일 다운로드 | `Guard` + working folder 지정 |
| local app QA | CLI + `localhost` smoke test |
| coding agent에 browser 붙이기 | `aside mcp` |
| 반복 업무 | routine card + approval gates |
| provider 실험 | ChatGPT/Claude/Copilot subscription 또는 BYOK |

---

## 관련 노트

- [[../codex/cheatsheet|Codex cheatsheet]] - CLI agent 명령어 비교
- [[../model-context-protocol-mcp/cheatsheet|MCP cheatsheet]] - MCP server 연결 빠른 참조
- [[../../scraping/playwright/cheatsheet|Playwright cheatsheet]] - browser automation 비교
