# Persistent Sessions - 세션 유지

## 개요

웹 스크래핑이나 자동화에서 로그인 상태를 유지하는 것은 매우 중요합니다. Browserless의 Persistent Sessions를 사용하면 쿠키, 로컬 스토리지, 세션 데이터를 유지할 수 있습니다.

## 세션 유지 방식

### 방식 비교

| 방식 | 장점 | 단점 |
|------|------|------|
| 쿠키 저장/복원 | 간단, 대부분 사이트 동작 | 일부 사이트 불완전 |
| 브라우저 컨텍스트 | 완전한 상태 유지 | 메모리 사용량 |
| 사용자 데이터 디렉토리 | 영구 저장 | 디스크 공간 |
| Browserless Session API | 관리 용이 | 설정 필요 |

## 쿠키 기반 세션

### 쿠키 저장

```javascript
const puppeteer = require('puppeteer-core');
const fs = require('fs');

async function saveCookies() {
  const browser = await puppeteer.connect({
    browserWSEndpoint: 'ws://localhost:3000'
  });

  const page = await browser.newPage();

  // 로그인 수행
  await page.goto('https://example.com/login');
  await page.type('#username', 'myuser');
  await page.type('#password', 'mypassword');
  await page.click('#login-button');
  await page.waitForNavigation();

  // 쿠키 저장
  const cookies = await page.cookies();
  fs.writeFileSync('cookies.json', JSON.stringify(cookies, null, 2));

  console.log('쿠키 저장 완료:', cookies.length, '개');

  await browser.close();
}
```

### 쿠키 복원

```javascript
async function loadCookies() {
  const browser = await puppeteer.connect({
    browserWSEndpoint: 'ws://localhost:3000'
  });

  const page = await browser.newPage();

  // 쿠키 로드
  const cookiesString = fs.readFileSync('cookies.json', 'utf8');
  const cookies = JSON.parse(cookiesString);
  await page.setCookie(...cookies);

  // 로그인 상태로 페이지 접근
  await page.goto('https://example.com/dashboard');

  // 로그인 상태 확인
  const isLoggedIn = await page.$('.user-profile');
  console.log('로그인 상태:', isLoggedIn ? '성공' : '실패');

  await browser.close();
}
```

### 쿠키 + 로컬 스토리지

```javascript
async function saveFullSession() {
  const browser = await puppeteer.connect({
    browserWSEndpoint: 'ws://localhost:3000'
  });

  const page = await browser.newPage();
  await page.goto('https://example.com/login');

  // 로그인 수행...

  // 쿠키 저장
  const cookies = await page.cookies();

  // 로컬 스토리지 저장
  const localStorage = await page.evaluate(() => {
    const items = {};
    for (let i = 0; i < window.localStorage.length; i++) {
      const key = window.localStorage.key(i);
      items[key] = window.localStorage.getItem(key);
    }
    return items;
  });

  // 세션 스토리지 저장
  const sessionStorage = await page.evaluate(() => {
    const items = {};
    for (let i = 0; i < window.sessionStorage.length; i++) {
      const key = window.sessionStorage.key(i);
      items[key] = window.sessionStorage.getItem(key);
    }
    return items;
  });

  const session = { cookies, localStorage, sessionStorage };
  fs.writeFileSync('session.json', JSON.stringify(session, null, 2));

  await browser.close();
}

async function loadFullSession() {
  const browser = await puppeteer.connect({
    browserWSEndpoint: 'ws://localhost:3000'
  });

  const page = await browser.newPage();

  const session = JSON.parse(fs.readFileSync('session.json', 'utf8'));

  // 쿠키 복원
  await page.setCookie(...session.cookies);

  await page.goto('https://example.com');

  // 로컬 스토리지 복원
  await page.evaluate((items) => {
    for (const [key, value] of Object.entries(items)) {
      window.localStorage.setItem(key, value);
    }
  }, session.localStorage);

  // 세션 스토리지 복원
  await page.evaluate((items) => {
    for (const [key, value] of Object.entries(items)) {
      window.sessionStorage.setItem(key, value);
    }
  }, session.sessionStorage);

  // 페이지 새로고침으로 스토리지 적용
  await page.reload();

  await browser.close();
}
```

## Playwright 컨텍스트 저장

### 스토리지 상태 저장

