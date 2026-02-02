# Browserless 심층 스터디 가이드

> **한 줄 정의**: 헤드리스 브라우저를 관리형 서비스로 제공하여 스크래핑, 자동화, PDF 생성 등을 인프라 걱정 없이 실행할 수 있게 해주는 플랫폼

---

## Part 1: 개요

### 1.1 정의 및 핵심 개념

**3줄 요약**:
1. Puppeteer, Playwright, Selenium 코드를 클라우드 브라우저에서 실행 - 인프라 관리 불필요
2. REST API로 스크린샷, PDF 생성, 웹 스크래핑을 간단한 HTTP 요청으로 처리
3. 안티봇 우회, CAPTCHA 해결, 세션 유지 등 고급 기능 제공

**핵심 키워드**: `#헤드리스브라우저` `#웹스크래핑` `#BaaS` `#자동화인프라` `#Puppeteer`

**Browserless가 해결하는 문제**:

```
Before Browserless:
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  스크래핑 코드   │ ──▶ │  Chrome 설치    │ ──▶ │  서버 관리      │
│  (Puppeteer)    │     │  메모리 관리    │     │  스케일링 문제  │
└─────────────────┘     └─────────────────┘     └─────────────────┘

After Browserless:
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  스크래핑 코드   │ ──▶ │   API 호출      │ ──▶ │  결과 수신      │
│  (Puppeteer)    │     │   (HTTP/WS)     │     │  (JSON/PDF 등)  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### 1.2 Quick Start (30초 체험)

**REST API로 스크린샷 생성**:
```bash
# cURL로 스크린샷 API 호출
curl -X POST "https://production-sfo.browserless.io/screenshot?token=YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "options": {
      "fullPage": true,
      "type": "png"
    }
  }' \
  --output screenshot.png
```

**Puppeteer로 연결**:
```javascript
const puppeteer = require('puppeteer');

(async () => {
    // Browserless에 연결 (로컬 Chrome 대신)
    const browser = await puppeteer.connect({
        browserWSEndpoint: 'wss://production-sfo.browserless.io?token=YOUR_TOKEN'
    });

    const page = await browser.newPage();
    await page.goto('https://example.com');
    await page.screenshot({ path: 'screenshot.png' });

    await browser.close();
})();
```

**Docker로 Self-hosted 실행**:
```bash
# 로컬에서 Browserless 실행
docker run -p 3000:3000 ghcr.io/browserless/chromium

# http://localhost:3000/docs 에서 문서 확인
```

### 1.3 왜 Browserless인가?

**장점**:
- **인프라 제로**: Chrome 설치, 메모리 관리, 스케일링 불필요
- **간단한 API**: REST API로 스크린샷, PDF, 스크래핑 즉시 가능
- **Puppeteer/Playwright 호환**: 기존 코드 거의 그대로 사용
- **안티봇 우회**: BrowserQL, Stealth 모드로 차단 회피
- **Self-hosted 가능**: Docker로 자체 서버 운영 가능 (무료)
- **세션 유지**: 쿠키, localStorage 90일까지 보관

**단점**:
- 클라우드 사용 시 비용 발생
- 네트워크 지연 (로컬 실행 대비)
- 복잡한 인터랙션은 직접 코드 작성 필요

**주요 사용 사례**:
- 대규모 웹 스크래핑
- 동적 웹페이지 PDF 생성
- E2E 테스트 (CI/CD)
- SEO 크롤링
- 소셜 미디어 자동화

---

## Part 2: 생태계 파악

### 2.1 관련 기술/용어 맵

```
┌─────────────────────────────────────────────────────────────┐
│                    Browserless 생태계                        │
├─────────────────────────────────────────────────────────────┤
│  [연결 방식]                                                 │
│  ├── WebSocket: Puppeteer/Playwright 연결                   │
│  ├── REST API: 스크린샷, PDF, 스크래핑 등                    │
│  └── BrowserQL: GraphQL 기반 브라우저 제어 (Stealth)         │
│                                                              │
│  [REST API 엔드포인트]                                       │
│  ├── /screenshot: 스크린샷 생성                              │
│  ├── /pdf: PDF 생성                                          │
│  ├── /scrape: 콘텐츠 스크래핑                                │
│  ├── /content: HTML 가져오기                                 │
│  ├── /function: 커스텀 함수 실행                             │
│  └── /unblock: 안티봇 우회                                   │
│                                                              │
│  [고급 기능]                                                 │
│  ├── Stealth Mode: 봇 탐지 회피                              │
│  ├── Persistent Sessions: 세션 유지 (90일)                   │
│  ├── Session Replay: 실행 녹화/디버깅                        │
│  ├── CAPTCHA Solving: 자동 캡차 해결                         │
│  └── Residential Proxies: IP 로테이션                        │
│                                                              │
│  [배포 옵션]                                                 │
│  ├── Cloud (SaaS): production-sfo.browserless.io             │
│  ├── Self-hosted: Docker 컨테이너                            │
│  └── Enterprise: 전용 인프라                                 │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 함께 자주 쓰이는 기술 스택

