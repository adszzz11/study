# Puppeteer/Playwright 연결

## 개요

Browserless는 WebSocket을 통해 Puppeteer와 Playwright를 원격 브라우저에 연결할 수 있습니다. 로컬에 Chrome을 설치하지 않고도 브라우저 자동화를 실행할 수 있습니다.

## Puppeteer 연결

### 설치

```bash
npm install puppeteer-core
# 또는
npm install puppeteer  # Chromium 포함
```

> **참고**: `puppeteer-core`는 Chromium을 포함하지 않아 용량이 작습니다. Browserless 사용 시 권장합니다.

### 기본 연결

```javascript
const puppeteer = require('puppeteer-core');

async function main() {
  // Browserless에 연결
  const browser = await puppeteer.connect({
    browserWSEndpoint: 'ws://localhost:3000'
  });

  const page = await browser.newPage();
  await page.goto('https://example.com');

  // 스크린샷
  await page.screenshot({ path: 'screenshot.png' });

  // 연결 종료
  await browser.close();
}

main();
```

### 인증 토큰 사용 (Cloud)

```javascript
const browser = await puppeteer.connect({
  browserWSEndpoint: 'wss://chrome.browserless.io?token=YOUR_API_TOKEN'
});
```

### 스크린샷 및 PDF

```javascript
const puppeteer = require('puppeteer-core');

async function captureScreenshotAndPdf() {
  const browser = await puppeteer.connect({
    browserWSEndpoint: 'ws://localhost:3000'
  });

  const page = await browser.newPage();

  // 뷰포트 설정
  await page.setViewport({ width: 1920, height: 1080 });

  await page.goto('https://example.com', {
    waitUntil: 'networkidle0'
  });

  // 스크린샷
  await page.screenshot({
    path: 'fullpage.png',
    fullPage: true
  });

  // PDF
  await page.pdf({
    path: 'document.pdf',
    format: 'A4',
    printBackground: true
  });

  await browser.close();
}
```

### 데이터 스크래핑

```javascript
const puppeteer = require('puppeteer-core');

async function scrapeHackerNews() {
  const browser = await puppeteer.connect({
    browserWSEndpoint: 'ws://localhost:3000'
  });

  const page = await browser.newPage();
  await page.goto('https://news.ycombinator.com');

  // 데이터 추출
  const articles = await page.evaluate(() => {
    const items = document.querySelectorAll('.athing');
    return Array.from(items).slice(0, 10).map(item => {
      const titleEl = item.querySelector('.titleline > a');
      return {
        title: titleEl?.textContent,
        link: titleEl?.href
      };
    });
  });

  console.log(articles);
  await browser.close();
}
```

### 폼 입력 및 클릭

```javascript
async function loginExample() {
  const browser = await puppeteer.connect({
    browserWSEndpoint: 'ws://localhost:3000'
  });

  const page = await browser.newPage();
  await page.goto('https://example.com/login');

  // 입력
  await page.type('#username', 'myuser');
  await page.type('#password', 'mypassword');

  // 클릭 및 네비게이션 대기
  await Promise.all([
    page.waitForNavigation(),
    page.click('#login-button')
  ]);

  // 로그인 후 작업...

  await browser.close();
}
```

## Playwright 연결

### 설치

```bash
npm install playwright
# 또는 특정 브라우저만
npm install playwright-chromium
```

### 기본 연결

```javascript
const { chromium } = require('playwright');

async function main() {
  // Browserless에 연결
  const browser = await chromium.connect({
    wsEndpoint: 'ws://localhost:3000/chromium/playwright'
  });

  const context = await browser.newContext();
  const page = await context.newPage();

  await page.goto('https://example.com');
  await page.screenshot({ path: 'screenshot.png' });

  await browser.close();
}

main();
```

### 컨텍스트 옵션

```javascript
const { chromium } = require('playwright');

async function withContext() {
  const browser = await chromium.connect({
    wsEndpoint: 'ws://localhost:3000/chromium/playwright'
  });

  // 브라우저 컨텍스트 생성 (시크릿 모드처럼 동작)
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    userAgent: 'Custom User Agent',
    locale: 'ko-KR',
    timezoneId: 'Asia/Seoul',
    geolocation: { latitude: 37.5665, longitude: 126.9780 },
    permissions: ['geolocation']
  });

  const page = await context.newPage();
  await page.goto('https://example.com');

  await context.close();
  await browser.close();
}
```

### 자동 대기 활용

```javascript
const { chromium } = require('playwright');

async function autoWaitExample() {
  const browser = await chromium.connect({
    wsEndpoint: 'ws://localhost:3000/chromium/playwright'
  });

  const page = await browser.newPage();
  await page.goto('https://spa-example.com');

  // Playwright는 자동으로 요소가 나타날 때까지 대기
  await page.click('button.load-more');  // 자동 대기

  // 특정 조건 대기
  await page.waitForSelector('.loaded-content');

  // 네트워크 요청 대기
  await page.waitForResponse(response =>
    response.url().includes('/api/data')
  );

  const data = await page.textContent('.data-container');
  console.log(data);

  await browser.close();
}
```

