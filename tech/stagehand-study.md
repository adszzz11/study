# Stagehand 심층 스터디 가이드

> **한 줄 정의**: 자연어와 코드를 결합하여 AI 기반 웹 브라우저 자동화를 가능하게 하는 프레임워크 (Browserbase 개발)

---

## Part 1: 개요

### 1.1 정의 및 핵심 개념

**3줄 요약**:
1. 자연어 명령("로그인 버튼 클릭")과 코드를 결합한 하이브리드 브라우저 자동화
2. CSS 선택자 없이 LLM이 페이지를 이해하고 요소를 찾아 조작
3. 깨지기 쉬운 선택자 대신 AI가 동적으로 적응하여 유지보수 비용 절감

**핵심 키워드**: `#AI자동화` `#웹에이전트` `#자연어브라우저` `#셀렉터리스` `#Browserbase`

**기존 자동화 vs Stagehand**:

```
기존 방식 (Playwright/Puppeteer):
await page.click('button.login-btn-v2.primary');  // 클래스 변경 시 깨짐

Stagehand 방식:
await stagehand.act({ action: "로그인 버튼을 클릭" });  // AI가 알아서 찾음
```

**핵심 API 3가지**:
| 메서드 | 설명 | 예시 |
|--------|------|------|
| `act()` | 자연어로 액션 수행 | "검색창에 'AI' 입력 후 Enter" |
| `extract()` | 페이지에서 데이터 추출 | "모든 상품 가격 추출" |
| `observe()` | 페이지 상태 관찰 | "현재 로그인 상태인지 확인" |

### 1.2 Quick Start (30초 체험)

```bash
# 1. 설치
npm install @browserbasehq/stagehand
```

```typescript
// 2. 기본 사용 (TypeScript)
import { Stagehand } from "@browserbasehq/stagehand";

async function main() {
    const stagehand = new Stagehand({
        env: "LOCAL",  // 또는 "BROWSERBASE"
        modelName: "gpt-4o",
        modelClientOptions: {
            apiKey: process.env.OPENAI_API_KEY,
        },
    });

    await stagehand.init();
    const page = stagehand.page;

    // 페이지 이동
    await page.goto("https://news.ycombinator.com");

    // 자연어로 액션 수행
    await stagehand.act({ action: "첫 번째 뉴스 링크를 클릭" });

    // 데이터 추출
    const { title } = await stagehand.extract({
        instruction: "기사 제목을 추출",
        schema: { title: "string" }
    });

    console.log("제목:", title);
    await stagehand.close();
}

main();
```

```bash
# 3. 실행
npx ts-node example.ts
```

### 1.3 왜 Stagehand인가?

**장점**:
- **선택자 불필요**: CSS/XPath 대신 자연어로 요소 지정
- **자가 치유(Self-healing)**: 페이지 변경 시 AI가 자동 적응
- **하이브리드**: 정확한 부분은 코드, 불확실한 부분은 AI
- **캐싱**: 반복 동작은 LLM 호출 없이 실행 (비용/속도 절감)
- **Playwright 통합**: 기존 Playwright 코드와 함께 사용 가능

**단점**:
- LLM API 비용 발생 (OpenAI/Anthropic)
- 로컬 모델(Ollama) 권장하지 않음
- 복잡한 인터랙션은 여전히 코드 필요
- 2FA/CAPTCHA 자동 해결 미내장

**주요 사용 사례**:
- 동적 웹사이트 스크래핑
- E2E 테스트 (선택자 유지보수 감소)
- RPA (반복 업무 자동화)
- AI 에이전트의 웹 브라우징 기능

---

## Part 2: 생태계 파악

### 2.1 관련 기술/용어 맵

