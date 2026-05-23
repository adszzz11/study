# 4-4. 외부 접속 + 보안 하드닝

> 시간 ~40분. 결과: 카페에서도 텔레그램 봇이 동작하고, "Claw Chain" 같은 sandbox escape에도 호스트가 안 털림.

## 📌 핵심 개념: 두 가지 위험을 분리해서 다룬다

| 위험 | 어디서 옴 | 대응 |
|------|----------|------|
| **외부 노출 위험** | Mac mini를 인터넷에 띄우는 행위 자체 | Tailscale로 직접 노출 회피 |
| **에이전트 폭주 위험** | OpenClaw가 host 권한으로 동작 → 프롬프트 인젝션 시 ⚠️ | 컨테이너 격리, 권한 최소화 |

## 🌐 Part A. 외부 접속 — Tailscale 권장

### 왜 Tailscale인가

| 옵션 | 평가 |
|------|------|
| **Tailscale** (WireGuard mesh VPN) | ⭐⭐⭐⭐⭐ 무료, 포트포워딩 X, 종단간 암호화 |
| Cloudflare Tunnel | ⭐⭐⭐⭐ 무료, 공개 URL 필요할 때 |
| Public SSH + 포트포워딩 | ⭐ 위험. 절대 비추 |
| ngrok 무료 | ⭐⭐ URL이 매번 바뀜, 데모용 |

**텔레그램 봇은 Tailscale 없어도 동작한다** (텔레그램이 봇에 outbound로 push). Tailscale은 **관리 UI(8080)나 Ollama(11434)에 외부에서 접근하고 싶을 때** 필요.

### Tailscale 셋업

```bash
# Mac mini에 설치
brew install --cask tailscale

# 로그인 (브라우저 열림)
open /Applications/Tailscale.app

# 또는 CLI:
sudo tailscaled install-system-daemon
sudo tailscale up --advertise-tags=tag:server
```

