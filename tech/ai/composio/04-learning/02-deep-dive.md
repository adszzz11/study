---
date: 2026-07-19
tags: [tech]
type: tech-tool-study
status: draft
---

# Composio — Deep Dive

> [[01-getting-started|이전: Getting Started]] · [[../README|목차]] · [[../05-projects|다음: Projects]]

## 1. Session as a Security Boundary

Session은 편의상 conversation state를 저장하는 객체인 동시에 user, tool access, auth, execution state를 묶는 경계다. 그러나 application authorization을 대신하지는 않는다.

```text
App authentication
  -> tenant/user authorization
      -> Session ownership check
          -> toolkit/tool allowlist
              -> Connected Account pin
                  -> approval for side effect
```

각 층이 다른 실패를 막는다.

| 층 | 막는 오류 |
|---|---|
| App auth | 익명/위조 user |
| Tenant authorization | 다른 organization 접근 |
| Session ownership | 다른 user의 runtime state 재사용 |
| Tool allowlist | 불필요한 action discovery |
| Account pin | 개인/업무 account 혼동 |
| Approval | 의도하지 않은 write/destructive action |

### Multi-account policy

복수 Gmail/GitHub account가 연결되어 있으면 “활성 account”를 추론하지 않는다.

```yaml
account_binding:
  app_user_id: usr_01J...
  tenant_id: org_02K...
  toolkit: github
  connected_account_id: ca_...
  label: work
  verified_at: 2026-07-19
```

## 2. Discovery and Context Engineering

Dynamic discovery의 이득은 catalog 전체 schema를 prompt에서 제거하는 것이다. 대신 검색 query와 tool description 품질이 새로운 control point가 된다.

```text
intent -> search -> shortlist -> schema fetch -> validate -> execute
```

### Mode selection

| Workflow shape | 권장 mode |
|---|---|
| “내 업무를 도와줘”처럼 open-ended | dynamic search |
| support triage처럼 domain이 좁음 | allowlist + preload |
| issue 생성만 하는 form workflow | direct tool |
| backend reconciliation job | direct execution, LLM 생략 고려 |

`preload.tools`는 latency를 줄이지만 다시 context를 늘린다. 공식 가이드의 대체로 20개 미만 기준을 시작점으로 삼고 실제 token/selection eval로 조정한다.

### Discovery eval

```yaml
case:
  intent: "지난주 실패한 deploy issue를 찾아 담당자에게 Slack으로 알려줘"
  expected_tools:
    - GITHUB_...
    - SLACK_...
  forbidden_tools:
    - GITHUB_DELETE_...
  metrics:
    search_recall: true
    unnecessary_schema_count: 0
    forbidden_selected: false
```

## 3. Authentication Lifecycle

Auth Config와 Connected Account를 분리해 이해한다.

| 객체 | 수명/범위 | 담는 것 |
|---|---|---|
| Auth Config | 여러 user가 재사용 | auth method, OAuth client, scope |
| Connected Account | 한 user의 실제 연결 | credential/token과 연결 상태 |
| Session binding | 특정 runtime context | 어떤 account를 어떤 tool에 쓸지 |

### Managed vs Custom auth

- managed auth는 onboarding이 빠르다.
- custom auth는 제품 branding, scope, quota, OAuth consent screen control에 유리하다.
- managed auth 지원 여부는 toolkit마다 다를 수 있다.
- scope를 넓히는 것은 기능 선택이 아니라 security decision이다.

운영해야 할 state:

```text
INITIATED -> ACTIVE -> EXPIRED/FAILED -> REAUTH_REQUIRED -> ACTIVE
                      └-> REVOKED
```

token refresh를 platform이 처리하더라도 revoked consent, changed scope, deleted user에 대한 product UX는 application이 설계한다.

## 4. Execution Semantics

Agent action은 일반 chat completion보다 실패 mode가 많다.

| 실패 | 잘못된 대응 | 권장 대응 |
|---|---|---|
| timeout | 즉시 같은 write 재호출 | remote state 조회 후 idempotent retry |
| rate limit | 무제한 빠른 retry | bounded exponential backoff + jitter |
| partial success | workflow 전체를 처음부터 실행 | step별 checkpoint와 compensation |
| schema drift | LLM에게 오류문만 던짐 | pinned version, validation, upgrade test |
| auth expired | 다른 account 자동 선택 | 같은 user/account reauth 요청 |
| ambiguous intent | 가장 강한 action 실행 | clarification 또는 approval |

