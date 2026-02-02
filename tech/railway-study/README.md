# Railway 학습 가이드

## 개요

Railway는 개발자 친화적인 PaaS(Platform as a Service)로, GitHub 연동을 통한 자동 배포와 다양한 데이터베이스 원클릭 배포를 지원합니다.

## 목차

### 기본 개념
1. [[01-overview|Railway 개요]] - 핵심 개념, 장단점, 사용 사례
2. [[02-ecosystem|에코시스템]] - 관련 기술, 비교, 트렌드
3. [[03-references|참고 자료]] - 공식 문서, 학습 자료, 커뮤니티

### 실습 가이드
4. 학습 가이드
   - [[04-learning/01-quickstart|Quick Start]] - 첫 배포, GitHub 연동
   - [[04-learning/02-services|서비스 유형]] - Web, Worker, Cron
   - [[04-learning/03-databases|데이터베이스]] - PostgreSQL, Redis, MySQL
   - [[04-learning/04-environment|환경 변수]] - 환경 변수 및 시크릿 관리
   - [[04-learning/05-networking|네트워킹]] - 도메인, HTTPS, Private Networking
   - [[04-learning/06-monitoring|모니터링]] - 로깅, 메트릭, 스케일링

### 실전 적용
5. [[05-projects|실전 프로젝트]] - 프로젝트 예제, Best Practices
6. [[cheatsheet|Cheatsheet]] - 빠른 참조

---

## Quick Start

### 1. Railway 가입 및 프로젝트 생성
```bash
# 1. railway.app 접속
# 2. GitHub 계정으로 로그인
# 3. "New Project" 클릭
# 4. "Deploy from GitHub repo" 선택
# 5. 배포할 저장소 선택
```

### 2. CLI 설치 (선택사항)
```bash
# npm으로 설치
npm install -g @railway/cli

# 로그인
railway login

# 프로젝트 연결
railway link
```

### 3. 첫 배포
```bash
# GitHub에 코드 푸시하면 자동 배포
git push origin main

# 또는 CLI로 수동 배포
railway up
```

---

## 학습 플랜

### Week 1: 기초
- [ ] Railway 계정 생성 및 첫 프로젝트 배포
- [ ] CLI 설치 및 기본 명령어 학습
- [ ] 환경 변수 설정 방법 이해

### Week 2: 데이터베이스
- [ ] PostgreSQL 추가 및 연결
- [ ] Redis 캐시 서버 구성
- [ ] 데이터베이스 백업/복원 학습

### Week 3: 고급 기능
- [ ] 커스텀 도메인 설정
- [ ] Private Networking 구성
- [ ] 모니터링 및 로깅 설정

### Week 4: 실전 프로젝트
- [ ] 풀스택 애플리케이션 배포
- [ ] CI/CD 파이프라인 최적화
- [ ] 비용 최적화 및 스케일링 전략

---

## 핵심 특징

| 특징 | 설명 |
|------|------|
| **자동 빌드** | Nixpacks로 언어/프레임워크 자동 감지 |
| **GitHub 연동** | Push 시 자동 배포 |
| **원클릭 DB** | PostgreSQL, MySQL, Redis, MongoDB 지원 |
| **환경 분리** | Development, Staging, Production 환경 지원 |
| **Private Network** | 서비스 간 안전한 내부 통신 |

---

## 관련 링크

- [Railway 공식 사이트](https://railway.app)
- [Railway 공식 문서](https://docs.railway.app)
- [Railway GitHub](https://github.com/railwayapp)
- [Railway Discord](https://discord.gg/railway)
