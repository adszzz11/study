---
date: 2026-02-02
tags:
  - tech
  - stagehand
  - cheatsheet
  - reference
parent: "[[README]]"
---

# Stagehand 치트시트

> [[05-projects|이전: 프로젝트]] | [[README|목차]]

---

## Quick Reference

### 설치

```bash
npm install @browserbasehq/stagehand zod
```

### 기본 설정

```typescript
import { Stagehand } from "@browserbasehq/stagehand";
import { z } from "zod";

const stagehand = new Stagehand({
  env: "LOCAL",
  modelName: "gpt-4o",
  modelClientOptions: { apiKey: process.env.OPENAI_API_KEY },
  enableCaching: true,
  headless: false,
  verbose: 1
});

await stagehand.init();
// ... 작업 수행
await stagehand.close();
```

---

## Core API

### act() - 액션 수행

```typescript
// 기본 사용
await stagehand.act({ action: "로그인 버튼 클릭" });

// 변수 사용
await stagehand.act({
  action: "검색창에 {{query}} 입력",
  variables: { query: "Stagehand" }
});

// 비전 모드
await stagehand.act({
  action: "빨간색 버튼 클릭",
  useVision: true
});
```

### extract() - 데이터 추출

```typescript
const result = await stagehand.extract({
  instruction: "상품 정보 추출",
  schema: z.object({
    name: z.string().describe("상품명"),
    price: z.number().describe("가격"),
    rating: z.number().optional()
  })
});
```

### observe() - 페이지 관찰

```typescript
// 모든 가능한 액션
const actions = await stagehand.observe();

// 특정 영역
const navActions = await stagehand.observe({
  instruction: "네비게이션 메뉴의 액션들"
});
```

### Agent - 자율 에이전트

```typescript
const agent = stagehand.agent({
  provider: "openai",
  model: "computer-use-preview",
  maxSteps: 20
});

await agent.execute("Amazon에서 MacBook 검색 후 최저가 찾기");
```

---

## Zod 스키마 패턴

### 기본 타입

```typescript
z.string()                    // 문자열
z.number()                    // 숫자
z.boolean()                   // 불린
z.array(z.string())           // 배열
z.object({ ... })             // 객체
```

### 수정자

```typescript
z.string().optional()         // 선택적
z.number().default(0)         // 기본값
z.string().nullable()         // null 허용
z.string().describe("설명")   // LLM 힌트
```

### 자주 쓰는 스키마

```typescript
// 상품 목록
const ProductsSchema = z.object({
  products: z.array(z.object({
    name: z.string(),
    price: z.number(),
    url: z.string().optional()
  }))
});

// 기사/콘텐츠
const ArticleSchema = z.object({
  title: z.string(),
  content: z.string(),
  author: z.string().optional(),
  date: z.string().optional()
});

// 테이블 데이터
const TableSchema = z.object({
  rows: z.array(z.object({
    columns: z.array(z.string())
  }))
});
```

---

## Playwright 통합

```typescript
// page 객체 접근
const page = stagehand.page;

// 페이지 이동
await page.goto("https://example.com");

// 대기
await page.waitForLoadState("networkidle");
await page.waitForSelector(".element");

// 스크린샷
await page.screenshot({ path: "screenshot.png" });

// 리소스 차단
await page.route("**/*.{png,jpg}", route => route.abort());
```

---

## 설정 옵션

| 옵션 | 타입 | 기본값 | 설명 |
|------|------|--------|------|
| `env` | "LOCAL" \| "BROWSERBASE" | "LOCAL" | 실행 환경 |
| `modelName` | string | - | LLM 모델 |
| `enableCaching` | boolean | false | 캐싱 |
| `headless` | boolean | false | 헤드리스 |
| `verbose` | 0 \| 1 \| 2 | 0 | 로그 레벨 |

---

## 자주 쓰는 패턴

### 로그인

```typescript
await stagehand.act({ action: "이메일에 user@email.com 입력" });
await stagehand.act({ action: "비밀번호에 password123 입력" });
await stagehand.act({ action: "로그인 버튼 클릭" });
```

### 검색 후 추출

```typescript
await stagehand.act({ action: "검색창에 'keyword' 입력 후 검색" });
await page.waitForLoadState("networkidle");
const results = await stagehand.extract({
  instruction: "검색 결과 목록",
  schema: ResultsSchema
});
```

### 페이지네이션

```typescript
const allData = [];
while (true) {
  const data = await stagehand.extract({ ... });
  allData.push(...data.items);

  const actions = await stagehand.observe();
  if (!actions.some(a => a.action.includes("다음"))) break;

  await stagehand.act({ action: "다음 페이지" });
}
```

### 조건부 처리

```typescript
const actions = await stagehand.observe();
if (actions.some(a => a.action.includes("팝업"))) {
  await stagehand.act({ action: "팝업 닫기" });
}
```

### 에러 처리

```typescript
try {
  await stagehand.act({ action: "버튼 클릭" });
} catch (error) {
  const actions = await stagehand.observe();
  console.log("가능한 액션:", actions);
}
```

---

## 환경 변수

```bash
# .env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
BROWSERBASE_API_KEY=...
BROWSERBASE_PROJECT_ID=...
```

---

## 디버깅

```typescript
// 상세 로그
const stagehand = new Stagehand({ verbose: 2 });

// 스크린샷 저장
await stagehand.page.screenshot({ path: "debug.png" });

// 가능한 액션 확인
const actions = await stagehand.observe();
console.log(actions);
```

---

## 성능 팁

1. `enableCaching: true` 설정
2. 명확한 작업은 Playwright 직접 사용
3. 가벼운 모델 사용 (`gpt-4o-mini`)
4. 불필요한 리소스 차단
5. `observe()` 결과 재사용

---

## 링크

- [공식 문서](https://docs.stagehand.dev)
- [GitHub](https://github.com/browserbase/stagehand)
- [npm](https://www.npmjs.com/package/@browserbasehq/stagehand)
- [Browserbase](https://browserbase.com)

---

## 관련 학습 자료

- [[README|Stagehand 학습 가이드]]
- [[01-overview|개요]]
- [[04-learning/01-setup|초기 설정]]
- [[04-learning/02-act|act() 상세]]
- [[04-learning/03-extract|extract() 상세]]
- [[05-projects|실전 프로젝트]]