```
┌─────────────────────────────────────────────────────────────┐
│                    Stagehand 생태계                          │
├─────────────────────────────────────────────────────────────┤
│  [Core API]                                                  │
│  ├── act(): 자연어로 액션 수행                               │
│  ├── extract(): 구조화된 데이터 추출                         │
│  ├── observe(): 페이지 상태 관찰                             │
│  └── page: Playwright Page 객체 (직접 접근)                  │
│                                                              │
│  [지원 LLM]                                                  │
│  ├── OpenAI: gpt-4o, gpt-4o-mini (권장)                     │
│  ├── Anthropic: claude-sonnet-4-20250514, claude-opus-4-20250514 (권장)     │
│  └── Local: Ollama (권장하지 않음)                           │
│                                                              │
│  [실행 환경]                                                 │
│  ├── LOCAL: 로컬 브라우저 (Playwright)                       │
│  ├── BROWSERBASE: 클라우드 브라우저                          │
│  └── Cloudflare Browser Rendering: Edge 환경                 │
│                                                              │
│  [Stagehand Agent]                                           │
│  └── 고수준 자율 에이전트 (multi-step 작업)                   │
│                                                              │
│  [v3 변경사항]                                               │
│  ├── Playwright 의존성 제거 → 모듈형 드라이버               │
│  ├── Puppeteer, CDP 직접 지원                                │
│  └── 44% 성능 향상                                           │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 함께 자주 쓰이는 기술 스택

| 영역 | 기술 | 용도 |
|------|------|------|
| **LLM** | OpenAI, Anthropic | 자연어 처리 |
| **브라우저 인프라** | Browserbase | 클라우드 브라우저 |
| **AI 프레임워크** | LangChain, CrewAI | 에이전트 통합 |
| **워크플로우** | Prefect, Temporal | 스케줄링 |
| **데이터 저장** | Supabase, PostgreSQL | 추출 데이터 저장 |

### 2.3 경쟁/대안 기술 비교

| 기준 | Stagehand | Browser Use | Skyvern | Playwright |
|------|-----------|-------------|---------|------------|
| **접근 방식** | 코드 + 자연어 | Python + LLM | 컴퓨터 비전 | 순수 코드 |
| **선택자 필요** | 선택적 | 불필요 | 불필요 | 필수 |
| **LLM 필수** | 예 | 예 | 예 | 아니오 |
| **자가 치유** | 예 (캐싱) | 매번 재분석 | 예 | 아니오 |
| **2FA/CAPTCHA** | 미내장 | 미내장 | 내장 | 미내장 |
| **오픈소스** | 예 | 예 | 부분 | 예 |
| **주 언어** | TypeScript | Python | Python | 다수 |

**선택 가이드**:
- **Stagehand**: TypeScript/JavaScript 프로젝트, Playwright 경험자
- **Browser Use**: Python 프로젝트, 빠른 프로토타이핑
- **Skyvern**: 기업용, CAPTCHA 해결 필요
- **Playwright**: 정적 선택자로 충분한 경우

### 2.4 최신 트렌드 및 동향 (2025)

- **Stagehand v3 출시 (2025.10)**: Playwright 의존성 제거, 44% 성능 향상
- **모듈형 드라이버 시스템**: Puppeteer, CDP 직접 지원
- **월 50만 다운로드**: 프로덕션 채택 증가
- **Cloudflare 통합**: Edge 환경에서 실행 가능
- **자동 캐싱**: 반복 액션 시 LLM 호출 없이 실행

---

## Part 3: 레퍼런스

### 3.1 공식 문서 및 필수 링크

| 리소스 | URL | 설명 |
|--------|-----|------|
| 🟢 공식 문서 | [docs.stagehand.dev](https://docs.stagehand.dev/) | 메인 문서 |
| 🟢 GitHub | [github.com/browserbase/stagehand](https://github.com/browserbase/stagehand) | 소스 코드 |
| 🟢 Stagehand.dev | [stagehand.dev](https://www.stagehand.dev/) | 공식 사이트 |
| 🟡 Browserbase | [browserbase.com](https://www.browserbase.com/) | 클라우드 브라우저 |

### 3.2 추천 학습 자료

**🟢 입문**:
- [Introducing Stagehand](https://docs.stagehand.dev/) - 공식 소개 문서
- [Stagehand Quickstart](https://docs.stagehand.dev/quickstart) - 빠른 시작

**🟡 중급**:
- [Browserbase Blog: Stagehand v3](https://www.browserbase.com/blog/stagehand-v3) - v3 기능
- [Stagehand Agent](https://docs.stagehand.dev/agent) - 자율 에이전트

**🔴 고급**:
- [Cloudflare Stagehand Integration](https://developers.cloudflare.com/browser-rendering/stagehand/) - Edge 배포
- [GitHub Examples](https://github.com/browserbase/stagehand/tree/main/examples) - 실전 예제

### 3.3 커뮤니티 및 질문할 곳

- **GitHub Issues**: [browserbase/stagehand/issues](https://github.com/browserbase/stagehand/issues)
- **Browserbase Discord**: 공식 커뮤니티
- **Twitter/X**: @browseraborbase

### 3.4 실무 예제/오픈소스 프로젝트

- [Stagehand Examples](https://github.com/browserbase/stagehand/tree/main/examples)
- [Stagehand + CrewAI Integration](https://docs.crewai.com/tools/stagehand-tools)

---

## Part 4: 상세 학습 로드맵

### 4.1 초기 설정 및 구조

📌 **핵심 개념**

Stagehand는 Playwright 위에 구축된 AI 레이어입니다. `page` 객체를 통해 Playwright API에 직접 접근할 수도 있습니다.

💻 **코드 예제: 초기화 옵션**

```typescript
import { Stagehand } from "@browserbasehq/stagehand";

