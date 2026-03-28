# Browserless 치트시트

## Docker 명령어

```bash
# 기본 실행
docker run -p 3000:3000 ghcr.io/browserless/chromium

# 백그라운드 실행
docker run -d -p 3000:3000 --name browserless ghcr.io/browserless/chromium

# 환경 변수와 함께 실행
docker run -d -p 3000:3000 \
  -e "CONCURRENT=10" \
  -e "TIMEOUT=60000" \
  -e "TOKEN=my-token" \
  --shm-size=2gb \
  ghcr.io/browserless/chromium

# 로그 확인
docker logs -f browserless

# 컨테이너 중지/삭제
docker stop browserless && docker rm browserless
```

## REST API

### 스크린샷

```bash
# 기본 스크린샷
curl -X POST http://localhost:3000/screenshot \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}' \
  --output screenshot.png

# 전체 페이지
curl -X POST http://localhost:3000/screenshot \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "options": {"fullPage": true}}' \
  --output full.png

# 모바일 뷰
curl -X POST http://localhost:3000/screenshot \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "viewport": {"width": 375, "height": 812, "isMobile": true}}' \
  --output mobile.png
```

### PDF

```bash
# 기본 PDF
curl -X POST http://localhost:3000/pdf \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}' \
  --output document.pdf

# A4 + 배경 인쇄
curl -X POST http://localhost:3000/pdf \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "options": {"format": "A4", "printBackground": true}}' \
  --output print.pdf
```

### 콘텐츠/스크래핑

```bash
# HTML 콘텐츠
curl -X POST http://localhost:3000/content \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# 데이터 스크래핑
curl -X POST http://localhost:3000/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "elements": [{"selector": "h1", "name": "title"}]}'
```

## Puppeteer

### 연결

```javascript
const puppeteer = require('puppeteer-core');

// 기본 연결
const browser = await puppeteer.connect({
  browserWSEndpoint: 'ws://localhost:3000'
});

// 토큰 인증
const browser = await puppeteer.connect({
  browserWSEndpoint: 'ws://localhost:3000?token=my-token'
});
```

### 기본 작업

```javascript
const page = await browser.newPage();

// 페이지 이동
await page.goto('https://example.com', { waitUntil: 'networkidle2' });

// 뷰포트 설정
await page.setViewport({ width: 1920, height: 1080 });

// 스크린샷
await page.screenshot({ path: 'screenshot.png', fullPage: true });

// PDF
await page.pdf({ path: 'document.pdf', format: 'A4' });

// HTML 콘텐츠
const html = await page.content();

// 제목
const title = await page.title();

// 연결 종료
await browser.close();
```

### 요소 조작

```javascript
// 클릭
await page.click('button.submit');

// 입력
await page.type('#input', 'text');

// 선택
await page.select('select#dropdown', 'option-value');

// 텍스트 추출
const text = await page.$eval('h1', el => el.textContent);

// 다중 요소
const items = await page.$$eval('.item', els => els.map(el => el.textContent));

// 요소 존재 확인
const exists = await page.$('.element') !== null;
```

### 대기

```javascript
// 셀렉터 대기
await page.waitForSelector('.loaded');

// 네비게이션 대기
await page.waitForNavigation();

// 함수 대기
await page.waitForFunction(() => window.loaded === true);

// 시간 대기
await page.waitForTimeout(1000);
```

## Playwright

### 연결

```javascript
const { chromium } = require('playwright');

const browser = await chromium.connect({
  wsEndpoint: 'ws://localhost:3000/chromium/playwright'
});

const context = await browser.newContext();
const page = await context.newPage();
```

### 기본 작업

```javascript
// 페이지 이동
await page.goto('https://example.com');

// 클릭 (자동 대기)
await page.click('button');

// 입력
await page.fill('#input', 'text');

// 텍스트 추출
const text = await page.textContent('h1');

// 스크린샷
await page.screenshot({ path: 'screenshot.png' });

// 스토리지 상태 저장
await context.storageState({ path: 'state.json' });
```

### 스토리지 상태 복원

```javascript
const context = await browser.newContext({
  storageState: 'state.json'
});
```

## 쿠키 관리

### Puppeteer

```javascript
// 쿠키 저장
const cookies = await page.cookies();
fs.writeFileSync('cookies.json', JSON.stringify(cookies));

// 쿠키 복원
const cookies = JSON.parse(fs.readFileSync('cookies.json'));
await page.setCookie(...cookies);
```

### Playwright

```javascript
// 저장
await context.storageState({ path: 'state.json' });

// 복원
const context = await browser.newContext({
  storageState: 'state.json'
});
```

## BrowserQL

```graphql
# 기본 쿼리
mutation {
  goto(url: "https://example.com") {
    status
  }
  screenshot {
    base64
  }
}

# 클릭 및 입력
mutation {
  goto(url: "https://example.com/login") { status }
  type(selector: "#username", text: "user") { selector }
  type(selector: "#password", text: "pass") { selector }
  click(selector: "#login", waitForNavigation: true) { selector }
}
```

## 환경 변수

| 변수 | 설명 | 기본값 |
|------|------|--------|
| `CONCURRENT` | 동시 브라우저 수 | 10 |
| `QUEUED` | 대기열 크기 | 10 |
| `TIMEOUT` | 타임아웃 (ms) | 30000 |
| `TOKEN` | API 토큰 | - |
| `PREBOOT_CHROME` | 미리 시작 | false |
| `MAX_PAYLOAD_SIZE` | 최대 요청 크기 | 5mb |

## 자주 쓰는 패턴

### 재시도 로직

```javascript
async function withRetry(fn, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      return await fn();
    } catch (e) {
      if (i === retries - 1) throw e;
      await new Promise(r => setTimeout(r, 1000 * (i + 1)));
    }
  }
}
```

### 에러 처리

```javascript
try {
  await page.goto(url, { timeout: 30000 });
} catch (error) {
  await page.screenshot({ path: 'error.png' });
  throw error;
} finally {
  await browser.close();
}
```

### 리소스 차단

```javascript
await page.setRequestInterception(true);
page.on('request', req => {
  if (['image', 'font'].includes(req.resourceType())) {
    req.abort();
  } else {
    req.continue();
  }
});
```

### 콘솔 로그 캡처

```javascript
page.on('console', msg => console.log(`Browser: ${msg.text()}`));
page.on('pageerror', err => console.error(`Page error: ${err}`));
```

## 문제 해결

| 문제 | 해결 |
|------|------|
| 메모리 부족 | `--shm-size=2gb` 추가 |
| 타임아웃 | `TIMEOUT` 증가 |
| 연결 거부 | `CONCURRENT` 확인 |
| 봇 탐지 | BrowserQL 또는 Stealth 사용 |
| 권한 오류 | `--cap-add=SYS_ADMIN` |

## 유용한 링크

- 공식 문서: https://docs.browserless.io
- GitHub: https://github.com/browserless/browserless
- Puppeteer 문서: https://pptr.dev
- Playwright 문서: https://playwright.dev
