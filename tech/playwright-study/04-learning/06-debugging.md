---
date: 2026-02-02
tags:
  - tech
  - playwright
  - learning
  - debugging
  - codegen
parent: "[[../README]]"
---

# Playwright - Codegen과 디버깅

> [[05-config|이전: 설정]] | [[../README|목차]] | [[../05-projects|다음: 실전 프로젝트]]

---

## 1. Codegen (코드 생성기)

### 개요

Codegen은 브라우저에서 수행하는 동작을 녹화하여 Playwright 코드를 자동 생성해주는 도구입니다.

### 기본 사용법

```bash
# 빈 브라우저로 시작
npx playwright codegen

# 특정 URL로 시작
npx playwright codegen https://example.com

# 특정 뷰포트
npx playwright codegen --viewport-size=1280,720 https://example.com

# 특정 브라우저
npx playwright codegen --browser=firefox https://example.com

# 모바일 에뮬레이션
npx playwright codegen --device="iPhone 12" https://example.com
```

### Codegen 옵션

| 옵션 | 설명 |
|------|------|
| `--browser=<browser>` | 브라우저 선택 (chromium, firefox, webkit) |
| `--device=<device>` | 디바이스 에뮬레이션 |
| `--viewport-size=<w,h>` | 뷰포트 크기 |
| `--color-scheme=<scheme>` | 색상 스킴 (dark, light) |
| `--lang=<lang>` | 브라우저 언어 |
| `--save-storage=<file>` | 스토리지 상태 저장 |
| `--load-storage=<file>` | 스토리지 상태 로드 |

### Codegen 인터페이스

```
+------------------+----------------------+
|    브라우저      |    Playwright        |
|                  |    Inspector         |
|  [웹페이지]      |  +---------------+   |
|                  |  | 생성된 코드   |   |
|  클릭/입력 녹화  |  | await page... |   |
|                  |  +---------------+   |
|                  |  [Locator] [Assert]  |
+------------------+----------------------+
```

### 녹화 팁

1. **Locator 버튼**: 요소 위에 마우스를 올리면 추천 Locator 표시
2. **Assert 버튼**: 검증 코드 추가 (toBeVisible, toHaveText 등)
3. **Record 버튼**: 녹화 시작/중지
4. **코드 복사**: 생성된 코드를 테스트 파일에 붙여넣기

---

## 2. UI 모드

### 개요

UI 모드는 대화형 테스트 실행 환경으로, 테스트를 시각적으로 실행하고 디버깅할 수 있습니다.

### 시작

```bash
npx playwright test --ui
```

### UI 모드 기능

| 기능 | 설명 |
|------|------|
| 테스트 탐색기 | 파일/테스트 목록 |
| Watch 모드 | 파일 변경 시 자동 재실행 |
| 타임라인 | 각 단계별 스크린샷 |
| DOM 스냅샷 | 각 단계의 DOM 상태 |
| 네트워크 탭 | 요청/응답 확인 |
| 콘솔 탭 | 콘솔 로그 |
| 소스 탭 | 테스트 코드 |

### Watch 모드

```
UI 모드에서:
1. 테스트 선택
2. "Watch" 체크박스 활성화
3. 테스트 코드 수정
4. 자동으로 해당 테스트만 재실행
```

---

## 3. 디버그 모드

### 기본 디버깅

```bash
# 디버그 모드로 실행
npx playwright test --debug

# 특정 테스트 디버그
npx playwright test --debug tests/login.spec.ts

# 특정 라인에서 시작
npx playwright test --debug:10 tests/login.spec.ts
```

### PWDEBUG 환경 변수

```bash
# Inspector 열기
PWDEBUG=1 npx playwright test

# 콘솔 디버깅
PWDEBUG=console npx playwright test
```

### 코드에서 일시정지

```typescript
test('디버깅 중', async ({ page }) => {
  await page.goto('/');

  // 여기서 일시정지 (Inspector 열림)
  await page.pause();

  await page.click('button');
});
```

### Playwright Inspector

Inspector가 열리면:
- **Step Over**: 다음 Playwright 명령으로 이동
- **Step Into**: 함수 내부로 진입
- **Resume**: 다음 breakpoint까지 실행
- **Record**: 추가 동작 녹화

---

## 4. Trace Viewer

### 개요

Trace Viewer는 테스트 실행의 전체 기록을 시각화하는 도구입니다.

### Trace 활성화

```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    trace: 'on-first-retry', // 첫 재시도에서 trace 기록
  },
});

// 옵션:
// 'on' - 항상 기록
// 'off' - 기록 안 함
// 'on-first-retry' - 첫 재시도에서만 (권장)
// 'retain-on-failure' - 실패 시 유지
```

### Trace 보기

```bash
# HTML 리포트에서 Trace 열기
npx playwright show-report

# Trace 파일 직접 열기
npx playwright show-trace trace.zip
```

### Trace Viewer 인터페이스

| 패널 | 내용 |
|------|------|
| Actions | 수행된 액션 목록 |
| Screenshots | 각 단계 스크린샷 |
| Snapshots | DOM 스냅샷 (요소 검사 가능) |
| Network | 네트워크 요청 |
| Console | 콘솔 로그 |
| Source | 테스트 소스 코드 |
| Call | 호출 정보 |

### Trace 분석 팁

1. **Timeline**: 실패 지점 확인
2. **Before/After**: 액션 전후 스크린샷 비교
3. **Network**: 실패한 API 요청 확인
4. **Console**: JavaScript 에러 확인

---

