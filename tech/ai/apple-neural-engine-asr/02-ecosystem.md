---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem: 처리 방식 비교

## 비교 범위

dossier에는 개별 경쟁 제품의 근거가 없다. 아래 표는 제품 순위가 아니라 소개된 기능을 평가하기 위한 비교 축이다.

| 비교 축 | Lightning-SimulWhisper 소개 | 대안·실험 관점 | 판단 가능한 범위 |
|---|---|---|---|
| 출력 시점 | 확실한 부분부터 출력 | 녹음 종료 후 일괄 변환 | 출력 정책의 차이 |
| 실행 위치 | Mac 내부, 녹음 서버 전송 없음 | 서버 처리 구성 | 소개된 로컬 처리 특성 |
| 가속 장치 | M2 Neural Engine 강조 | 다른 장치·가속 설정 | 상대 속도·효율 비교 불가 |
| 모델 | tiny~large 선택 | 같은 입력에서 모델 변경 | 선택 기능만 확인 |
| 언어·용어 | 한국어·자동 감지·용어 사전 | 설정 활성화 전후 비교 | 효과 크기 미확인 |
| 배포 | 무료·오픈소스 Mac 전용으로 소개 | 다른 플랫폼·라이선스 | 정확한 라이선스·지원 범위 미제공 |

## 선택 기준

- 짧은 메모: 최초 출력 지연과 수정 빈도를 먼저 본다.
- 긴 발화: 확정 지연과 backlog 누적을 본다.
- 전문용어: 용어 정확도와 일반 문장의 오류 변화를 함께 본다.
- 외부 전송 제한: 네트워크 관찰에 더해 전사문·로그·임시 파일 저장 방식을 확인한다.

Apple Silicon에서 실행된다는 사실만으로 Neural Engine 사용을 확정할 수 없다. Core ML의 실행 장치 선택 개념도 이 도구의 내부 구성과는 별도의 배경 지식이다.

## 다음 학습

[[tech/ai/apple-neural-engine-asr/04-learning/01-getting-started|동일 조건 실험 준비]] · [[tech/ai/apple-neural-engine-asr/README|학습 진입점]]

## Sources

- 사용자 제공 dossier: Lightning-SimulWhisper 소개 영상의 수집 요약. 원본 영상·공식 저장소 URL 미제공이며, 구현과 성능 수치를 독립 검증하지 않았다.
- Apple Core ML 공식 배경 문서: https://developer.apple.com/documentation/coreml — Apple 기기의 모델 실행 개념 참고용. 이 도구가 Core ML을 사용한다는 증거는 아니다.
- Apple MLComputeUnits 공식 배경 문서: https://developer.apple.com/documentation/coreml/mlcomputeunits — 실행 장치 선택 개념 참고용. 이 도구의 실제 연산 배치를 증명하지 않는다.
