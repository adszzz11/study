# Dolt 학습 가이드

> Git처럼 버전 관리되는 SQL 데이터베이스

## 목차

1. [[01-overview|개요]] - 핵심 개념, 장단점, 사용 사례
2. [[02-ecosystem|에코시스템]] - 관련 기술, 비교, 트렌드
3. [[03-references|참고 자료]] - 공식 문서, 학습 자료, 커뮤니티
4. 실습 가이드
   - [[04-learning/01-installation|설치 및 기본 사용]]
   - [[04-learning/02-git-for-data|Git 명령어와 데이터 버전 관리]]
   - [[04-learning/03-sql-operations|SQL 작업]]
   - [[04-learning/04-branching-merging|브랜칭과 머지]]
   - [[04-learning/05-dolthub|DoltHub]]
   - [[04-learning/06-integration|프로그래밍 언어 통합]]
5. [[05-projects|실전 프로젝트]] - Best Practices
6. [[cheatsheet|치트시트]] - 빠른 참조

---

## Quick Start

### 설치

```bash
# Linux/macOS
curl -L https://github.com/dolthub/dolt/releases/latest/download/install.sh | sudo bash

# macOS (Homebrew)
brew install dolt

# Windows (Chocolatey)
choco install dolt
```

### 첫 데이터베이스 만들기

```bash
# 디렉토리 생성 및 초기화
mkdir my-first-dolt-db && cd my-first-dolt-db
dolt init

# 사용자 설정
dolt config --global --add user.email "you@example.com"
dolt config --global --add user.name "Your Name"

# SQL 쉘 시작
dolt sql

# 테이블 생성 및 데이터 추가
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(100)
);

INSERT INTO users (name, email) VALUES ('홍길동', 'hong@example.com');

# 변경사항 커밋
dolt add .
dolt commit -m "첫 번째 커밋: users 테이블 생성"
```

---

## 학습 플랜

### 1주차: 기초 (Day 1-7)

| 일차 | 주제 | 학습 내용 |
|------|------|----------|
| Day 1 | 설치 및 개요 | Dolt 설치, 기본 개념 이해 |
| Day 2 | SQL 기초 | 테이블 생성, CRUD 작업 |
| Day 3 | 버전 관리 기초 | commit, log, diff 명령어 |
| Day 4 | 브랜칭 입문 | branch 생성, checkout |
| Day 5 | 머지 기초 | 브랜치 머지, 충돌 해결 |
| Day 6 | DoltHub 탐색 | 계정 생성, 공개 데이터셋 탐색 |
| Day 7 | 복습 및 실습 | 미니 프로젝트 |

### 2주차: 심화 (Day 8-14)

| 일차 | 주제 | 학습 내용 |
|------|------|----------|
| Day 8 | 고급 SQL | 인덱스, 조인, 서브쿼리 |
| Day 9 | 데이터 가져오기 | CSV/JSON 임포트 |
| Day 10 | 원격 저장소 | clone, push, pull |
| Day 11 | DoltHub 협업 | fork, PR, 데이터 공유 |
| Day 12 | Python 연동 | doltpy 라이브러리 |
| Day 13 | 실전 프로젝트 | 데이터 파이프라인 구축 |
| Day 14 | 마무리 | Best Practices, 트러블슈팅 |

---

## Dolt가 적합한 경우

- 데이터 변경 이력 추적이 필요할 때
- 여러 팀원이 데이터를 협업할 때
- 데이터 스키마 진화를 관리할 때
- 실험적 데이터 변경을 안전하게 테스트할 때
- ML 학습 데이터 버전 관리가 필요할 때

## Dolt가 적합하지 않은 경우

- 초고성능 OLTP 워크로드
- 대규모 실시간 트랜잭션
- 기존 MySQL을 단순 대체하려는 경우

---

## 핵심 명령어 미리보기

```bash
# Git과 유사한 명령어
dolt init          # 저장소 초기화
dolt status        # 상태 확인
dolt add .         # 변경사항 스테이징
dolt commit        # 커밋
dolt log           # 히스토리 확인
dolt diff          # 변경사항 비교
dolt branch        # 브랜치 관리
dolt merge         # 머지
dolt clone         # 원격 저장소 복제
dolt push          # 원격에 푸시
dolt pull          # 원격에서 풀
```

---

## 관련 링크

- [공식 문서](https://docs.dolthub.com)
- [GitHub](https://github.com/dolthub/dolt)
- [DoltHub](https://www.dolthub.com)
- [Discord 커뮤니티](https://discord.gg/gqr7K4VNKe)
