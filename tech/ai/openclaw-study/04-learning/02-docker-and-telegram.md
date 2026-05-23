# 4-2. OpenClaw Docker 셋업 + 텔레그램 봇 연결

> 시간 ~30분. 결과: 텔레그램에서 봇에게 "오늘 일정 알려줘" 했을 때 응답이 돌아옴.

## 📌 핵심 개념

OpenClaw는 두 가지 방식으로 띄울 수 있다:

| 방식 | 장점 | 단점 |
|------|------|------|
| **Docker Compose (권장)** | 환경 격리, 업데이트 쉬움, 보안 ↑ | Docker 자원 추가 사용 |
| npm 글로벌 설치 | 호스트 자원 직접 사용 | 의존성 충돌, 보안 약함 |

**보안 관점**: CVE-2026-44112/44113 같은 sandbox escape이 보고된 상황이라, **Docker로 격리해서 운영**하는 게 사실상 필수.

## 💻 설치 단계

### 1. 텔레그램 봇 만들기

1. 텔레그램에서 [@BotFather](https://t.me/BotFather) 검색 → `/newbot`
2. 봇 이름·username 입력 → **HTTP API token** 받기 (예: `7234567890:AAH...`)
3. (선택) `/setjoingroups`, `/setprivacy`로 그룹 동작 설정

### 2. 작업 디렉터리 + 환경변수

```bash
mkdir -p ~/openclaw && cd ~/openclaw

# 워크스페이스 디렉터리 (에이전트가 파일 다룰 영역)
mkdir -p workspace ./.openclaw/data

cat > .env <<'EOF'
# === LLM Provider (둘 중 하나 이상) ===
ANTHROPIC_API_KEY=sk-ant-xxx
# OPENAI_API_KEY=sk-xxx

# === 로컬 모델 사용 시 ===
# OLLAMA_BASE_URL=http://host.docker.internal:11434

# === 텔레그램 ===
TELEGRAM_BOT_TOKEN=7234567890:AAHxxxxxxxxxxxxxxxxx

# === OpenClaw 기본 ===
OPENCLAW_DEFAULT_MODEL=claude-opus-4-7
OPENCLAW_DATA_DIR=/data
OPENCLAW_WORKSPACE=/workspace
OPENCLAW_TZ=Asia/Seoul
EOF

chmod 600 .env   # 시크릿 보호
```

### 3. docker-compose.yml

```yaml
# ~/openclaw/docker-compose.yml
version: "3.9"

services:
  openclaw:
    image: openclaw/openclaw:latest
    container_name: openclaw
    restart: unless-stopped
    env_file: .env
    ports:
      - "127.0.0.1:8080:8080"   # 관리 UI - 로컬 바인딩만
    volumes:
      - ./.openclaw:/data       # 세션·설정 영속화
      - ./workspace:/workspace  # 에이전트 작업 공간
    networks:
      - openclaw-net
    # 추후 보안 하드닝: 04-remote-and-hardening.md 참고

  # 관리용 CLI 사이드카 (one-shot 실행)
  openclaw-cli:
    image: openclaw/openclaw:latest
    profiles: ["cli"]   # docker compose run으로만 호출
    env_file: .env
    volumes:
      - ./.openclaw:/data
    entrypoint: ["openclaw", "cli"]
    networks:
      - openclaw-net

networks:
  openclaw-net:
    driver: bridge
```

### 4. 기동

```bash
# 이미지 풀 + 컨테이너 기동
docker compose up -d

# 로그 따라가기 (별도 터미널)
docker compose logs -f openclaw
```

로그에 `[telegram] plugin loaded`, `gateway listening on :8080` 같은 줄이 보이면 OK.

### 5. 텔레그램 봇 페어링

OpenClaw는 봇 토큰만으로는 충분하지 않다. **봇과 사용자 본인 계정을 페어링**해야 권한이 부여된다.

```bash
# 봇이 처음에 페어링 코드를 텔레그램으로 보내줌
# 그 코드를 받아서 승인:
docker compose run --rm openclaw-cli pairing approve telegram 123456
```

이후 텔레그램에서 봇과 `/start` → 첫 메시지 보내보기.

### 6. 동작 확인

텔레그램 봇에게:
```
서울 오늘 날씨 알려줘
```

OpenClaw가 내부 browser 도구를 호출해 결과를 텍스트로 답하면 성공.

## ⚙️ 설정 파일 구조

`~/openclaw/.openclaw/config.yaml`에서 더 정밀한 설정 가능:

```yaml
agents:
  default:
    model: claude-opus-4-7
    tools: [browser, files, shell, http]
    skills: [calendar, gmail]

channels:
  telegram:
    enabled: true
    dmPolicy: pairing   # "open"은 누구나 접근 가능 — 권장X
    agent: default

  # 추가 채널은 .env에 토큰 넣고 여기서 enable
  # discord:
  #   enabled: false
  #   agent: default
```

> `dmPolicy: open`은 봇 ID만 알면 누구든 사용 가능 → **절대 안 됨**. 항상 `pairing`.

## ✅ 체크포인트

- [ ] `docker compose ps`에서 openclaw가 `Up (healthy)` 상태
- [ ] `docker compose logs openclaw | grep -i error` → 에러 없음
- [ ] `curl -s http://localhost:8080/health` → 200 OK
- [ ] 텔레그램에서 봇과 첫 페어링 메시지 받음
- [ ] 봇에게 보낸 첫 질문에 답이 옴

## ⚠️ 흔한 실수

| 증상 | 원인 | 해결 |
|------|------|------|
| `Invalid token` 에러 | `.env`에 따옴표 들어감 | 따옴표 없이 `TELEGRAM_BOT_TOKEN=123:abc` |
| 봇이 메시지에 응답 안 함 | `dmPolicy`가 `pairing`인데 페어링 안 함 | `pairing approve` 명령 실행 |
| 그룹에서 봇이 메시지 못 읽음 | BotFather privacy mode ON | `/setprivacy` → Disable |
| 에이전트가 `OPENAI_API_KEY missing` 호소 | 모델 키와 default model 불일치 | `OPENCLAW_DEFAULT_MODEL`을 보유한 키 모델로 |
| host.docker.internal 안 됨 (Linux) | Linux Docker는 기본 미지원 | compose에 `extra_hosts: ["host.docker.internal:host-gateway"]` |
| 페어링 코드 분실 | 봇 메시지 못 받음 | `docker compose logs openclaw | grep pairing` 에 평문 출력됨 |

## 🛡️ 최소 보안 권장

- `.env`는 항상 `chmod 600`
- 포트는 `127.0.0.1:8080`로 바인딩 (외부 접근은 Tailscale로) → [04-remote-and-hardening.md](04-remote-and-hardening.md)
- 봇은 1개 채널 = 1개 에이전트로 분리, 권한 최소화
- Docker 이미지는 specific tag로 핀(`openclaw:1.x.y`) — `latest`는 사고 위험

## 🔗 다음 단계

- 로컬 모델로 비용 0원 운영 → [03-local-llm-ollama.md](03-local-llm-ollama.md)
- 외부 접속 + 하드닝 → [04-remote-and-hardening.md](04-remote-and-hardening.md)

## 참고

- [aifreeapi: From Zero to Personal AI Bot in 15 Minutes](https://www.aifreeapi.com/en/posts/openclaw-telegram-setup)
- [Simon Willison: Running OpenClaw in Docker](https://til.simonwillison.net/llms/openclaw-docker)
