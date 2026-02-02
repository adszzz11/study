---
date: 2026-02-02
tags:
  - tech
  - playwright
  - learning
  - locator
parent: "[[../README]]"
---

# Playwright - Locator 전략

> [[01-page-control|이전: 페이지 조작]] | [[../README|목차]] | [[03-assertions|다음: Assertions]]

---

## 1. Locator란?

### 개념

**Locator**는 페이지에서 요소를 찾는 방법을 캡슐화한 객체입니다.

```typescript
// Locator 생성 (아직 요소를 찾지 않음)
const button = page.locator('button.submit');

// 액션 수행 시점에 요소를 찾음
await button.click();
```

### Locator vs ElementHandle

| Locator | ElementHandle |
|---------|---------------|
| 액션마다 요소를 새로 찾음 | 특정 시점의 요소 참조 |
| DOM 변경에 강건함 | DOM 변경 시 stale 가능 |
| **권장** | 특수한 경우만 사용 |

```typescript
// Locator (권장)
const locator = page.locator('button');
await locator.click(); // 매번 새로 찾음

// ElementHandle (권장하지 않음)
const element = await page.$('button');
await element?.click(); // 이 참조가 stale될 수 있음
```

---

## 2. 권장 Locator (우선순위순)

### 1순위: 사용자 대면 속성

```typescript
// getByRole - 가장 권장
await page.getByRole('button', { name: '로그인' }).click();
await page.getByRole('heading', { name: '환영합니다' });
await page.getByRole('link', { name: '더 보기' });

// getByText - 텍스트로 찾기
await page.getByText('로그인').click();
await page.getByText('로그인', { exact: true }); // 정확히 일치

// getByLabel - 폼 라벨로 찾기
await page.getByLabel('이메일').fill('test@example.com');
await page.getByLabel('비밀번호').fill('password');

// getByPlaceholder - placeholder로 찾기
await page.getByPlaceholder('이메일을 입력하세요').fill('test@example.com');

// getByAltText - 이미지 alt 텍스트
await page.getByAltText('회사 로고').click();

// getByTitle - title 속성
await page.getByTitle('설정').click();
```

### 2순위: 테스트 전용 속성

```typescript
// getByTestId - data-testid 속성
await page.getByTestId('submit-button').click();
await page.getByTestId('user-profile').isVisible();

// 커스텀 testId 속성 (playwright.config.ts)
// export default defineConfig({
//   use: { testIdAttribute: 'data-test' }
// });
```

### 3순위: CSS/XPath (필요한 경우만)

```typescript
// CSS 선택자
await page.locator('button.primary').click();
await page.locator('#login-form input[type="email"]').fill('test@example.com');

// XPath (복잡한 DOM 구조에서)
await page.locator('xpath=//button[contains(text(), "Submit")]').click();
```

---

## 3. Role 기반 Locator 상세

### 주요 Role 목록

| Role | HTML 요소 예시 |
|------|---------------|
| `button` | `<button>`, `<input type="button">` |
| `link` | `<a href>` |
| `heading` | `<h1>` ~ `<h6>` |
| `textbox` | `<input type="text">`, `<textarea>` |
| `checkbox` | `<input type="checkbox">` |
| `radio` | `<input type="radio">` |
| `combobox` | `<select>` |
| `listbox` | `<select>`, `<ul role="listbox">` |
| `list` | `<ul>`, `<ol>` |
| `listitem` | `<li>` |
| `dialog` | `<dialog>`, `role="dialog"` |
| `alert` | `role="alert"` |
| `navigation` | `<nav>` |
| `main` | `<main>` |

### Role 옵션

```typescript
// name으로 필터
page.getByRole('button', { name: '제출' });

// 정확히 일치
page.getByRole('button', { name: '제출', exact: true });

// 눌린 상태
page.getByRole('button', { pressed: true });

// 확장 상태 (accordion 등)
page.getByRole('button', { expanded: true });

// 체크 상태
page.getByRole('checkbox', { checked: true });

// 레벨 (heading)
page.getByRole('heading', { level: 1 }); // <h1>

// 선택 상태 (탭 등)
page.getByRole('tab', { selected: true });
```

---

## 4. Locator 체이닝과 필터링

### 체이닝 (범위 좁히기)

```typescript
// 특정 컨테이너 내에서 찾기
const modal = page.locator('.modal');
await modal.locator('button.close').click();

// 또는
await page.locator('.modal').locator('button.close').click();
```

### filter() 메서드

```typescript
// 텍스트로 필터
page.locator('li').filter({ hasText: '장바구니' });

// 텍스트가 없는 것 필터
page.locator('li').filter({ hasNotText: '품절' });

// 하위 요소로 필터
page.locator('div.card').filter({
  has: page.locator('span.badge')
});

// 하위 요소가 없는 것
page.locator('div.card').filter({
  hasNot: page.locator('span.sold-out')
});
```

