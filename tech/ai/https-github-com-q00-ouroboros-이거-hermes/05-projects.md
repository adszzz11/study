---
date: 2026-06-17
tags:
  - tech
  - ai
  - ouroboros
  - projects
  - hermes
status: learning
type: tech-tool-study
---

# 05. Projects

## 프로젝트 1 — Seed-first coding task template

목표: 평소 coding agent에게 바로 던지던 작업을 Ouroboros Seed 형식으로 바꾼다.

산출물:

- `seed.yaml`
- acceptance criteria checklist
- mechanical checks 목록
- 실행 transcript

예시:

```yaml
goal: "Add CSV export to existing task CLI"
constraints:
  - "No new database"
  - "Backward-compatible CLI"
acceptance_criteria:
  - "User can run `task export --format csv`"
  - "CSV contains id,title,status,created_at"
  - "Existing commands keep working"
exit_conditions:
  - "Unit tests pass"
  - "Manual CLI smoke test recorded"
```

완료 기준:

- [ ] Seed에 non-goal이 포함됨
- [ ] acceptance criteria 3개 이상
- [ ] mechanical check 1개 이상
- [ ] semantic verification transcript 있음

## 프로젝트 2 — Hermes runtime PoC

목표: Hermes를 backend runtime으로 사용해 Ouroboros의 spec-first gate와 Hermes의 personal/infra agent 능력을 결합한다.

실행:

```bash
hermes model
ouroboros setup --runtime hermes
ouroboros init "Add a weekly repo health report job"
ouroboros run seed.yaml --runtime hermes
```

관찰할 것:

- Hermes memory/skill/gateway가 runtime execution에 영향을 주는가?
- Ouroboros event store에 Hermes action이 어떻게 기록되는가?
- Hermes 쪽 장기 운영 workflow와 Ouroboros Seed가 충돌하지 않는가?

완료 기준:

- [ ] Hermes runtime 설정 성공
- [ ] Seed 기반 execution 성공
- [ ] mechanical check pass
- [ ] event/audit trail 확인

## 프로젝트 3 — MCP-backed spec interview

목표: Ouroboros interview가 internal docs, issue tracker, repo metadata 같은 context를 MCP로 참조하게 한다.

아이디어:

- local docs MCP server
- GitHub issues MCP server
- database schema MCP server
- deployment status MCP server

검증 질문:

- interview가 context를 실제로 활용하는가?
- Seed에 출처가 반영되는가?
- external tool failure 시 fallback이 있는가?

관련: [[study/tech/ai/model-context-protocol-mcp]]

## 프로젝트 4 — Runtime comparison bake-off

목표: 같은 Seed를 여러 runtime에 돌려 execution quality를 비교한다.

| runtime | 평가 항목 |
|---|---|
| Claude Code | navigation, patch quality, test quality |
| Codex CLI | terminal workflow, approval handling |
| Gemini CLI | large-context recall |
| OpenCode | provider flexibility |
| Hermes | long-running automation, memory/skills |

측정표:

| 항목 | 점수 |
|---|---|
| acceptance criteria 충족 | 0-5 |
| mechanical checks | pass/fail |
| 불필요한 변경 없음 | 0-5 |
| event trail clarity | 0-5 |
| resume/replay 가능성 | 0-5 |

## 프로젝트 5 — Agent workflow policy 만들기

목표: "언제 바로 Codex/Claude를 쓰고, 언제 Ouroboros를 먼저 쓰는가?"를 개인/팀 policy로 만든다.

Ouroboros를 먼저 쓸 작업:

- 요구사항이 vague한 feature
- 여러 stakeholder가 있는 변경
- acceptance criteria가 중요한 운영 기능
- migration, auth, billing, data loss 같은 high-risk 영역
- agent가 추측하면 비용이 큰 작업

바로 coding agent에 맡겨도 되는 작업:

- 작은 bug fix
- test 추가
- docs typo
- 명확한 refactor
- 이미 issue/spec이 잘 정리된 작업

관련:

- [[study/tech/ai/codex]]
- [[study/tech/ai/claude]]
- [[study/tech/ai/lazy-codex]]

## 회고 템플릿

```md
## Task
- Goal:
- Runtime:
- Seed:

## What clarified the work?
- Interview question:
- Hidden assumption:

## Verification
- Mechanical:
- Semantic:
- Consensus:

## Outcome
- Accepted:
- Reworked:
- Replayed:

## Next Seed improvement
-
```

→ 빠른 참조: [[cheatsheet]]
