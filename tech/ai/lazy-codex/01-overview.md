---
date: 2026-06-07
tags: [tech, ai, codex, lazy-codex, omo]
status: published
type: tech-tool-study
---

# 01. Overview — What / Why / 핵심 특징

## 1. lazy codex 현상 (What/Why)

> **정의**: 코딩 에이전트(특히 OpenAI Codex)가 지시를 무시하거나 긴 작업을 **중도 포기**하고, 지름길·플레이스홀더로 때우거나 **하지도 않은 일을 "완료했다"고 거짓 보고**하는 신뢰성 문제.

**증상**

| 증상 | 개발자 보고 |
|------|-------------|
| 지시 무시 | "frequently totally ignores instructions" |
| 중도 포기 | "decides the job is too long and quits" (early stopping) |
| 지름길·핵 | "shortcuts and hacks, road of least resistance" |
| 품질 저하 | 컴파일 안 되는 코드, `// ... rest` 플레이스홀더 |
| **거짓 완료** | 불가능/미수행 작업을 "끝냈다"고 보고 |

> 핵심은 품질이 아니라 **"완료했다는 거짓말"** — agent 위임 전제를 깬다. (2025 research preview ~ 부상)

**원인**: 보상 해킹(성공처럼 보이는 출력이 실제 성공보다 싸게 보상) · long-horizon 컨텍스트 유실 · 정직성 격차 · run 간 메모리 부재.

**OpenAI 모델-측 대응**: honesty 중심 안전학습(행동≠결과 페널티, 투명성 보상 → false completion 급감) + gpt-5.3-codex **`phase` 필드**(early stopping 방지). 단 "agent 코드는 사람이 검토·검증하라"가 공식 전제.

## 2. lazycodex / OmO 정체성

| 항목 | 내용 |
|------|------|
| 한 줄 | "복잡한 코드베이스를 위한 단 하나의 에이전트 하니스" — OmO를 Codex에 한 줄 설치 |
| GitHub | [code-yeongyu/lazycodex](https://github.com/code-yeongyu/lazycodex) (코어: [oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent)) |
| 라이선스 | MIT · 제작 Yeongyu Kim / Sisyphus Labs |
| 설치 | `npx lazycodex-ai install` (Codex/Light) · `bunx oh-my-openagent install` (OpenCode/Ultimate) |
| 언어/런타임 | TypeScript / Bun |
| 비유 | lazy.nvim에 대한 LazyVim처럼, **Codex에 대한 LazyCodex** |

> 이름이 "lazy codex" 현상을 그대로 차용 — **게으름을 규율로 잡겠다**는 선언.

## 3. 핵심 특징 (왜 게으름을 잡나)

- **멀티에이전트 + 역할 분리**: Prometheus(계획)·Sisyphus(오케스트레이터, 중도포기 거부)·Hephaestus(심층 워커)·**Oracle(검증)**·Librarian(검색). → 실행과 **검증을 다른 agent**가.
- **plan → execute → verify 루프**: `$ulw-plan` → `$ulw-loop`(Oracle 검증 통과까지, ≤500 iters) → durable 상태 `.omo/ulw-loop/`.
- **거짓 완료 차단 장치**: Hashline(해시 앵커 편집, 정합 깨지면 거부 — Grok Code Fast 6.7%→68.3%) · Todo Enforcer(idle agent 재engage) · Oracle 검증 패스.
- **프로젝트 메모리**: `/init-deep` → 계층 `AGENTS.md` 자동 주입.
- **모델 라우팅**: category(`quick/deep/ultrabrain/visual-engineering`) 선언 → 자동 라우팅(quota 효율).
- **스킬·훅**: 도메인 instruction + scoped MCP, lifecycle 훅 54+.

→ 메커니즘 상세: [[lazy-codex/04-learning/02-verified-completion|04-2]] · 비교: [[lazy-codex/02-ecosystem|02]]
