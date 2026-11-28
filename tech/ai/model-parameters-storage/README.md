---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# AI 모델의 파라미터·저장 용량과 로컬 실행의 판단 기준

> **한 줄 정의**: Parameters의 수와 저장 파일의 크기를 구분하고, Coding Evaluation과 Local Inference 조건을 따로 검증해 모델 활용 여부를 판단하는 학습 노트다.

## Overview

영상 요약은 “모델 크기를 줄이면 성능도 떨어지는가?”에서 시작해 세 가지 값을 쓰는 표현 방식, 코딩 능력, 노트북 실행, 회사 문서 처리로 확장된다. 핵심은 **저장 용량·성능·실행 가능성이 각각 다른 판단 대상**이라는 점이다.

- 약 54GB·3.6GB 비교와 별도 5.9GB 표기가 등장하지만 측정 대상과 관계는 미확인이다.
- 동일 기준이라는 가정 아래 54 ÷ 3.6 = 15다. 특정 모델의 15배 압축을 입증하지 않는다.
- 모델명, 저장 규격, 평가 조건, 장치 사양이 없어 특정 Quantization·Pruning·ternary 구현이나 실행 가능성을 확정할 수 없다.
- Apache 2.0 가중치 공개 언급도 실제 배포물과 라이선스 적용 범위 확인이 필요하다.

## Learning Path

- [ ] [[tech/ai/model-parameters-storage/README|학습 안내 다시 보기]]
- [ ] [[tech/ai/model-parameters-storage/01-overview|Overview]]
- [ ] [[tech/ai/model-parameters-storage/02-ecosystem|Ecosystem 비교]]
- [ ] [[tech/ai/model-parameters-storage/03-references|References]]
- [ ] [[tech/ai/model-parameters-storage/04-learning/01-getting-started|시작하기]]
- [ ] [[tech/ai/model-parameters-storage/04-learning/02-deep-dive|심화 학습]]
- [ ] [[tech/ai/model-parameters-storage/05-projects|Projects]]
- [ ] [[tech/ai/model-parameters-storage/cheatsheet|Cheatsheet]]

## When To Use

- 모델 다운로드 전에 파일 크기와 실행 메모리 요구를 구분할 때.
- 작은 배포 파일의 코딩 품질을 같은 조건으로 비교할 때.
- 노트북 실행이나 회사 문서 처리의 검증 계획을 세울 때.

## When Not To Use

- 이 요약만으로 특정 모델의 압축률·코딩 순위·권장 사양을 확정할 때.
- 5.9GB를 실행 메모리로 간주하거나 로컬이라는 이름만으로 외부 전송이 없다고 판단할 때.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/apple-silicon-local-llm/README|Apple Silicon 로컬 LLM 학습 가이드]] — 장치·런타임 검토를 이어갈 관련 노트.

## Sources

- 사용자 제공 dossier: 영상 관찰 요약. 원영상 URL·모델 식별자는 제공되지 않아 원자료 대조 불가.
- 보충 개념 자료: Hugging Face Transformers Quantization — https://huggingface.co/docs/transformers/quantization/overview
- 보충 라이선스 원문: Apache License 2.0 — https://www.apache.org/licenses/LICENSE-2.0

보충 URL은 일반 개념과 라이선스를 위한 참고이며, 영상의 모델·수치·성능을 입증하는 출처가 아니다.