// 로컬 실행
const localStagehand = new Stagehand({
    env: "LOCAL",
    headless: false,  // 브라우저 창 표시
    verbose: 1,       // 로깅 레벨 (0-2)
    modelName: "gpt-4o",
    modelClientOptions: {
        apiKey: process.env.OPENAI_API_KEY,
    },
});

// Browserbase 클라우드 실행
const cloudStagehand = new Stagehand({
    env: "BROWSERBASE",
    apiKey: process.env.BROWSERBASE_API_KEY,
    projectId: process.env.BROWSERBASE_PROJECT_ID,
    modelName: "claude-sonnet-4-20250514",
    modelClientOptions: {
        apiKey: process.env.ANTHROPIC_API_KEY,
    },
});

// 초기화 및 페이지 접근
await localStagehand.init();
const page = localStagehand.page;  // Playwright Page 객체

// Playwright API 직접 사용 가능
await page.goto("https://example.com");
await page.waitForSelector("h1");
const title = await page.title();

// 종료
await localStagehand.close();
```

**Playwright와 혼합 사용**:
```typescript
const stagehand = new Stagehand({ env: "LOCAL", modelName: "gpt-4o" });
await stagehand.init();
const page = stagehand.page;

// Playwright로 정확한 조작
await page.goto("https://shop.example.com");
await page.fill("#search", "laptop");

// Stagehand로 동적 요소 처리
await stagehand.act({ action: "검색 결과에서 첫 번째 상품 클릭" });

// 다시 Playwright
const price = await page.locator(".price").textContent();
console.log("가격:", price);
```

✅ **체크포인트**
- [ ] Stagehand를 초기화하고 `page` 객체에 접근할 수 있는가?
- [ ] LOCAL과 BROWSERBASE 환경의 차이를 이해하는가?
- [ ] Playwright API와 Stagehand API를 혼합할 수 있는가?

⚠️ **흔한 실수**
- `init()` 호출 필수 (page 접근 전)
- `close()` 호출 안 하면 브라우저 프로세스 남음
- API 키 환경 변수 설정 확인

🔗 **더 알아보기**: [Configuration](https://docs.stagehand.dev/configuration)

---

### 4.2 act() - 자연어 액션

📌 **핵심 개념**

`act()`는 자연어 명령을 받아 페이지에서 해당 액션을 수행합니다. 클릭, 입력, 스크롤 등을 처리합니다.

💻 **코드 예제: 다양한 액션**

```typescript
import { Stagehand } from "@browserbasehq/stagehand";

