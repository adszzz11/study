# Cheat Sheet — 자주 쓰는 명령어 빠른 참조

## 🐳 Docker / OpenClaw

```bash
# 기동·중지
cd ~/openclaw && docker compose up -d
docker compose down                      # 컨테이너 중지+제거 (볼륨 유지)
docker compose restart openclaw

# 로그
docker compose logs -f openclaw
docker compose logs --since 1h openclaw | grep ERROR
docker compose logs openclaw | grep pairing   # 페어링 코드 찾기

# 상태 확인
docker compose ps
docker stats openclaw                    # 실시간 CPU/메모리

# CLI 실행 (one-shot)
docker compose run --rm openclaw-cli pairing approve telegram 123456
docker compose run --rm openclaw-cli agent test default "Hello"
docker compose run --rm openclaw-cli skills list
docker compose run --rm openclaw-cli skills install <name>

# 업데이트
docker compose pull && docker compose up -d
docker image prune -f
```

## 🦙 Ollama

```bash
# 서비스 관리
brew services start ollama
brew services restart ollama
brew services stop ollama

# 모델 관리
ollama list
ollama pull qwen2.5:14b
ollama rm llama2:7b
ollama ps                                # 로드된 모델 + 메모리

# 동작 확인
ollama run llama3.2:8b "한 줄로 자기소개"
curl http://localhost:11434/api/tags | jq .
curl http://localhost:11434/api/generate -d '{"model":"llama3.2:8b","prompt":"hi","stream":false}'

# 환경변수
launchctl setenv OLLAMA_HOST "0.0.0.0:11434"
launchctl getenv OLLAMA_HOST
```

## 🌐 Tailscale

```bash
# 시작·로그인
sudo tailscale up
tailscale status
tailscale ip -4                          # 내 tail IP

# MagicDNS 호스트네임
tailscale dns status

# 노드 끄기 (휴가 갈 때)
sudo tailscale down

# SSH
ssh user@mac-mini.tail-XXXX.ts.net
```

## ⚡ macOS 시스템

```bash
# 슬립 / 절전
pmset -g                                 # 현재 설정
sudo pmset -a sleep 0                    # 슬립 OFF
sudo pmset -a autorestart 1              # 정전 후 자동 복귀
caffeinate -dimsu &                      # 임시 슬립 방지

# 시스템 자원
btop                                     # top 대체
sudo powermetrics --samplers gpu_power -i 1000  # GPU 사용량

# launchd
launchctl list | grep openclaw
launchctl load ~/Library/LaunchAgents/com.user.openclaw.plist
launchctl unload ~/Library/LaunchAgents/com.user.openclaw.plist
```

## 🤖 텔레그램 봇 운영

```bash
# 봇 토큰 검증
curl https://api.telegram.org/bot<TOKEN>/getMe | jq .

# 봇 알림 발송 (테스트)
curl -s "https://api.telegram.org/bot<TOKEN>/sendMessage" \
  -d "chat_id=<MY_CHAT_ID>" \
  -d "text=Hello from CLI"

# 내 chat_id 확인
# 1. 봇에 메시지 한 통 보낸 후:
curl "https://api.telegram.org/bot<TOKEN>/getUpdates" | jq '.result[].message.chat.id'
```

## ☁️ Cloudflare Tunnel

```bash
# 인증·생성·실행
cloudflared tunnel login
cloudflared tunnel create openclaw-mac
cloudflared tunnel route dns openclaw-mac openclaw.example.com
cloudflared tunnel run openclaw-mac

# 상태
cloudflared tunnel list
cloudflared tunnel info openclaw-mac
```

## 🔍 OpenClaw 설정 파일 위치

| 위치 | 용도 |
|------|------|
| `~/openclaw/docker-compose.yml` | 컨테이너 설정 |
| `~/openclaw/.env` | 시크릿 (chmod 600) |
| `~/openclaw/.openclaw/config.yaml` | 에이전트/채널/cron 설정 |
| `~/openclaw/.openclaw/data/` | 세션·상태 영속화 |
| `~/openclaw/workspace/` | 에이전트가 다루는 파일 |

## 🛡️ 보안 확인

```bash
# .env 권한
ls -l ~/openclaw/.env                    # -rw------- 인지

# 외부 노출 점검
curl -m 5 http://<공인IP>:8080           # → 실패해야 정상
nmap -p 8080 <공인IP>                    # → closed/filtered 기대

# 시크릿 로그 누출 스캔
docker compose logs --since 24h openclaw | \
  grep -E 'sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{20,}|xoxb-[a-zA-Z0-9]{20,}'

# 컨테이너 권한
docker compose exec openclaw cat /proc/self/status | grep CapEff
```

## 📊 로그 분석 한 줄 트릭

```bash
# 가장 많이 호출된 도구
docker compose logs openclaw --since 24h | grep "tool_call" | \
  awk '{print $5}' | sort | uniq -c | sort -rn | head

# 응답 시간 분포
docker compose logs openclaw --since 24h | grep "response_ms" | \
  awk '{print $NF}' | sort -n | awk '
    BEGIN{c=0} {a[c++]=$1} 
    END{print "p50:", a[int(c*0.5)], "p95:", a[int(c*0.95)]}'

# 오류 빈도
docker compose logs openclaw --since 24h | grep -c ERROR
```

## 🔗 빠른 링크

- 본 vault 내 OpenClaw study: `study/tech/ai/openclaw-study/`
- 관련 카테고리: [[study/tech/ai/agent-orchestration]], [[study/tech/ai/claude]]
- 공식: https://github.com/openclaw/openclaw
- Awesome: https://github.com/mergisi/awesome-openclaw-agents
- 보안 모니터링: https://github.com/adibirzu/openclaw-security-monitor