### nth(), first(), last()

```typescript
// 인덱스로 선택 (0부터 시작)
await page.locator('li').nth(2).click(); // 세 번째

// 첫 번째
await page.locator('li').first().click();

// 마지막
await page.locator('li').last().click();
```

---

## 5. 고급 Locator 패턴

### or() - 여러 조건 중 하나

```typescript
// 버튼 또는 링크
const actionButton = page.locator('button.action')
  .or(page.locator('a.action'));
await actionButton.click();
```

### and() - 모든 조건 충족

```typescript
// visible이면서 enabled인 버튼
const button = page.getByRole('button')
  .and(page.locator(':visible'));
```

### 부모/형제 요소 찾기

```typescript
// XPath로 부모 요소
page.locator('span.icon').locator('xpath=..');

// XPath로 형제 요소
page.locator('label:has-text("이름")').locator('xpath=following-sibling::input');
```

### 텍스트 매칭

```typescript
// 포함
page.locator('text=환영합니다');

// 정확히 일치
page.locator('text="로그인"');

// 정규식
page.locator('text=/Log\s?in/i');
```

---

## 6. FrameLocator

### iframe 내 요소 선택

```typescript
// 프레임 내 요소 선택
const frame = page.frameLocator('iframe#editor');
await frame.locator('button.bold').click();

// 중첩 프레임
const nestedFrame = page
  .frameLocator('iframe.outer')
  .frameLocator('iframe.inner');
await nestedFrame.locator('input').fill('텍스트');
```

---

## 7. Best Practices

### DO - 좋은 패턴

```typescript
// 1. Role 기반 Locator 사용
await page.getByRole('button', { name: '제출' }).click();

// 2. 사용자 관점의 선택자
await page.getByLabel('이메일').fill('test@example.com');
await page.getByPlaceholder('검색어를 입력하세요').fill('playwright');

// 3. 테스트 ID 사용 (복잡한 경우)
await page.getByTestId('user-menu').click();

// 4. 명시적인 대기 대신 Locator 사용
await page.locator('button.submit').click(); // 자동 대기
```

### DON'T - 피해야 할 패턴

```typescript
// 1. XPath 전체 경로
await page.locator('xpath=/html/body/div[1]/div[2]/button').click();

// 2. 구현 세부사항 의존
await page.locator('.btn-primary.sc-abc123').click();

// 3. 불안정한 인덱스
await page.locator('button').nth(5).click();

// 4. 명시적 타임아웃 대신 대기
await page.waitForTimeout(3000); // 피하세요
await page.locator('button').click(); // 대신 자동 대기 활용
```

### Locator 우선순위 정리

```
1. getByRole()        ← 가장 권장 (접근성 기반)
2. getByLabel()       ← 폼 요소
3. getByPlaceholder() ← 입력 필드
4. getByText()        ← 고유 텍스트
5. getByTestId()      ← 다른 방법이 없을 때
6. CSS Selector       ← 필요한 경우만
7. XPath              ← 최후의 수단
```

---

## 8. 디버깅

### Codegen으로 Locator 확인

```bash
npx playwright codegen https://example.com
```

### VS Code에서 Locator 선택

1. VS Code Playwright 확장 설치
2. 테스트 파일에서 "Pick Locator" 클릭
3. 브라우저에서 요소 클릭

### Locator 테스트

```typescript
// 요소가 몇 개 매칭되는지 확인
console.log(await page.locator('button').count());

// 모든 매칭 요소의 텍스트
console.log(await page.locator('li').allTextContents());
```

---

## 9. 실전 예제

### 동적 테이블에서 특정 행 찾기

```typescript
// 이름이 "홍길동"인 행의 삭제 버튼 클릭
const row = page.locator('tr').filter({
  has: page.locator('td', { hasText: '홍길동' })
});
await row.locator('button.delete').click();
```

### 드롭다운 메뉴 선택

```typescript
// 메뉴 열기
await page.getByRole('button', { name: '설정' }).click();

// 메뉴 아이템 선택
await page.getByRole('menuitem', { name: '로그아웃' }).click();
```

### 모달 내 폼 작성

```typescript
const modal = page.getByRole('dialog');

await modal.getByLabel('제목').fill('새 항목');
await modal.getByLabel('설명').fill('설명 내용');
await modal.getByRole('button', { name: '저장' }).click();

// 모달이 닫혔는지 확인
await expect(modal).not.toBeVisible();
```

---

## 다음 단계

> [!tip] 다음으로
> Locator 전략을 이해했다면 [[03-assertions|Assertions]]에서 검증 방법을 배워보세요.

---

## References

- [Playwright - Locators](https://playwright.dev/docs/locators)
- [Playwright - Best Practices](https://playwright.dev/docs/best-practices)
- [Playwright - Other Locators](https://playwright.dev/docs/other-locators)