const stagehand = new Stagehand({
    env: "LOCAL",
    modelName: "gpt-4o",
    modelClientOptions: { apiKey: process.env.OPENAI_API_KEY }
});

await stagehand.init();
await stagehand.page.goto("https://demo.playwright.dev/todomvc");

// 1. 기본 클릭
await stagehand.act({ action: "What needs to be done 입력창을 클릭" });

// 2. 텍스트 입력
await stagehand.act({ action: "'우유 사기'를 입력하고 Enter 키를 누름" });
await stagehand.act({ action: "'빵 사기'를 입력하고 Enter 키를 누름" });

// 3. 체크박스 토글
await stagehand.act({ action: "첫 번째 할일 항목을 완료 처리" });

// 4. 필터 클릭
await stagehand.act({ action: "Active 필터를 클릭" });

// 5. 삭제
await stagehand.act({ action: "완료된 항목들을 모두 삭제" });

// 6. 복합 액션
await stagehand.act({
    action: "새 할일로 '청소하기'를 추가하고 완료 체크"
});

await stagehand.close();
```

**액션 결과 확인**:
```typescript
const result = await stagehand.act({
    action: "로그인 버튼을 클릭"
});

console.log("성공 여부:", result.success);
console.log("수행한 액션:", result.action);
console.log("메시지:", result.message);

// 실패 시 처리
if (!result.success) {
    console.error("액션 실패:", result.message);
    // 대체 로직...
}
```

**변수 사용**:
```typescript
const searchTerm = "Stagehand tutorial";
const username = "user@example.com";

// 템플릿 리터럴로 변수 삽입
await stagehand.act({
    action: `검색창에 '${searchTerm}'을 입력하고 검색 버튼 클릭`
});

await stagehand.act({
    action: `이메일 입력란에 '${username}'을 입력`
});
```

✅ **체크포인트**
- [ ] `act()`로 클릭, 입력, 스크롤 등을 수행할 수 있는가?
- [ ] 액션 결과를 확인하고 실패 시 처리할 수 있는가?
- [ ] 변수를 액션 명령에 포함시킬 수 있는가?

⚠️ **흔한 실수**
- 너무 복잡한 액션은 단계별로 분리
- 명확하고 구체적인 명령어 사용
- 한국어/영어 모두 가능하지만 영어가 더 정확할 수 있음

🔗 **더 알아보기**: [act() API](https://docs.stagehand.dev/api/act)

---

### 4.3 extract() - 데이터 추출

📌 **핵심 개념**

`extract()`는 페이지에서 구조화된 데이터를 추출합니다. Zod 스키마 또는 JSON 스키마로 출력 형식을 정의합니다.

💻 **코드 예제: 데이터 추출**

```typescript
import { Stagehand } from "@browserbasehq/stagehand";
import { z } from "zod";

const stagehand = new Stagehand({
    env: "LOCAL",
    modelName: "gpt-4o",
    modelClientOptions: { apiKey: process.env.OPENAI_API_KEY }
});

await stagehand.init();
await stagehand.page.goto("https://news.ycombinator.com");

// 1. Zod 스키마로 구조화된 추출
const NewsSchema = z.object({
    articles: z.array(z.object({
        title: z.string().describe("기사 제목"),
        url: z.string().describe("기사 링크"),
        points: z.number().describe("포인트 수"),
        comments: z.number().describe("댓글 수")
    })).describe("상위 5개 뉴스 기사")
});

const result = await stagehand.extract({
    instruction: "페이지에서 상위 5개 뉴스 기사의 정보를 추출",
    schema: NewsSchema
});

console.log("추출 결과:", result.articles);

// 2. 간단한 텍스트 추출
const SimpleSchema = z.object({
    headline: z.string().describe("메인 헤드라인")
});

const { headline } = await stagehand.extract({
    instruction: "페이지의 메인 헤드라인을 추출",
    schema: SimpleSchema
});

// 3. 리스트 추출
const ListSchema = z.object({
    items: z.array(z.string()).describe("모든 항목 텍스트")
});

