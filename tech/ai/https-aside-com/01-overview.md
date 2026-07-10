---
date: 2026-06-25
tags:
  - tech
  - ai
  - aside
  - overview
type: tech-tool-study
parent: "[[README]]"
---

# Aside - 개요

> [[README|목차로 돌아가기]] | [[02-ecosystem|다음: 생태계]]

---

## 1. What - Aside란?

Aside는 macOS용 **agentic AI browser**다. 일반 agent app 위에 browser connector를 붙이는 방식이 아니라, browser 자체를 agent runtime으로 삼는다.

```text
User task
  -> Aside task runtime
  -> browser tabs / logged-in websites / files / history / credentials
  -> approval gates / artifacts / wait-resume
```

### 핵심 정의

| 항목 | 설명 |
|------|------|
| 제품 유형 | Browser-native AI agent |
| 실행 환경 | macOS 15.0+의 Aside browser |
| 주요 컨텍스트 | 웹사이트, 계정, browsing history, local files, saved credentials |
| task 구성 | mode, permission, working folder, model |
| 개발자 인터페이스 | `aside` CLI, MCP server, REPL |

---

## 2. Why - 왜 필요한가?

기존 AI agent는 API integration이나 connector가 없으면 실제 업무 사이트에서 멈추기 쉽다. 하지만 현대 업무는 Gmail, CRM, payroll, dashboard, docs, spreadsheets 같은 "탭" 안에서 이루어진다.

Aside의 문제의식은 다음과 같다.

- 업무 시스템은 API보다 UI workflow가 먼저 열려 있는 경우가 많다.
- 사용자는 이미 browser에 로그인되어 있고, 필요한 파일과 히스토리도 local/browser context에 있다.
- agent가 실제 업무를 하려면 사람처럼 웹을 탐색하고, 필요한 순간에 권한 확인을 받고, 결과 artifact를 남겨야 한다.

YC profile도 Aside를 "웹을 사람처럼 사용하며 integration에 의존하지 않는 브라우저 agent"로 설명한다.

---

## 3. 핵심 특징

### Browser-native agent

Aside 자체가 browser로 동작한다. 설정에 따라 웹사이트, 계정, history, file, saved credentials를 task에 사용할 수 있다.

### Task runtime

Task는 다음 요소를 가진다.

| 요소 | 의미 |
|------|------|
| mode | `Read only`, `Guard`, `Full access` 같은 session mode |
| permission | file, browser, network, tool access rule |
| working folder | artifact 저장과 파일 작업 기준 위치 |
| model | Aside plan model, subscription model, BYOK provider |

Agent는 browsing, web search, file step, credential autofill, approval, wait/resume을 수행하고 결과 artifact를 남긴다.

### Permission model

기본값은 `Guard`다.

| Mode | 용도 |
|------|------|
| `Read only` | 조사, 읽기 중심 task |
| `Guard` | 제한된 파일/브라우저 작업, 승인 기반 workflow |
| `Full access` | 신뢰 가능한 local 작업, 넓은 파일 접근이 필요한 task |

추가로 sandbox, readable/writable roots, tool/browser/network rules를 `Allow`, `Ask`, `Deny`로 제어한다.

### Agent-safe Password Manager

Credential은 raw password로 agent에게 노출되지 않는다. 웹사이트에는 autofill payload로 입력되며 URL과 access policy를 확인한다. Touch ID unlock, passkey/FIDO2/TOTP 흐름도 지원한다.

### Local memory / privacy

Browsing history, chats, tasks에서 memory를 만들 수 있고 retention은 `Never forget`, `30 days`, `90 days`로 설정한다. Privacy setting에는 browsing history, cookies, analytics sharing, Safe Browsing 등이 포함된다.

### Model/provider layer

Aside plan model 외에도 ChatGPT, Claude, GitHub Copilot subscription을 연결할 수 있고, OpenAI, Anthropic, OpenRouter, Google, xAI, Vercel AI Gateway, Cloudflare AI Gateway API key도 사용할 수 있다.

### Developer interface

개발자는 CLI, MCP server, REPL을 사용할 수 있다.

```bash
aside "Open localhost:3000 and run a smoke test"
aside mcp
aside repl
```

### Routines / Ultrabrowse

- **Routines**: cron/heartbeat routine으로 반복 업무를 실행한다.
- **Ultrabrowse**: citation-heavy research, vendor comparison, pricing/security/compliance 조사에 맞춘 mode다.

---

## 4. 2026년 6월 변화

2026년 6월 changelog 기준으로 다음 기능들이 추가됐다.

| 변화 | 의미 |
|------|------|
| Custom skills | 반복 업무 절차를 skill로 재사용 |
| Suggested tasks | 현재 context 기반 task 제안 |
| Help Center | 제품 학습 문서 강화 |
| Routine cards | 반복 task 상태를 UI 카드로 관리 |
| OpenRouter models | model 선택 폭 확대 |
| Apple Passwords / external password managers | credential source 확장 |
| Payment autofill | 결제 form 자동 입력 지원 |
| Event-triggered routines | event 기반 자동화 |

---

## 관련 노트

- [[../codex/README|Codex]] - CLI/MCP 기반 agent workflow 비교 대상
- [[../model-context-protocol-mcp/README|MCP]] - Aside developer integration의 연결 표준
- [[../ai-ecosystem/01-overview|AI ecosystem]] - AI browser category 위치

## References

- [Aside official](https://aside.com/)
- [Aside Help Center](https://docs.aside.com/)
- [Get started](https://docs.aside.com/help/get-started)
- [Run tasks](https://docs.aside.com/help/tasks)
- [Permissions](https://docs.aside.com/help/security)
- [Password Manager](https://docs.aside.com/help/password-manager)
- [Memory](https://docs.aside.com/help/memory)
- [Privacy](https://docs.aside.com/help/privacy)
- [AI providers](https://docs.aside.com/help/ai)
- [Developers](https://docs.aside.com/help/developers)
- [Automation](https://docs.aside.com/help/automation)
- [Ultrabrowse](https://docs.aside.com/help/ultrabrowse)
- [Changelog](https://docs.aside.com/changelog/components)
- [YC profile](https://www.ycombinator.com/companies/aside)
