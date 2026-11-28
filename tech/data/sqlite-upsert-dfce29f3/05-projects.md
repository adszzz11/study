---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects

## 1. 단어 빈도 적재기

- 목표: 같은 `word` 입력이 반복되면 `count`를 누적한다.
- schema: `word TEXT PRIMARY KEY`, `count INT DEFAULT 1`.
- 정책: `ON CONFLICT(word) DO UPDATE SET count = count + 1`.
- 완료 조건: 신규 단어와 기존 단어를 섞어 입력한 뒤 단어별 예상 횟수를 비교한다.
- 주의: 수신 횟수 누적 정책이므로 같은 이벤트 재전송도 다시 증가한다. 중복 이벤트 제거와 동일한 정책은 아니다.

## 2. 날짜 기반 연락처 동기화

- 목표: 같은 이름의 연락처는 더 최신 날짜일 때만 교체한다.
- 정책: `excluded.validDate > phonebook2.validDate`.
- 검증표: 신규 이름은 삽입, 이전·동일 날짜는 보존, 이후 날짜는 교체.
- 완료 조건: 네 가지 경우의 번호와 날짜를 조회해 확인한다.
- 설계 질문: 이름이 실제 식별자로 충분한가? 예제의 primary key를 실제 업무 식별 기준으로 그대로 옮기지 않는다.

## 3. 충돌 정책과 실패 경계 검증기

- 목표: id/email 각각의 충돌 분기와 `DO UPDATE` 실패를 분리해서 관찰한다.
- SQLite 3.35.0 이상에서 여러 `ON CONFLICT` 절을 사용한다.
- 두 constraint가 같은 행에서 충돌하는 입력으로 첫 절만 실행됨을 검증한다.
- multi-row 입력에 신규 행과 기존 행을 섞고, 갱신 중 `CHECK` 위반을 유발한다.
- 완료 조건: 오류 발생 시 먼저 삽입된 행도 사라지고, 해당 문장 이전 데이터는 보존되는지 확인한다.

## Sources

- https://www.sqlite.org/lang_upsert.html
- 내용 기준: 제공 dossier가 인용한 문서 갱신일 **2024-04-11**. 이후 변경은 이 노트의 검토 범위 밖이다.
