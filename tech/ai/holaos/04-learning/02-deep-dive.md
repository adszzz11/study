---
date: 2026-08-17
tags: [tech]
type: tech-tool-study
status: draft
---

# holaOS Deep Dive

> [[01-getting-started|이전: Getting Started]] | [[../README|목차로 돌아가기]] | [[../05-projects|다음: Projects]]

## 1. Run Compilation as a Trust Boundary

workspace 원본을 모두 model에 넘기면 context 비용뿐 아니라 불필요한 secret, instruction, tool이 노출될 수 있다. holaOS Runtime은 run마다 필요한 요소를 조합해 **reduced execution package**를 만든다.

```text
Authored workspace     Runtime state       Discovered capability
       \                    |                    /
        \                   |                   /
         └──── selection + composition + checksum ────┘
                              ↓
                  Reduced execution package
                  - model
                  - composed prompt
                  - selected tools
                  - MCP payload
                  - recalled memory
                  - checksum
                              ↓
                         Harness Host
```

### Review questions

- input source마다 신뢰 수준이 구분되는가?
- prompt composition 순서와 precedence가 결정적인가?
- selected tool이 workspace allowlist와 일치하는가?
- recalled memory에 source와 scope가 남는가?
- checksum이 어느 입력을 포함하며 mismatch 시 fail하는가?

## 2. State Ownership

장기 agent의 어려움은 data를 저장하는 것보다 **어떤 상태가 진실인지** 결정하는 데 있다.

| 상태 | Source of truth | 수명 | 잘못 저장했을 때 |
|---|---|---|---|
| Policy | `AGENTS.md` | workspace 장기 | agent 행동이 지속적으로 왜곡됨 |
| Session/turn/queue | SQLite `runtime.db` | 실행 lifecycle | 중복 실행, 잘못된 resume |
| Resume snapshot | runtime continuity | session 사이 | 오래된 blocker를 계속 수행 |
| Fact/procedure | durable knowledge | 장기 | 잘못된 사실이 반복 recall |
| Preference/identity | user memory | 여러 workspace 가능 | 일시 관찰이 사용자 성향으로 굳음 |

### Promotion rule

```text
Observation
  → memory update proposal
  → scope/source/confidence review
  → accept, edit, or reject
  → durable memory
```

권장 metadata:

- `source`: 어디서 얻었는가
- `scope`: run, workspace, user 중 어디에 적용되는가
- `confidence`: verified, inferred, tentative
- `created_at`, `reviewed_at`, `expires_at`
- `supersedes`: 어떤 이전 기억을 대체하는가

## 3. Recall Design

vector similarity만으로 recall하면 의미가 비슷하지만 현재 작업과 무관한 memory가 들어올 수 있다. 실무에서는 다음 filter를 함께 고려한다.

```text
candidate memory
  → workspace/user scope filter
  → permission filter
  → recency + confidence
  → vector relevance
  → token budget
  → run context
```

### Failure modes

| 실패 | 예시 | 완화 |
|---|---|---|
| Stale memory | 이전 provider 설정을 현재값으로 recall | expiry와 supersedes 관리 |
| Scope leak | 개인 preference가 팀 workspace에 노출 | user/workspace ACL 분리 |
| Over-recall | 관련 없는 과거 note로 prompt 비대화 | top-k, threshold, token budget |
| Under-recall | 핵심 blocker 누락 | continuity snapshot을 semantic recall과 분리 |
| False permanence | 한 번의 말투를 영구 preference로 저장 | proposal review와 evidence threshold |

## 4. Capability Projection

Capability는 많을수록 좋은 것이 아니다. model의 선택 공간, prompt injection surface, credential scope와 side effect 가능성이 함께 커진다.

### Projection inputs

- browser tools
- Runtime tools: todo, scratchpad, web search, cronjob, image generation, report 등
- workspace Skills와 Commands
- local/remote MCP servers
- App-provided MCP tools

### Least-privilege example

