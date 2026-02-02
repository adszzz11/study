# Browserless 개요

## Browserless란?

Browserless는 헤드리스 Chrome/Chromium 브라우저를 관리하고 실행하기 위한 플랫폼입니다. 웹 스크래핑, PDF 생성, 스크린샷, 자동화 테스트 등 다양한 브라우저 작업을 REST API 또는 WebSocket을 통해 수행할 수 있습니다.

## 핵심 개념

### 헤드리스 브라우저 (Headless Browser)
- GUI(화면) 없이 백그라운드에서 실행되는 브라우저
- 서버 환경에서 브라우저 자동화 가능
- 리소스 효율적 (GPU, 디스플레이 불필요)

### 브라우저 풀 (Browser Pool)
- 여러 브라우저 인스턴스를 미리 생성하여 관리
- 요청 시 즉시 브라우저 할당
- 동시 요청 처리 최적화

### 연결 방식
```
┌─────────────────────────────────────────────────────────┐
│                    Browserless                          │
├─────────────────────────────────────────────────────────┤
│  REST API        │  WebSocket       │  CDP Protocol     │
│  - /screenshot   │  - Puppeteer     │  - Chrome DevTools│
│  - /pdf          │  - Playwright    │  - Selenium       │
│  - /scrape       │  - 실시간 제어    │  - 디버깅         │
└─────────────────────────────────────────────────────────┘
```

## 주요 기능

### 1. REST API 엔드포인트
| 엔드포인트 | 설명 |
|-----------|------|
| `/screenshot` | 웹 페이지 스크린샷 생성 |
| `/pdf` | 웹 페이지 PDF 변환 |
| `/content` | HTML 콘텐츠 추출 |
| `/scrape` | 데이터 스크래핑 |
| `/function` | 커스텀 코드 실행 |

### 2. 브라우저 자동화 도구 연결
- **Puppeteer**: Google의 Node.js 브라우저 자동화 라이브러리
- **Playwright**: Microsoft의 크로스 브라우저 자동화 도구
- **Selenium**: 전통적인 웹 테스트 프레임워크

### 3. 고급 기능
- **BrowserQL**: 안티봇 우회 및 CAPTCHA 해결
- **Persistent Sessions**: 로그인 상태 유지
- **Proxy 지원**: IP 우회 및 지역 제한 해제
- **Stealth Mode**: 봇 탐지 회피

## 장점

### 운영 관점
- **인프라 관리 간소화**: 브라우저 설치/업데이트 자동화
- **확장성**: 동시 요청 처리 용이
- **비용 효율**: Self-hosted로 무료 운영 가능
- **모니터링**: 내장 대시보드 제공

### 개발 관점
- **간편한 시작**: Docker 한 줄로 실행
- **다양한 연동**: REST API, WebSocket, CDP 지원
- **풍부한 문서**: 공식 문서 및 예제 제공
- **커뮤니티**: 활발한 GitHub 커뮤니티

### 기술 관점
- **안정성**: 브라우저 크래시 자동 복구
- **메모리 관리**: 메모리 누수 방지
- **타임아웃 처리**: 무한 루프 방지
- **보안**: Sandbox 모드 지원

## 단점

### Self-hosted
- 서버 리소스 필요 (메모리, CPU)
- 인프라 관리 책임
- 대규모 트래픽 시 스케일링 복잡

### Cloud 서비스
- 비용 발생 (사용량 기반)
- 네트워크 지연 (원격 실행)
- 데이터 보안 고려 필요

### 공통
- 복잡한 SPA 처리 시 학습 곡선
- 안티봇 완전 우회 불가 (일부 사이트)
- 법적 제약 고려 필요 (스크래핑)

## 사용 사례

### 1. 웹 스크래핑
```javascript
// 뉴스 사이트에서 기사 수집
const articles = await scrape({
  url: 'https://news.example.com',
  elements: [{
    selector: '.article-title',
    name: 'title'
  }]
});
```

### 2. 문서 생성
```javascript
// 보고서를 PDF로 변환
const pdf = await browserless.pdf({
  url: 'https://dashboard.example.com/report',
  format: 'A4',
  printBackground: true
});
```

### 3. 자동화 테스트
```javascript
// E2E 테스트 실행
const browser = await puppeteer.connect({
  browserWSEndpoint: 'ws://localhost:3000'
});
// 테스트 코드 실행...
```

### 4. 소셜 미디어 자동화
- 게시물 스크래핑
- 자동 포스팅
- 데이터 분석

### 5. 모니터링
- 웹사이트 변경 감지
- 가격 추적
- 재고 모니터링

## Browserless 버전

### v1 (레거시)
- Puppeteer 중심 설계
- 기본적인 REST API
- 안정적이지만 기능 제한

### v2 (현재)
- Playwright, Puppeteer, Selenium 모두 지원
- BrowserQL 도입
- 개선된 안티봇 우회
- 향상된 성능 및 안정성

## 아키텍처 개요

```
┌─────────────┐     ┌─────────────────────────────────────┐
│   Client    │     │           Browserless               │
│  ─────────  │     │  ┌─────────────────────────────────┐│
│  Puppeteer  │────▶│  │     Connection Manager         ││
│  Playwright │     │  └─────────────────────────────────┘│
│  REST API   │     │              │                      │
└─────────────┘     │              ▼                      │
                    │  ┌─────────────────────────────────┐│
                    │  │       Browser Pool              ││
                    │  │  ┌───────┐ ┌───────┐ ┌───────┐ ││
                    │  │  │Chrome1│ │Chrome2│ │Chrome3│ ││
                    │  │  └───────┘ └───────┘ └───────┘ ││
                    │  └─────────────────────────────────┘│
                    └─────────────────────────────────────┘
```

## 다음 단계

- [[02-ecosystem|에코시스템]] - 관련 기술 및 비교
- [[04-learning/01-rest-api|REST API 기본 사용]] - 첫 번째 실습
