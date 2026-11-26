---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet: 실시간 ASR 평가

## 빠른 구분

| 질문 | 확인할 항목 |
|---|---|
| 계산이 빨라졌나? | 동일 조건 처리 시간, RTF, 계측 가능한 단계 시간 |
| 결과가 빨리 보이나? | 최초 출력 지연 |
| 결과가 안정적인가? | 확정 지연, 수정 빈도, CER·누락 |
| 오래 말해도 따라오나? | 구간별 지연·미처리량 추이 |
| 외부 전송을 피하나? | 관찰 범위의 네트워크 활동과 데이터 흐름 |

## 실험 전 체크

- [ ] Mac·칩·메모리·OS·앱·모델 버전 기록
- [ ] 파일 입력과 마이크 입력 분리
- [ ] 같은 음성·정답·언어·사전 설정 유지
- [ ] 첫 실행과 이후 실행 분리
- [ ] 첫 출력·마지막 출력·확정 시각 구분
- [ ] 확정 이벤트가 없으면 관찰 기준 명시
- [ ] 미지원 계측은 ‘측정 불가’로 표시

```text
RTF = 파일 처리 경과 시간 / 음성 길이
CER = (대치 + 삭제 + 삽입 문자 수) / 정답 문자 수
speedup = 동일 조건 기준 시간 / 가속 시간
```

## 해석 규칙

- 최대 18배·15배는 미검증 단계별 주장이다. 곱하기·평균·전체 속도로 환산하지 않는다.
- Neural Engine 실행 비율, CPU/GPU 분담, 모델 정밀도는 미확인이다.
- ‘소리 분석·텍스트 변환’을 특정 encoder/decoder 구조로 단정하지 않는다.
- 한국어 지원과 전문용어 정확도는 별개다. tiny~large의 성능 차이는 직접 측정한다.
- 로컬 음성 처리 설명은 앱 전체의 무통신·로그 미저장 보장이 아니다.
- 공식 배포처·라이선스·설치 명령·지원 OS/칩은 원문 확보 후 확인한다.

## 바로 이동

[[tech/ai/apple-neural-engine-asr/README|학습 진입점]] · [[tech/ai/apple-neural-engine-asr/03-references|근거 수준]] · [[tech/ai/apple-neural-engine-asr/04-learning/01-getting-started|첫 실험]]

## Sources

- 사용자 제공 dossier: Lightning-SimulWhisper 소개 영상의 수집 요약. 원본 영상·공식 저장소 URL 미제공이며, 구현과 성능 수치를 독립 검증하지 않았다.
- Apple Core ML 공식 배경 문서: https://developer.apple.com/documentation/coreml — Apple 기기의 모델 실행 개념 참고용. 이 도구가 Core ML을 사용한다는 증거는 아니다.
- Apple MLComputeUnits 공식 배경 문서: https://developer.apple.com/documentation/coreml/mlcomputeunits — 실행 장치 선택 개념 참고용. 이 도구의 실제 연산 배치를 증명하지 않는다.
