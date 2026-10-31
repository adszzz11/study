---
date: 2026-06-24
tags:
  - tech
  - ai
  - hankweave
  - agent-runtime
  - repairable-agents
status: learning
type: tech-tool-study
---

# Hankweave

> **한 줄 정의**: Hankweave는 Southbridge.AI가 공개한 "repairable agents"용 runtime으로, 긴 시간 실행되는 AI agent 작업을 `hank.json` 기반 declarative workflow, codon, checkpoint, sentinel, harness abstraction으로 재현·디버그·수리 가능하게 만드는 도구다.

## 개요

Hankweave는 Claude Code, Codex, Gemini CLI, Pi, OpenCode 같은 coding agent harness를 대체하는 agent가 아니라, 그런 harness를 실행·격리·관찰·복구하는 **headless-first long-horizon agent runtime**이다.

핵심 문제의식은 long-horizon agent가 수백~수천 tool call, 수 시간~수일 실행으로 커질수록 병목이 "모델 성능"보다 **인간이 agent behavior를 이해하고 고칠 수 있는가**로 옮겨간다는 점이다. Southbridge는 이를 brownfield AI engineering 문제로 본다.

```text
hank.json
  -> hank
      -> codon sequence
          -> harness shim
              -> Claude Code / Codex / Gemini CLI / Pi / OpenCode
      -> checkpoint, sentinel, event journal, budget, rollback
```

## 기술스택 요약

- Hankweave는 TypeScript/Bun 기반의 headless AI agent runtime이며, `hank.json` declarative config로 codon sequence를 실행한다.
- Claude Code, Codex, Gemini CLI, Pi, OpenCode 같은 harness를 shim으로 호출하고, runtime은 checkpoint, rollback, WebSocket event stream, sentinel, budget, preflight validation을 담당한다.
- 데이터는 read-only로 mount하고 작업은 isolated execution directory에서 수행해 재현성과 복구성을 높인다.
- 2026-06-24 기준 공개 `release/alpha` package metadata는 `hankweave` `0.6.2`, Node `>=20`, Apache-2.0 GitHub repository를 표시한다.

---

## 학습 경로

### 1단계: 문제의식 이해

- [ ] [[01-overview|개요]]에서 repairable agent, brownfield AI engineering, context firewalling 이해
- [ ] Hank, Codon, Sentinel, Harness, Checkpoint 용어 정리
- [ ] [[study/tech/ai/agent-orchestration]] 맥락에서 "agent framework"와 "agent runtime" 차이 구분

### 2단계: 생태계 비교

- [ ] [[02-ecosystem|생태계]]에서 LangGraph, AutoGen, CrewAI, Temporal, bash/CI와 비교
- [ ] Hankweave가 graph app framework보다 harness orchestration/runtime에 가까운 이유 정리
- [ ] [[study/tech/ai/lazy-codex]]와 검증·복구 관점 비교

### 3단계: 공식 자료 확인

- [ ] [[03-references|참고자료]]에서 공식 소개, docs, concepts, GitHub source 확인
- [ ] `package.json`의 runtime 요구사항, license, version 확인
- [ ] CCEPL-driven development 글과 Hankweave의 연결점 읽기

### 4단계: 실습

- [ ] [[04-learning/01-getting-started|시작하기]] - starter project, validation, TUI/headless 실행
- [ ] [[04-learning/02-deep-dive|심화]] - codon boundary, checkpoint, sentinel, Docker/CI 패턴 실험

### 5단계: 적용 설계

- [ ] [[05-projects|실전 프로젝트]]에서 research dossier, data codebook, migration assistant 설계
- [ ] [[cheatsheet|치트시트]]로 config key, guardrail, 운영 체크리스트 빠르게 복습

---

## 파일 구조

```text
https-www-southbridge-ai-hankweave/
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
| 개요 | [[01-overview]] | What/Why, 핵심 특징, 아키텍처 |
| 생태계 | [[02-ecosystem]] | LangGraph, AutoGen, CrewAI, Temporal 등과 비교 |
| 참고자료 | [[03-references]] | 공식 문서, source, 관련 문서 |
| 시작하기 | [[04-learning/01-getting-started]] | 설치, init, validate, run |
| 심화 | [[04-learning/02-deep-dive]] | context firewall, checkpoint, sentinel, CI |
| 프로젝트 | [[05-projects]] | 적용 아이디어와 설계 패턴 |
| 치트시트 | [[cheatsheet]] | 명령, 개념, config 빠른 참조 |

## 관련 노트

- [[study/tech/ai/agent-orchestration]] - agent runtime/orchestration 맥락
- [[study/tech/ai/lazy-codex]] - coding agent harness와 검증 루프
- [[study/tech/ai/model-context-protocol-mcp]] - agent tool/resource integration 계층
- [[study/tech/ai/multi-agent-platforms]] - multi-agent framework 생태계

---

**생성일**: 2026-06-24  
**상태**: 학습 중
