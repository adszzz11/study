# Paperclip 심층 스터디

> "Zero-human company" — AI 에이전트를 직원처럼 채용·운영하는 오픈소스 OS

## 한 줄 정의

**Paperclip = AI 에이전트 회사 관리 OS**. Node.js 서버 + React 대시보드로 여러 에이전트를 **직원**처럼 등록하고, 조직도·예산·거버넌스를 한 곳에서 관리한다. 핵심 차별점은 **"agent runtime unopinionated"** — Claude Code, OpenClaw 봇, Codex, Cursor, Python 스크립트, Bash, HTTP webhook **무엇이든 heartbeat만 보내면 직원**.

## 3줄 요약

1. **회사 메타포**: 회사·조직도·직책·예산·승인 워크플로우를 1급 객체로 모델링.
2. **Heartbeat 프로토콜**: 에이전트가 DB 큐로 wakeup 신호를 받고 실행. 시크릿 주입·스킬 로딩·어댑터 호출이 표준화됨.
3. **예산 hard-stop**: 직원별 월 예산 → 80% 경고 → 100% 자동 정지. 비용 폭주 차단.

## 핵심 키워드

`#multi-agent` `#orchestration` `#zero-human-company` `#governance` `#budget-control` `#heartbeat` `#typescript` `#postgres` `#react` `#mit`

## ⚡ Quick Start

```bash
# 한 줄 부트스트랩
npx paperclipai onboard --yes

# 또는 git clone
git clone https://github.com/paperclipai/paperclip.git
cd paperclip && pnpm install && pnpm dev
# UI: http://localhost:3000
```

요구사항: Node 20+, pnpm 9.15+, PostgreSQL (embedded SQLite도 OK).

## 📑 전체 목차

| 파일 | 내용 |
|------|------|
| [01-overview.md](01-overview.md) | 회사 메타포·heartbeat·구성 모듈 12개 |
| [02-ecosystem.md](02-ecosystem.md) | CrewAI/Agency Swarm/AutoGen 등과의 차이 |
| [03-references.md](03-references.md) | 공식·튜토리얼·커뮤니티 |
| [04-learning/01-install-and-onboard.md](04-learning/01-install-and-onboard.md) | 셋업 + 첫 회사 생성 |
| [04-learning/02-hiring-agents.md](04-learning/02-hiring-agents.md) | Claude Code·OpenClaw·Bash 직원 채용 |
| [04-learning/03-budget-and-governance.md](04-learning/03-budget-and-governance.md) | 예산·승인·감사로그 |
| [04-learning/04-routines-and-tickets.md](04-learning/04-routines-and-tickets.md) | 정기 작업·티켓 시스템 |
| [05-projects.md](05-projects.md) | 맥미니 자치 운영 시나리오 |
| [cheatsheet.md](cheatsheet.md) | CLI/API 빠른 참조 |

## 🗓️ 학습 플랜

| 일차 | 목표 |
|------|------|
| Day 1 | 01-overview + 02-ecosystem 읽고 카테고리 안의 위치 이해 |
| Day 2 | Quick Start로 띄우고 첫 회사·직원 생성 |
| Day 3 | Claude Code 직원 채용 + 첫 티켓 처리 |
| Day 4 | 예산·승인 워크플로우 구성 |
| Day 5 | 정기 루틴(매일 메일 정리) 직원으로 자동화 |
| Day 6+ | 맥미니 자치 운영 시나리오 (05-projects) |
