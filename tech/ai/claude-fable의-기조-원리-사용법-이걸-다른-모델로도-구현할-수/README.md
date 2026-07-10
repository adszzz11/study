---
date: 2026-07-09
tags:
  - tech
  - ai
  - claude
  - claude-code
  - fable
  - agentic-ai
  - codex
  - gemini
status: published
type: tech-tool-study
---

# Claude Fable 5 — 기조·원리·사용법·재현 알고리즘 (tool-study)

> **한 줄**: Claude Fable 5는 Anthropic의 5세대 frontier model로, Claude Code 같은 agent harness에서 장시간 agentic coding과 knowledge work를 수행하도록 설계된 고성능 모델이다.

## 핵심 질문

- Claude Fable 5의 기조는 무엇인가? → **long-horizon autonomous work**
- 어떤 원리로 굴러가는가? → **Constitutional AI / RLAIF**, tool use, MCP, self-verification, context management
- 어떻게 효율적으로 쓰는가? → Claude에는 복잡한 설계·장기 작업, Codex에는 scoped implementation, Gemini에는 긴 문서·검색·멀티모달 검증
- 이걸 다른 모델로도 구현할 수 있는가? → Planner-Executor-Reviewer, ReAct, Self-Refine, Tree/Graph of Thoughts, parallel sampling, RAG+MCP, safety gate로 재현 가능

## 학습 경로

| 순서 | 파일 | 무엇 |
|------|------|------|
| 1 | [[claude-fable의-기조-원리-사용법-이걸-다른-모델로도-구현할-수/01-overview\|01. Overview]] | Fable 5의 What/Why/핵심 특징 |
| 2 | [[claude-fable의-기조-원리-사용법-이걸-다른-모델로도-구현할-수/02-ecosystem\|02. Ecosystem]] | Claude Fable/Sonnet, Codex, Gemini, Cursor/Copilot/Devin/Jules 비교 |
| 3 | [[claude-fable의-기조-원리-사용법-이걸-다른-모델로도-구현할-수/03-references\|03. References]] | 공식 문서·출처 |
| 4 | [[claude-fable의-기조-원리-사용법-이걸-다른-모델로도-구현할-수/04-learning/01-getting-started\|04-1. Getting Started]] | Claude Code 프로젝트 메모리와 기본 루프 |
| 5 | [[claude-fable의-기조-원리-사용법-이걸-다른-모델로도-구현할-수/04-learning/02-deep-dive\|04-2. Deep Dive]] | 다른 모델로 구현 가능한 agent algorithm |
| 6 | [[claude-fable의-기조-원리-사용법-이걸-다른-모델로도-구현할-수/05-projects\|05. Projects]] | Claude + Codex + Gemini 실전 파이프라인 |
| 7 | [[claude-fable의-기조-원리-사용법-이걸-다른-모델로도-구현할-수/cheatsheet\|cheatsheet]] | 명령·프롬프트·역할 분배 빠른 참조 |

## 파일 구조

```text
claude-fable의-기조-원리-사용법-이걸-다른-모델로도-구현할-수/
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

- **Fable 5의 기조**: 단발 답변보다 며칠 단위의 계획, 위임, tool use, 검증, 반복을 견디는 autonomous work.
- **Claude를 효율적으로 쓰는 법**: `CLAUDE.md`에 build/test/style/architecture 규칙을 넣고, “탐색 → 계획 → 수정 → 검증 → 반복 → 요약”을 강제한다.
- **다중 모델 운용**: Claude = planner/architect, Codex = implementer/test fixer, Gemini = long-context researcher/reviewer.
- **주의점**: cyber/bio/chem 등 위험 도메인은 safeguard와 fallback routing이 걸릴 수 있다. API에서는 Fallback API 설정을 확인해야 한다.

## 관련 노트

- [[claude]] · [[codex]] · [[model-context-protocol-mcp]] · [[agent-orchestration/README]] · [[lazy-codex/README]] · [[ai-ecosystem/01-overview]]
