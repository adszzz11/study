---
date: 2026-02-02
tags:
  - tech
  - playwright
  - projects
  - best-practices
parent: "[[README]]"
---

# Playwright - 실전 프로젝트 및 Best Practices

> [[04-learning/06-debugging|이전: 디버깅]] | [[README|목차]] | [[cheatsheet|다음: Cheatsheet]]

---

## 1. 프로젝트 구조

### 권장 디렉토리 구조

```
my-project/
├── playwright.config.ts
├── package.json
├── tests/
│   ├── auth/
│   │   ├── login.spec.ts
│   │   └── signup.spec.ts
│   ├── dashboard/
│   │   └── dashboard.spec.ts
│   ├── api/
│   │   └── api.spec.ts
│   └── e2e/
│       ├── checkout.spec.ts
│       └── search.spec.ts
├── fixtures/
│   ├── auth.ts
│   ├── api.ts
│   └── index.ts
├── mocks/
│   ├── api-responses/
│   │   ├── users.json
│   │   └── products.json
│   └── handlers.ts
├── utils/
│   ├── helpers.ts
│   └── test-data.ts
└── .auth/
    └── user.json          # storageState (gitignore)
```

### 파일 네이밍 컨벤션

| 패턴 | 용도 |
|------|------|
| `*.spec.ts` | 테스트 파일 |
| `*.fixture.ts` | Fixture 정의 |
| `*.mock.ts` | 모킹 헬퍼 |
| `*.helper.ts` | 유틸리티 함수 |

---

## 2. Best Practices

### 테스트 작성 원칙

#### 1. 사용자 관점에서 테스트

```typescript
// 좋은 예: 사용자 행동 기반
test('사용자가 상품을 장바구니에 추가할 수 있다', async ({ page }) => {
  await page.goto('/products');
  await page.getByRole('button', { name: '장바구니 담기' }).first().click();
  await expect(page.getByRole('status')).toContainText('장바구니에 추가됨');
});

// 나쁜 예: 구현 세부사항 테스트
test('addToCart 함수가 호출된다', async ({ page }) => {
  await page.click('button.add-to-cart-btn-v2');
  await expect(page.locator('.cart-count-span')).toHaveText('1');
});
```

#### 2. 테스트 독립성 유지

```typescript
// 좋은 예: 각 테스트가 독립적
test.beforeEach(async ({ page }) => {
  await page.goto('/');
});

test('테스트 A', async ({ page }) => {
  // 자체적으로 완결
});

test('테스트 B', async ({ page }) => {
  // 테스트 A와 무관하게 실행 가능
});

// 나쁜 예: 테스트 간 의존성
let createdUserId: string;

test('사용자 생성', async ({ page }) => {
  // createdUserId 설정
});

test('사용자 삭제', async ({ page }) => {
  // createdUserId 사용 - 테스트 A 실패 시 B도 실패
});
```

#### 3. Role 기반 Locator 우선

```typescript
// 좋은 예: 접근성 기반 선택자
await page.getByRole('button', { name: '제출' }).click();
await page.getByLabel('이메일').fill('test@example.com');
await page.getByRole('heading', { name: '환영합니다' });

// 나쁜 예: 구현 의존 선택자
await page.click('.btn-primary.submit-form');
await page.fill('#input-email-field');
```

#### 4. 적절한 Assertion 사용

```typescript
// 좋은 예: Web-first assertions (자동 재시도)
await expect(page.getByRole('alert')).toBeVisible();
await expect(page.getByRole('heading')).toHaveText('성공');

// 나쁜 예: 수동 대기 + 일반 assertion
await page.waitForSelector('.alert');
const text = await page.locator('h1').textContent();
expect(text).toBe('성공');
```

### 성능 최적화

#### 1. 병렬 실행 활용

```typescript
// playwright.config.ts
export default defineConfig({
  fullyParallel: true,
  workers: process.env.CI ? 2 : undefined,
});
```

#### 2. 인증 상태 재사용

```typescript
// global-setup.ts
async function globalSetup() {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.goto('/login');
  await page.fill('#email', 'test@example.com');
  await page.fill('#password', 'password');
  await page.click('button[type="submit"]');

  await page.context().storageState({ path: '.auth/user.json' });
  await browser.close();
}

// playwright.config.ts
export default defineConfig({
  globalSetup: require.resolve('./global-setup'),
  projects: [
    {
      name: 'authenticated',
      use: { storageState: '.auth/user.json' },
    },
  ],
});
```

