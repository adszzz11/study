# Playwright 심층 스터디 가이드

> **한 줄 정의**: Microsoft가 개발한 크로스 브라우저 웹 테스트 및 자동화 프레임워크로, Chromium, Firefox, WebKit을 단일 API로 제어

---

## Part 1: 개요

### 1.1 정의 및 핵심 개념

**3줄 요약**:
1. Chrome, Firefox, Safari(WebKit)를 하나의 API로 자동화 - 크로스 브라우저 테스트 완벽 지원
2. 자동 대기(Auto-wait), 병렬 실행, 네트워크 가로채기 등 현대적인 테스트 기능 내장
3. TypeScript, JavaScript, Python, Java, C# 등 다양한 언어 지원

**핵심 키워드**: `#브라우저자동화` `#E2E테스트` `#웹스크래핑` `#크로스브라우저` `#Microsoft`

**Playwright vs 기존 도구**:

| 특징 | Playwright | Selenium | Puppeteer | Cypress |
|------|------------|----------|-----------|---------|
| 브라우저 | Chromium, Firefox, WebKit | 모든 브라우저 | Chromium만 | Chromium 위주 |
| 속도 | 매우 빠름 | 느림 | 빠름 | 빠름 |
| 자동 대기 | 내장 | 없음 | 부분적 | 내장 |
| 병렬 실행 | 내장 | 추가 설정 | 추가 설정 | 추가 설정 |
| 언어 | JS/TS/Python/Java/C# | 다수 | JS/TS | JS/TS만 |

### 1.2 Quick Start (30초 체험)

```bash
# 1. 설치 (Node.js)
npm init playwright@latest

# 또는 Python
pip install playwright
playwright install
```

```javascript
// example.spec.js - 첫 번째 테스트
const { test, expect } = require('@playwright/test');

test('구글 검색 테스트', async ({ page }) => {
    // 페이지 이동
    await page.goto('https://www.google.com');

    // 검색어 입력
    await page.fill('textarea[name="q"]', 'Playwright');

    // 검색 버튼 클릭 또는 Enter
    await page.keyboard.press('Enter');

    // 결과 확인
    await expect(page).toHaveTitle(/Playwright/);
});
```

```bash
# 3. 테스트 실행
npx playwright test

# UI 모드로 실행 (디버깅에 유용)
npx playwright test --ui
```

### 1.3 왜 Playwright인가?

**장점**:
- **크로스 브라우저**: 단일 코드로 Chrome, Firefox, Safari 테스트
- **자동 대기**: 요소가 준비될 때까지 자동으로 기다림 - Flaky 테스트 감소
- **강력한 디버깅**: Trace Viewer, VS Code 확장, UI 모드
- **빠른 실행**: 병렬 실행, 브라우저 컨텍스트 격리
- **네트워크 제어**: 요청 가로채기, 모킹 가능
- **모바일 에뮬레이션**: 디바이스별 테스트 지원

**단점**:
- Selenium 대비 작은 커뮤니티 (빠르게 성장 중)
- 레거시 브라우저(IE) 미지원
- 학습 곡선이 Cypress보다 약간 높음

**주요 사용 사례**:
- E2E(End-to-End) 테스트 자동화
- 웹 스크래핑/크롤링
- 시각적 회귀 테스트
- 성능 테스트
- PDF/스크린샷 생성

---

## Part 2: 생태계 파악

### 2.1 관련 기술/용어 맵

