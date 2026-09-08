---
date: 2026-09-09
tags: [tech]
type: tech-tool-study
status: draft
---

# Muse 심화: 생성 구조와 평가

[[tech/ai/muse/README|학습 진입점]] · 이전: [[tech/ai/muse/04-learning/01-getting-started|Getting started]]

## 1. 초기 WHAM의 token sequence

1. ViT-VQGAN으로 게임 화면을 discrete image tokens로 바꾼다.
2. controller actions를 action tokens로 표현한다.
3. 시간 순서대로 화면과 행동을 교차 배치한다.
4. decoder-only Transformer가 다음 token을 예측한다.
5. 예측한 image tokens를 화면으로 복원하고 다음 step으로 진행한다.

```text
[image_t tokens][action_t tokens][image_t+1 tokens][action_t+1 tokens]...
```

이 표기는 개념 설명이며 실제 파일 포맷이나 실행 API가 아니다. 어떤 token을 조건으로 고정하고 어떤 token을 생성하는지가 world modelling·behaviour policy·joint generation을 구분한다.

**생각할 질문:** 화면을 압축하며 사라지는 작은 UI 정보가 이후 수치 인식에 어떤 영향을 줄 수 있는가? 이는 실험으로 확인할 가설이며, 특정 오류의 원인으로 단정하지 않는다.

## 2. WHAM-RT / 2025 WHAMM의 지연 개선

초기 WHAM은 화면 token을 순차 생성한다. 실시간 계열은 **MaskGIT**로 여러 token을 병렬 예측하고 다시 mask하여 반복 정제한다.

```text
이전 9개 image-action pairs
          ↓
Backbone Transformer (~500M)
          ├── 다음 화면 token 초안
          └── 작은 conditioning representation
                         ↓
           Refinement Transformer (~250M)
                         ↓
               mask → 예측 → 반복 정제
                         ↓
                    다음 화면 복원
```

큰 Backbone을 여러 번 실행하는 비용을 줄이고 작은 Refinement로 품질을 개선한다. 2025년 구조 설명과 현재 WHAM-RT 소개를 함께 읽되, 초기 공개 checkpoint의 구조로 혼동하지 않는다.

## 3. 세 평가 축을 분리하기

| 축 | 논문·dossier의 접근 | 학습용 관찰 | 해석의 한계 |
|---|---|---|---|
| Consistency | FVD | 위치·움직임·장면 연결이 갑자기 깨지는 시점 | 좋은 영상 분포가 규칙 정확성을 보장하지 않음 |
| Diversity | 행동 분포의 Wasserstein distance | 같은 prompt의 여러 rollout이 다른 타당한 선택을 보이는가 | 화면 노이즈와 의미 있는 행동 차이를 구분 |
| Persistency | 추가한 객체·캐릭터의 유지 | 수정 요소가 이후에도 남는가 | 화면에 계속 보이는 것과 화면 밖 기억은 다름 |

공식 지표를 재현하려면 sample 수, 전처리, feature extractor와 평가 구간을 논문과 맞춰야 한다. 아래 실습은 정성 관찰이며 논문 수치의 재현을 주장하지 않는다.

## 4. 작은 비교 실험 설계

1. 같은 prompt와 checkpoint를 고정한다.
2. 반복 생성 설정을 기록한다. seed 옵션은 실제 `--help`와 코드에서 확인한다.
3. rollout마다 첫 이상 시점, 행동 변화, 객체 유지 여부를 기록한다.
4. 모델 크기를 바꿀 때 prompt·길이·하드웨어·batch size를 맞춘다.
5. 영상 품질, 생성 시간, 규칙 위반을 별도로 정리한다.

```yaml
# 학습용 기록 예시이며 Muse 설정 파일이 아니다.
checkpoint: WHAM_200M.ckpt
repository_revision: "record-the-actual-revision"
prompt_id: "record-the-actual-sample"
run_id: 1
first_inconsistency_seconds: null
observed_action_variation: ""
object_persistence_observation: ""
```

## 5. 단기 context가 주는 한계

2025년 Quake II 데모는 9 frames / 10 FPS, 즉 0.9초 context를 사용한다. 화면 밖 객체의 상태가 달라지거나 체력·전투가 부정확할 수 있다. FPS 개선과 장기 기억 개선은 별도 문제다.

공식 비교에서 데이터는 초기 Muse 약 7년 상당에서 Quake II 약 일주일로 줄었지만, 후자는 범위를 좁히고 gameplay를 선별했다. 데이터 양만으로 일반적 학습 효율을 판정할 수 없다.

## 이해도 점검

- [ ] image tokenizer와 sequence model의 역할을 각각 설명할 수 있다.
- [ ] MaskGIT가 token별 순차 생성의 지연을 줄이는 이유를 설명할 수 있다.
- [ ] 같은 rollout의 자연스러움과 규칙 위반을 따로 평가할 수 있다.
- [ ] 짧은 context와 rollout 전체 길이를 혼동하지 않는다.

## Sources

- [Nature — World and Human Action Models towards gameplay ideation](https://www.nature.com/articles/s41586-025-08600-3)
- [WHAMM 아키텍처·한계 (2025-04-04)](https://www.microsoft.com/en-us/research/articles/whamm-real-time-world-modelling-of-interactive-environments/)
- [WHAM-RT 현재 소개](https://www.microsoft.com/en-us/research/project/wham/wham-rt/)
