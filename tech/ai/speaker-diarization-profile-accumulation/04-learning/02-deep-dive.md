---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: 출처를 보존하는 누적 구조

## 설계 원칙

아래 구조는 학습용 제안이며 Damso의 실제 구현이 아니다.

| 쟁점 | 구분 | 목적 |
|---|---|---|
| 식별자 | 회의 내부 speaker_id / 지속 profile_id | 임시 번호의 영구 식별자 오인 방지 |
| 연결 상태 | 미확정 / 자동 연결 / 사용자 확인 | 판단 상태와 확인 주체 보존 |
| 출처 | 회의·구간·연결 판단 | 오류 추적과 영향 범위 파악 |
| 변경 이력 | 연결 취소·병합·분리 | 사후 복구 |
| 보존 범위 | 오디오·전사문·화자 정보·프로필 | 저장·삭제 범위 정의 |

## 개념 schema

```text
meetings(id)
segments(id, meeting_id, start, end, text, speaker_id)
profiles(id)
speaker_profile_links(id, meeting_id, speaker_id, profile_id?, status, evidence)
link_history(id, link_id, before, after, actor, reason, changed_at)
```

이는 실행 가능한 DDL이 아니다. 구현 시 회의 내부 화자 키, 참조 무결성, 상태 제약과 이력 변경의 원자성을 정의해야 한다. SQLite는 실습용 선택지다. SQLite 사용이 자료에서 확인된 제품은 Sokki뿐이다.

## 상태와 수정

```text
미확정 → 자동 연결 → 사용자 확인
미확정 ─────────→ 사용자 확인
자동 연결 / 사용자 확인 → 연결 취소 → 미확정
```

자동 연결은 사용자 확인과 동등하지 않다. `evidence`에는 판단 근거의 출처를 남기고, 상태만 바꿔 과거 판단을 덮어쓰지 않는다. 취소 때도 이전 대상·수정 주체·이유를 이력에 남긴다. 구체적 confidence 계산법이나 임계값은 자료에 없다.

## 오류를 나누어 실습

| 오류 | 회의 내부 영향 | 누적 시 영향 |
|---|---|---|
| 다른 화자를 하나로 묶음 | 발언 귀속 혼합 | 다른 사람의 기록이 같은 프로필에 축적될 수 있음 |
| 같은 화자를 여러 명으로 나눔 | 발언 흐름 분산 | 같은 사람의 정보가 여러 프로필에 분산될 수 있음 |
| 내부 분리는 맞지만 프로필 연결이 틀림 | 회의 label은 유지 가능 | 지속 프로필의 기록 오염 |

1. 잘못된 링크 하나를 만들고 연결된 회의·구간을 조회한다.
2. 링크를 취소하거나 다른 프로필로 옮기고 before/after를 남긴다.
3. 두 프로필을 병합한 뒤 원래 링크의 출처를 이용해 다시 분리한다.
4. 원본 회의 삭제 시 파생 정보·근거·이력 중 무엇을 지우거나 익명화할지 정책을 정한다.

병합 후 원래 출처가 사라지면 분리를 복구하기 어렵다. 반대로 삭제된 개인정보를 이력에 무조건 남겨서도 안 된다. 추적성과 삭제 요구를 함께 만족하는 정책을 실습에서 명시한다.

## 승인 경계

녹음 시작 승인과 프로필 생성·연결·보존은 별도 제어 지점이다. Damso의 녹음 전 질문만으로 나머지 단계의 정책을 판단할 수 없다.

[[tech/ai/speaker-diarization-profile-accumulation/05-projects|프로젝트로 적용]] · [[tech/ai/speaker-diarization-profile-accumulation/README|학습 경로]]

## Sources

- 사용자 제공 dossier: Sokki·Damso 소개 내용 및 README 설명 요약. 원문 URL과 조회일은 제공되지 않았다. 이 노트의 제품 관련 사실은 해당 요약 범위에 한정한다.
- 보충 학습: OpenAI Whisper 공식 저장소 — https://github.com/openai/whisper (일반 ASR 학습용이며 Damso의 사용 기술을 입증하지 않는다.)
- 보충 학습: SQLite Foreign Key 문서 — https://www.sqlite.org/foreignkeys.html (실습 schema 참고용이며 Damso의 DB를 입증하지 않는다.)
