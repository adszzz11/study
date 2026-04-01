---
date: 2026-04-01
tags:
  - tech
  - series
  - gas-town
  - ai-agent
  - orchestration
status: learning
type: tech-tool-study
---

# Gas Town (gastownhall.ai)

> **한 줄 정의**: Steve Yegge가 만든 오픈소스 멀티 AI 코딩 에이전트 오케스트레이션 레이어 -- 20~30개의 AI 에이전트를 동시에 관리하며 Git 기반으로 작업 상태를 추적하는 시스템

## 개요

Gas Town은 Claude Code, Codex, Gemini 등 여러 AI 코딩 에이전트를 병렬로 조율하는 워크스페이스 매니저다. 2026년 1월 출시 이후 13.3k GitHub 스타를 기록하며, "한 명의 개발자가 하나의 AI 어시스턴트를 사용하는 패러다임"에서 "개발자가 에이전트 군단을 관리하는 공장 운영자 패러다임"으로의 전환을 대표하는 프로젝트다. Gas Town Hall(gastownhall.ai)은 이 프로젝트의 공식 문서 및 커뮤니티 허브 역할을 한다.

---

## Quick Start

```bash
# 1. 설치 (Homebrew 권장)
brew install gastown

# 2. 초기화
gt install ~/gt --git
cd ~/gt

# 3. 에이전트 확인 및 Mayor 연결
gt config agent list
gt mayor attach
```

---

## 학습 경로

### 1단계: 기초 이해
- [ ] [[01-overview|개요]] 읽기 - 핵심 개념, 아키텍처, 역할 체계
- [ ] [[02-ecosystem|생태계]] 파악 - BMAD, Claude Flow 등 대안 비교

### 2단계: 참고자료 확인
- [ ] [[03-references|참고자료]] 확인 - 공식 문서, Steve Yegge 에세이, 커뮤니티 분석

### 3단계: 핵심 기능 학습
- [ ] [[04-learning/01-architecture|아키텍처]] - 역할 계층, MEOW 스택, 핵심 원칙
- [ ] [[04-learning/02-workflow-patterns|워크플로우 패턴]] - Convoy, Molecule, 작업 관리
- [ ] [[04-learning/03-vibecoding-at-scale|바이브코딩과 스케일링]] - 대규모 에이전트 운영의 현실
- [ ] [[04-learning/04-criticism-and-lessons|비판과 교훈]] - 커뮤니티 반응, 한계, 미래 방향

### 4단계: 실전 적용
- [ ] [[05-projects|실전 프로젝트]] - 인사이트 적용 아이디어
- [ ] [[cheatsheet|치트시트]] - 명령어 빠른 참조

---

## 파일 구조

```
gastownhall-ai-study/
├── README.md                          ← 여기 (개요 + 학습 로드맵)
├── 01-overview.md                     ← 핵심 개념, 아키텍처, 사용 사례
├── 02-ecosystem.md                    ← BMAD, Claude Flow 등 대안 비교
├── 03-references.md                   ← 공식 문서, 에세이, 커뮤니티
├── 04-learning/                       ← 심층 학습
│   ├── 01-architecture.md             ← 역할 계층, MEOW 스택
│   ├── 02-workflow-patterns.md        ← Convoy, Molecule, 작업 흐름
│   ├── 03-vibecoding-at-scale.md      ← 대규모 바이브코딩의 현실
│   └── 04-criticism-and-lessons.md    ← 비판, 교훈, 미래 방향
├── 05-projects.md                     ← 인사이트 적용 프로젝트
└── cheatsheet.md                      ← 명령어 빠른 참조
```

## 바로가기

| 단계 | 파일 | 설명 |
|------|------|------|
| 개요 | [[01-overview]] | 핵심 개념, 아키텍처, 역할 체계 |
| 생태계 | [[02-ecosystem]] | 멀티 에이전트 오케스트레이션 도구 비교 |
| 참고자료 | [[03-references]] | 공식 문서, 에세이, 커뮤니티 자료 |
| 아키텍처 | [[04-learning/01-architecture]] | 역할 계층과 MEOW 스택 |
| 워크플로우 | [[04-learning/02-workflow-patterns]] | Convoy, Molecule 패턴 |
| 바이브코딩 | [[04-learning/03-vibecoding-at-scale]] | 스케일링의 현실과 비용 |
| 비판과 교훈 | [[04-learning/04-criticism-and-lessons]] | 커뮤니티 반응과 미래 방향 |
| 프로젝트 | [[05-projects]] | 인사이트 적용 아이디어 |
| 치트시트 | [[cheatsheet]] | 명령어 빠른 참조 |

---

## 관련 노트

- [[agent-orchestration|에이전트 오케스트레이션]]

---

**생성일**: 2026-04-01
**상태**: 학습 중
