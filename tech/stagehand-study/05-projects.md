---
date: 2026-02-02
tags:
  - tech
  - stagehand
  - projects
  - practice
parent: "[[README]]"
---

# Stagehand - 실전 프로젝트

> [[04-learning/06-agent|이전: Agent]] | [[README|목차]] | [[cheatsheet|다음: 치트시트]]

---

## 1. 프로젝트 아이디어

### 난이도별 분류

| 난이도 | 프로젝트 | 학습 포인트 |
|--------|----------|------------|
| 초급 | 뉴스 헤드라인 수집 | extract() 기초 |
| 초급 | 로그인 자동화 | act() 기초 |
| 중급 | 가격 모니터링 | 페이지네이션, 스케줄링 |
| 중급 | 양식 자동 작성 | 복잡한 폼 처리 |
| 고급 | 멀티사이트 비교 | 병렬 처리, 캐싱 |
| 고급 | AI 리서치 어시스턴트 | Agent 활용 |

---

## 2. 초급 프로젝트

### 2.1 뉴스 헤드라인 수집기

**목표**: Hacker News에서 상위 뉴스 제목과 점수 수집

```typescript
// src/projects/news-collector.ts
import { Stagehand } from "@browserbasehq/stagehand";
import { z } from "zod";
import "dotenv/config";

const NewsSchema = z.object({
  articles: z.array(z.object({
    rank: z.number().describe("순위"),
    title: z.string().describe("제목"),
    url: z.string().optional().describe("링크"),
    score: z.number().optional().describe("점수"),
    comments: z.number().optional().describe("댓글 수")
  }))
});

async function collectNews() {
  const stagehand = new Stagehand({
    env: "LOCAL",
    modelName: "gpt-4o",
    modelClientOptions: { apiKey: process.env.OPENAI_API_KEY },
    enableCaching: true,
    headless: false
  });

  try {
    await stagehand.init();
    await stagehand.page.goto("https://news.ycombinator.com");

    const result = await stagehand.extract({
      instruction: "상위 10개 뉴스의 순위, 제목, 점수, 댓글 수를 추출해줘",
      schema: NewsSchema
    });

    console.log("=== Hacker News Top 10 ===");
    result.articles.forEach(article => {
      console.log(`${article.rank}. ${article.title}`);
      console.log(`   점수: ${article.score}, 댓글: ${article.comments}`);
    });

    return result;
  } finally {
    await stagehand.close();
  }
}

collectNews();
```

### 2.2 간단한 로그인 자동화

**목표**: 웹사이트 로그인 프로세스 자동화

```typescript
// src/projects/auto-login.ts
import { Stagehand } from "@browserbasehq/stagehand";
import "dotenv/config";

interface Credentials {
  email: string;
  password: string;
}

async function autoLogin(url: string, credentials: Credentials) {
  const stagehand = new Stagehand({
    env: "LOCAL",
    modelName: "gpt-4o",
    modelClientOptions: { apiKey: process.env.OPENAI_API_KEY },
    headless: false
  });

  try {
    await stagehand.init();
    await stagehand.page.goto(url);

    // 이메일 입력
    await stagehand.act({
      action: "이메일 또는 사용자명 입력 필드에 {{email}} 입력",
      variables: { email: credentials.email }
    });

    // 비밀번호 입력
    await stagehand.act({
      action: "비밀번호 입력 필드에 {{password}} 입력",
      variables: { password: credentials.password }
    });

    // 로그인 버튼 클릭
    await stagehand.act({ action: "로그인 또는 Sign In 버튼 클릭" });

    // 로그인 성공 확인
    await stagehand.page.waitForLoadState("networkidle");

    console.log("로그인 성공!");
    console.log("현재 URL:", await stagehand.page.url());

  } catch (error) {
    console.error("로그인 실패:", error);
  } finally {
    await stagehand.close();
  }
}

// 사용 예시
autoLogin("https://example.com/login", {
  email: "user@example.com",
  password: "your-password"
});
```

---

## 3. 중급 프로젝트

### 3.1 상품 가격 모니터링

**목표**: 여러 상품의 가격을 주기적으로 확인하고 변동 알림

```typescript
// src/projects/price-monitor.ts
import { Stagehand } from "@browserbasehq/stagehand";
import { z } from "zod";
import * as fs from "fs";
import "dotenv/config";

const ProductSchema = z.object({
  name: z.string().describe("상품명"),
  price: z.number().describe("현재 가격 (숫자만)"),
  originalPrice: z.number().optional().describe("원가"),
  available: z.boolean().describe("구매 가능 여부")
});

interface PriceRecord {
  url: string;
  name: string;
  price: number;
  timestamp: string;
}

class PriceMonitor {
  private stagehand: Stagehand | null = null;
  private history: PriceRecord[] = [];
  private historyFile = "price-history.json";

  async init() {
    this.stagehand = new Stagehand({
      env: "LOCAL",
      modelName: "gpt-4o",
      modelClientOptions: { apiKey: process.env.OPENAI_API_KEY },
      enableCaching: true,
      headless: true
    });
    await this.stagehand.init();

    // 기존 기록 로드
    if (fs.existsSync(this.historyFile)) {
      this.history = JSON.parse(fs.readFileSync(this.historyFile, "utf-8"));
    }
  }

  async checkPrice(url: string): Promise<PriceRecord | null> {
    if (!this.stagehand) throw new Error("초기화 필요");

    try {
      await this.stagehand.page.goto(url);
      await this.stagehand.page.waitForLoadState("networkidle");

      const result = await this.stagehand.extract({
        instruction: "이 상품의 이름, 현재 가격, 원가, 구매 가능 여부를 추출해줘",
        schema: ProductSchema
      });

      const record: PriceRecord = {
        url,
        name: result.name,
        price: result.price,
        timestamp: new Date().toISOString()
      };

      // 가격 변동 확인
      const lastPrice = this.getLastPrice(url);
      if (lastPrice !== null && lastPrice !== result.price) {
        const change = result.price - lastPrice;
        const emoji = change < 0 ? "⬇️" : "⬆️";
        console.log(`${emoji} 가격 변동: ${result.name}`);
        console.log(`   ${lastPrice} → ${result.price} (${change > 0 ? "+" : ""}${change})`);
      }

      // 기록 저장
      this.history.push(record);
      this.saveHistory();

      return record;
    } catch (error) {
      console.error(`가격 확인 실패: ${url}`, error);
      return null;
    }
  }

  private getLastPrice(url: string): number | null {
    const records = this.history.filter(r => r.url === url);
    return records.length > 0 ? records[records.length - 1].price : null;
  }

  private saveHistory() {
    fs.writeFileSync(this.historyFile, JSON.stringify(this.history, null, 2));
  }

  async close() {
    if (this.stagehand) {
      await this.stagehand.close();
    }
  }
}

// 사용 예시
async function main() {
  const monitor = new PriceMonitor();
  await monitor.init();

  const urls = [
    "https://www.example.com/product/1",
    "https://www.example.com/product/2"
  ];

  for (const url of urls) {
    const result = await monitor.checkPrice(url);
    if (result) {
      console.log(`${result.name}: ${result.price}원`);
    }
  }

  await monitor.close();
}

main();
```

### 3.2 양식 자동 작성기

**목표**: 복잡한 웹 양식을 데이터 기반으로 자동 작성

