# DoltHub - 데이터 공유 플랫폼

## DoltHub 소개

### DoltHub란?

```
DoltHub = GitHub for Data
```

- Dolt 데이터베이스용 호스팅 플랫폼
- 데이터 공유, 협업, 발견
- 공개/비공개 저장소
- 웹 기반 SQL 쿼리 편집기

### 주요 기능

| 기능 | 설명 |
|------|------|
| **호스팅** | 클라우드에서 Dolt DB 호스팅 |
| **협업** | Pull Request로 데이터 변경 검토 |
| **발견** | 공개 데이터셋 검색 및 탐색 |
| **쿼리** | 웹에서 SQL 쿼리 실행 |
| **API** | REST/GraphQL API 제공 |

---

## 시작하기

### 계정 생성

1. https://www.dolthub.com 접속
2. Sign Up 클릭
3. GitHub 또는 이메일로 가입

### CLI 인증

```bash
# 로그인
dolt login

# 브라우저가 열리면 인증
# 또는 토큰 직접 입력
```

### 인증 확인

```bash
dolt creds ls
```

---

## 저장소 만들기

### 웹에서 생성

1. DoltHub 웹사이트 접속
2. "New Repository" 클릭
3. 이름, 설명, 공개/비공개 설정
4. Create Repository

### CLI에서 생성

```bash
# 로컬 저장소를 DoltHub에 푸시
cd my-dolt-db
dolt remote add origin your-username/my-dolt-db
dolt push -u origin main
```

---

## 원격 저장소 작업

### Clone (복제)

```bash
# 공개 저장소 복제
dolt clone dolthub/museum-collections

# 비공개 저장소 복제 (인증 필요)
dolt clone your-username/private-repo
```

### Remote 관리

```bash
# 원격 저장소 추가
dolt remote add origin your-username/repo-name

# 원격 목록
dolt remote -v

# 원격 삭제
dolt remote remove origin
```

### Push (푸시)

```bash
# main 브랜치 푸시
dolt push origin main

# 모든 브랜치 푸시
dolt push origin --all

# 업스트림 설정
dolt push -u origin main
```

### Pull (풀)

```bash
# 원격 변경사항 가져오기
dolt pull origin main

# 또는 (업스트림 설정 시)
dolt pull
```

### Fetch (페치)

```bash
# 원격 변경사항 확인만 (머지 안 함)
dolt fetch origin

# 원격 브랜치 확인
dolt branch -r
```

---

## 공개 데이터셋 탐색

### 인기 데이터셋

https://www.dolthub.com/discover

```
카테고리:
- Government (정부 데이터)
- Sports (스포츠 통계)
- Science (과학 데이터)
- Geography (지리 데이터)
- Finance (금융 데이터)
```

### 데이터셋 클론

```bash
# 박물관 컬렉션
dolt clone dolthub/museum-collections

# 미국 주택 가격
dolt clone dolthub/us-housing-prices

# IP 지오로케이션
dolt clone dolthub/ip-to-country
```

### 온라인 쿼리

1. 저장소 페이지 접속
2. "Query" 탭 클릭
3. SQL 쿼리 작성 및 실행

---

## 협업 워크플로우

### Fork (포크)

1. 원본 저장소에서 "Fork" 클릭
2. 내 계정에 복사본 생성

```bash
# 포크된 저장소 클론
dolt clone my-username/forked-repo
```

### Pull Request

#### 1. 브랜치 생성 및 작업

```bash
dolt checkout -b feature/my-changes

# 변경 작업
dolt sql -q "INSERT INTO data VALUES (...);"

# 커밋
dolt add .
dolt commit -m "새 데이터 추가"

# 푸시
dolt push origin feature/my-changes
```

#### 2. Pull Request 생성

1. DoltHub 웹에서 저장소 접속
2. "Pull Requests" 탭
3. "New Pull Request" 클릭
4. 브랜치 선택 및 설명 작성

#### 3. 리뷰 및 머지

- 리뷰어가 변경사항 검토
- 댓글로 피드백
- 승인 후 머지

### Issue 트래킹

- 저장소의 "Issues" 탭
- 버그 리포트, 기능 요청
- GitHub Issues와 유사

---

## SQL API

