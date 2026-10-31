---
date: 2026-07-11
tags:
  - tech
  - ai
  - codex
  - gpt-5-6
  - references
type: tech-tool-study
parent: "[[README]]"
---

# GPT-5.6 / Codex 참고자료

> [[02-ecosystem|이전: 생태계]] | [[04-learning/01-getting-started|다음: 시작하기]]

---

## 공식 문서

| 구분 | 링크 | 확인 포인트 |
|------|------|-------------|
| Release | [OpenAI GPT-5.6 release](https://openai.com/index/gpt-5-6/) | GA 날짜, Sol/Terra/Luna, Codex/ChatGPT Work 제공, benchmark |
| Safety | [GPT-5.6 system card](https://deploymentsafety.openai.com/gpt-5-6) | cyber/bio/chemical High capability, safeguards, monitoring |
| Model guide | [OpenAI latest model guide](https://developers.openai.com/api/docs/guides/latest-model) | model tier, alias, reasoning effort, migration guidance |
| Tool calling | [Programmatic Tool Calling](https://developers.openai.com/api/docs/guides/tools-programmatic-tool-calling) | JavaScript 기반 tool orchestration, token/round trip 절감 |
| Multi-agent | [Multi-agent API beta](https://developers.openai.com/api/docs/guides/tools-multi-agent) | Responses API에서 multi-agent pattern 구현 |
| Codex product | [Codex product page](https://openai.com/codex/) | Codex surface, coding agent positioning |
| Codex cloud | [Codex cloud docs](https://learn.chatgpt.com/codex/cloud) | isolated cloud environments, GitHub/Linear/Slack task |
| Codex CLI | [Codex CLI docs](https://learn.chatgpt.com/codex/cli) | local project directory 실행, sign-in, agent loop |
| AGENTS.md | [AGENTS.md docs](https://learn.chatgpt.com/codex/agent-configuration/agents-md) | repo/team convention, lint/test/approval rule 고정 |

## 읽는 순서

1. **Release page**에서 "Codex 5.6"이 아니라 GPT-5.6 model family라는 이름과 tier를 확인한다.
2. **Latest model guide**에서 `sol/terra/luna`, `reasoning effort`, migration guidance를 본다.
3. **Codex CLI/cloud docs**에서 실제 Codex surface에 어떻게 적용되는지 본다.
4. **Programmatic Tool Calling**과 **Multi-agent beta**로 API에서 구현 가능한 agentic pattern을 확인한다.
5. **System card**에서 high capability risk와 운영 제한을 확인한다.

## 용어 사전

| 용어 | 설명 |
|------|------|
| Frontier reasoning model | 복잡한 추론과 계획을 수행하는 최신 고성능 모델군 |
| Agentic coding | 모델이 코드 탐색, 수정, 테스트, 리뷰를 연속 workflow로 수행하는 방식 |
| Reasoning effort | 모델이 추론에 배정하는 깊이/비용/시간 설정 |
| `max` | 품질 우선의 어려운 task용 reasoning effort |
| `ultra` | Codex에서 여러 agent를 병렬 조율하는 고성능 모드 |
| Programmatic Tool Calling | 모델이 code를 작성/실행해 tool calls를 조율하는 방식 |
| Multi-agent beta | Responses API에서 여러 agent role을 구성하는 beta 기능 |
| Codex cloud | 격리된 cloud environment에서 repo task를 실행하는 Codex runtime |

## 관련 노트

- [[study/tech/ai/lazy-codex]] - Codex agent의 완료 검증과 신뢰성 문제
- [[study/tech/ai/model-context-protocol-mcp]] - tool/resource discovery와 agent integration 표준
- [[study/tech/ai/litellm]] - model selection/routing 관점
