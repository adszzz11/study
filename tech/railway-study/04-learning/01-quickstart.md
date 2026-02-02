# Railway Quick Start - 첫 배포

## 개요

이 가이드에서는 GitHub 저장소를 Railway에 연결하여 첫 애플리케이션을 배포합니다.

---

## 사전 준비

### 필요 사항
- [ ] GitHub 계정
- [ ] 배포할 프로젝트 (또는 예제 사용)
- [ ] (선택) Node.js 설치 (CLI 사용 시)

### 지원 환경
Railway는 Nixpacks를 통해 대부분의 언어를 자동 감지합니다:
- Node.js, Python, Go, Ruby, Java, Rust, PHP, .NET 등

---

## 방법 1: 웹 대시보드로 배포

### Step 1: 계정 생성
```
1. https://railway.app 접속
2. "Login" 또는 "Start a New Project" 클릭
3. GitHub 계정으로 로그인
```

### Step 2: 새 프로젝트 생성
```
1. 대시보드에서 "New Project" 클릭
2. "Deploy from GitHub repo" 선택
3. GitHub 저장소 접근 권한 허용
```

### Step 3: 저장소 선택
```
1. 배포할 저장소 검색 및 선택
2. 브랜치 선택 (기본: main)
3. "Deploy Now" 클릭
```

### Step 4: 배포 확인
```
1. 빌드 로그 실시간 확인
2. 배포 완료 후 "Generate Domain" 클릭
3. 생성된 URL로 접속하여 확인
```

---

## 방법 2: CLI로 배포

### Step 1: CLI 설치
```bash
# npm으로 설치
npm install -g @railway/cli

# 또는 curl로 설치
curl -fsSL https://railway.app/install.sh | sh

# 설치 확인
railway --version
```

### Step 2: 로그인
```bash
railway login

# 브라우저가 열리고 인증 완료
```

### Step 3: 프로젝트 초기화
```bash
# 프로젝트 디렉토리로 이동
cd your-project

# 새 프로젝트 생성
railway init

# 또는 기존 프로젝트 연결
railway link
```

### Step 4: 배포
```bash
# 배포 실행
railway up

# 로그 확인
railway logs
```

### Step 5: 도메인 생성
```bash
# 대시보드에서 도메인 생성
railway open

# 또는 CLI로 정보 확인
railway status
```

---

## 예제: Node.js Express 앱

### 프로젝트 구조
```
my-app/
├── package.json
├── index.js
└── .gitignore
```

### package.json
```json
{
  "name": "railway-example",
  "version": "1.0.0",
  "main": "index.js",
  "scripts": {
    "start": "node index.js"
  },
  "dependencies": {
    "express": "^4.18.2"
  }
}
```

### index.js
```javascript
const express = require('express');
const app = express();

// Railway는 PORT 환경변수를 자동 주입
const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.json({
    message: 'Hello from Railway!',
    env: process.env.NODE_ENV || 'development'
  });
});

app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

### 배포
```bash
# GitHub에 푸시
git add .
git commit -m "Initial commit"
git push origin main

# Railway가 자동으로 감지하고 배포 시작
```

---

## 예제: Python Flask 앱

### 프로젝트 구조
```
my-flask-app/
├── requirements.txt
├── app.py
└── .gitignore
```

### requirements.txt
```
flask==3.0.0
gunicorn==21.2.0
```

### app.py
```python
import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({
        'message': 'Hello from Railway!',
        'env': os.environ.get('RAILWAY_ENVIRONMENT', 'development')
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

### Procfile (선택사항)
```
web: gunicorn app:app
```

---

## 배포 확인하기

### 대시보드에서 확인
1. [railway.app](https://railway.app) 접속
2. 프로젝트 선택
3. 서비스 클릭하여 상세 정보 확인

### 확인 항목
| 항목 | 위치 | 설명 |
|------|------|------|
| **빌드 로그** | Deployments > Build Logs | 빌드 과정 확인 |
| **런타임 로그** | Deployments > Deploy Logs | 실행 중 로그 |
| **메트릭** | Metrics 탭 | CPU, 메모리 사용량 |
| **도메인** | Settings > Domains | 접속 URL |

### CLI로 확인
```bash
# 상태 확인
railway status

# 로그 확인 (실시간)
railway logs -f

# 환경 변수 확인
railway variables

# 대시보드 열기
railway open
```

---

## 문제 해결

### 빌드 실패
```bash
# 원인: 언어/프레임워크 감지 실패
# 해결: railway.toml 파일 추가

# railway.toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "npm start"
```

### 포트 문제
```javascript
// 원인: 하드코딩된 포트
// 해결: PORT 환경변수 사용
const PORT = process.env.PORT || 3000;
```

### 접속 불가
```bash
# 체크리스트
1. 도메인이 생성되었는지 확인
2. 서비스가 Running 상태인지 확인
3. 0.0.0.0으로 바인딩했는지 확인
4. 헬스체크 경로 설정 확인
```

---

## 다음 단계

배포가 완료되었다면:
1. [[04-environment|환경 변수 설정]] - 시크릿 관리
2. [[03-databases|데이터베이스 추가]] - PostgreSQL 연결
3. [[05-networking|도메인 설정]] - 커스텀 도메인 연결

---

## 체크리스트

- [ ] Railway 계정 생성
- [ ] GitHub 저장소 연결
- [ ] 첫 배포 성공
- [ ] 도메인으로 접속 확인
- [ ] CLI 설치 (선택)
- [ ] 로그 확인 방법 숙지
