---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview: 화자 분리와 프로필 누적

## What

| 기능 | 질문 | 결과 예시 | 의미의 경계 |
|---|---|---|---|
| Speech Recognition / ASR | 무슨 말을 했는가? | 전사문 | 화자 귀속의 정확성을 보장하지 않음 |
| Speaker Diarization | 어느 화자의 발화인가? | 구간별 speaker label | 실명 확인과 다름 |
| 지속 프로필 연결 | 기존 어떤 프로필과 연결하는가? | profile link | 회의 내부 분리와 별도 판단 |

화자 구분, 동일 화자 연결, 실명 확인은 서로 다른 기능이다. 화자 관련 정보의 누적이 반드시 여러 회의에 걸친 동일인 연결을 뜻하는 것도 아니다.

## Why

전사문이 정확해도 화자가 틀리면 발언 귀속이 잘못된다. 회의 내부 오류가 지속 프로필에 들어가면 후속 기록에도 잘못된 정보가 이어질 수 있다. 누적에서는 정보량뿐 아니라 연결 근거와 수정 가능성이 중요하다.

## 특징과 개념적 구조

다음은 **학습용 모델이며 Damso의 실제 pipeline이 아니다.**

```text
발화 구간 → 회의 내부 화자 구분 → 화자 관련 정보 축적
                            ↓ 여러 회의에 걸친 지속 프로필을 설계한다면
                    기존 프로필과 연결 판단 → 확정 또는 보류
```

| 대상 | 자료에서 확인되는 기능 | 알 수 없는 내용 |
|---|---|---|
| Sokki | 텍스트 입력, 파형·경과 시간·한국어 인식 텍스트 표시 | 화자 분리 지원 여부 |
| Sokki | 기기 내 Speech Recognition·Whisper | 모델 버전·성능 |
| Sokki | 로컬 SQLite 기록 저장, 오디오 외부 미전송 | schema·암호화 |
| Damso | 회의 기록, 화자 분리, 누적 화자 프로필 | 내부 pipeline·누적 범위 |
| Damso | 회의 감지 뒤 녹음 전 사용자에게 질문 | 감지 기준·승인 UI 세부 동작 |

## 제어 지점

1. 회의를 감지한다.
2. 녹음 시작 여부를 묻는다.
3. 발화를 회의 내부 화자로 나눈다.
4. 지속 프로필을 사용하는 설계라면 기존 프로필 연결 여부를 판단한다.
5. 연결 결과의 보존·삭제를 관리한다.

자료에서 Damso의 동작으로 확인되는 것은 회의 감지 후 녹음 전 질문이다. 이 설명만으로 프로필 생성·갱신에 별도 확인이 있다고 판단할 수 없다. Sokki의 로컬 처리 설명도 Damso에 전이할 수 없다.

## 다음 학습

[[tech/ai/speaker-diarization-profile-accumulation/02-ecosystem|비교 읽기]] · [[tech/ai/speaker-diarization-profile-accumulation/README|학습 경로]]

## Sources

- 사용자 제공 dossier: Sokki·Damso 소개 내용 및 README 설명 요약. 원문 URL과 조회일은 제공되지 않았다. 이 노트의 제품 관련 사실은 해당 요약 범위에 한정한다.
- 보충 학습: OpenAI Whisper 공식 저장소 — https://github.com/openai/whisper (일반 ASR 학습용이며 Damso의 사용 기술을 입증하지 않는다.)
- 보충 학습: SQLite Foreign Key 문서 — https://www.sqlite.org/foreignkeys.html (실습 schema 참고용이며 Damso의 DB를 입증하지 않는다.)
