---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem: 접근과 배포 선택 비교

모델명·제품명이 없어 특정 경쟁 제품의 순위를 매길 수 없다.

| 비교 대상 | 자료에서 확인되는 내용 | 평가 기준 | 판단의 한계 |
|---|---|---|---|
| 큰 모델 파일 | 약 54GB 표기 | 기준 품질·저장·실행 비용 | 기준 모델인지 미확인 |
| 작은 모델 파일 | 3.6GB·5.9GB 표기 | 크기와 품질 변화 | 두 값의 관계·모델 대응 불명 |
| 세 값 표현 | 표현 방식 소개 | 적용 범위·저장 형식·runtime 지원 | 알고리즘 미확인 |
| 노트북 로컬 실행 | 실행 가능성 질문 | 로딩·메모리·응답 시간·품질 | 사양·실측 없음 |
| 회사 문서 로컬 처리 | 클라우드와 대비 | 처리 경로·업무 정확도 | 외부 통신 미확인 |
| 클라우드 처리 | 로컬 대안으로 등장 | 전송 경로·서비스 조건 | 제공자·비용·성능 불명 |

## 선택 기준

- 로컬: 장치에서 목표 품질과 시간·메모리 한도를 만족하는지 실측한다. 다운로드·업데이트·telemetry·외부 API 호출 등 실제 처리 경로도 확인한다.
- 클라우드: 제공자별 데이터 처리 조건, 비용, 응답 시간, 업무 정확도를 조사한다. 이 dossier에는 비교 수치가 없다.
- 압축 모델: 변환 관계가 확인된 원본과 비교해야 압축 효과를 논의할 수 있다.

목표는 최소 파일 크기가 아니라 **필요한 품질과 실행 조건의 동시 충족**이다. llama.cpp 같은 runtime은 조사 후보이며 미상 모델의 실행 지원을 뜻하지 않는다.

## 다음 학습

[[tech/ai/model-compression-coding-evaluation/04-learning/01-getting-started|평가 준비]] · [[tech/ai/model-compression-coding-evaluation/README|학습 경로]]

## Sources

- 사용자 제공 dossier: 원영상 URL·모델 배포 URL이 제공되지 않음. 아래 링크는 보충 학습 자료이며 영상의 모델·수치를 입증하지 않는다.
- HumanEval 공식 저장소: https://github.com/openai/human-eval — 코드 생성 결과를 실행 테스트로 평가하는 참고 자료.
- llama.cpp 공식 저장소: https://github.com/ggml-org/llama.cpp — 로컬 inference runtime 조사 출발점. 대상 모델과의 호환성은 별도 확인.
- Apache License 2.0 원문: https://www.apache.org/licenses/LICENSE-2.0 — 개별 가중치에 적용되는지는 배포물에서 확인.
