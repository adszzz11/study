---
date: 2026-09-09
tags: [tech]
type: tech-tool-study
status: draft
---

# Muse 학습 프로젝트

[[tech/ai/muse/README|학습 진입점]]

아래는 **제안된 학습 과제**다. 실험을 완료했다거나 성능을 측정했다는 의미가 아니다. 실행 파일은 vault 밖에 두고 공개 노트에는 직접 작성한 방법·관찰·공식 링크를 정리한다.

## 프로젝트 1: 같은 시작점의 여러 전개

**질문:** 동일한 prompt에서 생성 결과는 어떻게 달라지는가?

- 준비: [[tech/ai/muse/04-learning/01-getting-started|200M 시작하기]] 완료.
- 수행: prompt 하나를 고정해 여러 rollout을 생성하고 checkpoint·설정을 기록한다.
- 관찰: 이동 방향, 행동 변화, 객체 출현, 처음 깨지는 장면을 구분한다.
- 산출물: 아래 형식의 관찰표와 다양성이 타당한 행동 변화인지에 대한 짧은 해석.
- 완료 기준: 정상·실패 사례를 모두 기록하고 소수 표본의 한계를 명시한다.

| Run | Prompt | 행동 차이 | 첫 이상 시점 | 객체 유지 | 실행 시간 |
|---|---|---|---|---|---|
| 실행 후 기록 | 실행 후 기록 | 실행 후 기록 | 실행 후 기록 | 실행 후 기록 | 실행 후 기록 |

## 프로젝트 2: 200M과 1.6B의 비용·품질 비교

**질문:** 같은 실험 조건에서 모델 크기에 따른 관찰 차이는 무엇인가?

- 준비: 큰 checkpoint를 실행할 하드웨어·저장 공간 확보.
- 수행: 같은 sample과 생성 길이, 동일 GPU 및 batch size를 사용한다. 맞추지 못한 조건은 차이로 명시한다.
- 측정: wall-clock 시간, 가능하면 peak VRAM, 오류 유형과 타당한 행동 전개.
- 산출물: 실험 조건표와 결과표. 모델 크기만으로 품질 향상을 미리 결론 내리지 않는다.
- 완료 기준: 비교 조건과 측정 방법을 다른 사람이 이해할 수 있도록 쓴다.

## 프로젝트 3: 실시간 데모의 기억 한계 읽기

**질문:** 빠르게 생성되는 환경은 화면 밖 상태도 유지하는가?

- 준비: WHAMM의 Limitations와 현재 WHAM-RT 소개를 읽는다.
- 수행: 공식 데모가 접근 가능하면 동일한 객체를 본 뒤 시선을 돌렸다 돌아오는 과정을 관찰한다. 접속 불가하면 공식 사례를 분석하고 직접 실험과 구분한다.
- 산출물: 객체 기억·체력 수치·전투 오류를 구분한 사례 기록.
- 완료 기준: 2025년 보고된 한계와 직접 관찰한 결과의 날짜·출처를 분리한다.

## 프로젝트 4: gameplay ideation 평가안 작성

**질문:** 제작자가 여러 rollout에서 무엇을 판단할 수 있는가?

- 장면의 의도, 허용할 변형, 반드시 유지할 요소를 먼저 정의한다.
- Consistency·Diversity·Persistency별 질문을 각각 만든다.
- 아이디어에 도움이 되는 차이와 게임 규칙을 깨는 오류를 나눠 기록한다.
- 산출물: 한 페이지 평가안. 실제 사용자 연구를 수행하지 않았다면 만족도 수치를 만들지 않는다.

## 공개 산출물 범위

Microsoft Research License는 코드·모델·데이터 배포와 독립 hosted service를 제한한다. 연구 결과의 발표는 허용 조항이 있지만 Materials의 실질적 부분을 포함하지 않아야 한다. 이 프로젝트의 기본 산출물은 자체 작성한 분석이며, 원본 배포물은 공식 링크로 연결한다.

## Sources

- [공식 Model Card·실행 코드·weights](https://huggingface.co/microsoft/wham)
- [Nature — World and Human Action Models towards gameplay ideation](https://www.nature.com/articles/s41586-025-08600-3)
- [WHAMM 아키텍처·한계 (2025-04-04)](https://www.microsoft.com/en-us/research/articles/whamm-real-time-world-modelling-of-interactive-environments/)
- [WHAM-RT 현재 소개](https://www.microsoft.com/en-us/research/project/wham/wham-rt/)
- [Microsoft Research License](https://huggingface.co/microsoft/wham/blob/main/LICENSE.md)
