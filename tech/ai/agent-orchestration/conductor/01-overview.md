---
date: 2026-03-28
tags:
  - tech
  - conductor
  - overview
parent: "[[README]]"
---

# Conductor - 개요

> [[README|목차로 돌아가기]] | [[02-ecosystem|다음: 생태계]]

---

## 1. What - Conductor란?

> **한 줄 정의**: Claude Code 에이전트를 병렬로 실행하고 시각적 대시보드로 관리하는 macOS 네이티브 앱

### 핵심 개념

Conductor는 Melty Labs(Y Combinator S24)가 개발한 macOS 전용 앱으로, 여러 Claude Code 인스턴스를 동시에 실행하면서 각각을 독립된 git worktree에서 격리한다. 하나의 대시보드에서 모든 에이전트의 상태를 모니터링하고, 결과물을 리뷰/머지할 수 있다.

### 주요 용어

| 용어 | 설명 |
|------|------|
| Agent | 개별 Claude Code 세션 (하나의 작업 단위) |
| Worktree | git worktree로 격리된 작업 디렉토리 |
| Dashboard | 모든 에이전트 상태를 한눈에 보는 GUI |
| Task Queue | 에이전트에게 할당할 작업 목록 |

### 동작 방식

```
사용자 → Conductor 앱 → 작업 할당
                         ├── Agent 1 (worktree-1) → Claude Code 세션
                         ├── Agent 2 (worktree-2) → Claude Code 세션
                         └── Agent 3 (worktree-3) → Claude Code 세션
                                    ↓
                         결과 리뷰 → 메인 브랜치 머지
```

---

## 2. Why - 왜 Conductor인가?

### 해결하려는 문제

- Claude Code 세션 하나로는 처리량에 한계
- 여러 터미널에서 수동으로 에이전트 관리하면 혼란
- 에이전트 간 코드 충돌 위험

### 기존 방식의 한계

| 문제 | 기존 방식 | Conductor |
|------|----------|-----------|
| 병렬 실행 | 터미널 탭 수동 관리 | 대시보드에서 원클릭 실행 |
| 코드 충돌 | 같은 브랜치에서 작업 | git worktree 자동 격리 |
| 상태 파악 | 각 터미널 직접 확인 | 통합 대시보드 |
| 결과 머지 | 수동 git merge | GUI에서 리뷰 & 머지 |

---

## 3. 핵심 특징

### 장점

- **시각적 UX**: GUI 대시보드로 에이전트 상태 한눈에 파악
- **git worktree 격리**: 에이전트 간 충돌 원천 차단
- **macOS 네이티브**: 쾌적한 성능과 OS 통합
- **YC 백킹**: 지속적 개발 기대 가능

### 단점

- **macOS 전용**: Linux/Windows 사용 불가
- **유료**: 오픈소스 대안 대비 비용 발생
- **Claude Code 전용**: Gemini CLI, Codex 등 다른 에이전트 미지원
- **폐쇄적**: 커스터마이즈 제한

---

## 4. 사용 사례

### 적합한 경우

| 사용 사례 | 설명 |
|----------|------|
| 대규모 리팩토링 | 모듈별로 에이전트 분배하여 병렬 작업 |
| 멀티 피처 개발 | 여러 기능을 동시에 각각의 에이전트가 구현 |
| 코드 리뷰 자동화 | 에이전트가 생성한 코드를 대시보드에서 리뷰 |
| 마이그레이션 작업 | 파일/모듈 단위로 분할하여 병렬 마이그레이션 |

---

## 5. 가격 정책

| 플랜 | 가격 | 특징 |
|------|------|------|
| 무료 체험 | $0 | 제한된 에이전트 수 |
| Pro | 유료 (정확한 가격 확인 필요) | 무제한 에이전트, 우선 지원 |

> ⚠️ Conductor 자체 비용 + Claude API/구독 비용이 별도로 발생

---

## 다음 단계

> [!tip] 다음으로
> Conductor의 개요를 이해했다면 [[02-ecosystem|생태계와 대안 도구 비교]]를 살펴보세요.

---

## References

- [공식 사이트](https://www.conductor.build/)
- [The New Stack 리뷰](https://thenewstack.io/a-hands-on-review-of-conductor-an-ai-parallel-runner-app/)
