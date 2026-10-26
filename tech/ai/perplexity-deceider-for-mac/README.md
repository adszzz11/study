---
date: 2026-10-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Perplexity Decider for Mac tool study

> **한 줄 정의**: Perplexity Decider for Mac은 Apple silicon Mac에서 `pplx-decider-flash-v1.2`를 로컬 실행하고, text·image를 확률형 분류 결과로 반환하는 무료 menu-bar Decisions API 앱이다.

## Overview

일반 LLM의 설명형 답변을 다시 파싱하는 대신, 명시한 질문에 대해 software가 바로 사용할 typed probability를 받는다. 고객 export·meeting note·내부 screenshot처럼 cloud API로 보내기 어려운 데이터를 `127.0.0.1`에서 분류할 때 유용하다.

- endpoint: `POST http://127.0.0.1:8080/v1/decisions`
- 입력: `state`의 text, JSON, image와 이름 있는 `questions`
- 출력: `noul`(yes 확률), `choice`(option별 확률/선택/confidence), `score`(level별 확률/expected score)
- 환경: Apple silicon M1+, macOS 13+, RAM 16 GB, 여유 디스크 약 6 GB

## Learning Path

- [ ] [01-overview](./01-overview.md)에서 decision model과 local 실행의 경계를 이해한다.
- [ ] [04-learning/01-getting-started](./04-learning/01-getting-started.md)에서 앱을 설치하고 `choice` 요청 하나를 실행한다.
- [ ] `noul`의 보수적 threshold와 human review queue를 설계한다.
- [ ] `score` rubric을 상호 배타적인 level로 작성하고 labeled sample에서 검증한다.
- [ ] [02-ecosystem](./02-ecosystem.md)에서 hosted Decisions API와 Structured Outputs의 차이를 비교한다.
- [ ] [04-learning/02-deep-dive](./04-learning/02-deep-dive.md)로 calibration·migration·runtime 제약을 점검한다.
- [ ] [05-projects](./05-projects.md)의 작은 local automation을 구현한다.

## When To Use

- 민감한 text·JSON·screenshot을 Mac 밖으로 내보내지 않고 분류/라우팅할 때
- 선택지 또는 ordered rubric에 대해 parse 없는 확률 결과와 thresholding이 필요할 때
- API key·usage bill 없이 질문·criteria·threshold를 빠르게 튜닝할 때

## When Not To Use

- Intel Mac, Windows, Linux 또는 macOS 13 미만 환경에서 실행해야 할 때
- 장문·대량 처리나 Flash보다 높은 품질이 우선일 때: hosted 27B `pplx-decider-v1.2`를 평가한다.
- 설명 생성, 자유로운 추론, 문서 작성까지 같은 호출에서 필요할 때: 범용 LLM과 Structured Outputs를 검토한다.
- 사람에게 중대한 영향을 주는 거절·해고·법적 판단을 모델 결과만으로 확정할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/litellm/README|LiteLLM]]

## Sources

- https://docs.perplexity.ai/docs/decisions/decider-for-mac
- https://docs.perplexity.ai/docs/decisions/quickstart
- https://docs.perplexity.ai/api-reference/decisions-post
- https://www.perplexity.ai/en-GB/changelog/ultrafast-computer-models-decisions-api-and-connector-controls
- https://huggingface.co/perplexity-ai/pplx-decider-flash-gguf-v1.2
