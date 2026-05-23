# 4-4. Routines & Tickets — 정기 자동화 + 작업 추적

> 시간 ~15분. 결과: 매일 자동 돌아가는 워크플로우 3개 + 사용자 요청 티켓 처리 모델 이해.

## 📌 핵심 개념

- **Routine** = 정기 실행 작업 (cron 표현식)
- **Ticket** = 일회성 작업 (사용자 요청, 다른 직원의 위임)
- 둘 다 동일하게 **task queue**로 흘러가고, 같은 감사 로그·예산 시스템 적용

## ⏰ Routine 정의

`routines/morning-briefing.yaml`:
```yaml
id: morning-briefing
agent: telegram-chief
schedule: "0 7 * * *"           # 매일 07:00
timezone: Asia/Seoul
input:
  task: |
    오늘의 브리핑을 작성해 텔레그램으로 전송:
    1) 서울 날씨 (현재·최고·최저)
    2) 오늘 캘린더 일정
    3) 새 이메일 중요 3건 요약
    4) GitHub: 내 리뷰 대기 PR
    5) Linear: 이번주 마감 이슈
on_failure:
  retry: 2
  notify: admin
budget_per_run: 0.30   # 1회당 한도 (월 한도와 별도)
```

등록:
```bash
paperclip routine create -f routines/morning-briefing.yaml
paperclip routine list
paperclip routine test morning-briefing   # dry-run
```

## 🌅 더 많은 정기 루틴 예시

### 매시간 PR 점검
```yaml
id: hourly-pr-check
agent: code-reviewer
schedule: "0 * * * *"
input:
  task: "최근 1시간 내 새 PR/코멘트 점검. 중요한 것만 chief에게 위임."
delegation_target: telegram-chief
```

### 주 1회 노트 정리
```yaml
id: weekly-notes-cleanup
agent: research
schedule: "0 10 * * 6"   # 매주 토요일 10시
workspace: /Users/sm/code/leetangle/Note
input:
  task: "지난 주 작성한 노트 중 정리 안 된 것 정돈 (TOC, 태그, wiki-link). 결과를 chief에게 보고."
```

### 매일 백업
```yaml
id: daily-backup
agent: daily-backup       # bash 직원
schedule: "0 2 * * *"
```

## 🎫 Ticket 워크플로우

티켓 = 직원이 처리할 일회성 작업.

### 생성 방법

```bash
# CLI
paperclip ticket create \
  --agent research \
  --title "LangGraph vs CrewAI 정리" \
  --description "프로덕션 적합도 관점에서 비교, 30분 작업, 보고서 마크다운"

# API
curl -X POST http://localhost:3000/api/tickets ...

# 다른 직원이 위임 (delegation 권한 있는 경우)
# telegram-chief가 사용자 메시지 받아 자동 생성
```

### 티켓 상태 라이프사이클

```
created ──► queued ──► in_progress ──► completed
                          │              ▲
                          ├──► failed ───┤ (재시도)
                          ├──► awaiting_approval
                          ├──► blocked   (다른 작업 결과 대기)
                          └──► cancelled
```

### Skill 시스템 활용

직원이 가진 skill에 따라 ticket이 자동 라우팅:

```yaml
# skills/registry.yaml
skills:
  git_review:
    available_to: [code-reviewer]
    description: "Git PR 변경사항 리뷰"
  email_draft:
    available_to: [research, telegram-chief]
  notion_publish:
    available_to: [notion-publisher]
```

티켓에 `required_skills`를 명시하면 적합한 직원에게 자동 할당:

```bash
paperclip ticket create \
  --required-skills git_review,email_draft \
  --title "PR 리뷰 후 매니저에게 메일 초안"
# → code-reviewer가 받음 (git_review) + 결과를 research에 위임 (email_draft)
```

## 🔄 직원 간 협업 패턴 (실전)

### 패턴 1: 순차 (sequential)
```
research → writer → publisher
   (조사)   (작성)    (발행)
```

```yaml
# routines/weekly-report.yaml
id: weekly-report
schedule: "0 18 * * 5"   # 매주 금요일 18시
chain:
  - agent: research
    input: "이번주 AI 뉴스 핵심 5건"
    output_to: $ARTIFACT_1
  - agent: writer
    input: "$ARTIFACT_1을 본 vault 톤으로 마크다운 작성"
    output_to: $ARTIFACT_2
  - agent: notion-publisher
    input: { page_title: "Weekly AI Report", markdown: "$ARTIFACT_2" }
```

### 패턴 2: 팬아웃 (fan-out)
```
chief ─┬─► mail
       ├─► pr-bot
       └─► research
```

chief가 한 사용자 명령을 3명에게 동시 위임 후 결과 통합.

### 패턴 3: 합의 (consensus)
여러 직원이 같은 문제 풀고, chief가 합의:
```yaml
consensus:
  agents: [reviewer-1, reviewer-2, reviewer-3]
  input: "이 PR 머지해도 될까?"
  aggregator: chief
  policy: majority   # 또는 unanimous
```

## ✅ 체크포인트

- [ ] morning-briefing routine 등록 + 다음날 07시 메시지 받음
- [ ] 티켓 1개 수동 생성 → in_progress → completed
- [ ] 순차 chain 1개 동작 (research → writer → publisher)
- [ ] 한 직원이 fail해도 재시도 후 admin 알림 옴
- [ ] `paperclip ticket list --status completed` 어제 완료 작업 보임

## ⚠️ 함정

| 함정 | 대응 |
|------|------|
| Cron 시간대 헷갈림 | 회사 `timezone` 명시, `paperclip routine show`로 next_run 확인 |
| Routine이 겹쳐 실행 | `concurrency: 1` 설정으로 중복 방지 |
| 체인 중간 실패 시 partial state | `on_failure: rollback` 또는 idempotent하게 설계 |
| 티켓 무한 대기 | `max_lifetime: 1h` 후 자동 fail |
| 직원 부하 과도 | 직원별 `max_concurrent_tasks: 3` |

## 🔗 다음

→ 실전 프로젝트 → [../05-projects.md](../05-projects.md)
