# Function API - 커스텀 코드 실행

## 개요

Browserless의 Function API를 사용하면 서버에서 커스텀 JavaScript 코드를 실행할 수 있습니다. 복잡한 스크래핑 로직이나 데이터 처리를 브라우저 컨텍스트에서 직접 수행할 수 있습니다.

## 기본 사용법

### 엔드포인트

```
POST http://localhost:3000/function
```

### 요청 구조

```json
{
  "code": "JavaScript 코드 문자열",
  "context": {
    "변수명": "값"
  }
}
```

### 첫 번째 Function 실행

```bash
curl -X POST http://localhost:3000/function \
  -H "Content-Type: application/json" \
  -d '{
    "code": "export default async function({ page }) { await page.goto(\"https://example.com\"); return await page.title(); }"
  }'
```

응답:
```json
{
  "data": "Example Domain"
}
```

## Function 코드 구조

### 기본 템플릿

```javascript
export default async function({ page, context }) {
  // page: Puppeteer Page 객체
  // context: 요청에서 전달된 컨텍스트 데이터

  await page.goto('https://example.com');

  // 결과 반환
  return {
    title: await page.title(),
    url: page.url()
  };
}
```

### 컨텍스트 사용

```javascript
// 요청
{
  "code": "...",
  "context": {
    "url": "https://example.com",
    "selector": ".article"
  }
}

// Function 코드
export default async function({ page, context }) {
  const { url, selector } = context;

  await page.goto(url);

  const elements = await page.$$eval(selector, els =>
    els.map(el => el.textContent)
  );

  return elements;
}
```

## 실전 예제

### 예제 1: 웹 스크래핑

```javascript
export default async function({ page, context }) {
  const { url } = context;

  await page.goto(url, { waitUntil: 'networkidle2' });

  // 데이터 추출
  const data = await page.evaluate(() => {
    const articles = document.querySelectorAll('.article');

    return Array.from(articles).map(article => ({
      title: article.querySelector('h2')?.textContent?.trim(),
      summary: article.querySelector('p')?.textContent?.trim(),
      link: article.querySelector('a')?.href
    }));
  });

  return {
    url,
    count: data.length,
    articles: data
  };
}
```

curl 요청:
```bash
curl -X POST http://localhost:3000/function \
  -H "Content-Type: application/json" \
  -d '{
    "code": "export default async function({ page, context }) { const { url } = context; await page.goto(url, { waitUntil: \"networkidle2\" }); const data = await page.evaluate(() => { const articles = document.querySelectorAll(\".article\"); return Array.from(articles).map(article => ({ title: article.querySelector(\"h2\")?.textContent?.trim(), link: article.querySelector(\"a\")?.href })); }); return { url, count: data.length, articles: data }; }",
    "context": {
      "url": "https://news.ycombinator.com"
    }
  }'
```

### 예제 2: 폼 자동 제출

```javascript
export default async function({ page, context }) {
  const { formUrl, formData } = context;

  await page.goto(formUrl);

  // 폼 필드 입력
  for (const [selector, value] of Object.entries(formData)) {
    await page.type(selector, value);
  }

  // 제출 버튼 클릭
  await Promise.all([
    page.waitForNavigation(),
    page.click('button[type="submit"]')
  ]);

  // 결과 확인
  const successMessage = await page.$eval('.success-message', el => el.textContent)
    .catch(() => null);

  return {
    success: !!successMessage,
    message: successMessage,
    finalUrl: page.url()
  };
}
```

### 예제 3: 로그인 후 데이터 수집

```javascript
export default async function({ page, context }) {
  const { loginUrl, credentials, targetUrl } = context;

  // 로그인
  await page.goto(loginUrl);
  await page.type('#username', credentials.username);
  await page.type('#password', credentials.password);

  await Promise.all([
    page.waitForNavigation(),
    page.click('#login-button')
  ]);

  // 로그인 확인
  const isLoggedIn = await page.$('.user-menu') !== null;

  if (!isLoggedIn) {
    return { success: false, error: '로그인 실패' };
  }

  // 타겟 페이지로 이동
  await page.goto(targetUrl);

  // 데이터 수집
  const data = await page.evaluate(() => {
    return {
      username: document.querySelector('.username')?.textContent,
      balance: document.querySelector('.balance')?.textContent,
      orders: Array.from(document.querySelectorAll('.order')).map(order => ({
        id: order.querySelector('.order-id')?.textContent,
        status: order.querySelector('.order-status')?.textContent
      }))
    };
  });

  return { success: true, data };
}
```

