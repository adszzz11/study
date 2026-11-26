---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects — 적용 과제

아래는 dossier를 바탕으로 제안하는 학습 프로젝트다. Damso 기능의 구현 사실이나 성능 보장이 아니다.

## 1. 녹음 전 승인 gate prototype

- **구성:** 가상 회의 이벤트, 승인 UI, mock recorder, 상태 전이 로그.
- **입력:** 승인·거부·무응답·회의 종료·반복 감지·늦은 승인.
- **산출물:** 상태도와 session/request ID를 포함한 이벤트 기록.
- **완료 기준:** 승인 없는 시작 0회, 같은 회의 중복 시작 0회, 종료 후 승인 무효화. 실제 오디오 수집 없이 검증한다.

## 2. 감지 품질과 승인 경험 평가 도구

- **구성:** 감지 횟수, 승인·거부, 반복 질문 횟수, 승인 소요 시간의 집계.
- **산출물:** 지표 정의표와 mock 데이터 기반 보고서.
- **완료 기준:** 거부와 오탐을 구분한다. 오탐 지표는 독립적인 회의 여부 ground truth가 있을 때만 계산한다.
- **주의:** 거부 이유는 회의가 아님, 기록 원치 않음 등으로 다를 수 있다. 거부율을 감지 정확도로 표현하지 않는다.

## 3. 회의 기록 데이터 lifecycle 설계

- **구성:** 원본 오디오, transcript, diarization 결과, 누적 speaker profile의 데이터 지도.
- **산출물:** 생성·처리·보관·삭제 정책표와 회의/프로필 연결도.
- **완료 기준:** 각 데이터의 보관 기간·삭제 범위를 명시하고, 회의 삭제가 여러 회의에 걸친 누적 프로필에 미치는 영향을 결정한다.
- **주의:** 자료는 누적 프로필 기능의 존재만 소개한다. 삭제 전파와 보존 정책은 새롭게 정할 요구사항이다.

## 구현 전 확인

참석자 고지·동의와 철회 요구사항, 감지 입력의 접근 권한, 실제 recorder 시작·중지·실패 처리를 정한 뒤 오디오 실습으로 확장한다.

## 연결

[[tech/ai/meeting-detection-recording-consent/04-learning/01-getting-started|mock 실습]] · [[tech/ai/meeting-detection-recording-consent/04-learning/02-deep-dive|심화 설계]] · [[tech/ai/meeting-detection-recording-consent/README|진입점]]

## Sources

- 사용자 제공 dossier: Damso README 및 영상 요약에 관한 수집 설명, Sokki README에 관한 수집 설명.
- **출처 URL: 제공되지 않음.** 원문 README와 영상 URL을 확인할 수 없어 링크를 기재하지 않았다. 이 노트는 원문을 직접 검증한 결과가 아니다.
- 상태 모델·실습·프로젝트는 dossier에 근거한 **설계 제안**이며, Damso의 실제 구현이나 검증된 성능을 뜻하지 않는다.
