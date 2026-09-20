---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Jev References

> [[README|목차로 돌아가기]]

## 공식 문서

1. [Introduction](https://docs.typesafe.ai/introduction) — System One과 Jev의 기본 개념
2. [Quick Start / REST API](https://docs.typesafe.ai/introduction/quickstart) — endpoint, model, 첫 호출
3. [Primitives](https://docs.typesafe.ai/primitives) — Choice, Score, Noul schema
4. [Confidence](https://docs.typesafe.ai/confidence) — confidence 의미와 policy 설계
5. [Jev launch post](https://typesafe.ai/blog/introducing-system-one-models-and-jev) — 공개 배경, architecture, vendor evaluation

## SDK와 integration

- [Official Python SDK](https://github.com/typesafe-ai/typesafe-sdk-python)
- [Official JavaScript/TypeScript SDK](https://github.com/typesafe-ai/typesafe-sdk-js)
- [LLM-backed System One adapter](https://github.com/typesafe-ai/system-one-adapter-python)
- [Cloudflare AI Gateway model page](https://developers.cloudflare.com/ai/models/typesafe/jev/)
- [Vercel AI Gateway adoption](https://vercel.com/blog/ai-gateway-jev-model-launch)

## 모델 metadata

- [OpenRouter — Jev 1.13](https://openrouter.ai/typesafe/jev-1.13/) — 가격·context 등 provider metadata. 값은 변경될 수 있으므로 사용 시점에 재확인한다.

## 읽는 순서

Introduction → Primitives → Quick Start → Confidence → SDK README 순으로 읽고, launch post와 gateway 페이지는 vendor 주장·배포 경로를 확인하는 보조 자료로 쓴다.
