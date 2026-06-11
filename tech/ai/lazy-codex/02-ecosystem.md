---
date: 2026-06-07
tags: [tech, ai, codex, agent-harness, hermes, comparison]
status: published
type: tech-tool-study
---

# 02. Ecosystem — 코딩 하니스 landscape & 비교

## 1. 분류 (2026)

| 유형 | 예시 |
|------|------|
| CLI 에이전트 | **Codex**, Claude Code, Gemini CLI, Aider, OpenCode, Goose, Pi |
| 하니스(오케스트레이터) | **OmO/lazycodex**, parallel runners, 자율 루프 |
| IDE/확장 | Cursor, Windsurf, Zed, GitHub Copilot, Cline, Continue |
| 클라우드 | Devin, OpenHands, Jules |
| 운영 인프라 | **hermes**(내 것 — 24/7 비서) |

> 벤치마크: **SWE-bench Verified**(실 GitHub 이슈 해결률)가 표준, 2026 **SWE-bench Pro**(2000+, 비공개)로 강화. 예: Claude Code 하니스 ~92.1%, Codex CLI ~77.3% (출처별 상이).

## 2. 게으름 관점 비교

| 도구 | 게으름 차단 | 비고 |
|------|------------|------|
| 그냥 Codex CLI | 모델 honesty + `phase` | 외부 검증 없음 → 사람 의존 |
| Claude Code | CLAUDE.md 지속 컨텍스트, computer-use | 가장 완성형 런타임 |
| Cursor 3 | /worktree 격리, parallel Agent Tabs, cloud VM | "첫 모호 지점에서 stall" — overnight엔 약함 |
| Devin | 완전 샌드박스, plan→write→test→PR 자율 | 가장 자율, 클라우드 |
| **OmO/lazycodex** | **Oracle 검증 + Ralph Loop + Todo Enforcer + Hashline** | 검증을 1급으로 |
| **hermes** | self-test 게이트 + autodeploy 롤백 + PR 사람-머지 | 운영 인프라 레벨 |

## 3. OmO/lazycodex vs hermes (핵심 대조)

| 축 | lazycodex / OmO | **hermes** |
|----|------------------|------------|
| 정체성 | 단일-작업 규율 하니스 | 24/7 개인 비서 인프라 |
| 검증 | Oracle(독립 agent) + Ralph Loop | self-test.sh + 사람 PR 리뷰 |
| 완료 증명 | durable `.omo/ulw-loop/` + Hashline | self-test PASS + PR merge |
| 메모리 | 계층 AGENTS.md(/init-deep) | Knowledge Graph(wiki) + CLAUDE.md |
| 실행 범위 | 로컬 코드베이스 직접 | **WORKROOT 격리 워크트리**(로컬 작업본 무수정) |
| 사람 게이트 | 선택(Oracle 자동) | **강제**(PR-only, 머지는 사람) |
| 운영 | 개발 보조 | launchd 서비스 + GitOps + Discord 봇 |
| 보안 | 스킬 권한 제한 | **RCX**(R+C+X 분리) + budget 게이트 |

> 흥미로운 평행: OmO **Librarian** ↔ hermes **com.hermes.librarian**, OmO **Ralph Loop** ↔ hermes **ralph-loop**. 수렴 진화.

## 4. 공통 원리 (수렴)
- **"실행 ≠ 검증"** 분리 → 거짓 완료를 독립 검증이 잡는다.
- **루프-until-검증** + **durable 상태**.
- 차이는 **범위**: OmO=한 작업 완수 / hermes=항상 켜진 운영(+격리+사람 게이트+보안).

→ 다음: [[lazy-codex/03-references|03. References]] · 통합 아이디어: [[lazy-codex/05-projects|05]]
