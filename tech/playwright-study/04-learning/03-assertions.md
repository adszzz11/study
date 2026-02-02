---
date: 2026-02-02
tags:
  - tech
  - playwright
  - learning
  - assertions
parent: "[[../README]]"
---

# Playwright - Assertions

> [[02-locators|이전: Locator]] | [[../README|목차]] | [[04-network|다음: 네트워크]]

---

## 1. Assertions 개요

### Web-First Assertions

Playwright의 Assertions는 **자동 재시도**와 **자동 대기** 기능이 내장되어 있습니다.

```typescript
import { test, expect } from '@playwright/test';

test('자동 재시도 예시', async ({ page }) => {
  await page.goto('/dashboard');

  // 요소가 나타날 때까지 자동으로 재시도 (기본 5초)
  await expect(page.locator('.loading')).not.toBeVisible();
  await expect(page.locator('.content')).toBeVisible();
});
```

### Generic vs Web-First

| 종류 | 재시도 | 사용 |
|------|--------|------|
| Web-First | O | `expect(locator).toBeVisible()` |
| Generic | X | `expect(value).toBe(5)` |

---

## 2. 페이지 Assertions

### URL 확인

```typescript
// URL 포함
await expect(page).toHaveURL(/.*dashboard/);

// 정확한 URL
await expect(page).toHaveURL('https://example.com/dashboard');

// 쿼리 파라미터 포함
await expect(page).toHaveURL(/\?tab=settings/);
```

### 제목 확인

```typescript
// 제목 포함
await expect(page).toHaveTitle(/Dashboard/);

// 정확한 제목
await expect(page).toHaveTitle('Dashboard - MyApp');
```

---

## 3. 요소 Assertions

### 가시성

```typescript
// 보이는지
await expect(page.locator('.modal')).toBeVisible();

// 숨겨졌는지
await expect(page.locator('.loading')).toBeHidden();

// DOM에 존재하는지 (visible과 별개)
await expect(page.locator('.element')).toBeAttached();
```

### 텍스트

```typescript
// 텍스트 포함
await expect(page.locator('h1')).toContainText('환영합니다');

// 정확한 텍스트
await expect(page.locator('h1')).toHaveText('환영합니다, 홍길동님');

// 여러 요소 텍스트 (리스트 등)
await expect(page.locator('li')).toHaveText([
  '항목 1',
  '항목 2',
  '항목 3'
]);

// 정규식
await expect(page.locator('.price')).toHaveText(/\d+,\d+원/);
```

### 속성

```typescript
// 특정 속성 값
await expect(page.locator('input')).toHaveAttribute('type', 'email');

// 속성 존재
await expect(page.locator('button')).toHaveAttribute('disabled');

// 클래스 포함
await expect(page.locator('div')).toHaveClass(/active/);

// 정확한 클래스
await expect(page.locator('div')).toHaveClass('btn btn-primary');

// ID
await expect(page.locator('button')).toHaveId('submit-btn');
```

### CSS 속성

```typescript
// CSS 스타일 확인
await expect(page.locator('.error')).toHaveCSS('color', 'rgb(255, 0, 0)');
await expect(page.locator('.box')).toHaveCSS('display', 'flex');
```

### 입력 값

```typescript
// input 값
await expect(page.locator('input[name="email"]')).toHaveValue('test@example.com');

// 정규식
await expect(page.locator('input')).toHaveValue(/test@.*/);

// 빈 값
await expect(page.locator('input')).toBeEmpty();
```

### 상태

```typescript
// 활성화/비활성화
await expect(page.locator('button')).toBeEnabled();
await expect(page.locator('button')).toBeDisabled();

// 체크 상태
await expect(page.locator('input[type="checkbox"]')).toBeChecked();
await expect(page.locator('input[type="checkbox"]')).not.toBeChecked();

// 편집 가능
await expect(page.locator('input')).toBeEditable();

// 포커스
await expect(page.locator('input')).toBeFocused();
```

### 요소 개수

```typescript
// 정확한 개수
await expect(page.locator('li')).toHaveCount(5);

// 최소 1개 존재
await expect(page.locator('li')).not.toHaveCount(0);
```

---

## 4. 스크린샷 Assertions

### 시각적 비교

```typescript
// 페이지 전체
await expect(page).toHaveScreenshot();

// 특정 요소
await expect(page.locator('.chart')).toHaveScreenshot();

// 이름 지정
await expect(page).toHaveScreenshot('dashboard.png');

// 옵션
await expect(page).toHaveScreenshot({
  maxDiffPixels: 100,        // 허용 픽셀 차이
  maxDiffPixelRatio: 0.1,    // 허용 비율
  threshold: 0.2,            // 픽셀 비교 민감도
  animations: 'disabled',    // 애니메이션 비활성화
  mask: [page.locator('.timestamp')], // 마스킹
});
```

### 스크린샷 업데이트

```bash
# 기준 스크린샷 업데이트
npx playwright test --update-snapshots
```

---

## 5. Soft Assertions

### 테스트 중단 없이 검증

```typescript
test('여러 검증을 한 번에', async ({ page }) => {
  await page.goto('/profile');

  // soft assertion - 실패해도 테스트 계속 진행
  await expect.soft(page.locator('.name')).toHaveText('홍길동');
  await expect.soft(page.locator('.email')).toHaveText('hong@example.com');
  await expect.soft(page.locator('.role')).toHaveText('관리자');

  // 모든 soft assertion 결과를 테스트 끝에 확인
});
```