### 예제 4: 스크린샷과 PDF 생성

```javascript
export default async function({ page, context }) {
  const { url, options = {} } = context;

  await page.setViewport({
    width: options.width || 1920,
    height: options.height || 1080
  });

  await page.goto(url, { waitUntil: 'networkidle0' });

  // 스크린샷
  const screenshot = await page.screenshot({
    fullPage: options.fullPage || false,
    encoding: 'base64'
  });

  // PDF
  const pdf = await page.pdf({
    format: 'A4',
    printBackground: true
  });

  return {
    screenshot: screenshot,
    pdf: pdf.toString('base64'),
    title: await page.title()
  };
}
```

### 예제 5: 무한 스크롤 처리

```javascript
export default async function({ page, context }) {
  const { url, maxScrolls = 5, itemSelector } = context;

  await page.goto(url, { waitUntil: 'networkidle2' });

  let previousHeight = 0;
  let scrollCount = 0;
  let items = [];

  while (scrollCount < maxScrolls) {
    // 현재 아이템 수집
    const newItems = await page.$$eval(itemSelector, els =>
      els.map(el => el.textContent?.trim())
    );

    items = [...new Set([...items, ...newItems])];

    // 스크롤
    const currentHeight = await page.evaluate(() => {
      window.scrollTo(0, document.body.scrollHeight);
      return document.body.scrollHeight;
    });

    // 더 이상 스크롤할 내용이 없으면 종료
    if (currentHeight === previousHeight) {
      break;
    }

    previousHeight = currentHeight;
    scrollCount++;

    // 콘텐츠 로딩 대기
    await page.waitForTimeout(2000);
  }

  return {
    totalItems: items.length,
    scrollCount,
    items
  };
}
```

## 고급 기능

### 네트워크 인터셉트

```javascript
export default async function({ page, context }) {
  const apiResponses = [];

  // API 응답 캡처
  page.on('response', async response => {
    if (response.url().includes('/api/')) {
      try {
        const json = await response.json();
        apiResponses.push({
          url: response.url(),
          status: response.status(),
          data: json
        });
      } catch (e) {
        // JSON이 아닌 응답 무시
      }
    }
  });

  await page.goto(context.url, { waitUntil: 'networkidle0' });

  return {
    pageTitle: await page.title(),
    apiCalls: apiResponses
  };
}
```

### 리소스 차단

```javascript
export default async function({ page, context }) {
  // 이미지, 폰트, 스타일시트 차단 (성능 향상)
  await page.setRequestInterception(true);

  page.on('request', request => {
    const resourceType = request.resourceType();

    if (['image', 'font', 'stylesheet'].includes(resourceType)) {
      request.abort();
    } else {
      request.continue();
    }
  });

  await page.goto(context.url);

  return await page.content();
}
```

### 에러 처리

```javascript
export default async function({ page, context }) {
  const errors = [];

  // 페이지 에러 캡처
  page.on('pageerror', error => {
    errors.push({ type: 'pageerror', message: error.message });
  });

  page.on('error', error => {
    errors.push({ type: 'error', message: error.message });
  });

  page.on('console', msg => {
    if (msg.type() === 'error') {
      errors.push({ type: 'console', message: msg.text() });
    }
  });

  try {
    await page.goto(context.url, { timeout: 30000 });

    const result = await page.evaluate(() => {
      // 데이터 추출 로직
      return document.title;
    });

    return {
      success: true,
      result,
      errors: errors.length > 0 ? errors : null
    };
  } catch (error) {
    return {
      success: false,
      error: error.message,
      pageErrors: errors
    };
  }
}
```

### 다중 페이지 처리

