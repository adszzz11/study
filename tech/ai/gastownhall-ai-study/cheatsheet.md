---
date: 2026-04-01
tags:
  - tech
  - gas-town
  - cheatsheet
parent: "[[README]]"
---

# Gas Town - 치트시트

> [[README|목차로 돌아가기]]

---

## 설치 & 설정

```bash
# 설치 (3가지 방법)
brew install gastown              # Homebrew (권장)
npm install -g @gastown/gt        # npm
go install github.com/steveyegge/gastown/cmd/gt@latest  # Go 소스

# 사전 요구사항
# Go 1.25+, Git 2.25+, Dolt 1.82.4+, SQLite3, tmux 3.0+
# Claude Code CLI 또는 GitHub Copilot CLI

# 초기화
gt install ~/gt --git
cd ~/gt
gt config agent list
```

---

## 자주 사용하는 명령어

### 기본 운영

| 명령어 | 설명 |
|--------|------|
| `gt mayor attach` | Mayor(코디네이터) 연결 |
| `gt sling <bead-id> <rig>` | 작업을 Rig에 할당 |
| `gt prime` | 크래시 후 복구 |
| `gt config agent list` | 설정된 에이전트 목록 확인 |

### Convoy (배치 작업)

| 명령어 | 설명 |
|--------|------|
| `gt convoy create "<이름>" <bead1> <bead2> --notify` | Convoy 생성 |
| `gt convoy create "<이름>" <beads> --notify --mountain` | 자율 정체 감지 Convoy |
| `gt convoy list` | 활성 Convoy 목록 |
| `gt convoy show "<이름>"` | Convoy 상세 조회 |

### Bead (작업 단위)

| 명령어 | 설명 |
|--------|------|
| `gt bead list` | 전체 Bead 목록 |
| `gt bead list --status done` | 완료된 Bead 목록 |
| `gt bead show <bead-id>` | Bead 상세 조회 |

### Hook (작업 큐)

| 명령어 | 설명 |
|--------|------|
| `gt hook list` | 현재 Hook 상태 확인 |
| `gt handoff` | 작업 인수인계 |

### Seance (이전 세션 질의)

| 명령어 | 설명 |
|--------|------|
| `gt seance <agent-name> "<질문>"` | 이전 세션 에이전트에게 질의 |

### Molecule (워크플로우)

| 명령어 | 설명 |
|--------|------|
| `bd formula list` | Formula 목록 |
| `bd cook <formula> --var key=value` | Formula 실행 |
| `gt molecule status <name>` | Molecule 실행 상태 |

### Worktree (교차 Rig)

| 명령어 | 설명 |
|--------|------|
| `gt worktree create <target-rig> --from <source>` | 교차 Rig 워크트리 생성 |
| `gt mr create <rig> "<설명>"` | MR 생성 |

### 에스컬레이션

| 명령어 | 설명 |
|--------|------|
| `gt escalation list` | 에스컬레이션 목록 |
| `gt escalation create --severity HIGH --message "<내용>"` | 수동 에스컬레이션 |

---

## 역할 빠른 참조

| 역할 | 범위 | 수명 | 한 줄 설명 |
|------|------|------|-----------|
| **Overseer** | Town | 영구 | 인간 운영자 |
| **Mayor** | Town | 장기 | 주 코디네이터 AI |
| **Deacon** | Town | 장기 | 건강 감시 데몬 |
| **Dog** | Town | 단기 | Deacon 보조 |
| **Witness** | Rig | 장기 | Polecat 관리자 |
| **Polecat** | Rig | 임시 | 일회성 워커 |
| **Crew** | Rig | 장기 | 지속 워커 |
| **Refinery** | Rig | 장기 | 머지 큐 처리 |

---

## MEOW 스택 빠른 참조

```
Formula (TOML)          ← 워크플로우 선언
  └─ Protomolecule      ← 재사용 템플릿
       └─ Molecule      ← 실행 중 인스턴스
            └─ Epic     ← Bead 그룹
                 └─ Bead (JSONL)  ← 원자적 작업
```

---

## 핵심 원칙 빠른 참조

| 원칙 | 의미 |
|------|------|
| **GUPP** | Hook에 작업이 있으면 반드시 실행 |
| **Sessions are cattle** | 세션은 일회용, 에이전트는 영속 |
| **Physics over Politeness** | 혼돈을 Git으로 수용 |
| **Design is the bottleneck** | 구현이 아닌 설계가 병목 |

---

## 디렉토리 구조

```
~/gt/                     # Town 루트
├── .gt/                  # 설정
├── mayor/                # Mayor 워크스페이스
├── deacon/               # Deacon 데몬
└── <rig>/                # 프로젝트별
    ├── .beads/           # Bead 저장소
    ├── crew/             # Crew 워크스페이스
    ├── polecats/         # Polecat 워크트리
    ├── witness/          # Witness 설정
    └── refinery/         # 머지 큐 설정
```

---

## 트러블슈팅

| 증상 | 해결 |
|------|------|
| 에이전트 정체 (30분+) | `gt escalation create --severity HIGH` |
| 크래시 후 작업 유실 | `gt prime` 으로 Hook에서 복구 |
| 머지 충돌 폭발 | Refinery 로그 확인, 작업 분할 재검토 |
| 컨텍스트 유실 | `gt seance <agent> "<질문>"` |
| API 비용 초과 | `gt config` 에서 동시 에이전트 수 조절 |
| Mayor 응답 없음 | `gt mayor detach && gt mayor attach` |

---

## 비용 참고

| 항목 | 비용 |
|------|------|
| 일반 세션 (1시간) | ~$100 |
| 월간 (활발한 사용) | $2,000~$5,000 |
| 비효율 오버헤드 | 30~50% 추가 |

---

## 커뮤니티 & 지원

| 채널 | 링크 |
|------|------|
| Discord | [discord.gg/xHpUGUzZp2](https://discord.gg/xHpUGUzZp2) |
| GitHub | [steveyegge/gastown](https://github.com/steveyegge/gastown) |
| 문서 | [docs.gastownhall.ai](https://docs.gastownhall.ai/) |
| X | [@gastownhall](https://twitter.com/gastownhall) |
| Email | gastownhall@gmail.com |
