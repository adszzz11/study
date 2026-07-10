---
date: 2026-07-11
tags:
  - tech
  - ai
  - codex
  - gpt-5-6
  - agentic-coding
status: learning
type: tech-tool-study
---

# Codex 5.6? GPT-5.6 in Codex - 종합 스터디

> **한 줄 정의**: "Codex 5.6"이라는 별도 제품명이라기보다, 공식 명칭은 **GPT-5.6 model family**이고 이것이 Codex, ChatGPT Work, API에 들어온 최신 frontier reasoning/agentic model 라인업이다.

## 개요

GPT-5.6은 2026년 7월 9일 GA로 공개된 OpenAI의 최신 모델군이다. 핵심은 단순히 "더 똑똑한 모델" 하나가 아니라, **agentic coding**, **long-running knowledge work**, **computer use**, **cybersecurity/science tasks**를 더 적은 token, latency, cost로 처리하는 3-tier model family다.

Codex 관점에서는 모델 선택지가 확장된다. dossier 기준 OpenAI는 GPT-5.6이 Codex와 ChatGPT Work에 바로 제공되며, Codex에서는 Plus 이상 사용자가 `Sol`, `Terra`, `Luna`, `max`, `ultra`를 사용할 수 있다고 설명한다.

## 중요한 정정

- 제품명이 **Codex 5.6**인 것은 아니다.
- 정확히는 **GPT-5.6 model family가 Codex surface에 통합**된 것이다.
- 그래서 학습 초점은 "Codex 앱 자체 변경"보다 **모델 tier, reasoning effort, multi-agent/ultra, Programmatic Tool Calling, Codex cloud workflow**를 이해하는 데 있다.

## 학습 경로

| 순서 | 파일 | 무엇 |
|------|------|------|
| 1 | [[01-overview\|01. Overview]] | What/Why, 핵심 특징, Codex 관점의 의미 |
| 2 | [[02-ecosystem\|02. Ecosystem]] | Claude, Gemini, GitHub Copilot/Agent HQ와 비교 |
| 3 | [[03-references\|03. References]] | 공식 release, system card, API/Codex 문서 |
| 4 | [[04-learning/01-getting-started\|04-1. 시작하기]] | 모델 선택, reasoning effort, Codex CLI/cloud 첫 실습 |
| 5 | [[04-learning/02-deep-dive\|04-2. 심화]] | Programmatic Tool Calling, Multi-agent beta, safety stack |
| 6 | [[05-projects\|05. Projects]] | repo migration, PR review, research agent, security hardening |
| 7 | [[cheatsheet\|cheatsheet]] | tier/effort/surface 빠른 참조 |

## 파일 구조

```text
codex-5-6-나왔는데-이거-분석해서-확인해봐-어떤건지/
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

## 30초 핵심

- **정체**: Codex 5.6이 아니라 GPT-5.6 model family의 Codex 통합.
- **Tier**: `gpt-5.6-sol` flagship, `gpt-5.6-terra` balance, `gpt-5.6-luna` high-volume/low-cost.
- **Reasoning**: `none`, `low`, `medium`, `high`, `xhigh`, `max`; quality-first 작업은 `max`.
- **Codex 확장**: `ultra`는 여러 agent를 병렬 조율하는 Codex 고성능 모드.
- **API 확장**: Programmatic Tool Calling과 Responses API Multi-agent beta가 핵심 패턴.

## 기술스택 요약

GPT-5.6은 Codex에 통합된 최신 OpenAI agentic model family로, Sol/Terra/Luna 3개 tier와 `max/ultra` reasoning/multi-agent 기능이 핵심이다.  
Codex CLI, IDE, ChatGPT desktop/web, Codex cloud에서 사용할 수 있고, API에서는 Responses API와 Programmatic Tool Calling, Multi-agent beta로 유사한 workflow를 구성한다.  
실무 도입 시에는 `AGENTS.md`, test/lint convention, PR review gate, secret/access boundary를 함께 설계해야 한다.  
이 노트에서는 GPT-5.6을 coding model이 아니라 **agentic work runtime의 모델 계층**으로 다룬다.

## 관련 노트

- [[study/tech/ai/lazy-codex]] - Codex agent의 검증 루프와 false completion 대응
- [[study/tech/ai/model-context-protocol-mcp]] - agent tool/resource integration 표준
- [[study/tech/ai/agent-orchestration/cli-agents]] - CLI agent와 multi-agent orchestration 맥락
- [[study/tech/ai/litellm]] - 모델 gateway/routing 관점의 비교

---

**생성일**: 2026-07-11  
**상태**: 학습 중
