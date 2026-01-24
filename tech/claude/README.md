---
date: 2026-01-24
tags:
  - tech
  - series
  - ai
  - llm
status: learning
type: tech-series
---

# Claude

> **한 줄 정의**: Anthropic이 개발한 AI 어시스턴트로, 안전하고 유용한 대화형 AI를 목표로 설계됨

## 개요

```mermaid
graph LR
    A[기초] --> B[API]
    B --> C[Claude Code]
    C --> D[심화]

    style A fill:#e1f5ff
    style D fill:#ffe1e1
```

## 학습 경로

### 1단계: 기초 (30분)
- [ ] [[01-basics|기초 개념]] 읽기
- [ ] Claude 모델 종류 이해 (Opus, Sonnet, Haiku)
- [ ] Constitutional AI 개념 이해

### 2단계: API (1시간)
- [ ] [[02-api|Claude API]] 학습
- [ ] Messages API 구조 이해
- [ ] Tool Use (Function Calling) 학습

### 3단계: Claude Code (1시간)
- [ ] [[03-claude-code|Claude Code]] 실습
- [ ] CLI 설치 및 설정
- [ ] 프로젝트 연동

### 4단계: 심화 (선택)
- [ ] [[04-advanced|심화 학습]]
- [ ] 프롬프트 엔지니어링
- [ ] Agent SDK

---

## 파일 구조

```
claude/
├── README.md          ← 여기 (개요 + 로드맵)
├── 01-basics.md       ← 기초 (모델, 특징)
├── 02-api.md          ← API (Messages, Tool Use)
├── 03-claude-code.md  ← Claude Code CLI
└── 04-advanced.md     ← 심화 (프롬프트, Agent)
```

## 바로가기

| 단계 | 파일 | 설명 |
|------|------|------|
| 기초 | [[01-basics]] | Claude 모델, Constitutional AI |
| API | [[02-api]] | Messages API, Tool Use |
| Claude Code | [[03-claude-code]] | CLI 도구 사용법 |
| 심화 | [[04-advanced]] | 프롬프트 엔지니어링, Agent |

---

## 관련 노트

- [[study/tech/http/pre/api-design|API 설계]]

---

**생성일**: 2026-01-24
**상태**: 학습 중
