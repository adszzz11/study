---
date: 2026-03-29
tags:
  - tech
  - ai
  - cli-coding-agents
parent: "[[README]]"
---

# CLI 코딩 에이전트 종합 비교

> [[README|목차로 돌아가기]]

---

## 개요

오케스트레이션 도구(Conductor, Claude Squad 등)가 **관리하는 대상**인 CLI 코딩 에이전트들의 종합 비교.
무료 여부와 실제 비용이 핵심 관심사.

---

## 무료 여부 한눈에 보기

### 완전 무료 (OSS + BYOK)

> 도구 자체는 무료. API 비용만 사용자가 직접 부담.

| 에이전트 | Stars | 라이선스 | 지원 모델 | 언어 | 핵심 차별점 |
|----------|-------|---------|----------|------|------------|
| **Gemini CLI** | ~99K | Apache-2.0 | Gemini 2.5 Pro/Flash | TS | **일 1,000회 무료 + 1M 컨텍스트** |
| **Cline CLI** | ~59.6K | Apache-2.0 | 모든 프로바이더 | TS | Human-in-the-loop, Checkpoint |
| **Aider** | ~42.5K | Apache-2.0 | 100+ 모델 | Python | 가장 성숙, 자동 git 커밋 |
| **Goose** | ~33.7K | Apache-2.0 | 모든 LLM | Rust | Block 12K 직원 사용, MCP 네이티브 |
| **Pi** | ~28.7K | MIT | 15+ 프로바이더 | TS | 미니멀, 4가지 모드 (interactive/print/RPC/SDK) |
| **Qwen Code** | ~21.2K | Apache-2.0 | Qwen3-Coder 480B + 기타 | TS | SWE-bench 69.6%, Gemini CLI 포크 |
| **Hermes** | ~15.4K | MIT | 200+ 모델 (OpenRouter) | Python | Self-learning, 크론 스케줄러, 6가지 터미널 백엔드 |
| **OpenCode** | ~11.6K | MIT | 75+ 프로바이더 | Go | LSP 자동 설정, 멀티 세션 |

### 무료 티어 있음 (제한적)

| 에이전트 | Stars | 무료 티어 | 유료 플랜 | 핵심 차별점 |
|----------|-------|----------|----------|------------|
| **Gemini CLI** | ~99K | **일 1,000회** (가장 관대) | Pay-as-you-go | Google Search 연동, 1M 컨텍스트 |
| **Copilot CLI** | ~9.6K | 제한된 프리미엄 요청 | Pro $10/월 (300회) | GitHub 네이티브 연동 |
| **Amp** | N/A | 광고 기반, ~$10/일 상당 | Smart ~$20+/월 | Deep mode, 서브에이전트 (Oracle/Librarian) |
| **Amazon Q CLI** | ~1.9K | 월 50회 에이전틱 채팅 | Pro $19/user/월 | AWS 서비스 깊은 연동 |
| **Kiro** | ~3.3K | 50 크레딧 (영구) + 500 보너스 | Pro $20/월 (1,000 크레딧) | Spec-driven 개발, Agent Hooks |
| **Cursor CLI** | N/A | 월 2,000 completions | Pro $20/월 | IDE 연동, Background Agents |
| **Warp** | N/A | 월 75 AI 크레딧 | Build $20/월 | GPU 가속 터미널, 에이전트 병렬 실행 |

### 무료 티어 없음 (유료만)

| 에이전트 | Stars | 최저 가격 | 핵심 차별점 |
|----------|-------|----------|------------|
| **Claude Code** | ~84K | Pro $20/월 또는 API BYOK | Skills, Hooks, MCP, 서브에이전트, 1M 컨텍스트 |
| **Codex CLI** | ~68K | Plus $20/월 또는 API BYOK | Terminal-Bench #1 (77.3%), Rust 네이티브 |
| **Mistral Vibe** | ~3.7K | Le Chat Pro $14.99/월 | Sonnet 대비 7x 비용 효율, 유럽 데이터 주권 |
| **Droid** | ~700 | Pro $20/월 | 전문 Droid 시스템 (Code/Knowledge/Reliability) |
| **Auggie** | ~165 | Indie $20/월 | Context Engine, SWE-Bench Pro #1 |

