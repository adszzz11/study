---
date: 2026-05-20
tags:
  - tech
  - series
  - Codex
status: learning
type: tech-tool-study
---

# Codex (OpenAI Codex CLI)

> **한 줄 정의**: OpenAI의 터미널 기반 AI 코딩 에이전트 CLI — Claude Code의 OpenAI 진영 카운터파트.

## 개요

GPT-5.3-Codex 모델(2026-03 출시) 기반의 에이전트 CLI 도구. 터미널 TUI / 헤드리스 모드 / IDE 확장 / GitHub Cloud 통합 / 원격 제어를 모두 지원하며, AGENTS.md(=CLAUDE.md 등가), Skills, MCP, Hooks 시스템으로 워크플로우 자동화. 2026-05 기준 최신 버전 **v0.130.0**.

---

## Quick Start

```bash
# 1. 설치 (npm)
npm install -g @openai/codex

# 2. 인증
codex login

# 3. 실행 (대화형 TUI)
codex

# 4. 비대화형 (CI/CD/스크립트)
codex exec "Add unit tests for src/auth.ts"

# 5. 모델 지정
codex --model gpt-5.3-codex

# 6. AGENTS.md 초기화
codex /init
```

---

## 학습 경로

### 1단계: 기초 이해
- [ ] [[01-overview|개요]] — Codex CLI 정체, GPT-5.3-Codex, Claude Code와의 위치
- [ ] [[02-ecosystem|생태계]] — vs Claude Code / Aider / Cursor 비교

### 2단계: 참고자료 확인
- [ ] [[03-references|참고자료]] — 공식 문서, changelog, 베스트프랙티스 모음

### 3단계: 핵심 기능 학습
- [ ] [[04-learning/01-getting-started|시작하기]] — 설치, 첫 세션, AGENTS.md, Skills

### 4단계: 실전 적용
- [ ] [[05-projects|실전 프로젝트]] — CI 통합, 원격 제어, 팀 설정
- [ ] [[cheatsheet|치트시트]] — 빠른 참조

---

## 파일 구조

```
codex/
├── README.md              ← 여기 (개요 + 학습 로드맵)
├── 01-overview.md         ← Codex CLI 정체, 모델, 핵심 기능
├── 02-ecosystem.md        ← vs Claude Code, 비교 매트릭스, 트렌드
├── 03-references.md       ← 공식 문서, 학습 자료
├── 04-learning/           ← 실습 가이드
│   └── 01-getting-started.md
├── 05-projects.md         ← 실전 워크플로우, Best Practices
└── cheatsheet.md          ← 명령어 / 단축키 빠른 참조
```

## 바로가기

| 단계 | 파일 | 설명 |
|------|------|------|
| 개요 | [[01-overview]] | 핵심 개념, 모델, 주요 기능 |
| 생태계 | [[02-ecosystem]] | Claude Code 비교, 트렌드 |
| 참고자료 | [[03-references]] | 공식 문서, 학습 자료 |
| 시작하기 | [[04-learning/01-getting-started]] | 설치, 첫 세션 |
| 프로젝트 | [[05-projects]] | 실전 예제 |
| 치트시트 | [[cheatsheet]] | 빠른 참조 |

---

## 관련 노트

- [[../claude/README|Claude tool-study]] — 카운터파트
- [[../claude/13-2026-05-latest|Claude 2026-05 최신]]
- [[../ai-ecosystem/README|AI 생태계 노트]]

---

**생성일**: 2026-05-20
**상태**: 학습 중
