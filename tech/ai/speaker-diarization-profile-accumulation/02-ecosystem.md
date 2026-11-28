---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem: 제품 소개와 설계 접근 비교

## 비교 범위

제공 자료에는 외부 경쟁 제품이나 benchmark가 없다. 제품 소개와 개념적 설계 접근만 비교한다. “언급 없음”은 기능이 없다는 뜻이 아니다.

| 대상·접근 | 주된 목적 | 화자 처리 | 누적 프로필 | 판단 가능한 범위 |
|---|---|---|---|---|
| Sokki | 음성의 텍스트 입력 | 언급 없음 | 언급 없음 | 기기 내 인식·Whisper·로컬 SQLite·오디오 외부 미전송 |
| Damso | 회의 기록 | 화자 분리 소개 | 기능 소개 | 녹음 전 질문 동작 소개 |
| 회의 내부 분리 설계 | 한 회의의 발언 귀속 | 회의별 구분 | 지속 프로필 없음 | 특정 제품이 아닌 개념 비교 |
| 지속 프로필 연결 설계 | 기록 간 정보 축적 | 내부 구분과 별도 연결 | 회의 간 연결 설계 가능 | Damso가 이 방식인지는 불명 |

## 선택 기준

- 받아쓰기 중심: 입력 흐름과 전사 결과를 우선 검토한다.
- 회의별 발언 귀속: 화자 교정과 회의 내부 label의 일관성을 검토한다.
- 기록 간 누적: 연결 보류·출처 추적·연결 취소·병합 후 분리를 함께 검토한다.

제품 간 정확도, 지연, 비용, 지원 언어, 처리 규모의 우열은 이 자료만으로 판단할 수 없다. 한국어 인식 텍스트가 표시된다는 관찰도 전체 지원 언어 목록을 뜻하지 않는다. Whisper는 Sokki의 ASR 요소로 언급되며 Damso의 diarization 기술로 제시되지 않았다.

## 이어 읽기

[[tech/ai/speaker-diarization-profile-accumulation/03-references|근거와 확인 질문]] · [[tech/ai/speaker-diarization-profile-accumulation/README|학습 경로]]

## Sources

- 사용자 제공 dossier: Sokki·Damso 소개 내용 및 README 설명 요약. 원문 URL과 조회일은 제공되지 않았다. 이 노트의 제품 관련 사실은 해당 요약 범위에 한정한다.
- 보충 학습: OpenAI Whisper 공식 저장소 — https://github.com/openai/whisper (일반 ASR 학습용이며 Damso의 사용 기술을 입증하지 않는다.)
- 보충 학습: SQLite Foreign Key 문서 — https://www.sqlite.org/foreignkeys.html (실습 schema 참고용이며 Damso의 DB를 입증하지 않는다.)