---

## 상세 비교

### Tier 1: 메이저 (Stars 30K+)

#### Claude Code (Anthropic) — ~84K stars

| 항목 | 내용 |
|------|------|
| **모델** | Sonnet 4.6 (기본), Opus 4.6 (고성능, 1M 컨텍스트), Haiku 4.5 (경량) |
| **가격** | Pro $20/월 (~44K 토큰/5h), Max 5x $100/월, Max 20x $200/월, API BYOK |
| **무료** | ❌ (신규 API 계정 소액 크레딧만) |
| **라이선스** | Source-available (오픈소스 아님) |
| **언어** | TypeScript |
| **플랫폼** | macOS, Linux, Windows (WSL) |
| **차별점** | MCP, Skills, Hooks, 서브에이전트, Agent Teams, Voice Mode, /loop |

#### Gemini CLI (Google) — ~99K stars

| 항목 | 내용 |
|------|------|
| **모델** | Gemini 2.5 Pro, Flash, Flash-Lite, Gemini 3 |
| **가격** | **무료 (일 1,000회)**, Pay-as-you-go (Flash-Lite $0.10/$0.40 MTok) |
| **무료** | ✅ **시장 최고 무료 티어** |
| **라이선스** | Apache-2.0 |
| **언어** | TypeScript |
| **플랫폼** | macOS, **Windows (네이티브, WSL 불필요)**, Linux |
| **차별점** | Google Search 그라운딩, 1M 컨텍스트, Conversation Checkpointing, Vim 모드 |

#### Codex CLI (OpenAI) — ~68K stars

| 항목 | 내용 |
|------|------|
| **모델** | GPT-5.1-Codex (Max/Mini), GPT-5.4, codex-mini-latest |
| **가격** | Plus $20/월 (30-150 msgs/5h), Pro $200/월, API BYOK |
| **무료** | ❌ (Free/Go 티어 일시적 제한 접근만) |
| **라이선스** | Apache-2.0 |
| **언어** | **Rust** (2025년 TS에서 리라이트) |
| **플랫폼** | macOS, Linux, Windows (WSL) |
| **차별점** | Terminal-Bench 2.0 #1 (77.3%), seccomp 샌드박스, 경량 로컬 우선 |

#### Cline CLI (독립) — ~59.6K stars

| 항목 | 내용 |
|------|------|
| **모델** | OpenRouter, Anthropic, OpenAI, Gemini, Bedrock, Azure, Ollama |
| **가격** | **무료** (API 비용만), Teams: 10석까지 무료, 이후 $20/월 |
| **무료** | ✅ |
| **라이선스** | Apache-2.0 |
| **언어** | TypeScript |
| **플랫폼** | macOS, Linux, Windows |
| **차별점** | 모든 변경에 승인 필요 (안전), Plan/Act 모드 (Tab 전환), 브라우저 자동화, Checkpoint |

#### Aider (독립) — ~42.5K stars

| 항목 | 내용 |
|------|------|
| **모델** | 100+ 모델 (Claude, GPT, DeepSeek, Gemini, Ollama 등) |
| **가격** | **완전 무료** (API 비용만) |
| **무료** | ✅ |
| **라이선스** | Apache-2.0 |
| **언어** | Python |
| **플랫폼** | macOS, Linux, Windows |
| **차별점** | 가장 성숙한 도구 (4.1M+ 설치), 자동 git 커밋, 린터/테스트 자동 실행, 50+ 언어 |

#### Goose (Block) — ~33.7K stars

