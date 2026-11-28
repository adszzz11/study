---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# 화자 분리와 누적 화자 프로필의 구조 및 설계 쟁점

> **한 줄 정의**: Speaker Diarization은 발화 구간을 화자별로 구분하고, 화자 프로필 누적은 화자 관련 정보를 지속적으로 축적하는 기능이다. Damso의 누적 범위와 구현 방식은 제공 자료로 확인되지 않는다.

## Overview

Speech Recognition은 “무슨 말을 했는가”, Speaker Diarization은 “어느 화자의 발화인가”를 다룬다. 회의 기록에서는 두 결과가 함께 있어야 발언의 귀속과 대화 흐름을 파악하기 쉽다.

이 학습 묶음은 회의 내부 화자 구분과 지속 프로필 연결의 경계를 살핀다. 한 회의의 `Speaker A`를 다른 회의의 같은 label과 동일인으로 단정하면 안 된다.

| 근거 수준 | 내용 |
|---|---|
| 자료에서 확인 | Damso의 회의 기록·화자 분리·누적 화자 프로필 소개, 회의 감지 후 녹음 전 사용자 질문 |
| Sokki에 한정 | 기기 내 Speech Recognition·Whisper, 로컬 SQLite 기록 저장, 오디오의 Mac 외부 미전송 |
| 확인 불가 | Damso의 모델·DB·처리 위치·프로필 구성·정확도·보존 정책·회의 간 연결 방식 |
| 학습용 제안 | ID 분리, 연결 보류, 출처 보존, 병합·분리·복구 구조 |

## Learning Path

- [ ] [[tech/ai/speaker-diarization-profile-accumulation/01-overview|Overview]] — 정의, 배경과 근거 범위
- [ ] [[tech/ai/speaker-diarization-profile-accumulation/02-ecosystem|Ecosystem]] — 제품 소개와 설계 접근 비교
- [ ] [[tech/ai/speaker-diarization-profile-accumulation/03-references|References]] — 출처의 한계와 추가 확인 질문
- [ ] [[tech/ai/speaker-diarization-profile-accumulation/04-learning/01-getting-started|시작하기]] — 발화 구간과 회의 내부 ID 실습
- [ ] [[tech/ai/speaker-diarization-profile-accumulation/04-learning/02-deep-dive|Deep Dive]] — 연결 상태, 출처와 복구 설계
- [ ] [[tech/ai/speaker-diarization-profile-accumulation/05-projects|Projects]] — 교정 도구와 검증 시나리오
- [ ] [[tech/ai/speaker-diarization-profile-accumulation/cheatsheet|Cheatsheet]] — 설계 검토용 빠른 참조

## When To Use

- 회의 전사문에 화자별 발언 귀속을 표현할 때.
- 여러 기록의 화자 정보를 축적하는 기능을 설계하거나 평가할 때.
- 잘못된 연결의 영향 범위와 복구 방법을 검토할 때.

## When Not To Use

- 화자를 구분할 필요 없이 텍스트 입력만 필요할 때는 받아쓰기 도구부터 검토한다.
- 실명 인증이 필요할 때 화자 clustering 결과만으로 신원을 확정하지 않는다.
- Damso의 정확도·비용·보안·배포 적합성을 확정하는 자료로 사용하기에는 근거가 부족하다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/speaker-diarization-profile-accumulation/01-overview|관련 tech 노트: 화자 분리 개요]]
- 기존 vault가 제공되지 않아 다른 관련 tech 노트의 존재는 확인하지 못했다. 위 관련 tech 노트는 이 묶음에서 생성한다.

## Sources

- 사용자 제공 dossier: Sokki·Damso 소개 내용 및 README 설명 요약. 원문 URL과 조회일은 제공되지 않았다. 이 노트의 제품 관련 사실은 해당 요약 범위에 한정한다.
- 보충 학습: OpenAI Whisper 공식 저장소 — https://github.com/openai/whisper (일반 ASR 학습용이며 Damso의 사용 기술을 입증하지 않는다.)
- 보충 학습: SQLite Foreign Key 문서 — https://www.sqlite.org/foreignkeys.html (실습 schema 참고용이며 Damso의 DB를 입증하지 않는다.)
