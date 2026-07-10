---
date: 2026-07-11
tags:
  - tech
  - ai
  - codex
  - gpt-5-6
  - deep-dive
type: tech-tool-study
parent: "[[../README]]"
---

# GPT-5.6 in Codex - 심화

> [[01-getting-started|이전: 시작하기]] | [[../05-projects|다음: 프로젝트]]

---

## 목표

심화 단계에서는 GPT-5.6을 단순 chat/coding model로 보지 않고, **tool-heavy agent runtime**과 **multi-agent workflow**의 구성 요소로 이해한다.

## 1. Programmatic Tool Calling

Programmatic Tool Calling은 모델이 JavaScript를 작성/실행해 tool calls를 조율하는 방식이다. 핵심 이점은 tool output 전체를 매번 model context로 되돌리지 않고, code로 필터링/집계한 결과만 전달할 수 있다는 점이다.

### 일반 tool calling과 비교

| 방식 | 흐름 | 장점 | 주의점 |
|------|------|------|--------|
| 일반 tool calling | model이 tool 호출을 순차 결정 | 단순하고 투명함 | round trip/token 증가 |
| Programmatic Tool Calling | model이 code로 tool 호출과 필터링을 조율 | token/latency 절감, 복잡한 orchestration | sandbox, 권한, debugging 필요 |

```javascript
// 개념 예시: DB와 검색 tool을 조합해 후보를 줄인다.
const issues = await tools.github.searchIssues({ label: "bug", state: "open" });
const failures = await tools.ci.recentFailures({ branch: "main" });

const candidates = issues.filter((issue) =>
  failures.some((failure) => issue.title.includes(failure.testName))
);

return candidates.map((issue) => ({
  id: issue.id,
  title: issue.title,
  likelyTest: failures.find((failure) => issue.title.includes(failure.testName))?.testName
}));
```

### 적용하기 좋은 작업

- web/search/db 결과를 필터링한 뒤 요약하는 research agent.
- 여러 CI/test 결과를 조합해 root cause 후보를 좁히는 debugging agent.
- 긴 document set에서 규칙 기반 후보를 추리고 reasoning은 마지막에 쓰는 workflow.

## 2. Multi-agent beta

Codex의 `ultra`는 여러 agent를 병렬 조율하는 고성능 모드로 설명된다. API에서는 Responses API의 Multi-agent beta로 유사한 패턴을 직접 설계할 수 있다.

```text
Coordinator
  -> Frontend agent: UI 영향 조사
  -> Backend agent: API/schema 영향 조사
  -> Test agent: regression coverage 조사
  -> Security agent: auth/permission risk 조사
  -> Coordinator: 결과 병합, 최종 plan/diff/review
```

### 설계 원칙

- agent마다 책임 영역을 좁힌다.
- 같은 파일을 동시에 수정하기보다 조사/분석을 병렬화한다.
- 최종 merge/review는 coordinator가 수행한다.
- test command와 acceptance criteria를 shared context로 고정한다.

## 3. `max`와 `ultra`를 구분하기

| 기능 | 의미 | 사용 위치 |
|------|------|-----------|
| `max` | reasoning effort의 최상위 설정 | 어려운 단일 task의 quality-first reasoning |
| `ultra` | 여러 agent를 병렬 조율하는 Codex 고성능 모드 | 큰 작업을 나누고 병합하는 workflow |

`max`는 "한 모델이 더 깊게 생각하게 하는 설정"에 가깝고, `ultra`는 "여러 agent를 조율해 큰 작업을 처리하는 실행 방식"에 가깝다.

## 4. Safety와 운영 고려

GPT-5.6 system card는 Sol/Terra/Luna를 cyber 및 bio/chemical risk에서 High capability로 본다. 코딩 작업에서도 다음 경계를 명확히 해야 한다.

| 영역 | 운영 원칙 |
|------|-----------|
| Security hardening | defensive workflow로 제한하고 exploit automation은 피한다 |
| Secrets | Codex cloud/env secret 접근을 최소화한다 |
| Production change | PR review, CI, human merge gate를 둔다 |
| Tool permissions | destructive command, external side effect는 별도 승인/격리 |
| Monitoring | high-risk task는 log와 diff provenance를 남긴다 |

## 5. 평가 프레임

GPT-5.6 도입 효과는 모델 점수만으로 판단하지 않는다.

| 지표 | 질문 |
|------|------|
| Success rate | 같은 task를 완수하는 비율이 올랐는가? |
| Verification | test/lint/typecheck까지 실제로 실행했는가? |
| Diff quality | 변경 범위가 작고 review 가능한가? |
| Latency | 대기 시간이 workflow에 맞는가? |
| Cost | tier/effort 대비 비용이 정당한가? |
| Safety | 권한과 risk boundary가 명확한가? |

## 관련 노트

- [[study/tech/ai/model-context-protocol-mcp]] - tool/resource protocol과 Programmatic Tool Calling의 비교 축
- [[study/tech/ai/lazy-codex]] - agent 완료 검증과 false completion 방지
- [[study/tech/ai/litellm]] - tier/provider routing과 비용 측정

## References

- [Programmatic Tool Calling](https://developers.openai.com/api/docs/guides/tools-programmatic-tool-calling)
- [Multi-agent API beta](https://developers.openai.com/api/docs/guides/tools-multi-agent)
- [GPT-5.6 system card](https://deploymentsafety.openai.com/gpt-5-6)
