# Dolt 참고 자료

## 공식 문서

### 핵심 문서

| 문서 | URL | 설명 |
|------|-----|------|
| **메인 문서** | https://docs.dolthub.com | 전체 문서 포털 |
| **시작하기** | https://docs.dolthub.com/introduction/getting-started | 빠른 시작 가이드 |
| **CLI 레퍼런스** | https://docs.dolthub.com/cli-reference/cli | 명령어 상세 설명 |
| **SQL 레퍼런스** | https://docs.dolthub.com/sql-reference/sql-support | SQL 기능 지원 현황 |
| **시스템 테이블** | https://docs.dolthub.com/sql-reference/version-control/dolt-system-tables | dolt_ 테이블 설명 |

### 주제별 문서

```
개념 이해
├── https://docs.dolthub.com/concepts/dolt/git-for-data
├── https://docs.dolthub.com/concepts/dolt/commits
└── https://docs.dolthub.com/concepts/dolt/branches

실용 가이드
├── https://docs.dolthub.com/guides/import-data
├── https://docs.dolthub.com/guides/merging
└── https://docs.dolthub.com/guides/sql-server
```

---

## GitHub 저장소

### 핵심 저장소

| 저장소 | URL | 설명 |
|--------|-----|------|
| **dolt** | https://github.com/dolthub/dolt | 메인 저장소 |
| **doltpy** | https://github.com/dolthub/doltpy | Python 라이브러리 |
| **go-mysql-server** | https://github.com/dolthub/go-mysql-server | SQL 엔진 |
| **dolt-workbench** | https://github.com/dolthub/dolt-workbench | 웹 UI |

### 유용한 링크

```bash
# 이슈 트래커
https://github.com/dolthub/dolt/issues

# 릴리스 노트
https://github.com/dolthub/dolt/releases

# 로드맵
https://github.com/dolthub/dolt/blob/main/ROADMAP.md
```

---

## 학습 자료

### 블로그 포스트 (추천)

1. **Dolt 소개**
   - [What is Dolt?](https://www.dolthub.com/blog/2021-09-17-dolt-the-first-version-controlled-database/)

2. **사용 사례**
   - [Dolt for ML Data](https://www.dolthub.com/blog/2022-03-09-dolt-for-ml-data/)
   - [Dolt for Audit Logs](https://www.dolthub.com/blog/2022-02-16-dolt-audit-log/)

3. **기술 심층**
   - [How Dolt Stores Data](https://www.dolthub.com/blog/2022-06-27-prolly-trees/)
   - [Dolt Performance](https://www.dolthub.com/blog/2022-01-12-dolt-vs-mysql-performance/)

### 비디오 튜토리얼

```
YouTube 채널: DoltHub
https://www.youtube.com/c/DoltHub

추천 재생목록:
- Getting Started with Dolt
- Dolt Deep Dives
- DoltHub Tutorials
```

### 발표 자료

- [Git for Data - 개념 소개](https://www.dolthub.com/blog/2021-09-17-dolt-the-first-version-controlled-database/)
- [Dolt 아키텍처](https://www.dolthub.com/blog/2022-06-27-prolly-trees/)

---

## 커뮤니티

### Discord (가장 활발)

```
https://discord.gg/gqr7K4VNKe

주요 채널:
#general - 일반 대화
#help - 질문/답변
#show-and-tell - 프로젝트 공유
#feature-requests - 기능 요청
```

### 기타 채널

| 채널 | URL | 용도 |
|------|-----|------|
| **Twitter/X** | https://twitter.com/daborosoft | 공지, 업데이트 |
| **Reddit** | https://www.reddit.com/r/dolt/ | 토론 |
| **Stack Overflow** | `[dolt]` 태그 | Q&A |

---

## 데이터셋 저장소

### DoltHub 인기 데이터셋

```
https://www.dolthub.com/discover

카테고리:
- 공공 데이터
- 스포츠 통계
- 지리/위치 데이터
- 금융 데이터
```

### 추천 탐색 데이터셋

| 데이터셋 | URL | 설명 |
|----------|-----|------|
| **museum-collections** | dolthub/museum-collections | 박물관 컬렉션 |
| **us-housing-prices** | dolthub/us-housing-prices | 미국 주택 가격 |
| **wikipedia-ngrams** | dolthub/wikipedia-ngrams | 위키피디아 n-gram |

---

## 도구 및 통합

### 공식 도구

| 도구 | 설명 | 링크 |
|------|------|------|
| **doltpy** | Python 클라이언트 | https://pypi.org/project/doltpy/ |
| **dolt-workbench** | 웹 UI | https://github.com/dolthub/dolt-workbench |

### 커뮤니티 도구

```
dbt-dolt: dbt 어댑터
https://github.com/dolthub/dbt-dolt

dolt-jdbc: JDBC 드라이버 (MySQL 호환)
표준 MySQL JDBC 드라이버 사용
```

---

## 책 및 심층 자료

### 관련 개념 학습

| 주제 | 추천 자료 |
|------|----------|
| **Git 기초** | Pro Git (https://git-scm.com/book) |
| **SQL 기초** | SQLBolt (https://sqlbolt.com/) |
| **데이터 버전 관리** | DVC 문서 (비교 학습용) |

### 데이터 엔지니어링

```
Fundamentals of Data Engineering
- 데이터 관리 전반 이해
- DataOps 개념

Data Version Control with DVC
- 파일 기반 접근법 이해
- Dolt와의 차이점 파악
```

---

## 업데이트 추적

### 릴리스 정보

```bash
# GitHub 릴리스 페이지
https://github.com/dolthub/dolt/releases

# 버전 확인
dolt version
```

### 뉴스레터 및 블로그

```
DoltHub 블로그: https://www.dolthub.com/blog
- 주간 업데이트
- 새 기능 소개
- 기술 심층 분석
```

---

## 빠른 참조 북마크

```markdown
## 즐겨찾기 추천

1. 공식 문서 홈
   https://docs.dolthub.com

2. CLI 레퍼런스
   https://docs.dolthub.com/cli-reference/cli

3. SQL 지원 현황
   https://docs.dolthub.com/sql-reference/sql-support

4. Discord 커뮤니티
   https://discord.gg/gqr7K4VNKe

5. GitHub 이슈
   https://github.com/dolthub/dolt/issues
```

---

## 다음 단계

- [[04-learning/01-installation|설치 가이드]] - 직접 설치해보기
- [[cheatsheet|치트시트]] - 명령어 빠른 참조
