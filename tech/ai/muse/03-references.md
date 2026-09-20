---
date: 2026-09-09
tags: [tech]
type: tech-tool-study
status: draft
---

# Muse 참고자료

[[tech/ai/muse/README|학습 진입점]] · 기준일: 2026-09-09

## 권장 읽기 순서

1. **최초 발표:** gameplay ideation이라는 문제와 연구 배경을 파악한다.
2. **현재 WHAM 프로젝트:** 초기 모델과 실시간 계열의 명칭을 구분한다.
3. **Model Card + License:** 지원 환경·입력·사용 조건을 확인한다.
4. **Nature 논문:** 모델 구조와 세 평가 축의 실험 조건을 읽는다.
5. **WHAMM 기술 설명 + WHAM-RT:** 생성 지연 개선과 기억 한계를 연결한다.

## 주장별 근거 지도

| 확인할 주장 | 우선 자료 | 확인할 부분 |
|---|---|---|
| Muse의 목적·협력·공개 시점 | 최초 발표 | 연구 목적과 공개 구성물 |
| 27명 인터뷰·평가 방법·tokenization | Nature 논문 | 사용자 연구, 방법, 평가 조건 |
| 200M·1.6B 및 실행 방법 | Model Card | Trained Models, Usage |
| 실습 입력 | sample dataset | tiny-sample 및 데이터 설명 |
| 비상업 연구·배포 제한 | License | Sections 1, 2, 5 |
| 현재 실시간 계열 명칭 | WHAM-RT | 현재 소개와 2025년 설명 링크 |
| 약 500M/250M 구조·0.9초 context | WHAMM 발표 | Architecture, Limitations |
| 동명 제품과 대안 | Genie 3 / Unity AI / Muse Spark | 각 공식 페이지의 목적·입출력 |

## 자료를 해석하는 원칙

- **발표일과 확인일 분리:** 2025년 데모의 한계를 향후 모든 모델에 일반화하지 않는다.
- **재현성과 소개 구분:** 영상 데모, 공개 checkpoint, 실제 실행 기록은 다른 종류의 근거다.
- **학습 데이터와 공개 sample 구분:** sample을 전체 학습 데이터로 간주하지 않는다.
- **논문 지표와 관찰 구분:** 소수 rollout을 눈으로 비교한 결과를 FVD 재현 결과라고 쓰지 않는다.
- 제공 dossier는 참고자료 8번 URL 중간에서 끝난다. WHAM-RT URL은 dossier 본문에 있는 완전한 주소와 공식 페이지로 보완했다.

## 후속 확인 항목

- [ ] 실습 시 모델 저장소 revision과 checkpoint 이름을 기록한다.
- [ ] 데모 접근 가능 여부와 별도 이용 조건을 실행 시점에 확인한다.
- [ ] 실시간 모델의 배포 상태가 바뀌면 공식 배포 링크를 근거로 갱신한다.
- [ ] 출처 변경 시 새 확인일과 해당 주장만 갱신한다.

## Sources

- [Microsoft Research — WHAM 프로젝트](https://www.microsoft.com/en-us/research/project/wham/)
- [Muse 최초 발표 (2025-02-19)](https://www.microsoft.com/en-us/research/blog/introducing-muse-our-first-generative-ai-model-designed-for-gameplay-ideation/)
- [Nature — World and Human Action Models towards gameplay ideation](https://www.nature.com/articles/s41586-025-08600-3)
- [공식 Model Card·실행 코드·weights](https://huggingface.co/microsoft/wham)
- [Bleeding Edge sample dataset](https://huggingface.co/datasets/microsoft/bleeding-edge-gameplay-sample)
- [Microsoft Research License](https://huggingface.co/microsoft/wham/blob/main/LICENSE.md)
- [WHAM-RT 현재 소개](https://www.microsoft.com/en-us/research/project/wham/wham-rt/)
- [WHAMM 아키텍처·한계 (2025-04-04)](https://www.microsoft.com/en-us/research/articles/whamm-real-time-world-modelling-of-interactive-environments/)
- [Google DeepMind — Genie 3](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/)
- [Unity AI FAQ](https://unity.com/features/ai?trial=true)
- [Meta — Muse Spark](https://ai.meta.com/blog/introducing-muse-spark-msl/)

## 추가 조사: Meta Muse 재학습용 1차 자료

> 확인일: 2026-09-09. 위 Microsoft 자료는 동명 연구 참고용이다. Meta 학습에는 아래 자료를 우선한다.

| 읽기 순서 | 공식 자료 | 확인할 내용 |
|---|---|---|
| 1 | [Muse 제품 발표](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) | 2026-09-08 제품 범위와 배포 상태 |
| 2 | [How We Designed Muse](https://introducing.muse.ai/) | Goals, Memory, Artifacts, 활동 기록 |
| 3 | [Muse Spark 최초 기술 발표](https://ai.meta.com/blog/introducing-muse-spark-msl/) | 모델 학습과 추론의 scaling axes |
| 4 | [Muse Spark 1.3](https://research.meta.ai/blog/introducing-muse-spark-1-3) | 2026-09-02 모델 업데이트와 제공 경로 |

### 근거의 한계와 다음 조사

- 제품 발표가 연결한 [보안 상세 자료](https://security.muse.ai/)는 이번 열람에서 리다이렉트 후 본문을 가져오지 못했다. 상세 구현을 확인한 것으로 간주하지 않는다.
- 발표일, 페이지 갱신일, 실제 실험일을 분리한다. 마케팅 표현을 독립적인 비교 평가로 취급하지 않는다.
- API 실습을 추가할 때는 공식 개발 문서에서 endpoint, model ID, 인증 방식, 가격·제한을 다시 확인한다. 이번 보강에서는 API 호출이나 제품 실행을 수행하지 않았다.