#### 3. 불필요한 리소스 차단

```typescript
test.beforeEach(async ({ page }) => {
  // 이미지, 폰트, 스타일시트 차단 (선택적)
  await page.route('**/*.{png,jpg,jpeg,gif,webp,svg}', route => route.abort());
  await page.route('**/*.woff2', route => route.abort());
});
```

---

## 3. Page Object Model (POM)

### Page Object 정의

```typescript
// pages/LoginPage.ts
import { Page, Locator, expect } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel('이메일');
    this.passwordInput = page.getByLabel('비밀번호');
    this.submitButton = page.getByRole('button', { name: '로그인' });
    this.errorMessage = page.getByRole('alert');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async expectError(message: string) {
    await expect(this.errorMessage).toContainText(message);
  }
}
```

### Page Object 사용

```typescript
// tests/login.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

test.describe('로그인', () => {
  test('성공적인 로그인', async ({ page }) => {
    const loginPage = new LoginPage(page);

    await loginPage.goto();
    await loginPage.login('user@example.com', 'password123');

    await expect(page).toHaveURL(/.*dashboard/);
  });

  test('잘못된 비밀번호', async ({ page }) => {
    const loginPage = new LoginPage(page);

    await loginPage.goto();
    await loginPage.login('user@example.com', 'wrong');

    await loginPage.expectError('비밀번호가 올바르지 않습니다');
  });
});
```

### Fixture로 Page Object 제공

```typescript
// fixtures/pages.ts
import { test as base } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { DashboardPage } from '../pages/DashboardPage';

type Pages = {
  loginPage: LoginPage;
  dashboardPage: DashboardPage;
};

export const test = base.extend<Pages>({
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page));
  },
  dashboardPage: async ({ page }, use) => {
    await use(new DashboardPage(page));
  },
});

export { expect } from '@playwright/test';
```

```typescript
// tests/login.spec.ts
import { test, expect } from '../fixtures/pages';

test('로그인', async ({ loginPage }) => {
  await loginPage.goto();
  await loginPage.login('user@example.com', 'password');
});
```

---

## 4. 테스트 데이터 관리

### 팩토리 패턴

```typescript
// utils/factories.ts
export const UserFactory = {
  create(overrides = {}) {
    return {
      email: `test-${Date.now()}@example.com`,
      password: 'Password123!',
      name: '테스트 사용자',
      ...overrides,
    };
  },

  admin() {
    return this.create({
      email: 'admin@example.com',
      role: 'admin',
    });
  },
};
```

### API를 통한 테스트 데이터 생성

```typescript
import { test, expect } from '@playwright/test';
import { UserFactory } from '../utils/factories';

test.describe('사용자 프로필', () => {
  let testUser: { id: string; email: string };

  test.beforeEach(async ({ request }) => {
    // API로 테스트 사용자 생성
    const userData = UserFactory.create();
    const response = await request.post('/api/users', { data: userData });
    testUser = await response.json();
  });

  test.afterEach(async ({ request }) => {
    // 테스트 데이터 정리
    await request.delete(`/api/users/${testUser.id}`);
  });

  test('프로필 수정', async ({ page }) => {
    await page.goto(`/users/${testUser.id}/profile`);
    // ...
  });
});
```

---

## 5. 실전 프로젝트 예제

### E-commerce 체크아웃 플로우

```typescript
// tests/e2e/checkout.spec.ts
import { test, expect } from '@playwright/test';

test.describe('체크아웃 플로우', () => {
  test.beforeEach(async ({ page }) => {
    // 로그인 상태로 시작 (storageState 사용)
    await page.goto('/products');
  });

  test('장바구니에서 결제까지', async ({ page }) => {
    // 1. 상품 선택
    await page.getByRole('button', { name: '장바구니 담기' }).first().click();
    await expect(page.getByRole('status')).toContainText('추가됨');

    // 2. 장바구니로 이동
    await page.getByRole('link', { name: '장바구니' }).click();
    await expect(page.getByRole('heading')).toHaveText('장바구니');

    // 3. 결제 진행
    await page.getByRole('button', { name: '결제하기' }).click();

    // 4. 배송 정보 입력
    await page.getByLabel('주소').fill('서울시 강남구');
    await page.getByLabel('상세주소').fill('테헤란로 123');
    await page.getByRole('button', { name: '다음' }).click();

    // 5. 결제 정보 입력 (테스트 카드)
    await page.getByLabel('카드번호').fill('4242424242424242');
    await page.getByLabel('유효기간').fill('12/25');
    await page.getByLabel('CVC').fill('123');

    // 6. 결제 완료
    await page.getByRole('button', { name: '결제하기' }).click();

    // 7. 주문 완료 확인
    await expect(page).toHaveURL(/.*order-complete/);
    await expect(page.getByRole('heading')).toContainText('주문이 완료되었습니다');
  });
});
```

