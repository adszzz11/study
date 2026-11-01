---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Agent Skills 시작하기

## 목표

`merged PR`을 분류하고 customer-facing release note 초안을 만드는 작은 `release-notes` Skill을 설계한다. 처음에는 workflow 하나만 다루고, 검증 가능한 산출물을 만든다.

## 1. 좁은 workflow 선택

좋은 첫 후보는 빈도가 높고 입력·출력·완료 조건이 명확하다.

| 항목 | 예시 |
|---|---|
| 입력 | merged PR 목록, label, 변경 diff |
| 출력 | 분류된 release note Markdown |
| 품질 기준 | customer-facing 문장, breaking change 누락 없음 |
| 실패 시 | 정보가 모자라면 추정하지 않고 질문 목록 생성 |

## 2. 명확한 trigger 작성

모호한 `description`은 잘못된 routing을 부른다.

```yaml
---
name: release-notes
description: Use when classifying merged pull requests and drafting customer-facing release notes for a release.
---
```

`release note 작성 시 사용`보다 task, 입력, 기대 산출물을 함께 표현한 description이 낫다.

## 3. 최소 `SKILL.md` 작성

```markdown
---
name: release-notes
description: Use when classifying merged pull requests and drafting customer-facing release notes for a release.
---

# Release notes workflow
1. PR 제목, label, linked issue와 diff를 읽는다.
2. feature, fix, breaking change, internal로 분류한다.
3. customer-facing 항목만 짧고 검증 가능한 문장으로 쓴다.
4. breaking change와 불명확한 항목은 별도 확인 목록에 남긴다.
```

## 4. 평가하고 수정

- 실제 release 3~5개에서 Skill 사용/미사용 결과를 비교한다.
- false positive trigger, 누락된 failure mode, 애매한 품질 기준을 기록한다.
- 반복 계산은 prose에 쌓지 말고 `scripts/`로 옮긴다.

## Related Notes

- [[tech/ai/agent-skills-ecosystem/README|Agent Skills README]]
- [[tech/ai/agent-skills-ecosystem/01-overview|Overview]]
- [[tech/ai/agent-skills-ecosystem/04-learning/02-deep-dive|Deep Dive]]
- [[tech/ai/agent-skills-ecosystem/05-projects|Projects]]

## Sources

- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- https://developers.openai.com/api/docs/guides/tools-skills
