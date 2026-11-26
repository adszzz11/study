---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# References

## 원자료의 한계

제공 dossier에는 Sokki README의 설명과 영상 관찰 내용이 요약되어 있지만 URL이 없다. 제품 저장소나 영상 주소를 추측해 넣지 않는다. 아래 공식 문서는 SQLite 일반 개념과 실습을 위한 보충 자료이며 Sokki·Damso의 동작을 검증하는 출처가 아니다.

| 근거 | 뒷받침하는 내용 | 뒷받침하지 않는 내용 |
|---|---|---|
| Sokki README에 관한 dossier 설명 | 기기 내 음성 인식·Whisper, 로컬 SQLite 기록, 오디오 외부 미전송 | 암호화, 텍스트 전송 여부, 백업 |
| 영상 관찰 요약 | 오버레이의 파형·시간·한국어 텍스트, 배경 앱 | DB 저장 컬럼, 공식 앱 연동 |
| Damso 소개 요약 | 화자 분리, 누적 화자 프로필, 녹음 전 질문 | SQLite 사용, 내부 schema |

## 권장 읽기 순서

1. SQLite 소개로 embedded database의 역할을 이해한다.
2. CLI 문서와 CREATE TABLE·INSERT·SELECT 문서로 최소 실습을 진행한다.
3. transaction과 backup 문서로 실패·보관 정책을 검토한다.

## 관련 노트

[[tech/data/sqlite-local-history/04-learning/01-getting-started|SQL 시작하기]] · [[tech/data/sqlite-local-history/README|학습 경로]]

## Sources

- 원자료: 제공 dossier. URL 미제공.
- SQLite 소개: https://www.sqlite.org/about.html
- CLI: https://www.sqlite.org/cli.html
- SQL 문법: https://www.sqlite.org/lang.html
- Transaction: https://www.sqlite.org/lang_transaction.html
- Backup API: https://www.sqlite.org/backup.html