---

## 6. Generic Assertions

### 일반 값 비교 (재시도 없음)

```typescript
// 동등
expect(value).toBe(5);
expect(text).toBe('hello');

// 동등 (객체/배열)
expect(obj).toEqual({ name: 'test' });

// truthy/falsy
expect(value).toBeTruthy();
expect(value).toBeFalsy();

// null/undefined
expect(value).toBeNull();
expect(value).toBeUndefined();
expect(value).toBeDefined();

// 숫자 비교
expect(count).toBeGreaterThan(0);
expect(count).toBeLessThanOrEqual(10);
expect(price).toBeCloseTo(9.99, 2);

// 문자열
expect(text).toContain('hello');
expect(text).toMatch(/hello/i);

// 배열
expect(list).toContain('item');
expect(list).toHaveLength(3);
```

---

## 7. 커스텀 메시지

### 실패 시 메시지 추가

```typescript
// 두 번째 인자로 메시지 전달
await expect(page.locator('.error'), '에러 메시지가 표시되어야 함')
  .toBeVisible();

// 복잡한 검증에 유용
await expect(
  page.locator('.notification'),
  `알림이 "${expectedText}" 메시지를 포함해야 함`
).toContainText(expectedText);
```

---

## 8. 타임아웃 설정

### 개별 Assertion 타임아웃

```typescript
// 30초 대기
await expect(page.locator('.slow-element')).toBeVisible({
  timeout: 30000
});
```

### 전역 타임아웃 설정

```typescript
// playwright.config.ts
export default defineConfig({
  expect: {
    timeout: 10000, // 10초 (기본값 5초)
  },
});
```

---

## 9. 부정(Negation)

### not 사용

```typescript
// 보이지 않음
await expect(page.locator('.modal')).not.toBeVisible();

// 텍스트 미포함
await expect(page.locator('body')).not.toContainText('에러');

// 비활성화 아님
await expect(page.locator('button')).not.toBeDisabled();

// 특정 개수 아님
await expect(page.locator('li')).not.toHaveCount(0);
```

---

## 10. 실전 예제

### 로그인 검증

```typescript
test('로그인 성공 검증', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('이메일').fill('user@example.com');
  await page.getByLabel('비밀번호').fill('password123');
  await page.getByRole('button', { name: '로그인' }).click();

  // 페이지 이동 확인
  await expect(page).toHaveURL(/.*dashboard/);

  // 환영 메시지 확인
  await expect(page.locator('.welcome')).toContainText('환영합니다');

  // 로그아웃 버튼 표시 확인
  await expect(page.getByRole('button', { name: '로그아웃' })).toBeVisible();

  // 로그인 버튼 사라짐 확인
  await expect(page.getByRole('button', { name: '로그인' })).not.toBeVisible();
});
```

### 폼 검증

```typescript
test('필수 필드 검증', async ({ page }) => {
  await page.goto('/signup');

  // 빈 폼 제출
  await page.getByRole('button', { name: '가입' }).click();

  // 에러 메시지 확인
  await expect(page.locator('.error-email')).toHaveText('이메일은 필수입니다');
  await expect(page.locator('.error-password')).toHaveText('비밀번호는 필수입니다');

  // 입력 필드 테두리 색상 확인 (에러 상태)
  await expect(page.locator('input[name="email"]'))
    .toHaveCSS('border-color', 'rgb(255, 0, 0)');
});
```

### 목록 검증

```typescript
test('상품 목록 검증', async ({ page }) => {
  await page.goto('/products');

  const products = page.locator('.product-card');

  // 최소 1개 이상
  await expect(products).not.toHaveCount(0);

  // 각 상품에 필수 요소 존재
  for (const product of await products.all()) {
    await expect(product.locator('.name')).toBeVisible();
    await expect(product.locator('.price')).toHaveText(/\d+원/);
    await expect(product.locator('button')).toBeEnabled();
  }
});
```

---

## 11. Best Practices

### DO - 좋은 패턴

```typescript
// 1. Web-First Assertions 사용 (자동 재시도)
await expect(page.locator('.result')).toBeVisible();

// 2. 명확한 검증
await expect(page).toHaveURL(/.*success/);
await expect(page.locator('h1')).toHaveText('완료');

// 3. 부정 검증으로 사라짐 확인
await expect(page.locator('.loading')).not.toBeVisible();
```

### DON'T - 피해야 할 패턴

```typescript
// 1. 명시적 대기 후 generic assertion
await page.waitForSelector('.result');
expect(await page.locator('.result').isVisible()).toBe(true); // 비권장

// 2. 하드코딩된 대기
await page.waitForTimeout(3000);

// 3. 불안정한 텍스트 검증
await expect(page.locator('.date')).toHaveText('2024-01-15'); // 날짜가 변함
```

---

## 다음 단계

> [!tip] 다음으로
> Assertions를 익혔다면 [[04-network|네트워크 가로채기]]에서 API 모킹을 배워보세요.

---

## References

- [Playwright - Assertions](https://playwright.dev/docs/test-assertions)
- [Playwright - API: expect](https://playwright.dev/docs/api/class-genericassertions)
- [Playwright - Visual Comparisons](https://playwright.dev/docs/test-snapshots)
