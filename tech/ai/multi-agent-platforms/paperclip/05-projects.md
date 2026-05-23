# Part 5. 실전 프로젝트 — 맥미니 자치 운영

> 사용자의 진짜 목표: **"맥미니의 모든 걸 관리하는 AI 인프라"**. Paperclip을 관제탑으로 시작.

## 🎯 Project A. 맥미니 자치 OS (메인 프로젝트)

### 아키텍처

```
┌──────────────────────────────────────────────────────────┐
│  Mac mini M4 Pro                                          │
│                                                            │
│  Paperclip (관제탑, http://localhost:3000)                │
│        │                                                   │
│  ┌─────┼──────────┬──────────┬──────────┬───────┐         │
│  ▼     ▼          ▼          ▼          ▼       ▼         │
│ chief  mail     pr-bot    research    notes  sysadmin     │
│ (TG)   (Gmail)  (GitHub)  (Browser)   (Vault)  (Bash)     │
│  │                                                         │
│  │     ┌────────────┐                                     │
│  └──►│ Letta 공유메모리 │◄── 모든 직원 참조                  │
│        └────────────┘                                     │
│                                                            │
│  Ollama (qwen2.5:14b, 로컬, 민감 데이터용)                │
│                                                            │
└──────────────────────────────────────────────────────────┘
```

### 직원 명단

| 직원 | 런타임 | 책임 | 예산/월 | LLM |
|------|--------|------|---------|-----|
| **chief** | OpenClaw 또는 Hermes | TG/Discord 응대·위임 | $50 | claude-opus-4-7 |
| **mail** | claude-code | 메일 분류·답장 초안 | $10 | claude-sonnet-4-6 |
| **pr-bot** | claude-code | GitHub PR 점검 | $10 | claude-sonnet-4-6 |
| **research** | claude-code | 리서치·요약 | $15 | mixed |
| **notes** | claude-code | Obsidian 정리 | $5 | ollama/qwen2.5 |
| **sysadmin** | bash | 백업·디스크·재시작 | $0 | (LLM 없음) |
| **monitor** | python | CPU/디스크 모니터링 | $0 | (LLM 없음) |
| **updater** | bash | 이미지/패키지 업데이트 | $2 | haiku-4-5 |

총 예산: $92/월 + 회사 한도 $100 (안전 마진).

### 핵심 루틴

```yaml
- morning-briefing  @ 07:00       chief
- hourly-pr-check   @ * h         pr-bot → chief
- mail-triage       @ 09:00, 15:00 mail → chief
- daily-backup      @ 02:00        sysadmin
- disk-check        @ */2 h        monitor
- weekly-cleanup    @ Sat 10:00    notes
- monthly-report    @ 1d 09:00     research → chief
```

### 거버넌스 정책

```yaml
- shell-destructive: admin 승인 (rm/dd/format)
- email-external: chief 승인 (외부 도메인 수신)
- file-write-system: admin 승인 (/etc, ~/.ssh)
- budget-exceed: hard_stop 모두 ON
- delegation-loop: 위임 깊이 max 3
```

### 셋업 순서 (Day별)

1. **Day 1**: Paperclip + Postgres + "Home OS" 회사 생성
2. **Day 2**: chief (OpenClaw) 직원 등록 + 텔레그램 페어링
3. **Day 3**: mail/pr-bot/research 추가 + delegation_allowed 설정
4. **Day 4**: sysadmin/monitor (Bash/Python 직원) — LLM 없는 안정 직원
5. **Day 5**: Letta 메모리 백엔드 연결
6. **Day 6**: 거버넌스 정책 + Tailscale 외부접근
7. **Day 7-**: 1주일 사용 후 회고 → 직원 조정

## 🎯 Project B. 가족용 1인 회사 (소규모)

소박한 버전: chief 1명 + mail 1명 + reminder 1명.

```yaml
agents:
  - id: family-chief
    runtime: openclaw
    channels: [telegram]   # 가족 그룹
    budget: $20
  - id: family-mail
    runtime: claude-code
    budget: $5
  - id: family-reminder
    runtime: bash
    schedule: "0 19 * * *"   # 매일 19시 일정 알림
```

가족 카톡 대신 텔레그램 가족 그룹에서 봇이 일정 알람·할일 정리.

## 🎯 Project C. 사이드 프로젝트 자동화

매 프로젝트마다 회사 1개:

```yaml
companies:
  - id: zone-app
    budget: $40
    agents: [code-reviewer, deployer, customer-support]
  - id: blog-project
    budget: $15
    agents: [writer, publisher, seo-checker]
```

회사별 데이터 격리 → 사이드 프로젝트끼리 컨텍스트 안 섞임.

## 🎯 Project D. 학습 보조 회사

```yaml
agents:
  - id: tutor
    runtime: claude-code
    workspace: /Users/sm/study
    skills: [explain, quiz, summarize]
    budget: $10
  - id: spaced-repetition
    runtime: bash
    routine: "0 21 * * *"
    command: "anki-cli review"
```

매일 저녁 학습 + 주말 자동 요약.

## 🧭 Best Practices

- [ ] **회사부터 분리**: 개인용, 가족용, 사이드 프로젝트별 → 데이터/예산 격리
- [ ] **chief 1명은 필수**: 사용자가 직접 상대하는 단일 직원. 다른 직원은 chief 뒤로
- [ ] **LLM 없는 직원 적극 활용**: bash/python 직원이 안전·저비용
- [ ] **delegation 깊이 제한**: max 3. 더 깊으면 디버깅 지옥
- [ ] **routine은 idempotent**: 두 번 실행돼도 같은 결과
- [ ] **첫 2주는 hard_stop 적극**: 패턴 안 잡힌 상태에서 폭주 위험
- [ ] **감사로그 정기 검토**: 주 1회는 `paperclip activity --since 7d` 훑기

## 📈 KPI 예시

| 지표 | 목표 |
|------|------|
| 월 LLM 비용 | 회사 한도의 70-90% |
| 직원당 평균 응답 시간 | < 10s |
| Routine 성공률 | > 98% |
| 승인 대기 시간 (p50) | < 5분 |
| 감사 누락 이벤트 | 0건 |

## 🔗 cheatsheet → [cheatsheet.md](cheatsheet.md)