설치 후 [admin 콘솔](https://login.tailscale.com/admin/machines)에서 Mac mini 확인. **MagicDNS** 켜면 `mac-mini.tail-XXXX.ts.net` 같은 호스트네임으로 접근 가능.

### 폰/노트북에서도 Tailscale 설치

같은 계정으로 로그인 → 즉시 같은 tailnet. 폰에서 `http://mac-mini.tail-XXXX.ts.net:8080` 접근 가능.

### Ollama Tailnet 전용 바인딩

```bash
# Tailscale 인터페이스만 바인딩 (가장 안전)
launchctl setenv OLLAMA_HOST "100.x.x.x:11434"   # Tailscale에서 받은 IP

# 또는 0.0.0.0 바인딩 + Mac 방화벽에서 Tailscale 외 차단
```

### Cloudflare Tunnel (공개 URL이 필요할 때)

OpenClaw 관리 UI를 공개해야 하는 케이스 (예: 외부 webhook 받기) — Cloudflare Tunnel 사용:

```bash
brew install cloudflared

# 인증
cloudflared tunnel login

# 터널 생성
cloudflared tunnel create openclaw-mac

# config.yml
mkdir -p ~/.cloudflared
cat > ~/.cloudflared/config.yml <<EOF
tunnel: <tunnel-id>
credentials-file: ~/.cloudflared/<tunnel-id>.json
ingress:
  - hostname: openclaw.example.com
    service: http://localhost:8080
  - service: http_status:404
EOF

# DNS 등록
cloudflared tunnel route dns openclaw-mac openclaw.example.com

# 데몬 실행
cloudflared tunnel run openclaw-mac &
```

> **Cloudflare Access**로 SSO/이메일 OTP를 앞에 붙이면 인증된 사용자만 접근하게 할 수 있다. 권장.

## 🔒 Part B. 에이전트 보안 하드닝

> CVE-2026-25253, CVE-2026-44112/44113, "Claw Chain" 사건들의 공통점: **에이전트가 호스트 권한으로 실행 → 프롬프트 인젝션이 시스템 침해로 직결**. 다음 가드를 모두 적용하라.

### 1. 컨테이너 격리 강화 (docker-compose 보강)

```yaml
services:
  openclaw:
    image: openclaw/openclaw:1.x.y   # latest 금지
    restart: unless-stopped
    env_file: .env
    ports:
      - "127.0.0.1:8080:8080"        # localhost 바인딩만
    volumes:
      - ./.openclaw:/data
      - ./workspace:/workspace
    read_only: true                  # 루트 FS 읽기 전용
    tmpfs:
      - /tmp                         # tmpfs로만 쓰기 허용
    cap_drop:
      - ALL                          # 모든 capability 제거
    cap_add:
      - NET_BIND_SERVICE             # 필요한 것만 다시 부여
    security_opt:
      - no-new-privileges:true       # setuid 차단
      - seccomp:default
    mem_limit: 4g
    cpus: "2.0"
    networks:
      openclaw-net:
        aliases: [openclaw]
    user: "1000:1000"                # non-root
```

### 2. 도구 권한 최소화 (skills allowlist)

`config.yaml`에서 명시적 허용 목록:

```yaml
agents:
  default:
    tools_allowlist:
      - browser     # 헤드리스, 별도 컨테이너 권장
      - http_get    # GET만, POST 차단
      - files_read  # 읽기 전용
      - calendar_read
    tools_blocklist:
      - shell       # 절대 쓰지 마라
      - files_write_root
      - email_send  # 봇이 메일 마음대로 보내는 사고 방지
    require_confirmation:
      - files_write
      - email_send
      - http_post
```

### 3. 시크릿 분리

- `.env`는 절대 git에 넣지 말 것 (`echo .env >> .gitignore`)
- 추가 보안: `pass`(GPG) / 1Password CLI로 시크릿 주입
- API 키는 **사용량 한도 설정** (Anthropic Console / OpenAI Usage Limits)

### 4. 채널 권한

- `dmPolicy: pairing` 강제 (절대 `open` 금지)
- 텔레그램 봇 — `/setjoingroups` Disabled
- 슬랙 — 봇이 자동으로 채널 가입 안 하게 OAuth scope 최소

### 5. 모니터링

```bash
# 컨테이너 로그 토큰 누출 스캔 (cron으로)
docker compose logs --since 24h openclaw | \
  grep -E 'sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{20,}' \
  && cmux notify --title "⚠️ Secret leak in logs!"

# 부팅 시 OpenClaw 이미지 해시 검증
docker image inspect openclaw/openclaw:1.x.y --format '{{.Id}}' \
  | tee -a ~/openclaw/audit/images.log
```

추천 도구: [openclaw-security-monitor](https://github.com/adibirzu/openclaw-security-monitor) — Claw Chain, AMOS stealer, memory poisoning 패턴 감지.

### 6. 정기 업데이트 / 패치

```bash
# 주 1회 (cron 또는 launchd로 자동화 가능)
cd ~/openclaw
docker compose pull
docker compose up -d
docker image prune -f

# 보안 권고 RSS 구독:
# https://github.com/openclaw/openclaw/security/advisories
```

## 🚦 "Lethal Trifecta" 차단 체크리스트

Simon Willison의 lethal trifecta = (1) 사적 데이터 + (2) 외부 입력 + (3) 외부 통신. 셋 중 **하나라도 끊으면** 위험이 격감.

- [ ] (외부 입력 제한) `dmPolicy: pairing` + 페어링된 ID만 허용
- [ ] (외부 통신 제한) `tools_blocklist`에 `email_send`, `http_post` 포함 또는 confirmation 필수
- [ ] (사적 데이터 격리) 에이전트가 `~/Documents` 같은 영역 마운트 금지. 별도 `workspace/` 디렉터리만
- [ ] (감사 로그) 모든 tool 호출 로그 보관, 30일 이상

## ✅ 검증

```bash
# 1. 외부 노출 안 됐는지 확인 (외부 망에서)
curl -m 5 http://공인IP:8080  # → 연결 실패가 정상

# 2. Tailnet에서는 동작
curl http://mac-mini.tail-XXXX.ts.net:8080/health  # → 200

# 3. 컨테이너 권한 확인
docker compose exec openclaw cat /proc/self/status | grep CapEff
# CapEff: 0000000000000400 (NET_BIND_SERVICE만) 같은 결과 = OK

# 4. 시크릿이 컨테이너 환경에 잘 격리되어 있는지
docker compose exec openclaw env | grep -E 'KEY|TOKEN'
# 호스트 env에는 없고 컨테이너에만 있어야 OK
```

## ⚠️ 절대 하지 말 것

| 안 됨 | 이유 |
|-------|------|
| Mac mini를 공유기 DMZ에 두기 | OpenClaw + macOS + Docker 전체가 인터넷에 노출 |
| `dmPolicy: open` | 봇 ID만 알면 누구든 명령 가능 |
| `shell` tool을 default agent에 허용 | 프롬프트 인젝션 → 시스템 명령 실행 |
| `latest` 태그 사용 | 자동 업데이트로 breaking change/취약점 함께 들어옴 |
| `.env`를 git에 push | API 키 즉시 폐기 + abuse 청구 위험 |
| FileVault OFF + 외부 접근 허용 | 디스크 도난 시 시크릿 평문 노출 |

## 🔗 더 알아보기

- [Conscia: The OpenClaw security crisis](https://conscia.com/blog/the-openclaw-security-crisis/)
- [Adversa AI: OpenClaw security 101 — hardening guide](https://adversa.ai/blog/openclaw-security-101-vulnerabilities-hardening-2026/)
- [The Hacker News: Four OpenClaw Flaws (Claw Chain)](https://thehackernews.com/2026/05/four-openclaw-flaws-enable-data-theft.html)
- [Tailscale + Mac mini guide](https://www.mager.co/blog/2026-02-22-openclaw-mac-mini-tailscale/)
- [VPSMAC: Tailscale vs Cloudflare Tunnel vs Public SSH (2026)](https://vpsmac.com/en/blog/mac-cloud-zero-trust-tailscale-cloudflare-tunnel-ssh-2026.html)

## 다음 단계

→ 안전한 상태가 되었으면 [05-projects.md](../05-projects.md) 에서 실전 프로젝트로
