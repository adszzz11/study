# REST API 기본 사용

## 개요

Browserless는 강력한 REST API를 제공하여 브라우저 작업을 HTTP 요청으로 수행할 수 있습니다. 코드 작성 없이 curl이나 Postman으로 바로 테스트할 수 있습니다.

## 사전 준비

### Browserless 실행
```bash
# Docker로 Browserless 실행
docker run -p 3000:3000 ghcr.io/browserless/chromium

# 실행 확인
curl http://localhost:3000
```

### 인증 (Cloud 서비스 사용 시)
```bash
# API 토큰을 헤더로 전달
curl -H "Authorization: Bearer YOUR_API_TOKEN" \
  https://chrome.browserless.io/screenshot
```

## 주요 엔드포인트

### 1. Screenshot API - 스크린샷 생성

#### 기본 사용법
```bash
curl -X POST http://localhost:3000/screenshot \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}' \
  --output screenshot.png
```

#### 옵션 상세
```json
{
  "url": "https://example.com",
  "options": {
    "type": "png",
    "fullPage": true,
    "quality": 80
  },
  "viewport": {
    "width": 1920,
    "height": 1080
  }
}
```

#### 옵션 설명
| 옵션 | 타입 | 설명 |
|------|------|------|
| `type` | string | 이미지 형식 (png, jpeg, webp) |
| `fullPage` | boolean | 전체 페이지 캡처 여부 |
| `quality` | number | 이미지 품질 (0-100, jpeg/webp만) |
| `clip` | object | 특정 영역만 캡처 |

#### 특정 영역 캡처
```bash
curl -X POST http://localhost:3000/screenshot \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "options": {
      "clip": {
        "x": 0,
        "y": 0,
        "width": 500,
        "height": 300
      }
    }
  }' \
  --output clip.png
```

### 2. PDF API - PDF 생성

#### 기본 사용법
```bash
curl -X POST http://localhost:3000/pdf \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}' \
  --output document.pdf
```

#### 옵션 상세
```json
{
  "url": "https://example.com",
  "options": {
    "format": "A4",
    "printBackground": true,
    "margin": {
      "top": "20mm",
      "right": "20mm",
      "bottom": "20mm",
      "left": "20mm"
    },
    "displayHeaderFooter": true,
    "headerTemplate": "<div style='font-size:10px;'>Header</div>",
    "footerTemplate": "<div style='font-size:10px;text-align:center;'>Page <span class='pageNumber'></span></div>"
  }
}
```

#### 옵션 설명
| 옵션 | 타입 | 설명 |
|------|------|------|
| `format` | string | 용지 크기 (A4, Letter, Legal 등) |
| `printBackground` | boolean | 배경 인쇄 여부 |
| `landscape` | boolean | 가로 방향 |
| `scale` | number | 확대/축소 (0.1-2) |
| `margin` | object | 여백 설정 |

### 3. Content API - HTML 추출

#### 기본 사용법
```bash
curl -X POST http://localhost:3000/content \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

#### 응답 예시
```html
<!DOCTYPE html>
<html>
<head>
  <title>Example Domain</title>
</head>
<body>
  <h1>Example Domain</h1>
  <p>This domain is for use in illustrative examples...</p>
</body>
</html>
```

### 4. Scrape API - 데이터 추출

#### 기본 사용법
```bash
curl -X POST http://localhost:3000/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://news.ycombinator.com",
    "elements": [
      {
        "selector": ".titleline > a",
        "name": "titles"
      },
      {
        "selector": ".score",
        "name": "scores"
      }
    ]
  }'
