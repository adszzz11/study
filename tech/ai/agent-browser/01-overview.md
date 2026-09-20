---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Agent Browser — Overview

> [[README|목차로 돌아가기]] · [[02-ecosystem|다음: Ecosystem]]

## What

Agent browser는 목표를 받은 AI agent가 browser 상태를 관찰하고, 다음 action을 계획·실행한 뒤 실제 결과를 검증하는 automation system이다. 여기서 **agent browser**는 특정 제품명이 아니라 browser-use agent, framework, runtime, protocol을 포괄하는 기술군이다.

```text
User goal
   ↓
Planner / Policy LLM
   ↓
Observation adapter
[screenshot | DOM | accessibility tree | WebMCP tools]
   ↓
Action executor
[click | type | scroll | navigate | extract | upload/download | API]
   ↓
Browser runtime
[local Chrome | isolated container | remote/cloud browser]
   ↓
Verifier → success / retry / re-plan / human approval
```

## Why

Playwright·Selenium 같은 기존 automation은 selector와 사전 정의 workflow가 안정적일 때 빠르고 결정적이다. 그러나 화면 구조, 문구, iframe, Shadow DOM이 바뀌거나 처음 보는 site를 만나면 작성된 script가 쉽게 깨진다.

Agent browser는 다음 간극을 메운다.

- 자연어 목표를 실행 계획과 browser action으로 변환한다.
- 변경된 UI를 다시 관찰해 element를 재탐색하고 replanning한다.
- 로그인 이후 dashboard, multi-page form, 다운로드처럼 긴 workflow를 처리한다.
- 단순 정보 수집뿐 아니라 데이터 입력, 예약 준비 등 state-changing task도 다룬다.
- 성공한 탐색 action을 selector/script/cache로 승격해 반복 비용을 줄일 수 있다.

2025년 공개된 OpenAI CUA는 screenshot과 virtual mouse/keyboard를 사용해 WebArena에서 58.1%를 기록했지만 인간 기준 78.2%에는 미치지 못했다. 이는 범용 UI control의 가능성과 장기 작업 신뢰성의 한계를 동시에 보여준다. 이후 실용적 system은 visual control 하나보다 text browser, API, terminal, DOM/AX tree를 함께 쓰는 hybrid architecture로 발전했다.

## 비슷한 개념과 구분

| 개념 | 주목적 | 의사결정 방식 |
|---|---|---|
| Web search / crawler | 정보 검색·수집 | query·crawl rule 중심 |
| RPA | 알려진 업무의 안정적 반복 | 사전 정의 workflow |
| Browser automation | UI test·반복 조작 | selector·script 중심 |
| Browser agent | 목표에 맞는 다음 action 결정 | 동적 planning과 feedback loop |
| Agentic browser | agent UX가 browser에 통합된 제품 | 사용자-facing assistant/agent |
| Computer Use | browser를 포함한 desktop 전체 조작 | screenshot·mouse·keyboard 중심 |

## 핵심 특징

### 1. Perception

| 방식 | 강점 | 한계 |
|---|---|---|
| Visual | Canvas, image-only UI, remote desktop에도 적용 | token·latency 비용, coordinate error, 해상도 의존 |
| DOM/accessibility | 빠르고 구조적이며 role·label 기반 조작 가능 | Canvas, closed Shadow DOM, 비표준 component에 취약 |
| Hybrid | 구조적 탐색을 우선하고 시각 정보로 빈틈 보완 | adapter와 관찰 병합 로직이 복잡 |
| WebMCP | website가 typed semantic tool을 직접 노출 | early-stage 표준이며 tool도 untrusted input일 수 있음 |

### 2. Planning–action–verification loop

1. 사용자 목표, 허용 origin, 금지 action을 해석한다.
2. 현재 page state를 관찰한다.
3. 다음 action 또는 제한된 action batch를 만든다.
4. browser runtime에서 실행한다.
5. navigation, error, network 결과와 새 state를 받는다.
6. 외부 상태 기반 verifier로 완료 여부를 판정한다.
7. 실패하면 selector 갱신, 다른 경로, retry, human takeover 중 하나를 선택한다.

### 3. Action abstraction

- **Low-level:** mouse move, coordinate click, keyboard typing, scroll, screenshot
- **Structural:** role, label, text, element reference 기반 `click`, `fill`, `select`
- **AI primitive:** `act`, `observe`, `extract`, `validate`
- **Workflow:** login, invoice download, multi-page form completion
- **Website-native:** WebMCP declarative/imperative typed tool

### 4. Runtime와 session

Production runtime은 cookie/localStorage/profile 수명, concurrent session 격리, proxy/region, upload/download, recording/trace, timeout/retry를 관리해야 한다. CAPTCHA와 MFA는 우회 대상이 아니라 **human takeover 지점**으로 설계한다.

| Runtime | 적합한 상황 | 주요 주의점 |
|---|---|---|
| Local browser | 개인 보조, 개발·디버깅 | 개인 profile과 secret 노출 |
| Isolated container | CI, 평가, 재현 가능한 task | session persistence와 file 전달 |
| Remote/cloud browser | 병렬 session, proxy, recording | 비용, data residency, provider trust |

## 실용적 설계 원칙

```text
API / URL / stable selector
        ↓ 가능하면 직접 실행
uncertain element discovery
        ↓ agentic fallback
external-state verification
        ↓
cache or promote successful path to script
```

- **Deterministic-first:** 알려진 selector, API, URL을 우선한다.
- **Least agency:** 필요한 origin, data, action만 허용한다.
- **Evidence over narration:** 완료 주장이 아니라 외부 증거를 확인한다.
- **Approval before commitment:** purchase, send, publish, delete 직전에 승인한다.
- **Progressive hardening:** 성공한 agent action을 test와 script로 고정한다.

## 한계

- 긴 workflow에서는 작은 오류가 누적돼 end-to-end 성공률이 급격히 낮아진다.
- page 안의 문장은 instruction이 아니라 untrusted data인데 model이 혼동할 수 있다.
- 로그인 profile 재사용은 편하지만 credential과 개인 데이터의 공격 표면을 넓힌다.
- visual-only 조작은 느리고 좌표 변화에 민감하다.
- benchmark 성공률이 실제 조직의 auth, latency, policy, failure recovery를 그대로 대변하지 않는다.

## Sources

- [OpenAI — Computer-Using Agent](https://openai.com/index/computer-using-agent/)
- [OpenAI — Introducing ChatGPT agent](https://openai.com/index/introducing-chatgpt-agent/)
- [Microsoft — Playwright MCP](https://github.com/microsoft/playwright-mcp)
- [Chrome for Developers — WebMCP early preview](https://developer.chrome.com/blog/webmcp-epp)

