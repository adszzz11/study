# BLOB/CLOB 대용량 데이터 처리 방법은?

## 답변

[여기에 답변 작성]

## 핵심 키워드

- BLOB (Binary Large Object)
- CLOB (Character Large Object)
- LOB Locator
- 스트리밍 처리
- 청크(Chunk) 단위 처리
- 외부 저장소 활용

## 처리 방법

- 스트리밍 방식으로 읽기/쓰기
- 청크 단위 분할 처리
- LOB Locator 활용
- 임시 LOB 사용
- 외부 파일 시스템/오브젝트 스토리지 저장

## 성능 최적화

- SECUREFILE vs BASICFILE
- Compression 활용
- Deduplication 설정
- CACHE/NOCACHE 옵션
- PCTVERSION 튜닝

## 주의사항

- 메모리 부족 방지
- 트랜잭션 크기 관리
- Undo 테이블스페이스 고려
- 백업/복구 전략

## 코드/쿼리 예시

```sql
-- CLOB 테이블 생성 (SECUREFILE)
CREATE TABLE documents (
  doc_id NUMBER PRIMARY KEY,
  content CLOB
)
LOB (content) STORE AS SECUREFILE (
  TABLESPACE lob_data
  ENABLE STORAGE IN ROW
  CHUNK 8192
  CACHE
  COMPRESS HIGH
);

-- BLOB 데이터 삽입 (PL/SQL)
DECLARE
  v_blob BLOB;
  v_bfile BFILE;
BEGIN
  -- 빈 BLOB 생성
  INSERT INTO images (image_id, image_data)
  VALUES (1, EMPTY_BLOB())
  RETURNING image_data INTO v_blob;

  -- 외부 파일에서 읽기
  v_bfile := BFILENAME('IMAGE_DIR', 'photo.jpg');
  DBMS_LOB.FILEOPEN(v_bfile, DBMS_LOB.FILE_READONLY);
  DBMS_LOB.LOADFROMFILE(v_blob, v_bfile, DBMS_LOB.GETLENGTH(v_bfile));
  DBMS_LOB.FILECLOSE(v_bfile);

  COMMIT;
END;
/

-- CLOB 청크 단위 읽기
DECLARE
  v_clob CLOB;
  v_buffer VARCHAR2(32767);
  v_amount INTEGER := 32767;
  v_offset INTEGER := 1;
BEGIN
  SELECT content INTO v_clob FROM documents WHERE doc_id = 1;

  LOOP
    DBMS_LOB.READ(v_clob, v_amount, v_offset, v_buffer);
    -- 버퍼 처리
    v_offset := v_offset + v_amount;
  END LOOP;
EXCEPTION
  WHEN NO_DATA_FOUND THEN
    NULL; -- 읽기 완료
END;
/

-- LOB 저장 공간 확인
SELECT table_name, column_name,
       segment_name, bytes/1024/1024 as size_mb
FROM user_lobs l
JOIN user_segments s ON l.segment_name = s.segment_name
WHERE table_name = 'DOCUMENTS';
```

## 참고 자료

- Oracle Database SecureFiles and Large Objects Guide
- LOB Performance Best Practices
