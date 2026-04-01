---
date: 2026-04-01
tags:
  - tech
  - symphony
  - openai
  - cheatsheet
parent: "[[README]]"
---

# Symphony - 치트시트

> [[README|목차로 돌아가기]]

---

## 설치 & 설정

```bash
# 저장소 클론
git clone https://github.com/openai/symphony
cd symphony/elixir

# Elixir 런타임 설치 (mise)
mise trust && mise install
mise exec -- elixir --version

# 의존성 설치 및 빌드
mise exec -- mix setup
mise exec -- mix build

# 환경변수
export LINEAR_API_KEY="lin_api_xxxxx"
```

---

## 자주 사용하는 명령어

| 명령어 | 설명 |
|--------|------|
| `./bin/symphony ./WORKFLOW.md` | Symphony 시작 |
| `./bin/symphony ./WORKFLOW.md --port 4000` | 대시보드 포함 시작 |
| `./bin/symphony ./WORKFLOW.md --logs-root ./log` | 커스텀 로그 디렉토리 |
| `make all` | 전체 품질 게이트 (format, lint, test, dialyzer) |
| `make e2e` | 실제 Linear + Codex 엔드투엔드 테스트 |
| `mix specs.check` | @spec 검사 |
| `mix pr_body.check --file body.md` | PR 본문 검사 |

---

## WORKFLOW.md 최소 설정

```yaml
---
tracker:
  kind: linear
  project_slug: "your-slug-here"
workspace:
  root: ~/code/workspaces
---
You are working on {{ issue.identifier }}: {{ issue.title }}
{{ issue.description }}
```

---

## 설정 옵션 빠른 참조

### tracker

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `kind` | (필수) | `linear` |
| `api_key` | `$LINEAR_API_KEY` | API 키 |
| `project_slug` | (필수) | Linear 프로젝트 슬러그 |
| `active_states` | `[Todo, In Progress]` | 활성 상태 |
| `terminal_states` | `[Closed, Cancelled, Canceled, Duplicate, Done]` | 종료 상태 |

### polling

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `interval_ms` | `30000` | 폴링 간격 (30초) |

### workspace

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `root` | `<temp>/symphony_workspaces` | 워크스페이스 루트 |

### hooks

| 옵션 | 기본값 | 실패 시 |
|------|--------|--------|
| `after_create` | null | **FATAL** (생성 중단) |
| `before_run` | null | **FATAL** (실행 중단) |
| `after_run` | null | 무시 |
| `before_remove` | null | 무시 |
| `timeout_ms` | `60000` | 1분 |

### agent

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `max_concurrent_agents` | `10` | 동시 에이전트 수 |
| `max_turns` | `20` | 연속 턴 최대 횟수 |
| `max_retry_backoff_ms` | `300000` | 재시도 최대 백오프 (5분) |
| `max_concurrent_agents_by_state` | `{}` | 상태별 동시 제한 |

### codex

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `command` | `codex app-server` | Codex 실행 명령 |
| `approval_policy` | 구현 정의 | 승인 정책 |
| `thread_sandbox` | 구현 정의 | 세션 샌드박스 |
| `turn_sandbox_policy` | 구현 정의 | 턴별 샌드박스 |
| `turn_timeout_ms` | `3600000` | 턴 타임아웃 (1시간) |
| `read_timeout_ms` | `5000` | 읽기 타임아웃 |
| `stall_timeout_ms` | `300000` | 정체 감지 (5분) |

---

## 프롬프트 템플릿 변수

```
{{ issue.identifier }}       # ABC-123
{{ issue.id }}               # Linear 내부 ID
{{ issue.title }}            # 이슈 제목
{{ issue.description }}      # 이슈 설명 (null 가능)
{{ issue.state }}            # 현재 상태
{{ issue.priority }}         # 우선순위 (1-4)
{{ issue.url }}              # Linear URL
{{ issue.labels }}           # 라벨 목록
{{ issue.branch_name }}      # 브랜치명
{{ issue.blocked_by }}       # 블로커 목록
{{ issue.created_at }}       # 생성 시각
{{ issue.updated_at }}       # 수정 시각
{{ attempt }}                # 재시도 횟수 (첫 실행 null)
```

---

## 오케스트레이션 상태 머신

```
Unclaimed ──(디스패치)──► Claimed ──(워커시작)──► Running
                            │                      │
                            │                      ├──(정상종료)──► RetryQueued (1초)
                            │                      ├──(실패)────► RetryQueued (백오프)
                            │                      └──(Terminal)─► Released
                            │
                            └──(재시도예약)──► RetryQueued
                                                   │
                                                   ├──(재디스패치)──► Running
                                                   └──(비활성)────► Released
```