| 항목 | 내용 |
|------|------|
| **모델** | Claude, GPT-5, Gemini, Llama, DeepSeek, OpenRouter, Ollama 등 |
| **가격** | **완전 무료** (API 비용만) |
| **무료** | ✅ |
| **라이선스** | Apache-2.0 |
| **언어** | **Rust** |
| **플랫폼** | macOS, Linux, Windows (데스크톱 앱 + CLI) |
| **차별점** | Block 12,000 직원 실사용, 빌드/실행/디버그/테스트 전체 워크플로우, MCP 네이티브 |

### Tier 2: 주목할 도구 (Stars 10K~30K)

#### Pi (독립) — ~28.7K stars

| 항목 | 내용 |
|------|------|
| **모델** | 15+ 프로바이더 (Anthropic, OpenAI, Google, Ollama 등) |
| **가격** | **완전 무료** (API 비용만) |
| **라이선스** | MIT |
| **차별점** | 미니멀 철학, 4가지 모드 (interactive/print/JSON/RPC/SDK), TypeScript 확장, npm 공유 가능 |

#### Qwen Code (Alibaba) — ~21.2K stars

| 항목 | 내용 |
|------|------|
| **모델** | Qwen3-Coder 480B MoE + GPT-5.4, Opus 4.6, Gemini 3.1 Pro, Ollama |
| **가격** | **완전 무료** (API 비용만, Ollama로 로컬 실행 시 $0) |
| **라이선스** | Apache-2.0 |
| **차별점** | SWE-bench 69.6%, 480B MoE (35B active), Gemini CLI 포크, 256K-1M 컨텍스트 |

#### Hermes Agent (Nous Research) — ~15.4K stars

| 항목 | 내용 |
|------|------|
| **모델** | 200+ (OpenRouter, Ollama, 커스텀 엔드포인트 등) |
| **가격** | **완전 무료** (자체 호스팅, $5 VPS에서도 실행 가능) |
| **라이선스** | MIT |
| **차별점** | Self-learning + 영속 메모리, 크론 스케줄러, 40+ 빌트인 도구, 6가지 터미널 백엔드 (Docker/SSH/Modal 등) |

#### OpenCode (독립) — ~11.6K stars

| 항목 | 내용 |
|------|------|
| **모델** | 75+ 프로바이더 (Models.dev 경유) |
| **가격** | **코어 무료**, Go $10/월 (큐레이션 모델), Zen 종량제 ($20 단위) |
| **라이선스** | MIT |
| **차별점** | LSP 자동 설정 (언어서버를 LLM에 연결), 멀티 세션, 세션 링크 공유, Go 언어 TUI |

### Tier 3: 벤더/니치 도구

#### Copilot CLI (GitHub) — ~9.6K stars

| 항목 | 내용 |
|------|------|
| **가격** | Free $0 (제한), Pro $10/월 (300 프리미엄 요청), Pro+ $39/월 |
| **차별점** | GitHub 네이티브 (repos, issues, PRs, Actions), 다중 모델 (Claude/GPT/o3) |

#### Mistral Vibe (Mistral AI) — ~3.7K stars

| 항목 | 내용 |
|------|------|
| **가격** | Le Chat Pro **$14.99/월** (시장 최저가 구독), API: Devstral 2 $0.40/$2.00 MTok |
| **차별점** | Sonnet 대비 7x 비용 효율, 유럽 데이터 주권, SWE-bench 72.2%, ACP 지원 |

#### Kiro (AWS) — ~3.3K stars

| 항목 | 내용 |
|------|------|
| **가격** | 무료 50 크레딧 (영구) + 500 보너스, Pro $20/월, Power $200/월 |
| **차별점** | Spec-driven 개발 (EARS 표기법), Agent Hooks, IDE + CLI, Claude 모델 사용 |

#### Amazon Q Developer CLI (AWS) — ~1.9K stars

