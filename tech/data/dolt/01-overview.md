# Dolt 개요

> "Git for Data" - 데이터를 위한 버전 관리 시스템

## 핵심 개념

### Dolt란?

Dolt는 **Git처럼 버전 관리가 가능한 SQL 데이터베이스**입니다. Git이 소스 코드의 변경 이력을 관리하듯, Dolt는 데이터의 변경 이력을 관리합니다.

```
Git : 소스 코드 = Dolt : 데이터
```

### 주요 특징

1. **MySQL 호환성**
   - MySQL 프로토콜 지원
   - 표준 SQL 구문 사용
   - MySQL 클라이언트/드라이버 사용 가능

2. **Git 스타일 버전 관리**
   - commit, branch, merge, diff
   - 모든 변경사항 추적
   - 이전 버전으로 롤백 가능

3. **분산 데이터베이스**
   - clone, push, pull 지원
   - 오프라인 작업 가능
   - 여러 복제본 간 동기화

---

## 아키텍처

```
+------------------+
|   SQL 클라이언트   |  (MySQL Workbench, DBeaver, 애플리케이션)
+--------+---------+
         |
         v
+------------------+
|   MySQL 프로토콜   |  (3306 포트)
+--------+---------+
         |
         v
+------------------+
|   Dolt SQL 엔진   |  (파싱, 실행 계획, 최적화)
+--------+---------+
         |
         v
+------------------+
|   스토리지 엔진    |  (Prolly Tree, Content-Addressed)
+--------+---------+
         |
         v
+------------------+
|     파일 시스템    |  (.dolt 디렉토리)
+------------------+
```

### 핵심 데이터 구조

- **Prolly Tree**: B-Tree와 Merkle Tree의 하이브리드
- **Content-Addressed Storage**: 데이터를 해시로 참조
- **Structural Sharing**: 변경되지 않은 데이터 공유로 저장 공간 효율화

---

## 장점

### 1. 데이터 이력 추적

```sql
-- 특정 시점의 데이터 조회
SELECT * FROM users AS OF 'main~3';

-- 두 커밋 간 차이 확인
SELECT * FROM dolt_diff('main~1', 'main', 'users');
```

### 2. 안전한 실험

```bash
# 실험용 브랜치 생성
dolt checkout -b experiment

# 마음껏 수정 후 문제 있으면 폐기
dolt checkout main
dolt branch -d experiment
```

### 3. 협업 용이

```bash
# 팀원의 변경사항 가져오기
dolt pull origin main

# 내 변경사항 공유
dolt push origin feature/new-data
```

### 4. 롤백 가능

```bash
# 특정 커밋으로 되돌리기
dolt reset --hard HEAD~2

# 특정 테이블만 복구
dolt checkout HEAD~1 -- users
```

### 5. 감사(Audit) 지원

```sql
-- 누가, 언제, 무엇을 변경했는지 추적
SELECT * FROM dolt_log;
SELECT * FROM dolt_blame_users;
```

---

## 단점

### 1. 성능 오버헤드

- 버전 관리를 위한 추가 저장 공간 필요
- 순수 MySQL 대비 쓰기 성능 약간 저하
- 대용량 바이너리 데이터에 비효율적

### 2. 학습 곡선

- Git + SQL 두 가지 패러다임 이해 필요
- 충돌 해결 방법 학습 필요

### 3. 생태계 성숙도

- 일부 MySQL 기능 미지원
- 써드파티 도구 호환성 제한
- 커뮤니티 크기가 상대적으로 작음

### 4. 운영 복잡성

- 백업/복구 전략 수립 필요
- 브랜치 전략 설계 필요

---

## 사용 사례

### 1. ML/AI 데이터 관리

```
데이터셋 v1.0 (baseline)
    │
    ├── v1.1 (라벨링 수정)
    │
    └── v1.2 (데이터 증강)
```

- 학습 데이터 버전 관리
- 실험별 데이터셋 브랜칭
- 모델 성능과 데이터 버전 연관

### 2. 데이터 협업

```bash
# 데이터 분석가 A
dolt checkout -b analysis/q4-report
# 분석 작업...
dolt push origin analysis/q4-report

# 데이터 분석가 B
dolt fetch origin
dolt checkout analysis/q4-report
# 리뷰 및 추가 분석...
```

### 3. 설정 데이터 관리

```sql
-- 환경별 설정 브랜치
-- main: 프로덕션
-- staging: 스테이징
-- dev: 개발

SELECT * FROM config;  -- 현재 브랜치의 설정
```

### 4. 감사 로그

```sql
-- 특정 레코드의 변경 이력
SELECT * FROM dolt_history_users WHERE id = 123;
```

### 5. 데이터 마이그레이션

```bash
# 마이그레이션 테스트
dolt checkout -b migration-test
# 스키마 변경 적용
dolt sql < migration.sql
# 검증 후 main에 머지
dolt checkout main
dolt merge migration-test
```

---

## Git vs Dolt 비교

| 구분 | Git | Dolt |
|------|-----|------|
| 대상 | 소스 코드 (텍스트) | 데이터 (테이블) |
| 단위 | 파일, 라인 | 테이블, 행 |
| 쿼리 | 없음 | SQL |
| 충돌 단위 | 라인 | 셀 (Cell) |
| 원격 저장소 | GitHub, GitLab | DoltHub |
| 프로토콜 | Git 프로토콜 | Git + MySQL 프로토콜 |

---

## Dolt 사용을 고려해야 하는 신호

- "이 데이터가 언제 변경됐지?"
- "이전 버전의 데이터가 필요해"
- "실험적으로 데이터를 수정해보고 싶어"
- "여러 팀이 같은 데이터를 수정해야 해"
- "데이터 변경에 대한 코드 리뷰가 필요해"

---

## 다음 단계

- [[02-ecosystem|에코시스템]] - 관련 도구 및 기술 비교
- [[04-learning/01-installation|설치 가이드]] - 직접 설치해보기
