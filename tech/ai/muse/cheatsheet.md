---
date: 2026-09-09
tags: [tech]
type: tech-tool-study
status: draft
---

# Muse Cheatsheet

[[tech/ai/muse/README|학습 진입점]] · 기준일: 2026-09-09

## 이름과 숫자

| 항목 | 기억할 내용 |
|---|---|
| Muse | Microsoft Research의 gameplay world model 연구 계열 |
| WHAM | World and Human Action Model |
| 초기 공개 모델 | 200M / 1.6B, Bleeding Edge 특화 |
| 초기 1.6B 화면 | 300×180 → 540 discrete image tokens |
| WHAM-RT | 현재 실시간 계열 명칭 |
| WHAMM | 2025년 World and Human Action MaskGIT Model 명칭 |
| 실시간 출력 | 공식 소개 기준 640×360, 10+ FPS |
| 2025년 실시간 구조 | Backbone 약 500M + Refinement 약 250M |
| 2025년 Quake II context | 9 image-action pairs, 0.9초 |
| 입력 | gameplay 화면·controller actions; 기본 자연어 chatbot 입력과 다름 |

## 평가 용어

- **Consistency:** 전개가 일관적인가? FVD를 규칙 정확성의 증명으로 해석하지 않는다.
- **Diversity:** 여러 타당한 행동이 나오는가? 행동 분포 비교와 화면 노이즈를 구분한다.
- **Persistency:** 추가·수정 요소가 유지되는가? 짧은 유지와 장기 기억은 다르다.

## 실행 명령

아래는 환경·checkpoint·tiny-sample 준비 후 WHAM 저장소에서 실행한다. 세부 준비는 [[tech/ai/muse/04-learning/01-getting-started|Getting started]] 참고. 이 노트에서 실행 검증한 명령은 아니다.

```bash
source venv/bin/activate
python run_dreaming.py --help
python run_dreaming.py --model_path models/WHAM_200M.ckpt --data_path tiny-sample
# 선택: 연구용 Demonstrator 모델 서버
python run_server.py --model models/WHAM_200M.ckpt
```

## 해석 점검

- 초기 WHAM과 WHAM-RT의 사양을 섞지 않는다.
- 생성 영상은 게임 엔진의 정확한 실행 결과가 아니다.
- 타 게임 입력으로 일반화된다고 가정하지 않는다.
- 서로 다른 발표의 FPS·해상도로 benchmark 순위를 만들지 않는다.
- 약 7년과 약 일주일의 데이터량을 학습 효율 배수로 환산하지 않는다.
- weights 공개를 자유로운 상업 이용으로 해석하지 않는다.
- Meta Muse Spark·Unity Muse는 별개다.

## 실험 기록 최소 항목

```text
실행일 / repository revision / checkpoint / prompt
GPU / batch size / 생성 설정 / 소요 시간
일관성 오류 / 행동 다양성 / 객체 유지 / 관찰 한계
```

실제 측정값만 채우고 재현하지 않은 결과는 공식 보고와 구분한다.

## Sources

- [Nature — World and Human Action Models towards gameplay ideation](https://www.nature.com/articles/s41586-025-08600-3)
- [공식 Model Card·실행 코드·weights](https://huggingface.co/microsoft/wham)
- [WHAMM 아키텍처·한계 (2025-04-04)](https://www.microsoft.com/en-us/research/articles/whamm-real-time-world-modelling-of-interactive-environments/)
- [WHAM-RT 현재 소개](https://www.microsoft.com/en-us/research/project/wham/wham-rt/)
- [Microsoft Research License](https://huggingface.co/microsoft/wham/blob/main/LICENSE.md)
