---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: 전사와 화자 구분 분리하기

## 준비

제품 설치 안내가 아닌 개념 실습이다. 실제 개인 음성 대신 가상의 대화와 수동 label을 사용한다. 아래 결과는 모델 추론값이 아니다.

## 1. 발화 구간 표현

```json
[
  {"meeting_id":"m1","segment_id":"s1","start":0.0,"end":2.0,"text":"일정을 확인하겠습니다.","speaker_id":"A"},
  {"meeting_id":"m1","segment_id":"s2","start":2.2,"end":4.0,"text":"금요일이 좋겠습니다.","speaker_id":"B"},
  {"meeting_id":"m2","segment_id":"s3","start":0.0,"end":1.5,"text":"다시 검토하겠습니다.","speaker_id":"A"}
]
```

`start`와 `end`는 회의 시작 기준 초 단위다. 텍스트를 유지한 채 `s2`의 화자를 A로 바꿔 보자. 전사는 그대로여도 귀속이 틀릴 수 있다.

## 2. 회의 내부 ID 범위 확인

| 회의·화자 키 | 가정한 사람 | 지속 프로필 |
|---|---|---|
| `(m1, A)` | 가상 인물 1 | p1 |
| `(m1, B)` | 가상 인물 2 | 미확정 |
| `(m2, A)` | 가상 인물 3 | 미확정 |

`A`만으로 join하면 서로 다른 사람이 합쳐진다. 회의 내부 키는 `(meeting_id, speaker_id)`로 취급한다. `profile_id`는 별도 공간에서 관리한다.

## 3. 연결 보류 비교

- 미확정 화자를 p1에 강제로 연결한 결과와 `profile_id: null`로 보류한 결과를 비교한다.
- 어느 기록이 어떤 근거로 연결되었는지 적는다.
- 이름이 없다는 사실과 연결이 불확실하다는 사실을 구분한다.

## 4. 데이터 종류 구분

오디오, 전사문, 화자 label, 프로필 연결을 각각 나열하고 저장 위치·보존 기간을 별도 열에 적는다. Sokki의 확인된 설명과 Damso의 미확인 항목을 구분한다. 모르는 값은 “미확인”으로 남긴다.

## 완료 기준

- [ ] 전사 오류와 화자 귀속 오류를 별도로 설명할 수 있다.
- [ ] 같은 label이 다른 회의에서 동일인을 뜻하지 않음을 재현했다.
- [ ] 불확실한 연결을 보류했다.

[[tech/ai/speaker-diarization-profile-accumulation/04-learning/02-deep-dive|다음: 누적과 복구]] · [[tech/ai/speaker-diarization-profile-accumulation/README|학습 경로]]

## Sources

- 사용자 제공 dossier: Sokki·Damso 소개 내용 및 README 설명 요약. 원문 URL과 조회일은 제공되지 않았다. 이 노트의 제품 관련 사실은 해당 요약 범위에 한정한다.
- 보충 학습: OpenAI Whisper 공식 저장소 — https://github.com/openai/whisper (일반 ASR 학습용이며 Damso의 사용 기술을 입증하지 않는다.)
- 보충 학습: SQLite Foreign Key 문서 — https://www.sqlite.org/foreignkeys.html (실습 schema 참고용이며 Damso의 DB를 입증하지 않는다.)
