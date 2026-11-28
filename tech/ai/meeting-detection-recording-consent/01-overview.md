---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview — 회의 감지와 녹음 전 승인

## What

회의 감지 결과를 곧바로 녹음 명령으로 사용하지 않고, 사용자에게 시작 여부를 묻는 흐름이다. Damso 설명에서 확인되는 순서는 다음뿐이다.

```text
회의 감지 → 사용자에게 녹음 여부 질문 → [이후 처리는 자료에 구체적으로 설명되지 않음]
```

승인 후 녹음을 시작한다는 해석은 자연스럽지만, 승인·거부·무응답별 실제 처리는 확인되지 않는다.

## Why

자동 감지는 사용자의 수동 실행 부담을 줄일 수 있다. 승인 단계는 감지 오판과 원치 않는 기록을 걸러내는 사용자 통제 지점이 된다. 이는 설계상 이점이며 실제 오탐률이나 UX 개선 수치가 제시된 것은 아니다.

## 특징과 확인 범위

| 구성 요소 | dossier에서 소개된 내용 | 확인되지 않은 항목 |
|---|---|---|
| Meeting detection | Damso의 회의 감지 후 질문 | 입력 신호, 알고리즘, 지원 앱, 정확도 |
| Pre-recording prompt | 녹음 전 사용자 질문 | UI, timeout, 기본값, 재질문 정책 |
| Recording lifecycle | 질문이 녹음 시작보다 앞섬 | 시작·중지 조건, 중복 방지, 장애 복구 |
| Speaker diarization | Damso의 화자 분리 | 모델, 처리 위치, 정확도 |
| 누적 화자 프로필 | Damso의 누적 프로필 기능 | 식별 방식, 보존, 삭제·수정 정책 |
| Local processing/storage | Sokki의 기기 내 인식·Whisper, SQLite, 오디오 외부 미전송 설명 | Damso에도 적용되는지 여부 |

## 제안 아키텍처

아래 모델은 학습을 위한 제안이며 Damso의 내부 구조가 아니다.

```text
Idle → MeetingCandidate → AwaitingApproval
                              ├─ 승인 → Recording
                              ├─ 거부 → Dismissed
                              └─ 무응답 → 녹음 시작 보류
```

- 감지 이벤트는 후보만 생성한다. Recorder는 별도 승인 결과를 요구한다.
- 질문 표시와 승인 완료는 서로 다른 사건이다.
- 승인은 meeting/session ID와 녹음 범위에 연결하고 다른 세션으로 재사용하지 않는다.
- 사용자 승인과 참석자 고지·동의·철회는 별도 요구사항이다. 자료로 참석자 동의 절차나 법적 충족 여부를 판단할 수 없다.
- 감지 단계가 마이크나 시스템 오디오를 사용하는지 불명이다. 입력 접근과 녹음 저장을 따로 확인해야 한다.

## 다음 학습

[[tech/ai/meeting-detection-recording-consent/02-ecosystem|비교]] → [[tech/ai/meeting-detection-recording-consent/04-learning/01-getting-started|mock 실습]] · [[tech/ai/meeting-detection-recording-consent/README|진입점]]

## Sources

- 사용자 제공 dossier: Damso README 및 영상 요약에 관한 수집 설명, Sokki README에 관한 수집 설명.
- **출처 URL: 제공되지 않음.** 원문 README와 영상 URL을 확인할 수 없어 링크를 기재하지 않았다. 이 노트는 원문을 직접 검증한 결과가 아니다.
- 상태 모델·실습·프로젝트는 dossier에 근거한 **설계 제안**이며, Damso의 실제 구현이나 검증된 성능을 뜻하지 않는다.