const { items } = await stagehand.extract({
    instruction: "네비게이션 메뉴의 모든 항목 추출",
    schema: ListSchema
});

await stagehand.close();
```

**JSON 스키마 사용**:
```typescript
// Zod 대신 JSON 스키마도 가능
const result = await stagehand.extract({
    instruction: "상품 정보 추출",
    schema: {
        type: "object",
        properties: {
            name: { type: "string", description: "상품명" },
            price: { type: "number", description: "가격 (숫자만)" },
            inStock: { type: "boolean", description: "재고 여부" }
        },
        required: ["name", "price"]
    }
});
```

**테이블 데이터 추출**:
```typescript
const TableSchema = z.object({
    rows: z.array(z.object({
        column1: z.string(),
        column2: z.string(),
        column3: z.number()
    }))
});

const tableData = await stagehand.extract({
    instruction: "테이블의 모든 행 데이터를 추출 (헤더 제외)",
    schema: TableSchema
});
```

✅ **체크포인트**
- [ ] Zod 스키마로 추출 형식을 정의할 수 있는가?
- [ ] 배열/중첩 객체를 추출할 수 있는가?
- [ ] 설명(describe)을 활용하여 추출 정확도를 높일 수 있는가?

⚠️ **흔한 실수**
- 스키마의 `describe()`는 LLM에게 힌트 제공 - 명확하게 작성
- 숫자 추출 시 문자열로 오면 타입 변환 필요
- 너무 많은 데이터 요청 시 토큰 제한 주의

🔗 **더 알아보기**: [extract() API](https://docs.stagehand.dev/api/extract)

---

### 4.4 observe() - 페이지 관찰

📌 **핵심 개념**

`observe()`는 페이지 상태를 관찰하고, 특정 조건을 확인하거나 가능한 액션을 탐색합니다.

💻 **코드 예제: 페이지 관찰**

```typescript
import { Stagehand } from "@browserbasehq/stagehand";

const stagehand = new Stagehand({
    env: "LOCAL",
    modelName: "gpt-4o",
    modelClientOptions: { apiKey: process.env.OPENAI_API_KEY }
});

await stagehand.init();
await stagehand.page.goto("https://example.com");

// 1. 페이지 상태 확인
const observation = await stagehand.observe({
    instruction: "현재 페이지에서 사용자가 할 수 있는 모든 액션을 나열"
});

console.log("가능한 액션들:", observation);
// 예: ["More information 링크 클릭", "페이지 스크롤"]

// 2. 특정 요소 존재 확인
const elements = await stagehand.observe({
    instruction: "로그인 버튼이 있는지 확인"
});

if (elements.length > 0) {
    console.log("로그인 버튼 발견");
    await stagehand.act({ action: "로그인 버튼 클릭" });
}

// 3. 폼 필드 탐색
const formFields = await stagehand.observe({
    instruction: "이 페이지의 모든 입력 폼 필드를 식별"
});

console.log("폼 필드:", formFields);

// 4. 조건부 로직
const loginStatus = await stagehand.observe({
    instruction: "사용자가 현재 로그인되어 있는지 확인"
});

const isLoggedIn = loginStatus.some(obs =>
    obs.toLowerCase().includes("로그인됨") ||
    obs.toLowerCase().includes("logged in")
);

if (!isLoggedIn) {
    await stagehand.act({ action: "로그인 페이지로 이동" });
}

await stagehand.close();
```

**observe()와 act() 조합**:
```typescript
// 동적 네비게이션: 메뉴 항목을 찾아서 클릭
const menuItems = await stagehand.observe({
    instruction: "메인 네비게이션 메뉴의 모든 항목 나열"
});

// 원하는 항목 찾기
const targetItem = menuItems.find(item =>
    item.toLowerCase().includes("products")
);