```
┌─────────────────────────────────────────────────────────────┐
│                    Playwright 생태계                         │
├─────────────────────────────────────────────────────────────┤
│  [Core]                                                      │
│  ├── Browser: Chromium, Firefox, WebKit 인스턴스             │
│  ├── BrowserContext: 독립된 브라우저 세션 (쿠키, 스토리지)     │
│  ├── Page: 단일 탭/페이지                                    │
│  └── Locator: 요소 선택자 (권장 방식)                         │
│                                                              │
│  [Test Runner]                                               │
│  ├── @playwright/test: 내장 테스트 러너                      │
│  ├── Fixtures: 테스트 환경 설정                              │
│  └── Reporters: 결과 리포팅 (HTML, JSON, JUnit)              │
│                                                              │
│  [Tools]                                                     │
│  ├── Codegen: 자동 코드 생성 (녹화)                          │
│  ├── Trace Viewer: 실행 추적/디버깅                          │
│  ├── VS Code Extension: IDE 통합                             │
│  └── Playwright MCP: AI 도구 통합                            │
│                                                              │
│  [언어별 패키지]                                              │
│  ├── playwright (Node.js)                                    │
│  ├── playwright-python (Python)                              │
│  ├── playwright-java (Java)                                  │
│  └── playwright-dotnet (C#)                                  │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 함께 자주 쓰이는 기술 스택

| 영역 | 기술 | 용도 |
|------|------|------|
| **CI/CD** | GitHub Actions, Jenkins | 자동화된 테스트 실행 |
| **리포팅** | Allure, HTML Reporter | 테스트 결과 시각화 |
| **모킹** | MSW (Mock Service Worker) | API 모킹 |
| **BDD** | Cucumber | 행위 주도 개발 |
| **헤드리스 서비스** | Browserless | 클라우드 브라우저 |

### 2.3 경쟁/대안 기술 비교

| 기준 | Playwright | Selenium | Puppeteer | Cypress |
|------|------------|----------|-----------|---------|
| **개발사** | Microsoft | 커뮤니티 | Google | Cypress.io |
| **출시** | 2020 | 2004 | 2017 | 2015 |
| **아키텍처** | WebSocket | HTTP/WebDriver | WebSocket | In-browser |
| **속도** | 빠름 | 느림 | 빠름 | 빠름 |
| **크로스 브라우저** | 완벽 | 완벽 | 제한적 | 제한적 |
| **추천 상황** | 새 프로젝트 | 레거시 지원 | Chrome 전용 | React/Vue 앱 |

**선택 가이드**:
- **Playwright**: 새 프로젝트, 크로스 브라우저 필수, 현대적인 DX
- **Selenium**: 레거시 브라우저 지원 필요, 기존 인프라 활용
- **Puppeteer**: Chrome 전용 스크래핑, 경량 필요
- **Cypress**: 프론트엔드 중심, 빠른 피드백 루프

### 2.4 최신 트렌드 및 동향 (2025)

- **Playwright MCP 서버**: AI 도구(Claude, Cursor)에서 Playwright 직접 사용
- **Component Testing**: React, Vue 컴포넌트 단위 테스트 지원 확대
- **AI 기반 선택자**: Locator 대신 자연어로 요소 선택 (실험적)
- **성능 향상**: 지속적인 실행 속도 개선
- **Cloud 통합**: Browserbase, Sauce Labs 등과의 연동 강화

---

## Part 3: 레퍼런스

### 3.1 공식 문서 및 필수 링크

| 리소스 | URL | 설명 |
|--------|-----|------|
| 🟢 공식 문서 | [playwright.dev](https://playwright.dev/) | 메인 문서 |
| 🟢 GitHub | [github.com/microsoft/playwright](https://github.com/microsoft/playwright) | 소스 코드 |
| 🟢 API Reference | [playwright.dev/docs/api/class-playwright](https://playwright.dev/docs/api/class-playwright) | API 레퍼런스 |
| 🟡 Python 문서 | [playwright.dev/python](https://playwright.dev/python/) | Python 버전 |
| 🟡 MCP 서버 | [github.com/microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) | AI 통합 |

### 3.2 추천 학습 자료

**🟢 입문**:
- [Playwright 공식 Getting Started](https://playwright.dev/docs/intro) - 설치부터 첫 테스트까지
- [BrowserStack Playwright Tutorial](https://www.browserstack.com/guide/playwright-tutorial) - 종합 튜토리얼

**🟡 중급**:
- [Checkly: Playwright Guide](https://www.checklyhq.com/docs/learn/playwright/) - 실전 가이드
- [Playwright 공식 Best Practices](https://playwright.dev/docs/best-practices) - 베스트 프랙티스

**🔴 고급**:
- [Playwright for Component Testing](https://playwright.dev/docs/test-components) - 컴포넌트 테스트
- [Playwright Trace Viewer](https://playwright.dev/docs/trace-viewer) - 고급 디버깅

### 3.3 커뮤니티 및 질문할 곳

- **Discord**: [Playwright Community](https://aka.ms/playwright-discord)
- **GitHub Issues**: [microsoft/playwright/issues](https://github.com/microsoft/playwright/issues)
- **Stack Overflow**: `[playwright]` 태그

### 3.4 실무 예제/오픈소스 프로젝트

- [Playwright Examples](https://github.com/microsoft/playwright/tree/main/examples) - 공식 예제
- [Awesome Playwright](https://github.com/mxschmitt/awesome-playwright) - 리소스 모음
- [Checkly](https://www.checklyhq.com/) - Playwright 기반 모니터링 서비스

---

## Part 4: 상세 학습 로드맵

### 4.1 기본 페이지 조작

📌 **핵심 개념**

Playwright의 기본 흐름: Browser → BrowserContext → Page → Locator

```
Browser (브라우저 프로세스)
  └── BrowserContext (독립된 세션)
        └── Page (탭/페이지)
              └── Locator (요소 참조)