```javascript
const { chromium } = require('playwright');

async function saveStorageState() {
  const browser = await chromium.connect({
    wsEndpoint: 'ws://localhost:3000/chromium/playwright'
  });

  const context = await browser.newContext();
  const page = await context.newPage();

  // 로그인 수행
  await page.goto('https://example.com/login');
  await page.fill('#username', 'myuser');
  await page.fill('#password', 'mypassword');
  await page.click('#login-button');
  await page.waitForURL('**/dashboard');

  // 스토리지 상태 저장 (쿠키 + 로컬 스토리지)
  await context.storageState({ path: 'state.json' });

  console.log('스토리지 상태 저장 완료');

  await browser.close();
}
```

### 스토리지 상태 복원

```javascript
async function loadStorageState() {
  const browser = await chromium.connect({
    wsEndpoint: 'ws://localhost:3000/chromium/playwright'
  });

  // 저장된 상태로 컨텍스트 생성
  const context = await browser.newContext({
    storageState: 'state.json'
  });

  const page = await context.newPage();
  await page.goto('https://example.com/dashboard');

  // 이미 로그인된 상태
  console.log('현재 URL:', page.url());

  await browser.close();
}
```

## Browserless Session API

### 세션 생성

```bash
# 세션 생성
curl -X POST http://localhost:3000/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "ttl": 3600000,
    "stealth": true
  }'
```

응답:
```json
{
  "id": "session-abc123",
  "ttl": 3600000,
  "createdAt": "2024-01-15T10:00:00Z"
}
```

### 세션 사용

```javascript
const puppeteer = require('puppeteer-core');

async function useSession(sessionId) {
  const browser = await puppeteer.connect({
    browserWSEndpoint: `ws://localhost:3000?sessionId=${sessionId}`
  });

  const page = await browser.newPage();
  // 이전 세션 상태 유지됨
  await page.goto('https://example.com/dashboard');

  await browser.close();
}
```

### 세션 관리

```bash
# 세션 목록 조회
curl http://localhost:3000/sessions

# 세션 삭제
curl -X DELETE http://localhost:3000/sessions/session-abc123
```

## Docker 볼륨으로 영구 저장

### 사용자 데이터 디렉토리

```yaml
# docker-compose.yml
version: '3.8'

services:
  browserless:
    image: ghcr.io/browserless/chromium
    ports:
      - "3000:3000"
    volumes:
      - browserless-data:/data
    environment:
      - DATA_DIR=/data

volumes:
  browserless-data:
```

### 데이터 디렉토리 사용

```javascript
const browser = await puppeteer.connect({
  browserWSEndpoint: 'ws://localhost:3000?userDataDir=/data/profile1'
});
```

## 세션 관리 유틸리티

### SessionManager 클래스

```javascript
const fs = require('fs');
const path = require('path');

class SessionManager {
  constructor(sessionDir = './sessions') {
    this.sessionDir = sessionDir;
    if (!fs.existsSync(sessionDir)) {
      fs.mkdirSync(sessionDir, { recursive: true });
    }
  }

  getSessionPath(name) {
    return path.join(this.sessionDir, `${name}.json`);
  }

  async save(page, name) {
    const cookies = await page.cookies();
    const localStorage = await page.evaluate(() => {
      const items = {};
      for (let i = 0; i < window.localStorage.length; i++) {
        const key = window.localStorage.key(i);
        items[key] = window.localStorage.getItem(key);
      }
      return items;
    });

    const session = {
      cookies,
      localStorage,
      savedAt: new Date().toISOString()
    };

    fs.writeFileSync(this.getSessionPath(name), JSON.stringify(session, null, 2));
    console.log(`세션 '${name}' 저장 완료`);
  }

  async load(page, name) {
    const sessionPath = this.getSessionPath(name);

    if (!fs.existsSync(sessionPath)) {
      throw new Error(`세션 '${name}' 을 찾을 수 없습니다`);
    }

    const session = JSON.parse(fs.readFileSync(sessionPath, 'utf8'));

    // 쿠키 복원
    if (session.cookies.length > 0) {
      await page.setCookie(...session.cookies);
    }

    return session;
  }

  async restore(page, name, url) {
    await this.load(page, name);
    await page.goto(url);

    // 로컬 스토리지는 도메인에 접근한 후 복원
    const session = JSON.parse(fs.readFileSync(this.getSessionPath(name), 'utf8'));

    await page.evaluate((items) => {
      for (const [key, value] of Object.entries(items)) {
        window.localStorage.setItem(key, value);
      }
    }, session.localStorage);

    await page.reload();
  }

  exists(name) {
    return fs.existsSync(this.getSessionPath(name));
  }

  delete(name) {
    const sessionPath = this.getSessionPath(name);
    if (fs.existsSync(sessionPath)) {
      fs.unlinkSync(sessionPath);
      console.log(`세션 '${name}' 삭제 완료`);
    }
  }

