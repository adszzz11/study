---
date: 2026-09-09
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem — 무엇을 표준화하고 무엇을 적응시킬까

[학습 진입점](README.md) · 이전: [Overview](01-overview.md) · 다음: [References](03-references.md)

## 두 설계 방향의 비교

| 기준 | Standardized Harness | Provider-adaptive Harness |
|---|---|---|
| 중심 질문 | 어떤 모델이든 어떤 계약을 지켜야 하는가? | 이 API·모델에서 계약을 잘 수행하려면 무엇을 바꿔야 하는가? |
| 주요 대상 | task·권한·상태·예산·검증·로그 | context·tool 설명·reasoning 연속성·실행 전략 |
| 장점 | 일관된 운영과 과제 비교 | 모델별 실패 패턴과 native 기능 반영 |
| 비용 | 지나친 공통화 시 기능·상태 손실 | profile 유지와 regression 평가 증가 |
| 대표 실패 | 모든 history를 문자열로 합쳐 API 상태 유실 | 모델 변경 후에도 과거 workaround 유지 |
| 결합 방식 | core의 불변 조건 제공 | 그 조건 안에서 검증된 profile 적용 |

이 표는 제품 순위가 아니라 설계 선택을 위한 분석이다. provider가 하나여도 모델·API 버전이 달라지면 적응이 필요할 수 있다.

## 인접 개념과 경계

| 개념 | 담당하는 일 | 혼동하면 안 되는 점 |
|---|---|---|
| Prompt template | 모델에 전달할 지시 구성 | 상태·복구·실행 전체를 관리하지 않음 |
| API adapter / gateway | 호출 형식·인증·응답·오류 연결 | 연결 성공만으로 행동 최적화가 증명되지 않음 |
| Agent Harness | 일을 수행하는 loop와 상태·검증 관리 | 모델 자체나 채점기와 다름 |
| MCP | 외부 tools·resources 등을 연결하는 protocol | agent loop·memory·compaction·recovery 전체 표준이 아님 |
| Evaluation Harness | 실행 결과를 채점·비교 | 일을 수행하는 Agent Harness와 역할이 다름 |

SWE-bench는 Docker 환경에서 patch와 테스트 결과를 평가하는 사례다. Agent Harness가 만든 patch를 Evaluation Harness가 채점할 수 있다. MCP는 그 실행 중 사용하는 외부 도구의 연결 계층이 될 수 있다. [SWE-bench Quickstart](https://www.swebench.com/SWE-bench/guides/quickstart/) · [MCP Specification](https://modelcontextprotocol.io/specification/2025-11-25)

## Deep Agents: 두 Profile의 차이

| 구분 | ProviderProfile | HarnessProfile |
|---|---|---|
| 관심사 | 모델 객체를 어떻게 생성할까? | 생성된 모델을 어떻게 운용할까? |
| 설정 예 | 생성 인자·credential 검사·runtime-derived kwargs | system prompt·tool 설명 및 노출·middleware·기본 subagent |
| 바뀌는 층 | 연결 및 모델 초기화 | 실행 행동 |

`base_url`과 API key 교체는 provider 연결에 해당한다. 파일 읽기 오해를 줄이는 tool 설명이나 middleware는 harness 적응이다. Profiles는 조사 기준일 문서에서 **Beta**이며, 실습 시 package·SDK 버전을 고정하고 실제 설정 API를 확인한다. [Profiles](https://docs.langchain.com/oss/python/deepagents/profiles)

## Provider보다 더 세밀한 API 경계

| Provider / API | 보존해야 하는 차이 | 구현 시 점검 |
|---|---|---|
| OpenAI Responses | `previous_response_id` 또는 response items로 이어지는 상태, model family 호환 제약 | 텍스트 외 items를 유지하고 모델 변경의 호환성을 확인 |
| Claude Messages | tool-use turn의 `thinking`, `redacted_thinking` blocks | 필요한 blocks를 원형대로 되돌려주고 문자열로 평탄화하지 않음 |
| Gemini `generateContent` | Gemini 3 function calling의 `thought_signature` | signature와 content part 위치·순서를 보존; 누락 시 400 가능 |
| Gemini Interactions | 별도 `thought` steps 구조 | `generateContent` adapter의 schema를 그대로 재사용하지 않음 |

각 행의 공식 근거는 아래 Sources의 provider 문서다. **`provider + API + model/version + capabilities`로 profile을 선택하자**는 것은 위 차이에서 도출한 설계 제안이다. Deep Agents의 공식 등록 키 자체가 이 모든 필드를 지원한다는 뜻은 아니다.

## 선택 가이드

- 여러 모델을 비교하려면 먼저 동일 과제·권한·예산·채점기를 고정한다.
- 연결 오류는 adapter에서, 반복 행동 오류는 harness profile에서 원인을 찾는다.
- provider failover는 확인된 작업 사실과 산출물로 context를 재구성한다. opaque reasoning 상태의 직접 이전은 가정하지 않는다.
- 장기 작업의 checkpoint 구조와 프로파일 평가 방법은 [Deep dive](04-learning/02-deep-dive.md)에서 다룬다.

## Sources

- [Deep Agents Profiles](https://docs.langchain.com/oss/python/deepagents/profiles)
- [MCP Specification — 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25)
- [SWE-bench Quickstart](https://www.swebench.com/SWE-bench/guides/quickstart/)
- [OpenAI Reasoning](https://developers.openai.com/api/docs/guides/reasoning)
- [Claude Thinking](https://platform.claude.com/docs/en/build-with-claude/thinking)
- [Gemini Generate Content signatures](https://ai.google.dev/gemini-api/docs/generate-content/thought-signatures)
- [Gemini Interactions thinking](https://ai.google.dev/gemini-api/docs/thought-signatures)
