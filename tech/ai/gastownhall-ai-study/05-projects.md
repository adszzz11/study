---
date: 2026-04-01
tags:
  - tech
  - gas-town
  - projects
parent: "[[README]]"
---

# Gas Town - 인사이트 적용 프로젝트

> [[README|목차로 돌아가기]]

---

## 1. 프로젝트 아이디어

Gas Town을 직접 사용하거나, Gas Town의 패턴을 차용하여 적용할 수 있는 프로젝트 아이디어.

| 프로젝트 | 난이도 | 학습 포인트 | Gas Town 필요 여부 |
|----------|--------|------------|-------------------|
| 개인 에이전트 코디네이터 | ⭐⭐ | 계층적 위임, 작업 원자화 | 불필요 -- 패턴만 차용 |
| Git-backed 작업 트래커 | ⭐ | JSONL 상태 관리, Git 영속화 | 불필요 -- Bead 패턴 차용 |
| 멀티 에이전트 코드 리팩토링 | ⭐⭐⭐ | 병렬 작업, 머지 큐 관리 | 선택적 |
| Gas Town 직접 설치 및 체험 | ⭐⭐⭐ | 전체 아키텍처 이해 | 필수 |
| 경량 오케스트레이터 자체 구축 | ⭐⭐⭐ | 오케스트레이션 설계 전반 | 불필요 -- 영감만 차용 |

---

## 2. 프로젝트 상세

### 프로젝트 A: 개인 에이전트 코디네이터 (추천)

**목표**: Gas Town의 핵심 패턴을 활용하여 2~3개 Claude Code 세션을 체계적으로 관리

```
프로젝트 구조:
coordinator/
├── tasks/                    # Bead 패턴 차용
│   ├── TASK-001.json         # 원자적 작업 정의
│   ├── TASK-002.json
│   └── TASK-003.json
├── specs/                    # 설계 문서
│   ├── TASK-001-spec.md      # 작업별 명세
│   └── architecture.md       # 전체 아키텍처
├── status/                   # 작업 상태 추적
│   └── convoy-feature-x.json # Convoy 패턴 차용
└── scripts/
    ├── create-task.sh        # 작업 생성 스크립트
    └── status-check.sh       # 상태 확인 스크립트
```

**핵심 구현**:
1. 작업을 JSON으로 정의 (Bead 패턴)
2. Claude Code 세션 1: 코디네이터 역할 (설계 + 명세 작성)
3. Claude Code 세션 2~3: 워커 역할 (명세 기반 구현)
4. 각 작업을 별도 Git 브랜치에서 수행
5. 순차적 머지로 충돌 관리

### 프로젝트 B: Git-backed 작업 트래커

**목표**: Bead 시스템의 핵심을 JSONL 기반으로 구현

```bash
# 작업 생성
echo '{"id":"PROJ-001","title":"API 설계","status":"todo","created":"2026-04-01"}' \
  >> .tasks/beads.jsonl

# 상태 업데이트
jq 'select(.id=="PROJ-001") | .status = "done"' .tasks/beads.jsonl

# Git으로 영속화
git add .tasks/
git commit -m "📝 PROJ-001 완료"
```

### 프로젝트 C: Gas Town 직접 체험

**목표**: Gas Town을 설치하고 Mayor 워크플로우를 체험

```bash
# 사전 요구사항 설치
brew install go git dolt tmux

# Gas Town 설치
brew install gastown

# 초기화
gt install ~/gt --git
cd ~/gt

# Mayor만으로 시작 (권장 입문 방법)
gt config agent list
gt mayor attach

# 간단한 작업 할당
gt sling gt-test01 my-test-project
```

---

## 3. Best Practices

### Gas Town 패턴 적용 시

- **설계 먼저**: 에이전트에게 구현 전 반드시 설계 문서 작성 요청
- **작업 원자화**: 하나의 작업 = 하나의 PR 수준으로 쪼개기
- **상태 외부화**: 에이전트 대화에만 의존하지 말고 파일/Git에 상태 저장
- **검증 게이트**: 자동 테스트를 통과해야만 머지 가능하도록 설정
- **점진적 확장**: 1~2개 에이전트부터 시작하여 점차 늘려가기

### 피해야 할 안티패턴

- 설계 없이 바로 구현 지시
- 에이전트 수만 늘리면 생산성이 올라갈 것이라는 기대
- 코드 리뷰 없이 자동 머지
- 모든 작업을 병렬로 처리하려는 시도 (의존성 있는 작업은 순차)

---

## 4. 실무 적용 시 고려사항

### 비용

- Gas Town 직접 사용 시 월 $2,000~$5,000 API 비용 예상
- 패턴만 차용하면 일반 Claude Code 비용으로 유사 효과
- ROI 계산: 시간 절감 > API 비용인지 사전 검증

### 보안

- 에이전트가 생성한 코드의 보안 취약점 검사 필수
- 민감한 정보(API 키, 비밀번호)가 Bead/작업 파일에 포함되지 않도록 주의
- .gitignore에 민감 정보 패턴 추가

### 모니터링

- 에이전트 작업 상태를 주기적으로 확인 (최소 30분 간격)
- 비용 모니터링 대시보드 설정 (API 사용량 알림)
- 머지 실패율 추적 -- 높으면 작업 분할 전략 재검토

---

## 5. 관련 도구 체험 로드맵

| 순서 | 도구 | 체험 목표 | 소요 시간 |
|------|------|----------|----------|
| 1 | Claude Code 단독 | 단일 에이전트 숙달 | 1~2주 |
| 2 | Claude Code + Git worktree | 병렬 작업 기초 | 1주 |
| 3 | Gas Town (Mayor만) | 코디네이터 패턴 체험 | 2~3일 |
| 4 | Gas Town (Polecat 추가) | 멀티 에이전트 체험 | 1주 |
| 5 | BMAD 또는 Claude Flow | 대안 비교 | 1주 |
