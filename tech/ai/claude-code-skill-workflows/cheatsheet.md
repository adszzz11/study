---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet — Multi-Agent 운영 빠른 참조

## Worker brief

```text
Role: <researcher | implementer | critic>
Input: <scope, repository paths, approved sources>
Output: <structured result, citations, tests, unknowns>
Budget: <token/time/tool-call limit>
Done when: <measurable acceptance criteria>
Do not: <write production, expose secrets, expand scope>
```

## Judge checklist

- [ ] 모든 중요한 claim에 URL 또는 명시된 inference가 있는가?
- [ ] test·lint·typecheck 등 deterministic evidence가 있는가?
- [ ] worker 간 모순과 반증을 실제로 처리했는가?
- [ ] 변경 범위와 권한이 task에 맞는가?
- [ ] human approval이 필요한 위험·비용·production 변경을 분리했는가?

## 비용 절약

| 피할 것 | 대신 할 것 |
|---|---|
| 전체 repository를 모든 worker에 전달 | `CODEMAP`과 필요한 파일만 전달 |
| 성공 log 전체 공유 | 실패 test와 관련 output만 공유 |
| 즉시 범용 Skill 만들기 | 반복 확인 후 좁은 Skill로 승격 |
| 병렬화 = 비용 절감 가정 | 총 token·시간·재시도를 함께 계측 |

## Related Notes

- [[tech/ai/claude-code-skill-workflows/README|README]]
- [[tech/ai/claude-code-skill-workflows/01-overview|Overview]]

## Sources

- https://github.com/camilo-acevedo/claude-skills
- https://github.com/jfkconstruct/claude-skills/blob/main/skills/self-critique/SKILL.md
