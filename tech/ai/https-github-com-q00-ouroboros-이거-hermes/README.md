---
date: 2026-06-17
tags:
  - tech
  - ai
  - ouroboros
  - hermes
  - coding-agent
  - spec-first
status: learning
type: tech-tool-study
---

# Ouroboros — spec-first Agent OS/workflow engine

> **한 줄 정의**: `Q00/ouroboros`는 Claude Code, Codex CLI, Hermes, Gemini CLI, OpenCode 같은 coding agent 위에 얹어 **vague prompt -> clarified spec -> execution -> evaluation -> evolution** 흐름으로 바꾸는 specification-first Agent OS/workflow engine이다.

## 개요

Ouroboros는 coding agent 자체를 대체하는 도구라기보다, agent가 실행하기 전에 **무엇을 만들지**를 명확하게 만드는 control plane이다.

핵심 문제의식은 단순하다. Claude Code, Codex CLI, Gemini CLI, OpenCode, Hermes 같은 agent는 파일 읽기/수정, command 실행, test, MCP tool 호출을 이미 잘한다. 하지만 요구사항이 흐릿하면 agent는 hidden assumption을 추측으로 채우고, 나중에 architecture, QA, acceptance criteria가 어긋난다.

Ouroboros는 이 문제를 **model capability 부족**보다 **input clarity 부족**으로 본다. 그래서 바로 coding하지 않고 Socratic interview로 모호성을 낮추고, immutable `Seed` spec을 만든 뒤, evaluation gate를 통과하는 방식으로 작업을 진행한다.

## 학습 경로

| 순서 | 파일 | 무엇 |
|---|---|---|
| 1 | [[01-overview]] | What/Why, Seed, ambiguity gate, Agent OS stack |
| 2 | [[02-ecosystem]] | Hermes, Claude Code, Codex CLI, Gemini CLI, OpenCode, Copilot Agent와 비교 |
| 3 | [[03-references]] | 공식 repo, README, architecture, CLI, runtime guide, 관련 agent 문서 |
| 4 | [[04-learning/01-getting-started]] | 설치, setup, 첫 Seed 생성, Hermes runtime 연결 |
| 5 | [[04-learning/02-deep-dive]] | Seed schema, Double Diamond, evaluation pipeline, event sourcing |
| 6 | [[05-projects]] | spec-first workflow를 실제 repo와 Hermes 운영에 붙이는 프로젝트 |
| 7 | [[cheatsheet]] | 핵심 개념, 명령, 비교, 체크리스트 빠른 참조 |

## 파일 구조

```text
https-github-com-q00-ouroboros-이거-hermes/
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

- **coding agent = executor**: repo를 읽고, 파일을 고치고, test를 돌리는 실행자.
- **Ouroboros = requirements/spec/evaluation control plane**: vague prompt를 실행 가능한 contract로 바꾼다.
- **Seed = workflow constitution**: goal, constraints, acceptance criteria, ontology, exit conditions를 담는 immutable spec.
- **Ambiguity gate**: clarity가 부족하면 execution으로 넘어가지 않는다. dossier 기준 threshold는 `Ambiguity <= 0.2`.
- **Evaluation pipeline**: mechanical checks -> semantic verification -> multi-model consensus.
- **Hermes와의 관계**: Hermes가 broader personal/infra agent라면, Ouroboros는 Hermes 같은 runtime 위에서 spec-first coding workflow를 통제하는 layer다.

## 관련 노트

- [[study/tech/ai/model-context-protocol-mcp]] - MCP external tool/context protocol
- [[study/tech/ai/codex]] - Codex CLI terminal coding agent
- [[study/tech/ai/claude]] - Claude Code, skills, hooks, MCP context
- [[study/tech/ai/agent-orchestration/cli-agents]] - terminal agent orchestration 맥락
- [[study/tech/ai/lazy-codex]] - 실행과 검증을 분리하는 agent harness 관점

---

**생성일**: 2026-06-17  
**상태**: 학습 중
