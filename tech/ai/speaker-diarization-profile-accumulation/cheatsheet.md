---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet: 화자 분리와 프로필 누적

## 세 가지 질문

| 질문 | 기능 | 주의 |
|---|---|---|
| 무슨 말을 했는가? | ASR | 전사가 맞아도 화자는 틀릴 수 있음 |
| 어느 화자의 발화인가? | Diarization | label은 실명이 아님 |
| 기존 누구의 기록과 연결하는가? | Profile linking | 회의 내부 분리와 별도 판단 |

```text
회의 내부 키 = (meeting_id, speaker_id)
지속 프로필 키 = profile_id
같은 label ≠ 같은 사람
녹음 승인 ≠ 프로필 연결·보존 정책 확인
```

## 사실과 미확인 사항

- **Sokki만 확인:** 기기 내 Speech Recognition·Whisper, 로컬 SQLite 기록, 오디오의 Mac 외부 미전송.
- **Damso 소개:** 회의 기록·화자 분리·누적 프로필, 회의 감지 후 녹음 전 질문.
- **Damso 미확인:** 모델·DB·처리 위치·음성 특징 저장·누적 범위·회의 간 연결·정확도·보존 정책.
- **설계 제안:** ID 분리, 연결 상태, 출처 보존, 병합·분리·취소 이력.

## 설계 검토 체크리스트

- [ ] speaker_id와 profile_id를 분리했는가?
- [ ] 미확정·자동 연결·사용자 확인을 구분했는가?
- [ ] 연결 근거를 회의·구간까지 추적할 수 있는가?
- [ ] 한 구간 수정과 회의 전체 수정, 프로필 연결 수정을 구분했는가?
- [ ] 잘못된 병합을 분리하고 연결을 취소할 수 있는가?
- [ ] 오디오·전사문·화자 정보·프로필의 저장·삭제 범위를 정했는가?
- [ ] 녹음 승인과 프로필 생성·갱신 제어를 별도로 검토했는가?

## 피해야 할 해석

| 잘못된 추론 | 올바른 처리 |
|---|---|
| Sokki가 로컬이므로 Damso도 로컬 | 제품별로 근거 확인 |
| Whisper가 Damso의 화자 분리 모델 | 자료에는 그런 근거 없음 |
| 누적 프로필이므로 반드시 회의 간 동일인 연결 | 누적 범위부터 확인 |
| 모든 화자를 기존 프로필에 연결 | 불확실하면 보류 |

[[tech/ai/speaker-diarization-profile-accumulation/README|전체 학습 경로]] · [[tech/ai/speaker-diarization-profile-accumulation/05-projects|검증 프로젝트]]

## Sources

- 사용자 제공 dossier: Sokki·Damso 소개 내용 및 README 설명 요약. 원문 URL과 조회일은 제공되지 않았다. 이 노트의 제품 관련 사실은 해당 요약 범위에 한정한다.
- 보충 학습: OpenAI Whisper 공식 저장소 — https://github.com/openai/whisper (일반 ASR 학습용이며 Damso의 사용 기술을 입증하지 않는다.)
- 보충 학습: SQLite Foreign Key 문서 — https://www.sqlite.org/foreignkeys.html (실습 schema 참고용이며 Damso의 DB를 입증하지 않는다.)
