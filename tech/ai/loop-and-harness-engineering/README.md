---
date: 2026-06-23
tags: [tech, ai, agent, loop-engineering, harness-engineering]
status: learning
type: tech-tool-study
---

# Loop Engineering & Harness Engineering

> **한 줄 정의**: Loop engineering은 AI agent가 `observe -> act -> verify -> learn/continue`를 반복하게 설계하는 일이고, harness engineering은 그 loop가 안전하고 재현 가능하게 돌도록 `context, tools, memory, permissions, evals, traces` 같은 실행 기반을 설계하는 일이다.

## 개요

2025-2026년 agentic coding 도구는 `prompt 한 번 -> 답변`에서 `목표 부여 -> agent가 파일 읽기, 명령 실행, 테스트, 수정, 재시도`로 이동했다. 그래서 성능은 prompt 문장만이 아니라 **model-harness-environment system** 전체에서 나온다.

한국식으로 말하면 junior 개발자에게 "버그 고쳐줘"라고 던지는 것보다, 이슈 설명서·코드베이스 안내·실행 권한·검증 기준·보고 양식·실패 재시도 규칙을 갖춘 업무 시스템을 만들어 주는 쪽에 가깝다. 이 업무 시스템이 **agent harness**, 반복 업무 방식이 **agent loop**다.

---

## Quick Start

```text
Goal
 -> Plan
 -> Retrieve context
 -> Use tools
 -> Observe results
 -> Diagnose failure
 -> Patch/change
 -> Verify
 -> Decide: stop or continue
```

```bash
# repo-level harness의 최소 시작점
touch AGENTS.md

# AGENTS.md에 적을 것
# - setup command
# - test command
# - code style
# - PR/report rule
# - forbidden action
```

---

## 학습 경로

### 1단계: 문제의식 이해

- [ ] [[01-overview|개요]] 읽기 - 왜 prompt engineering만으로는 부족한가
- [ ] `agent loop`, `agent harness`, `verification protocol` 용어 구분
- [ ] junior 개발자 업무 시스템 비유로 loop/harness를 설명해 보기

### 2단계: 생태계 비교

- [ ] [[02-ecosystem|생태계]] 파악 - Codex, Claude Code, LangGraph, Agents SDK, MCP 비교
- [ ] [[study/tech/ai/model-context-protocol-mcp]]와 harness의 관계 이해
- [ ] [[study/tech/ai/lazy-codex]]처럼 검증 중심 harness가 왜 필요한지 정리

### 3단계: 근거 자료 확인

- [ ] [[03-references|참고자료]]에서 AI Harness Engineering 논문과 Agentic Harness Engineering 논문 확인
- [ ] Claude Code의 `/loop`, Routines, hooks, subagents 문서 훑기
- [ ] OpenAI Cookbook의 trace/eval 기반 agent improvement loop 읽기

### 4단계: 실습

- [ ] [[04-learning/01-getting-started|시작하기]] - 작은 repo용 `AGENTS.md`와 검증 루프 만들기
- [ ] [[04-learning/02-deep-dive|심화]] - traces, eval gate, failure attribution, permission boundary 설계

### 5단계: 적용

- [ ] [[05-projects|실전 프로젝트]] - 코딩 agent harness, 운영 감시 loop, PR eval gate 만들기
- [ ] [[cheatsheet|치트시트]] - 용어·구성요소·설계 체크리스트 빠른 참조

---

## 파일 구조

```text
loop-engineering-harness-engineering에-대해/
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
| 개요 | [[01-overview]] | What/Why, 특징, 기본 아키텍처 |
| 생태계 | [[02-ecosystem]] | 관련 도구·프레임워크 비교 |
| 참고자료 | [[03-references]] | 논문, 공식 문서, benchmark |
| 시작하기 | [[04-learning/01-getting-started]] | repo harness 최소 구성 |
| 심화 | [[04-learning/02-deep-dive]] | trace/eval/permission 설계 |
| 프로젝트 | [[05-projects]] | 실전 적용 아이디어 |
| 치트시트 | [[cheatsheet]] | 핵심 용어와 체크리스트 |

## 관련 노트

- [[study/tech/ai/lazy-codex]] - 검증 루프와 agent harness 사례
- [[study/tech/ai/model-context-protocol-mcp]] - tool/context 연결 표준
- [[study/tech/ai/codex]] - coding agent workflow
- [[study/tech/ai/agent-orchestration/cli-agents]] - CLI agent orchestration 맥락

---

**생성일**: 2026-06-23  
**상태**: 학습 중
