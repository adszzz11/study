---
date: 2026-09-09
tags: [tech]
type: tech-tool-study
status: draft
---

# Muse: What / Why / 특징

[[tech/ai/muse/README|학습 진입점]] · 기준일: 2026-09-09

## What

Muse는 gameplay 화면과 controller actions의 관계를 학습하는 world model 연구다. 초기 모델 WHAM은 다음 token을 예측하는 decoder-only Transformer를 사용한다. 자연어 대화보다 **화면·행동 sequence**가 입력의 중심이다.

| 동작 모드 | 주어지는 조건 | 생성 결과 |
|---|---|---|
| World modelling | 이전 화면과 controller actions | 이후 화면 |
| Behaviour policy | 이전 화면·기록 | controller actions |
| Joint generation | 초기 gameplay prompt | 화면과 행동 모두 |

## Why

게임 아이디어를 검토하려면 장면, 움직임, 여러 플레이 상황을 구현하고 비교해야 한다. Muse는 기록된 gameplay를 바탕으로 짧은 장면에서 가능한 전개를 탐색하도록 돕는 접근이다. 완성된 게임을 자동 제작한다는 의미는 아니다.

Microsoft Research와 Xbox Game Studios의 Ninja Theory가 협력했다. 2025-02-19 Nature 논문과 함께 모델 weights, sample data, WHAM Demonstrator가 공개됐다. 연구진은 게임 제작 관련 종사자 27명의 인터뷰에서 다음 요구를 도출했다.

| 요구 | 질문 | 평가 접근과 해석 |
|---|---|---|
| Consistency | 시간과 게임 규칙에 맞게 이어지는가? | FVD로 영상 분포 비교; 정확한 규칙 실행의 증명은 아님 |
| Diversity | 같은 시작점에서 여러 타당한 전개가 나오는가? | 행동 분포의 Wasserstein distance; 무작위 오류와 다양성을 구분 |
| Persistency | 추가·수정한 요소가 이후에도 유지되는가? | 장면 수정 후 유지 여부 관찰; 무한한 기억을 뜻하지 않음 |

## 핵심 구조

```text
게임 화면 ── ViT-VQGAN ── image tokens ──┐
controller actions ───── action tokens ─┤
                                       ↓
                         화면·행동을 교차 배치한 sequence
                                       ↓
                            decoder-only Transformer
                                       ↓
                         다음 화면·행동 tokens → rollout
```

1.6B WHAM은 300×180 화면을 540개 discrete tokens로 표현한다. 학습에는 PyTorch Lightning과 FSDP가 사용됐다. 공개 checkpoint는 200M과 1.6B이며 초기 탐색에는 작은 모델을 사용할 수 있다.

## 2025–2026 흐름

| 시점 | 확인된 변화 | 읽는 방법 |
|---|---|---|
| 2025-02-19 | 초기 Muse/WHAM 공개 | Bleeding Edge 기반 연구 |
| 2025-04-04 | WHAMM 기반 Quake II 실시간 데모 | 입력에 반응하는 생성 속도 개선 |
| 2026-09-09 기준 | 현재 프로젝트가 WHAM·WHAM-RT 소개 | 초기 checkpoint와 실시간 계열 구분 |

현재 WHAM-RT 소개는 2025년 WHAMM 설명으로 연결된다. 제공 dossier와 확인한 공식 자료에서는 별도 **“Muse 2” 정식 출시를 확인하지 못했다**. 이를 출시가 없다는 보편적 단정으로 확대하지 않는다.

## 제한과 적용 경계

- 초기 WHAM은 Bleeding Edge에 특화됐고 실시간 사용에는 느리다.
- 2025년 Quake II 데모는 전투·체력 수치·화면 밖 객체 기억에서 오류가 보고됐다. 해당 데모의 0.9초 context는 초기 WHAM의 설정과 구분한다.
- 게임을 학습해 근사한 결과이므로 원본 게임의 정확한 실행을 보장하는 emulator와 다르다.
- Microsoft Research License는 비상업·비수익 연구 목적을 허용하며 코드·모델 재배포와 독립 hosted service 제공 등을 제한한다. 공개 vault에는 자체 학습 설명과 공식 링크를 남기고 원본 배포물을 복사하지 않는다.

## Sources

- [Muse 최초 발표 (2025-02-19)](https://www.microsoft.com/en-us/research/blog/introducing-muse-our-first-generative-ai-model-designed-for-gameplay-ideation/)
- [Nature — World and Human Action Models towards gameplay ideation](https://www.nature.com/articles/s41586-025-08600-3)
- [공식 Model Card·실행 코드·weights](https://huggingface.co/microsoft/wham)
- [WHAMM 아키텍처·한계 (2025-04-04)](https://www.microsoft.com/en-us/research/articles/whamm-real-time-world-modelling-of-interactive-environments/)
- [WHAM-RT 현재 소개](https://www.microsoft.com/en-us/research/project/wham/wham-rt/)
- [Microsoft Research License](https://huggingface.co/microsoft/wham/blob/main/LICENSE.md)