```

#### 응답 예시
```json
{
  "data": [
    {
      "titles": ["Article 1", "Article 2", "Article 3"],
      "scores": ["100 points", "50 points", "25 points"]
    }
  ]
}
```

#### 고급 셀렉터
```json
{
  "url": "https://example.com/products",
  "elements": [
    {
      "selector": ".product",
      "name": "products",
      "extractors": [
        { "selector": ".name", "name": "name" },
        { "selector": ".price", "name": "price" },
        { "selector": "img", "name": "image", "attribute": "src" }
      ]
    }
  ]
}
```

## 공통 옵션

### Wait 옵션 - 페이지 로딩 대기

```json
{
  "url": "https://example.com",
  "waitForSelector": ".loaded-content",
  "waitForTimeout": 3000
}
```

| 옵션 | 설명 |
|------|------|
| `waitForSelector` | 특정 요소가 나타날 때까지 대기 |
| `waitForTimeout` | 지정 시간(ms) 대기 |
| `waitForFunction` | 커스텀 조건 대기 |
| `waitForEvent` | 특정 이벤트 대기 |

### Goto 옵션 - 페이지 이동 설정

```json
{
  "url": "https://example.com",
  "gotoOptions": {
    "timeout": 30000,
    "waitUntil": "networkidle2"
  }
}
```

| waitUntil 값 | 설명 |
|-------------|------|
| `load` | load 이벤트 발생 |
| `domcontentloaded` | DOMContentLoaded 이벤트 |
| `networkidle0` | 0.5초간 네트워크 연결 없음 |
| `networkidle2` | 0.5초간 2개 이하 연결 |

### User-Agent 및 헤더

```json
{
  "url": "https://example.com",
  "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
  "extraHeaders": {
    "Accept-Language": "ko-KR,ko;q=0.9"
  }
}
```

## 실전 예제

### 예제 1: 뉴스 사이트 스크래핑

```bash
curl -X POST http://localhost:3000/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://news.ycombinator.com",
    "elements": [
      {
        "selector": ".athing",
        "name": "articles",
        "extractors": [
          {"selector": ".titleline > a", "name": "title"},
          {"selector": ".titleline > a", "name": "link", "attribute": "href"}
        ]
      }
    ]
  }' | jq
```

### 예제 2: 모바일 스크린샷

```bash
curl -X POST http://localhost:3000/screenshot \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "viewport": {
      "width": 375,
      "height": 812,
      "isMobile": true,
      "deviceScaleFactor": 2
    }
  }' \
  --output mobile.png
```

### 예제 3: 인쇄용 PDF

```bash
curl -X POST http://localhost:3000/pdf \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/report",
    "options": {
      "format": "A4",
      "printBackground": true,
      "preferCSSPageSize": true,
      "displayHeaderFooter": true,
      "footerTemplate": "<div style=\"font-size:10px;width:100%;text-align:center;\">페이지 <span class=\"pageNumber\"></span> / <span class=\"totalPages\"></span></div>"
    },
    "emulateMedia": "print"
  }' \
  --output report.pdf
```

### 예제 4: SPA 페이지 콘텐츠 추출

```bash
curl -X POST http://localhost:3000/content \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://spa-example.com",
    "waitForSelector": "#app-loaded",
    "waitForTimeout": 5000,
    "gotoOptions": {
      "waitUntil": "networkidle0"
    }
  }'
```

## 에러 처리

### 일반적인 에러 코드

| 코드 | 설명 | 해결 방법 |
|------|------|----------|
| 400 | 잘못된 요청 | JSON 형식 확인 |
| 401 | 인증 실패 | API 토큰 확인 |
| 408 | 타임아웃 | timeout 값 증가 |
| 500 | 서버 에러 | 로그 확인 |

### 에러 응답 예시
```json
{
  "error": "Navigation timeout of 30000ms exceeded",
  "code": "TIMEOUT"
}
```

## 성능 최적화 팁

### 1. 리소스 차단
```json
{
  "url": "https://example.com",
  "blockAds": true,
  "rejectResourceTypes": ["image", "font", "stylesheet"]
}
```

### 2. 캐싱 활용
- 동일 URL 반복 요청 시 로컬 캐싱 구현
- 이미지 등 정적 리소스는 별도 저장

### 3. 타임아웃 조정
```json
{
  "url": "https://slow-site.com",
  "gotoOptions": {
    "timeout": 60000
  }
}
```

## 다음 단계

- [[02-puppeteer-playwright|Puppeteer/Playwright 연결]] - WebSocket 연결 학습
- [[03-docker-selfhost|Docker Self-hosted]] - 로컬 환경 구축
