---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude Observer

> **한 줄 정의**: Claude Code의 여러 로컬 session 상태와 permission request를 macOS Dynamic Island/Menu Bar 및 LAN Web Dashboard에서 감시·처리하는 hook 기반 monitoring UI다.

## Overview

[Claude Observer](https://github.com/svenliebig/claude-observer)는 여러 terminal에서 동시에 실행되는 Claude Code session을 한 화면에서 추적하기 위한 독립 오픈소스 도구다. Claude Code lifecycle hook이 남긴 session별 JSON을 native Swift app이 읽어, repository마다 이름 붙은 crab 캐릭터와 색상으로 `working`, `idle`, `needs_input`, `needs_permission`, `error` 상태를 표시한다.

핵심 가치는 **주의 전환 비용을 줄이는 것**이다. 사용자는 terminal을 순회하지 않고 어떤 session이 멈췄는지 확인하고, 해당 terminal로 돌아가거나 permission request에 응답할 수 있다.

> [!important]
> 이 프로젝트는 Anthropic 공식 제품이 아니다. LLM observability/APM, token·cost analytics, agent orchestrator도 아니다.

## Learning Path

- [ ] [[tech/devtools/claude-observer/01-overview|Overview]] — 해결하는 문제와 핵심 특징 파악
- [ ] [[tech/devtools/claude-observer/02-ecosystem|Ecosystem]] — 대안과 선택 기준 비교
- [ ] [[tech/devtools/claude-observer/03-references|References]] — 공식·프로젝트 자료 확인
- [ ] [[tech/devtools/claude-observer/04-learning/01-getting-started|Getting started]] — 안전한 로컬 평가 환경 구성
- [ ] [[tech/devtools/claude-observer/04-learning/02-deep-dive|Deep dive]] — hook, state store, permission broker 분석
- [ ] [[tech/devtools/claude-observer/05-projects|Projects]] — 실습 과제로 동작 검증
- [ ] [[tech/devtools/claude-observer/cheatsheet|Cheatsheet]] — 상태와 운영 점검표 빠르게 찾기

## When To Use

- macOS에서 여러 Claude Code session을 병렬로 실행할 때
- 응답 완료, 사용자 입력 대기, API error를 terminal 전환 없이 확인하고 싶을 때
- Ghostty, iTerm2, Terminal.app, WezTerm, Alacritty, kitty 또는 tmux session으로 빠르게 복귀하고 싶을 때
- 같은 LAN의 mobile browser에서 상태를 확인하거나 permission에 응답하려 할 때
- 외부 SaaS나 중앙 database 없이 local-first monitoring을 실험할 때

## When Not To Use

- Windows/Linux에서 native desktop UI가 필요할 때
- prompt, token, cost, latency trace를 분석하는 observability가 필요할 때
- agent scheduling, task queue, retry, orchestration이 필요할 때
- license와 장기 유지보수 정책이 확정된 enterprise 도구가 필요할 때
- 인증·TLS·origin 검증을 확인하지 않은 상태로 공용 네트워크나 Internet에 dashboard를 노출해야 할 때
- 모든 최신 Claude Code hook event를 완전하게 추적해야 할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/ai/agent-orchestration/cli-agents|CLI Agents]]
- [[tech/ai/agent-orchestration/README|Agent Orchestration]]

## Sources

- Claude Observer repository and README: https://github.com/svenliebig/claude-observer
- Claude Code hooks reference: https://code.claude.com/docs/en/hooks
- Claude Code permissions: https://code.claude.com/docs/en/permissions

