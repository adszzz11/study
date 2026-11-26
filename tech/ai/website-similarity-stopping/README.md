---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# 웹사이트 유사도 기반 반복 개선과 종료 조건

> **한 줄 정의**: 웹사이트 제작 결과를 Check 단계에서 평가하고 Build로 되돌려 개선하되, 유사도 90% 또는 최대 6라운드를 종료 기준으로 제시하는 반복 제작 방식이다.

## Overview

Craft Anything 소개 영상 요약에서 관찰된 흐름은 `Browse → Build ↔ Check → Complete`다. 품질 목표인 **유사도 90%**와 실행 한도인 **최대 6라운드**를 함께 둔다. 성공적으로 목표에 도달한 종료와, 미달 상태에서 한도에 도달한 종료는 의미가 다르다.

Similarity metric, reference, 라운드 정의와 실제 달성률은 공개된 수집 자료로 확인할 수 없다. 이 노트는 제품 사용 설명서가 아니라 관찰된 흐름을 바탕으로 종료 정책을 학습하는 자료다.

## Learning Path

- [ ] [[tech/ai/website-similarity-stopping/01-overview|Overview]]
- [ ] [[tech/ai/website-similarity-stopping/02-ecosystem|종료 정책 비교]]
- [ ] [[tech/ai/website-similarity-stopping/03-references|References]]
- [ ] [[tech/ai/website-similarity-stopping/04-learning/01-getting-started|시작하기]]
- [ ] [[tech/ai/website-similarity-stopping/04-learning/02-deep-dive|심화 학습]]
- [ ] [[tech/ai/website-similarity-stopping/05-projects|프로젝트]]
- [ ] [[tech/ai/website-similarity-stopping/cheatsheet|Cheatsheet]]

## When To Use

- reference에 가까운 웹사이트를 반복 제작하면서 품질 목표와 실행 한도를 함께 관리할 때
- 자동 평가 점수와 기능 검사를 분리하고 종료 이유를 기록할 때
- 추가 반복의 이득과 회귀를 관찰하는 실습을 설계할 때

## When Not To Use

- 90%를 기능·접근성·보안까지 보장하는 종합 품질 인증으로 사용할 때
- 6라운드만으로 총시간이나 비용을 보장해야 할 때
- 원본 reference나 재현 가능한 평가 조건 없이 점수만 비교할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/website-similarity-stopping/01-overview|웹사이트 반복 평가 개요]]

## Sources

- 제공된 dossier: Craft Anything 소개 영상의 수집 요약. 원본 영상 URL과 공식 문서 URL은 제공되지 않았다. 따라서 기재할 수 있는 출처 URL이 없으며, 임의로 추정하지 않는다.
- 아래 정책 해석과 실습 제안은 제품 구현이나 성능을 검증한 자료가 아니다.
