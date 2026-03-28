# Browserless 학습 가이드

## 개요

Browserless는 헤드리스 브라우저를 관리형 서비스 또는 Self-hosted로 운영할 수 있는 플랫폼입니다. 웹 스크래핑, PDF 생성, 스크린샷, 자동화 테스트 등 다양한 브라우저 작업을 효율적으로 처리할 수 있습니다.

## 목차

1. [[01-overview|개요]] - 핵심 개념, 장단점, 사용 사례
2. [[02-ecosystem|에코시스템]] - 관련 기술, 비교, 트렌드
3. [[03-references|참고 자료]] - 공식 문서, 학습 자료, 커뮤니티
4. **학습 모듈**
   - [[04-learning/01-rest-api|REST API 기본 사용]]
   - [[04-learning/02-puppeteer-playwright|Puppeteer/Playwright 연결]]
   - [[04-learning/03-docker-selfhost|Docker Self-hosted 실행]]
   - [[04-learning/04-antibot|안티봇 우회 BrowserQL]]
   - [[04-learning/05-sessions|Persistent Sessions]]
   - [[04-learning/06-function-api|Function API 커스텀 코드]]
5. [[05-projects|실전 프로젝트]] - 프로젝트 아이디어, Best Practices
6. [[cheatsheet|치트시트]] - 빠른 참조

## Quick Start

### Docker로 바로 시작하기

```bash
# Browserless 컨테이너 실행
docker run -p 3000:3000 ghcr.io/browserless/chromium

# 실행 확인
curl http://localhost:3000
```

### 첫 번째 스크린샷 생성

```bash
curl -X POST http://localhost:3000/screenshot \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### 첫 번째 PDF 생성

```bash
curl -X POST http://localhost:3000/pdf \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}' \
  --output example.pdf
```

## 학습 플랜

### 1주차: 기초 다지기
- [ ] Browserless 개요 이해 (01-overview)
- [ ] Docker로 로컬 환경 구축 (03-docker-selfhost)
- [ ] REST API 기본 사용법 익히기 (01-rest-api)

### 2주차: 도구 연동
- [ ] Puppeteer 연결 및 스크립트 작성 (02-puppeteer-playwright)
- [ ] Playwright 연결 및 비교 (02-puppeteer-playwright)
- [ ] 간단한 스크래핑 프로젝트 실습

### 3주차: 고급 기능
- [ ] BrowserQL로 안티봇 우회 (04-antibot)
- [ ] Persistent Sessions 활용 (05-sessions)
- [ ] Function API로 커스텀 코드 실행 (06-function-api)

### 4주차: 실전 프로젝트
- [ ] 실전 프로젝트 진행 (05-projects)
- [ ] Best Practices 적용
- [ ] 운영 환경 고려사항 학습

## 핵심 키워드

- **헤드리스 브라우저**: GUI 없이 실행되는 브라우저
- **웹 스크래핑**: 웹 페이지에서 데이터 추출
- **브라우저 자동화**: 브라우저 작업 프로그래밍
- **Puppeteer/Playwright**: 브라우저 자동화 라이브러리
- **BrowserQL**: Browserless의 안티봇 우회 기술

## 필요 환경

- Docker Desktop 또는 Docker Engine
- Node.js 18+ (Puppeteer/Playwright 사용 시)
- 터미널/CLI 기본 지식
