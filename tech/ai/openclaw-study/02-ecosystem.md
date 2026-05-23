# Part 2. 생태계 — OpenClaw같은 프로젝트들

> "OpenClaw 같은 거"라고 두루뭉술하게 말해도, 안에는 **5가지 다른 갈래**가 섞여 있다. 이 챕터에서 그 갈래를 정리한다.

## 🗺️ 카테고리 지도

```
자가호스팅 개인 AI 에이전트
│
├─ A. 메신저 게이트웨이형 (OpenClaw 스타일)
│   └─ OpenClaw, Hermes, Nanobot, ZeroClaw
│
├─ B. 장기 기억 중심형
│   └─ Letta(MemGPT), memU, LettaBot
│
├─ C. 코드/터미널 실행 중심형
│   └─ Open Interpreter, Aider, OpenDevin
│
├─ D. 개인 지식 검색형 (Personal RAG)
│   └─ Khoj, Reor, AnythingLLM
│
└─ E. 워크플로우/노드 기반형
    └─ n8n + AI, Flowise, Activepieces
```

## 🆚 핵심 비교 표

| 프로젝트 | 카테고리 | 코드 크기 | 메모리 | 보안 모델 | 핵심 특징 | 적합 사용처 |
|---------|---------|----------|--------|----------|----------|------------|
| **OpenClaw** | A | 430k LOC, TS | ~512MB+ | Host 직접 실행 | 20+ 메신저, 모델 자유 | 멀티채널 만능 봇 |
| **Hermes** | A | TS/Python | ~300MB | 컨테이너 sandbox | 보안 강화판 OpenClaw fork 계열 | 보안 민감 환경 |
| **Nanobot** | A | 4k LOC, Python | <100MB | 가벼움 | HKU 발 OpenClaw 라이트 99% 축소 | 가벼움 우선 |
| **ZeroClaw** | A | Rust 단일 바이너리 | **<5MB** | 정적 컴파일 | 10ms 부팅, 임베디드 가능 | 라즈베리파이/임베디드 |
| **NanoClaw** | A | Python+컨테이너 | 격리 | 강제 컨테이너 격리 | "탈출해도 샌드박스만 죽음" | 보안 + 단순함 |
| **Letta** (구 MemGPT) | B | Python | ~500MB | API/Self-host | 영속 메모리, 에이전트 상태 DB | 장기 기억 비서 |
| **memU** | B | Python | - | API | 사용자 지식 그래프 자동 구축 | "나를 아는" PA |
| **Open Interpreter** | C | Python | ~300MB | 로컬 실행 | "ChatGPT가 내 PC를 조작" | 코드 실행 우선 |
| **Khoj** | D | Python | ~400MB | Self-host | 노트·이메일·문서 RAG + 채팅 | 개인 지식 검색 |
| **AnythingLLM** | D | JS+Python | ~600MB | Docker | 멀티 워크스페이스 RAG | 팀/문서 챗봇 |

## 🔍 같은 카테고리 A 안에서의 차이 (메신저 게이트웨이형)

### OpenClaw vs Nanobot vs ZeroClaw vs NanoClaw

| 축 | OpenClaw | Nanobot | ZeroClaw | NanoClaw |
|----|----------|---------|----------|----------|
| **철학** | "기능 최대" | "코드 4천줄로 본질만" | "리소스 최소화" | "보안 우선" |
| **언어** | TypeScript | Python | Rust | Python |
| **메모리 사용** | 512MB+ | <100MB | **<5MB** | 컨테이너당 |
| **부팅 시간** | 수 초 | <1s | **<10ms** | 컨테이너 부팅 |
| **메신저 수** | 20+ | 5-8 | 3-5 | 5-8 |
| **확장성(skills)** | 매우 큼 (커뮤니티 162+) | 작음 | 작음 | 중간 |
| **GitHub ★** | 374k | 26.8k | 29k | (소규모) |
| **추천 환경** | Mac mini 8GB+ | RPi 4 | RPi Zero | Docker host |

### 언제 무엇을 고를까

