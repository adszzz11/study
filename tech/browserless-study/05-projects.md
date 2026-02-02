# 실전 프로젝트 및 Best Practices

## 프로젝트 아이디어

### 난이도별 프로젝트

#### 초급 프로젝트

##### 1. 웹사이트 스크린샷 자동화
**목표**: 여러 웹사이트의 스크린샷을 자동으로 생성하고 저장

```javascript
const puppeteer = require('puppeteer-core');
const fs = require('fs');

async function captureWebsites(urls) {
  const browser = await puppeteer.connect({
    browserWSEndpoint: 'ws://localhost:3000'
  });

  const results = [];

  for (const url of urls) {
    const page = await browser.newPage();

    try {
      await page.setViewport({ width: 1920, height: 1080 });
      await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });

      const filename = `screenshot_${new URL(url).hostname}_${Date.now()}.png`;
      await page.screenshot({ path: filename, fullPage: true });

      results.push({ url, filename, success: true });
    } catch (error) {
      results.push({ url, error: error.message, success: false });
    } finally {
      await page.close();
    }
  }

  await browser.close();
  return results;
}

// 실행
const websites = [
  'https://github.com',
  'https://news.ycombinator.com',
  'https://example.com'
];

captureWebsites(websites).then(results => {
  console.log(JSON.stringify(results, null, 2));
});
```

##### 2. 가격 모니터링 알림
**목표**: 특정 상품 가격을 주기적으로 확인하고 변동 시 알림

```javascript
const puppeteer = require('puppeteer-core');
const fs = require('fs');

const PRICE_FILE = 'prices.json';

async function checkPrice(url, selector) {
  const browser = await puppeteer.connect({
    browserWSEndpoint: 'ws://localhost:3000'
  });

  const page = await browser.newPage();
  await page.goto(url, { waitUntil: 'networkidle2' });

  const priceText = await page.$eval(selector, el => el.textContent);
  const price = parseFloat(priceText.replace(/[^0-9.]/g, ''));

  await browser.close();
  return price;
}

async function monitorPrice(productUrl, priceSelector, targetPrice) {
  const currentPrice = await checkPrice(productUrl, priceSelector);

  // 이전 가격 로드
  let previousPrice = null;
  if (fs.existsSync(PRICE_FILE)) {
    const data = JSON.parse(fs.readFileSync(PRICE_FILE, 'utf8'));
    previousPrice = data[productUrl];
  }

  // 가격 저장
  const prices = fs.existsSync(PRICE_FILE)
    ? JSON.parse(fs.readFileSync(PRICE_FILE, 'utf8'))
    : {};
  prices[productUrl] = currentPrice;
  fs.writeFileSync(PRICE_FILE, JSON.stringify(prices, null, 2));

  // 결과 분석
  const result = {
    url: productUrl,
    currentPrice,
    previousPrice,
    targetPrice,
    priceDropped: currentPrice < targetPrice,
    priceChanged: previousPrice !== null && previousPrice !== currentPrice
  };

  if (result.priceDropped) {
    console.log(`가격 알림: ${currentPrice}원 (목표: ${targetPrice}원 이하)`);
  }

  return result;
}
```

#### 중급 프로젝트

##### 3. 뉴스 애그리게이터
**목표**: 여러 뉴스 사이트에서 기사를 수집하여 통합

```javascript
const puppeteer = require('puppeteer-core');

class NewsAggregator {
  constructor() {
    this.sources = [
      {
        name: 'Hacker News',
        url: 'https://news.ycombinator.com',
        selectors: {
          articles: '.athing',
          title: '.titleline > a',
          link: '.titleline > a',
          score: '.score'
        }
      },
      // 다른 뉴스 소스 추가...
    ];
  }

  async scrapeSource(browser, source) {
    const page = await browser.newPage();

    try {
      await page.goto(source.url, { waitUntil: 'networkidle2' });

      const articles = await page.$$eval(
        source.selectors.articles,
        (elements, selectors) => {
          return elements.slice(0, 10).map(el => {
            const titleEl = el.querySelector(selectors.title);
            const linkEl = el.querySelector(selectors.link);

            return {
              title: titleEl?.textContent?.trim(),
              link: linkEl?.href
            };
          });
        },
        source.selectors
      );

      return {
        source: source.name,
        articles: articles.filter(a => a.title && a.link),
        success: true
      };
    } catch (error) {
      return {
        source: source.name,
        error: error.message,
        success: false
      };
    } finally {
      await page.close();
    }
  }

  async aggregate() {
    const browser = await puppeteer.connect({
      browserWSEndpoint: 'ws://localhost:3000'
    });

    const results = await Promise.all(
      this.sources.map(source => this.scrapeSource(browser, source))
    );

    await browser.close();

    return {
      timestamp: new Date().toISOString(),
      sources: results
    };
  }
}

// 사용
const aggregator = new NewsAggregator();
aggregator.aggregate().then(data => {
  console.log(JSON.stringify(data, null, 2));
});
```

