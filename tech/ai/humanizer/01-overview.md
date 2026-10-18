---
date: 2026-10-18
tags: [tech]
type: tech-tool-study
status: draft
---

# Humanizer — Overview

> [[README|목차로 돌아가기]]

## What

Humanizer는 사람이 작성한 것처럼 보이게 하는 단순 치환기가 아니라, 입력 초안을 주어진 **voice, tone, audience, channel, purpose** 제약 아래 다시 쓰는 AI text-rewriting 도구다. 실무에서는 grammar checker, paraphraser, CMS editor, LLM gateway와 결합되는 경우가 많다.

## Why

LLM 초안은 정보 전달 속도는 높지만 문체가 평평하거나 브랜드의 고유한 목소리와 어긋날 수 있다. Humanizer는 문장 리듬·격식·직접성·선호 어휘를 조정해 읽기 쉬운 초안으로 만들되, 다음 불변 조건을 지켜야 한다.

- 사실, 수치, 날짜, 고유명사
- 인용, URL, 출처 표기
- 법률·의학·제품 terminology와 금지어
- 원래의 목적과 독자가 취해야 할 행동

## Core Features

| 계층 | 역할 | 운영상 핵심 |
|---|---|---|
| Input / Context | 원문, audience, channel, tone, glossary, style guide 수집 | PII redaction과 data retention policy를 먼저 적용 |
| Voice modeling | writing sample·style guide에서 문장 길이, 격식, locale, 어휘 선호 추출 | Grammarly는 200단어 이상 sample로 custom voice를 만들 수 있음 |
| Constrained rewrite | tone·readability·purpose 조건에 맞춰 재작성 | preserve list를 prompt와 검증기에 모두 전달 |
| Quality gate | semantic similarity, factuality, citation/URL, glossary, grammar 검사 | 자연스러움보다 의미·근거 보존을 우선 |
| Human-in-the-loop | diff, 변경 이유, version history, 승인자 기록 | publish 전 책임 있는 사람이 최종 결정 |

## Two Market Positions

생산성 중심 제품은 브랜드 voice와 독자 적합성을 개선한다. 반면 detector bypass를 전면에 내세우는 제품은 authorship와 교육·채용 규정을 위반할 위험이 있다. Turnitin도 AI score가 사람 글, AI 글, AI-paraphrased text를 오인할 수 있으므로 제재의 유일한 근거가 되어서는 안 된다고 안내한다. detector score는 품질 KPI가 아니라 참고 신호로만 다룬다.

## Quality Definition

```text
quality = clarity + audience fit + voice consistency
        + factual/citation preservation + approved edits
```

위 식은 산술적 모델이 아니라 도입 판단의 체크 틀이다. 하나의 detector score가 높거나 낮다고 문서 품질이나 저작자 책임이 증명되지는 않는다.

## Sources

- https://support.grammarly.com/hc/en-us/articles/38552339652109-Humanizer-user-guide
- https://guides.turnitin.com/hc/en-us/articles/22774058814093-Using-the-AI-Writing-Report
- https://arxiv.org/abs/2501.03437