if (targetItem) {
    await stagehand.act({ action: `${targetItem} 클릭` });
}
```

✅ **체크포인트**
- [ ] `observe()`로 페이지 상태를 파악할 수 있는가?
- [ ] 관찰 결과를 조건문에 활용할 수 있는가?
- [ ] `observe()` → `act()` 패턴으로 동적 자동화를 구현할 수 있는가?

⚠️ **흔한 실수**
- observe는 LLM 호출이므로 비용/시간 고려
- 반환값은 문자열 배열 (정확한 형식 보장 안 됨)
- 명확한 instruction 작성 중요

🔗 **더 알아보기**: [observe() API](https://docs.stagehand.dev/api/observe)

---

### 4.5 캐싱과 성능 최적화

📌 **핵심 개념**

Stagehand는 반복되는 액션을 캐싱하여 LLM 호출을 줄이고 속도를 높입니다.

💻 **코드 예제: 캐싱 활용**

```typescript
import { Stagehand } from "@browserbasehq/stagehand";

const stagehand = new Stagehand({
    env: "LOCAL",
    modelName: "gpt-4o",
    enableCaching: true,  // 캐싱 활성화
    modelClientOptions: { apiKey: process.env.OPENAI_API_KEY }
});

await stagehand.init();

// 첫 번째 실행: LLM 호출 발생
await stagehand.page.goto("https://example.com");
await stagehand.act({ action: "More information 링크 클릭" });
// → LLM이 요소를 찾고 선택자 결정

// 두 번째 실행: 캐시 사용 (LLM 호출 없음)
await stagehand.page.goto("https://example.com");
await stagehand.act({ action: "More information 링크 클릭" });
// → 캐시된 선택자로 즉시 클릭

await stagehand.close();
```

**성능 최적화 전략**:
```typescript
// 1. 정확한 요소는 Playwright 직접 사용
const page = stagehand.page;

// 빠른 조작: Playwright 직접
await page.fill("#email", "user@example.com");
await page.fill("#password", "password123");

// 동적 요소: Stagehand
await stagehand.act({ action: "로그인 버튼 클릭" });

// 2. 모델 선택 (비용 vs 정확도)
const costOptimized = new Stagehand({
    modelName: "gpt-4o-mini",  // 저렴하지만 덜 정확
    // ...
});

const accuracyOptimized = new Stagehand({
    modelName: "gpt-4o",  // 더 비싸지만 정확
    // ...
});

// 3. 배치 추출 (한 번의 호출로 여러 데이터)
const allData = await stagehand.extract({
    instruction: "상품명, 가격, 설명, 리뷰 수를 모두 추출",
    schema: z.object({
        name: z.string(),
        price: z.number(),
        description: z.string(),
        reviewCount: z.number()
    })
});
// 여러 번 extract() 호출보다 효율적
```

**디버그 모드**:
```typescript
const stagehand = new Stagehand({
    env: "LOCAL",
    verbose: 2,  // 최대 로깅
    modelName: "gpt-4o",
    modelClientOptions: { apiKey: process.env.OPENAI_API_KEY }
});

// 실행 시 상세 로그 출력
// - LLM 프롬프트/응답
// - 찾은 요소 정보
// - 캐시 히트/미스
```

✅ **체크포인트**
- [ ] 캐싱의 동작 방식을 이해하는가?
- [ ] Playwright와 Stagehand를 적절히 혼합할 수 있는가?
- [ ] verbose 로깅으로 디버깅할 수 있는가?

⚠️ **흔한 실수**
- 캐시는 동일한 instruction + 비슷한 페이지에서만 작동
- 페이지 구조가 크게 바뀌면 캐시 무효화
- `gpt-4o-mini`는 복잡한 페이지에서 정확도 저하

🔗 **더 알아보기**: [Performance](https://docs.stagehand.dev/performance)

---

### 4.6 Stagehand Agent (자율 에이전트)

📌 **핵심 개념**

Stagehand Agent는 고수준 목표를 받아 여러 단계를 자율적으로 수행하는 에이전트입니다.

💻 **코드 예제: Agent 사용**

```typescript
import { Stagehand } from "@browserbasehq/stagehand";

const stagehand = new Stagehand({
    env: "LOCAL",
    modelName: "gpt-4o",
    modelClientOptions: { apiKey: process.env.OPENAI_API_KEY }
});

