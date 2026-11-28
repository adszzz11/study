---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# References: 출처와 근거 수준

## 1차 자료 상태

제공 dossier는 Lightning-SimulWhisper 소개 영상의 수집 요약이다. 영상 URL·작성자·게시일·공식 저장소 URL이 없어 원문 대조나 재현은 수행하지 않았다. 이름이 비슷한 저장소를 공식 자료로 추정해 연결하지 않는다.

| 주장 | 현재 근거 | 추가 확인 자료 |
|---|---|---|
| 무료·오픈소스 | 소개 요약 | 공식 저장소, LICENSE, 배포 경로 |
| 최대 18배·15배 | 측정 과정 없는 영상 설명 | 기준 장치·모델·입력·정확도·벤치마크 코드 |
| Neural Engine 활용 | 기능 소개 | 실행 프로파일, 연산 그래프, CPU/GPU 분담 |
| 로컬 음성 처리 | 서버 전송 없다는 설명 | 네트워크 관찰, 데이터 흐름·저장 정책 |
| 한국어·용어 사전 | 기능 소개 | 고정 입력의 적용 전후 결과 |

## 공식 배경 자료의 역할

Apple Core ML 문서와 MLComputeUnits 문서는 모델 실행 및 장치 선택을 학습하는 자료다. Lightning-SimulWhisper의 Core ML 채택, 전체 모델의 Neural Engine 실행, 성능 배수를 입증하지 않는다.

## 원문 확보 후 확인할 항목

- [ ] 공식 배포처·LICENSE·버전·commit을 식별한다.
- [ ] macOS·칩·메모리 요구 사항과 모델 다운로드 경로를 확인한다.
- [ ] 출력 확정 정책과 용어 사전 적용 방식을 확인한다.
- [ ] 성능 주장에 대응하는 재현 조건을 확보한다.

## 다음 학습

[[tech/ai/apple-neural-engine-asr/04-learning/02-deep-dive|검증 설계]] · [[tech/ai/apple-neural-engine-asr/README|학습 진입점]]

## Sources

- 사용자 제공 dossier: Lightning-SimulWhisper 소개 영상의 수집 요약. 원본 영상·공식 저장소 URL 미제공이며, 구현과 성능 수치를 독립 검증하지 않았다.
- Apple Core ML 공식 배경 문서: https://developer.apple.com/documentation/coreml — Apple 기기의 모델 실행 개념 참고용. 이 도구가 Core ML을 사용한다는 증거는 아니다.
- Apple MLComputeUnits 공식 배경 문서: https://developer.apple.com/documentation/coreml/mlcomputeunits — 실행 장치 선택 개념 참고용. 이 도구의 실제 연산 배치를 증명하지 않는다.
