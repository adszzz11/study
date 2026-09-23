---
date: 2026-09-23
tags: [tech]
type: tech-tool-study
status: draft
---

# ECC harness — Projects / 적용

## 1. Multi-agent 개발 표준화

**상황**: Claude Code와 Codex를 함께 쓰는 팀이 code review, TDD, security review 기준을 맞추려 한다.

- repo에서 공통 rules와 선택한 skills를 version control한다.
- 각 harness adapter의 실제 적용 범위를 test repository에서 확인한다.
- PR template에 plan, test evidence, review, AgentShield finding 검토를 남긴다.

**성공 기준**: 동일한 task에서 harness가 달라도 필요한 test·review evidence가 빠지지 않는다.

## 2. Legacy modernization

**흐름**:

```text
repository analysis → architecture plan → characterization tests
→ implementation → fresh-context review → verification
```

analysis와 implementation을 분리하고 fresh-context review로 기존 session의 확증 편향을 낮춘다. hooks/memory는 승인된 summary와 decision만 남기는지 먼저 확인한다.

## 3. Agent configuration security gate

PR마다 AgentShield를 실행하여 과도한 shell permission, malicious hook, exposed secret, 위험한 MCP 연결을 찾는다.

```bash
npx -y ecc-agentshield scan --path . --format json
```

CI policy는 scanner 결과만으로 merge를 결정하지 않는다. 새 finding, baseline drift, permission/config diff를 reviewer가 함께 확인하도록 만든다.

## 4. Cross-harness handoff PoC

Codex에서 repository 조사와 plan을 수행하고, 지원되는 unified memory handoff로 Claude Code 또는 다른 harness의 구현 session에 넘긴다.

| 평가 항목 | 측정 예 |
|---|---|
| 재작업 | 새 session의 재탐색 시간·중복 질문 수 |
| 품질 | 누락된 제약·test failure·review finding 수 |
| 비용 | token·wall-clock time |
| 안전 | handoff에 민감 데이터가 포함됐는지 |

## 5. Selective platform rollout

전사 설치 전에 한 프로젝트에 minimal/no-hooks profile을 적용한다. 품질, token cost, security finding, adapter compatibility를 기준선과 비교한 뒤 필요한 component만 확장한다. 설치 경로는 끝까지 하나만 유지하고, 확장 전 rollback(제거 대상 파일·config·hook)을 rehearsal한다.

## Sources

- https://github.com/affaan-m/ECC
- https://github.com/affaan-m/agentshield
- https://www.npmjs.com/package/ecc-agentshield
