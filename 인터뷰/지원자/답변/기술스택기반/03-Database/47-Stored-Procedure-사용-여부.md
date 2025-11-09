# Stored Procedure 사용 여부와 그 이유는?

## 답변

[여기에 답변 작성]

## 핵심 키워드

- Stored Procedure
- T-SQL
- 비즈니스 로직 위치
- 성능 최적화
- 유지보수성
- 데이터베이스 종속성

## Stored Procedure 장점

- 네트워크 트래픽 감소
- 실행 계획 캐싱
- 데이터베이스 레벨 보안
- 복잡한 트랜잭션 처리
- Precompiled 실행

## Stored Procedure 단점

- 데이터베이스 종속성
- 버전 관리 어려움
- 디버깅 어려움
- 비즈니스 로직 분산
- ORM과의 불일치
- 테스트 복잡도

## 사용 판단 기준

- 복잡한 데이터 처리 로직
- 배치 작업
- 레거시 시스템 연동
- 성능 크리티컬 쿼리
- 트랜잭션 일관성

## 대안

- Application Layer에서 처리
- ORM Query Builder
- Database View
- Function

## 코드/쿼리 예시

```sql
-- Stored Procedure 생성
CREATE PROCEDURE sp_TransferMoney
  @FromAccountId INT,
  @ToAccountId INT,
  @Amount DECIMAL(18,2)
AS
BEGIN
  SET NOCOUNT ON;

  BEGIN TRANSACTION;
  BEGIN TRY
    -- 출금
    UPDATE accounts
    SET balance = balance - @Amount
    WHERE account_id = @FromAccountId;

    -- 잔액 확인
    IF (SELECT balance FROM accounts WHERE account_id = @FromAccountId) < 0
    BEGIN
      RAISERROR('Insufficient balance', 16, 1);
      ROLLBACK TRANSACTION;
      RETURN;
    END

    -- 입금
    UPDATE accounts
    SET balance = balance + @Amount
    WHERE account_id = @ToAccountId;

    COMMIT TRANSACTION;
  END TRY
  BEGIN CATCH
    ROLLBACK TRANSACTION;
    THROW;
  END CATCH
END;
GO

-- Stored Procedure 실행
EXEC sp_TransferMoney
  @FromAccountId = 1,
  @ToAccountId = 2,
  @Amount = 100.00;

-- OUTPUT 파라미터 사용
CREATE PROCEDURE sp_GetAccountBalance
  @AccountId INT,
  @Balance DECIMAL(18,2) OUTPUT
AS
BEGIN
  SELECT @Balance = balance
  FROM accounts
  WHERE account_id = @AccountId;
END;
GO

-- OUTPUT 파라미터 실행
DECLARE @CurrentBalance DECIMAL(18,2);
EXEC sp_GetAccountBalance
  @AccountId = 1,
  @Balance = @CurrentBalance OUTPUT;
SELECT @CurrentBalance AS Balance;

-- Table-Valued Function (대안)
CREATE FUNCTION fn_GetActiveOrders (@CustomerId INT)
RETURNS TABLE
AS
RETURN (
  SELECT order_id, order_date, total_amount
  FROM orders
  WHERE customer_id = @CustomerId
    AND status = 'ACTIVE'
);
GO

-- Function 사용
SELECT * FROM fn_GetActiveOrders(123);

-- Stored Procedure 수정
ALTER PROCEDURE sp_TransferMoney
  -- 수정된 파라미터 및 로직
AS
BEGIN
  -- ...
END;
GO

-- Stored Procedure 삭제
DROP PROCEDURE sp_TransferMoney;
```

## 참고 자료

- MSSQL Stored Procedures Best Practices
- When to Use Stored Procedures vs Application Logic