### 네트워크 인터셉트

```javascript
const { chromium } = require('playwright');

async function interceptNetwork() {
  const browser = await chromium.connect({
    wsEndpoint: 'ws://localhost:3000/chromium/playwright'
  });

  const page = await browser.newPage();

  // 이미지 차단 (성능 향상)
  await page.route('**/*.{png,jpg,jpeg,gif,webp}', route => route.abort());

  // API 응답 수정
  await page.route('**/api/data', async route => {
    const response = await route.fetch();
    const json = await response.json();
    json.modified = true;
    await route.fulfill({ json });
  });

  await page.goto('https://example.com');
  await browser.close();
}
```

## Puppeteer vs Playwright 비교

### 코드 비교

| 작업 | Puppeteer | Playwright |
|------|-----------|------------|
| 연결 | `puppeteer.connect({ browserWSEndpoint })` | `chromium.connect({ wsEndpoint })` |
| 페이지 생성 | `browser.newPage()` | `context.newPage()` |
| 요소 대기 | `page.waitForSelector()` | 자동 (또는 명시적) |
| 텍스트 입력 | `page.type()` | `page.fill()` |
| 클릭 | `page.click()` | `page.click()` |

### 기능 비교

```javascript
// Puppeteer: 셀렉터 대기 필요
await page.waitForSelector('.button');
await page.click('.button');

// Playwright: 자동 대기
await page.click('.button');  // 자동으로 대기
```

### 선택 가이드

**Puppeteer 선택 시**:
- Chrome/Chromium만 사용
- 기존 Puppeteer 코드 마이그레이션
- Google 에코시스템 선호

**Playwright 선택 시**:
- 멀티 브라우저 테스트 필요
- 자동 대기 기능 활용
- 모던 API 선호

## 공통 패턴

### 재시도 로직

```javascript
async function withRetry(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      console.log(`시도 ${i + 1} 실패: ${error.message}`);
      if (i === maxRetries - 1) throw error;
      await new Promise(r => setTimeout(r, 1000 * (i + 1)));
    }
  }
}

// 사용
await withRetry(async () => {
  const browser = await puppeteer.connect({ browserWSEndpoint: 'ws://localhost:3000' });
  // ...
});
```

### 에러 처리

```javascript
const puppeteer = require('puppeteer-core');

async function safeNavigation() {
  let browser;

  try {
    browser = await puppeteer.connect({
      browserWSEndpoint: 'ws://localhost:3000'
    });

    const page = await browser.newPage();

    page.on('error', err => console.error('Page error:', err));
    page.on('pageerror', err => console.error('Page JS error:', err));

    await page.goto('https://example.com', {
      timeout: 30000,
      waitUntil: 'networkidle2'
    });

    // 작업 수행...

  } catch (error) {
    console.error('Error:', error.message);
  } finally {
    if (browser) {
      await browser.close();
    }
  }
}
```

### 병렬 처리

```javascript
const puppeteer = require('puppeteer-core');

async function parallelScraping(urls) {
  const browser = await puppeteer.connect({
    browserWSEndpoint: 'ws://localhost:3000'
  });

  const results = await Promise.all(
    urls.map(async (url) => {
      const page = await browser.newPage();
      try {
        await page.goto(url, { waitUntil: 'networkidle2' });
        const title = await page.title();
        return { url, title, success: true };
      } catch (error) {
        return { url, error: error.message, success: false };
      } finally {
        await page.close();
      }
    })
  );

  await browser.close();
  return results;
}

// 사용
const urls = [
  'https://example.com',
  'https://github.com',
  'https://google.com'
];

parallelScraping(urls).then(console.log);
```

## 디버깅 팁

### 1. 스크린샷으로 디버깅

```javascript
// 에러 발생 시 스크린샷
try {
  await page.click('.non-existent');
} catch (error) {
  await page.screenshot({ path: 'debug-error.png' });
  throw error;
}
```

### 2. 콘솔 로그 캡처

```javascript
page.on('console', msg => {
  console.log(`Browser console: ${msg.type()}: ${msg.text()}`);
});
```

### 3. 네트워크 요청 로깅

```javascript
page.on('request', request => {
  console.log(`>> ${request.method()} ${request.url()}`);
});

page.on('response', response => {
  console.log(`<< ${response.status()} ${response.url()}`);
});
```

## 다음 단계

- [[03-docker-selfhost|Docker Self-hosted]] - 로컬 환경 최적화
- [[04-antibot|안티봇 우회]] - BrowserQL 학습