```

💻 **코드 예제: 기본 조작 (Node.js)**

```javascript
const { chromium } = require('playwright');

(async () => {
    // 1. 브라우저 시작
    const browser = await chromium.launch({
        headless: false  // 브라우저 창 표시
    });

    // 2. 새 컨텍스트 (독립된 세션)
    const context = await browser.newContext();

    // 3. 새 페이지
    const page = await context.newPage();

    // 4. 페이지 이동
    await page.goto('https://example.com');

    // 5. 요소 찾기 (Locator 사용 - 권장)
    const heading = page.locator('h1');
    console.log(await heading.textContent());

    // 6. 클릭
    await page.locator('a').first().click();

    // 7. 입력
    await page.locator('input[type="text"]').fill('Hello Playwright');

    // 8. 스크린샷
    await page.screenshot({ path: 'screenshot.png' });

    // 9. 종료
    await browser.close();
})();
```

**Python 버전**:
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://example.com")

    # Locator 사용
    heading = page.locator("h1")
    print(heading.text_content())

    # 입력 및 클릭
    page.locator("input").fill("Hello")
    page.locator("button").click()

    # 스크린샷
    page.screenshot(path="screenshot.png")

    browser.close()
```

✅ **체크포인트**
- [ ] Browser, Context, Page의 계층 구조를 이해하는가?
- [ ] Locator를 사용해 요소를 찾을 수 있는가?
- [ ] `fill()`, `click()`, `goto()` 메서드를 사용할 수 있는가?

⚠️ **흔한 실수**
- `page.$()` 대신 `page.locator()` 사용 권장 (자동 재시도)
- `headless: true`가 기본값 - 디버깅 시 `false`로 설정

