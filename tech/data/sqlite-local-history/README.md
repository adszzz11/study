---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# SQLite를 이용한 로컬 음성 인식 기록 저장

> **한 줄 정의**: 음성 인식으로 생성한 기록을 기기의 SQLite에 보관하는 방식으로, 수집 자료에서는 Sokki의 Mac 내 음성 처리 및 기록 저장 구조로 소개된다.

## Overview

Sokki는 음성을 텍스트로 입력하는 도구다. 사례의 핵심은 **기기 내 음성 처리와 로컬 기록 저장의 결합**이다. SQLite는 인식 엔진이 아니라 생성된 기록의 저장을 맡는다.

- 음성 인식과 Whisper는 기기에서 실행된다고 소개된다.
- 기록은 로컬 SQLite에 저장되며, 오디오는 Mac 밖으로 나가지 않는다고 설명된다.
- 받아쓰기 오버레이에는 파형, 경과 시간, 한국어 인식 텍스트가 보인다.
- schema, 저장 파일 경로, 저장 범위, 암호화, 백업, 보관 정책, 텍스트 전송 여부는 미확인이다.

```text
음성 입력 → 기기 내 음성 인식·Whisper → 인식 텍스트 표시
                                     → 기록의 로컬 SQLite 저장
```

이는 개념적 관계이며 실제 내부 호출 순서나 저장 시점을 뜻하지 않는다. 아래 실습의 SQL과 정책은 학습용 제안이며 Sokki 구현을 재현한 것이 아니다.

## Learning Path

- [ ] [[tech/data/sqlite-local-history/01-overview|Overview — 역할과 경계]]
- [ ] [[tech/data/sqlite-local-history/02-ecosystem|Ecosystem — Sokki와 Damso 비교]]
- [ ] [[tech/data/sqlite-local-history/03-references|References — 근거와 보충 문서]]
- [ ] [[tech/data/sqlite-local-history/04-learning/01-getting-started|시작하기 — 최소 기록 저장]]
- [ ] [[tech/data/sqlite-local-history/04-learning/02-deep-dive|심화 — 저장 정책과 생애주기]]
- [ ] [[tech/data/sqlite-local-history/05-projects|Projects — 적용 실습]]
- [ ] [[tech/data/sqlite-local-history/cheatsheet|Cheatsheet — 명령과 점검표]]

## When To Use

- 받아쓰기 결과를 기기에 남기고 재실행 뒤에도 조회하려는 경우
- 음성 인식 처리와 기록 저장의 책임을 분리해 설계할 때
- 처리·저장·전송 경계를 데이터 종류별로 검토할 때

## When Not To Use

- 이 사례만으로 모든 기능의 offline 동작이나 네트워크 미사용을 보장해야 하는 경우
- 로컬 저장만으로 암호화·백업·안전한 삭제가 충족된다고 판단하려는 경우
- 여러 기기 동기화나 서버 공동 편집이 필요하지만 관련 설계를 아직 하지 않은 경우

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Data]]
- [[tech/data/sqlite-local-history/01-overview|음성 처리와 로컬 저장의 경계]]
- [[tech/data/sqlite-local-history/04-learning/02-deep-dive|SQLite 기록 정책 설계]]

필수 MOC 링크의 대상은 현재 빈 작업 폴더에서 확인할 수 없다. MOC 파일은 생성하거나 수정하지 않는다.

## Sources

- 제공 dossier: Sokki·Damso 소개 내용과 화면 관찰. 원자료 URL 미제공으로 제품 관련 주장의 외부 검증은 제한된다.
- SQLite 공식 소개(보충): https://www.sqlite.org/about.html
- SQLite SQL 문서(실습 참고): https://www.sqlite.org/lang.html
