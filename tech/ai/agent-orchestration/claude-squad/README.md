---
date: 2026-03-28
tags:
  - tech
  - series
  - claude-squad
status: learning
type: tech-tool-study
---

# Claude Squad

> **한 줄 정의**: tmux 기반으로 여러 AI 코딩 에이전트를 git worktree 격리된 환경에서 관리하는 CLI 도구

## 개요

Claude Squad는 여러 AI 코딩 에이전트(Claude Code, Codex, Aider 등)를 각각 독립된 git worktree에서 실행하고 tmux 세션으로 관리하는 터미널 도구다. `brew install claude-squad` 한 줄로 설치할 수 있고, 자동 수락(auto-accept) 모드로 백그라운드 실행을 지원한다.

---

## Quick Start

```bash
# 1. 설치
brew install claude-squad

# 2. 실행
cs

# 3. 새 에이전트 추가 → 작업 할당 → 병렬 실행
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
claude-squad/
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
