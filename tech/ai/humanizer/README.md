---
date: 2026-10-18
tags: [tech]
type: tech-tool-study
status: draft
---

# Humanizer

> **한 줄 정의**: Humanizer는 LLM 초안을 사용자의 voice·tone·문맥에 맞게 다시 쓰고, 자연스러운 표현과 가독성을 높이는 AI text-rewriting 계열 제품이다.

## Overview

LLM은 빠르게 초안을 만들지만 문장 길이, 전환어, 어휘가 균질해져 독자에게 `robotic`하게 느껴질 수 있다. Humanizer는 이를 **style transfer + constrained rewriting** 문제로 다룬다. 좋은 결과는 단지 문장을 바꾸는 것이 아니라, 원문의 사실·수치·인용을 보존한 채 독자와 채널에 맞는 표현으로 편집하는 것이다.

이 범주에는 brand voice와 편집 생산성을 목표로 하는 제품, 그리고 AI detector 판정을 낮추는 것을 전면에 내세우는 제품이 함께 있다. 후자를 품질 목표로 삼으면 academic integrity, 저작자 표시, 평판 위험이 생긴다. detector score 대신 명확성, 독자 적합성, 사실 보존, 편집 승인률을 평가 기준으로 둔다.

## Learning Path

- [ ] [[01-overview|개요]] — What/Why와 핵심 특징 이해
- [ ] [[02-ecosystem|생태계]] — 제품·DIY pipeline·전통 편집 도구 비교
- [ ] [[03-references|참고자료]] — 공식 문서와 detector 연구 읽기
- [ ] [[04-learning/01-getting-started|시작하기]] — 안전한 rewrite 평가 세트 만들기
- [ ] [[04-learning/02-deep-dive|심화]] — constrained rewrite, QA, provenance 설계
- [ ] [[05-projects|프로젝트]] — brand voice·localization·editorial workflow 적용
- [ ] [[cheatsheet|치트시트]] — 입력 계약, 품질 gate, 운영 규칙 빠른 참조

## When To Use

- 브랜드 style guide, 독자 수준, channel별 tone에 맞춰 초안을 편집할 때
- 번역 뒤의 직역투를 줄이되 제품명·수치·전문 용어는 유지해야 할 때
- support reply나 editorial draft를 더 명확하고 따뜻하게 다듬을 때
- diff, 검증, 최종 승인까지 포함한 조직의 writing workflow를 만들 때

## When Not To Use

- detector score를 낮추거나 authorship를 숨기는 목적의 제출물에 사용할 때
- 법률·의학·재무 문서에서 사실 검증과 담당자 승인을 생략할 때
- 인용, URL, 고유명사, 계약상 표현을 보존할 수 없는 단순 재작성에 맡길 때
- 민감한 원문을 retention policy·PII redaction 검토 없이 외부 서비스에 보낼 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/litellm/README|LiteLLM]] — LLM gateway와 provider별 모델 호출을 다루는 도구

## Sources

- https://support.grammarly.com/hc/en-us/articles/38552339652109-Humanizer-user-guide
- https://quillbot.com/ai-humanizer
- https://help.undetectable.ai/en/article/humanization-api-v2-p28b2n/
- https://guides.turnitin.com/hc/en-us/articles/22774058814093-Using-the-AI-Writing-Report
- https://arxiv.org/abs/2501.03437