  list() {
    return fs.readdirSync(this.sessionDir)
      .filter(f => f.endsWith('.json'))
      .map(f => f.replace('.json', ''));
  }
}

module.exports = SessionManager;
```

### 사용 예시

```javascript
const puppeteer = require('puppeteer-core');
const SessionManager = require('./SessionManager');

const sessions = new SessionManager('./sessions');

async function loginAndSave() {
  const browser = await puppeteer.connect({
    browserWSEndpoint: 'ws://localhost:3000'
  });

  const page = await browser.newPage();
  await page.goto('https://example.com/login');

  // 로그인 수행
  await page.type('#username', 'myuser');
  await page.type('#password', 'mypassword');
  await page.click('#login-button');
  await page.waitForNavigation();

  // 세션 저장
  await sessions.save(page, 'example-user');

  await browser.close();
}

async function useSession() {
  const browser = await puppeteer.connect({
    browserWSEndpoint: 'ws://localhost:3000'
  });

  const page = await browser.newPage();

  if (sessions.exists('example-user')) {
    await sessions.restore(page, 'example-user', 'https://example.com/dashboard');
    console.log('세션 복원 완료');
  } else {
    console.log('세션이 없습니다. 로그인이 필요합니다.');
  }

  await browser.close();
}
```

## 세션 만료 처리

### 세션 유효성 검사

```javascript
async function isSessionValid(page) {
  // 로그인 상태를 나타내는 요소 확인
  const userProfile = await page.$('.user-profile');
  const loginButton = await page.$('#login-button');

  return userProfile !== null && loginButton === null;
}

async function ensureLoggedIn(page, loginFn) {
  if (await isSessionValid(page)) {
    console.log('세션 유효');
    return true;
  }

  console.log('세션 만료, 재로그인 필요');
  await loginFn(page);
  return false;
}
```

### 자동 재로그인

```javascript
async function withAutoLogin(page, url, loginFn) {
  await page.goto(url);

  // 로그인 페이지로 리다이렉트되었는지 확인
  if (page.url().includes('/login')) {
    console.log('세션 만료, 재로그인 수행');
    await loginFn(page);
    await page.goto(url);
  }
}
```

## 멀티 계정 관리

### 계정별 세션 분리

```javascript
async function multiAccountScraping() {
  const accounts = [
    { name: 'account1', username: 'user1', password: 'pass1' },
    { name: 'account2', username: 'user2', password: 'pass2' }
  ];

  for (const account of accounts) {
    const browser = await puppeteer.connect({
      browserWSEndpoint: 'ws://localhost:3000'
    });

    const page = await browser.newPage();

    // 계정별 세션 로드 또는 로그인
    if (sessions.exists(account.name)) {
      await sessions.restore(page, account.name, 'https://example.com');
    } else {
      await login(page, account.username, account.password);
      await sessions.save(page, account.name);
    }

    // 작업 수행...

    await browser.close();
  }
}
```

## 보안 고려사항

### 세션 데이터 암호화

```javascript
const crypto = require('crypto');

const ENCRYPTION_KEY = process.env.SESSION_KEY || 'your-32-char-secret-key-here!!';
const IV_LENGTH = 16;

function encrypt(text) {
  const iv = crypto.randomBytes(IV_LENGTH);
  const cipher = crypto.createCipheriv('aes-256-cbc', Buffer.from(ENCRYPTION_KEY), iv);
  let encrypted = cipher.update(text);
  encrypted = Buffer.concat([encrypted, cipher.final()]);
  return iv.toString('hex') + ':' + encrypted.toString('hex');
}

function decrypt(text) {
  const [ivHex, encryptedHex] = text.split(':');
  const iv = Buffer.from(ivHex, 'hex');
  const encrypted = Buffer.from(encryptedHex, 'hex');
  const decipher = crypto.createDecipheriv('aes-256-cbc', Buffer.from(ENCRYPTION_KEY), iv);
  let decrypted = decipher.update(encrypted);
  decrypted = Buffer.concat([decrypted, decipher.final()]);
  return decrypted.toString();
}

// 세션 저장 시 암호화
const sessionData = JSON.stringify({ cookies, localStorage });
const encrypted = encrypt(sessionData);
fs.writeFileSync('session.enc', encrypted);

// 세션 로드 시 복호화
const encrypted = fs.readFileSync('session.enc', 'utf8');
const sessionData = JSON.parse(decrypt(encrypted));
```

## 다음 단계

- [[06-function-api|Function API]] - 커스텀 코드 실행
- [[../05-projects|실전 프로젝트]] - 세션 활용 프로젝트
