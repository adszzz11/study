---
date: 2026-10-21
tags: [tech]
type: tech-tool-study
status: draft
---

# Jcode — 생태계와 비교

> [[README|목차로 돌아가기]] | [[03-references|다음: 참고자료]]

## Comparison

| 도구 | 중심 강점 | Jcode 대비 선택 기준 |
|---|---|---|
| **Jcode** | Rust TUI, daemon/socket, semantic memory, native swarm | 같은 host/repo에서 많은 agent를 장시간 병렬 운용할 때 |
| **Claude Code** | Anthropic model·workflow 중심의 범용 coding agent | Claude 중심 팀 운영과 Anthropic 생태계를 우선할 때 |
| **Codex CLI** | OpenAI/Codex 중심 terminal agent | OpenAI model, Codex account, Codex-native workflow가 우선일 때 |
| **OpenCode** | multi-provider, TUI/desktop/web, OpenAPI server | HTTP server/API와 확장 가능한 config 중심 운영일 때 |
| **Pi** | 최소주의 terminal harness, TypeScript extension·skill·package | subagent/swarm 기본값보다 workflow를 직접 조립하고 싶을 때 |

## Decision Criteria

- **병렬성**: task 간 파일 ownership이 분명하고 coordinator가 결과를 통합할 수 있는가?
- **Provider**: 필요한 model, 인증 방식(OAuth/API key), local endpoint를 지원하는가?
- **운영성**: 원격 host session 지속, dashboard/CI SDK, approval 처리 방식이 필요한가?
- **보안**: filesystem/shell/MCP 권한을 최소화하고 untrusted input을 격리하는가?
- **검증**: latency, RAM, 성공률, conflict rate를 같은 workload에서 측정했는가?

Jcode는 더 좋은 model을 제공하기보다 여러 provider 위에서 **parallel execution과 harness behavior**를 최적화한다. 프로젝트의 성능 표는 가설을 세우는 참고자료이며 독립 benchmark가 아니다.

## Sources

- https://github.com/1jehuang/jcode
- https://docs.opencode.ai/docs/server/
- https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent
