---
date: 2026-09-08
tags: [tech]
type: tech-tool-study
status: draft
---

# Ruflo Cheatsheet

> [[README|목차]]

## 한눈에 보기

| 항목 | 요약 |
|---|---|
| 정체 | coding agent용 agent meta-harness / orchestration platform |
| Surface | CLI + MCP + hooks + plugins |
| Orchestration | specialized agents, swarm, workflow |
| Memory | AgentDB, RuVector, SQLite/hybrid, semantic retrieval |
| Policy | guidance, gates, deterministic tool gateway, proof chain |
| 조사 기준 | 2026-09-08 |
| npm `latest` snapshot | `3.38.23` — 실행 전 재확인 |
| 이전 이름 | Claude Flow; 2026-02-27 v3.5에서 Ruflo로 rebranding |

## Version과 help

```bash
npm view ruflo version
npm view ruflo dist-tags --json
npx ruflo@latest --help

# 재현 가능한 run은 확인한 version pin
npx ruflo@3.38.23 --help
```

## Topology

| 값 | 기억할 문장 |
|---|---|
| `mesh` | 소규모 peer 탐색 |
| `hierarchical` | coordinator 중심 분해·승인 |
| `hierarchical-mesh` | 계층 제어 + peer 협업; 문서상 default |
| `adaptive` | workload에 따라 구조 변경 |

Configuration snapshot의 max agents는 15지만 처음에는 2~3으로 시작한다.

## Lifecycle hooks

| Hook | 주 용도 |
|---|---|
| `PreToolUse` | routing, schema, policy, budget 검사 |
| `PostToolUse` | 결과 평가, telemetry, memory 후보 |
| `PreCompact` | compaction 전 핵심 context 보존 |
| `Stop` | outcome 정리와 learning 반영 |

## Learning loop

```text
RETRIEVE → JUDGE → DISTILL → CONSOLIDATE
```

- Retrieve: 관련 memory 검색
- Judge: 현재 task 적합성·신뢰도 평가
- Distill: reusable lesson으로 축약
- Consolidate: provenance와 namespace를 붙여 저장

## 최소 보안 원칙

- [ ] MCP namespace는 default deny + allowlist
- [ ] destructive action은 dry-run/approval/idempotency 적용
- [ ] memory write 전 secret·PII redaction
- [ ] project/user namespace 분리
- [ ] hook input/output과 side effect audit
- [ ] diff size, token, tool call budget에 hard limit
- [ ] installed version에서 denial test 수행

## 선택 요약

| 필요 | 먼저 볼 것 |
|---|---|
| coding agent workspace를 swarm으로 확장 | Ruflo |
| 명시적 durable state graph | LangGraph |
| Python role/goal team | CrewAI |
| custom message-driven agent runtime | AutoGen |
| 작은 OpenAI-native agent SDK | OpenAI Agents SDK |
| model/provider gateway | [[tech/ai/litellm/README|LiteLLM]] |
| tool/data integration protocol | [[tech/ai/model-context-protocol-mcp/README|MCP]] |

## 도입 전 60초 점검

```text
1. npm latest와 changelog 확인
2. exact version pin
3. generated config/hook diff 검토
4. 2~3 agents + read-heavy task로 시작
5. 필요한 MCP tools만 노출
6. single-agent baseline과 품질/비용 비교
7. memory leakage와 policy bypass test
8. upgrade/rollback 기록
```

## Sources

- https://www.npmjs.com/package/ruflo?activeTab=versions
- https://github.com/ruvnet/ruflo/blob/main/README.md
- https://github.com/ruvnet/ruflo/blob/main/CHANGELOG.md
- https://github.com/ruvnet/ruflo/blob/main/v3/implementation/init/CONFIGURATION.md
- https://github.com/ruvnet/ruflo/blob/main/SKILL.md