```typescript
// src/projects/form-filler.ts
import { Stagehand } from "@browserbasehq/stagehand";
import "dotenv/config";

interface FormData {
  [key: string]: string | boolean | number;
}

class FormFiller {
  private stagehand: Stagehand;

  constructor() {
    this.stagehand = new Stagehand({
      env: "LOCAL",
      modelName: "gpt-4o",
      modelClientOptions: { apiKey: process.env.OPENAI_API_KEY },
      headless: false,
      verbose: 1
    });
  }

  async init() {
    await this.stagehand.init();
  }

  async fillForm(url: string, data: FormData) {
    await this.stagehand.page.goto(url);
    await this.stagehand.page.waitForLoadState("networkidle");

    // 가능한 입력 필드 확인
    const fields = await this.stagehand.observe({
      instruction: "모든 입력 가능한 필드 (텍스트, 드롭다운, 체크박스 등)"
    });

    console.log("발견된 필드:", fields.length);

    // 각 필드 작성
    for (const [key, value] of Object.entries(data)) {
      try {
        if (typeof value === "boolean") {
          // 체크박스
          await this.stagehand.act({
            action: value
              ? `'${key}' 체크박스 선택`
              : `'${key}' 체크박스 선택 해제`
          });
        } else {
          // 텍스트 또는 선택
          await this.stagehand.act({
            action: `'${key}' 필드에 '${value}' 입력 또는 선택`,
          });
        }
        console.log(`  ${key}: ${value}`);
      } catch (error) {
        console.log(`  ${key}: 입력 실패 - ${error}`);
      }
    }

    // 스크린샷 저장
    await this.stagehand.page.screenshot({ path: "form-filled.png" });
    console.log("양식 작성 완료");
  }

  async submit() {
    await this.stagehand.act({ action: "제출 또는 Submit 버튼 클릭" });
  }

  async close() {
    await this.stagehand.close();
  }
}

// 사용 예시
async function main() {
  const filler = new FormFiller();
  await filler.init();

  await filler.fillForm("https://example.com/apply", {
    "이름": "홍길동",
    "이메일": "hong@example.com",
    "전화번호": "010-1234-5678",
    "생년월일": "1990-01-15",
    "성별": "남성",
    "직업": "개발자",
    "이용약관 동의": true,
    "마케팅 수신": false
  });

  // await filler.submit();  // 실제 제출 원할 경우
  await filler.close();
}

main();
```

---

## 4. 고급 프로젝트

### 4.1 멀티사이트 가격 비교

**목표**: 여러 쇼핑몰에서 동일 상품 가격 비교

```typescript
// src/projects/price-compare.ts
import { Stagehand } from "@browserbasehq/stagehand";
import { z } from "zod";
import "dotenv/config";

const PriceSchema = z.object({
  productName: z.string().describe("상품명"),
  price: z.number().describe("가격"),
  shipping: z.string().optional().describe("배송비 정보"),
  seller: z.string().optional().describe("판매자")
});

interface CompareResult {
  site: string;
  productName: string;
  price: number;
  shipping?: string;
  url: string;
}

class PriceComparer {
  private sites = [
    {
      name: "쿠팡",
      searchUrl: "https://www.coupang.com/np/search?q=",
      searchAction: "검색 결과 첫 번째 상품 클릭"
    },
    {
      name: "11번가",
      searchUrl: "https://search.11st.co.kr/Search.tmall?kwd=",
      searchAction: "첫 번째 검색 결과 상품 클릭"
    }
  ];

  async compare(productName: string): Promise<CompareResult[]> {
    const results: CompareResult[] = [];

    for (const site of this.sites) {
      const stagehand = new Stagehand({
        env: "LOCAL",
        modelName: "gpt-4o",
        modelClientOptions: { apiKey: process.env.OPENAI_API_KEY },
        enableCaching: true,
        headless: true
      });

      try {
        await stagehand.init();
        const searchUrl = `${site.searchUrl}${encodeURIComponent(productName)}`;
        await stagehand.page.goto(searchUrl);
        await stagehand.page.waitForLoadState("networkidle");

        // 첫 번째 상품 클릭
        await stagehand.act({ action: site.searchAction });
        await stagehand.page.waitForLoadState("networkidle");

        // 가격 추출
        const data = await stagehand.extract({
          instruction: "상품명, 가격, 배송비 정보를 추출해줘",
          schema: PriceSchema
        });

        results.push({
          site: site.name,
          productName: data.productName,
          price: data.price,
          shipping: data.shipping,
          url: await stagehand.page.url()
        });

      } catch (error) {
        console.error(`${site.name} 검색 실패:`, error);
      } finally {
        await stagehand.close();
      }
    }

    // 가격순 정렬
    results.sort((a, b) => a.price - b.price);

    return results;
  }

  printResults(results: CompareResult[]) {
    console.log("\n=== 가격 비교 결과 ===\n");
    results.forEach((r, i) => {
      const badge = i === 0 ? " [최저가]" : "";
      console.log(`${i + 1}. ${r.site}${badge}`);
      console.log(`   상품: ${r.productName}`);
      console.log(`   가격: ${r.price.toLocaleString()}원`);
      if (r.shipping) console.log(`   배송: ${r.shipping}`);
      console.log(`   링크: ${r.url}\n`);
    });
  }
}

// 사용
async function main() {
  const comparer = new PriceComparer();
  const results = await comparer.compare("에어팟 프로 2");
  comparer.printResults(results);
}

main();
```

