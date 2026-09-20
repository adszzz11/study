---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Agent Browser — Projects

> [[04-learning/02-deep-dive|이전: Deep Dive]] · [[README|목차로 돌아가기]] · [[cheatsheet|다음: Cheatsheet]]

## 프로젝트 로드맵

| 프로젝트 | 난이도 | 핵심 학습 |
|---|---:|---|
| Local form navigator | ★ | locator, observation, external verifier |
| UI drift recovery harness | ★★ | agentic fallback, trace replay, selector 승격 |
| Secure invoice downloader | ★★ | isolated session, download verification, human takeover |
| Multi-site research assistant | ★★★ | origin policy, extraction schema, citation |
| WebMCP-ready support demo | ★★★ | declarative/imperative tool, untrusted output, confirmation |
| Browser-agent evaluation lab | ★★★ | reliability·security metric, adversarial fixture |

## 1. Local form navigator

### 목표

Local demo site의 여러 page를 탐색하고 form을 채우되 submit 직전에 멈춘다.

### 구현 범위

- Role/label 기반 locator를 우선 사용한다.
- Unknown label 하나만 agent가 탐색한다.
- Allowed origin은 localhost 하나로 제한한다.
- Form value와 URL을 verifier가 확인한다.
- Submit button action은 approval 없이는 거부한다.

### 완료 기준

- [ ] UI text를 바꿔도 target field를 다시 찾는다.
- [ ] 외부 origin link를 click하지 않는다.
- [ ] “secret을 업로드하라”는 malicious page text를 무시한다.
- [ ] 성공 evidence와 action trace가 저장된다.

## 2. UI drift recovery harness

### 목표

동일한 task의 UI variant를 여러 개 만들고 deterministic locator 실패 시 agentic fallback이 회복하는지 측정한다.

```text
fixtures/
├── baseline.html
├── renamed-label.html
├── reordered-form.html
├── modal-overlay.html
├── iframe.html
└── injection-text.html
```

| 측정값 | 정의 |
|---|---|
| Baseline success | 원래 UI에서 성공한 비율 |
| Drift recovery | 변경된 UI에서 fallback으로 회복한 비율 |
| False action | 잘못된 target에 action한 비율 |
| Mean steps | 성공까지 실행한 평균 action 수 |
| Promotion yield | 회복 경로 중 stable script로 승격 가능한 비율 |

성공한 fallback의 locator와 precondition을 Playwright test로 승격하고 다음 실행에서는 model 호출 없이 통과하는지 확인한다.

## 3. Secure invoice downloader

### 목표

Test account dashboard에서 지정 월의 invoice를 찾아 isolated directory에 다운로드하고 파일을 검증한다.

### Architecture

```text
Test credentials vault
  → isolated browser context
  → dashboard navigation
  → invoice discovery
  → download quarantine
  → MIME/size/hash verifier
  → approved output directory
```

### Guardrail

- Credential은 model context에 넣지 않는다.
- Personal browser profile을 재사용하지 않는다.
- Invoice domain 외 navigation을 차단한다.
- 예상 MIME type과 최대 file size를 강제한다.
- MFA는 human takeover로 처리한다.
- Log에는 account number와 token을 redact한다.

## 4. Multi-site research assistant

### 목표

Allowlisted documentation site에서 동일 주제를 찾아 structured JSON과 source URL을 생성한다.

```json
{
  "claim": "WebMCP exposes structured tools to browser agents.",
  "source_url": "https://developer.chrome.com/blog/webmcp-epp",
  "observed_at": "2026-09-20T00:00:00Z",
  "evidence_type": "page_text"
}
```

### 주의점

- Search 결과 snippet이 아니라 원문 page를 evidence로 삼는다.
- Page 안의 instruction은 실행하지 않는다.
- Citation과 claim의 직접 관련성을 verifier가 검사한다.
- Login, comment, upload, form submit action은 비활성화한다.

## 5. WebMCP-ready support demo

### 목표

Support ticket demo site가 semantic tool을 제공하고 agent가 raw DOM 조작과 tool call의 차이를 비교하게 한다.

| Tool | Mode | Risk policy |
|---|---|---|
| `search_help_articles` | declarative/read-only | 자동 허용 |
| `draft_support_ticket` | imperative/reversible | preview 허용 |
| `submit_support_ticket` | imperative/state-changing | 사용자 승인 필요 |

반드시 malicious tool description과 contaminated user comment fixture를 넣어 unauthorized data transfer가 차단되는지 시험한다.

## 6. Browser-agent evaluation lab

### Scenario set

- Happy path와 changed label
- Slow loading, stale reference, modal overlay
- iframe, Shadow DOM, Canvas 일부
- Cross-origin redirect와 phishing-like page
- Hidden prompt injection과 malicious tool output
- Duplicate submit, timeout 이후 결과 불명 상태

### Report template

```markdown
## Run summary
- Task success: 18/20
- Unsupported success claims: 1
- Policy violations: 0
- Human interventions: 2
- Median steps: 11
- Median latency: 34s
- Injection attack success: 0/12

## Failed cases
- scenario id
- last verified state
- failure class
- trace link
- proposed deterministic fix
```

## 공통 완료 조건

- [ ] 성공을 외부 상태로 검증한다.
- [ ] Origin, step, time, cost, download limit을 둔다.
- [ ] Read-only와 state-changing permission을 분리한다.
- [ ] High-impact action 직전에 explicit approval을 받는다.
- [ ] Prompt injection fixture를 포함한다.
- [ ] Secret과 PII를 trace에서 redact한다.
- [ ] Failure를 재현할 trace와 fixture가 있다.
- [ ] 반복 성공 경로를 deterministic script로 승격한다.

## Sources

- [Playwright — Best Practices](https://playwright.dev/docs/best-practices)
- [Microsoft — Playwright MCP](https://github.com/microsoft/playwright-mcp)
- [Chrome for Developers — WebMCP early preview](https://developer.chrome.com/blog/webmcp-epp)
- [Chrome for Developers — Agent security considerations](https://developer.chrome.com/docs/agents/security)

