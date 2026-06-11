---
date: 2026-06-09
tags:
  - tech
  - devtools
  - claude
  - dynamic-workflows
status: learning
type: tech-tool-study
---

# Claude Dynamic Workflows

> **한 줄 정의**: Claude Code가 task-specific JavaScript orchestration script를 생성하고, 별도 runtime이 다수의 subagents를 병렬 실행해 대규모 작업을 검증·종합하는 multi-agent workflow 기능.

## 개요

Claude Dynamic Workflows는 Claude Code의 기본 agent loop를 넘어서는 대규모 작업용 orchestration 기능이다. Claude가 작업마다 custom harness를 JavaScript로 만들고, workflow runtime이 그 script를 실행하면서 subagent fan-out, 검증, 종합, 반복을 관리한다.

- 공개 상태: research preview
- 공개일: 2026-05-28 announcement, 2026-06-02 deep dive
- 핵심 위치: [[study/tech/ai/claude/03-claude-code]]의 고강도 작업 모드
- 관련 축: [[study/tech/ai/multi-agent-platforms]], [[study/tech/ai/codex]]

---

## Quick Start

```bash
# 1. Claude Code 버전 확인
claude --version

# 2. /config에서 Dynamic workflows 활성화 여부 확인
/config

# 3. 작은 범위로 workflow 요청
ultracode: audit src/auth for missing permission checks

# 4. 실행 중 상태 확인
/workflows

# 5. 성공한 workflow 저장
# /workflows UI에서 s(save)로 .claude/workflows/ 또는 ~/.claude/workflows/에 저장
```

---

## 학습 경로

### 1단계: 기초 이해
- [ ] [[01-overview|개요]] - What/Why, architecture, trigger, 제한
- [ ] [[02-ecosystem|생태계]] - Claude subagents, Skills, Codex, Copilot, LangGraph, AutoGen 비교

### 2단계: 참고자료 확인
- [ ] [[03-references|참고자료]] - 공식 문서, announcement, deep dive, FAQ

### 3단계: 핵심 기능 학습
- [ ] [[04-learning/01-getting-started|시작하기]] - 작은 audit workflow 실행
- [ ] [[04-learning/02-deep-dive|딥다이브]] - orchestration pattern과 prompt 설계

### 4단계: 실전 적용
- [ ] [[05-projects|실전 프로젝트]] - security sweep, migration, deep research
- [ ] [[cheatsheet|치트시트]] - trigger, 제한, prompt checklist 빠른 참조

---

## 파일 구조

```text
claude의-dynamic-workflow에-대해-알려줘/
├── README.md
├── 01-overview.md
├── 02-ecosystem.md
├── 03-references.md
├── 04-learning/
│   ├── 01-getting-started.md
│   └── 02-deep-dive.md
├── 05-projects.md
└── cheatsheet.md
```

## 바로가기

| 단계 | 파일 | 설명 |
|------|------|------|
| 개요 | [[01-overview]] | What/Why, 특징, 아키텍처 |
| 생태계 | [[02-ecosystem]] | 경쟁/대안 비교 |
| 참고자료 | [[03-references]] | 공식 문서와 소스 |
| 시작하기 | [[04-learning/01-getting-started]] | 첫 workflow 실행 |
| 딥다이브 | [[04-learning/02-deep-dive]] | pattern, budget, verifier 설계 |
| 프로젝트 | [[05-projects]] | 실전 적용 시나리오 |
| 치트시트 | [[cheatsheet]] | 빠른 참조 |

---

## 관련 노트

- [[study/tech/ai/claude/03-claude-code]] - Claude Code 기본 사용 맥락
- [[study/tech/ai/claude/08-subagents]] - subagent isolation과 역할 분리
- [[study/tech/ai/codex]] - OpenAI Codex와 coding agent 비교
- [[study/tech/ai/multi-agent-platforms]] - multi-agent orchestration 관점

---

**생성일**: 2026-06-09  
**상태**: 학습 중
