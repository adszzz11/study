---
date: 2026-10-11
tags: [tech]
type: tech-tool-study
status: draft
---

# DeerFlow — 심화

> [[../README|목차로 돌아가기]] | [[01-getting-started|이전: 시작하기]]

## 1. Delegation 설계

subagent는 main thread를 길게 만드는 수단이 아니라, 독립 context에서 검증 가능한 하위 결과를 만드는 boundary다.

```text
Lead Agent
 ├─ general-purpose: 경쟁사 문서 조사
 ├─ general-purpose: release note 변화 추출
 └─ bash: 허용된 workspace에서 표·chart artifact 생성
                 ↓
          Lead Agent가 source·artifact를 종합
```

각 task에는 목표, 허용 source/tool, 기대 산출물, 완료 기준을 넣는다. subagent output은 신뢰된 사실이 아니라 검토 대상 evidence로 취급한다.

## 2. Middleware와 Config

middleware chain은 모델 호출의 전후에 summarization, memory, guardrail, tool policy를 결합한다. 변경은 한 번에 여러 개를 하지 말고 다음처럼 실험한다.

1. 기준 config와 task set을 고정한다.
2. middleware 또는 tool group 하나만 바꾼다.
3. task success, citation fidelity, tool error rate, cost, latency를 비교한다.
4. 결과가 나쁘면 config를 되돌리고 로그에서 failure mode를 분류한다.

## 3. Memory와 Durable State

checkpoint는 실행 재개에, memory는 이후 turn에 필요한 정보를 선택적으로 제공하는 데 쓰인다. 둘을 같은 것으로 취급하지 않는다.

| 구분 | 질문 | 점검 |
|---|---|---|
| checkpoint | 중단된 graph를 재개할 수 있는가? | DB backup, schema migration, recovery test |
| application data | 프로젝트·대화가 올바르게 분리되는가? | tenant/project authorization |
| memory | 오래된 요약이 잘못된 결론을 강화하지 않는가? | expiry, source link, correction path |

## 4. Production Boundary

v2.1 계열의 durable batch delegation, pluggable memory backend, extension system, auth/authz, project·conversation branching은 기능 도입 자체보다 운영 경계를 검증해야 한다는 신호다.

- multi-user 환경에서는 LocalSandbox 대신 격리된 provider를 선택한다.
- custom agent마다 skill·tool group을 whitelist하고 credential을 분리한다.
- 외부 write, deploy, 결제, production command는 human approval 뒤에 실행한다.
- untrusted web page/PDF의 instruction은 data로 취급하고 prompt injection을 검사한다.
- checkpoint DB, artifact storage, audit log의 보존·backup·삭제 정책을 문서화한다.

## Evaluation Matrix

| 축 | 측정 예 |
|---|---|
| 품질 | task success, citation fidelity, artifact correctness |
| 안정성 | retry 성공률, resume 성공률, tool error rate |
| 보안 | denied action 동작, sandbox escape test, secret leak 여부 |
| 운영 | p95 latency, token/tool cost, trace와 audit completeness |

## Sources

- https://deerflow.tech/en/docs/harness/design-principles
- https://deerflow.tech/en/docs/harness/subagents
- https://deerflow.tech/en/docs/tutorials/work-with-memory
- https://github.com/bytedance/deer-flow/releases
