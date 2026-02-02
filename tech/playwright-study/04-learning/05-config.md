---
date: 2026-02-02
tags:
  - tech
  - playwright
  - learning
  - config
parent: "[[../README]]"
---

# Playwright - 테스트 구성 및 설정

> [[04-network|이전: 네트워크]] | [[../README|목차]] | [[06-debugging|다음: 디버깅]]

---

## 1. playwright.config.ts 개요

### 기본 구조

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  // 테스트 디렉토리
  testDir: './tests',

  // 병렬 실행
  fullyParallel: true,

  // CI에서 재시도 횟수
  retries: process.env.CI ? 2 : 0,

  // 병렬 워커 수
  workers: process.env.CI ? 1 : undefined,

  // 리포터
  reporter: 'html',

  // 공통 설정
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },

  // 프로젝트 (브라우저별 설정)
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],
});
```

---

## 2. 주요 설정 옵션

### 테스트 실행 설정

```typescript
export default defineConfig({
  // 테스트 파일 위치
  testDir: './tests',

  // 테스트 파일 패턴
  testMatch: '**/*.spec.ts',

  // 무시할 파일
  testIgnore: '**/fixtures/**',

  // 전역 타임아웃 (테스트당)
  timeout: 30000,

  // expect 타임아웃
  expect: {
    timeout: 5000,
  },

  // 완전 병렬 실행
  fullyParallel: true,

  // 실패 시 재시도
  retries: 2,

  // 워커 수 (undefined = CPU 코어의 절반)
  workers: 4,

  // 첫 실패 시 중단
  forbidOnly: !!process.env.CI,

  // 최대 실패 허용 수
  maxFailures: process.env.CI ? 10 : 0,
});
```

### use 옵션 (공통 설정)

```typescript
export default defineConfig({
  use: {
    // 기본 URL
    baseURL: 'http://localhost:3000',

    // 헤드리스 모드
    headless: true,

    // 뷰포트
    viewport: { width: 1280, height: 720 },

    // 스크린샷 (on, off, only-on-failure)
    screenshot: 'only-on-failure',

    // 트레이스 (on, off, on-first-retry, retain-on-failure)
    trace: 'on-first-retry',

    // 비디오 (on, off, on-first-retry, retain-on-failure)
    video: 'retain-on-failure',

    // 브라우저 시작 타임아웃
    launchOptions: {
      slowMo: 50, // 액션 사이 지연 (디버깅용)
    },

    // 기본 탐색 타임아웃
    navigationTimeout: 30000,

    // 액션 타임아웃
    actionTimeout: 10000,

    // 로케일
    locale: 'ko-KR',

    // 타임존
    timezoneId: 'Asia/Seoul',

    // 지리적 위치
    geolocation: { longitude: 126.9780, latitude: 37.5665 },

    // 권한
    permissions: ['geolocation'],

    // 색상 스킴
    colorScheme: 'dark',

    // 테스트 ID 속성
    testIdAttribute: 'data-testid',
  },
});
```

---

## 3. 프로젝트 설정

### 다중 브라우저 테스트

```typescript
export default defineConfig({
  projects: [
    // 데스크톱 브라우저
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },

    // 모바일 브라우저
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },
  ],
});
```

### 환경별 프로젝트

```typescript
export default defineConfig({
  projects: [
    {
      name: 'development',
      use: {
        baseURL: 'http://localhost:3000',
      },
    },
    {
      name: 'staging',
      use: {
        baseURL: 'https://staging.example.com',
      },
    },
    {
      name: 'production',
      use: {
        baseURL: 'https://www.example.com',
      },
    },
  ],
});
```

### 의존성 있는 프로젝트

```typescript
export default defineConfig({
  projects: [
    {
      name: 'setup',
      testMatch: /global\.setup\.ts/,
    },
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
      dependencies: ['setup'], // setup 먼저 실행
    },
  ],
});
```

---

## 4. 리포터 설정

### 기본 리포터

```typescript
export default defineConfig({
  // 단일 리포터
  reporter: 'html',

  // 다중 리포터
  reporter: [
    ['list'],              // 콘솔에 리스트 출력
    ['html', { open: 'never' }], // HTML 리포트
    ['junit', { outputFile: 'results.xml' }], // JUnit XML
  ],
});
```

### 리포터 종류

| 리포터 | 설명 | 용도 |
|--------|------|------|
| `list` | 콘솔에 리스트 출력 | 개발 중 |
| `line` | 한 줄씩 출력 | CI |
| `dot` | 점으로 표시 | 간단한 확인 |
| `html` | HTML 리포트 | 상세 분석 |
| `json` | JSON 형식 | 다른 도구 연동 |
| `junit` | JUnit XML | CI/CD 연동 |
| `github` | GitHub Actions 통합 | GitHub Actions |
| `blob` | 바이너리 형식 | 샤딩된 결과 병합 |

### HTML 리포터 옵션

```typescript
reporter: [
  ['html', {
    open: 'on-failure',    // 실패 시 자동 열기
    outputFolder: 'playwright-report',
    attachmentsBaseURL: 'https://cdn.example.com',
  }]
],
```

---

## 5. Global Setup/Teardown

### 전역 설정 파일

```typescript
// playwright.config.ts
export default defineConfig({
  globalSetup: require.resolve('./global-setup'),
  globalTeardown: require.resolve('./global-teardown'),
});
```

```typescript
// global-setup.ts
import { chromium, FullConfig } from '@playwright/test';

