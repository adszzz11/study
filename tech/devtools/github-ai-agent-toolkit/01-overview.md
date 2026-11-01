---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# GitHub AI Agent 도구군 개요

[[tech/devtools/github-ai-agent-toolkit/README|README]]의 도구군은 모델을 바꾸기보다 agent의 작업 절차와 실행 환경을 확장한다.

## What

| 계층 | 도구 | 역할 |
|---|---|---|
| Agent skill | Ponytail, Taste Skill, Impeccable, security-audit-skill | 지침과 검증 loop 배포 |
| Agent harness | ECC | rules, hooks, MCP convention, skills 이식 |
| Access/research | Agent-Reach | read-only channel과 fallback backend 통합 |
| Serving/routing | FreeLLMAPI, DeepInfer | OpenAI-compatible gateway와 inference runtime |
| Production | HyperFrames, VoiceStudio, Ghidra | video·voice·reverse engineering 작업 |

## Why

매 세션마다 prompt로 품질 기준을 설명하면 재사용과 검증이 어렵다. `SKILL.md`와 hook은 일관된 절차를 만들지만, 실행 권한도 함께 넓힌다. 따라서 생산성 평가에는 결과물뿐 아니라 permission, install ownership, rollback 가능성도 포함해야 한다.

## 핵심 특징

- **Ponytail**: YAGNI를 중심에 두고 가장 작은 patch를 유도한다.
- **Taste Skill / Impeccable**: visual direction, render inspection, design system·accessibility 기준을 workflow에 넣는다.
- **ECC**: 여러 harness로 규칙을 옮기지만, 큰 설치 범위와 hook supply chain을 검토해야 한다.
- **Agent-Reach**: 일부 channel이 별도 browser profile의 로그인 session을 재사용한다. secondary account가 적합하다.
- **FreeLLMAPI**: `/v1` gateway, provider fallback/routing, encrypted SQLite credential storage를 제공한다.
- **DeepInfer**: 대규모 DeepSeek serving에서 prefill/decode 성능을 겨냥한다.

다음: [[tech/devtools/github-ai-agent-toolkit/02-ecosystem|Ecosystem]]

## Sources

- https://github.com/DietrichGebert/ponytail
- https://github.com/Panniantong/Agent-Reach/blob/main/docs/README_en.md
- https://github.com/deepseek-ai/DeepInfer
