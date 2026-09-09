---
date: 2026-09-09
tags: [tech]
type: tech-tool-study
status: draft
---

# 표준 하네스랑 프로바이더 적응형 하네스

> **한 줄 정의**: Standardized Harness는 모델들을 공통 실행 계약으로 운용하는 에이전트 기반이며, Provider-adaptive Harness는 그 기반 위에서 provider·model·API 특성에 맞춰 context, tools, reasoning, 실행 전략을 조정하는 구조다.

## Overview

**공통 코어를 표준화하고, 모델별 차이는 검증된 profile로 분리한다.** 두 용어는 서로 배타적인 공식 규격명이 아니라, 이 노트에서 공통화와 특화를 비교하기 위해 사용하는 설계 용어다.

Agent Harness는 모델 호출과 tool 실행을 반복하며 context, 작업 상태, 종료, 복구, 검증을 관리하는 모델 외부 소프트웨어다. API 연결만 바꾸는 adapter보다 범위가 넓다. Deep Agents의 `ProviderProfile`과 `HarnessProfile` 구분이 구체적인 참고 사례다. [공식 Profiles 문서](https://docs.langchain.com/oss/python/deepagents/profiles)

| 공통으로 유지 | profile로 조정 | 따로 평가 |
|---|---|---|
| 목표·권한·예산·checkpoint·완료 조건 | tool 설명·context 정책·planning 및 verification 전략 | 동일 과제의 성공률·비용·지연·복구율 |

조사 기준일은 **2026-09-09**다. 개발사 실험 결과와 설계 제안을 구분하고, HarnessDev는 **preprint**로 다룬다. 제공 dossier는 Better Harness 링크 중간에서 끝나므로 해당 자료의 URL과 후속 내용을 추정해 채우지 않았다.

## Learning Path

- [ ] [Overview](01-overview.md): Agent Harness의 What/Why와 공통 코어 이해
- [ ] [Ecosystem](02-ecosystem.md): 표준화·적응·API adapter·MCP·Evaluation Harness 비교
- [ ] [References](03-references.md): 공식 문서, 실험 보고, preprint의 근거 수준 구분
- [ ] [Getting started](04-learning/01-getting-started.md): 작은 과제와 baseline으로 static profile 비교
- [ ] [Deep dive](04-learning/02-deep-dive.md): reasoning 상태 보존, failover, ablation 설계
- [ ] [Projects](05-projects.md): 페이지 읽기, 작업 재개, profile regression 실습
- [ ] [Cheatsheet](cheatsheet.md): 구현·검토 시 확인할 항목 빠르게 참조

## When To Use

- 같은 작업을 여러 provider·model에서 실행하면서 동일한 완료 기준으로 비교할 때
- 장시간 작업의 context 손실, 조기 종료, tool 결과 오해가 반복될 때
- 모델 교체 후 기존 workaround가 여전히 필요한지 검증할 때
- API 연결에는 성공했지만 실제 작업 성공률이 provider마다 달라질 때

## When Not To Use

- 한 번의 모델 호출로 끝나는 작업이라면 전체 agent loop부터 구축할 필요가 없다.
- 도구 연결만 필요하다면 먼저 해당 API나 MCP integration 범위를 확인한다.
- 실패 사례와 평가 과제가 없다면 자동 profile 생성·진화보다 baseline 기록부터 시작한다.
- 모든 모델에 동일한 JSON을 보내거나 provider 간 opaque reasoning 상태를 그대로 옮기려는 목적에는 맞지 않는다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol]] — 도구 연결 protocol과 실행 하네스의 경계
- [[tech/ai/litellm/README|LiteLLM]] — provider 연결·routing과 행동 적응의 차이를 함께 학습

## Sources

- [Deep Agents Overview](https://docs.langchain.com/oss/python/deepagents/overview)
- [Deep Agents Profiles — Beta](https://docs.langchain.com/oss/python/deepagents/profiles)
- [Anthropic: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [LangChain: Improving Deep Agents with harness engineering](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering)
- [HarnessDev — preprint](https://arxiv.org/abs/2609.01437)
- 전체 출처와 읽기 순서: [03-references.md](03-references.md)
