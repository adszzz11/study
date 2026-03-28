---
date: 2026-02-02
tags:
  - tech
  - playwright
  - cheatsheet
parent: "[[README]]"
---

# Playwright Cheatsheet

> [[05-projects|이전: 실전 프로젝트]] | [[README|목차]]

빠른 참조를 위한 Playwright 핵심 명령어 및 패턴 모음

---

## 설치 및 실행

```bash
# 새 프로젝트 초기화
npm init playwright@latest

# 기존 프로젝트에 추가
npm install -D @playwright/test
npx playwright install

# 테스트 실행
npx playwright test                    # 모든 테스트
npx playwright test login.spec.ts      # 특정 파일
npx playwright test --project=chromium # 특정 브라우저
npx playwright test -g "로그인"        # 특정 테스트명
npx playwright test --grep @smoke      # 태그 필터

# 디버깅
npx playwright test --ui               # UI 모드
npx playwright test --headed           # 브라우저 표시
npx playwright test --debug            # 디버그 모드
npx playwright codegen https://example.com  # 코드 생성

# 리포트
npx playwright show-report
```

---

## 기본 테스트 구조

```typescript
import { test, expect } from '@playwright/test';

test.describe('테스트 그룹', () => {
  test.beforeAll(async () => { /* 그룹 시작 전 1회 */ });
  test.beforeEach(async ({ page }) => { /* 각 테스트 전 */ });
  test.afterEach(async ({ page }) => { /* 각 테스트 후 */ });
  test.afterAll(async () => { /* 그룹 종료 후 1회 */ });

  test('테스트명', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/타이틀/);
  });
});
```

---

## Locator (요소 선택)

### 권장 순서

```typescript
// 1. Role 기반 (가장 권장)
page.getByRole('button', { name: '제출' })
page.getByRole('heading', { name: '환영합니다', level: 1 })
page.getByRole('link', { name: '더 보기' })
page.getByRole('checkbox', { checked: true })
page.getByRole('textbox')

// 2. 폼 요소
page.getByLabel('이메일')
page.getByPlaceholder('검색어 입력')

// 3. 텍스트
page.getByText('로그인')
page.getByText('로그인', { exact: true })

// 4. 테스트 ID
page.getByTestId('submit-btn')

// 5. CSS/XPath (필요 시만)
page.locator('button.primary')
page.locator('xpath=//button')
```

### Locator 체이닝 및 필터

```typescript
// 체이닝
page.locator('.modal').locator('button')

// 필터
page.locator('li').filter({ hasText: '항목' })
page.locator('div').filter({ has: page.locator('.badge') })

// 인덱스
page.locator('li').first()
page.locator('li').last()
page.locator('li').nth(2)  // 0-indexed

// OR/AND
page.locator('button').or(page.locator('a.button'))
page.locator('button').and(page.locator(':visible'))
```

---

## 액션

```typescript
// 탐색
await page.goto('https://example.com')
await page.goto('/path')  // baseURL 기준
await page.goBack()
await page.goForward()
await page.reload()

// 클릭
await page.locator('button').click()
await page.locator('button').dblclick()
await page.locator('button').click({ button: 'right' })
await page.locator('button').click({ modifiers: ['Shift'] })

// 입력
await page.locator('input').fill('텍스트')
await page.locator('input').clear()
await page.locator('input').pressSequentially('타이핑', { delay: 100 })

// 선택
await page.selectOption('select', 'value')
await page.selectOption('select', { label: '라벨' })
await page.locator('input[type=checkbox]').check()
await page.locator('input[type=checkbox]').uncheck()

// 파일 업로드
await page.setInputFiles('input[type=file]', 'path/to/file.pdf')

// 키보드
await page.keyboard.press('Enter')
await page.keyboard.press('Control+A')

// 마우스
await page.mouse.click(100, 200)
await page.mouse.wheel(0, 500)
```

---

## Assertions (검증)

### 페이지

```typescript
await expect(page).toHaveURL(/.*dashboard/)
await expect(page).toHaveTitle('제목')
```

### 요소

```typescript
// 가시성
await expect(locator).toBeVisible()
await expect(locator).toBeHidden()
await expect(locator).toBeAttached()

// 텍스트
await expect(locator).toHaveText('정확한 텍스트')
await expect(locator).toContainText('포함 텍스트')
await expect(locator).toHaveText(['항목1', '항목2'])  // 리스트

// 속성/값
await expect(locator).toHaveAttribute('type', 'email')
await expect(locator).toHaveClass(/active/)
await expect(locator).toHaveValue('입력값')
await expect(locator).toBeEmpty()

// 상태
await expect(locator).toBeEnabled()
await expect(locator).toBeDisabled()
await expect(locator).toBeChecked()
await expect(locator).toBeFocused()

// 개수
await expect(locator).toHaveCount(5)

// 부정
await expect(locator).not.toBeVisible()

// Soft Assertion (실패해도 계속)
await expect.soft(locator).toHaveText('텍스트')
```

