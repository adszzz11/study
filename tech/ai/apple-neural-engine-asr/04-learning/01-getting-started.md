---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: 기준 실험 만들기

## 목표와 준비

설치 명령이나 패키지 이름은 제공 자료로 확인되지 않는다. 공식 배포처가 식별되기 전 임의의 설치 명령을 실행하지 않는다. 다음은 도구를 확보한 후 수행할 평가 절차이며 검증된 실행 결과가 아니다.

1. 공식 저장소·LICENSE와 지원 macOS·칩·메모리를 확인한다.
2. Mac 모델, 칩, 메모리, OS, 앱 버전, 모델 이름을 기록한다.
3. 한국어 일반 문장과 전문용어 문장의 고정 녹음 및 정답 전사문을 준비한다.
4. 허용되는 언어·사전 설정을 고정한다. 첫 실행과 반복 실행을 구분한다.
5. 파일 입력부터 평가하고 마이크 입력은 별도 세션으로 진행한다.

## 시간 기록

| 시점 | 파일 입력 | 마이크 입력 |
|---|---|---|
| 시작 | 처리 요청 시각 | 처리 요청과 실제 발화 시작을 각각 기록 |
| 첫 출력 | 첫 텍스트 표시 | 발화 시작 이후 첫 텍스트 표시 |
| 마지막 출력 | 마지막 텍스트 표시 | 발화 종료와 마지막 표시를 각각 기록 |
| 최종 확정 | 수정이 끝난 시각 | 해당 발화 결과가 안정된 시각 |

도구가 확정 이벤트를 제공하지 않으면 관찰 종료 기준을 사전에 정하고 ‘관찰 기준 확정’으로 표시한다. 마이크 관찰 시간에는 실제 발화 시간도 들어가므로 파일 처리 시간과 직접 비교하지 않는다.

```text
run_id, input_mode, audio_duration_s, chip, macOS, app_version,
model, language_setting, dictionary_setting, cold_or_warm,
request_time, speech_start, speech_end, first_text_time,
last_text_time, stable_time, revision_count, errors, memory
```

## 첫 실험 완료 기준

- [ ] 동일 파일로 반복 가능한 입력을 확보했다.
- [ ] 첫 출력과 확정을 분리해 기록했다.
- [ ] 오인식·누락·문장 분리를 정답과 비교했다.
- [ ] 지원하지 않는 측정 항목은 0 대신 ‘측정 불가’로 남겼다.

## 다음 학습

[[tech/ai/apple-neural-engine-asr/04-learning/02-deep-dive|심화 측정]] · [[tech/ai/apple-neural-engine-asr/README|학습 진입점]]

## Sources

- 사용자 제공 dossier: Lightning-SimulWhisper 소개 영상의 수집 요약. 원본 영상·공식 저장소 URL 미제공이며, 구현과 성능 수치를 독립 검증하지 않았다.
- Apple Core ML 공식 배경 문서: https://developer.apple.com/documentation/coreml — Apple 기기의 모델 실행 개념 참고용. 이 도구가 Core ML을 사용한다는 증거는 아니다.
- Apple MLComputeUnits 공식 배경 문서: https://developer.apple.com/documentation/coreml/mlcomputeunits — 실행 장치 선택 개념 참고용. 이 도구의 실제 연산 배치를 증명하지 않는다.
