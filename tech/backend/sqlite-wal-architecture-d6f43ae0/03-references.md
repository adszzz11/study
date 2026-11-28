---
date: 2026-11-23
tags: [tech]
type: tech-tool-study
status: draft
---

# References와 근거 범위

## 주 출처

- SQLite 공식 Write-Ahead Logging 문서: https://www.sqlite.org/wal.html
- 작성 근거는 사용자가 제공한 dossier이며, 원문 전체나 현재 최신 구현을 별도로 검증한 결과는 아니다.

## 읽기 안내

| 주제 | 원문에서 확인할 내용 | 연결 노트 |
|---|---|---|
| 개요·장단점 | WAL/rollback 흐름과 제약 | [[tech/backend/sqlite-wal-architecture-d6f43ae0/01-overview|Overview]] |
| 동작 원리 | end mark, wal-index, 단일 writer | [[tech/backend/sqlite-wal-architecture-d6f43ae0/04-learning/02-deep-dive|심화]] |
| Checkpoint | 자동 임계값, 진행 제한, 재사용 | [[tech/backend/sqlite-wal-architecture-d6f43ae0/cheatsheet|Cheatsheet]] |
| 설정과 파일 | WAL 활성화, 지속성, WAL 수명 | [[tech/backend/sqlite-wal-architecture-d6f43ae0/04-learning/01-getting-started|시작하기]] |

## 버전과 해석 주의

- WAL 도입: SQLite 3.7.0.
- 대용량 transaction 개선: 3.11.0. 초기 용량 경고를 현재 제한으로 일반화하지 않는다.
- read-only WAL의 조건부 지원: 3.22.0.
- 기본 checkpoint는 1000 **pages**다. 약 4MB라는 설명은 page 크기에 의존한다.

## 확인하지 못한 내용

dossier는 §6 checkpoint starvation 설명 도중 끝난다. shared-memory 예외 구현, `SQLITE_BUSY` 상세 조건, WAL-reset bug의 원인·영향·수정 버전은 이 자료만으로 판단하지 않는다. 관련 항목은 원문과 사용 중인 SQLite 버전의 추가 자료를 확인해야 한다.

## 돌아가기

[[tech/backend/sqlite-wal-architecture-d6f43ae0/README|학습 경로]]

## Sources

- https://www.sqlite.org/wal.html — 제공된 dossier의 본문 범위(§6 checkpoint starvation 설명 도중까지)를 근거로 정리.