## 5. VS Code 통합

### Playwright Test for VS Code

1. 확장 설치: "Playwright Test for VS Code"
2. 기능:
   - 테스트 탐색기에서 실행
   - Locator 클릭으로 선택
   - 디버그 breakpoint
   - 실시간 Watch 모드

### VS Code에서 디버깅

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Playwright Tests",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/node_modules/.bin/playwright",
      "args": ["test", "--debug"],
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}"
    }
  ]
}
```

### Pick Locator

1. VS Code에서 테스트 파일 열기
2. 왼쪽 Testing 탭 클릭
3. "Pick locator" 클릭
4. 브라우저에서 요소 클릭
5. 선택된 Locator가 코드에 삽입됨

---

## 6. 스크린샷과 비디오

### 스크린샷

```typescript
// 테스트 중 수동 스크린샷
await page.screenshot({ path: 'screenshot.png' });

// 요소 스크린샷
await page.locator('.chart').screenshot({ path: 'chart.png' });
```

### 설정으로 자동 캡처

```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    screenshot: 'only-on-failure', // 실패 시에만
    video: 'retain-on-failure',    // 실패 시 비디오 유지
  },
});
```

### 비디오 옵션

| 옵션 | 설명 |
|------|------|
| `'off'` | 비디오 없음 |
| `'on'` | 항상 녹화 |
| `'retain-on-failure'` | 실패 시만 유지 |
| `'on-first-retry'` | 첫 재시도에서 녹화 |

---

## 7. 콘솔 로깅

### 브라우저 콘솔 로그 캡처

```typescript
test('콘솔 로그 확인', async ({ page }) => {
  // 콘솔 이벤트 리스너
  page.on('console', msg => {
    console.log(`Browser console: ${msg.type()}: ${msg.text()}`);
  });

  // 에러만 캡처
  page.on('console', msg => {
    if (msg.type() === 'error') {
      console.error(`Browser error: ${msg.text()}`);
    }
  });

  await page.goto('/');
});
```

### 페이지 에러 캡처

```typescript
test('페이지 에러 확인', async ({ page }) => {
  page.on('pageerror', error => {
    console.error(`Page error: ${error.message}`);
  });

  await page.goto('/');
});
```

---

## 8. 트러블슈팅

### 일반적인 문제

#### 1. 요소를 찾을 수 없음

```typescript
// 문제: 요소가 아직 로드되지 않음
await page.click('button'); // TimeoutError

// 해결: Locator가 자동 대기하지만, DOM이 완전히 로드될 때까지 추가 대기
await page.locator('button').waitFor();
await page.locator('button').click();

// 또는 명시적 대기
await page.waitForLoadState('networkidle');
```

#### 2. Flaky 테스트

```typescript
// 문제: 애니메이션으로 인한 불안정
await page.click('button');

// 해결 1: 애니메이션 비활성화
await page.addStyleTag({
  content: `*, *::before, *::after {
    animation-duration: 0s !important;
    transition-duration: 0s !important;
  }`
});

// 해결 2: 강제 클릭 (권장하지 않음)
await page.click('button', { force: true });
```

#### 3. iframe 내 요소

```typescript
// 문제: iframe 내 요소에 접근 불가
await page.click('button'); // 못 찾음

// 해결: frameLocator 사용
const frame = page.frameLocator('iframe#editor');
await frame.locator('button').click();
```

#### 4. 새 탭/팝업

```typescript
// 문제: 새 탭의 요소에 접근 불가

// 해결: 팝업 이벤트 대기
const [newPage] = await Promise.all([
  page.waitForEvent('popup'),
  page.click('a[target="_blank"]')
]);
await newPage.waitForLoadState();
await newPage.locator('h1').click();
```

### 디버깅 체크리스트

```
[ ] 올바른 Locator인가? (Codegen으로 확인)
[ ] 요소가 visible 상태인가?
[ ] 요소가 enabled 상태인가?
[ ] iframe 내부에 있는가?
[ ] 새 탭/팝업인가?
[ ] 네트워크 요청이 완료되었는가?
[ ] 애니메이션이 완료되었는가?
[ ] 타임아웃이 충분한가?
```

---

## 9. 실전 디버깅 예제

### 로그인 실패 디버깅

```typescript
test('로그인 디버깅', async ({ page }) => {
  await page.goto('/login');

  // 네트워크 요청 로깅
  page.on('request', request => {
    if (request.url().includes('/api/')) {
      console.log('Request:', request.method(), request.url());
    }
  });

  page.on('response', response => {
    if (response.url().includes('/api/')) {
      console.log('Response:', response.status(), response.url());
    }
  });

  // 콘솔 로그
  page.on('console', msg => console.log('Console:', msg.text()));

  await page.fill('#email', 'test@example.com');
  await page.fill('#password', 'password');

  // 일시정지하여 상태 확인
  await page.pause();

  await page.click('button[type="submit"]');

  // 스크린샷 저장
  await page.screenshot({ path: 'debug-login.png' });
});
```

---

## 다음 단계

> [!tip] 다음으로
> 디버깅 방법을 익혔다면 [[../05-projects|실전 프로젝트]]에서 Best Practices를 배워보세요.

---

## References

- [Playwright - Debugging](https://playwright.dev/docs/debug)
- [Playwright - Trace Viewer](https://playwright.dev/docs/trace-viewer)
- [Playwright - Codegen](https://playwright.dev/docs/codegen)
- [Playwright - VS Code Extension](https://playwright.dev/docs/getting-started-vscode)