async function globalSetup(config: FullConfig) {
  // 인증 상태 저장
  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.goto('http://localhost:3000/login');
  await page.fill('#username', 'admin');
  await page.fill('#password', 'password');
  await page.click('button[type="submit"]');
  await page.waitForURL('**/dashboard');

  // 스토리지 상태 저장
  await page.context().storageState({ path: '.auth/user.json' });

  await browser.close();
}

export default globalSetup;
```

### 저장된 인증 사용

```typescript
export default defineConfig({
  projects: [
    {
      name: 'authenticated',
      use: {
        storageState: '.auth/user.json', // 저장된 인증 사용
      },
    },
  ],
});
```

---

## 6. Fixtures

### 커스텀 Fixture

```typescript
// fixtures.ts
import { test as base } from '@playwright/test';

// 타입 정의
type MyFixtures = {
  adminPage: Page;
  testUser: { email: string; password: string };
};

// fixture 확장
export const test = base.extend<MyFixtures>({
  // testUser fixture
  testUser: async ({}, use) => {
    await use({
      email: 'test@example.com',
      password: 'password123'
    });
  },

  // adminPage fixture (로그인된 페이지)
  adminPage: async ({ page }, use) => {
    await page.goto('/login');
    await page.fill('#email', 'admin@example.com');
    await page.fill('#password', 'admin123');
    await page.click('button[type="submit"]');
    await page.waitForURL('**/dashboard');

    await use(page);
  },
});

export { expect } from '@playwright/test';
```

```typescript
// 테스트에서 사용
import { test, expect } from './fixtures';

test('관리자 대시보드', async ({ adminPage }) => {
  await expect(adminPage.locator('h1')).toHaveText('관리자 대시보드');
});

test('테스트 사용자 정보', async ({ testUser }) => {
  console.log(testUser.email); // test@example.com
});
```

---

## 7. 테스트 구성

### describe로 그룹화

```typescript
import { test, expect } from '@playwright/test';

test.describe('사용자 인증', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
  });

  test('로그인 성공', async ({ page }) => {
    // ...
  });

  test('로그인 실패', async ({ page }) => {
    // ...
  });
});
```

### 테스트 어노테이션

```typescript
// 테스트 건너뛰기
test.skip('미구현 기능', async ({ page }) => {});

// 조건부 건너뛰기
test('Windows 전용', async ({ page }) => {
  test.skip(process.platform !== 'win32', 'Windows에서만 실행');
});

// 실패 예상
test.fail('알려진 버그', async ({ page }) => {});

// 느린 테스트 (타임아웃 3배)
test.slow('대용량 처리', async ({ page }) => {});

// 단독 실행 (CI에서는 에러)
test.only('디버깅 중', async ({ page }) => {});

// 태그
test('로그인 @smoke', async ({ page }) => {});
test('상세검색 @regression', async ({ page }) => {});
```

### 병렬/순차 실행

```typescript
// 순차 실행 (기본)
test.describe.serial('순서 의존 테스트', () => {
  test('1단계', async ({ page }) => {});
  test('2단계', async ({ page }) => {}); // 1단계 후 실행
});

// 병렬 실행
test.describe.parallel('독립 테스트', () => {
  test('테스트 A', async ({ page }) => {});
  test('테스트 B', async ({ page }) => {}); // 동시 실행 가능
});
```

---

## 8. 환경 변수

### .env 파일 사용

```bash
# .env
BASE_URL=http://localhost:3000
TEST_USER_EMAIL=test@example.com
TEST_USER_PASSWORD=password123
```

```typescript
// playwright.config.ts
import dotenv from 'dotenv';
dotenv.config();

export default defineConfig({
  use: {
    baseURL: process.env.BASE_URL,
  },
});
```

### 테스트에서 환경 변수 사용

```typescript
test('환경 변수 사용', async ({ page }) => {
  await page.fill('#email', process.env.TEST_USER_EMAIL!);
  await page.fill('#password', process.env.TEST_USER_PASSWORD!);
});
```

---

## 9. 웹서버 실행

### 테스트 전 서버 시작

```typescript
export default defineConfig({
  webServer: {
    command: 'npm run start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },
});
```

### 다중 서버

```typescript
export default defineConfig({
  webServer: [
    {
      command: 'npm run start:frontend',
      url: 'http://localhost:3000',
      reuseExistingServer: !process.env.CI,
    },
    {
      command: 'npm run start:backend',
      url: 'http://localhost:4000',
      reuseExistingServer: !process.env.CI,
    },
  ],
});
```

---

## 10. CLI 옵션

### 주요 명령어

```bash
# 모든 테스트 실행
npx playwright test

# 특정 파일 실행
npx playwright test tests/login.spec.ts

# 특정 프로젝트
npx playwright test --project=chromium

# 특정 테스트 이름
npx playwright test -g "로그인"

# 태그로 필터링
npx playwright test --grep @smoke

# UI 모드
npx playwright test --ui

# 헤드 모드 (브라우저 보이기)
npx playwright test --headed

# 디버그 모드
npx playwright test --debug

# 워커 수 지정
npx playwright test --workers=2

# 재시도 횟수
npx playwright test --retries=2

# 스냅샷 업데이트
npx playwright test --update-snapshots

# 리포트 보기
npx playwright show-report
```

---

## 다음 단계

> [!tip] 다음으로
> 테스트 설정을 마쳤다면 [[06-debugging|디버깅]]에서 Codegen과 트러블슈팅을 배워보세요.

---

## References

- [Playwright - Configuration](https://playwright.dev/docs/test-configuration)
- [Playwright - Projects](https://playwright.dev/docs/test-projects)
- [Playwright - Fixtures](https://playwright.dev/docs/test-fixtures)
- [Playwright - CLI](https://playwright.dev/docs/test-cli)