---

## 재시도 백오프 표

| Attempt | 지연 시간 | 계산 |
|---------|----------|------|
| 정상 종료 | 1초 | 고정 |
| 1 | 10초 | 10000 * 2^0 |
| 2 | 20초 | 10000 * 2^1 |
| 3 | 40초 | 10000 * 2^2 |
| 4 | 80초 | 10000 * 2^3 |
| 5 | 160초 | 10000 * 2^4 |
| 6+ | 300초 (cap) | min(계산값, 300000) |

---

## Codex App Server 핸드셰이크

```
1. initialize      → 클라이언트 정보 + 능력 교환
2. initialized     → 알림 (응답 없음)
3. thread/start    → 스레드 생성 (thread_id 획득)
4. turn/start      → 턴 시작 (turn_id 획득)
   ↕ 스트리밍       → 진행 이벤트, 승인 요청, 도구 호출
5. turn/completed  → 턴 완료
   또는 turn/failed → 턴 실패
```

---

## 안전성 불변식 (3대 규칙)

| # | 규칙 | 내용 |
|---|------|------|
| 1 | CWD 격리 | Codex `cwd` = 반드시 워크스페이스 경로 |
| 2 | 경로 봉쇄 | 워크스페이스 경로 = workspace_root의 하위 |
| 3 | 키 새니타이징 | 디렉토리명에 `[A-Za-z0-9._-]` 외는 `_`로 |

---

## API 엔드포인트 (대시보드)

| 경로 | 메서드 | 설명 |
|------|--------|------|
| `/` | GET | LiveView 대시보드 |
| `/api/v1/state` | GET | 전체 오케스트레이터 상태 |
| `/api/v1/<identifier>` | GET | 특정 이슈 상태 |
| `/api/v1/refresh` | POST | 즉시 폴링 트리거 |

---

## Skills (Codex 스킬)

| 스킬 | 파일 | 용도 |
|------|------|------|
| commit | `.codex/skills/commit/SKILL.md` | 깔끔한 커밋 생성 |
| push | `.codex/skills/push/SKILL.md` | 리모트 브랜치 푸시 |
| pull | `.codex/skills/pull/SKILL.md` | origin/main 동기화 |
| land | `.codex/skills/land/SKILL.md` | PR 안전 머지 |
| linear | `.codex/skills/linear/SKILL.md` | Linear 이슈 조작 |
| debug | `.codex/skills/debug/SKILL.md` | 디버깅 가이드 |

---

## 트러블슈팅

| 증상 | 해결 |
|------|------|
| `missing_workflow_file` | WORKFLOW.md 경로 확인, `./bin/symphony /path/to/WORKFLOW.md` |
| `workflow_parse_error` | YAML 문법 확인 (들여쓰기, 콜론 뒤 공백) |
| 이슈가 감지되지 않음 | `tracker.project_slug` 확인, `active_states`에 이슈 상태 포함 여부 |
| 워크스페이스 생성 실패 | `workspace.root` 경로 존재 여부, 쓰기 권한 확인 |
| `after_create` 훅 실패 | git clone URL, SSH 키 설정 확인, timeout_ms 증가 |
| Codex 세션 시작 실패 | Codex CLI 설치 여부, OpenAI API 키 확인 |
| 정체(stall) 자주 발생 | `stall_timeout_ms` 증가 또는 네트워크 확인 |
| 재시도 무한 반복 | 이슈 상태가 active인데 에이전트가 완료 못 하는 경우. 이슈 설명 개선 필요 |
| 대시보드 접근 불가 | `--port` 옵션 지정 여부 확인 |
| 환경변수 인식 안 됨 | `$VAR` 형식으로 WORKFLOW.md에 지정, 쉘에서 export 확인 |

---

## 핵심 코드 패턴

### 후보 선택 조건 (7가지 AND)

```
1. 필수 필드 존재 (id, identifier, title, state)
2. active_states에 포함
3. terminal_states에 미포함
4. running에 없음
5. claimed에 없음
6. 전역 동시성 슬롯 가용
7. Todo이면 블로커 전부 terminal
```

### 디스패치 우선순위

```
1. priority 오름차순 (1 > 2 > 3 > 4 > null)
2. created_at 오래된 순
3. identifier 사전순 (타이브레이커)
```
