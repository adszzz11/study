# 4-1. Paperclip 셋업 + 첫 회사 만들기

> 시간 ~20분. 결과: 대시보드 접속 + 회사 1개 + 직원 0명.

## 📌 핵심 개념

- Paperclip은 **단일 Node.js 프로세스 + Postgres**로 동작 (메시지 큐, Redis 불필요)
- 회사(Company)가 1급 객체 — 멀티 테넌트 가능
- 첫 셋업 = `npx paperclipai onboard` 한 줄

## 💻 셋업 (Mac mini 기준)

### 1. 사전 조건

```bash
# Node 20+ 확인
node -v  # v20.x.x 이상

# pnpm 설치
brew install pnpm
pnpm -v   # 9.15+ 필요

# Postgres (옵션 1: 로컬 Homebrew)
brew install postgresql@16
brew services start postgresql@16

# Postgres (옵션 2: Docker)
docker run -d --name paperclip-pg \
  -e POSTGRES_PASSWORD=paperclip \
  -e POSTGRES_DB=paperclip \
  -p 5432:5432 -v paperclip_pg:/var/lib/postgresql/data \
  postgres:16
```

> SQLite로도 시작 가능하지만 운영은 Postgres 권장 (큐 동시성·잠금 정확함).

### 2. 인터랙티브 부트스트랩

```bash
mkdir -p ~/paperclip && cd ~/paperclip
npx paperclipai onboard --yes
```

이 명령이 자동으로:
- DB 마이그레이션
- 첫 회사 생성 프롬프트
- admin 계정 생성
- `.env` 작성
- dev 서버 기동 (`http://localhost:3000`)

### 3. 수동 셋업 (선호 시)

```bash
git clone https://github.com/paperclipai/paperclip.git
cd paperclip
pnpm install

cp .env.example .env
# .env 편집:
#   DATABASE_URL=postgresql://paperclip:paperclip@localhost:5432/paperclip
#   ADMIN_EMAIL=you@example.com
#   ADMIN_PASSWORD=...

pnpm db:migrate
pnpm db:seed   # (선택) 샘플 데이터
pnpm dev
```

### 4. 첫 회사 만들기

대시보드 `/companies/new`에서:

```yaml
Company Name: Home OS
Description: Mac mini 자치 운영
Default LLM: claude-opus-4-7
Monthly Budget: $100
Timezone: Asia/Seoul
```

생성 후 회사 대시보드로 자동 이동.

### 5. 동작 확인

```bash
# 헬스체크
curl http://localhost:3000/api/health

# 회사 목록
curl http://localhost:3000/api/companies \
  -H "Authorization: Bearer <ADMIN_TOKEN>"
```

## ✅ 체크포인트

- [ ] `http://localhost:3000` 대시보드 보임
- [ ] admin 계정으로 로그인 가능
- [ ] "Home OS" 회사 생성됨
- [ ] `pnpm db:status` 마이그레이션 완료
- [ ] Postgres 연결 정상 (`psql paperclip -c '\dt'`로 테이블 확인)

## ⚠️ 흔한 실수

| 증상 | 원인·해결 |
|------|----------|
| Node 18에서 안 됨 | Node 20+ 필요. `brew install node@20` |
| Postgres 연결 거부 | `pg_isready` 확인. Docker라면 `5432` 포트 확인 |
| 마이그레이션 실패 | 권한 부족. DB 사용자에 `CREATEDB` 권한 부여 |
| `npx onboard` 멈춤 | Postgres 안 떠 있음. 먼저 띄우고 재실행 |
| ADMIN_TOKEN 어디? | 대시보드 `/settings/api-keys`에서 발급 |
| 한글이 깨짐 | Postgres `LC_CTYPE` UTF-8 확인 |

## 🛡️ 첫 단계부터 챙길 보안

```bash
# 포트 외부 노출 방지 (Tailscale 안에서만)
# .env에:
HOST=127.0.0.1   # 또는 Tailnet IP

# 시크릿 권한
chmod 600 .env
```

## 🔌 launchd 자동 시작 (선택)

```bash
# ~/Library/LaunchAgents/com.user.paperclip.plist 만들고
launchctl load ~/Library/LaunchAgents/com.user.paperclip.plist
```

`com.user.openclaw.plist` 패턴과 동일 (참고: [[study/tech/ai/openclaw-study/04-learning/01-mac-mini-setup]]).

## 🔗 다음

→ 직원 채용 → [02-hiring-agents.md](02-hiring-agents.md)
