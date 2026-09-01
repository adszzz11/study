---
date: 2026-09-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Prime Agent

> **한 줄 정의**: Prime Agent는 persistent Python REPL, recursive subagents, durable session, self-refining `Continual Harness`를 결합한 MIT-licensed 오픈소스 coding/research agent harness다.

## Overview

Prime Agent는 긴 작업의 대화·로그·tool output을 매번 LLM의 active context에 넣는 대신, persistent computation과 disk-backed state에 보관한다. 모델은 Python으로 필요한 정보만 filtering·aggregation·verification하고 명시적으로 출력한다. 핵심 목표는 context window를 무작정 키우는 것이 아니라 `context pollution/context rot`, compaction 손실, 장기 작업 중단을 줄이는 것이다.

핵심 구성은 다음과 같다.

- **RLM-native persistent REPL**: session마다 독립적인 IPython kernel과 Python object state 유지
- **Recursive subagents**: `rlm()`을 function처럼 호출해 runtime에 delegation topology 구성
- **Continual Harness**: `/refine`으로 prompt notes, memories, skills, subagent specifications 개선
- **Durable sessions**: daemon이 detach/reattach, crash recovery, goal, heartbeat, history를 관리
- **Provider-neutral layer**: subscription, API-key provider, OpenAI-compatible local endpoint 지원

> [!warning] 보안 경계
> worker/kernel 분리는 lifecycle과 recovery를 위한 구조이며 security sandbox가 아니다. Model-generated Python과 shell command는 현재 사용자 권한으로 실행된다.

## Learning Path

- [ ] [[01-overview|Overview]] — What/Why, L0–L3 정보 계층, 핵심 특징 이해
- [ ] [[02-ecosystem|Ecosystem]] — Claude Code, Codex, Pi-mono, 고정 orchestration framework와 비교
- [ ] [[03-references|References]] — 공식 저장소, 논문, runtime·provider 문서의 신뢰 범위 확인
- [ ] [[04-learning/01-getting-started|Getting started]] — 격리 환경, provider, persistent REPL, session 복구 실습
- [ ] [[04-learning/02-deep-dive|Deep dive]] — recursive delegation, `/refine`, budget와 verifier 설계
- [ ] [[05-projects|Projects]] — 안전한 장기 coding/research 프로젝트로 적용
- [ ] [[cheatsheet|Cheatsheet]] — 명령, 개념, 운영·보안 체크리스트 빠른 참조

## When To Use

- 대형 log, dataset, repository를 반복적으로 filtering·aggregation해야 하는 장기 작업
- context compaction이나 client 종료 뒤에도 objective와 computation state를 이어가야 할 때
- 모델이 작업 중 필요에 따라 recursive subagent 구조를 구성해야 할 때
- prompt·memory·skill·role을 실행 trajectory에서 versioned state로 개선하려는 실험
- 여러 model provider 또는 local OpenAI-compatible endpoint를 같은 harness에서 비교할 때
- root와 descendant의 token, cost, time을 합산해 추적해야 할 때

## When Not To Use

- 신뢰할 수 없는 code를 현재 사용자 권한으로 실행할 수 없는 production 환경
- 한두 번의 단순 질의처럼 persistent state와 delegation의 운영 비용이 이득보다 큰 작업
- 고정된 승인 절차와 deterministic DAG만 허용되는 workflow
- 독립적으로 재현된 benchmark가 필수인 도입 의사결정
- 외부 verifier, immutable acceptance test, credential 격리 없이 `/refine`을 자동 적용하려는 경우
- model weights의 online learning이 필요한 경우: Continual Harness는 supplemental state를 바꾸며 weights를 학습하지 않는다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/agent-orchestration/README|Agent Orchestration]] — durable session과 recursive delegation 비교 맥락
- [[tech/ai/codex/README|Codex]] — coding agent workflow와 provider subscription 비교
- [[tech/ai/autoresearch-study/README|Autoresearch Study]] — 장기 자율 연구와 immutable evaluation 설계

## Sources

- [Prime Agent 공식 저장소](https://github.com/PrimeIntellect-ai/prime-agent)
- [Prime Agent 논문](https://arxiv.org/html/2608.23552)
- [공식 출시 보고서](https://www.primeintellect.ai/blog/prime-agent)
- [Architecture documentation index](https://github.com/PrimeIntellect-ai/prime-agent/blob/main/packages/coding-agent/docs/index.md)
- [RLM Runtime Architecture](https://github.com/PrimeIntellect-ai/prime-agent/blob/main/packages/coding-agent/docs/rlm-runtime.md)
- [공식 Quickstart](https://github.com/PrimeIntellect-ai/prime-agent/blob/main/packages/coding-agent/docs/quickstart.md)
- [Continual Harness 논문](https://arxiv.org/abs/2605.09998)