- **"기능 다 있고 메신저 많은 게 좋다"** → **OpenClaw**
- **"내가 코드 다 읽고 이해하고 싶다"** → **Nanobot** (며칠이면 정독 가능)
- **"라즈베리파이/임베디드 환경"** → **ZeroClaw**
- **"보안이 가장 중요. AI가 폭주해도 호스트 안 건드리길"** → **NanoClaw**

## 🔁 카테고리 B (장기 기억) 와의 조합

OpenClaw는 **장기 기억 시스템이 약하다**. 그래서 실전에서는 흔히 **memU/Letta를 메모리 백엔드로 연결**하는 조합이 쓰임:

```
[OpenClaw Gateway] ─► [Letta API] ─► [Postgres/SQLite (영속 상태)]
                       │
                       └─► 이전 대화·사용자 프로파일·선호도 반환
```

- **Letta**: ICalIBM/MemGPT의 정식 후속. Agent 상태를 DB에 저장, 컨텍스트 재구성 자동화
- **memU**: 사용자 발화에서 자동으로 지식 그래프 구축. "나를 점점 알아가는" 봇 만들 때

## 🌐 함께 쓰는 스택

| 역할 | 추천 도구 |
|------|----------|
| **로컬 LLM 서버** | Ollama, LM Studio, vLLM, MLX-LM |
| **외부 접근** | Tailscale, Cloudflare Tunnel, ngrok |
| **모니터링** | Grafana + Prometheus, Uptime Kuma |
| **메모리 레이어** | Letta, memU, Mem0 |
| **MCP 서버** | filesystem, github, slack, brave-search, sqlite |
| **자동화 트리거** | n8n, Activepieces, cron |
| **Voice** | Whisper.cpp, Piper TTS, OpenWakeWord |

## 🔥 최신 트렌드 (2026 Q1-Q2)

1. **"Lethal Trifecta" 인식 확산** — Simon Willison이 명명한 3대 위험(사적 데이터 + 외부 입력 + 외부 통신) 인식이 OpenClaw 폭풍 성장과 함께 메인스트림화.
2. **컨테이너 강제 격리** — NanoClaw/Hermes처럼 "에이전트는 무조건 컨테이너 안에서" 패턴 부상.
3. **MCP의 사실상 표준화** — Anthropic의 MCP가 자가호스팅 에이전트의 도구 인터페이스 표준으로 굳어지는 중.
4. **Mac mini M4 = 표준 홈 AI 서버** — 16GB+ 통합 메모리, 15W idle/30W load, Metal GPU 자동 사용. 월 전기료 $3-5.
5. **로컬 모델 품질 약진** — Llama 3.3 70B, Gemma 3, Qwen 2.5가 M4 Pro 48GB에서 GPT-4 mini급 품질을 35-50 tok/s로 제공.
6. **OWASP Top 10 for Agentic Apps** — Palo Alto Networks가 정리. OpenClaw가 모든 카테고리에 매핑됨.

## 🤔 의사결정 플로우 차트

```
시작: 자가호스팅 AI 비서 필요
   │
   ▼
메신저로 부르고 싶나? ─── No ──► Khoj (지식검색) / Open Interpreter (코드실행)
   │ Yes
   ▼
하드웨어 사양? 
   ├─ Mac mini 16GB+ / x86 32GB ──► OpenClaw (풀기능) ★
   ├─ RPi 4/5 / 미니PC ──────────► Nanobot
   └─ 라즈베리파이 Zero/임베디드 ──► ZeroClaw
   │
   ▼
보안이 최우선? ─── Yes ──► NanoClaw 또는 OpenClaw + 컨테이너 격리
   │ No (편의 우선)
   ▼
장기 기억 필요? ─── Yes ──► OpenClaw + Letta/memU 조합
   │ No
   ▼
OpenClaw 단독 운영
```

## 🔗 다음 챕터

- 공식 자료와 추천 학습 링크 → [03-references.md](03-references.md)
- 실제 Mac mini에 띄우기 → [04-learning/01-mac-mini-setup.md](04-learning/01-mac-mini-setup.md)