| 항목 | 내용 |
|------|------|
| **가격** | 무료 월 50회 에이전틱 채팅, Pro $19/user/월 |
| **차별점** | AWS 서비스 깊은 연동 (Lambda, CloudFormation), Java/.NET 코드 변환, 보안 스캐닝 |

#### Amp (Sourcegraph) — 비공개

| 항목 | 내용 |
|------|------|
| **가격** | 무료 (광고 기반, ~$10/일 상당), Smart ~$20+/월 |
| **차별점** | Deep mode (자율 추론), 서브에이전트 (Oracle/Librarian/Painter), 무제한 토큰 |

#### Droid (Factory AI) — ~700 stars

| 항목 | 내용 |
|------|------|
| **가격** | $0부터, Pro $20/월, Enterprise $2,000/월 |
| **차별점** | 전문 Droid 시스템 (Code/Knowledge/Reliability/Product), Terminal-Bench #1 (58.75%), Headless CI |

#### Warp — 비공개

| 항목 | 내용 |
|------|------|
| **가격** | 무료 월 75 AI 크레딧, Build $20/월 |
| **차별점** | **터미널 자체를 대체** (GPU 가속 Rust), 에이전트 병렬 실행, 700K+ 개발자 |

---

## 비용 최적화 전략

### 무료로 시작하기

1. **Gemini CLI** — 일 1,000회 무료, 가장 관대한 무료 티어
2. **Aider + Ollama** — 도구 무료 + 로컬 모델로 API 비용 $0
3. **Goose + Ollama** — 동일 전략, Rust 기반 빠른 실행
4. **Qwen Code + Ollama** — Qwen3-Coder 로컬 실행 가능

### BYOK (Bring Your Own Key) 최적 조합

| 용도 | 추천 조합 | 예상 비용 |
|------|----------|----------|
| 일상 코딩 | Aider + Sonnet 4.6 | ~$5-15/일 |
| 비용 민감 | Aider + DeepSeek V3 | ~$1-3/일 |
| 복잡한 작업 | Claude Code (Max 5x) | $100/월 고정 |
| 무료 우선 | Gemini CLI (무료 티어) | $0 |
| 로컬 우선 | Goose + Ollama (Qwen3-Coder) | $0 (전기세만) |

### 구독 가성비 순위

| 순위 | 에이전트 | 월 비용 | 가성비 포인트 |
|------|---------|--------|-------------|
| 1 | **Gemini CLI** | $0 | 일 1,000회 무료, 대부분 충분 |
| 2 | **Copilot CLI** | $10 | GitHub 연동 가치 |
| 3 | **Mistral Vibe** | $14.99 | 시장 최저 구독, 7x 비용 효율 |
| 4 | **Amazon Q CLI** | $19 | AWS 사용자에게 필수 |
| 5 | **Claude Code / Codex / Kiro** | $20 | 각각 고유 강점 |

---

## 벤치마크 (2026-03 기준)

| 벤치마크 | #1 | #2 | #3 |
|----------|-----|-----|-----|
| **Terminal-Bench 2.0** | Codex (77.3%) | Droid (58.75%) | - |
| **SWE-bench Verified** | Mistral Vibe (72.2%) | Qwen Code (69.6%) | - |
| **SWE-Bench Pro** | Auggie | - | - |

> 벤치마크는 자사 발표 기준이므로 교차 검증 필요

---

## 관련 노트

- [[README|AI 에이전트 오케스트레이션 플랫폼]]
- [[study/tech/ai/claude/03-claude-code|Claude Code CLI]]

---

## References

- [awesome-cli-coding-agents](https://github.com/bradAGI/awesome-cli-coding-agents) — 80+ 에이전트 목록
- [Tembo: 15 CLI Tools Compared](https://www.tembo.io/blog/coding-cli-tools-comparison)
- [NxCode: AI Coding Tools Pricing Comparison 2026](https://www.nxcode.io/resources/news/ai-coding-tools-pricing-comparison-2026)

---

**생성일**: 2026-03-29
**상태**: 학습 중
