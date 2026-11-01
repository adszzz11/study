---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기 — 작은 검증 루프 만들기

## 1. 단일 loop부터 완주

공식 경로로 Claude Code를 설치한 뒤 빈 Git repository에서 `plan → implement → test → review`를 한 번 끝낸다. 시작부터 다수 agent와 MCP를 연결하면 실패 원인을 분리하기 어렵다.

## 2. 설치 없이 역할 분리 실험

다음 prompt로 독립 조사와 반증을 먼저 연습한다.

```text
독립적인 3개 가설을 제시하고, 각 가설의 반증 근거를 찾은 뒤,
신뢰도와 출처 URL을 포함한 하나의 권고안을 작성하라.
```

결과에서 확인할 것:

- 가설마다 실제로 독립된 근거가 있는가?
- 반증이 형식적인 문장이 아니라 결론을 바꿀 수 있는가?
- 권고안이 출처와 불확실성을 분명히 드러내는가?

## 3. 반복될 때만 Skill로 승격

`research-with-citations`처럼 좁은 목적을 고른다. 입력, 절차, 출력 형식, 금지 사항, 완료 기준을 적고 실제 두세 번의 사용 후에만 일반화한다.

```markdown
# research-with-citations
Input: research question, date range
Process: collect independent sources; record counter-evidence
Output: claim / URL / confidence / unknowns
Done: every material claim has a source or is labelled inference
```

## Related Notes

- [[tech/ai/claude-code-skill-workflows/README|README]]
- [[tech/ai/claude-code-skill-workflows/04-learning/02-deep-dive|Deep Dive]]
- [[tech/ai/claude-code-skill-workflows/cheatsheet|Cheatsheet]]

## Sources

- https://docs.anthropic.com/en/docs/claude-code/getting-started
- https://docs.anthropic.com/en/docs/claude-code/cli-usage