### 검색 기능 테스트

```typescript
// tests/e2e/search.spec.ts
import { test, expect } from '@playwright/test';

test.describe('검색 기능', () => {
  test('키워드 검색', async ({ page }) => {
    await page.goto('/');

    // 검색어 입력
    await page.getByRole('searchbox').fill('노트북');
    await page.getByRole('button', { name: '검색' }).click();

    // 결과 확인
    await expect(page).toHaveURL(/.*search\?q=노트북/);
    await expect(page.getByRole('heading')).toContainText('검색 결과');
    await expect(page.locator('.product-card')).not.toHaveCount(0);
  });

  test('필터 적용', async ({ page }) => {
    await page.goto('/search?q=노트북');

    // 가격 필터
    await page.getByLabel('최소 가격').fill('500000');
    await page.getByLabel('최대 가격').fill('1000000');
    await page.getByRole('button', { name: '필터 적용' }).click();

    // 결과 확인
    await expect(page).toHaveURL(/.*minPrice=500000.*maxPrice=1000000/);

    // 모든 결과가 필터 조건 충족 확인
    const prices = page.locator('.product-price');
    const count = await prices.count();

    for (let i = 0; i < count; i++) {
      const priceText = await prices.nth(i).textContent();
      const price = parseInt(priceText!.replace(/[^0-9]/g, ''));
      expect(price).toBeGreaterThanOrEqual(500000);
      expect(price).toBeLessThanOrEqual(1000000);
    }
  });

  test('검색어 없음 처리', async ({ page }) => {
    await page.goto('/search?q=존재하지않는상품명12345');

    await expect(page.getByText('검색 결과가 없습니다')).toBeVisible();
    await expect(page.getByRole('link', { name: '인기 상품 보기' })).toBeVisible();
  });
});
```

---

## 6. CI/CD 통합

### GitHub Actions

```yaml
# .github/workflows/playwright.yml
name: Playwright Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    timeout-minutes: 60
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright Browsers
        run: npx playwright install --with-deps

      - name: Run Playwright tests
        run: npx playwright test

      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

### 샤딩 (대규모 테스트)

```yaml
# .github/workflows/playwright.yml
jobs:
  test:
    strategy:
      fail-fast: false
      matrix:
        shardIndex: [1, 2, 3, 4]
        shardTotal: [4]

    steps:
      - name: Run Playwright tests
        run: npx playwright test --shard=${{ matrix.shardIndex }}/${{ matrix.shardTotal }}
```

---

## 7. 체크리스트

### 테스트 작성 전

- [ ] 테스트 범위 정의 (무엇을 테스트할 것인가?)
- [ ] 테스트 데이터 준비
- [ ] 환경 설정 (baseURL, 인증 등)

### 테스트 작성 중

- [ ] Role 기반 Locator 사용
- [ ] 적절한 Assertion 사용
- [ ] 테스트 독립성 확보
- [ ] 명확한 테스트 이름

### 테스트 작성 후

- [ ] 로컬에서 실행 확인
- [ ] CI에서 실행 확인
- [ ] Flaky 테스트 확인
- [ ] 리포트 검토

---

## 다음 단계

> [!tip] 다음으로
> Best Practices를 이해했다면 [[cheatsheet|Cheatsheet]]에서 빠른 참조를 확인하세요.

---

## References

- [Playwright - Best Practices](https://playwright.dev/docs/best-practices)
- [Playwright - Page Object Models](https://playwright.dev/docs/pom)
- [Playwright - CI/CD](https://playwright.dev/docs/ci)
