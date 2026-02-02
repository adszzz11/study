---
date: 2026-02-02
tags:
  - tech
  - stagehand
  - setup
parent: "[[README]]"
---

# Stagehand - 초기 설정

> [[03-references|이전: 참고자료]] | [[README|목차]] | [[02-act|다음: act()]]

---

## 1. 사전 요구사항

### 필수 환경

| 요구사항 | 버전 | 확인 방법 |
|----------|------|----------|
| Node.js | 18 이상 | `node --version` |
| npm 또는 pnpm | 최신 | `npm --version` |
| TypeScript | 5.0+ | 프로젝트 설정 |

### LLM API 키

Stagehand는 LLM을 사용하므로 API 키가 필요합니다.

| 제공자 | 환경 변수 | 발급 |
|--------|----------|------|
| OpenAI | `OPENAI_API_KEY` | [platform.openai.com](https://platform.openai.com) |
| Anthropic | `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com) |

---

## 2. 프로젝트 초기화

### 새 프로젝트 생성

```bash
# 프로젝트 폴더 생성
mkdir my-stagehand-project
cd my-stagehand-project

# npm 초기화
npm init -y

# TypeScript 설정
npm install typescript ts-node @types/node -D
npx tsc --init
```

### Stagehand 설치

```bash
npm install @browserbasehq/stagehand
```

### 추가 의존성

```bash
# Zod (스키마 검증용)
npm install zod

# 환경 변수 관리 (선택)
npm install dotenv
```

---

## 3. 프로젝트 구조

### 권장 폴더 구조

```
my-stagehand-project/
├── src/
│   ├── index.ts          ← 메인 진입점
│   ├── scripts/          ← 자동화 스크립트들
│   │   ├── scrape.ts
│   │   └── login.ts
│   └── schemas/          ← Zod 스키마 정의
│       └── product.ts
├── .env                  ← API 키 (gitignore!)
├── .gitignore
├── package.json
└── tsconfig.json
```

### tsconfig.json 설정

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "./dist"
  },
  "include": ["src/**/*"]
}
```

### .env 파일

```bash
# .env
OPENAI_API_KEY=sk-your-openai-api-key
# 또는
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key

# Browserbase 사용 시 (선택)
BROWSERBASE_API_KEY=your-browserbase-key
BROWSERBASE_PROJECT_ID=your-project-id
```

### .gitignore

```
node_modules/
dist/
.env
.env.local
```

---

## 4. 기본 설정 옵션

### Stagehand 인스턴스 생성

```typescript
import { Stagehand } from "@browserbasehq/stagehand";

// 기본 설정 (로컬 브라우저)
const stagehand = new Stagehand();

// 상세 설정
const stagehand = new Stagehand({
  env: "LOCAL",                    // LOCAL 또는 BROWSERBASE
  modelName: "gpt-4o",             // 사용할 LLM 모델
  modelClientOptions: {
    apiKey: process.env.OPENAI_API_KEY
  },
  enableCaching: true,             // 캐싱 활성화
  verbose: 1,                      // 로그 레벨 (0: 없음, 1: 기본, 2: 상세)
  headless: false                  // 브라우저 표시 여부
});
```

### 주요 설정 옵션

| 옵션 | 타입 | 기본값 | 설명 |
|------|------|--------|------|
| `env` | `"LOCAL" \| "BROWSERBASE"` | `"LOCAL"` | 실행 환경 |
| `modelName` | string | - | LLM 모델명 |
| `enableCaching` | boolean | `false` | DOM 캐싱 |
| `headless` | boolean | `false` | 헤드리스 모드 |
| `verbose` | 0 \| 1 \| 2 | 0 | 로그 레벨 |

---

## 5. Hello World

### 첫 번째 스크립트

**src/index.ts**
```typescript
import { Stagehand } from "@browserbasehq/stagehand";
import { z } from "zod";
import "dotenv/config";

async function main() {
  // 1. Stagehand 인스턴스 생성
  const stagehand = new Stagehand({
    env: "LOCAL",
    modelName: "gpt-4o",
    modelClientOptions: {
      apiKey: process.env.OPENAI_API_KEY,
    },
    headless: false,
    verbose: 1,
  });

  try {
    // 2. 초기화
    await stagehand.init();
    console.log("Stagehand 초기화 완료!");

    // 3. 페이지 이동
    await stagehand.page.goto("https://news.ycombinator.com");
    console.log("페이지 로드 완료!");

    // 4. 데이터 추출
    const result = await stagehand.extract({
      instruction: "상위 3개 게시물의 제목을 추출해줘",
      schema: z.object({
        titles: z.array(z.string()).describe("게시물 제목들"),
      }),
    });

    console.log("추출된 제목:", result.titles);

  } catch (error) {
    console.error("오류 발생:", error);
  } finally {
    // 5. 정리
    await stagehand.close();
    console.log("브라우저 종료!");
  }
}

main();
```

### 실행

```bash
# ts-node로 직접 실행
npx ts-node src/index.ts

# 또는 컴파일 후 실행
npx tsc
node dist/index.js
```

### 예상 출력

```
Stagehand 초기화 완료!
페이지 로드 완료!
추출된 제목: [
  "Show HN: I built an AI-powered...",
  "The future of programming...",
  "Why Rust is taking over..."
]
브라우저 종료!
```

---

## 6. 개발 환경 팁

### VS Code 설정

```json
// .vscode/settings.json
{
  "typescript.preferences.importModuleSpecifier": "relative",
  "editor.formatOnSave": true
}
```

### 디버깅 설정

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Run Stagehand",
      "program": "${workspaceFolder}/src/index.ts",
      "runtimeExecutable": "npx",
      "runtimeArgs": ["ts-node"],
      "env": {
        "OPENAI_API_KEY": "${env:OPENAI_API_KEY}"
      }
    }
  ]
}
```

### package.json scripts

```json
{
  "scripts": {
    "start": "ts-node src/index.ts",
    "dev": "ts-node-dev --respawn src/index.ts",
    "build": "tsc",
    "scrape": "ts-node src/scripts/scrape.ts"
  }
}
```

---

## 7. 체크리스트

### 설치 확인

- [ ] Node.js 18+ 설치됨
- [ ] Stagehand 패키지 설치됨
- [ ] Zod 설치됨
- [ ] TypeScript 설정 완료

### 환경 설정 확인

- [ ] API 키 발급 완료
- [ ] .env 파일 생성
- [ ] .gitignore에 .env 추가

### 실행 확인

- [ ] Hello World 스크립트 작성
- [ ] 실행 시 브라우저 열림
- [ ] 데이터 추출 성공
- [ ] 오류 없이 종료

---

## 다음 단계

> [!tip] 다음으로
> 환경 설정이 완료되었다면 [[02-act|act()]]에서 자연어 액션을 배워보세요.

---

## References

- [Stagehand 공식 문서 - Getting Started](https://docs.stagehand.dev)
- [npm 패키지](https://www.npmjs.com/package/@browserbasehq/stagehand)