🔗 **더 알아보기**: [Pages and Frames](https://playwright.dev/docs/pages)

---

### 4.2 Locator 전략

📌 **핵심 개념**

Locator는 Playwright의 핵심 개념입니다. 자동 대기와 재시도가 내장되어 있어 안정적인 요소 선택이 가능합니다.

💻 **코드 예제: 다양한 Locator**

```javascript
const { test, expect } = require('@playwright/test');

test('Locator 예제', async ({ page }) => {
    await page.goto('https://demo.playwright.dev/todomvc');

    // 1. CSS 선택자
    const input = page.locator('.new-todo');

    // 2. 텍스트로 찾기 (권장)
    const button = page.getByRole('button', { name: 'Submit' });

    // 3. 역할(Role)로 찾기 (접근성 기반 - 가장 권장)
    const heading = page.getByRole('heading', { name: 'todos' });

    // 4. 레이블로 찾기 (폼 요소)
    const emailInput = page.getByLabel('Email');

    // 5. Placeholder로 찾기
    const searchInput = page.getByPlaceholder('Search...');

    // 6. Test ID로 찾기 (명시적)
    const customElement = page.getByTestId('submit-button');

    // 7. 텍스트로 찾기
    const link = page.getByText('Learn more');

    // 8. 체이닝 (부모 → 자식)
    const todoItem = page.locator('.todo-list')
                         .locator('li')
                         .filter({ hasText: 'Buy milk' });

    // 9. nth 선택
    const firstItem = page.locator('li').first();
    const secondItem = page.locator('li').nth(1);
    const lastItem = page.locator('li').last();

    // 10. 필터링
    const completedItems = page.locator('li').filter({
        has: page.locator('.completed')
    });
});
```

**Locator 우선순위 (권장순)**:
1. `getByRole()` - 접근성 기반, 가장 안정적
2. `getByLabel()` - 폼 요소
3. `getByPlaceholder()` - 입력 필드
4. `getByText()` - 텍스트 기반
5. `getByTestId()` - 명시적 테스트 ID
6. `locator()` - CSS/XPath (최후의 수단)

✅ **체크포인트**
- [ ] `getByRole()`을 사용할 수 있는가?
- [ ] Locator 체이닝으로 복잡한 요소를 찾을 수 있는가?
- [ ] `filter()`로 조건부 선택을 할 수 있는가?

⚠️ **흔한 실수**
- XPath보다 CSS 선택자가 더 빠름
- 동적 클래스명(`css-xxx123`)은 피할 것
- `data-testid` 속성 추가 권장

🔗 **더 알아보기**: [Locators](https://playwright.dev/docs/locators)

---

### 4.3 Assertions (검증)

📌 **핵심 개념**

`expect()`를 사용한 자동 재시도 Assertions로 안정적인 테스트 작성이 가능합니다.

💻 **코드 예제: 다양한 Assertions**

```javascript
const { test, expect } = require('@playwright/test');

test('Assertions 예제', async ({ page }) => {
    await page.goto('https://example.com');

    // 1. 페이지 제목 검증
    await expect(page).toHaveTitle('Example Domain');
    await expect(page).toHaveTitle(/Example/);  // 정규식

    // 2. URL 검증
    await expect(page).toHaveURL('https://example.com/');
    await expect(page).toHaveURL(/example/);

    // 3. 요소 가시성
    await expect(page.locator('h1')).toBeVisible();
    await expect(page.locator('.hidden')).toBeHidden();

    // 4. 텍스트 내용
    await expect(page.locator('h1')).toHaveText('Example Domain');
    await expect(page.locator('h1')).toContainText('Example');

    // 5. 입력 값
    await page.locator('input').fill('test');
    await expect(page.locator('input')).toHaveValue('test');

    // 6. 속성 검증
    await expect(page.locator('a')).toHaveAttribute('href', /iana/);

    // 7. 클래스 검증
    await expect(page.locator('div')).toHaveClass(/container/);

    // 8. 개수 검증
    await expect(page.locator('p')).toHaveCount(2);

    // 9. 활성화/비활성화
    await expect(page.locator('button')).toBeEnabled();
    await expect(page.locator('button.disabled')).toBeDisabled();

    // 10. 체크박스
    await expect(page.locator('input[type="checkbox"]')).toBeChecked();

    // 11. 스크린샷 비교 (Visual Regression)
    await expect(page).toHaveScreenshot('homepage.png');

    // 12. 소프트 Assertion (실패해도 계속 진행)
    await expect.soft(page.locator('h1')).toHaveText('Wrong Text');
    await expect.soft(page.locator('h2')).toBeVisible();
    // 테스트 끝에서 모든 실패 보고
});
```

**타임아웃 설정**:
```javascript
// 특정 assertion에 타임아웃 지정
await expect(page.locator('.slow-element')).toBeVisible({
    timeout: 10000  // 10초
});

// 전역 설정 (playwright.config.js)
module.exports = {
    expect: {
        timeout: 5000  // 모든 expect에 5초 타임아웃
    }
};
```

✅ **체크포인트**
- [ ] `toBeVisible()`, `toHaveText()` 등 기본 assertions를 사용할 수 있는가?
- [ ] 정규식을 사용한 유연한 검증을 할 수 있는가?
- [ ] 시각적 회귀 테스트(`toHaveScreenshot`)를 설정할 수 있는가?

⚠️ **흔한 실수**
- `expect()`에 await를 빼먹으면 제대로 동작 안 함
- 정확한 텍스트 매칭보다 `toContainText()` 권장

🔗 **더 알아보기**: [Assertions](https://playwright.dev/docs/test-assertions)

---

### 4.4 네트워크 가로채기

📌 **핵심 개념**

`page.route()`로 네트워크 요청을 가로채서 모킹, 수정, 차단이 가능합니다.

💻 **코드 예제: 네트워크 제어**

```javascript
const { test, expect } = require('@playwright/test');

test('API 모킹', async ({ page }) => {
    // 1. API 응답 모킹
    await page.route('**/api/users', async route => {
        await route.fulfill({
            status: 200,
            contentType: 'application/json',
            body: JSON.stringify([
                { id: 1, name: 'Mocked User' }
            ])
        });
    });

    await page.goto('/users');
    await expect(page.locator('.user-name')).toHaveText('Mocked User');
});

test('요청 수정', async ({ page }) => {
    // 2. 요청 헤더 수정
    await page.route('**/*', async route => {
        const headers = {
            ...route.request().headers(),
            'X-Custom-Header': 'test-value'
        };
        await route.continue({ headers });
    });
});

test('요청 차단', async ({ page }) => {
    // 3. 이미지 로딩 차단 (속도 향상)
    await page.route('**/*.{png,jpg,jpeg,gif,svg}', route => route.abort());

    // 4. 특정 도메인 차단
    await page.route('**/analytics.google.com/**', route => route.abort());

    await page.goto('/');
});

test('응답 대기', async ({ page }) => {
    // 5. 특정 API 응답 대기
    const responsePromise = page.waitForResponse('**/api/data');
    await page.click('button.load-data');
    const response = await responsePromise;

    expect(response.status()).toBe(200);
    const data = await response.json();
    console.log(data);
});

test('요청 기록', async ({ page }) => {
    // 6. 모든 요청 로깅
    page.on('request', request =>
        console.log('>>', request.method(), request.url())
    );

    page.on('response', response =>
        console.log('<<', response.status(), response.url())
    );

    await page.goto('/');
});
```

**HAR 파일로 기록/재생**:
```javascript
// 녹화
const context = await browser.newContext({
    recordHar: { path: 'network.har' }
});
// ... 테스트 실행
await context.close();  // HAR 파일 저장

// 재생 (오프라인 테스트)
const context = await browser.newContext({
    har: { path: 'network.har' }
});
```

✅ **체크포인트**
- [ ] API 응답을 모킹할 수 있는가?
- [ ] 특정 리소스(이미지 등)를 차단할 수 있는가?
- [ ] HAR 파일을 사용할 수 있는가?

⚠️ **흔한 실수**
- `route.continue()` 호출 안 하면 요청이 멈춤
- glob 패턴 `**` 사용 시 모든 요청에 영향

🔗 **더 알아보기**: [Network](https://playwright.dev/docs/network)

---

### 4.5 테스트 구성 및 설정

📌 **핵심 개념**

`playwright.config.js`로 브라우저, 타임아웃, 병렬 실행 등을 설정합니다.

💻 **코드 예제: 설정 파일**

```javascript
// playwright.config.js
const { defineConfig, devices } = require('@playwright/test');

module.exports = defineConfig({
    // 테스트 디렉토리
    testDir: './tests',

    // 병렬 실행 (워커 수)
    workers: process.env.CI ? 2 : 4,

    // 전체 타임아웃
    timeout: 30000,

    // 재시도 횟수
    retries: process.env.CI ? 2 : 0,

    // 리포터
    reporter: [
        ['html', { open: 'never' }],
        ['json', { outputFile: 'results.json' }]
    ],

    // 전역 설정
    use: {
        // 기본 URL
        baseURL: 'http://localhost:3000',

        // 스크린샷
        screenshot: 'only-on-failure',

        // 비디오 녹화
        video: 'retain-on-failure',

        // 추적 (Trace)
        trace: 'on-first-retry',

        // 뷰포트
        viewport: { width: 1280, height: 720 },

        // 헤더
        extraHTTPHeaders: {
            'Accept-Language': 'ko-KR'
        }
    },

    // 프로젝트별 설정 (브라우저/디바이스)
    projects: [
        {
            name: 'chromium',
            use: { ...devices['Desktop Chrome'] }
        },
        {
            name: 'firefox',
            use: { ...devices['Desktop Firefox'] }
        },
        {
            name: 'webkit',
            use: { ...devices['Desktop Safari'] }
        },
        {
            name: 'mobile',
            use: { ...devices['iPhone 14'] }
        }
    ],

    // 로컬 서버 자동 시작
    webServer: {
        command: 'npm run dev',
        url: 'http://localhost:3000',
        reuseExistingServer: !process.env.CI
    }
});
```

**환경별 설정**:
```javascript
// .env 파일 사용
require('dotenv').config();

module.exports = defineConfig({
    use: {
        baseURL: process.env.BASE_URL || 'http://localhost:3000'
    }
});
```

✅ **체크포인트**
- [ ] 멀티 브라우저 프로젝트를 설정할 수 있는가?
- [ ] CI 환경과 로컬 환경을 구분할 수 있는가?
- [ ] `webServer` 옵션으로 로컬 서버를 자동 시작할 수 있는가?

⚠️ **흔한 실수**
- `workers: 1`로 설정하면 병렬 실행 비활성화
- `retries`가 너무 많으면 실패 원인 파악 어려움

🔗 **더 알아보기**: [Test Configuration](https://playwright.dev/docs/test-configuration)

---

### 4.6 Codegen과 디버깅

📌 **핵심 개념**

Codegen은 브라우저 조작을 녹화하여 코드를 자동 생성합니다. Trace Viewer는 실행 내역을 시각적으로 분석합니다.

💻 **코드 예제: Codegen 사용**

```bash
# 기본 사용
npx playwright codegen https://example.com

# 특정 디바이스 에뮬레이션
npx playwright codegen --device="iPhone 14" https://example.com

# 저장된 인증 상태 사용
npx playwright codegen --load-storage=auth.json https://example.com

# Python 코드 생성
npx playwright codegen --target=python https://example.com
```

**Trace Viewer 사용**:
```javascript
// 테스트에서 Trace 활성화
const { test } = require('@playwright/test');

test.use({
    trace: 'on'  // 모든 테스트에 trace
});

test('my test', async ({ page }) => {
    await page.goto('/');
    // ...
});
```

```bash
# Trace 파일 보기
npx playwright show-trace trace.zip

# 또는 온라인 뷰어
# https://trace.playwright.dev/
```

**디버깅 모드**:
```bash
# Headed + 느린 실행
npx playwright test --headed --slowmo=500

# 디버거 연결
PWDEBUG=1 npx playwright test

# UI 모드 (강력 추천)
npx playwright test --ui
```

**VS Code 확장**:
```
1. VS Code 확장 "Playwright Test for VSCode" 설치
2. Testing 패널에서 테스트 실행
3. 브레이크포인트 설정 후 디버깅
4. Show Browser 옵션으로 실시간 확인
```

✅ **체크포인트**
- [ ] Codegen으로 기본 코드를 생성할 수 있는가?
- [ ] Trace Viewer로 실패 원인을 분석할 수 있는가?
- [ ] VS Code 확장을 사용한 디버깅을 할 수 있는가?

⚠️ **흔한 실수**
- Codegen 코드는 리팩토링 필요 (선택자 최적화)
- Trace 파일이 크므로 CI에서는 실패 시에만 저장

🔗 **더 알아보기**: [Debugging Tests](https://playwright.dev/docs/debug)

---

## Part 5: 실전 프로젝트

### 5.1 미니 프로젝트 아이디어

| 난이도 | 프로젝트 | 학습 포인트 |
|--------|---------|------------|
| 🟢 | 로그인 테스트 자동화 | 기본 조작, Assertions |
| 🟢 | 스크린샷 비교 테스트 | Visual Regression |
| 🟡 | E-commerce 체크아웃 테스트 | 복잡한 플로우 |
| 🟡 | API 모킹 테스트 | 네트워크 가로채기 |
| 🔴 | 크로스 브라우저 CI 파이프라인 | 설정, 병렬 실행 |

### 5.2 단계별 구현 가이드: 로그인 테스트

**목표**: 로그인 기능의 E2E 테스트 작성

```javascript
// tests/auth.spec.js
const { test, expect } = require('@playwright/test');

// 테스트 전 실행
test.beforeEach(async ({ page }) => {
    await page.goto('/login');
});

test.describe('로그인 기능', () => {

    test('성공적인 로그인', async ({ page }) => {
        // 입력
        await page.getByLabel('이메일').fill('user@example.com');
        await page.getByLabel('비밀번호').fill('password123');

        // 로그인 버튼 클릭
        await page.getByRole('button', { name: '로그인' }).click();

        // 검증: 대시보드로 이동
        await expect(page).toHaveURL('/dashboard');
        await expect(page.getByRole('heading', { name: '환영합니다' })).toBeVisible();
    });

    test('잘못된 비밀번호', async ({ page }) => {
        await page.getByLabel('이메일').fill('user@example.com');
        await page.getByLabel('비밀번호').fill('wrongpassword');
        await page.getByRole('button', { name: '로그인' }).click();

        // 에러 메시지 확인
        await expect(page.getByRole('alert')).toHaveText('비밀번호가 올바르지 않습니다');

        // URL 변경 없음
        await expect(page).toHaveURL('/login');
    });

    test('빈 필드 검증', async ({ page }) => {
        // 빈 상태로 제출
        await page.getByRole('button', { name: '로그인' }).click();

        // 유효성 검사 메시지
        await expect(page.getByLabel('이메일')).toHaveAttribute('aria-invalid', 'true');
    });

    test('로그인 상태 유지 (Remember Me)', async ({ page, context }) => {
        await page.getByLabel('이메일').fill('user@example.com');
        await page.getByLabel('비밀번호').fill('password123');
        await page.getByLabel('로그인 상태 유지').check();
        await page.getByRole('button', { name: '로그인' }).click();

        await expect(page).toHaveURL('/dashboard');

        // 인증 상태 저장
        await context.storageState({ path: 'auth.json' });
    });

});

// 인증 상태 재사용
test.describe('인증된 사용자', () => {
    test.use({ storageState: 'auth.json' });

    test('프로필 페이지 접근', async ({ page }) => {
        await page.goto('/profile');
        await expect(page.getByRole('heading', { name: '내 프로필' })).toBeVisible();
    });
});
```

### 5.3 Best Practices

**프로젝트 구조**:
```
playwright-tests/
├── tests/
│   ├── auth.spec.js
│   ├── checkout.spec.js
│   └── search.spec.js
├── pages/                    # Page Object Model
│   ├── LoginPage.js
│   └── DashboardPage.js
├── fixtures/
│   └── test-data.json
├── playwright.config.js
└── package.json
```

**Page Object Model 패턴**:
```javascript
// pages/LoginPage.js
class LoginPage {
    constructor(page) {
        this.page = page;
        this.emailInput = page.getByLabel('이메일');
        this.passwordInput = page.getByLabel('비밀번호');
        this.submitButton = page.getByRole('button', { name: '로그인' });
    }

    async goto() {
        await this.page.goto('/login');
    }

    async login(email, password) {
        await this.emailInput.fill(email);
        await this.passwordInput.fill(password);
        await this.submitButton.click();
    }
}

module.exports = { LoginPage };

// 테스트에서 사용
const { LoginPage } = require('./pages/LoginPage');

test('POM 사용', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('user@example.com', 'password');
});
```

**운영 권장사항**:

1. **Locator 전략**: `getByRole()` > `getByTestId()` > CSS 선택자
2. **인증 재사용**: `storageState`로 로그인 상태 저장/재사용
3. **병렬 실행**: 테스트 간 독립성 유지
4. **CI 통합**: GitHub Actions + Playwright
5. **Visual Testing**: `toHaveScreenshot()`으로 UI 변경 감지

```yaml
# .github/workflows/playwright.yml
name: Playwright Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright
        run: npx playwright install --with-deps

      - name: Run tests
        run: npx playwright test

      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
```

---

## 요약

Playwright은 현대 웹 테스트의 표준이 되어가고 있습니다:

- **시작**: `npm init playwright@latest` → 즉시 테스트 작성
- **장점**: 크로스 브라우저, 자동 대기, 강력한 디버깅
- **핵심 기능**: Locator, Assertions, 네트워크 가로채기
- **도구**: Codegen(녹화), Trace Viewer(분석), UI Mode(디버깅)

다음 단계:
1. [공식 Getting Started](https://playwright.dev/docs/intro) 따라하기
2. Codegen으로 첫 테스트 생성
3. CI 파이프라인에 테스트 통합