| 영역 | 기술 | 용도 |
|------|------|------|
| **브라우저 자동화** | Puppeteer, Playwright | 클라이언트 라이브러리 |
| **스케줄링** | Prefect, Airflow | 정기 스크래핑 작업 |
| **데이터 저장** | PostgreSQL, MongoDB | 스크래핑 결과 저장 |
| **큐** | Redis, RabbitMQ | 작업 큐 관리 |
| **프록시** | Residential Proxies | IP 차단 회피 |

### 2.3 경쟁/대안 기술 비교

| 기준 | Browserless | BrowserCat | Apify | ScrapingBee |
|------|-------------|------------|-------|-------------|
| **접근 방식** | WebSocket + REST | WebSocket | Actor 기반 | REST API |
| **Self-hosted** | 가능 (무료) | 불가 | 불가 | 불가 |
| **Puppeteer 호환** | 완벽 | 완벽 | 부분적 | 없음 |
| **안티봇** | BrowserQL | 기본 | 고급 | 기본 |
| **가격** | 사용량 기반 | 사용량 기반 | Actor별 | 요청 기반 |
| **오픈소스** | 부분 | 없음 | 부분 | 없음 |

**선택 가이드**:
- **Browserless**: Puppeteer/Playwright 사용자, Self-hosted 필요
- **Apify**: 미리 만들어진 스크레이퍼 필요, 복잡한 워크플로우
- **ScrapingBee**: 단순 HTTP 요청 기반 스크래핑
- **BrowserCat**: 저렴한 클라우드 브라우저

### 2.4 최신 트렌드 및 동향 (2025)

- **BrowserQL 강화**: GraphQL로 브라우저 제어, Stealth 모드 통합
- **Hybrid Automations**: 라이브 브라우저 세션 스트리밍
- **Persistent Sessions**: 쿠키/캐시 90일 보관
- **AI 통합**: LangChain, LlamaIndex 등 AI 프레임워크와 연동
- **Chrome Extensions 지원**: 클라우드에서 확장 프로그램 실행

---

## Part 3: 레퍼런스

### 3.1 공식 문서 및 필수 링크

