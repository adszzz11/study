---
date: 2026-09-09
tags: [tech]
type: tech-tool-study
status: draft
---

# References — 근거의 종류와 읽기 순서

[학습 진입점](README.md) · 다음: [Getting started](04-learning/01-getting-started.md)

## 조사 범위

조사 기준일: **2026-09-09**. 제공 dossier를 바탕으로 공식 문서·개발사 기술 글·공개 연구를 연결했다. API 문서는 갱신될 수 있으므로 구현할 때 SDK·API·모델 버전과 확인일을 함께 기록한다.

| 근거 종류 | 무엇을 뒷받침하는가? | 읽을 때의 주의점 |
|---|---|---|
| 공식 API·protocol 문서 | 필드·상태 보존·설정 계약 | 모든 모델·API에 동일하게 적용된다고 확대하지 않음 |
| 개발사 기술 글 | 특정 환경의 구현 경험과 실험 | 자체 보고 수치를 범용 성능으로 해석하지 않음 |
| arXiv preprint | 연구 문제와 실험 결과 | 동료심사 확정 연구로 취급하지 않음 |
| 이 노트의 설계 제안 | 공통 코어·적응 계층의 구성 방법 | 공식 표준이나 제품 API와 구분 |

## 권장 읽기 순서

1. Deep Agents Overview로 Agent Harness의 범위를 잡는다.
2. Profiles에서 provider 연결과 실행 행동 설정을 구분한다.
3. 실제 사용할 provider의 reasoning·tool-use 상태 문서를 읽는다.
4. Anthropic 장기 실행 사례와 LangChain 개선 사례를 읽고 실패 원인을 분류한다.
5. NVIDIA 사례로 작은 middleware 변경과 평가 연결을 살펴본다.
6. HarnessDev를 읽으며 모델 간 이전 가능성을 별도 실험 문제로 다룬다.

## Sources

### 공식 문서와 명세

| 출처 | 읽을 내용 |
|---|---|
| [Deep Agents Overview](https://docs.langchain.com/oss/python/deepagents/overview) | tool-calling loop를 넘어서는 harness의 범위 |
| [Deep Agents Profiles — Beta](https://docs.langchain.com/oss/python/deepagents/profiles) | `HarnessProfile`과 `ProviderProfile`의 책임 분리 |
| [OpenAI Reasoning](https://developers.openai.com/api/docs/guides/reasoning) | Responses 상태와 reasoning items의 연속성 |
| [Claude Thinking](https://platform.claude.com/docs/en/build-with-claude/thinking) | tool-use 과정의 thinking blocks 취급 |
| [Gemini Generate Content signatures](https://ai.google.dev/gemini-api/docs/generate-content/thought-signatures) | function calling과 `thought_signature` 보존 |
| [Gemini Interactions thinking](https://ai.google.dev/gemini-api/docs/thought-signatures) | `thought` steps와 API별 표현 차이 |
| [MCP Specification — 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) | 외부 도구·리소스 연결 protocol의 범위 |
| [SWE-bench Quickstart](https://www.swebench.com/SWE-bench/guides/quickstart/) | Docker 기반 patch·테스트 평가 |

### 개발사 기술 글

| 날짜 | 출처 | 근거로 사용할 범위 |
|---|---|---|
| 2025-11-26 | [Anthropic: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | initializer·진행 기록·Git history 활용 |
| 2026-02-17 | [LangChain: Improving Deep Agents with harness engineering](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering) | 모델 고정 상태의 Terminal-Bench 2.0 **52.8% → 66.5%** 보고 |
| 2026-03-24 | [Anthropic: Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) | 모델 변경 후 context reset 제거 사례 |
| 2026-07-29 | [Deep Agents v0.7](https://www.langchain.com/blog/deep-agents-v0-7) | **base input tokens 약 65% 감소** 보고 |
| 2026, dossier에 세부 날짜 없음 | [NVIDIA: Nemotron 3 Ultra Harness Profile](https://developer.nvidia.com/blog/?p=119638) | 파일 읽기 middleware: 해당 테스트 **0/3 → 3/3**, 전체 평가 평균 **94/127 → 96/127** |

66.5%는 범용 성공률이 아니며 65%는 전체 비용 절감률이 아니다. NVIDIA의 작은 읽기 테스트도 일반적 성공 보장으로 확대하지 않는다. 이 노트는 해당 벤치마크를 직접 실행하지 않았다.

### 연구

- [HarnessDev: Can LLMs Create and Evolve Their Own Agent Harness?](https://arxiv.org/abs/2609.01437) — **2026-09-01, preprint**. harness 생성·진화와 모델별 성능 이전을 다룬다. 다른 모델에도 동일한 향상이 나올 것이라고 가정하지 않는 근거로 읽는다.

### 자료 누락

- 제공 dossier의 Better Harness 링크는 `https://w`에서 잘려 있다. 완전한 URL과 원문 내용을 확인하지 못한 항목으로 남기며, 출처를 추정하거나 해당 글에 구체적 주장을 귀속하지 않는다.
