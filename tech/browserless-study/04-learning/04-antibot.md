# 안티봇 우회 - BrowserQL

## 개요

많은 웹사이트들이 봇 탐지 시스템을 사용합니다. BrowserQL은 Browserless의 고급 안티봇 우회 기술로, CAPTCHA 해결과 봇 탐지 회피를 지원합니다.

## 봇 탐지 원리

### 일반적인 탐지 방법

```
┌─────────────────────────────────────────────────────────┐
│                  봇 탐지 시스템                          │
├─────────────────────────────────────────────────────────┤
│  1. 브라우저 지문 (Fingerprinting)                      │
│     - navigator.webdriver 속성                          │
│     - User-Agent 일관성                                 │
│     - 플러그인/폰트 목록                                │
│                                                         │
│  2. 행동 분석 (Behavior Analysis)                       │
│     - 마우스 움직임 패턴                                │
│     - 키보드 입력 속도                                  │
│     - 페이지 스크롤 패턴                                │
│                                                         │
│  3. 네트워크 분석                                       │
│     - IP 평판                                          │
│     - 요청 속도/패턴                                    │
│     - TLS 지문                                         │
│                                                         │
│  4. CAPTCHA                                            │
│     - reCAPTCHA                                        │
│     - hCaptcha                                         │
│     - 커스텀 챌린지                                     │
└─────────────────────────────────────────────────────────┘
```

### 탐지되는 신호들

| 신호 | 일반 브라우저 | 헤드리스 브라우저 |
|------|-------------|-----------------|
| `navigator.webdriver` | undefined | true |
| 플러그인 수 | 3+ | 0 |
| 언어 설정 | 지역 기반 | en-US |
| 화면 해상도 | 다양 | 고정 |
| WebGL 렌더러 | GPU 이름 | SwiftShader |

## BrowserQL 소개

### BrowserQL이란?

BrowserQL은 Browserless에서 제공하는 GraphQL 기반 브라우저 자동화 언어입니다. 안티봇 우회에 최적화되어 있습니다.

### 주요 특징

- **Stealth 모드 내장**: 봇 탐지 회피
- **인간 행동 시뮬레이션**: 자연스러운 마우스/키보드
- **CAPTCHA 해결**: reCAPTCHA, hCaptcha 지원
- **프록시 통합**: IP 우회

## BrowserQL 기본 사용

### 엔드포인트

```bash
# BrowserQL 엔드포인트
POST http://localhost:3000/chromium/bql

# Cloud 서비스
POST https://chrome.browserless.io/chromium/bql?token=YOUR_TOKEN
```

### 기본 쿼리 구조

```graphql
mutation Screenshot {
  goto(url: "https://example.com", waitUntil: networkIdle) {
    status
    time
  }

  screenshot {
    base64
  }
}
```

### curl로 실행

```bash
curl -X POST http://localhost:3000/chromium/bql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { goto(url: \"https://example.com\") { status } screenshot { base64 } }"
  }' | jq -r '.data.screenshot.base64' | base64 -d > screenshot.png
```

## BrowserQL 쿼리 예제

### 페이지 이동 및 스크린샷

```graphql
mutation NavigateAndCapture {
  goto(
    url: "https://example.com"
    waitUntil: networkIdle
    timeout: 30000
  ) {
    status
    url
    time
  }

  screenshot(
    fullPage: true
    type: png
    quality: 80
  ) {
    base64
  }
}
```

### 요소 클릭 및 입력

```graphql
mutation LoginFlow {
  goto(url: "https://example.com/login") {
    status
  }

  type(
    selector: "#username"
    text: "myuser"
    delay: 100
  ) {
    selector
  }

  type(
    selector: "#password"
    text: "mypassword"
    delay: 100
  ) {
    selector
  }

  click(
    selector: "#login-button"
    waitForNavigation: true
  ) {
    selector
  }

  screenshot {
    base64
  }
}
```

### 데이터 추출

```graphql
mutation ScrapeData {
  goto(url: "https://news.ycombinator.com") {
    status
  }

  elements: html(selector: ".titleline > a") {
    text
    attributes {
      name
      value
    }
  }
}
```

### 스크롤 및 대기

```graphql
mutation ScrollAndWait {
  goto(url: "https://example.com/infinite-scroll") {
    status
  }

  scroll(
    direction: down
    amount: 1000
  ) {
    currentPosition
  }

  wait(timeout: 2000) {
    time
  }

  scroll(
    direction: down
    amount: 1000
  ) {
    currentPosition
  }

  html(selector: ".loaded-items") {
    text
  }
}
```

## Stealth 모드

### 자동 스텔스 기능

BrowserQL은 자동으로 다음을 처리합니다:

```
- navigator.webdriver 숨김
- Chrome DevTools 프로토콜 헤더 제거
- 일반적인 브라우저 지문 에뮬레이션
- WebGL 벤더/렌더러 스푸핑
- 플러그인 목록 에뮬레이션
```

### 커스텀 지문 설정

```graphql
mutation WithCustomFingerprint {
  goto(
    url: "https://example.com"
    options: {
      userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
      viewport: {
        width: 1920
        height: 1080
      }
      locale: "ko-KR"
      timezone: "Asia/Seoul"
    }
  ) {
    status
  }
}
```

## CAPTCHA 해결

### reCAPTCHA v2

```graphql
mutation SolveRecaptcha {
  goto(url: "https://example.com/with-recaptcha") {
    status
  }

  solve(
    type: recaptcha
    timeout: 120000
  ) {
    solved
    time
  }

  click(selector: "#submit-button") {
    selector
  }
}
```

