# OpenClaw 심층 스터디

> 메신저로 말 걸면 답하는, 내 손에서 돌아가는 개인 AI 비서

## 한 줄 정의

**OpenClaw**는 로컬·자가 호스팅 환경에서 동작하는 오픈소스 개인 AI 에이전트 프레임워크다. WhatsApp/Telegram/Slack/Discord 등 **20+ 메신저 채널**을 단일 게이트웨이로 묶고, 브라우저·터미널·캘린더·이메일 같은 **로컬 도구**를 LLM이 직접 호출하도록 설계됐다.

## 3줄 요약

1. **로컬 우선(Local-first)**: 모든 세션·시크릿·작업 파일이 내 머신에 저장. 클라우드 종속 없음.
2. **Multi-channel 게이트웨이**: 20+ 메신저를 단일 inbox로 묶고, 채널별로 격리된 에이전트로 라우팅 가능.
3. **모델 비종속**: OpenAI, Claude, Gemini, Ollama 로컬 모델까지 모두 백엔드로 끼울 수 있음.

## 핵심 키워드

`#self-hosted-ai` `#personal-assistant` `#agent-framework` `#mcp` `#tool-calling` `#messenger-bot` `#local-llm` `#typescript` `#docker` `#mac-mini-server`

## ⚡ Quick Start (Mac mini 기준 5분 체험)

```bash
# 1. 작업 디렉터리 준비
mkdir -p ~/openclaw && cd ~/openclaw

# 2. Docker compose 설정 다운로드 (공식 docker-setup.sh 활용)
curl -fsSL https://openclaw.com/install/docker.sh | bash

# 3. .env에 LLM 키 + 기본 채널 설정
cat > .env <<'EOF'
ANTHROPIC_API_KEY=sk-ant-xxx
TELEGRAM_BOT_TOKEN=123:abc
OPENCLAW_DEFAULT_MODEL=claude-opus-4-7
EOF

# 4. 기동
docker compose up -d

# 5. 텔레그램에서 봇과 페어링 코드 입력
docker compose run --rm openclaw-cli pairing approve telegram <CODE>
```

> 진짜 첫 메시지: 텔레그램 봇에게 `"오늘 날씨"` 물어보면 OpenClaw가 브라우저 도구를 호출해 답한다.

## 📑 전체 목차

| 파일 | 내용 |
|------|------|
| [01-overview.md](01-overview.md) | OpenClaw가 뭐고 왜 쓰는지 — 아키텍처·핵심 기능·장단점·채택 사례 |
| [02-ecosystem.md](02-ecosystem.md) | 같은 카테고리(자가호스팅 AI 비서) 비교 — Hermes, Letta, Nanobot, ZeroClaw, OpenInterpreter, Khoj, memU |
| [03-references.md](03-references.md) | 공식 문서·튜토리얼·커뮤니티·오픈소스 예제 모음 |
| [04-learning/01-mac-mini-setup.md](04-learning/01-mac-mini-setup.md) | Mac mini를 24/7 AI 서버로: 사양 선택, 슬립 끄기, Docker 준비 |
| [04-learning/02-docker-and-telegram.md](04-learning/02-docker-and-telegram.md) | Docker Compose로 OpenClaw 띄우고 텔레그램 봇 페어링까지 |
| [04-learning/03-local-llm-ollama.md](04-learning/03-local-llm-ollama.md) | Ollama로 Llama 3.x · Gemma를 로컬에서 돌려 OpenClaw 백엔드로 사용 |
| [04-learning/04-remote-and-hardening.md](04-learning/04-remote-and-hardening.md) | Tailscale/Cloudflare Tunnel로 외부 접속 + 보안 하드닝 (CVE-2026-44112 회피) |
| [05-projects.md](05-projects.md) | 실전 프로젝트 5종 (개인 비서, 회의록 요약, 홈 모니터링 봇 등) |
| [cheatsheet.md](cheatsheet.md) | docker/openclaw/ollama 자주 쓰는 명령어 빠른 참조 |

## 🗓️ 학습 플랜

| 일차 | 목표 | 문서 |
|------|------|------|
| Day 1 | OpenClaw 개념 잡기 + 카테고리 지형도 | 01-overview, 02-ecosystem |
| Day 2 | Mac mini 준비 + Docker 셋업 + 텔레그램 봇 한 개 띄우기 | 04-learning/01, 02 |
| Day 3 | Ollama 로컬 모델 연결, Claude 백엔드와 라우팅 비교 | 04-learning/03 |
| Day 4 | Tailscale 외부접속 + 보안 하드닝 + 자동 재시작 (launchd) | 04-learning/04 |
| Day 5 | 실전 프로젝트 1개 완성 (예: 일일 브리핑 봇) | 05-projects |

## ⚠️ 시작 전 알아둘 점

- **OpenClaw는 2026년 폭발적으로 성장한 만큼 보안 이슈도 함께 등장**했다. CVE-2026-25253, Claw Chain(CVE-2026-44112/44113) 등 sandbox escape 취약점이 보고됐고, Simon Willison이 말한 "lethal trifecta"(사적 데이터 + 외부 콘텐츠 + 외부 통신) 조건을 그대로 만족함. **반드시 [04-learning/04-remote-and-hardening.md](04-learning/04-remote-and-hardening.md) 먼저 읽고 격리 환경에서 운영**할 것.
- 단순함을 원하면 **Nanobot**(Python 4,000 라인)이나 **ZeroClaw**(Rust 단일 바이너리)를 먼저 검토.
- 장기 기억이 핵심이면 **Letta/memU**가 더 적합 — [02-ecosystem.md](02-ecosystem.md) 비교 표 참고.
