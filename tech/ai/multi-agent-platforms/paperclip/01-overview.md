# Part 1. Paperclip 개요

## 📌 핵심 개념: "회사를 운영하는 OS"

다른 멀티에이전트 프레임워크가 **"에이전트를 코딩하는 라이브러리"**라면, Paperclip은 **"에이전트를 운영하는 회사"**다. 이 차이가 크다.

```
[CrewAI/LangGraph]      [Paperclip]
       │                      │
"코드로 에이전트 정의"   "직원을 채용해서 회사 운영"
       │                      │
   pip install            npx onboard
   .py 파일 작성         대시보드 + DB
   단일 프로세스         heartbeat 기반 분산
```

## 🧩 12개 핵심 모듈

공식 README에서 명시한 subsystem:

| 모듈 | 책임 |
|------|------|
| **Identity & Access** | 사용자/팀/직원 인증 |
| **Org Chart & Agents** | 조직도·직책·보고 라인 |
| **Work & Task System** | 티켓·할당·진행상태 |
| **Heartbeat Execution** | DB 기반 wakeup 큐 (핵심!) |
| **Workspaces & Runtime** | 직원별 작업 디렉터리/환경 |
| **Governance & Approvals** | 승인 워크플로우 |
| **Budget & Cost Control** | 월 예산·hard-stop |
| **Routines & Schedules** | 정기 실행 |
| **Plugins** | Skill/Tool 확장 |
| **Secrets & Storage** | 시크릿 안전 주입 |
| **Activity & Events** | 감사 로그·이벤트 스트림 |
| **Company Portability** | 회사 데이터 export/import |

## 💓 Heartbeat 프로토콜 (가장 중요)

에이전트가 어떤 언어/런타임이든 **이 프로토콜만 따르면 직원이 된다**:

```
Paperclip Control Plane             Agent (any runtime)
        │                                  │
        │  GET /heartbeat?agent_id=…      │
        │ ◄──────────────────────────────│  (poll loop)
        │                                  │
        │  ───────────────────────────►   │
        │  { tasks: [...], secrets:{...}, │
        │    workspace: "/path", skills:…}│
        │                                  │
        │  ◄──────────────────────────────│
        │   POST /result                   │
        │   { task_id, status, output,    │
        │     tokens_in, tokens_out, cost} │
        │                                  │
        ▼                                  ▼
   감사로그·예산차감             다음 heartbeat까지 대기
```

**핵심 속성**:
- DB 큐로 작업 분배 (Redis 같은 메시지 큐 없음 → 단순)
- 시크릿은 매 heartbeat마다 새로 주입 (장기 보관 X)
- 비용은 응답 시 계산 → 예산 hard-stop 가능
- 직원이 죽어도 큐는 유지

## 🏢 직원 등록 예시 (4가지 런타임)

### 1. Claude Code 직원
```yaml
agent: code-reviewer
runtime: claude-code
workspace: /Users/sm/projects/zone
budget: $30/month
skills: [git_review, lint]
routine: "0 9 * * 1-5"  # 평일 9시
```

### 2. OpenClaw 직원
```yaml
agent: telegram-secretary
runtime: openclaw
channels: [telegram]
budget: $10/month
```

### 3. Bash 직원 (LLM 없음)
```yaml
agent: daily-backup
runtime: bash
command: "rsync -av ~/code/ /Volumes/Backup/"
budget: $0
routine: "0 2 * * *"
```

### 4. HTTP webhook 직원
```yaml
agent: notion-publisher
runtime: webhook
endpoint: https://notion-bridge.example.com/run
budget: $5/month
```

## ⚖️ 장단점

### ✅ 장점
- **런타임 자유**: 어떤 에이전트든 채용 가능 (CrewAI/LangGraph 코드와 공존 가능)
- **예산 강제**: hard-stop이 진짜로 멈춤 — 폭주 사고 차단
- **대시보드 빌트인**: React UI로 직원 상태 즉시 확인
- **감사 로그**: 모든 작업 기록 → 사고 추적 쉬움
- **Company Portability**: 회사 단위로 데이터 옮길 수 있음 (vendor lock-in 없음)

### ❌ 단점
- **신생 (2026.3)**: 67k★지만 검증된 운영 사례 적음. Breaking change 가능성
- **Postgres 필수 (권장)**: 데이터 영속화에 RDB 필요 → 운영 부담
- **직원 코드는 별도 작성**: Paperclip 자체는 관제탑일 뿐, 일하는 코드는 직접
- **에이전트 간 직접 통신 제한**: 모든 게 Paperclip 큐 통과 → 지연 추가
- **TypeScript/Node 사용자만 편함**: Python 우선 사용자는 어댑터 작성 필요

## 🎯 누가 쓰면 좋은가

| 상황 | 적합도 |
|------|--------|
| **여러 에이전트 운영 + 비용 통제 필요** | ⭐⭐⭐⭐⭐ |
| **다양한 런타임 혼용 (Claude Code + OpenClaw + 스크립트)** | ⭐⭐⭐⭐⭐ |
| **혼자 코딩 vs 가족·팀과 공유** | ⭐⭐⭐⭐ |
| **에이전트 간 깊은 협업이 필요** | ⭐⭐ (직접 라이브러리가 더 적합) |
| **단일 supre-agent로 충분한 케이스** | ⭐⭐ (오버엔지니어링) |
| **노코드/비주얼만 원함** | ⭐⭐ (대시보드는 있지만 워크플로우 캔버스 X — Dify) |

## 📈 채택 사례

- @dotta(pseudonym)의 개인 자동화 (출시 동기 — 본인 1인 회사 운영)
- 2026.3 출시 후 3주 내 30k★ → 5월 기준 67k★
- ClawHost가 Paperclip + OpenClaw 매니지드로 묶어 제공

## 🔗 다음

- 같은 카테고리 비교 → [02-ecosystem.md](02-ecosystem.md)
- 띄우기 → [04-learning/01-install-and-onboard.md](04-learning/01-install-and-onboard.md)
