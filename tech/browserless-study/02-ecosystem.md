# Browserless 에코시스템

## 관련 기술 스택

### 브라우저 자동화 도구

#### Puppeteer
- **개발사**: Google
- **언어**: Node.js (JavaScript/TypeScript)
- **특징**:
  - Chrome/Chromium 전용
  - Google 공식 지원
  - 가장 널리 사용됨

```javascript
const puppeteer = require('puppeteer');
const browser = await puppeteer.connect({
  browserWSEndpoint: 'ws://localhost:3000'
});
```

#### Playwright
- **개발사**: Microsoft
- **언어**: Node.js, Python, Java, .NET
- **특징**:
  - 멀티 브라우저 (Chrome, Firefox, Safari)
  - 자동 대기 기능
  - 강력한 셀렉터

```javascript
const playwright = require('playwright');
const browser = await playwright.chromium.connect({
  wsEndpoint: 'ws://localhost:3000/chromium/playwright'
});
```

#### Selenium
- **개발사**: Selenium 프로젝트
- **언어**: 다중 언어 지원
- **특징**:
  - 전통적인 웹 테스트 도구
  - 광범위한 브라우저 지원
  - WebDriver 프로토콜

```python
from selenium import webdriver
driver = webdriver.Remote(
    command_executor='http://localhost:3000/webdriver',
    options=webdriver.ChromeOptions()
)
```

### 도구 비교표

| 특성 | Puppeteer | Playwright | Selenium |
|------|-----------|------------|----------|
| 다중 브라우저 | X | O | O |
| 자동 대기 | 수동 | 자동 | 수동 |
| 속도 | 빠름 | 빠름 | 보통 |
| 언어 지원 | Node.js | 다중 | 다중 |
| 학습 곡선 | 낮음 | 낮음 | 보통 |
| 병렬 실행 | 제한적 | 강력 | 제한적 |

## Browserless 대안 서비스

### Headless Browser 서비스

| 서비스 | 특징 | 가격 |
|--------|------|------|
| **Browserless** | Self-hosted 무료, BrowserQL | 무료~유료 |
| **Apify** | 웹 스크래핑 플랫폼 | 사용량 기반 |
| **ScrapingBee** | 프록시 통합 | API 호출 기반 |
| **Crawlee** | 오픈소스 크롤링 | 무료 (Self-hosted) |

### 비교 분석

#### Browserless vs Apify
```
Browserless:
- 순수 브라우저 서비스
- 낮은 가격
- Self-hosted 옵션

Apify:
- 전체 스크래핑 플랫폼
- 배우/스케줄러 포함
- 데이터 저장소 제공
```

#### Browserless vs ScrapingBee
```
Browserless:
- WebSocket 연결 지원
- 브라우저 직접 제어
- 커스텀 코드 실행

ScrapingBee:
- REST API 전용
- 프록시 자동 관리
- 간단한 스크래핑에 적합
```

## 기술 트렌드

### 1. 안티봇 대응 발전

```
2020년: 기본 User-Agent 변경
       │
       ▼
2022년: Stealth 플러그인 사용
       │
       ▼
2024년: 지문 스푸핑, 행동 시뮬레이션
       │
       ▼
현재:   AI 기반 CAPTCHA 해결, BrowserQL
```

### 2. 서버리스 브라우저

- AWS Lambda용 Chromium
- Vercel Edge Functions
- Cloudflare Workers
- 콜드 스타트 최소화 기술

### 3. AI 통합

```
웹 스크래핑 + LLM:
- 동적 셀렉터 생성
- 콘텐츠 이해 및 추출
- 자연어 명령 → 브라우저 액션
```

### 4. 크로스 브라우저 표준화

- WebDriver BiDi 프로토콜
- 브라우저 간 일관된 API
- 실시간 양방향 통신

## 관련 생태계

### 프록시 서비스
- **Bright Data**: 주거용 프록시
- **Oxylabs**: 데이터센터 프록시
- **SmartProxy**: 로테이팅 프록시

### CAPTCHA 해결
- **2Captcha**: 인간 해결사
- **Anti-Captcha**: 자동 해결
- **CapSolver**: AI 기반 해결

### 데이터 추출
- **Cheerio**: HTML 파싱 (Node.js)
- **BeautifulSoup**: HTML 파싱 (Python)
- **Scrapy**: 풀 스크래핑 프레임워크

## 통합 아키텍처 예시

```
┌─────────────────────────────────────────────────────────┐
│                    Application                          │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  Scheduler  │  │   Queue     │  │   Storage   │     │
│  │  (Cron/등)  │  │ (Redis/SQS) │  │ (S3/Mongo)  │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │             │
│         ▼                ▼                ▼             │
│  ┌─────────────────────────────────────────────────┐   │
│  │              Browserless                         │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐         │   │
│  │  │ Browser │  │ Browser │  │ Browser │         │   │
│  │  └─────────┘  └─────────┘  └─────────┘         │   │
│  └─────────────────────────────────────────────────┘   │
│                          │                              │
│                          ▼                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │              Proxy Service                       │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## 선택 가이드

### Browserless를 선택해야 할 때
- Self-hosted로 비용 절감 원할 때
- Puppeteer/Playwright 직접 제어 필요 시
- 복잡한 브라우저 자동화 작업
- 로그인 세션 유지 필요 시

### 다른 도구를 고려해야 할 때
- 단순 HTML 파싱만 필요: Cheerio/BeautifulSoup
- 대규모 분산 크롤링: Scrapy + Crawlee
- API 데이터만 필요: 직접 API 호출
- 관리형 서비스 선호: Apify

## 미래 전망

### 기술 발전 방향
1. **더 강력한 안티봇 우회**
2. **AI 기반 자동화**
3. **서버리스 최적화**
4. **실시간 협업 디버깅**

### 시장 동향
- 웹 자동화 수요 증가
- 데이터 스크래핑 규제 강화
- 프라이버시 중심 브라우저 등장

## 다음 단계

- [[03-references|참고 자료]] - 공식 문서 및 학습 자료
- [[04-learning/02-puppeteer-playwright|Puppeteer/Playwright 연결]] - 실습