### 4.2 AI 리서치 어시스턴트

**목표**: Agent를 활용한 자동 정보 수집 및 요약

```typescript
// src/projects/research-assistant.ts
import { Stagehand } from "@browserbasehq/stagehand";
import "dotenv/config";

interface ResearchConfig {
  topic: string;
  sources: string[];
  maxPagesPerSource: number;
}

class ResearchAssistant {
  private stagehand!: Stagehand;

  async init() {
    this.stagehand = new Stagehand({
      env: "LOCAL",
      modelName: "gpt-4o",
      modelClientOptions: { apiKey: process.env.OPENAI_API_KEY },
      headless: false,
      verbose: 1
    });
    await this.stagehand.init();
  }

  async research(config: ResearchConfig): Promise<string> {
    const agent = this.stagehand.agent({
      provider: "openai",
      model: "computer-use-preview",
      instructions: `
        당신은 리서치 어시스턴트입니다.
        - 신뢰할 수 있는 정보만 수집하세요
        - 출처를 명확히 기록하세요
        - 핵심 내용 위주로 요약하세요
        - 최신 정보를 우선하세요
      `,
      maxSteps: 30
    });

    const result = await agent.execute(`
      "${config.topic}"에 대해 조사해주세요.

      조사할 사이트:
      ${config.sources.map(s => `- ${s}`).join("\n")}

      각 사이트에서 최대 ${config.maxPagesPerSource}개 페이지를 확인하고:
      1. 핵심 개념 정리
      2. 최신 동향
      3. 주요 사용 사례
      4. 장단점

      마지막에 종합 요약을 제공해주세요.
    `);

    return result;
  }

  async close() {
    await this.stagehand.close();
  }
}

// 사용
async function main() {
  const assistant = new ResearchAssistant();
  await assistant.init();

  const report = await assistant.research({
    topic: "Stagehand AI 브라우저 자동화",
    sources: [
      "https://docs.stagehand.dev",
      "https://github.com/browserbase/stagehand"
    ],
    maxPagesPerSource: 3
  });

  console.log("\n=== 리서치 결과 ===\n");
  console.log(report);

  await assistant.close();
}

main();
```

---

## 5. Best Practices

### 프로젝트 구조

```
my-stagehand-project/
├── src/
│   ├── index.ts
│   ├── stagehand.ts      ← Stagehand 래퍼
│   ├── schemas/          ← Zod 스키마
│   ├── projects/         ← 프로젝트별 스크립트
│   └── utils/            ← 유틸리티
├── data/                 ← 수집된 데이터
├── screenshots/          ← 디버깅용 스크린샷
├── .env
└── package.json
```

### 에러 처리

```typescript
async function safeExecute<T>(
  fn: () => Promise<T>,
  fallback: T,
  retries = 3
): Promise<T> {
  for (let i = 0; i < retries; i++) {
    try {
      return await fn();
    } catch (error) {
      console.log(`시도 ${i + 1}/${retries} 실패`);
      if (i === retries - 1) {
        console.error("최종 실패:", error);
        return fallback;
      }
      await new Promise(r => setTimeout(r, 1000 * (i + 1)));
    }
  }
  return fallback;
}
```

### 로깅

```typescript
function log(level: "info" | "warn" | "error", message: string, data?: any) {
  const timestamp = new Date().toISOString();
  const prefix = { info: "INFO", warn: "WARN", error: "ERROR" }[level];
  console.log(`[${timestamp}] [${prefix}] ${message}`);
  if (data) console.log(JSON.stringify(data, null, 2));
}
```

---

## 다음 단계

> [!tip] 다음으로
> 프로젝트 아이디어를 얻었다면 [[cheatsheet|치트시트]]에서 빠른 참조를 확인하세요.

---

## References

- [Stagehand Examples](https://github.com/browserbase/stagehand/tree/main/examples)
- [Stagehand 공식 문서](https://docs.stagehand.dev)