##### 4. PDF 보고서 생성기
**목표**: 동적 데이터로 HTML 보고서를 생성하고 PDF로 변환

```javascript
const puppeteer = require('puppeteer-core');
const fs = require('fs');

class ReportGenerator {
  constructor(browserEndpoint = 'ws://localhost:3000') {
    this.browserEndpoint = browserEndpoint;
  }

  generateHTML(data) {
    return `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <style>
          body { font-family: 'Noto Sans KR', sans-serif; padding: 40px; }
          h1 { color: #333; border-bottom: 2px solid #007bff; }
          table { width: 100%; border-collapse: collapse; margin: 20px 0; }
          th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
          th { background-color: #007bff; color: white; }
          tr:nth-child(even) { background-color: #f9f9f9; }
          .footer { margin-top: 40px; font-size: 12px; color: #666; }
        </style>
      </head>
      <body>
        <h1>${data.title}</h1>
        <p>생성일: ${new Date().toLocaleDateString('ko-KR')}</p>

        <table>
          <thead>
            <tr>
              ${data.columns.map(col => `<th>${col}</th>`).join('')}
            </tr>
          </thead>
          <tbody>
            ${data.rows.map(row => `
              <tr>
                ${row.map(cell => `<td>${cell}</td>`).join('')}
              </tr>
            `).join('')}
          </tbody>
        </table>

        <div class="footer">
          <p>본 보고서는 자동으로 생성되었습니다.</p>
        </div>
      </body>
      </html>
    `;
  }

  async generatePDF(data, outputPath) {
    const html = this.generateHTML(data);
    const tempHtmlPath = `/tmp/report_${Date.now()}.html`;
    fs.writeFileSync(tempHtmlPath, html);

    const browser = await puppeteer.connect({
      browserWSEndpoint: this.browserEndpoint
    });

    const page = await browser.newPage();
    await page.goto(`file://${tempHtmlPath}`, { waitUntil: 'networkidle0' });

    await page.pdf({
      path: outputPath,
      format: 'A4',
      printBackground: true,
      margin: { top: '20mm', right: '20mm', bottom: '20mm', left: '20mm' }
    });

    await browser.close();
    fs.unlinkSync(tempHtmlPath);

    return outputPath;
  }
}

// 사용
const generator = new ReportGenerator();

const reportData = {
  title: '월간 판매 보고서',
  columns: ['제품명', '판매량', '매출액', '전월 대비'],
  rows: [
    ['제품 A', '1,234', '12,340,000원', '+15%'],
    ['제품 B', '567', '5,670,000원', '+8%'],
    ['제품 C', '890', '8,900,000원', '-3%']
  ]
};

generator.generatePDF(reportData, 'report.pdf').then(path => {
  console.log(`보고서 생성: ${path}`);
});
```

#### 고급 프로젝트

##### 5. 소셜 미디어 모니터링
**목표**: 키워드 기반 소셜 미디어 게시물 수집 및 분석

```javascript
const puppeteer = require('puppeteer-core');

class SocialMonitor {
  constructor() {
    this.browserEndpoint = 'ws://localhost:3000';
  }

  async searchTwitter(keyword, maxResults = 20) {
    const browser = await puppeteer.connect({
      browserWSEndpoint: this.browserEndpoint
    });

    const page = await browser.newPage();

    // User-Agent 설정
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');

    await page.goto(`https://twitter.com/search?q=${encodeURIComponent(keyword)}&f=live`);

    // 로딩 대기
    await page.waitForTimeout(3000);

    // 스크롤하여 더 많은 결과 로드
    let tweets = [];
    let scrollAttempts = 0;

    while (tweets.length < maxResults && scrollAttempts < 5) {
      const newTweets = await page.evaluate(() => {
        const tweetElements = document.querySelectorAll('article');
        return Array.from(tweetElements).map(tweet => {
          const textEl = tweet.querySelector('[data-testid="tweetText"]');
          const timeEl = tweet.querySelector('time');
          const authorEl = tweet.querySelector('[data-testid="User-Name"]');

          return {
            text: textEl?.textContent,
            time: timeEl?.getAttribute('datetime'),
            author: authorEl?.textContent
          };
        });
      });

      tweets = [...new Map(newTweets.map(t => [t.text, t])).values()];

      await page.evaluate(() => window.scrollBy(0, 1000));
      await page.waitForTimeout(2000);
      scrollAttempts++;
    }

    await browser.close();
    return tweets.slice(0, maxResults);
  }

  async monitor(keywords, interval = 300000) {
    console.log(`모니터링 시작: ${keywords.join(', ')}`);

    const check = async () => {
      for (const keyword of keywords) {
        console.log(`검색 중: ${keyword}`);
        const results = await this.searchTwitter(keyword, 10);
        console.log(`${keyword}: ${results.length}개 결과`);

        // 여기에 알림 로직 추가 (Slack, Discord, Email 등)
      }
    };

    await check();
    setInterval(check, interval);
  }
}
```

##### 6. E2E 테스트 자동화
**목표**: 웹 애플리케이션 E2E 테스트 실행 및 보고서 생성

```javascript
const puppeteer = require('puppeteer-core');

class E2ETestRunner {
  constructor(baseUrl, browserEndpoint = 'ws://localhost:3000') {
    this.baseUrl = baseUrl;
    this.browserEndpoint = browserEndpoint;
    this.results = [];
  }

  async runTest(name, testFn) {
    const browser = await puppeteer.connect({
      browserWSEndpoint: this.browserEndpoint
    });

    const page = await browser.newPage();
    const startTime = Date.now();

    try {
      await testFn(page, this.baseUrl);

      this.results.push({
        name,
        status: 'passed',
        duration: Date.now() - startTime
      });
    } catch (error) {
      // 실패 시 스크린샷
      const screenshot = await page.screenshot({ encoding: 'base64' });

      this.results.push({
        name,
        status: 'failed',
        duration: Date.now() - startTime,
        error: error.message,
        screenshot
      });
    } finally {
      await browser.close();
    }
  }

  async run(tests) {
    for (const [name, testFn] of Object.entries(tests)) {
      console.log(`테스트 실행: ${name}`);
      await this.runTest(name, testFn);
    }

    return this.generateReport();
  }

  generateReport() {
    const passed = this.results.filter(r => r.status === 'passed').length;
    const failed = this.results.filter(r => r.status === 'failed').length;
    const totalDuration = this.results.reduce((sum, r) => sum + r.duration, 0);

    return {
      summary: {
        total: this.results.length,
        passed,
        failed,
        duration: `${totalDuration}ms`
      },
      tests: this.results
    };
  }
}

// 테스트 정의
const tests = {
  '홈페이지 로드': async (page, baseUrl) => {
    await page.goto(baseUrl);
    const title = await page.title();
    if (!title) throw new Error('제목이 없습니다');
  },

  '로그인 폼 표시': async (page, baseUrl) => {
    await page.goto(`${baseUrl}/login`);
    await page.waitForSelector('#login-form');
  },

  '로그인 성공': async (page, baseUrl) => {
    await page.goto(`${baseUrl}/login`);
    await page.type('#username', 'testuser');
    await page.type('#password', 'testpass');
    await page.click('#login-button');
    await page.waitForNavigation();
    await page.waitForSelector('.user-dashboard');
  }
};

// 실행
const runner = new E2ETestRunner('https://example.com');
runner.run(tests).then(report => {
  console.log(JSON.stringify(report, null, 2));
});
```

## Best Practices

### 1. 코드 구조화

```
project/
├── src/
│   ├── browser/
│   │   ├── client.js      # Browserless 연결 관리
│   │   └── pool.js        # 브라우저 풀 관리
│   ├── scrapers/
│   │   ├── base.js        # 기본 스크래퍼 클래스
│   │   └── news.js        # 뉴스 스크래퍼
│   ├── utils/
│   │   ├── retry.js       # 재시도 로직
│   │   └── delay.js       # 딜레이 유틸리티
│   └── index.js
├── config/
│   └── default.json
├── sessions/              # 세션 데이터
├── output/                # 결과 파일
└── package.json
```

### 2. 에러 처리 패턴

```javascript
class RobustScraper {
  async withRetry(fn, maxRetries = 3, delay = 1000) {
    for (let i = 0; i < maxRetries; i++) {
      try {
        return await fn();
      } catch (error) {
        console.log(`시도 ${i + 1}/${maxRetries} 실패: ${error.message}`);

        if (i === maxRetries - 1) throw error;

        await new Promise(r => setTimeout(r, delay * (i + 1)));
      }
    }
  }

  async safeNavigate(page, url, options = {}) {
    const defaultOptions = {
      waitUntil: 'networkidle2',
      timeout: 30000
    };

    try {
      await page.goto(url, { ...defaultOptions, ...options });
      return { success: true };
    } catch (error) {
      // 타임아웃의 경우 부분 로드 시도
      if (error.message.includes('timeout')) {
        console.log('타임아웃, 부분 로드로 계속...');
        return { success: true, partial: true };
      }
      throw error;
    }
  }
}
```

### 3. 리소스 관리

```javascript
class ResourceManager {
  constructor(maxConcurrent = 5) {
    this.maxConcurrent = maxConcurrent;
    this.active = 0;
    this.queue = [];
  }

  async acquire() {
    if (this.active < this.maxConcurrent) {
      this.active++;
      return;
    }

    await new Promise(resolve => this.queue.push(resolve));
    this.active++;
  }

  release() {
    this.active--;
    if (this.queue.length > 0) {
      const next = this.queue.shift();
      next();
    }
  }

  async withResource(fn) {
    await this.acquire();
    try {
      return await fn();
    } finally {
      this.release();
    }
  }
}

// 사용
const manager = new ResourceManager(5);

const urls = ['url1', 'url2', /* ... */];

await Promise.all(urls.map(url =>
  manager.withResource(async () => {
    const browser = await puppeteer.connect({ browserWSEndpoint: 'ws://localhost:3000' });
    // 스크래핑...
    await browser.close();
  })
));
```

### 4. 로깅 및 모니터링

```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' }),
    new winston.transports.Console({
      format: winston.format.simple()
    })
  ]
});

