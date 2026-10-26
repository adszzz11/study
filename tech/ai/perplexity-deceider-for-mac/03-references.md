---
date: 2026-10-27
tags: [tech]
type: tech-tool-study
status: draft
---

# References

## Perplexity primary sources

1. [Decider for Mac 공식 문서](https://docs.perplexity.ai/docs/decisions/decider-for-mac) — 설치, local endpoint, local use case, 제한 사항.
2. [Decisions API Quickstart](https://docs.perplexity.ai/docs/decisions/quickstart) — question type, request/response, 모델 선택과 API 사용.
3. [Decisions API endpoint reference](https://docs.perplexity.ai/api-reference/decisions-post) — `POST /v1/decisions` contract.
4. [Changelog: Decisions API 및 local-device 지원](https://www.perplexity.ai/en-GB/changelog/ultrafast-computer-models-decisions-api-and-connector-controls) — 출시 배경과 제품 변경 이력.
5. [Flash GGUF model card](https://huggingface.co/perplexity-ai/pplx-decider-flash-gguf-v1.2) — local artifact와 runtime 관련 정보.
6. [27B Decider model card](https://huggingface.co/perplexity-ai/pplx-decider-v1.2) — hosted model과 model family 맥락.

## Structured Output 비교 자료

1. [OpenAI Structured model outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
2. [Anthropic Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
3. [Google Gemini Structured Outputs](https://ai.google.dev/gemini-api/docs/structured-output)

## 읽는 순서

공식 Mac 문서에서 설치와 local request를 확인하고, Quickstart/endpoint reference로 `state`·`questions` contract를 읽는다. 그 뒤 Flash와 27B model card로 runtime/배포 차이를 확인하고, 마지막에 Structured Outputs 문서와 비교해 문제에 맞는 API 계약을 선택한다.

## Sources

- https://docs.perplexity.ai/docs/decisions/decider-for-mac
- https://docs.perplexity.ai/docs/decisions/quickstart
- https://docs.perplexity.ai/api-reference/decisions-post
