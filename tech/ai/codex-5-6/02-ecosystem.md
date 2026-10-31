---
date: 2026-07-11
tags:
  - tech
  - ai
  - codex
  - gpt-5-6
  - ecosystem
type: tech-tool-study
parent: "[[README]]"
---

# GPT-5.6 / Codex 생태계 비교

> [[01-overview|이전: 개요]] | [[03-references|다음: 참고자료]]

---

## 1. 포지션

GPT-5.6은 model API 하나만의 문제가 아니라 Codex, ChatGPT Work, Responses API, cloud task workflow까지 걸친 **agentic work model line**이다. 그래서 비교 대상도 단순 LLM benchmark보다 coding agent, IDE workflow, multi-agent orchestration, tool calling runtime까지 포함해야 한다.

## 2. 주요 경쟁/대안

| 축 | GPT-5.6 / Codex | Claude 계열 | Gemini 계열 | GitHub Copilot/Agent HQ |
|---|---|---|---|---|
| 주 포지션 | Codex, ChatGPT Work, API 전반의 agentic work model | Claude Code/Cowork 계열 coding agent | Gemini coding/general model | GitHub workflow 안의 multi-agent hub |
| 강점 | Codex와 직접 결합, `max/ultra`, Programmatic Tool Calling, Multi-agent beta | coding agent 시장에서 강한 존재감 | Google ecosystem, multimodal/infra 통합 | PR/issue/VS Code workflow에 밀착 |
| 비용/효율 | Sol/Terra/Luna tier로 token/latency/cost 최적화 주장 | 모델별 상이 | 모델별 상이 | 모델 선택/agent orchestration layer |
| Codex와의 관계 | 1st-party runtime | 직접 경쟁 | 대안 모델/agent | Codex, Claude, Copilot을 함께 배치 가능 |

## 3. 벤치마크 해석

dossier 기준 공식 benchmark table에서 GPT-5.6 Sol은 다음 수치를 제시한다.

| Benchmark | GPT-5.6 Sol 수치 | 해석 |
|-----------|------------------|------|
| Artificial Analysis Coding Agent Index | 80 | coding agent 종합 지표에서 높은 포지션 |
| Terminal-Bench 2.1 | 88.8% | terminal 기반 task 수행 능력 강조 |
| DeepSWE | 72.7% | software engineering benchmark에서 강한 성능 |

다만 SWE-Bench Pro에서는 일부 Claude 계열 수치가 더 높게 제시되어 있다. 따라서 "모든 coding benchmark에서 절대 우위"라고 보기보다, **agentic workflow, efficiency, Codex integration까지 포함한 종합 업그레이드**로 보는 편이 정확하다.

## 4. 선택 기준

| 상황 | 우선 후보 | 이유 |
|------|-----------|------|
| Codex CLI/cloud를 이미 쓰는 팀 | GPT-5.6 in Codex | 1st-party integration, `AGENTS.md`, GitHub/PR workflow |
| 긴 refactor와 test loop | `gpt-5.6-sol` + `high/max` | quality-first reasoning과 codebase 탐색 |
| 반복 업무 자동화 | `gpt-5.6-terra` | 비용/성능 균형 |
| 대량 triage/변환 | `gpt-5.6-luna` | high-volume low-cost |
| GitHub 중심 PR/issue 운영 | Copilot/Agent HQ도 비교 | repo workflow native integration |
| Claude Code 중심 팀 | Claude 계열과 실측 비교 | 기존 agent workflow와 prompt 자산이 있을 수 있음 |

## 5. Codex와 주변 계층

```text
Developer workflow
  -> Codex CLI / IDE / Cloud
      -> GPT-5.6 Sol/Terra/Luna
      -> AGENTS.md conventions
      -> GitHub PR / diff review / test execution

API workflow
  -> Responses API
      -> Programmatic Tool Calling
      -> Multi-agent beta
      -> external tools/search/db/browser
```

### 함께 볼 기술

- **MCP(Model Context Protocol)**: tool/resource를 표준 protocol로 노출하는 integration layer.
- **LiteLLM**: 여러 provider/model을 routing하는 gateway layer.
- **Agent orchestration tools**: 여러 CLI agent나 cloud agent 작업을 병렬 운영하는 layer.
- **PR review automation**: backward compatibility, security, test gap 중심의 review workflow.

## 관련 노트

- [[study/tech/ai/model-context-protocol-mcp]] - Codex/API tool integration과 연결되는 protocol layer
- [[study/tech/ai/litellm]] - GPT-5.6, Claude, Gemini를 gateway에서 비교/라우팅하는 관점
- [[study/tech/ai/agent-orchestration/cli-agents]] - Codex/Claude Code 등 CLI agent 운영 맥락

## References

- [OpenAI GPT-5.6 release](https://openai.com/index/gpt-5-6/)
- [OpenAI latest model guide](https://developers.openai.com/api/docs/guides/latest-model)
- [Multi-agent API beta](https://developers.openai.com/api/docs/guides/tools-multi-agent)
- [Codex product page](https://openai.com/codex/)