```yaml
# Conceptual example; verify the current schema.
mcp_registry:
  github:
    enabled: true
    tools:
      - github.search_issues
      - github.get_issue
```

`create_issue`, `merge_pull_request` 같은 write tool은 read workflow에서 제외한다. allowlist가 empty일 때 discovery된 모든 tool을 expose하는 구현이라면 empty 상태 자체가 위험한 default다.

## 5. App Lifecycle and Integration Boundary

```text
Install/Setup
   ↓
Start → Health Check → Ready → MCP discovery
   ↑                         ↓
Stop  ← failure/restart policy
```

`app.runtime.yaml`이 선언할 수 있는 책임은 setup/start/stop, port, MCP endpoint, health check, integration scope다. 검토할 핵심은 manifest 선언과 실제 process 행동이 일치하는지다.

### Security review

- setup script가 network에서 무엇을 내려받는가?
- process가 어느 filesystem path와 environment variable을 읽는가?
- health endpoint가 secret이나 내부 상태를 노출하지 않는가?
- MCP tool schema보다 실제 handler 권한이 더 넓지 않은가?
- signed grant의 audience, scope, expiry가 제한되는가?
- broker URL이 raw provider credential을 App log로 유출하지 않는가?

## 6. Approval Is a Workflow, Not a Guarantee

Side effect tool의 안전성은 여러 층이 함께 지켜야 한다.

```text
Tool declaration
  → capability allowlist
  → model selects action
  → approval policy
  → user confirmation
  → tool implementation
  → provider permission
  → audit log
```

어느 한 단계라도 넓으면 approval dialog만으로 충분하지 않다.

| 위험 | 권장 control |
|---|---|
| 공개 게시 | preview, exact destination, final confirmation |
| 메시지 전송 | recipient/body 표시, batch size limit |
| 유료 작업 | amount/currency/vendor 표시, hard budget |
| 반복 automation | per-run cap, expiry, kill switch |
| retry | idempotency key, duplicate detection |

## 7. Harness Portability

이상적인 harness boundary는 workspace policy와 capability를 harness-specific session format에서 분리한다. 그러나 portability는 interface만으로 완성되지 않는다.

- tool call format과 streaming event 차이
- reasoning/control parameter 차이
- session resume semantics 차이
- attachment와 multimodal support 차이
- approval callback과 error mapping 차이

현재 OSS runtime의 실제 harness path가 `pi`라는 점을 baseline으로 삼고, 다른 harness 지원은 repository의 adapter와 integration test가 있을 때만 구현 완료로 판단한다.

## 8. Failure Drills

| Drill | 기대 결과 |
|---|---|
| Runtime 중단 후 재시작 | 중복 side effect 없이 queue/session 복원 |
| MCP server timeout | bounded retry 후 명확한 blocker 기록 |
| App health check 실패 | capability를 ready로 노출하지 않음 |
| provider 변경 | context 전송 경계와 reasoning option 재확인 |
| stale memory 주입 | source/recency 검토로 reject 또는 supersede |
| empty allowlist | 의도한 fail-closed 여부 확인 |
| approval 취소 | action 미실행, state와 audit 일치 |

## Deep-dive Checklist

- [ ] compiled package를 workspace source와 대조할 수 있다.
- [ ] authored policy, execution truth, continuity, knowledge를 구분한다.
- [ ] memory promotion/rejection 기준을 문서화했다.
- [ ] capability가 task별 최소 집합이다.
- [ ] App manifest와 실제 process 권한을 비교했다.
- [ ] approval 취소, retry, duplicate action을 시험했다.
- [ ] harness/provider 변경 시 portability gap을 기록했다.

## Sources

- https://www.holaos.ai/docs/contribute/runtime/run-compilation
- https://www.holaos.ai/docs/concepts/memory-and-continuity
- https://www.holaos.ai/docs/concepts/agent-harness/runtime-tools
- https://www.holaos.ai/docs/build/apps/app-anatomy
- https://www.holaos.ai/docs/concepts/workspace-model

