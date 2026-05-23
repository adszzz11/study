# 4-2. 직원 채용 — 4가지 런타임 등록

> 시간 ~30분. 결과: Claude Code + OpenClaw + Bash 스크립트 각각 1명씩 회사에 등록 + 첫 작업 실행.

## 📌 핵심: "If it can receive a heartbeat, it's hired"

```
직원 = (어댑터 종류, workspace, 시크릿, 예산, skill)
```

지원 어댑터: `claude-code`, `codex`, `openclaw`, `cursor`, `bash`, `webhook`, `python` (커스텀).

## 👨‍💻 1. Claude Code 직원 등록

### Step 1. 어댑터 검증
```bash
# Claude Code가 시스템에 설치되어 있어야 함
which claude
claude --version
```

### Step 2. 직원 정의 (대시보드 또는 YAML)

`agents/code-reviewer.yaml`:

```yaml
id: code-reviewer
display_name: "Code Reviewer"
runtime: claude-code
company: home-os
workspace: /Users/sm/code/zone
default_model: claude-opus-4-7
budget:
  monthly: 30   # USD
  hard_stop: true
skills:
  - git_review
  - lint_check
secrets:
  - GITHUB_TOKEN
description: |
  PR과 커밋 변경사항을 리뷰하고 한국어 요약 생성.
  보안/성능/스타일 이슈를 우선순위로 정리.
```

### Step 3. 등록
```bash
# CLI로
paperclip agent create -f agents/code-reviewer.yaml

# 또는 API
curl -X POST http://localhost:3000/api/agents \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d @agents/code-reviewer.yaml
```

### Step 4. 첫 작업 (티켓 생성)
```bash
paperclip ticket create \
  --agent code-reviewer \
  --title "Review PR #142" \
  --description "리포 zone의 PR #142 한국어 요약 + 보안 체크"
```

대시보드 → Tickets에서 진행 상황 보임.

## 📱 2. OpenClaw 직원 등록 (메신저 응대)

```yaml
# agents/telegram-chief.yaml
id: telegram-chief
runtime: openclaw
workspace: /Users/sm/openclaw   # OpenClaw 컨테이너와 공유 디렉터리
adapter_config:
  endpoint: http://host.docker.internal:8080   # OpenClaw 게이트웨이
  channels: [telegram, discord]
budget:
  monthly: 50
default_model: claude-opus-4-7
description: 메신저 응대 비서. 다른 직원에게 위임 가능.
delegation_allowed:
  - code-reviewer
  - daily-backup
```

```bash
paperclip agent create -f agents/telegram-chief.yaml
```

OpenClaw가 페어링되어 있다면 텔레그램에서 부르면 chief가 응답.

## 🔧 3. Bash 직원 (LLM 없이)

LLM 호출 없이 정해진 스크립트만 실행하는 "회계 직원" 같은 케이스. **예산 $0**.

```yaml
# agents/daily-backup.yaml
id: daily-backup
runtime: bash
workspace: /Users/sm
command: |
  rsync -av --delete \
    /Users/sm/code/ \
    /Volumes/Backup/code/
budget:
  monthly: 0
routine: "0 2 * * *"   # 매일 02:00
secrets: []
on_failure:
  notify_agent: telegram-chief
  message: "어제 백업 실패 — 디스크 확인 필요"
```

`on_failure.notify_agent` 같은 룰로 직원 간 알림 연계.

## 🌐 4. HTTP Webhook 직원

외부 SaaS (예: Notion publishing 서비스)를 직원으로:

```yaml
# agents/notion-publisher.yaml
id: notion-publisher
runtime: webhook
endpoint: https://notion-bridge.example.com/run
auth:
  type: bearer
  secret_ref: NOTION_BRIDGE_TOKEN   # Paperclip이 안전하게 주입
budget:
  monthly: 5
schema:
  input:
    type: object
    properties:
      page_title: { type: string }
      markdown: { type: string }
    required: [page_title, markdown]
```

`code-reviewer`가 리뷰 끝낸 후 `notion-publisher`를 호출해 결과 페이지 자동 생성.

## 🤝 직원 간 위임 (Delegation)

`telegram-chief.yaml`의 `delegation_allowed`처럼 명시. 위임 시 흐름:

```
사용자 ──"PR 리뷰해줘"──► telegram-chief
                            │
                            │  delegate(code-reviewer, ticket)
                            ▼
                       code-reviewer ── 작업 수행 ─► 결과
                            │
                            ◄── 결과 반환
                            │
사용자 ◄────── 요약 ─────────┘
```

위임도 모두 큐를 거치므로 감사 로그에 남음.

## ✅ 체크포인트

- [ ] `paperclip agent list` → 4명 모두 보임
- [ ] 각 직원의 첫 heartbeat 성공 (대시보드 last_seen)
- [ ] `code-reviewer`로 첫 티켓 처리 → 결과물 확인
- [ ] `daily-backup` 다음 새벽 2시 자동 실행 (cron 결과 확인)
- [ ] `telegram-chief`가 텔레그램 응대 + `code-reviewer`로 위임 동작

## ⚠️ 함정

| 함정 | 대응 |
|------|------|
| Claude Code workspace 권한 부족 | `workspace` 디렉터리에 쓰기 권한 확인. Paperclip은 같은 macOS 사용자로 실행 |
| `delegation_allowed` 미설정 → 위임 실패 | 명시적으로 허용 직원 목록 |
| 시크릿이 평문 노출 | `secrets:` 필드는 이름만. 실제 값은 `paperclip secrets set` |
| Bash 직원이 정지 안 됨 | LLM 비용은 $0이지만 cron은 도는 중. `agent pause`로 명시 정지 |
| Webhook 직원 timeout | 어댑터에 `timeout_sec: 30` 명시 |

## 🔗 다음

→ 예산·승인 워크플로우 → [03-budget-and-governance.md](03-budget-and-governance.md)
