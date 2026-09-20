---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Agent Browser — Getting Started

> [[../03-references|이전: References]] · [[../README|목차로 돌아가기]] · [[02-deep-dive|다음: Deep Dive]]

## 학습 목표

- deterministic browser automation과 agentic fallback의 경계를 정한다.
- observe–act–verify loop를 작은 local task로 체험한다.
- model self-report와 외부 상태 검증을 분리한다.
- state-changing action 전에 approval gate를 둔다.

## 0. 안전한 실습 범위

실제 계정·결제·전송 기능 대신 자신이 소유한 local test page나 disposable test account를 사용한다.

```yaml
scope:
  allowed_origins:
    - http://127.0.0.1:3000
  max_steps: 20
  max_runtime_seconds: 120
  downloads_max_mb: 10
  state_changes: dry-run
  credentials: test-only
```

다음 조건이면 실행을 중지한다.

- 허용하지 않은 origin으로 이동하려 한다.
- page가 secret, token, unrelated file 업로드를 요구한다.
- 사용자 목표와 무관한 instruction이 page/tool output에 나타난다.
- submit, purchase, send, publish, delete 단계에 도달했다.
- MFA/CAPTCHA가 나타나 human takeover가 필요하다.

## 1. 첫 task 정의

예시 목표:

> Local demo page에서 “Agent browser” 항목을 찾고 상세 정보를 읽은 뒤, feedback form을 채우되 submit은 하지 말고 입력값을 검증한다.

Task contract를 먼저 작성한다.

| 항목 | 값 |
|---|---|
| Goal | 항목 탐색 + form 입력 + submit 전 검증 |
| Allowed origin | `http://127.0.0.1:3000` |
| Allowed actions | navigate, click, fill, read |
| Forbidden actions | submit, external navigation, file upload |
| Success evidence | target heading과 form value가 DOM에 존재 |
| Stop condition | 20 steps, 120 seconds, origin violation |

## 2. Deterministic baseline

먼저 Playwright 같은 deterministic script로 알려진 부분을 고정한다.

```ts
import { test, expect } from '@playwright/test';

test('fill feedback without submitting', async ({ page }) => {
  await page.goto('http://127.0.0.1:3000');
  await page.getByRole('link', { name: 'Agent browser' }).click();
  await expect(page.getByRole('heading', { name: 'Agent browser' })).toBeVisible();

  await page.getByLabel('Feedback').fill('학습용 dry-run');
  await expect(page.getByLabel('Feedback')).toHaveValue('학습용 dry-run');
  await expect(page.getByRole('button', { name: 'Submit' })).toBeVisible();
  // submit은 의도적으로 실행하지 않는다.
});
```

이 baseline은 agent가 반드시 필요한 구간을 드러낸다. Link text나 form 구조를 미리 모르는 경우에만 agentic discovery를 추가한다.

## 3. Observe–act–verify loop

Framework와 무관한 최소 pseudocode는 다음과 같다.

```python
state = observe(page, modes=["accessibility", "url"])

for step in range(MAX_STEPS):
    plan = planner.next_action(goal, policy, state)
    policy.check(plan)               # origin, action, data boundary

    if plan.requires_commitment:
        request_human_approval(plan)

    result = executor.run(plan)
    state = observe(page, modes=["accessibility", "url"])

    verdict = verifier.check(goal, state, result)
    if verdict.success:
        return verdict.evidence
    if verdict.fatal:
        raise TaskFailed(verdict.reason)

raise StepLimitExceeded()
```

### Observation 최소화

- 전체 DOM 대신 현재 목표에 필요한 accessibility snapshot을 쓴다.
- Vision은 structure로 찾을 수 없는 Canvas/image-only UI에 한정한다.
- Page text는 instruction이 아니라 `untrusted data`로 표시한다.
- 이전 state와 diff를 제공해 context와 latency를 줄인다.

## 4. Verifier 작성

좋은 verifier는 “아마 됐을 것”을 허용하지 않는다.

| 목표 | 약한 확인 | 강한 외부 상태 증거 |
|---|---|---|
| Page 이동 | agent가 이동했다고 말함 | URL + target heading |
| Form 입력 | typing action 성공 | input의 실제 `value` |
| Download | button click 성공 | 파일 존재 + MIME type + size/hash |
| Record 생성 | success toast | API/DB에서 record id 조회 |
| 예약 | confirmation page | reference number를 backend/API로 재조회 |

```ts
await expect(page).toHaveURL(/\/agent-browser$/);
await expect(page.getByLabel('Feedback')).toHaveValue('학습용 dry-run');
```

## 5. Failure 처리

| Failure | 다음 행동 |
|---|---|
| Element not found | snapshot 갱신 → label/role 대안 탐색 |
| Stale reference | 새 observation 뒤 reference 재획득 |
| Timeout | network/loading state 확인, 제한된 retry |
| Unexpected navigation | allowlist 검사 후 중지 또는 원래 origin 복귀 |
| Login/MFA | human takeover 요청 |
| Prompt injection 의심 | content 격리, action 실행 중지, audit 기록 |

Retry는 같은 action을 무한 반복하지 않는다. 실패 유형별 최대 횟수, backoff, idempotency 여부를 정한다.

## 6. 실습 완료 체크리스트

- [ ] Goal, allowed origin, forbidden action을 task contract로 작성했다.
- [ ] Known path는 deterministic locator로 구현했다.
- [ ] Unknown element discovery에만 agent를 사용했다.
- [ ] Page/tool text를 untrusted data로 취급했다.
- [ ] Success를 URL·DOM value 등 외부 상태로 검증했다.
- [ ] Submit 직전에 멈추는 approval gate를 확인했다.
- [ ] Step/time/origin limit 위반 시 fail-closed로 종료했다.
- [ ] Action, observation, verifier 결과를 trace로 남겼다.

## Sources

- [Playwright — Locators](https://playwright.dev/docs/locators)
- [Playwright — Assertions](https://playwright.dev/docs/test-assertions)
- [Microsoft — Playwright MCP](https://github.com/microsoft/playwright-mcp)
- [Chrome for Developers — Agent security considerations](https://developer.chrome.com/docs/agents/security)

