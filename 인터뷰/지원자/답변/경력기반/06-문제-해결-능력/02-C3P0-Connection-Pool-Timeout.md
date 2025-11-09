# C3P0 Connection Pool의 timeout 문제를 어떻게 발견했고, setQueryTimeout 외에 고려한 다른 해결책은?

## 답변

[여기에 답변 작성]

## 핵심 키워드

- C3P0 Connection Pool
- Connection Timeout
- Query Timeout
- Connection Leak
- Pool 튜닝

## 문제 발견 과정

### 증상
-

### 모니터링 지표
-

### 분석 방법
-

## 해결책 비교

### 1. setQueryTimeout
**장점:**
-

**단점:**
-

### 2. Connection Pool 설정 조정
```properties
c3p0.maxPoolSize=
c3p0.minPoolSize=
c3p0.acquireIncrement=
c3p0.maxIdleTime=
```

### 3. HikariCP로 마이그레이션
-

### 4. Database Timeout 설정
-

## 최종 선택과 이유

-

## 성능 개선 결과

-

## 참고 자료

-
