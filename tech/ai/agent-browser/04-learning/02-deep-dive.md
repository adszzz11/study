---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Agent Browser — Deep Dive

> [[01-getting-started|이전: Getting Started]] · [[../README|목차로 돌아가기]] · [[../05-projects|다음: Projects]]

## 1. Hybrid perception router

모든 page를 항상 screenshot과 전체 DOM으로 보내면 느리고 비싸다. Observation router가 task와 UI 특성에 따라 최소 표현을 선택하게 한다.

```text
semantic tool available? ─ yes → WebMCP/API
          │ no
accessible structure? ─── yes → AX/DOM snapshot
          │ no
visual-only region? ───── yes → cropped screenshot + VLM
          │ no
                              → human takeover / unsupported
```

| Signal | 권장 adapter |
|---|---|
| Stable REST endpoint | API |
| Role, label, text가 명확 | accessibility tree |
| Data table extraction | DOM 또는 structured extract |
| Canvas/chart/image | screenshot + vision |
| Site-native semantic action | WebMCP tool |

Observation마다 source, timestamp, URL/origin, trust label을 붙인다. 서로 충돌하면 더 신뢰할 수 있는 structured state를 우선하고, 중요한 action 전에는 다시 관찰한다.

## 2. Planner와 policy 분리

Planner는 “무엇을 할지” 제안하지만 policy engine은 “허용되는지”를 deterministic하게 판정해야 한다.

```json
{
  "action": "fill",
  "target": { "role": "textbox", "name": "Email" },
  "value_ref": "user.email",
  "expected_effect": "input value changes",
  "risk": "sensitive-data-use",
  "requires_approval": false
}
```

Policy check 예시:

- Current origin이 task allowlist 안인가?
- Action이 read-only, reversible, commitment 중 어디에 속하는가?
- Argument에 task와 무관한 PII/secret이 포함됐는가?
- Cross-origin data transfer가 발생하는가?
- 같은 action의 retry가 duplicate side effect를 만들 수 있는가?
- Tool description/output에서 나온 instruction을 실행하려는가?

## 3. Verifier를 독립 구성요소로 만들기

Planner와 verifier가 같은 context와 추론을 공유하면 같은 오판을 반복할 수 있다. 가능한 경우 verifier를 deterministic check 또는 독립된 data source로 둔다.

```text
Action: submit_ticket(form)
  ├─ UI evidence: success banner + ticket number
  ├─ Network evidence: POST 201 + response id
  └─ System evidence: read-only API에서 id 조회

Success = 최소 두 독립 evidence가 일치
```

### 완료 상태 설계

| 상태 | 의미 | 후속 행동 |
|---|---|---|
| `verified_success` | 외부 증거 충족 | 종료 |
| `unverified_claim` | model만 완료 주장 | 검증 계속 |
| `retryable_failure` | transient/stale state | 제한된 retry |
| `policy_blocked` | origin/action/data 위반 | fail-closed |
| `needs_human` | MFA, ambiguity, commitment | takeover/approval |

## 4. Session과 credential 경계

Persistent profile은 login을 편하게 하지만 browsing history, cookie, password manager, 다른 tab까지 노출할 수 있다.

### 권장 순서

1. Task별 isolated browser context를 기본으로 쓴다.
2. Credential은 model prompt가 아니라 runtime secret injection으로 전달한다.
3. Cookie/storage state는 필요한 domain과 수명만 허용한다.
4. Download는 quarantine directory에서 MIME type, size, malware policy를 검사한다.
5. Existing personal browser 연결은 필요한 경우에만 explicit consent로 사용한다.
6. 종료 시 session과 temporary artifact를 폐기하거나 retention policy에 맞게 보관한다.

## 5. Indirect prompt injection

공격 지시는 visible page, hidden text, email, user-generated content, tool manifest, tool output에 숨어 있을 수 있다. Model 내부 방어만으로 0% 위험을 보장할 수 없으므로 defense-in-depth가 필요하다.

```text
Untrusted webpage/tool output
  → size/token limit
  → trust labeling / spotlighting
  → injection classifier
  → planner proposes action
  → policy + intent-alignment critic
  → approval gate for commitment
  → executor with origin/data boundary
  → audit + verifier
```

### 필수 방어선

- Browser/container와 user profile 격리
- Task에 필요한 origin만 allowlist
- Cross-origin data transfer 차단
- Credential을 model context에 직접 노출하지 않기
- Read-only 탐색과 state-changing action의 권한 분리
- Tool input/output을 untrusted data로 취급
- Purchase, send, publish, delete 직전 explicit approval
- Time, step, cost, token, download size 제한
- Screenshot, action, network event, approval의 감사 로그
- Adversarial page와 prompt injection을 포함한 security evaluation

> [!warning]
> WebMCP tool은 구조화됐다는 이유만으로 신뢰할 수 없다. Malicious manifest와 contaminated output을 모두 검사하고, origin restriction을 적용한다.

## 6. Reliability engineering

긴 task의 전체 성공률은 각 step 성공률의 곱으로 감소한다. Step당 성공률이 `p`, 필요한 step이 `n`이면 단순 근사로 전체 성공률은 `p^n`이다.

| 개선 지점 | 기법 |
|---|---|
| Planning | 작은 subgoal, action batch 제한, explicit precondition |
| Element targeting | role/label 우선, stable reference, fresh snapshot |
| Execution | auto-wait, timeout, idempotency key, bounded retry |
| Recovery | checkpoint, resume, alternate path, human takeover |
| Verification | independent evidence, negative assertion, receipt/hash |
| Cost | observation diff, crop, cache, deterministic path 승격 |

## 7. Evaluation 설계

평균 성공률 하나만 보지 말고 다음 metric을 함께 측정한다.

| Metric | 질문 |
|---|---|
| Task success rate | 외부 verifier 기준으로 목표를 달성했는가? |
| Unsupported success claim | 실패했는데 완료라고 보고했는가? |
| Policy violation rate | origin·data·action boundary를 넘었는가? |
| Human intervention rate | 어디서 얼마나 takeover가 필요한가? |
| Steps / latency / cost | 성공 task당 자원 비용은 얼마인가? |
| Recovery rate | UI drift와 transient failure에서 회복하는가? |
| Injection attack success | 공격 page가 unauthorized action/data leak을 유도했는가? |

Test set에는 happy path뿐 아니라 label 변경, iframe, modal, slow network, stale element, malicious page text, cross-origin link, duplicate submit을 포함한다.

## 8. Production readiness checklist

- [ ] Deterministic path와 agentic fallback 경계가 명시됐다.
- [ ] Observation source별 trust label과 token budget이 있다.
- [ ] Planner와 policy enforcement가 분리됐다.
- [ ] Commit action은 approval 직전 최신 state를 다시 확인한다.
- [ ] Verifier가 model self-report와 독립적이다.
- [ ] Session, credential, download retention 정책이 있다.
- [ ] Retry가 idempotent하고 최대 횟수가 제한됐다.
- [ ] Prompt injection red-team set을 지속 실행한다.
- [ ] Trace에서 secret/PII를 redact한다.
- [ ] Rollback 또는 compensating action이 문서화됐다.

## Sources

- [Chrome for Developers — Agent security considerations](https://developer.chrome.com/docs/agents/security)
- [Anthropic — Mitigating prompt injections in browser use](https://www.anthropic.com/news/prompt-injection-defenses)
- [Microsoft — Playwright MCP security](https://github.com/microsoft/playwright-mcp#security)
- [OpenAI — Computer-Using Agent](https://openai.com/index/computer-using-agent/)