### 웹 쿼리

```
https://www.dolthub.com/repositories/{owner}/{repo}/query
```

### REST API

```bash
# 쿼리 실행
curl "https://www.dolthub.com/api/v1alpha1/{owner}/{repo}/main" \
  -H "Content-Type: application/json" \
  -d '{"q": "SELECT * FROM users LIMIT 10"}'
```

### 응답 형식

```json
{
  "query_execution_status": "Success",
  "query_execution_message": "",
  "repository_owner": "owner",
  "repository_name": "repo",
  "commit_ref": "main",
  "sql_query": "SELECT * FROM users LIMIT 10",
  "schema": [...],
  "rows": [...]
}
```

---

## Bounty (현상금)

### Bounty란?

- 데이터 수집/개선에 대한 보상 시스템
- 데이터 기여자에게 금전적 보상

### Bounty 예시

```
"미국 병원 가격 데이터 수집"
- 보상: $X per validated entry
- 조건: 특정 포맷, 검증 통과
```

### 참여 방법

1. Bounties 페이지에서 활성 bounty 확인
2. 데이터 기여
3. 검증 후 보상 수령

---

## 비공개 저장소

### 권한 관리

- Owner: 전체 권한
- Admin: 설정 변경 가능
- Write: 푸시 가능
- Read: 클론/쿼리만 가능

### 팀 협업

1. Organization 생성
2. 팀 멤버 초대
3. 저장소별 권한 설정

---

## DoltLab (셀프 호스팅)

### DoltLab이란?

```
DoltLab = DoltHub 온프레미스 버전
```

- 기업 내부 설치
- 데이터 통제권 확보
- 커스텀 인증 (SSO/LDAP)

### 설치

```bash
# Docker Compose
curl -O https://doltlab.dolthub.com/docker-compose.yaml
docker-compose up -d
```

---

## 실전 활용 예제

### 예제 1: 공개 데이터 활용

```bash
# 데이터셋 클론
dolt clone dolthub/corona-virus

# 쿼리 실행
dolt sql -q "
SELECT country, SUM(confirmed) as total
FROM cases
GROUP BY country
ORDER BY total DESC
LIMIT 10
"
```

### 예제 2: 팀 데이터 협업

```bash
# 1. 저장소 클론
dolt clone company-org/shared-data

# 2. 작업 브랜치 생성
dolt checkout -b update/q4-data

# 3. 데이터 수정
dolt sql -q "INSERT INTO sales VALUES (...)"

# 4. 커밋 및 푸시
dolt add .
dolt commit -m "Q4 판매 데이터 추가"
dolt push origin update/q4-data

# 5. PR 생성 (웹에서)
```

### 예제 3: 데이터 백업

```bash
# DoltHub를 백업 저장소로 활용
dolt remote add backup my-username/db-backup
dolt push backup main

# 정기 백업 스크립트
#!/bin/bash
cd /path/to/dolt-db
dolt add .
dolt commit -m "자동 백업: $(date)"
dolt push backup main
```

---

## 팁과 주의사항

### 좋은 관행

1. **명확한 커밋 메시지**: 데이터 변경 내용 설명
2. **브랜치 전략**: feature/fix/update 접두사
3. **문서화**: README.md에 스키마 설명
4. **작은 커밋**: 관련 변경만 묶어서

### 주의사항

1. **민감 데이터**: 공개 저장소에 개인정보 금지
2. **대용량 데이터**: 점진적 푸시 권장
3. **동기화**: 푸시 전 항상 풀

---

## 실습 과제

### 과제 1: DoltHub 시작하기

1. DoltHub 계정 생성
2. CLI 인증 설정
3. 첫 번째 저장소 생성
4. 로컬 데이터베이스 푸시

### 과제 2: 공개 데이터 활용

1. 공개 데이터셋 클론
2. 데이터 탐색 및 쿼리
3. 분석 결과 저장

### 과제 3: 협업 시뮬레이션

1. 저장소 포크
2. 브랜치에서 변경 작업
3. Pull Request 생성
4. (가능하면) 리뷰 및 머지

---

## 다음 단계

- [[06-integration|프로그래밍 언어 통합]]
- [[../05-projects|실전 프로젝트]]
