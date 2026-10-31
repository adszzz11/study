---
date: 2026-06-25
tags:
  - tech
  - ai
  - aside
  - deep-dive
type: tech-tool-study
parent: "[[../README]]"
---

# Aside - 심화

> [[01-getting-started|이전: 시작하기]] | [[../README|목차로 돌아가기]] | [[../05-projects|다음: 프로젝트]]

---

## 1. Task runtime 해부

Aside task는 browser 작업을 길게 이어가기 위한 runtime 단위다.

| 구성요소 | 질문 |
|----------|------|
| Mode | 이 task는 읽기만 하는가, 제한된 쓰기인가, full access인가? |
| Permission | browser/file/network/tool access를 어디까지 허용할 것인가? |
| Working folder | artifact와 다운로드 파일을 어디에 둘 것인가? |
| Model | Aside plan model, subscription model, BYOK model 중 무엇을 쓸 것인가? |
| Approval | 어떤 action에서 반드시 사용자 확인을 받을 것인가? |
| Resume | MFA, wait, external event 이후 어떻게 이어갈 것인가? |

```text
Task starts
  -> inspect browser/file context
  -> ask approval when needed
  -> browse / search / download / draft
  -> wait or resume
  -> leave artifacts
```

---

## 2. Permission 설계

`Guard`를 기본값으로 두고, task별로 root와 action rule을 좁히는 방식이 안전하다.

| Rule | 적용 예 |
|------|---------|
| `Allow` | 지정 folder에 artifact 저장, 특정 internal dashboard 읽기 |
| `Ask` | payment, post, email send, CRM update, file overwrite |
| `Deny` | password raw export, payroll setting change, destructive delete |

### Task prompt에 넣을 문장

```text
Use Guard mode. You may read the current dashboard and download reports
to ./artifacts/aside-demo. Ask before sending messages, changing status,
submitting forms, deleting files, or using payment autofill.
```

---

## 3. Credential boundary

Agent-safe Password Manager의 핵심은 **credential은 입력되지만 agent에게 raw secret은 노출되지 않는다**는 점이다.

| 단계 | 확인할 점 |
|------|-----------|
| URL check | 예상 domain과 login form인지 |
| Access policy | `Always allow`, `While unlocked`, `Never` 중 무엇인지 |
| Unlock | Touch ID 또는 user confirmation이 필요한지 |
| Autofill | raw password 대신 browser autofill payload로 입력되는지 |
| Sensitive action | login 이후 결제/전송/삭제는 별도 approval을 거치는지 |

Passkey/FIDO2/TOTP 흐름은 사이트별 UX 차이가 크므로, 첫 자동화 전에 수동 fallback을 준비한다.

---

## 4. Memory와 privacy

Memory는 browsing history, chats, tasks에서 만들어질 수 있다. Retention은 다음 중 선택한다.

| Retention | 사용 예 |
|-----------|---------|
| `Never forget` | 장기 업무 context, 반복 vendor research |
| `30 days` | 단기 project, 임시 operational task |
| `90 days` | 분기 단위 비교/조사 |

Privacy setting에서는 browsing history, cookies, analytics sharing, Safe Browsing을 확인한다. 개인/회사 계정을 함께 쓰는 환경에서는 profile 분리와 task별 readable/writable root 제한이 중요하다.

---

## 5. Model/provider layer

Aside는 model provider를 유연하게 붙일 수 있다.

| Provider 유형 | 예 |
|---------------|----|
| Aside plan model | Aside plan에 포함된 model |
| Subscription | ChatGPT, Claude, GitHub Copilot |
| BYOK API key | OpenAI, Anthropic, OpenRouter, Google, xAI |
| Gateway | Vercel AI Gateway, Cloudflare AI Gateway |

업무별 선택 기준은 다음과 같다.

- **정확한 browser operation**: 안정성과 tool handling이 좋은 model
- **Long research**: context 처리와 citation 품질이 좋은 model
- **민감 업무**: 조직 policy와 audit이 가능한 provider
- **비용 관리**: gateway 또는 OpenRouter routing 검토

---

## 6. CLI, MCP, REPL

개발자 인터페이스는 browser automation을 coding tool과 연결하는 접점이다.

```bash
# Local app smoke test
aside "Open localhost:3000 and run a smoke test"

# MCP server
aside mcp

# Deterministic browser steps
aside repl
```

| 도구 | 용도 |
|------|------|
| CLI | 자연어 task를 command line에서 실행 |
| MCP server | coding agent나 IDE에 browser automation 제공 |
| REPL | screenshot, download, DOM inspection 같은 step 실험 |

---

## 7. Routines와 Ultrabrowse

### Routines

Routines는 반복 업무 자동화에 맞다.

| Routine | 예 |
|---------|----|
| Cron routine | 매주 월요일 dashboard summary 생성 |
| Heartbeat routine | ongoing research thread 갱신 |
| Event-triggered routine | 특정 event 이후 follow-up task 실행 |

### Ultrabrowse

Ultrabrowse는 citation-heavy research에 맞춘 mode다.

| 적합 업무 | 산출물 |
|-----------|--------|
| Vendor comparison | pricing/security/compliance 비교표 |
| API docs 조사 | integration requirement 요약 |
| SOC2/security docs 확인 | evidence link와 risk note |

---

## 심화 실습 과제

| 과제 | 목표 |
|------|------|
| Permission matrix 작성 | `Allow/Ask/Deny`를 업무별로 설계 |
| Credential flow 리허설 | login, MFA, autofill, approval boundary 확인 |
| MCP smoke test | coding agent에서 Aside browser automation 호출 |
| Ultrabrowse vendor report | citation 포함 pricing/security 비교 |
| Routine card 설계 | 반복 업무의 trigger, artifact, approval rule 정의 |

## 관련 노트

- [[../../openrouter/README|OpenRouter]] - BYOK/model routing 비교
- [[../../model-context-protocol-mcp/04-learning/02-deep-dive|MCP deep dive]] - MCP server 운영 설계
- [[../../thin-harness-fat-skills|Thin harness, fat skills]] - custom skills와 반복 workflow 설계
