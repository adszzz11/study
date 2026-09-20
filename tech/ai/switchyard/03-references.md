---
date: 2026-08-15
tags: [tech]
type: tech-tool-study
status: draft
---

# Switchyard References

> [[02-ecosystem|이전: Ecosystem]] · [[README|목차]] · [[04-learning/01-getting-started|다음: Getting Started]]

## Reading Order

1. [v0.2.0 Release](https://github.com/NVIDIA-NeMo/Switchyard/releases/tag/v0.2.0)에서 지원 범위와 known issues를 확인한다.
2. [Getting Started](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/docs/getting_started.md)로 native server 실행 흐름을 익힌다.
3. [Core Concepts](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/docs/core_concepts.md)에서 `llm_clients` → `targets` → `routes` 관계를 이해한다.
4. routing 목적에 따라 classifier 또는 stage router 문서를 읽는다.
5. protocol fidelity나 embedding이 중요하면 protocol crate와 `libsy` README로 내려간다.

## Official References

| 자료 | 확인할 내용 |
|---|---|
| [GitHub repository](https://github.com/NVIDIA-NeMo/Switchyard) | source, examples, issues, 최신 branch 상태 |
| [v0.2.0 Release](https://github.com/NVIDIA-NeMo/Switchyard/releases/tag/v0.2.0) | 2026-08-10 release, pre-alpha 고지, known issues |
| [PyPI 0.2.0](https://pypi.org/project/nemo-switchyard/0.2.0/) | package version, Python requirement, Alpha classifier |
| [Changelog](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/CHANGELOG.md) | native Rust 전환과 Unreleased breaking changes |
| [Getting Started](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/docs/getting_started.md) | 설치, server, launcher, 첫 요청 |
| [Core Concepts](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/docs/core_concepts.md) | client/target/route configuration model |
| [LLM Classifier Routing](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/docs/routing_algorithms/llm_classifier_routing.md) | capability, escalation, custom verdict, fallback |
| [Stage-Router Routing](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/docs/routing_algorithms/stage_router_routing.md) | trajectory signal, picker, confidence threshold |
| [Protocol crate](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/crates/protocol/README.md) | provider-neutral request/response/event types |
| [`libsy` README](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/crates/libsy/README.md) | state machine, `Step::CallModel`, host integration |

## Version Notes

| 항목 | 기준 |
|---|---|
| 조사일 | 2026-08-15 |
| 최신 공개 release | v0.2.0, 2026-08-10 |
| 성숙도 | pre-alpha / PyPI Alpha |
| 권장 신규 경로 | native TOML + `switchyard-server` |
| 피해야 할 legacy 자료 | `switchyard serve`, YAML route bundle, FastAPI endpoint, Python chain 중심 예제 |

`main` 문서는 다음 release를 향해 바뀔 수 있다. 재현 가능한 실습에는 release tag의 문서와 source를 우선하고, `main`은 차기 변경점 확인용으로 분리한다.

## Evaluation Questions

- tool call/result와 streaming event가 client가 기대하는 순서와 shape로 보존되는가?
- Responses reasoning/final-answer item과 Anthropic error envelope가 손실 없이 변환되는가?
- classifier parse failure와 timeout에서 어느 target으로 fallback하는가?
- session affinity key의 범위와 만료 정책은 무엇인가?
- retry와 context overflow fallback이 최대 몇 번의 upstream call을 만들 수 있는가?
- response `model`, routing header, span, JSONL log의 model attribution이 일치하는가?
- client disconnect 뒤 남는 작업의 비용을 어떻게 제한할 것인가?

## Sources

- [NVIDIA NeMo Switchyard documentation index](https://github.com/NVIDIA-NeMo/Switchyard/tree/main/docs)
- [NVIDIA NeMo Switchyard releases](https://github.com/NVIDIA-NeMo/Switchyard/releases)
- [nemo-switchyard on PyPI](https://pypi.org/project/nemo-switchyard/)