| 리소스 | URL | 설명 |
|--------|-----|------|
| 🟢 공식 문서 | [docs.browserless.io](https://docs.browserless.io/) | 메인 문서 |
| 🟢 GitHub | [github.com/browserless/browserless](https://github.com/browserless/browserless) | 오픈소스 코드 |
| 🟢 대시보드 | [browserless.io](https://www.browserless.io/) | 계정 관리 |
| 🟡 REST API 문서 | [docs.browserless.io/rest-apis](https://docs.browserless.io/rest-apis/intro) | API 레퍼런스 |

### 3.2 추천 학습 자료

**🟢 입문**:
- [Browserless Quickstart](https://docs.browserless.io/start) - 시작 가이드
- [REST APIs Overview](https://docs.browserless.io/rest-apis/intro) - API 개요

**🟡 중급**:
- [BrowserQL Guide](https://docs.browserless.io/browserql) - 고급 브라우저 제어
- [Stealth Mode](https://docs.browserless.io/stealth-mode) - 안티봇 우회

**🔴 고급**:
- [Self-hosting Guide](https://docs.browserless.io/docker/quickstart) - Docker 설정
- [Enterprise Features](https://docs.browserless.io/enterprise) - 엔터프라이즈 기능

### 3.3 커뮤니티 및 질문할 곳

- **GitHub Issues**: [browserless/browserless/issues](https://github.com/browserless/browserless/issues)
- **Discord**: Browserless 공식 커뮤니티
- **Stack Overflow**: `[browserless]` 태그

### 3.4 실무 예제/오픈소스 프로젝트

- [Browserless Examples](https://github.com/browserless/browserless/tree/main/examples)
- [LangChain Browserless Integration](https://python.langchain.com/docs/integrations/document_loaders/browserless/)

---

## Part 4: 상세 학습 로드맵

### 4.1 REST API 기본 사용

📌 **핵심 개념**

Browserless REST API는 HTTP 요청만으로 브라우저 작업을 수행합니다. 별도 라이브러리 없이 cURL이나 fetch로 사용 가능합니다.

💻 **코드 예제: 스크린샷 API**

```javascript
// Node.js fetch 예제
const fetch = require('node-fetch');
const fs = require('fs');

async function takeScreenshot(url) {
    const response = await fetch(
        'https://production-sfo.browserless.io/screenshot?token=YOUR_TOKEN',
        {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                url: url,
                options: {
                    fullPage: true,
                    type: 'png'
                },
                // 뷰포트 설정
                viewport: {
                    width: 1920,
                    height: 1080
                },
                // 페이지 로드 대기
                waitForTimeout: 3000
            })
        }
    );

    const buffer = await response.buffer();
    fs.writeFileSync('screenshot.png', buffer);
    console.log('Screenshot saved!');
}

takeScreenshot('https://example.com');
```

**PDF 생성**:
```javascript
async function generatePDF(url) {
    const response = await fetch(
        'https://production-sfo.browserless.io/pdf?token=YOUR_TOKEN',
        {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                url: url,
                options: {
                    format: 'A4',
                    printBackground: true,
                    margin: {
                        top: '1cm',
                        bottom: '1cm',
                        left: '1cm',
                        right: '1cm'
                    }
                }
            })
        }
    );

    const buffer = await response.buffer();
    fs.writeFileSync('document.pdf', buffer);
}
```

**콘텐츠 스크래핑**:
```javascript
async function scrapeContent(url) {
    const response = await fetch(
        'https://production-sfo.browserless.io/scrape?token=YOUR_TOKEN',
        {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                url: url,
                elements: [
                    { selector: 'h1' },
                    { selector: 'p', timeout: 5000 },
                    { selector: '.price', attribute: 'data-value' }
                ]
            })
        }
    );

    const data = await response.json();
    console.log(data);
    // { data: [{ selector: 'h1', results: [{text: '...'}] }, ...] }
}
```

✅ **체크포인트**
- [ ] 스크린샷 API를 호출할 수 있는가?
- [ ] PDF 옵션(마진, 포맷 등)을 설정할 수 있는가?
- [ ] 스크래핑 API로 특정 요소를 추출할 수 있는가?

⚠️ **흔한 실수**
- API 토큰이 URL 쿼리 파라미터에 포함되어야 함
- 응답이 바이너리(이미지/PDF)인지 JSON인지 확인

🔗 **더 알아보기**: [REST APIs](https://docs.browserless.io/rest-apis/intro)

---

### 4.2 Puppeteer/Playwright 연결

📌 **핵심 개념**

기존 Puppeteer/Playwright 코드의 `launch()`를 `connect()`로 바꾸면 Browserless 클라우드에서 실행됩니다.

💻 **코드 예제: Puppeteer 연결**

```javascript
const puppeteer = require('puppeteer');

async function runOnBrowserless() {
    // 로컬 실행 시:
    // const browser = await puppeteer.launch({ headless: true });

    // Browserless 연결:
    const browser = await puppeteer.connect({
        browserWSEndpoint: `wss://production-sfo.browserless.io?token=${process.env.BROWSERLESS_TOKEN}`
    });

    try {
        const page = await browser.newPage();

        // 뷰포트 설정
        await page.setViewport({ width: 1920, height: 1080 });

        // 유저 에이전트 설정
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...');

        // 페이지 이동
        await page.goto('https://example.com', {
            waitUntil: 'networkidle2',
            timeout: 30000
        });

        // 스크린샷
        await page.screenshot({ path: 'result.png', fullPage: true });

        // 데이터 추출
        const title = await page.title();
        const content = await page.evaluate(() => {
            return document.querySelector('h1').textContent;
        });

        console.log({ title, content });

    } finally {
        await browser.close();
    }
}

runOnBrowserless();
```

**Playwright 연결**:
```javascript
const { chromium } = require('playwright');

async function runPlaywright() {
    const browser = await chromium.connectOverCDP(
        `wss://production-sfo.browserless.io?token=${process.env.BROWSERLESS_TOKEN}`
    );

    const context = await browser.newContext();
    const page = await context.newPage();

    await page.goto('https://example.com');
    await page.screenshot({ path: 'playwright-result.png' });

    await browser.close();
}
```

**Python (Playwright)**:
```python
from playwright.sync_api import sync_playwright
import os

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(
        f"wss://production-sfo.browserless.io?token={os.environ['BROWSERLESS_TOKEN']}"
    )

    page = browser.new_page()
    page.goto("https://example.com")
    page.screenshot(path="result.png")

    browser.close()
```

✅ **체크포인트**
- [ ] `puppeteer.connect()`로 Browserless에 연결할 수 있는가?
- [ ] Playwright의 `connectOverCDP()`를 사용할 수 있는가?
- [ ] 기존 로컬 코드를 최소한의 수정으로 전환할 수 있는가?

⚠️ **흔한 실수**
- `launch()` 대신 `connect()` 사용
- WebSocket URL에 토큰 포함 필수
- `browser.close()` 호출로 세션 정리

🔗 **더 알아보기**: [Puppeteer Library](https://docs.browserless.io/libraries/puppeteer)

---

### 4.3 Self-hosted Docker 실행

📌 **핵심 개념**

Browserless Docker 이미지를 로컬이나 자체 서버에서 실행하면 무료로 사용할 수 있습니다.

💻 **코드 예제: Docker 설정**

```bash
# 기본 실행
docker run -p 3000:3000 ghcr.io/browserless/chromium

# 환경 변수 설정
docker run -p 3000:3000 \
  -e "MAX_CONCURRENT_SESSIONS=10" \
  -e "CONNECTION_TIMEOUT=60000" \
  -e "TOKEN=my-secret-token" \
  ghcr.io/browserless/chromium

# 볼륨 마운트 (데이터 유지)
docker run -p 3000:3000 \
  -v /tmp/browserless-data:/data \
  ghcr.io/browserless/chromium
```

**docker-compose.yml**:
```yaml
version: '3.8'
services:
  browserless:
    image: ghcr.io/browserless/chromium
    ports:
      - "3000:3000"
    environment:
      - MAX_CONCURRENT_SESSIONS=10
      - CONNECTION_TIMEOUT=60000
      - TOKEN=${BROWSERLESS_TOKEN}
      - ENABLE_CORS=true
    restart: unless-stopped
    # 메모리 제한 (권장)
    deploy:
      resources:
        limits:
          memory: 4G
```

**로컬 연결**:
```javascript
const puppeteer = require('puppeteer');

// Self-hosted 연결
const browser = await puppeteer.connect({
    browserWSEndpoint: 'ws://localhost:3000'  // 토큰 설정 안 했으면 생략
});

// 또는 토큰 포함
const browser = await puppeteer.connect({
    browserWSEndpoint: 'ws://localhost:3000?token=my-secret-token'
});
```

**모니터링 엔드포인트**:
```bash
# 상태 확인
curl http://localhost:3000/pressure

# 응답 예시:
# {
#   "date": "2025-01-15T...",
#   "isAvailable": true,
#   "queued": 0,
#   "running": 1,
#   "maxConcurrent": 10
# }

# 문서 페이지
# http://localhost:3000/docs
```

✅ **체크포인트**
- [ ] Docker로 Browserless를 실행할 수 있는가?
- [ ] 동시 세션 수와 타임아웃을 설정할 수 있는가?
- [ ] 로컬 인스턴스에 연결할 수 있는가?

⚠️ **흔한 실수**
- 메모리 부족 시 Chrome 크래시 → 4GB 이상 권장
- `MAX_CONCURRENT_SESSIONS`를 너무 높게 설정하지 말 것

🔗 **더 알아보기**: [Docker Quickstart](https://docs.browserless.io/docker/quickstart)

---

### 4.4 안티봇 우회 (BrowserQL)

📌 **핵심 개념**

BrowserQL은 GraphQL 기반 쿼리 언어로, Stealth 모드와 CAPTCHA 해결 기능을 제공합니다.

💻 **코드 예제: BrowserQL 쿼리**

```javascript
async function scrapeWithStealth(url) {
    const query = `
    mutation Scrape {
        goto(url: "${url}", waitUntil: networkIdle) {
            status
        }

        # Stealth 모드로 봇 탐지 우회
        stealth {
            fingerprint
        }

        # 페이지 콘텐츠 추출
        content: text(selector: "body")

        # 특정 요소 대기 후 추출
        title: text(selector: "h1", timeout: 5000)

        # 스크린샷
        screenshot(fullPage: true) {
            base64
        }
    }
    `;

    const response = await fetch(
        'https://production-sfo.browserless.io/chromium/bql?token=YOUR_TOKEN',
        {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        }
    );

    const result = await response.json();
    console.log(result.data);
}
```

**/unblock API (간단한 우회)**:
```javascript
async function unblockPage(url) {
    const response = await fetch(
        'https://production-sfo.browserless.io/unblock?token=YOUR_TOKEN',
        {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                url: url,
                browserWSEndpoint: false,  // 직접 콘텐츠 반환
                cookies: true,
                content: true,
                screenshot: true
            })
        }
    );

    const data = await response.json();
    console.log(data.content);  // HTML 콘텐츠
    // data.screenshot: base64 이미지
    // data.cookies: 쿠키 배열
}
```

**CAPTCHA 해결**:
```javascript
// BrowserQL로 CAPTCHA 자동 해결
const query = `
mutation SolveCaptcha {
    goto(url: "https://example.com/login") {
        status
    }

    # CAPTCHA 감지 및 해결
    solveCaptcha(timeout: 30000) {
        solved
        type  # recaptcha, hcaptcha 등
    }

    # 로그인 진행
    type(selector: "#email", text: "user@example.com")
    type(selector: "#password", text: "password123")
    click(selector: "button[type=submit]")

    # 결과 확인
    waitForNavigation(timeout: 10000) {
        url
    }
}
`;
```

✅ **체크포인트**
- [ ] BrowserQL 쿼리를 작성할 수 있는가?
- [ ] Stealth 모드를 활성화할 수 있는가?
- [ ] /unblock API를 사용할 수 있는가?

⚠️ **흔한 실수**
- BrowserQL은 Enterprise/Pro 플랜 기능
- CAPTCHA 해결은 추가 비용 발생 가능

🔗 **더 알아보기**: [BrowserQL](https://docs.browserless.io/browserql)

---

### 4.5 Persistent Sessions

📌 **핵심 개념**

쿠키, localStorage, 캐시를 세션 간에 유지하여 로그인 상태를 보존할 수 있습니다.

💻 **코드 예제: 세션 유지**

```javascript
const puppeteer = require('puppeteer');

// 1. 세션 ID 생성 및 로그인
async function createSession() {
    const sessionId = 'my-persistent-session-123';

    const browser = await puppeteer.connect({
        browserWSEndpoint:
            `wss://production-sfo.browserless.io?token=YOUR_TOKEN&persist=${sessionId}`
    });

    const page = await browser.newPage();
    await page.goto('https://example.com/login');

    // 로그인 수행
    await page.type('#email', 'user@example.com');
    await page.type('#password', 'password');
    await page.click('button[type="submit"]');
    await page.waitForNavigation();

    console.log('로그인 완료, 세션 저장됨');
    await browser.close();

    return sessionId;
}

// 2. 저장된 세션으로 재접속
async function useSession(sessionId) {
    const browser = await puppeteer.connect({
        browserWSEndpoint:
            `wss://production-sfo.browserless.io?token=YOUR_TOKEN&persist=${sessionId}`
    });

    const page = await browser.newPage();
    await page.goto('https://example.com/dashboard');

    // 이미 로그인된 상태!
    const username = await page.$eval('.username', el => el.textContent);
    console.log('현재 사용자:', username);

    await browser.close();
}

// 실행
(async () => {
    const sessionId = await createSession();
    // ... 나중에
    await useSession(sessionId);
})();
```

**세션 관리 API**:
```javascript
// 세션 목록 조회
const sessions = await fetch(
    'https://production-sfo.browserless.io/sessions?token=YOUR_TOKEN'
).then(r => r.json());

// 특정 세션 삭제
await fetch(
    `https://production-sfo.browserless.io/sessions/${sessionId}?token=YOUR_TOKEN`,
    { method: 'DELETE' }
);
```

✅ **체크포인트**
- [ ] `persist` 파라미터로 세션을 유지할 수 있는가?
- [ ] 동일 세션 ID로 재접속할 수 있는가?
- [ ] 세션 관리 API를 사용할 수 있는가?

⚠️ **흔한 실수**
- 세션은 최대 90일 보관 (플랜에 따라 다름)
- 민감한 정보(비밀번호 등)는 별도 관리

🔗 **더 알아보기**: [Persistent Sessions](https://docs.browserless.io/features/persistent-sessions)

---

### 4.6 Function API (커스텀 코드 실행)

📌 **핵심 개념**

Function API를 사용하면 Puppeteer/Playwright 코드를 서버에 전송하여 실행할 수 있습니다.

💻 **코드 예제: Function API**

```javascript
async function runCustomFunction() {
    const code = `
    module.exports = async ({ page }) => {
        await page.goto('https://news.ycombinator.com');

        // 뉴스 항목 추출
        const items = await page.evaluate(() => {
            const rows = document.querySelectorAll('.athing');
            return Array.from(rows).slice(0, 10).map(row => {
                const titleEl = row.querySelector('.titleline a');
                const scoreEl = row.nextElementSibling?.querySelector('.score');
                return {
                    title: titleEl?.textContent,
                    url: titleEl?.href,
                    score: scoreEl?.textContent || '0 points'
                };
            });
        });

        return { items };
    };
    `;

    const response = await fetch(
        'https://production-sfo.browserless.io/function?token=YOUR_TOKEN',
        {
            method: 'POST',
            headers: { 'Content-Type': 'application/javascript' },
            body: code
        }
    );

    const result = await response.json();
    console.log(result.items);
}
```

**컨텍스트 옵션 전달**:
```javascript
const code = `
module.exports = async ({ page, context }) => {
    const { searchTerm } = context;

    await page.goto('https://google.com');
    await page.type('textarea[name="q"]', searchTerm);
    await page.keyboard.press('Enter');
    await page.waitForNavigation();

    const results = await page.evaluate(() => {
        return Array.from(document.querySelectorAll('h3')).map(h => h.textContent);
    });

    return { searchTerm, results };
};
`;

const response = await fetch(
    'https://production-sfo.browserless.io/function?token=YOUR_TOKEN',
    {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            code,
            context: { searchTerm: 'Browserless tutorial' }
        })
    }
);
```

✅ **체크포인트**
- [ ] Function API에 코드를 전송할 수 있는가?
- [ ] context를 통해 파라미터를 전달할 수 있는가?
- [ ] 결과를 JSON으로 반환받을 수 있는가?

⚠️ **흔한 실수**
- 코드는 문자열로 전송 (템플릿 리터럴 사용)
- `module.exports` 필수
- 외부 모듈 import 제한

🔗 **더 알아보기**: [Function API](https://docs.browserless.io/rest-apis/function)

---

## Part 5: 실전 프로젝트

### 5.1 미니 프로젝트 아이디어

| 난이도 | 프로젝트 | 학습 포인트 |
|--------|---------|------------|
| 🟢 | 웹페이지 PDF 변환 서비스 | REST API 기본 |
| 🟢 | 경쟁사 가격 모니터링 | 스크래핑, 스케줄링 |
| 🟡 | 소셜 미디어 스크린샷 봇 | 인증, 세션 유지 |
| 🟡 | SEO 크롤러 | 대규모 크롤링, 큐 |
| 🔴 | 안티봇 사이트 스크래핑 | BrowserQL, Stealth |

### 5.2 단계별 구현 가이드: 가격 모니터링 시스템

**목표**: 경쟁사 상품 가격을 주기적으로 수집하여 저장

```javascript
// price-monitor.js
const puppeteer = require('puppeteer');

class PriceMonitor {
    constructor(browserlessToken) {
        this.token = browserlessToken;
        this.results = [];
    }

    async connect() {
        this.browser = await puppeteer.connect({
            browserWSEndpoint: `wss://production-sfo.browserless.io?token=${this.token}`
        });
    }

    async scrapePrice(url, selectors) {
        const page = await this.browser.newPage();

        try {
            // 봇 탐지 우회 설정
            await page.setUserAgent(
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            );
            await page.setExtraHTTPHeaders({
                'Accept-Language': 'ko-KR,ko;q=0.9'
            });

            await page.goto(url, {
                waitUntil: 'networkidle2',
                timeout: 30000
            });

            // 가격 추출
            const data = await page.evaluate((sel) => {
                const priceEl = document.querySelector(sel.price);
                const nameEl = document.querySelector(sel.name);

                return {
                    name: nameEl?.textContent?.trim(),
                    price: priceEl?.textContent?.trim(),
                    timestamp: new Date().toISOString()
                };
            }, selectors);

            // 스크린샷 (증거용)
            await page.screenshot({
                path: `screenshots/${Date.now()}.png`
            });

            this.results.push({ url, ...data });
            return data;

        } catch (error) {
            console.error(`Error scraping ${url}:`, error.message);
            return null;

        } finally {
            await page.close();
        }
    }

    async close() {
        await this.browser.close();
    }
}

// 사용 예시
async function main() {
    const monitor = new PriceMonitor(process.env.BROWSERLESS_TOKEN);
    await monitor.connect();

    const products = [
        {
            url: 'https://store1.com/product/123',
            selectors: { name: '.product-title', price: '.price' }
        },
        {
            url: 'https://store2.com/item/456',
            selectors: { name: 'h1', price: '.amount' }
        }
    ];

    for (const product of products) {
        const result = await monitor.scrapePrice(product.url, product.selectors);
        if (result) {
            console.log(`${result.name}: ${result.price}`);
        }
        // 요청 간 딜레이 (차단 방지)
        await new Promise(r => setTimeout(r, 2000));
    }

    await monitor.close();

    // 결과 저장 (DB 또는 파일)
    console.log('Results:', monitor.results);
}

main();
```

### 5.3 Best Practices

**비용 최적화**:
```javascript
// 1. 이미지/폰트 차단으로 대역폭 절약
await page.setRequestInterception(true);
page.on('request', req => {
    if (['image', 'stylesheet', 'font'].includes(req.resourceType())) {
        req.abort();
    } else {
        req.continue();
    }
});

// 2. 필요한 리소스만 대기
await page.goto(url, { waitUntil: 'domcontentloaded' });  // networkidle 대신

// 3. 세션 재사용
const sessionId = 'reusable-session';
// persist 파라미터 사용
```

**운영 권장사항**:

1. **요청 간 딜레이**: 2-5초 랜덤 딜레이로 차단 방지
2. **에러 처리**: 재시도 로직 구현
3. **프록시 로테이션**: 대규모 스크래핑 시 필수
4. **세션 관리**: 로그인 필요한 사이트는 세션 유지
5. **로깅**: 모든 요청/응답 기록

```javascript
// 재시도 로직 예시
async function scrapeWithRetry(url, maxRetries = 3) {
    for (let i = 0; i < maxRetries; i++) {
        try {
            return await scrape(url);
        } catch (error) {
            console.log(`Attempt ${i + 1} failed, retrying...`);
            await new Promise(r => setTimeout(r, 1000 * (i + 1)));
        }
    }
    throw new Error(`Failed after ${maxRetries} attempts`);
}
```

---

## 요약

Browserless는 브라우저 자동화의 인프라 부담을 제거합니다:

- **시작**: REST API 또는 Puppeteer/Playwright 연결
- **Self-hosted**: Docker로 무료 운영 가능
- **고급 기능**: Stealth 모드, CAPTCHA 해결, 세션 유지
- **통합**: 기존 코드 최소 수정으로 전환

다음 단계:
1. [Free 플랜 가입](https://www.browserless.io/) (500 크레딧 무료)
2. REST API로 스크린샷 테스트
3. 기존 Puppeteer 프로젝트 마이그레이션
