---
date: 2026-10-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Gemini 4 Argon — References

> [[README|목차로 돌아가기]]

## Primary Sources

1. [Google 공식 발표 — Gemini 4 Argon](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/) — 발표 배경, capability, 접근·가격 상태의 1차 출처.
2. [Google DeepMind — Gemini 모델 페이지 및 평가표](https://deepmind.google/models/gemini/) — Vals Index, DeepSWE, GraphWalks 등 공급자 발표 평가를 확인한다.
3. [Google DeepMind — Argon cybersecurity capability](https://deepmind.google/models/gemini/cyber/) — defensive cybersecurity 범위와 평가 설명을 확인한다.
4. [Google DeepMind — Fairwind Program](https://deepmind.google/fairwind-program/) — trusted cyber defender 대상 제한 배포의 접근 조건을 확인한다.
5. [Google DeepMind — Frontier Safety Framework](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) — safety case, frontier risk 관리의 배경 자료.

## Implementation References

6. [Gemini API 모델 목록](https://ai.google.dev/gemini-api/docs/models) — 현재 호출 가능한 Gemini API 모델 및 모델별 제약을 확인한다.
7. [Gemini API in Vertex AI Quickstart](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/quickstart) — Vertex AI에서 API를 시작하는 공식 안내.
8. [Gemini 1 기술 보고서](https://deepmind.google/gemini/gemini_1_report.pdf) — Gemini 계열 multimodality 연구의 역사적 기술 배경.

## Reading Order

1. 공식 발표와 모델 평가표를 함께 읽고, 주장과 측정치를 구분한다.
2. cyber capability와 Frontier Safety Framework로 허용되는 defensive workflow의 경계를 확인한다.
3. Fairwind 접근 상태를 확인한 뒤, 실습은 공개 API 모델 문서와 Vertex AI Quickstart로 진행한다.
4. benchmark 수치를 조직의 자체 evaluation으로 대체하지 않는다.