await stagehand.init();

// Agent 모드 - 고수준 목표 설정
const agent = stagehand.agent({
    provider: "openai",
    model: "gpt-4o"
});

// 자율 실행
const result = await agent.execute({
    instruction: `
        1. https://news.ycombinator.com으로 이동
        2. 가장 인기 있는 기사 3개의 제목과 링크 추출
        3. 각 기사의 댓글 수 확인
        4. 결과를 JSON으로 반환
    `,
    maxSteps: 10  // 최대 단계 수
});

console.log("Agent 결과:", result);

await stagehand.close();
```

**Agent vs 수동 제어**:
```typescript
// 수동: 각 단계를 직접 제어
await stagehand.page.goto("https://shop.example.com");
await stagehand.act({ action: "검색창에 'laptop' 입력" });
await stagehand.act({ action: "검색 버튼 클릭" });
const products = await stagehand.extract({
    instruction: "상품 목록 추출",
    schema: ProductListSchema
});

// Agent: 목표만 제시
const agentResult = await agent.execute({
    instruction: "shop.example.com에서 laptop을 검색하고 상품 목록 가져오기",
    maxSteps: 5
});
// Agent가 알아서 네비게이션, 검색, 추출 수행
```

**Agent 제약 설정**:
```typescript
const agent = stagehand.agent({
    provider: "anthropic",
    model: "claude-sonnet-4-20250514",
    systemPrompt: `
        당신은 웹 자동화 에이전트입니다.
        - 절대로 결제하지 마세요
        - 개인정보를 입력하지 마세요
        - 불확실하면 멈추고 확인 요청
    `
});

const result = await agent.execute({
    instruction: "아마존에서 가장 저렴한 키보드 찾기",
    maxSteps: 15,
    onStep: (step) => {
        console.log(`Step ${step.number}: ${step.action}`);
        // 특정 조건에서 중단
        if (step.action.includes("결제")) {
            throw new Error("결제 시도 차단");
        }
    }
});
```

✅ **체크포인트**
- [ ] Agent와 수동 제어의 차이를 이해하는가?
- [ ] `maxSteps`로 실행 범위를 제한할 수 있는가?
- [ ] `onStep` 콜백으로 실행을 모니터링할 수 있는가?

⚠️ **흔한 실수**
- Agent는 예측 불가능할 수 있음 → 적절한 제약 필요
- `maxSteps` 너무 높으면 비용 증가
- 민감한 작업에는 수동 제어 권장

🔗 **더 알아보기**: [Stagehand Agent](https://docs.stagehand.dev/agent)

---

## Part 5: 실전 프로젝트

### 5.1 미니 프로젝트 아이디어

| 난이도 | 프로젝트 | 학습 포인트 |
|--------|---------|------------|
| 🟢 | Hacker News 스크래퍼 | extract() 기본 |
| 🟢 | 자동 폼 작성기 | act() 연습 |
| 🟡 | 경쟁사 가격 모니터링 | 복합 워크플로우 |
| 🟡 | 소셜 미디어 모니터링 | 로그인 + 데이터 추출 |
| 🔴 | E-commerce 가격 비교 에이전트 | Agent 활용 |

### 5.2 단계별 구현 가이드: 뉴스 수집기

**목표**: 여러 뉴스 사이트에서 헤드라인을 자동 수집

```typescript
// news-collector.ts
import { Stagehand } from "@browserbasehq/stagehand";
import { z } from "zod";

const NewsSchema = z.object({
    articles: z.array(z.object({
        title: z.string().describe("기사 제목"),
        summary: z.string().optional().describe("요약 (있으면)"),
        source: z.string().describe("출처")
    }))
});

interface NewsSource {
    name: string;
    url: string;
    instruction: string;
}

const sources: NewsSource[] = [
    {
        name: "Hacker News",
        url: "https://news.ycombinator.com",
        instruction: "상위 5개 기사의 제목 추출"
    },
    {
        name: "TechCrunch",
        url: "https://techcrunch.com",
        instruction: "메인 헤드라인 5개 추출"
    }
];

