---
date: 2026-03-28
tags:
  - tech
  - series
  - vibe-kanban
status: learning
type: tech-tool-study
---

# Vibe Kanban

> **한 줄 정의**: 칸반 보드 + 내장 diff 리뷰어를 갖춘 AI 에이전트 병렬 실행 플랫폼

## 개요

Vibe Kanban(BloopAI)은 AI 코딩 에이전트를 칸반 보드 형태로 관리하는 오케스트레이션 플랫폼이다. 각 에이전트 작업을 칸반 카드로 표현하고, git worktree 격리 + 내장 diff 리뷰어(GitHub PR 스타일)로 결과를 리뷰/머지한다. CLI와 Web UI 모두 제공하며, Apache 2.0 라이선스 오픈소스다.

---

## Quick Start

```bash
# 1. 설치
npm install -g vibe-kanban
# 또는
npx vibe-kanban

# 2. 프로젝트에서 실행
cd my-project
vibe-kanban

# 3. 웹 UI에서 에이전트 추가 → 작업 할당 → 병렬 실행
```

---

## 학습 경로

### 1단계: 기초 이해
- [ ] [[01-overview|개요]] 읽기 - 핵심 개념, 장단점
- [ ] [[02-ecosystem|생태계]] 파악 - 관련 기술, 비교

### 2단계: 참고자료 확인
- [ ] [[03-references|참고자료]] 확인 - 공식 문서, 학습 자료

---

## 파일 구조

```
vibe-kanban/
├── README.md              ← 여기 (개요 + 학습 로드맵)
├── 01-overview.md         ← 핵심 개념, 장단점, 사용 사례
├── 02-ecosystem.md        ← 관련 기술, 비교, 트렌드
└── 03-references.md       ← 공식 문서, 학습 자료
```

## 바로가기

| 단계 | 파일 | 설명 |
|------|------|------|
| 개요 | [[01-overview]] | 핵심 개념, 장단점, 사용 사례 |
| 생태계 | [[02-ecosystem]] | 관련 기술 비교, 트렌드 |
| 참고자료 | [[03-references]] | 공식 문서, 학습 자료 |

---

## 관련 노트

- [[study/tech/ai/agent-orchestration/README|AI 에이전트 오케스트레이션]]

---

**생성일**: 2026-03-28
**상태**: 학습 중
