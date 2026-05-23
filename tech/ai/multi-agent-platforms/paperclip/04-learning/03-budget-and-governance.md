# 4-3. 예산·승인·감사로그 — Paperclip의 진짜 가치

> 시간 ~20분. 결과: 직원이 폭주해도 안전한 환경 + 위험 작업은 승인 후에만 실행.

## 💰 예산 통제 (Budget & Cost Control)

### 동작 방식

```
직원이 LLM 호출 → 토큰 사용 → Paperclip이 환산:
   used = used + (input_tokens × $/1M + output_tokens × $/1M)
   
if used ≥ 0.8 × monthly_budget:
   notify(직원 본인 + admin)   # 경고

if used ≥ monthly_budget:
   if hard_stop:
       pause(agent)            # 다음 heartbeat 거부
       open_ticket("BUDGET_EXCEEDED")
   else:
       allow + alert
```

### 설정 예시

회사 레벨 + 직원 레벨로 이중 한도:

```yaml
# 회사 레벨
company:
  monthly_budget: 200
  models:
    claude-opus-4-7:    { input: 15, output: 75 }   # $/1M tokens
    claude-sonnet-4-6:  { input: 3,  output: 15 }
    ollama/*:           { input: 0,  output: 0 }

# 직원 레벨
agents:
  code-reviewer:
    monthly: 30
    hard_stop: true        # 한도 도달 시 정지
  telegram-chief:
    monthly: 50
    hard_stop: true
  research:
    monthly: 20
    hard_stop: false       # 경고만 (필요시 수동 정지)
```

### 실시간 모니터링

```bash
# CLI
paperclip budget status

# 출력 예시:
# Company: Home OS  $84.30 / $200.00 (42%)
#   code-reviewer    $22.10 / $30.00  (74%)
#   telegram-chief   $41.50 / $50.00  (83%) ⚠️ 경고
#   daily-backup     $0.00  / $0.00   (—)
```

대시보드에서도 직원별 카드 + 그래프.

### 강제 정지 후 복구

```bash
# 한 직원만 재가동
paperclip agent resume code-reviewer

# 예산 상향
paperclip agent update code-reviewer --budget.monthly 50

# 새 달이 되면 자동 리셋 (회사 timezone 기준 1일 00:00)
```

## 🛡️ 거버넌스 / 승인 워크플로우

직원이 **위험한 작업**을 하려 할 때 사람 승인을 강제.

### 1. Approval 정책 정의

```yaml
# governance/policies.yaml
policies:
  - id: critical-file-write
    matches:
      tool: files_write
      paths: ["/etc/*", "~/.ssh/*", "/Library/LaunchAgents/*"]
    requires: admin_approval
    
  - id: shell-destructive
    matches:
      tool: shell
      command_pattern: "rm\\s+-rf|drop\\s+database"
    requires: admin_approval
    
  - id: high-cost-task
    matches:
      estimated_cost_usd: ">5"
    requires: admin_approval
    
  - id: external-email
    matches:
      tool: email_send
      to_domain_not: ["mycompany.com"]
    requires: chief_approval   # 매니저 직원이 승인
```

### 2. 승인 흐름

```
직원 ── 작업 시도 ──► Paperclip
                       │
                       │ 정책 매칭?
                       │
                  Yes  │  No
                       ▼   └──► 즉시 실행
              Approval 큐
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
  텔레그램 알림 (admin)    대시보드 알림
   "[승인 필요]"           "Pending: 3"
        │
        ▼
   /approve <id> 또는 /reject
        │
        ▼
       직원이 알림 받고 실행 (또는 중단)
```

### 3. 승인 명령

```bash
# CLI
paperclip approval list --pending
paperclip approval approve abc123 --note "확인됨"
paperclip approval reject abc123 --reason "도구 권한 너무 넓음"

# 텔레그램에서 직접 (telegram-chief 통해)
"/approve abc123"
```

## 📜 감사로그 (Activity & Events)

모든 동작이 이벤트로 기록:

```jsonl
{"ts":"2026-05-23T01:42:00Z","actor":"code-reviewer","event":"task.started","task_id":"t-789","prompt_excerpt":"리포 zone PR #142..."}
{"ts":"2026-05-23T01:42:03Z","actor":"code-reviewer","event":"llm.call","model":"claude-opus-4-7","tokens_in":4203,"tokens_out":612,"cost_usd":0.108}
{"ts":"2026-05-23T01:42:04Z","actor":"code-reviewer","event":"tool.call","tool":"git_diff","args":{"ref":"PR-142"}}
{"ts":"2026-05-23T01:42:08Z","actor":"code-reviewer","event":"task.completed","duration_ms":8120,"output_excerpt":"보안 이슈 1건..."}
```

### 조회

```bash
# 최근 1시간 이벤트
paperclip activity tail --since 1h

# 특정 직원
paperclip activity --agent code-reviewer --since 24h | jq .

# 비용 폭주 직전 무엇 했나
paperclip activity --agent telegram-chief \
  --before-event budget.warning --window 10m
```

### 영구 보관 (선택)

```yaml
# config
activity:
  retention_days: 90
  export:
    type: s3
    bucket: my-paperclip-audit
    schedule: "0 3 * * *"
```

## ✅ 체크포인트

- [ ] 직원 1명 예산 한도 90%까지 일부러 채워 → 경고 알림 옴
- [ ] hard_stop 직원을 100% 채워 → 정지 + BUDGET_EXCEEDED 티켓 생성
- [ ] critical-file-write 정책 트리거 → admin 승인 요청 옴
- [ ] /approve 또는 /reject 두 케이스 모두 정상 동작
- [ ] `paperclip activity tail`로 이벤트 스트림 확인

## ⚠️ 함정

| 함정 | 대응 |
|------|------|
| 정책이 너무 광범위해 모든 작업이 승인 대기 | `paths` `command_pattern`을 구체적으로 |
| Approval timeout — 직원이 무한 대기 | 정책에 `timeout: 1h` + 자동 reject |
| 예산 리셋 시점 헷갈림 | 회사 `timezone` 명시. `paperclip budget reset --dry-run`으로 확인 |
| 로그 비대화 (수GB) | retention + S3 export 또는 `paperclip activity prune` |
| 승인자가 자리 비움 | delegation: `escalation_after: 30m → admin@example.com` |

## 🔗 다음

→ 정기 작업 (Routines & Tickets) → [04-routines-and-tickets.md](04-routines-and-tickets.md)
