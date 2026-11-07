---
date: 2026-11-07
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: Enforcement와 Evaluation

## CI Gate 설계

instruction file 변경 또는 framework migration PR에서 다음을 검사한다.

```text
instruction diff
  ├─ referenced path exists?
  ├─ command exists in package/task config?
  ├─ framework/API reference still valid?
  ├─ sibling instruction conflicts?
  └─ executable policy duplicated in prose?
```

- 존재하지 않는 path와 폐기 command를 fail한다.
- sibling instruction 간 semantic conflict와 200-line 초과를 warning 또는 review gate로 둔다.
- format, type, test, security rule은 linter·hook·permission policy·CI로 승격한다.

## Security 모델

instruction file은 agent의 trusted prompt surface다. 외부 contributor가 수정 가능한 file이라면 protected branch, code owner review, content validation을 적용한다. “문서니까 harmless”라는 가정은 README instruction injection 위험을 놓친다.

## Release Eval

팀 convention 10개를 fixture로 만들고 stale instruction과 existing code를 충돌시킨다. Codex, Claude Code, Copilot release마다 다음을 측정한다.

| 지표 | 질문 |
|---|---|
| code-following rate | 실제 code convention을 골랐는가? |
| inconsistency reporting | 충돌을 final report에 밝혔는가? |
| test pass rate | 기존 behavior를 보존했는가? |
| harmful rewrite rate | 문서에 맞추려 existing code를 망가뜨렸는가? |

적용 후보: [[tech/devtools/stale-agent-instructions/05-projects|Projects]] · 근거: [[tech/devtools/stale-agent-instructions/03-references|References]]

## Sources

- https://arxiv.org/abs/2610.30571
- https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/03/CSA_research_note_readme_instruction_injection_ai_coding_agents_20260317-csa-styled.pdf