### Approval boundary

최종 실행 직전에 승인할 payload를 canonicalize하고 hash한다.

```text
plan -> resolve exact tool/input -> preview -> approve(input hash)
     -> execute same hash once -> record result
```

email recipient, payment amount, repository, branch가 바뀌면 이전 승인은 무효다.

## 5. SDK Path vs Hosted MCP

```text
Provider SDK path:
Agent -> local hooks/schema modifier/custom tool -> Composio -> SaaS

Hosted MCP path:
MCP Client -> hosted Session endpoint -> Composio -> SaaS
             (local SDK process를 지나지 않음)
```

| 요구사항 | 더 적합한 경로 |
|---|---|
| 여러 MCP client에서 portable하게 사용 | Hosted MCP |
| `beforeExecute`에서 policy 차단 | Provider SDK |
| `afterExecute`에서 local audit enrich | Provider SDK |
| process-local custom business tool | Provider SDK |
| client setup 단순화 | Hosted MCP |

중요 policy를 hook 하나에만 의존하면서 hosted MCP도 병행하지 않는다. 어느 경로에서도 강제되어야 하는 규칙은 backend authorization layer에 둔다.

## 6. Custom Tools and Proxy

### Three extension types

| 형태 | 예시 | 실행 위치 |
|---|---|---|
| Standalone tool | internal customer lookup | SDK application process |
| Extension tool | GitHub toolkit에 사내 labeling rule 추가 | local logic + authenticated `proxyExecute()` |
| Custom toolkit | `ACME_CRM_*` namespace | 등록/배포 설계에 따름 |

`proxyExecute()`는 toolkit의 인증을 재사용해 upstream API를 호출할 때 유용하다. 그렇다고 arbitrary URL proxy로 열면 SSRF/data exfiltration 통로가 될 수 있으므로 host/path/method를 고정하고 input schema를 좁힌다.

## 7. Triggers

Trigger는 polling 대신 Gmail 새 메일, GitHub commit 같은 event를 user/Connected Account 단위로 전달한다.

```text
External event
  -> Composio trigger
      -> signed webhook
          -> signature/timestamp 검증
              -> deduplicate event ID
                  -> enqueue
                      -> worker가 Session/action 실행
```

Webhook handler에서 긴 agent workflow를 동기 실행하지 않는다. 먼저 signature, timestamp, replay, tenant binding을 검증한 뒤 durable queue에 넣는다.

## 8. Sandbox / Workbench

Sandbox는 여러 tool result를 Python/shell로 join, filter, transform할 때 유용하다.

예:

```text
GitHub issues 조회
  -> Python으로 label/age 집계
      -> chart/table 생성
          -> Slack 요약 게시
```

보안 checklist:

- [ ] 필요 없으면 sandbox를 비활성화한다.
- [ ] network/file/command boundary를 최소화한다.
- [ ] tool output을 trusted shell input으로 취급하지 않는다.
- [ ] secret을 environment나 generated file에 불필요하게 노출하지 않는다.
- [ ] persistent file의 tenant/session retention을 정의한다.
- [ ] CPU/time/output size limit을 둔다.

## 9. Observability and Upgrade

최소 audit event:

```json
{
  "app_user_id": "usr_01J...",
  "tenant_id": "org_02K...",
  "session_id": "sess_...",
  "connected_account_id": "ca_...",
  "tool": "GITHUB_CREATE_ISSUE",
  "toolkit_version": "pinned-version",
  "approval_id": "appr_...",
  "outcome": "success",
  "latency_ms": 842,
  "timestamp": "2026-07-19T12:00:00Z"
}
```

credential, token, raw email body처럼 민감한 값은 기본 log에서 제거한다.

Upgrade 순서:

1. SDK/toolkit version pin
2. changelog와 migration guide review
3. schema snapshot diff
4. discovery/action golden test
5. auth/trigger sandbox test
6. canary user rollout
7. rollback 기준과 이전 version 보존

## Sources

- https://docs.composio.dev/docs/how-composio-works
- https://docs.composio.dev/docs/configuring-sessions
- https://docs.composio.dev/docs/sessions-via-mcp
- https://docs.composio.dev/docs/extending-sessions/custom-tools-and-toolkits
- https://docs.composio.dev/reference/api-reference/auth-configs
- https://docs.composio.dev/docs/auth-configuration/connected-accounts
- https://docs.composio.dev/reference/changelog

