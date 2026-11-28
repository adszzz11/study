---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects: 교정·누적·복구 실습

아래는 구현 제안이다. Damso의 기존 기능이나 공개 API로 해석하지 않는다. 가상 데이터로 시작한다.

## 1. 회의 기록의 화자 교정 도구

구간별 시각·텍스트·화자 label을 보여주고 수정 범위를 선택하게 한다.

- 한 구간의 화자만 변경.
- 회의 내부 같은 label 전체 변경.
- 회의 내부 화자의 지속 프로필 연결 변경.

**완료 기준:** 수정 전에 영향받는 구간·링크를 확인할 수 있고, 선택한 범위에만 적용되며 이전 연결을 복구할 수 있다. 구간 수정으로 화자 그룹이 달라지면 기존 프로필 연결의 재검토 필요 여부도 표시한다.

## 2. 출처를 보존하는 프로필 저장소

[[tech/ai/speaker-diarization-profile-accumulation/04-learning/02-deep-dive|개념 schema]]를 바탕으로 `meetings`, `segments`, `profiles`, `speaker_profile_links`, `link_history`를 구성한다. 프로필에 정보를 직접 덮어쓰기보다 원본 회의와 연결 판단에서 파생된 정보임을 추적한다.

**완료 기준:** 프로필에서 근거 회의로 역추적할 수 있고, 미확정 화자를 저장하며, 링크 변경과 이력을 함께 반영한다. SQLite는 실습 선택이며 Damso의 저장소라는 의미가 아니다.

## 3. 누적 오류 검증 시나리오

| 입력 상황 | 확인할 결과 |
|---|---|
| 새 화자 등장 | 기존 프로필에 강제로 연결하지 않고 보류 가능 |
| 같은 사람이 다른 회의에 등장 | 연결 판단의 근거와 상태를 보존 |
| 다른 사람을 같은 프로필에 연결 | 영향받은 기록을 찾아 분리 가능 |
| 같은 사람을 여러 프로필로 분할 | 원래 출처를 보존하며 병합 가능 |
| 병합 후 다시 분리 | 이전 링크를 바탕으로 복구 가능 |
| 원본 기록 삭제 | 정한 정책대로 파생 정보와 근거 처리 |

**완료 기준:** 프로필 개수 증가가 아니라 오류 발견·영향 조회·수정·복구를 입증한다. 각 시나리오의 예상 결과와 실제 결과를 나란히 기록한다. 제품 benchmark나 정확도 수치로 제시하지 않는다.

## 결과물

- 가상 회의 fixture와 예상 화자·프로필 연결.
- 수정 전후 화면 또는 데이터 diff.
- 연결 이력과 삭제 정책, 남은 불확실성 목록.

[[tech/ai/speaker-diarization-profile-accumulation/cheatsheet|검토 체크리스트]] · [[tech/ai/speaker-diarization-profile-accumulation/README|학습 경로]]

## Sources

- 사용자 제공 dossier: Sokki·Damso 소개 내용 및 README 설명 요약. 원문 URL과 조회일은 제공되지 않았다. 이 노트의 제품 관련 사실은 해당 요약 범위에 한정한다.
- 보충 학습: OpenAI Whisper 공식 저장소 — https://github.com/openai/whisper (일반 ASR 학습용이며 Damso의 사용 기술을 입증하지 않는다.)
- 보충 학습: SQLite Foreign Key 문서 — https://www.sqlite.org/foreignkeys.html (실습 schema 참고용이며 Damso의 DB를 입증하지 않는다.)
