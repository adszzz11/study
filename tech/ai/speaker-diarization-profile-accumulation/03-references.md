---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# References: 근거 범위와 확인 질문

## 제공 자료

제품 관련 근거는 사용자 제공 dossier뿐이다. dossier가 인용한 Sokki·Damso README의 URL과 원문은 제공되지 않아 직접 대조하지 못했다. 제품 URL이나 benchmark를 추정하여 적지 않는다.

| 주장 | 근거 범위 | 읽는 방법 |
|---|---|---|
| Sokki의 로컬 처리·SQLite·오디오 외부 미전송 | dossier의 Sokki README 요약 | Sokki에만 한정 |
| Damso의 화자 분리·누적 프로필 | dossier의 기능 소개 | 구성·기간·동일인 연결은 미확인 |
| Damso의 녹음 전 질문 | dossier의 Damso README 요약 | 프로필 갱신 승인까지 의미하지 않음 |
| ID 분리·연결 이력 schema | dossier의 설계 제안 | 실제 구현으로 인용하지 않음 |

## 제품 검토 시 확인할 질문

- 프로필의 수명은 한 회의인가, 여러 회의인가?
- 이름 등 사용자 입력 정보, 음성 특징, 과거 발언 중 무엇을 저장하는가?
- 자동 연결과 사용자 확인을 어떻게 구분하는가?
- 불확실한 연결을 보류할 수 있는가?
- 연결 취소·병합·분리와 변경 이력을 지원하는가?
- 오디오·전사문·화자 정보·프로필 각각의 처리 위치와 보존·삭제 범위는 무엇인가?
- 모델·정확도·지연·비용·지원 언어·규모에 대한 검증 자료가 있는가?

## 보충 문서 활용

Whisper 문서는 ASR의 역할을, SQLite 문서는 실습 저장소의 관계 무결성을 학습하는 데 사용한다. 두 문서는 Damso의 기술 선택에 대한 증거가 아니다. 링크 원문을 이번 작업에서 직접 검증하지는 않았다.

[[tech/ai/speaker-diarization-profile-accumulation/README|학습 경로]] · [[tech/ai/speaker-diarization-profile-accumulation/04-learning/01-getting-started|개념 실습]]

## Sources

- 사용자 제공 dossier: Sokki·Damso 소개 내용 및 README 설명 요약. 원문 URL과 조회일은 제공되지 않았다. 이 노트의 제품 관련 사실은 해당 요약 범위에 한정한다.
- 보충 학습: OpenAI Whisper 공식 저장소 — https://github.com/openai/whisper (일반 ASR 학습용이며 Damso의 사용 기술을 입증하지 않는다.)
- 보충 학습: SQLite Foreign Key 문서 — https://www.sqlite.org/foreignkeys.html (실습 schema 참고용이며 Damso의 DB를 입증하지 않는다.)
