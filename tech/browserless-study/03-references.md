# Browserless 참고 자료

## 공식 문서

### Browserless 공식
| 리소스 | URL | 설명 |
|--------|-----|------|
| 공식 문서 | https://docs.browserless.io | 전체 문서 |
| GitHub | https://github.com/browserless/browserless | 소스 코드 |
| Docker Hub | https://hub.docker.com/r/browserless/chrome | Docker 이미지 |
| GitHub Container | ghcr.io/browserless/chromium | 최신 이미지 |

### 주요 문서 섹션
- **Quick Start**: https://docs.browserless.io/start
- **REST API**: https://docs.browserless.io/http-apis
- **WebSocket**: https://docs.browserless.io/websocket
- **BrowserQL**: https://docs.browserless.io/browserql
- **Self-Hosting**: https://docs.browserless.io/docker

## 관련 도구 공식 문서

### Puppeteer
| 리소스 | URL |
|--------|-----|
| 공식 문서 | https://pptr.dev |
| GitHub | https://github.com/puppeteer/puppeteer |
| API Reference | https://pptr.dev/api |

### Playwright
| 리소스 | URL |
|--------|-----|
| 공식 문서 | https://playwright.dev |
| GitHub | https://github.com/microsoft/playwright |
| API Reference | https://playwright.dev/docs/api/class-playwright |

### Selenium
| 리소스 | URL |
|--------|-----|
| 공식 문서 | https://www.selenium.dev/documentation |
| WebDriver | https://www.w3.org/TR/webdriver |

## 학습 자료

### 튜토리얼 및 가이드

#### 초급
- Browserless 공식 Quick Start 가이드
- Puppeteer Getting Started
- Playwright 첫 번째 테스트 작성하기

#### 중급
- 효과적인 웹 스크래핑 패턴
- 안티봇 탐지 우회 기법
- 브라우저 자동화 최적화

#### 고급
- 대규모 스크래핑 아키텍처
- 분산 브라우저 풀 관리
- 커스텀 BrowserQL 작성

### 추천 학습 순서

```
1. 기초
   ├── Browserless 공식 문서 Quick Start
   ├── Docker 기본 사용법
   └── REST API 개념

2. 도구 학습
   ├── Puppeteer 튜토리얼
   ├── Playwright 튜토리얼 (선택)
   └── CSS/XPath 셀렉터

3. 실전
   ├── 웹 스크래핑 프로젝트
   ├── PDF 생성 자동화
   └── E2E 테스트 구축

4. 고급
   ├── BrowserQL 마스터
   ├── 안티봇 우회 기법
   └── 운영 환경 최적화
```

## 커뮤니티

### 공식 채널
- **GitHub Issues**: 버그 리포트 및 기능 요청
- **GitHub Discussions**: 질문 및 토론
- **Slack**: 실시간 커뮤니티 (공식 사이트에서 초대)

### 관련 커뮤니티
- **Reddit**: r/webscraping
- **Stack Overflow**: [browserless] 태그
- **Discord**: Puppeteer/Playwright 커뮤니티

## 유용한 도구

### 개발 도구
| 도구 | 용도 |
|------|------|
| Chrome DevTools | 셀렉터 테스트, 디버깅 |
| Postman | REST API 테스트 |
| VS Code | 코드 편집, 디버깅 |

### 브라우저 확장
| 확장 | 용도 |
|------|------|
| SelectorGadget | CSS 셀렉터 생성 |
| XPath Helper | XPath 테스트 |
| JSON Viewer | API 응답 확인 |

### CLI 도구
```bash
# curl - REST API 테스트
curl -X POST http://localhost:3000/screenshot \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# jq - JSON 처리
curl ... | jq '.data'

# httpie - 친화적 HTTP 클라이언트
http POST localhost:3000/content url=https://example.com
```

## 예제 저장소

### 공식 예제
- https://github.com/browserless/browserless/tree/main/examples

### 커뮤니티 예제
- Puppeteer 예제: https://github.com/puppeteer/puppeteer/tree/main/examples
- Playwright 예제: https://github.com/microsoft/playwright/tree/main/examples

## 블로그 및 아티클

### 공식 블로그
- Browserless Blog: https://www.browserless.io/blog

### 추천 읽을거리
- "웹 스크래핑 Best Practices"
- "헤드리스 브라우저 선택 가이드"
- "안티봇 탐지의 원리와 대응"
- "프로덕션 브라우저 자동화"

## 비디오 자료

### YouTube 채널
- Browserless 공식 채널
- Puppeteer 튜토리얼 시리즈
- Playwright Conference 발표 영상

### 추천 영상 주제
- Browserless 설치 및 설정
- 첫 번째 스크래핑 프로젝트
- 고급 셀렉터 기법
- 안티봇 우회 전략

## 참고 서적

### 웹 스크래핑 관련
- "Web Scraping with Python" - Ryan Mitchell
- "Automate the Boring Stuff with Python"
- "Node.js Web Development"

### 테스트 자동화 관련
- "Learning JavaScript Testing"
- "End-to-End Testing with Playwright"

## 법적 고려사항

### 스크래핑 관련 법률
- **robots.txt**: 웹사이트의 크롤링 정책 확인
- **이용약관**: 서비스 약관 위반 여부 확인
- **개인정보보호법**: 개인정보 수집 시 주의
- **저작권법**: 콘텐츠 무단 복제 금지

### Best Practices
```
1. robots.txt 확인 및 준수
2. 요청 속도 제한 (Rate Limiting)
3. 서버 부하 최소화
4. 개인정보 수집 시 동의 획득
5. 수집 데이터 보안 관리
```

## 다음 단계

- [[04-learning/01-rest-api|REST API 기본 사용]] - 첫 번째 실습 시작
- [[04-learning/03-docker-selfhost|Docker Self-hosted]] - 로컬 환경 구축
