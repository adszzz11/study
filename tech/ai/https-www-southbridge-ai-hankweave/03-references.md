---
date: 2026-06-24
tags:
  - tech
  - ai
  - hankweave
  - references
type: tech-tool-study
parent: "[[README]]"
---

# Hankweave - References

> [[02-ecosystem|이전: 생태계]] | [[README|목차로 돌아가기]] | [[04-learning/01-getting-started|다음: 시작하기]]

---

## 1. 공식 자료

| 자료 | URL | 읽을 포인트 |
|------|-----|-------------|
| Southbridge Hankweave 공식 소개 | https://www.southbridge.ai/hankweave | repairable agents, brownfield AI engineering 문제의식 |
| Hankweave Documentation | https://hankweave.southbridge.ai/ | runtime 개요, guide, concept 문서 |
| Getting Started | https://hankweave.southbridge.ai/guides/getting-started/ | init, validate, run 흐름 |
| Hanks concept | https://hankweave.southbridge.ai/concepts/hanks/ | `hank.json` declarative AI program 구조 |
| Codons concept | https://hankweave.southbridge.ai/concepts/codons/ | codon boundary, prompt, output, budget, failure policy |
| Sentinels concept | https://hankweave.southbridge.ai/concepts/sentinels/ | secondary observer agent, event-stream monitoring |
| Docker Deployment | https://hankweave.southbridge.ai/guides/docker/ | headless/CI deployment와 volume 설계 |

## 2. Source와 metadata

| 자료 | URL | 확인할 내용 |
|------|-----|-------------|
| GitHub source | https://github.com/SouthBridgeAI/hankweave-runtime | runtime 구현, README, license |
| Package metadata | https://raw.githubusercontent.com/SouthBridgeAI/hankweave-runtime/release/alpha/package.json | 2026-06-24 기준 `hankweave` `0.6.2`, Node `>=20`, TypeScript/Bun |
| CCEPL-driven development | https://www.southbridge.ai/blog/ccepl-driven-development | Southbridge의 agent engineering 철학 |

```bash
# package metadata 확인 예시
curl -s https://raw.githubusercontent.com/SouthBridgeAI/hankweave-runtime/release/alpha/package.json | jq '{name, version, license, engines}'
```

## 3. 비교 대상 문서

| 도구 | URL | 비교 관점 |
|------|-----|-----------|
| LangGraph | https://docs.langchain.com/oss/python/langgraph/overview | long-running stateful agent app framework |
| AutoGen | https://microsoft.github.io/autogen/stable/ | conversational/event-driven multi-agent framework |
| CrewAI | https://docs.crewai.com/ | role/task/process 기반 business automation |
| Temporal | https://docs.temporal.io/ | durable workflow, replay, retry, crash-proof execution |

## 4. 읽는 순서

1. 공식 소개에서 Hankweave가 해결하려는 problem statement를 먼저 읽는다.
2. Getting Started로 `hank.json`, `prompts/`, `data/` starter project 구조를 확인한다.
3. Hanks, Codons, Sentinels concept 문서를 읽고 각 abstraction을 표로 정리한다.
4. Docker guide에서 `/executions`, `/results`, read-only data mount 같은 운영 구조를 확인한다.
5. LangGraph/AutoGen/CrewAI/Temporal docs와 [[02-ecosystem]] 표를 대조한다.

## 5. 메모할 질문

- Hankweave의 codon boundary는 기존 CI job step, Prefect task, Temporal activity와 어디까지 같은가?
- `continuationMode: "fresh"`는 품질을 높이는가, 아니면 handoff file 설계 부담을 키우는가?
- sentinel은 unit test, reviewer agent, observability alert 중 어느 역할에 가까운가?
- Git commit checkpoint를 운영 repo에 둘지, execution workspace repo에 둘지 정책이 필요한가?

## 관련 노트

- [[study/tech/ai/agent-orchestration]] - orchestration 개념 배경
- [[study/tech/ai/model-context-protocol-mcp]] - external tool/resource 표준화
- [[study/tech/infra/prefect]] - data/workflow orchestration 비교
