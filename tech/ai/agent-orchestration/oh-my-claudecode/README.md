---
date: 2026-03-28
tags:
  - tech
  - series
  - oh-my-claudecode
status: learning
type: tech-tool-study
---

# oh-my-claudecode (OMC)

> **한 줄 정의**: Claude Code를 위한 32개 전문 에이전트 + 스마트 모델 라우팅으로 토큰 30-50% 절감하는 오케스트레이션 레이어

## 개요

oh-my-claudecode(OMC)는 Claude Code CLI 위에 올리는 확장 레이어로, 32개 전문 에이전트와 40+ 스킬을 통해 작업을 자동으로 분류하고 적절한 모델(Haiku→Sonnet→Opus)로 라우팅한다. 최대 5개 워커를 병렬로 실행하며, 소크라테스식 질문 모드로 요구사항을 정교화한다. 토큰 사용량을 30-50% 절감하는 것이 핵심 가치.

---

## Quick Start

```bash
# 1. 설치 (Claude Code CLI가 먼저 필요)
npm install -g oh-my-claudecode

# 2. 설정 (Anthropic API 키 또는 Claude Max/Pro 구독 필요)
omc init

# 3. 실행
omc start
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
oh-my-claudecode/
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
- [[study/tech/ai/claude/03-claude-code|Claude Code]]

---

**생성일**: 2026-03-28
**상태**: 학습 중
