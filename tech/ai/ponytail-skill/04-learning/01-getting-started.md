---
date: 2026-06-24
tags:
  - tech
  - ai
  - agent-skills
  - getting-started
  - ponytail
type: tech-tool-study
parent: "[[../README]]"
---

# ponytail skill - 시작하기

> [[../03-references|이전: 참고자료]] | [[../README|목차]] | [[02-deep-dive|다음: 심화]]

---

## 목표

`ponytail`을 공개 공식 skill로 가정하지 않고, Agent Skills 규격을 따르는 최소 custom skill로 만든다.

완료 기준:

- `ponytail/SKILL.md`가 존재한다.
- frontmatter에 `name: ponytail`, `description: ...`이 있다.
- agent가 언제 이 skill을 써야 하는지 판단할 수 있다.
- 간단한 test task로 activation 여부를 확인한다.

## 1. 위치 선택

Claude Code 기준으로는 `.claude/skills/ponytail/SKILL.md`, Agent Skills 호환 agent 기준으로는 `.agents/skills/ponytail/SKILL.md`처럼 둘 수 있다.

```bash
# Claude Code 스타일
mkdir -p .claude/skills/ponytail
touch .claude/skills/ponytail/SKILL.md

# Agent Skills 스타일
mkdir -p .agents/skills/ponytail
touch .agents/skills/ponytail/SKILL.md
```

## 2. 최소 SKILL.md 작성

`description`은 activation trigger다. “이 skill은 좋다”가 아니라 “이런 작업이면 사용하라”를 써야 한다.

```markdown
---
name: ponytail
description: Use this skill when the user asks to run the Ponytail workflow: validate inputs, apply the documented transformation steps, and report verification results. Do not use it for unrelated hair, fashion, or generic summarization tasks.
---

# Ponytail Skill

## Procedure

1. Identify the requested Ponytail workflow and required inputs.
2. Check whether all required inputs are present.
3. Apply the transformation or review checklist.
4. Validate the output against the acceptance criteria.
5. Report the result with assumptions, errors, and next steps.

## Inputs

| Input | Required | Notes |
|-------|----------|-------|
| task | yes | What the user wants the Ponytail workflow to do |
| source | optional | File, URL, or pasted content |
| output_format | optional | Markdown, JSON, table, report |

## Output

- Summary
- Steps performed
- Validation result
- Open issues
```

## 3. 나쁜 description 피하기

| 나쁜 예 | 문제 | 개선 |
|---------|------|------|
| `description: Helps with ponytail.` | activation 기준이 모호함 | 사용 조건과 제외 조건을 적는다 |
| `description: Use always.` | false positive 증가 | 특정 workflow에만 제한한다 |
| `description: Hair styling expert.` | 실제 skill 목적과 혼동 | 기술 workflow인지 domain workflow인지 명확히 한다 |

## 4. 첫 테스트

다음 3개 prompt로 activation을 관찰한다.

```text
1. Use the ponytail workflow to validate this output.
2. Summarize this article about ponytail hairstyles.
3. Create a PR review checklist using the Ponytail workflow.
```

예상:

| Prompt | 기대 |
|--------|------|
| 1 | skill 활성화 |
| 2 | 비활성화. 일반 머리 스타일 요약은 제외 |
| 3 | skill 목적이 PR review라면 활성화, 아니면 clarification |

## 5. 최소 평가표

| 평가 항목 | 질문 | 기록 |
|-----------|------|------|
| Activation | 켜져야 할 task에서 켜졌나? | pass/fail |
| False positive | 무관한 task에서 켜지지 않았나? | pass/fail |
| Output quality | 절차와 검증이 포함됐나? | pass/fail |
| Context cost | `SKILL.md`가 불필요하게 길지 않은가? | pass/fail |

## 관련 노트

- [[study/tech/ai/claude/05-skills]] - Claude Skills 사용 흐름
- [[study/tech/ai/codex]] - Codex 계열 지침/skill 운용 관점
- [[study/tech/ai/model-context-protocol-mcp]] - 외부 tool 연결이 필요할 때 비교

