---
date: 2026-10-18
tags: [tech]
type: tech-tool-study
status: draft
---

# Humanizer — References

> [[README|목차로 돌아가기]]

## Product Documentation

1. [Grammarly — Humanizer user guide](https://support.grammarly.com/hc/en-us/articles/38552339652109-Humanizer-user-guide) — custom voice와 Humanizer 사용 흐름.
2. [QuillBot — AI Humanizer](https://quillbot.com/ai-humanizer) — 용도와 responsible use 안내.
3. [QuillBot Help — Paraphraser modes](https://help.quillbot.com/hc/en-us/articles/35854318883351-What-are-modes-in-the-Quillbot-Paraphraser-and-how-do-I-use-them) — paraphrasing mode의 목적과 사용법.
4. [Undetectable.AI — Humanization API v2](https://help.undetectable.ai/en/article/humanization-api-v2-p28b2n/) — readability, purpose, strength와 streaming API 제어값.

## Policy and Assessment Context

5. [Turnitin — Using the AI Writing Report](https://guides.turnitin.com/hc/en-us/articles/22774058814093-Using-the-AI-Writing-Report) — AI score의 한계와 적절한 사용 범위.

## Research

6. [DAMAGE: Detecting Adversarially Modified AI Generated Text (2025)](https://arxiv.org/abs/2501.03437) — 19개 humanizer/paraphraser와 detector 취약성, augmentation 기반 탐지 가능성을 조사.
7. [AuthorMist: Evading AI Text Detectors with Reinforcement Learning (2025)](https://arxiv.org/abs/2503.08716) — detector 회피를 다룬 연구; 생산성 도구의 품질 목표로 채택하지 않는다.
8. [Understanding effects of human-written paraphrases in LLM-text detection (2025)](https://doi.org/10.1016/j.nlp.2025.100151) — 사람이 쓴 paraphrase가 LLM-text detection에 미치는 영향을 분석.

## Reading Rule

제품 문서는 기능과 제약을, 연구는 방법과 실험 조건을 설명한다. 어느 한 자료도 특정 조직의 문서 품질, 규정 준수, detector 신뢰성을 보장하지 않는다. 도입 전에는 실제 승인 문서로 만든 evaluation set과 human review 결과를 우선한다.
