# Part 3. 학습 자료 & 레퍼런스

## 📚 공식 자료

### OpenClaw 본가
- 🟢 [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw) — 본 리포 (374k★)
- 🟢 [github.com/openclaw](https://github.com/openclaw) — OpenClaw 조직 (관련 서브 프로젝트들)
- 🟡 [awesome-openclaw-agents](https://github.com/mergisi/awesome-openclaw-agents) — 162개 production-ready SOUL.md 템플릿
- 🟡 [OpenClaw-RL](https://github.com/Gen-Verse/OpenClaw-RL) — 강화학습으로 에이전트 훈련하는 분기
- 🟡 [openclaw.net (clawdotnet)](https://github.com/clawdotnet/openclaw.net) — .NET NativeAOT 재구현 (비공식)

### 매니지드 호스팅 (자가호스팅 대안)
- 🟡 [OneClaw](https://www.oneclaw.net) — $9.99/월부터, GitHub fork 기반 자동 배포
- 🟡 [ClawHost](https://github.com/bfzli/clawhost) — 오픈소스 셀프 호스팅 컨트롤 플레인
- 🟡 [ClawPort](https://clawport.io) — 텔레그램 봇 전용 매니지드

## 🎓 학습 자료

### 🟢 입문 (셋업·첫 동작)
- [Simon Willison: Running OpenClaw in Docker](https://til.simonwillison.net/llms/openclaw-docker) — 가장 정직하고 짧은 셋업 메모
- [Localtonet: How to Self-Host OpenClaw and Access It Remotely](https://localtonet.com/blog/how-to-self-host-openclaw) — VPS 셋업 + 원격 접근
- [aifreeapi: From Zero to Personal AI Bot in 15 Minutes](https://www.aifreeapi.com/en/posts/openclaw-telegram-setup) — 텔레그램 봇 끝까지

### 🟢 Mac mini 특화
- ⭐ [marc0.dev: Mac Mini M4 AI Server: Local LLM + Agent Setup (2026)](https://www.marc0.dev/en/blog/ai-agents/mac-mini-ai-server-ollama-openclaw-claude-code-complete-guide-2026-1770481256372) — Ollama + OpenClaw + Claude Code 전 과정
- [mager.co: OpenClaw + Tailscale: Your Always-On AI Agent](https://www.mager.co/blog/2026-02-22-openclaw-mac-mini-tailscale/) — Mac mini + Tailscale 조합
- [howaiworks.ai: Mac Mini M4: The Ultimate Hub for Autonomous AI Agents](https://howaiworks.ai/blog/mac-mini-m4-ai-agent-hub)
- [techtippr: Mac Mini M4 as a Local AI Server (2026)](https://techtippr.com/mac-mini-m4-ai-server-2026/) — 벤치마크 + 설정
- [popularai.org: The Best Mac mini for local LLMs in 2026](https://www.popularai.org/p/the-best-mac-mini-for-local-llms) — M4 vs M4 Pro 선택 가이드
- [stratobuilds: Run Your Own Local LLM with Ollama + Home Assistant](https://stratobuilds.com/project/local-llm-ollama-home-assistant/) — 홈오토메이션 연동

### 🟡 중급 (커스터마이즈·실전)
- [Andriy Buday: My 1-Hour Open Claw Setup: Docker, Llama 3.1, and Telegram](https://andriybuday.com/2026/02/my-1-hour-open-claw-setup-docker-llama-3-1-and-telegram.html) — 1시간 안에 완성
- [eastondev: OpenClaw Telegram Integration Guide](https://eastondev.com/blog/en/posts/ai/20260205-openclaw-telegram-integration/) — 텔레그램 봇 깊게
- [Bibek Poudel: How OpenClaw Works — Understanding AI Agents Through a Real Architecture](https://bibek-poudel.medium.com/how-openclaw-works-understanding-ai-agents-through-a-real-architecture-5d59cc7a4764)
- [Milvus: What Is OpenClaw? Complete Guide](https://milvus.io/blog/openclaw-formerly-clawdbot-moltbot-explained-a-complete-guide-to-the-autonomous-ai-agent.md) — 아키텍처 디테일
- [DataCamp: Top OpenClaw Alternatives — From Local to Enterprise](https://www.datacamp.com/blog/openclaw-alternatives) — 대안 비교

### 🔴 고급 (보안·운영·내부)
- ⭐ [Conscia: The OpenClaw security crisis](https://conscia.com/blog/the-openclaw-security-crisis/) — 보안 사태 정리 (필독)
- ⭐ [The Hacker News: Four OpenClaw Flaws — data theft, privilege escalation, persistence](https://thehackernews.com/2026/05/four-openclaw-flaws-enable-data-theft.html) — Claw Chain 취약점
- [Adversa AI: OpenClaw security 101 — Vulnerabilities & hardening (2026)](https://adversa.ai/blog/openclaw-security-101-vulnerabilities-hardening-2026/) — 하드닝 가이드
- [Cyberdesserts: OpenClaw Security Risks — Skills, Exposure and Exploits](https://blog.cyberdesserts.com/openclaw-malicious-skills-security/) — Skills 마켓플레이스 공급망 공격
- [TheHackerWire: OpenClaw Sandbox Bypass — CVE-2026-41329](https://www.thehackerwire.com/openclaw-sandbox-bypass-leads-to-privilege-escalation-cve-2026-41329/)
- [openclaw-security-monitor (GitHub)](https://github.com/adibirzu/openclaw-security-monitor) — 운영 모니터링 도구
- [Simon Willison: The "lethal trifecta" for AI agents](https://simonwillison.net/) — 개념 원전

### 🔴 한국 자료
- [velog "OpenClaw" 검색](https://velog.io/search?q=OpenClaw) — 한국어 후기 (검색해서 골라보기)
- 카테고리 자체에 대한 한국어 정리는 아직 빈약 → 본 노트가 그 빈자리를 메우는 목적

## 📡 커뮤니티 · 질문할 곳

| 채널 | 용도 |
|------|------|
| [OpenClaw GitHub Discussions](https://github.com/openclaw/openclaw/discussions) | 공식 Q&A. 첫 질문은 여기 |
| [Reddit r/selfhosted](https://www.reddit.com/r/selfhosted/) | "How I self-host X" 글 많음 |
| [Reddit r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/) | 로컬 모델 벤치마크·튜닝 |
| [Hacker News (검색: OpenClaw)](https://hn.algolia.com/?q=OpenClaw) | 비판적 시각 + 보안 토론 |
| [OpenClaw Discord](https://discord.gg/openclaw) | 비공식 빠른 답변 |

## 🌟 비교군 공식 자료

### Letta (장기 기억)
- [letta.com](https://www.letta.com/) / [github.com/letta-ai/letta](https://github.com/letta-ai/letta)
- 논문: MemGPT (UC Berkeley)

### Open Interpreter
- [openinterpreter.com](https://openinterpreter.com) / [github.com/OpenInterpreter/open-interpreter](https://github.com/OpenInterpreter/open-interpreter)

### Khoj
- [khoj.dev](https://khoj.dev/) / [github.com/khoj-ai/khoj](https://github.com/khoj-ai/khoj)

### Ollama (로컬 LLM)
- [ollama.com](https://ollama.com)
- [github.com/ollama/ollama](https://github.com/ollama/ollama)

### Tailscale / Cloudflare Tunnel
- [tailscale.com/kb](https://tailscale.com/kb)
- [Cloudflare Tunnel docs](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)

## 🎬 비디오 자료 (검색 키워드)

YouTube에서 직접 검색해 보기 (URL은 노출 시점에 따라 다름):
- `"OpenClaw self-hosted Mac mini 2026"`
- `"Ollama Mac M4 home server setup"`
- `"Tailscale Mac mini AI server"`
- `"OpenClaw vs Open Interpreter"`

## 📖 인접 학습 (이미 본 vault 안의 자료)

본 vault에서 함께 보면 좋은 폴더:
- [[study/tech/ai/agent-orchestration]] — Claude Squad, ccmanager, vibe-kanban 등 멀티 에이전트 도구
- [[study/tech/ai/claude]] — Claude Code, Claude API
- [[study/tech/ai/litellm]] — 여러 LLM API 통합 게이트웨이
- [[study/tech/ai/openrouter]] — LLM 라우팅
- [[study/tech/ai/mastra]] — TS 기반 AI 프레임워크

## 🔗 다음 챕터

- 실제 Mac mini 셋업 → [04-learning/01-mac-mini-setup.md](04-learning/01-mac-mini-setup.md)
