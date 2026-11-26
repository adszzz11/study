---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# 심화: 저장 정책과 기록 생애주기

## 저장 완료 조건

인식 종료, 사용자 확정, 입력 세션 종료 중 어느 사건이 저장을 일으키는지 정한다. 학습용 권장 흐름은 `인식 중 → 확정 대기 → 저장 요청 → commit 성공 → 저장 완료 표시`다. 실패 시 성공 표시를 하지 않고 재시도 가능한 상태로 남긴다. Sokki의 실제 저장 시점은 미확인이다.

Transaction은 여러 변경을 하나의 단위로 묶는 데 쓴다. 시작하기에서 만든 DB를 대상으로 한 예시다.

```sql
BEGIN TRANSACTION;
INSERT INTO recognition_history (transcript) VALUES ('확정된 예제 문장');
COMMIT;
```

오류가 발생하면 애플리케이션은 transaction 상태를 확인하고 필요 시 ROLLBACK한다. 앱 강제 종료 뒤에도 성공 처리한 기록이 남는지 실습한다. Transaction 사용만으로 모든 설정·저장 장치의 장애 내구성을 보장한다고 해석하지 않는다.

## 중복과 중간 결과

| 정책 | 이점 | 검토할 비용 |
|---|---|---|
| 최종 결과만 저장 | 목록이 단순하고 기록량이 적음 | 중간 수정 과정은 복원하기 어려움 |
| 중간 결과 전체 저장 | 변경 과정을 관찰 가능 | revision 순서, 저장량, 최종본 식별 필요 |

동일 저장 요청의 재시도에는 세션별 안정적인 request ID와 UNIQUE 제약을 검토한다. 동일 텍스트라도 서로 다른 받아쓰기라면 별도 기록일 수 있으므로 텍스트 자체를 중복 판정 기준으로 삼지 않는다. 이는 최소 schema에 아직 구현하지 않은 확장 요구사항이다.

## 조회·수정·삭제

시작하기의 실습 DB에서만 실행한다. id는 먼저 SELECT로 확인한다.

```sql
SELECT id, transcript FROM recognition_history ORDER BY id DESC;
UPDATE recognition_history SET transcript = '수정된 예제' WHERE id = 1;
DELETE FROM recognition_history WHERE id = 1;
SELECT * FROM recognition_history WHERE id = 1;
```

삭제 후 조회 결과가 없어야 한다. SQL DELETE는 백업 사본까지 삭제하거나 저장 매체에서 복구 불가능하게 지우는 보장이 아니다. 수정 이력이 필요하면 별도 revision 모델을 설계한다.

## 데이터 종류별 경계 문서화

| 데이터 | 처리 위치 | 저장 위치 | 외부 전송 |
|---|---|---|---|
| 오디오 | 기기 내 음성 처리 | 파일 보관 여부 미확인 | Mac 밖으로 나가지 않는다고 설명 |
| 인식 텍스트 | 기기 내 인식으로 생성 | 기록은 로컬 SQLite, 정확한 저장 범위 미확인 | 미확인 |
| 시간 정보 | 오버레이 표시, 계산 위치 미확인 | 저장 여부 미확인 | 미확인 |

위 표는 dossier의 확인 범위다. 직접 만든 앱의 정책은 별도 표로 작성한다. 암호화, 접근 권한, 보관 기간, 백업 위치·복구 절차도 명시한다. 실행 중 DB의 백업은 관련 파일 상태를 고려해야 하므로 단순 파일 복사 대신 SQLite backup 기능 등을 검토한다.

## 검증 질문

- [ ] 저장 실패와 재시도에서 누락·중복이 없는가?
- [ ] 삭제·재실행 뒤 결과가 요구사항과 일치하는가?
- [ ] 백업 복구 후 기록 수와 본문이 일치하는가?
- [ ] 모르는 데이터 취급 항목을 미확인으로 남겼는가?

## 관련 노트

[[tech/data/sqlite-local-history/05-projects|정책 비교 실험]] · [[tech/data/sqlite-local-history/README|학습 경로]]

## Sources

- 사례 범위: 제공 dossier, URL 미제공.
- Transaction: https://www.sqlite.org/lang_transaction.html
- Backup API: https://www.sqlite.org/backup.html
- DELETE: https://www.sqlite.org/lang_delete.html
