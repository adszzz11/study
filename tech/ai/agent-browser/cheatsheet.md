---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Agent Browser — Cheatsheet

> [[05-projects|이전: Projects]] · [[README|목차로 돌아가기]]

## 핵심 공식

```text
Agent browser = Planner + Observation + Action + Browser runtime + Verifier + Policy
```

```text
Prefer: API → stable selector → accessibility/DOM → screenshot
Finish: external evidence, not model self-report
Commit: re-observe → show impact → user approval → execute → verify
```

## Observe–act–verify

| 단계 | 핵심 질문 | 대표 산출물 |
|---|---|---|
| Goal | 무엇을 어디까지 허용하는가? | task contract, allowlist |
| Observe | 현재 state와 trust level은? | URL, AX tree, DOM, screenshot, tools |
| Plan | 다음 최소 action은? | typed action + expected effect |
| Check | Policy와 사용자 의도에 맞는가? | allow/deny/approval |
| Act | Reversible하고 idempotent한가? | browser/tool result |
| Verify | 어떤 외부 증거가 성공을 보이는가? | DOM/API/file/record evidence |
| Recover | Retry, re-plan, takeover 중 무엇인가? | bounded recovery decision |

## Observation 선택

| 조건 | 선택 |
|---|---|
| API 존재 | API 직접 호출 |
| Semantic WebMCP tool 존재 | Tool schema 검증 후 호출 |
| Role/label/text 존재 | Accessibility snapshot |
| Structured extraction | DOM |
| Canvas/image-only/remote desktop | Cropped screenshot + vision |
| 모두 불명확하거나 고위험 | Human takeover |

## Action 위험도

| 등급 | 예 | 기본 정책 |
|---|---|---|
| Read-only | read, search, inspect | allowlist 안에서 실행 |
| Reversible | fill draft, filter, open modal | trace 후 실행 |
| Commitment | submit, send, publish, purchase | 직전 explicit approval |
| Destructive | delete, cancel, revoke | preview + 강한 승인 + verify/rollback |

## Runtime 선택

| 상황 | Runtime |
|---|---|
| 개인 개발·debug | Local isolated context |
| CI·evaluation | Ephemeral container |
| 병렬 session·proxy·recording | Remote/cloud browser |
| 실제 personal profile 필요 | 마지막 선택, explicit consent |

## 실패와 복구

| 증상 | 처리 |
|---|---|
| Element missing | fresh observation → role/label 대안 |
| Stale reference | reference 재획득 |
| Loading timeout | state 확인 → bounded retry |
| Unexpected origin | 즉시 차단·기록 |
| MFA/CAPTCHA | human takeover |
| Duplicate 위험 | idempotency 확인, 결과부터 조회 |
| 완료 주장만 있음 | external verifier 실행 |
| Injection 의심 | 실행 중지, content 격리, audit |

## Security minimum

- [ ] Task별 isolated browser/container
- [ ] Origin allowlist와 cross-origin transfer 차단
- [ ] Credential은 model context 밖에서 injection
- [ ] Tool/page content는 untrusted data로 표시
- [ ] Read/write permission 분리
- [ ] High-impact action 직전 approval
- [ ] Step·time·token·cost·download size limit
- [ ] Action/screenshot/network/approval trace
- [ ] PII·secret redaction
- [ ] Prompt-injection security evaluation

## Verifier 예시

| Task | Evidence |
|---|---|
| Navigate | URL + heading |
| Fill | input value |
| Download | file existence + MIME + size/hash |
| Create | response/record id 재조회 |
| Send | outbox/message id |
| Purchase | 승인 후 order id + 금액·수량 재확인 |

## 선택 문장

| 기술 | 기억할 문장 |
|---|---|
| Playwright/Selenium | 알려진 workflow를 결정적으로 자동화 |
| Playwright MCP | AX snapshot과 MCP tool로 agent가 browser 조작 |
| Stagehand | Playwright-style code와 AI primitive를 혼합 |
| Browser Use | Python 중심 browser-agent loop framework |
| Computer Use | Screenshot·mouse·keyboard로 desktop까지 조작 |
| WebMCP | Website가 browser agent에 semantic tool을 제공 |
| Remote browser | Agent가 아니라 session runtime infrastructure |

## Production 질문 10개

1. API나 stable selector로 대체할 수 있는가?
2. Allowed origin과 forbidden action은 무엇인가?
3. Observation의 source와 trust label은 무엇인가?
4. Model이 credential 원문을 볼 필요가 있는가?
5. Action이 retry돼도 안전한가?
6. 완료를 검증할 외부 상태는 무엇인가?
7. Commitment 직전 무엇을 사용자에게 보여줄 것인가?
8. MFA/CAPTCHA/ambiguity에서 누가 takeover하는가?
9. Trace와 download를 얼마나 오래 보관하는가?
10. Injection fixture에서 unauthorized action이 0건인가?

## Sources

- [Microsoft — Playwright MCP](https://github.com/microsoft/playwright-mcp)
- [Browserbase — Stagehand](https://github.com/browserbase/stagehand)
- [Browser Use](https://github.com/browser-use/browser-use)
- [Chrome for Developers — WebMCP security](https://developer.chrome.com/docs/agents/security)
- [Anthropic — Prompt-injection defenses](https://www.anthropic.com/news/prompt-injection-defenses)