### 스크린샷

```typescript
await expect(page).toHaveScreenshot()
await expect(locator).toHaveScreenshot('name.png')
```

---

## 대기

```typescript
// 자동 대기 (대부분 불필요)
await page.locator('button').click()  // 자동으로 기다림

// 명시적 대기
await page.waitForURL('**/dashboard')
await page.waitForLoadState('networkidle')
await page.locator('.loaded').waitFor()
await page.locator('.loading').waitFor({ state: 'hidden' })

// 네트워크 대기
const response = await page.waitForResponse('**/api/data')
const request = await page.waitForRequest('**/api/submit')

// 권장하지 않음
await page.waitForTimeout(1000)
```

---

## 네트워크 모킹

```typescript
// 응답 모킹
await page.route('**/api/users', async route => {
  await route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify([{ id: 1, name: '홍길동' }])
  })
})

// 파일에서 응답
await page.route('**/api/data', async route => {
  await route.fulfill({ path: 'mocks/data.json' })
})

// 요청 수정
await page.route('**/api/**', async route => {
  await route.continue({
    headers: { ...route.request().headers(), 'X-Custom': 'value' }
  })
})

// 요청 차단
await page.route('**/*.{png,jpg}', route => route.abort())

// HAR 재생
await page.routeFromHAR('tests/api.har')
```

---

## 정보 추출

```typescript
// 텍스트
const text = await locator.textContent()
const innerText = await locator.innerText()
const texts = await locator.allTextContents()

// 속성
const href = await locator.getAttribute('href')
const value = await locator.inputValue()

// 개수
const count = await locator.count()

// 상태
const isVisible = await locator.isVisible()
const isEnabled = await locator.isEnabled()
const isChecked = await locator.isChecked()
```

---

## 스크린샷 & 비디오

```typescript
// 스크린샷
await page.screenshot({ path: 'screenshot.png' })
await page.screenshot({ path: 'full.png', fullPage: true })
await locator.screenshot({ path: 'element.png' })

// 설정 (playwright.config.ts)
use: {
  screenshot: 'only-on-failure',
  video: 'retain-on-failure',
  trace: 'on-first-retry',
}
```

---

## 프레임 & 팝업

```typescript
// iframe
const frame = page.frameLocator('iframe#editor')
await frame.locator('button').click()

// 팝업/새 탭
const [newPage] = await Promise.all([
  page.waitForEvent('popup'),
  page.click('a[target="_blank"]')
])
await newPage.waitForLoadState()
```

---

## 설정 (playwright.config.ts)

```typescript
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',

  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'mobile', use: { ...devices['iPhone 12'] } },
  ],

  webServer: {
    command: 'npm run start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```

---

## 테스트 어노테이션

```typescript
test.skip('건너뛰기', async ({ page }) => {})
test.fail('실패 예상', async ({ page }) => {})
test.slow('느린 테스트', async ({ page }) => {})
test.only('이것만 실행', async ({ page }) => {})  // CI에서 에러

// 조건부
test('조건부', async ({ page }) => {
  test.skip(process.platform === 'win32', 'Windows 미지원')
})

// 태그
test('스모크 테스트 @smoke', async ({ page }) => {})
// 실행: npx playwright test --grep @smoke
```

---

## 디버깅

```typescript
// 코드에서 일시정지
await page.pause()

// 콘솔 로그 캡처
page.on('console', msg => console.log(msg.text()))

// 페이지 에러 캡처
page.on('pageerror', err => console.error(err))
```

```bash
# CLI 디버깅
npx playwright test --debug
PWDEBUG=1 npx playwright test

# Trace 보기
npx playwright show-trace trace.zip
```

---

## 자주 쓰는 패턴

### 로그인 후 테스트

```typescript
// global-setup.ts
export default async function globalSetup() {
  const browser = await chromium.launch()
  const page = await browser.newPage()
  await page.goto('/login')
  await page.fill('#email', 'user@example.com')
  await page.fill('#password', 'password')
  await page.click('button[type=submit]')
  await page.context().storageState({ path: '.auth/user.json' })
  await browser.close()
}

// playwright.config.ts
use: { storageState: '.auth/user.json' }
```

### API 테스트

```typescript
test('API 테스트', async ({ request }) => {
  const response = await request.get('/api/users')
  expect(response.status()).toBe(200)

  const data = await response.json()
  expect(data.length).toBeGreaterThan(0)
})
```

### 파일 다운로드

```typescript
const [download] = await Promise.all([
  page.waitForEvent('download'),
  page.click('a.download')
])
await download.saveAs('downloaded-file.pdf')
```

---

## References

- [공식 문서](https://playwright.dev)
- [API 레퍼런스](https://playwright.dev/docs/api/class-playwright)
- [Best Practices](https://playwright.dev/docs/best-practices)