async function collectNews() {
    const stagehand = new Stagehand({
        env: "LOCAL",
        headless: true,
        modelName: "gpt-4o",
        modelClientOptions: {
            apiKey: process.env.OPENAI_API_KEY,
        }
    });

    await stagehand.init();
    const page = stagehand.page;
    const allNews: any[] = [];

    for (const source of sources) {
        console.log(`\n📰 ${source.name} 수집 중...`);

        try {
            await page.goto(source.url, { waitUntil: "networkidle" });

            const result = await stagehand.extract({
                instruction: source.instruction,
                schema: NewsSchema
            });

            const articlesWithSource = result.articles.map(article => ({
                ...article,
                source: source.name,
                collectedAt: new Date().toISOString()
            }));

            allNews.push(...articlesWithSource);
            console.log(`✅ ${result.articles.length}개 기사 수집`);

        } catch (error) {
            console.error(`❌ ${source.name} 실패:`, error);
        }

        // 요청 간 딜레이
        await new Promise(r => setTimeout(r, 2000));
    }

    await stagehand.close();

    // 결과 출력
    console.log("\n📋 수집 결과:");
    console.log(JSON.stringify(allNews, null, 2));

    return allNews;
}

// 실행
collectNews().catch(console.error);
```

### 5.3 Best Practices

**프로젝트 구조**:
```
stagehand-project/
├── src/
│   ├── index.ts
│   ├── config.ts
│   ├── schemas/
│   │   └── news.ts
│   └── collectors/
│       ├── base.ts
│       └── hackernews.ts
├── tests/
│   └── collectors.test.ts
├── package.json
└── tsconfig.json
```

**설계 패턴**:
```typescript
// 1. Playwright 우선, Stagehand는 보조
class WebAutomation {
    constructor(private stagehand: Stagehand) {}

    async login(email: string, password: string) {
        const page = this.stagehand.page;

        // 정적 요소: Playwright
        await page.fill("#email", email);
        await page.fill("#password", password);

        // 동적 요소 (CAPTCHA, 동의 팝업 등): Stagehand
        await this.stagehand.act({
            action: "로그인 버튼 클릭 (있다면 쿠키 동의 팝업 먼저 닫기)"
        });
    }
}

// 2. 에러 복구
async function robustAction(stagehand: Stagehand, action: string, maxRetries = 3) {
    for (let i = 0; i < maxRetries; i++) {
        const result = await stagehand.act({ action });
        if (result.success) return result;

        console.log(`Retry ${i + 1}/${maxRetries}...`);
        await new Promise(r => setTimeout(r, 1000));
    }
    throw new Error(`Action failed after ${maxRetries} attempts: ${action}`);
}

// 3. 비용 모니터링
let tokenCount = 0;

stagehand.on("llmCall", (data) => {
    tokenCount += data.tokens;
    console.log(`LLM 호출: ${data.tokens} 토큰 (총 ${tokenCount})`);
});
```

**운영 권장사항**:

1. **혼합 사용**: 정적 요소는 Playwright, 동적 요소는 Stagehand
2. **캐싱 활용**: 반복 작업에서 비용 절감
3. **에러 처리**: 재시도 로직 구현
4. **로깅**: 모든 액션과 결과 기록
5. **비용 관리**: 토큰 사용량 모니터링

---

## 요약

Stagehand는 AI 기반 웹 자동화의 새로운 패러다임을 제시합니다:

- **핵심 API**: `act()` (액션), `extract()` (추출), `observe()` (관찰)
- **하이브리드**: Playwright 정확성 + AI 유연성
- **자가 치유**: 페이지 변경에도 자동 적응
- **비용 절감**: 캐싱으로 반복 LLM 호출 방지

다음 단계:
1. [Stagehand Quickstart](https://docs.stagehand.dev/quickstart) 따라하기
2. 간단한 스크래핑 프로젝트 구현
3. Playwright 코드와 점진적 통합