class LoggedScraper {
  async scrape(url) {
    const startTime = Date.now();

    logger.info('스크래핑 시작', { url });

    try {
      const result = await this.doScrape(url);

      logger.info('스크래핑 완료', {
        url,
        duration: Date.now() - startTime,
        itemCount: result.length
      });

      return result;
    } catch (error) {
      logger.error('스크래핑 실패', {
        url,
        duration: Date.now() - startTime,
        error: error.message
      });

      throw error;
    }
  }
}
```

### 5. 설정 관리

```javascript
// config/default.json
{
  "browserless": {
    "endpoint": "ws://localhost:3000",
    "timeout": 30000
  },
  "scraping": {
    "maxConcurrent": 5,
    "retryCount": 3,
    "delayBetweenRequests": 1000
  },
  "output": {
    "directory": "./output",
    "format": "json"
  }
}

// src/config.js
const config = require('config');

module.exports = {
  browserEndpoint: config.get('browserless.endpoint'),
  timeout: config.get('browserless.timeout'),
  maxConcurrent: config.get('scraping.maxConcurrent'),
  // ...
};
```

## 운영 체크리스트

### 배포 전 확인

- [ ] Docker 리소스 설정 (메모리, CPU)
- [ ] 동시 접속 제한 설정
- [ ] API 토큰 설정
- [ ] 모니터링 구성
- [ ] 로그 로테이션 설정
- [ ] 백업 전략 수립

### 모니터링 항목

- [ ] 브라우저 메모리 사용량
- [ ] 요청 성공/실패율
- [ ] 응답 시간
- [ ] 큐 대기 시간
- [ ] 에러 발생 빈도

### 보안 점검

- [ ] API 토큰 보안
- [ ] 네트워크 격리
- [ ] 세션 데이터 암호화
- [ ] 입력 검증
- [ ] rate limiting

## 다음 단계

- [[cheatsheet|치트시트]] - 빠른 참조
- [[README|학습 가이드]] - 처음으로 돌아가기
