---
date: 2026-10-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Gemini 4 Argon — 시작하기

> [[../README|목차로 돌아가기]] | [[02-deep-dive|다음: 심화]]

## Goal

Argon 자체가 아닌 **현재 공개 endpoint가 있는 Gemini 모델**로 Gen AI SDK 호출, streaming, structured output을 실습한다. 모델 ID와 SDK 문법은 출시·region·계정 설정에 따라 바뀔 수 있으므로 실행 직전에 [모델 목록](https://ai.google.dev/gemini-api/docs/models)을 확인한다.

## Prerequisites

- Google AI Studio 또는 Vertex AI project와 유효한 인증 설정
- 공개 API에서 사용 가능한 Gemini 모델 ID
- API key 또는 workload identity를 secret manager/환경 변수로 주입할 수 있는 실행 환경
- 비용 상한, request logging의 민감정보 마스킹, human review 기준

## Minimal Experiment

아래 코드는 SDK의 세부 API가 변경될 수 있는 **의사 코드**다. 핵심은 모델 교체가 쉬운 interface와 결과 검증을 분리하는 것이다.

```python
client = make_genai_client(credentials=load_credentials())

response = client.generate_content(
    model="<currently-available-gemini-model>",
    contents=[{"role": "user", "parts": [{"text": "요구사항을 JSON으로 요약해줘."}]}],
    config={"response_mime_type": "application/json"},
)

result = validate_against_schema(response.text)
save_evaluation_record(result)
```

## Exercise 1: Streaming and Structured Output

| 실험 | 기록할 지표 | 실패 시 확인 |
|---|---|---|
| streaming 요약 | first-token latency, total latency, 중단 복구 | timeout, partial output 처리 |
| structured output | schema validation pass rate | enum/required field, repair retry |
| 문서 질의 | 정확도, citation fidelity, token cost | source 누락, hallucination |

`structured output`은 parser를 줄이는 데 도움이 되지만, business rule 검증이나 권한 검증을 대신하지 않는다. schema 통과 결과도 untrusted input으로 다룬다.

## Exercise 2: Long-context Baseline

1. 내부 문서·issue·코드 묶음에서 접근 권한이 있는 작은 평가 세트를 만든다.
2. retrieval 없이 전체 context를 제공한 결과와 RAG 결합 결과를 비교한다.
3. 정답률 외에 token cost, latency, citation fidelity, 누락 근거를 기록한다.
4. 동일 task set을 보관해 Argon 공개 후 endpoint만 바꾼 A/B evaluation에 사용한다.

## Safety Baseline

- API key를 prompt, source control, 평가 로그에 기록하지 않는다.
- 외부 문서·웹 콘텐츠는 instruction이 아니라 data로 격리한다.
- 도구는 allowlist와 최소 권한으로 노출하고, write·deploy에는 human approval을 둔다.
- model output을 곧바로 shell command, SQL, production patch로 실행하지 않는다.

## Checklist

- [ ] 현재 공개된 모델 ID와 quota를 공식 문서로 확인했다.
- [ ] streaming과 JSON schema validation을 분리해 측정했다.
- [ ] long-context와 RAG의 같은 task set 결과를 비교했다.
- [ ] 비용·latency·citation fidelity를 함께 기록했다.
- [ ] 비밀값·권한·실행 도구의 안전 경계를 점검했다.

## Sources

- https://ai.google.dev/gemini-api/docs/models
- https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/quickstart
