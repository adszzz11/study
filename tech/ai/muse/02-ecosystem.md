---
date: 2026-09-09
tags: [tech]
type: tech-tool-study
status: draft
---

# Muse 생태계와 비교

[[tech/ai/muse/README|학습 진입점]] · 비교 기준일: 2026-09-09

## 목적과 입출력으로 비교하기

| 기술 | 주요 목적·입출력 | Muse와의 관계·차이 | 적용 판단 |
|---|---|---|---|
| Muse / 초기 WHAM | gameplay 화면·행동 → 이후 화면·행동 | 특정 게임의 환경과 사람 행동을 공동 모델링 | 로컬 재현·평가 연구 |
| WHAM-RT | 사용자 조작 → 실시간 생성 화면 | 같은 연구 계열의 실시간 확장, 640×360·10+ FPS | interactive world model 탐색 |
| Google Genie 3 | text prompt → 탐색 가능한 환경 | 다양한 환경 생성, 발표 기준 720p·24 FPS | 범용 환경 생성 연구·체험 |
| Unity AI, 구 Unity Muse | Editor 내 개발 지원·asset 생성 | 게임 제작 workflow를 돕는 도구군 | 실제 Unity 프로젝트 제작 지원 |
| Meta Muse Spark | multimodal reasoning·tool use | 범용 assistant 모델 계열 | 동명 제품; 직접적인 게임 world model 대안은 아님 |

출처는 아래 공식 프로젝트·제품 페이지다. Unity AI FAQ는 Unity Muse를 **deprecated product**로 명시한다. 기존 Unity Muse 튜토리얼을 현재 Unity AI 기능과 동일하게 취급하지 않는다.

## 수치 비교에서 피할 해석

- WHAM-RT와 Genie 3의 해상도·FPS는 서로 다른 환경의 발표 수치다. 동일 benchmark 성능 순위가 아니다.
- 10+ FPS만으로 네트워크를 포함한 입력 지연이나 게임 규칙 재현성을 알 수 없다.
- Quake II의 선별된 약 일주일 gameplay와 초기 Muse의 약 7년 상당 데이터는 게임·범위·수집 방식이 다르다. 단순 나눗셈으로 학습 효율 향상 배수를 계산하지 않는다.
- 초기 WHAM weights 공개 사실에서 WHAM-RT checkpoint도 같은 방식으로 제공된다고 추론하지 않는다.

## 선택 질문

1. **화면과 행동의 관계를 분석하는가?** 초기 WHAM의 공개 모델·sample부터 살펴본다.
2. **입력에 반응하는 생성 환경이 관심인가?** WHAM-RT의 구조·기억 한계를 읽는다. 데모 접속 가능 여부는 이용 시 확인한다.
3. **게임 개발 작업을 돕는가?** Unity AI 같은 Editor 도구의 기능과 프로젝트 적합성을 검토한다.
4. **일반적인 대화·tool use가 필요한가?** Muse Spark는 별도 제품으로 조사한다.

## 주변 구성요소

- **Hugging Face:** 초기 모델, 실행 코드, sample data를 찾는 배포 경로.
- **WHAM Demonstrator:** 모델과의 상호작용을 탐색하는 연구용 UI.
- **ViT-VQGAN / Transformer / MaskGIT:** 구조를 이해하기 위한 핵심 개념.
- **원본 게임 엔진:** 모델 평가 시 실제 상태 변화를 판단하는 기준. 생성 모델과 역할이 다르다.

## Sources

- [Microsoft Research — WHAM 프로젝트](https://www.microsoft.com/en-us/research/project/wham/)
- [WHAM-RT 현재 소개](https://www.microsoft.com/en-us/research/project/wham/wham-rt/)
- [Google DeepMind — Genie 3](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/)
- [Unity AI FAQ](https://unity.com/features/ai?trial=true)
- [Meta — Muse Spark](https://ai.meta.com/blog/introducing-muse-spark-msl/)
- [WHAMM 아키텍처·한계 (2025-04-04)](https://www.microsoft.com/en-us/research/articles/whamm-real-time-world-modelling-of-interactive-environments/)