```javascript
export default async function({ page, browser, context }) {
  const { urls } = context;
  const results = [];

  for (const url of urls) {
    const newPage = await browser.newPage();

    try {
      await newPage.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });

      const title = await newPage.title();
      const content = await newPage.$eval('body', el => el.innerText.slice(0, 500));

      results.push({
        url,
        success: true,
        title,
        preview: content
      });
    } catch (error) {
      results.push({
        url,
        success: false,
        error: error.message
      });
    } finally {
      await newPage.close();
    }
  }

  return results;
}
```

## Node.js 클라이언트

### Function 실행 래퍼

```javascript
const axios = require('axios');

class BrowserlessFunction {
  constructor(endpoint = 'http://localhost:3000') {
    this.endpoint = endpoint;
  }

  async run(code, context = {}) {
    try {
      const response = await axios.post(`${this.endpoint}/function`, {
        code: code.toString(),
        context
      }, {
        timeout: 60000
      });

      return response.data;
    } catch (error) {
      if (error.response) {
        throw new Error(`Function 실행 실패: ${error.response.data.error}`);
      }
      throw error;
    }
  }

  // 파일에서 코드 로드
  async runFile(filePath, context = {}) {
    const fs = require('fs');
    const code = fs.readFileSync(filePath, 'utf8');
    return this.run(code, context);
  }
}

// 사용
const bf = new BrowserlessFunction();

const scrapeCode = `
export default async function({ page, context }) {
  await page.goto(context.url);
  return await page.title();
}
`;

const result = await bf.run(scrapeCode, { url: 'https://example.com' });
console.log(result);
```

### 배치 처리

```javascript
async function batchScrape(urls, scrapeFunction) {
  const bf = new BrowserlessFunction();

  const code = `
    export default async function({ page, context }) {
      const results = [];

      for (const url of context.urls) {
        try {
          await page.goto(url, { waitUntil: 'networkidle2' });
          results.push({
            url,
            success: true,
            title: await page.title()
          });
        } catch (error) {
          results.push({
            url,
            success: false,
            error: error.message
          });
        }
      }

      return results;
    }
  `;

  return bf.run(code, { urls });
}

// 사용
const urls = [
  'https://example.com',
  'https://github.com',
  'https://google.com'
];

const results = await batchScrape(urls);
console.log(results);
```

## 성능 최적화

### 팁 1: 불필요한 리소스 차단

```javascript
export default async function({ page, context }) {
  await page.setRequestInterception(true);

  page.on('request', request => {
    const blockedTypes = ['image', 'font', 'stylesheet', 'media'];
    if (blockedTypes.includes(request.resourceType())) {
      request.abort();
    } else {
      request.continue();
    }
  });

  // ...
}
```

### 팁 2: 적절한 대기 전략

```javascript
// 나쁜 예: 고정 대기
await page.waitForTimeout(5000);

// 좋은 예: 조건 기반 대기
await page.waitForSelector('.content-loaded');

// 더 좋은 예: 네트워크 안정화 대기
await page.goto(url, { waitUntil: 'networkidle0' });
```

### 팁 3: 메모리 관리

```javascript
export default async function({ page, browser, context }) {
  const pages = [];

  try {
    for (const url of context.urls) {
      const p = await browser.newPage();
      pages.push(p);
      // 작업...
    }
  } finally {
    // 페이지 정리
    for (const p of pages) {
      await p.close();
    }
  }
}
```

## 디버깅

### 스크린샷으로 디버깅

```javascript
export default async function({ page, context }) {
  try {
    await page.goto(context.url);
    await page.click('.non-existent');
  } catch (error) {
    const screenshot = await page.screenshot({ encoding: 'base64' });
    return {
      error: error.message,
      debugScreenshot: screenshot
    };
  }
}
```

### 콘솔 로그 수집

```javascript
export default async function({ page, context }) {
  const logs = [];

  page.on('console', msg => {
    logs.push({
      type: msg.type(),
      text: msg.text()
    });
  });

  await page.goto(context.url);

  return { logs };
}
```

## 다음 단계

- [[../05-projects|실전 프로젝트]] - Function API 활용 프로젝트
- [[../cheatsheet|치트시트]] - 빠른 참조