### hCaptcha

```graphql
mutation SolveHcaptcha {
  goto(url: "https://example.com/with-hcaptcha") {
    status
  }

  solve(
    type: hcaptcha
    timeout: 120000
  ) {
    solved
    time
  }
}
```

### CAPTCHA 해결 옵션

| 옵션 | 설명 |
|------|------|
| `type` | captcha 종류 (recaptcha, hcaptcha) |
| `timeout` | 최대 대기 시간 |
| `retries` | 재시도 횟수 |

> **참고**: CAPTCHA 해결은 Cloud 서비스에서만 사용 가능하며, 추가 비용이 발생할 수 있습니다.

## 프록시 사용

### 프록시 설정

```graphql
mutation WithProxy {
  goto(
    url: "https://example.com"
    options: {
      proxy: {
        server: "http://proxy.example.com:8080"
        username: "user"
        password: "pass"
      }
    }
  ) {
    status
  }
}
```

### 프록시 타입

| 타입 | 설명 | 사용 사례 |
|------|------|----------|
| 데이터센터 | 빠름, 저렴 | 일반 스크래핑 |
| 주거용 | 실제 IP | 안티봇 우회 |
| 모바일 | 모바일 IP | 모바일 전용 사이트 |

## Puppeteer/Playwright + Stealth

### Puppeteer Stealth 플러그인

```javascript
const puppeteer = require('puppeteer-core');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const puppeteerExtra = require('puppeteer-extra');

puppeteerExtra.use(StealthPlugin());

async function stealthBrowsing() {
  const browser = await puppeteerExtra.connect({
    browserWSEndpoint: 'ws://localhost:3000'
  });

  const page = await browser.newPage();
  await page.goto('https://bot.sannysoft.com');
  await page.screenshot({ path: 'stealth-test.png' });

  await browser.close();
}
```

### Playwright Stealth

```javascript
const { chromium } = require('playwright');

async function playwrightStealth() {
  const browser = await chromium.connect({
    wsEndpoint: 'ws://localhost:3000/chromium/playwright'
  });

  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    viewport: { width: 1920, height: 1080 },
    locale: 'ko-KR',
    timezoneId: 'Asia/Seoul'
  });

  // JavaScript로 webdriver 속성 숨김
  await context.addInitScript(() => {
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    });
  });

  const page = await context.newPage();
  await page.goto('https://example.com');

  await browser.close();
}
```

## 인간 행동 시뮬레이션

### 마우스 움직임

```graphql
mutation HumanLikeMouse {
  goto(url: "https://example.com") {
    status
  }

  # 인간처럼 마우스 이동
  mouse(
    action: move
    x: 500
    y: 300
    steps: 25
  ) {
    x
    y
  }

  wait(timeout: 500) { time }

  mouse(
    action: click
    x: 500
    y: 300
  ) {
    x
    y
  }
}
```

### 타이핑 딜레이

```graphql
mutation HumanLikeTyping {
  type(
    selector: "#search"
    text: "검색어"
    delay: 150  # 각 키 사이 딜레이 (ms)
  ) {
    selector
  }
}
```

### 스크롤 패턴

```graphql
mutation HumanLikeScroll {
  goto(url: "https://example.com") {
    status
  }

  # 천천히 스크롤
  scroll(direction: down, amount: 300) { currentPosition }
  wait(timeout: 1000) { time }

  scroll(direction: down, amount: 500) { currentPosition }
  wait(timeout: 800) { time }

  scroll(direction: up, amount: 200) { currentPosition }
  wait(timeout: 1200) { time }
}
```

## 우회 전략 정리

### 단계별 접근

```
1단계: 기본 설정
├── User-Agent 변경
├── Viewport 설정
└── 언어/타임존 설정

2단계: Stealth 적용
├── webdriver 속성 숨김
├── 플러그인 에뮬레이션
└── WebGL 스푸핑

3단계: 행동 시뮬레이션
├── 마우스 움직임
├── 타이핑 딜레이
└── 랜덤 대기

4단계: 프록시 사용
├── 주거용 프록시
├── IP 로테이션
└── 지역별 프록시

5단계: CAPTCHA 해결
├── 자동 해결 서비스
└── 수동 해결 대기
```

### 사이트별 대응

| 보호 수준 | 예시 사이트 | 권장 전략 |
|----------|-----------|----------|
| 낮음 | 일반 뉴스 사이트 | 기본 설정만 |
| 중간 | 쇼핑몰 | Stealth + 딜레이 |
| 높음 | 금융 서비스 | 프록시 + CAPTCHA |
| 매우 높음 | Cloudflare | BrowserQL + 주거용 프록시 |

## 윤리적 고려사항

### 스크래핑 원칙

1. **robots.txt 확인**: 크롤링 정책 준수
2. **요청 제한**: 서버 부하 최소화
3. **법적 검토**: 이용약관 확인
4. **개인정보**: 민감 데이터 수집 주의

### Best Practices

```javascript
// 요청 간 딜레이
const delay = ms => new Promise(r => setTimeout(r, ms));

async function ethicalScraping(urls) {
  for (const url of urls) {
    await scrapePage(url);
    await delay(2000 + Math.random() * 3000); // 2-5초 랜덤 대기
  }
}
```

## 다음 단계

- [[05-sessions|Persistent Sessions]] - 로그인 세션 유지
- [[06-function-api|Function API]] - 커스텀 코드 실행
