---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview: What / Why / 특징

## What

실시간 ASR(Automatic Speech Recognition)은 발화 도중에도 텍스트를 전달하는 음성 인식 접근이다. 여기서는 Lightning-SimulWhisper의 소개 내용을 바탕으로 Apple Neural Engine 가속과 점진적 출력의 가치를 구분한다.

## Why

녹음 종료 후 변환을 시작하면 사용자는 발화 시간에 더해 변환 시간을 기다린다. 추론 가속은 계산 시간을 줄이고, 점진적 출력은 전체 처리가 끝나기 전에 일부 결과를 확인하게 한다. 두 개선은 서로 대체되지 않는다.

## 개념적 흐름

다음은 소개된 기능을 정리한 흐름이며, 소스코드로 확인한 구현 구조가 아니다.

```text
마이크 / 녹음 파일
  → 음성 입력 처리 · 무음 건너뛰기
  → 소리 분석 · 텍스트 변환 (M2 Neural Engine 가속 강조)
  → 후보 비교 · 단어 경계 유지
  → 확실한 부분부터 점진적 출력
```

| 특징 | 소개된 기능 | 미확인 사항 |
|---|---|---|
| 실행 장치 | Neural Engine 활용 강조 | 연산별 실행 비율, CPU/GPU 분담, fallback |
| 모델 실행 | tiny~large 선택 | 모델 형식·정밀도·메모리·변환 방식 |
| 문맥 대응 | 한국어·자동 언어 감지·용어 사전 | 전문용어 정확도와 사전 적용 단계 |
| 출력 품질 | 후보 비교·단어 경계 유지 | 확실성 판단 기준과 출력 후 수정 허용 여부 |
| 배포 | 무료·오픈소스 Mac 전용으로 소개 | 정확한 라이선스와 지원 기기·OS |

‘소리 분석’과 ‘텍스트 변환’을 특정 encoder/decoder 구현에 대응시키지 않는다. 제품명의 Whisper만으로 upstream 버전이나 다른 Whisper 구현과의 호환성을 확정하지 않는다.

## 성능 주장의 경계

최대 18배와 최대 15배는 서로 다른 단계의 주장이다. 단계별 원래 실행 시간, 가속되지 않는 비중, 출력 대기 시간을 알 수 없으므로 전체 체감 지연 개선 폭을 계산할 수 없다. 빠른 첫 출력과 안정적인 최종 결과도 각각 확인해야 한다.

## 다음 학습

[[tech/ai/apple-neural-engine-asr/02-ecosystem|비교 관점]] · [[tech/ai/apple-neural-engine-asr/README|학습 진입점]]

## Sources

- 사용자 제공 dossier: Lightning-SimulWhisper 소개 영상의 수집 요약. 원본 영상·공식 저장소 URL 미제공이며, 구현과 성능 수치를 독립 검증하지 않았다.
- Apple Core ML 공식 배경 문서: https://developer.apple.com/documentation/coreml — Apple 기기의 모델 실행 개념 참고용. 이 도구가 Core ML을 사용한다는 증거는 아니다.
- Apple MLComputeUnits 공식 배경 문서: https://developer.apple.com/documentation/coreml/mlcomputeunits — 실행 장치 선택 개념 참고용. 이 도구의 실제 연산 배치를 증명하지 않는다.
