# 4-1. Mac mini를 24/7 AI 서버로 준비하기

> 시간 ~30분. 결과: 슬립 안 들어가고, 부팅 시 자동 로그인, Homebrew + Docker + 기본 모니터링까지 갖춘 Mac mini.

## 📌 핵심 개념

Mac mini를 AI 서버로 쓰는 이유:
- **15W idle / 30W load** → 24/7 운영해도 월 전기료 $3-5 (한국 환경 약 5,000-8,000원)
- **통합 메모리(Unified Memory)** → CPU/GPU가 동일 RAM 풀 공유 → LLM 추론 시 데이터 복사 비용 0
- **무팬 / 저소음** → 거실에 놓아도 됨
- **macOS 위에 직접** → Docker Desktop · OrbStack · Homebrew 다 그대로 동작

## 🛒 사양 선택 가이드

| 모델 | 메모리 | 추천 용도 | 가격대 |
|------|--------|----------|--------|
| M4 16GB | 16GB | 7B Q4 모델까지 / 메신저 봇 단독 | 보급 |
| M4 24GB | 24GB | 7-14B Q4 / OpenClaw + 가벼운 Ollama | ⭐ 가성비 |
| M4 32GB | 32GB | 14B 풀 / OpenClaw + 멀티 에이전트 | 안정 |
| **M4 Pro 48GB** | 48GB | 32B Q4 / Llama 3.3 70B Q3까지 | ⭐⭐ 추천 |
| M4 Pro 64GB | 64GB | 70B Q4 / 동시 멀티 모델 | 풍요 |

### 토큰/초 기준 (참고)

| 모델 | M4 16GB | M4 Pro 24GB | M4 Pro 48GB |
|------|---------|-------------|-------------|
| 7B Q4 | 25-35 t/s | 60-80 t/s | 70-90 t/s |
| 14B Q4 | 부족 | 35-50 t/s | 40-55 t/s |
| 32B Q4 | 불가 | 빠듯 | 15-22 t/s |
| 70B Q3 | 불가 | 불가 | 5-8 t/s |

## 💻 셋업 단계

### 1. macOS 초기 설정

```bash
# 시스템 업데이트 확인
softwareupdate --install --all
```

System Settings에서 처리:
- **Energy Saver**
  - Prevent automatic sleeping: ON
  - Start up automatically after power failure: ON
  - Wake for network access: ON
- **Users & Groups → Login Items**
  - 자동 로그인 ON (디스크 암호화 해제 후 사용 시)
- **Sharing**
  - Remote Login (SSH) ON — 추후 헤드리스 운영용

### 2. CLI에서 슬립 강제 해제

```bash
# 디스플레이 슬립만 끄고 시스템은 깨어 있게
sudo pmset -a sleep 0
sudo pmset -a displaysleep 10
sudo pmset -a disksleep 0

# 현재 설정 확인
pmset -g

# 부팅 후 자동 복귀
sudo pmset -a autorestart 1
```

### 3. Homebrew 설치

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Apple Silicon용 PATH 설정 (zsh 기준, 이미 되어있으면 스킵)
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
source ~/.zprofile
```

### 4. 필수 패키지

```bash
# 컨테이너 런타임
brew install --cask orbstack   # Docker Desktop보다 가볍고 빠름 (추천)
# 또는
# brew install --cask docker

# 유틸
brew install git jq yq htop wget curl gh
brew install --cask iterm2

# 로컬 LLM
brew install ollama
```

> **OrbStack 추천 이유**: Docker Desktop보다 메모리 50% 적게 쓰고, 부팅 빠르고, Volumes I/O 빠름. macOS 전용.

### 5. Ollama 데몬 띄우기

```bash
# 서비스로 등록 (백그라운드 상시 실행)
brew services start ollama

# 모델 다운로드 (한 번에 4-5GB)
ollama pull llama3.2:8b
ollama pull qwen2.5:14b

# 동작 확인
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:8b",
  "prompt": "Hello",
  "stream": false
}' | jq .
```

### 6. 기본 모니터링 (선택)

```bash
# 시스템 자원 실시간 확인
brew install btop
btop

# GPU/Neural Engine 사용량
sudo powermetrics --samplers gpu_power -i 1000
```

## ✅ 체크포인트

- [ ] `pmset -g | grep sleep` 했을 때 `sleep 0`인가?
- [ ] 노트북 덮어도 (또는 모니터 꺼도) `ssh user@mac-mini` 들어가지는가?
- [ ] `docker ps`나 `orb status`가 정상 응답하나?
- [ ] `curl http://localhost:11434/api/tags` 가 모델 리스트 반환하나?
- [ ] 재부팅 후 자동 로그인되고 Ollama 자동 시작되나?

## ⚠️ 흔한 실수

| 실수 | 해결 |
|------|------|
| `pmset` 설정했는데도 슬립 들어감 | "Prevent automatic sleeping" 체크 다시 확인. `caffeinate -dimsu` 백그라운드 실행으로 강제도 가능 |
| Ollama가 외부에서 접근 안 됨 | 기본은 `127.0.0.1`만 바인딩. `OLLAMA_HOST=0.0.0.0:11434 brew services restart ollama` 또는 `~/Library/LaunchAgents` plist 수정 |
| OrbStack에서 컨테이너 IP가 host와 다름 | `host.docker.internal`로 호스트 접근. Ollama가 host에서 돈다면 컨테이너에서 `http://host.docker.internal:11434` |
| FileVault + 자동 로그인 충돌 | FileVault 켜져 있으면 부팅 후 첫 로그인 수동 필요. AI 서버 전용이면 FileVault OFF 고려 |
| 디스크 용량 부족 | 14B 모델 1개당 8-10GB. 256GB SSD면 모델 3-4개가 한계. `ollama rm <model>`로 정리 |

## 🔌 자동 시작 패턴

macOS는 launchd로 부팅 시 데몬 실행. Docker Compose 스택을 자동 시작하려면:

```bash
# ~/Library/LaunchAgents/com.user.openclaw.plist
cat > ~/Library/LaunchAgents/com.user.openclaw.plist <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key><string>com.user.openclaw</string>
    <key>WorkingDirectory</key><string>/Users/USERNAME/openclaw</string>
    <key>ProgramArguments</key>
    <array>
        <string>/opt/homebrew/bin/docker</string>
        <string>compose</string><string>up</string><string>-d</string>
    </array>
    <key>RunAtLoad</key><true/>
    <key>KeepAlive</key><false/>
    <key>StandardOutPath</key><string>/tmp/openclaw.log</string>
    <key>StandardErrorPath</key><string>/tmp/openclaw.err</string>
</dict>
</plist>
EOF

# USERNAME 치환 후 로드
launchctl load ~/Library/LaunchAgents/com.user.openclaw.plist
```

## 🔗 더 알아보기

- [Energy Saver / pmset 옵션 전체](https://ss64.com/osx/pmset.html)
- [OrbStack 공식 문서](https://docs.orbstack.dev/)
- [launchd 가이드](https://www.launchd.info/)

## 다음 단계

→ [02-docker-and-telegram.md](02-docker-and-telegram.md) Docker Compose로 OpenClaw 띄우고 텔레그램 봇 페어링
