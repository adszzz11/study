---
date: 2026-09-09
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet — Harness 설계 빠른 참조

[학습 진입점](README.md) · 상세 절차: [Deep dive](04-learning/02-deep-dive.md)

## 핵심 구분

| 용어 | 기억할 것 |
|---|---|
| Standardized Harness | task·권한·상태·예산·검증의 공통 계약 |
| Provider-adaptive Harness | 모델·API 특성에 맞춘 실행 행동 조정 |
| API adapter | 호출과 상태의 protocol 변환·보존 |
| ProviderProfile | Deep Agents의 모델 생성 설정 |
| HarnessProfile | Deep Agents의 prompt·tool·middleware 등 행동 설정 |
| MCP | 외부 tools·resources 연결 protocol |
| Evaluation Harness | 결과를 채점하는 시스템 |

앞의 두 용어는 이 노트의 설계 구분이며 공식 규격명이 아니다. Deep Agents의 profile 구분은 [공식 문서](https://docs.langchain.com/oss/python/deepagents/profiles)를 참고한다.

## 구현 원칙

```text
Common contract + validated profile + lossless API adapter
Selection: provider + API + model/version + capabilities
Completion: candidate -> verifier -> pass or bounded repair
Failover: verified facts + artifacts + pending work + remaining budget
```

위 식은 설계 제안이다. `base_url` 변경만으로 행동 적응이 끝나지 않는다. 공통 event schema가 원본 provider payload를 대체해서도 안 된다.

## 상태 보존

| API | 보존 항목 | 피할 실수 |
|---|---|---|
| OpenAI Responses | response 연결 또는 필요한 output items | 텍스트만 저장, model family 호환성 미확인 |
| Claude Messages | tool-use turn의 thinking/redacted blocks | block 임의 수정·삭제 |
| Gemini `generateContent` | `thought_signature`, part 순서 | signature 누락·위치 변경 |
| Gemini Interactions | API 고유의 `thought` steps | 다른 Gemini API와 schema 혼용 |

적용 조건은 아래 공식 API 문서를 확인한다. Opaque reasoning 상태는 provider 간 이식 가능한 작업 요약이 아니다.

## 실험 전에

- [ ] task·tool 권한·예산·verifier 고정
- [ ] model/API/SDK/harness/profile 버전 기록
- [ ] baseline 확보 및 개발 과제·holdout 분리
- [ ] 같은 모델에서 변경 하나씩 비교
- [ ] 성공률뿐 아니라 tool 호출·비용·지연 측정
- [ ] 모델 교체 시 profile 제거 실험과 regression 수행
- [ ] simulation·자체 측정·개발사 보고를 구분

## 숫자 해석

| 보고 수치 | 의미 | 의미하지 않는 것 |
|---|---|---|
| 52.8% → 66.5% | LangChain의 특정 Terminal-Bench 2.0 실험 | 모든 작업의 성공률 |
| 약 65% 감소 | Deep Agents v0.7 base input tokens | 전체 서비스 비용 절감률 |
| 0/3 → 3/3; 94/127 → 96/127 | NVIDIA의 읽기 테스트 및 전체 평가 평균 | 모든 모델·파일에서의 성공 보장 |

HarnessDev는 preprint다. 실험 수치를 재현한 것으로 보고하지 않는다. 상세 범위는 [References](03-references.md)에서 확인한다.

## Sources

- [Deep Agents Profiles](https://docs.langchain.com/oss/python/deepagents/profiles)
- [MCP Specification](https://modelcontextprotocol.io/specification/2025-11-25)
- [SWE-bench Quickstart](https://www.swebench.com/SWE-bench/guides/quickstart/)
- [OpenAI Reasoning](https://developers.openai.com/api/docs/guides/reasoning)
- [Claude Thinking](https://platform.claude.com/docs/en/build-with-claude/thinking)
- [Gemini Generate Content signatures](https://ai.google.dev/gemini-api/docs/generate-content/thought-signatures)
- [Gemini Interactions thinking](https://ai.google.dev/gemini-api/docs/thought-signatures)
- [LangChain: Harness engineering](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering)
- [Deep Agents v0.7](https://www.langchain.com/blog/deep-agents-v0-7)
- [NVIDIA Harness Profile](https://developer.nvidia.com/blog/?p=119638)
- [HarnessDev — preprint](https://arxiv.org/abs/2609.01437)
