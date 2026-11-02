---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Agent·MCP·콘텐츠 자동화 시스템: 심화

[[tech/ai/ai-agent-automation-systems/README|README]] · 이전: [[tech/ai/ai-agent-automation-systems/04-learning/01-getting-started|시작하기]] · [[tech/ai/ai-agent-automation-systems/05-projects|Projects]]

## Context와 durable memory

| 저장물 | 내용 | 갱신 시점 |
|---|---|---|
| Project brief | 목표, 독자, 성공 기준, 금지 범위 | 프로젝트 변경 시 |
| Style guide | tone, 용어, 좋은/나쁜 예시 | 편집 검토 후 |
| Decision log | 결정, 근거, 담당자, 날짜 | 승인·변경 시 |
| Retrieval corpus | reference 문서와 metadata | source 갱신 시 |
| Run trace | input, tool call, output, cost, approval | 매 실행 |

## Approval 설계

외부 영향이 큰 action은 Agent가 직접 실행하지 않는다. Agent는 action proposal과 근거를 만들고, workflow가 정책을 확인한 뒤 승인된 경우만 실행한다.

```text
Agent proposal → policy validation → reviewer approval → action executor → immutable log
```

승인 화면에는 대상, 변경 내용, source, 예상 비용, 되돌리는 방법을 보여 준다. 삭제·결제·대량 발송은 별도의 강한 승인과 scope 제한이 필요하다.

## Evaluation과 관측

- **정확성**: citation이 실제 주장에 맞는가
- **도구 사용**: 적절한 tool을 최소 횟수로 호출했는가
- **안전성**: 금지된 write action 또는 민감 정보 노출이 없는가
- **운영성**: latency, token cost, retry rate, human override rate가 어떤가

대표 입력으로 작은 eval set을 만들고 변경 전후 결과를 비교한다. 실패의 원인이 prompt, context, tool schema, workflow 중 어디인지 trace로 구분한 후 수정한다.

## 콘텐츠 파이프라인

주제 조사 → short-form script → visual prompt → image/video asset → narration/caption → QA → human approval → scheduler → 성과 분석으로 나눈다. 사실성, 저작권, likeness, 광고 표기를 QA 기준에 포함한다.

## Sources

- https://docs.anthropic.com/en/docs/mcp
- https://docs.anthropic.com/en/docs/claude-code/cli-usage
- https://platform.openai.com/docs/assistants/migration

