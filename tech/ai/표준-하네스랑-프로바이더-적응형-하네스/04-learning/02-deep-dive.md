---
date: 2026-09-09
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep dive — 상태 보존·복구·평가

[학습 진입점](../README.md) · 이전: [Getting started](01-getting-started.md) · 다음: [Projects](../05-projects.md)

## 1. Portable State와 Native State 분리

다음 구조는 API별 차이에서 도출한 설계 제안이다. **작업 사실은 이식 가능하게, opaque protocol 상태는 원형대로** 관리한다.

| 상태 | 내용 | 모델·provider 전환 시 |
|---|---|---|
| Portable task state | 목표·제약·확인된 사실·산출물·검증 결과·미완료 항목 | 재검증 후 새 context 구성에 사용 |
| Native continuation state | response IDs·reasoning items·thinking blocks·signatures | 호환성이 확인된 API·모델 경로에서만 사용 |
| Operational state | 예산 사용량·취소·tool 실행 결과·재시도 상태 | 전환 후에도 유지하여 예산 초기화·중복 실행 방지 |

OpenAI Responses는 `previous_response_id` 또는 필요한 response items의 재전달을 통해 상태를 이어간다. Claude Messages의 tool-use turn은 필요한 `thinking`·`redacted_thinking` blocks를 보존해야 한다. Gemini의 `generateContent` signatures와 Interactions의 `thought` steps도 동일 schema로 취급하지 않는다. [OpenAI](https://developers.openai.com/api/docs/guides/reasoning) · [Claude](https://platform.claude.com/docs/en/build-with-claude/thinking) · [Generate Content](https://ai.google.dev/gemini-api/docs/generate-content/thought-signatures) · [Interactions](https://ai.google.dev/gemini-api/docs/thought-signatures)

공통 이벤트로 정규화할 때에도 native payload는 별도 저장한다. adapter에서 state를 serialize한 뒤 다시 읽는 round-trip 검증은 텍스트 비교만이 아니라 block 종류·순서·tool call 연결 관계를 확인해야 한다.

## 2. Profile 선택과 버전 관리

아래 YAML은 **개념 schema**이며 Deep Agents에 그대로 전달하는 설정 파일이 아니다. 실제 제품의 등록 키와 별도로 application이 추적할 정보를 보여준다.

```yaml
profile_id: paged-reader-v1
selector:
  provider: example-provider
  api: example-api
  model_version: pinned-model-version
  required_capabilities: [tool_calling]
behavior:
  explain_pagination: true
  verify_before_completion: true
evaluation:
  suite_version: paged-read-v1
  baseline_profile: baseline-v1
  report_ref: evaluation-report
```

- 정확한 model/API 조합에서 평가된 profile을 먼저 선택한다.
- 미등록 모델에는 별도 검증 없는 최적화 profile을 무조건 상속하지 않는다.
- 적용된 최종 설정을 기록하여 provider 기본값과 model override의 영향을 추적한다.
- 필수 권한 검사·sandbox·예산 제한은 profile이 해제할 수 없는 core 정책으로 둔다.
- 모델 교체 시 기존 profile 유지, 보정 제거, 새 profile을 각각 비교한다.

모델·provider에 따라 설정을 패키징하는 실제 예는 [Deep Agents Profiles](https://docs.langchain.com/oss/python/deepagents/profiles)를 참고한다. 위 selector schema는 그 제품의 공식 기능 명세가 아니다.

## 3. Context Compaction과 장기 작업

Compaction은 오래된 내용을 무조건 삭제하는 기능이 아니라 다음 행동에 필요한 정보를 남기는 정책이다. 다음 checkpoint는 portable state의 예시다.

```json
{
  "task_id": "paged-read-001",
  "goal": "Collect all required values",
  "verified_facts": ["Page 0 was read successfully"],
  "artifacts": [{"path": "result.json", "verified": false}],
  "pending": ["Read page 1", "Run verifier"],
  "last_completed_tool_call": "call-001",
  "tool_calls_used": 1,
  "tool_calls_remaining": 2
}
```

장기 실행에서는 새 세션이 진행 기록과 artifact를 확인하고 다음 작업을 이어가게 한다. Anthropic의 initializer·진행 기록·Git history 활용이 참고 사례다. 다만 모델 변경 후 context reset을 제거한 사례도 있으므로 reset 주기를 고정된 최적값으로 취급하지 않는다. [장기 실행 사례](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) · [모델 변경 후 설계 조정](https://www.anthropic.com/engineering/harness-design-long-running-apps)

## 4. Failover와 Retry는 다른 문제

권장 복구 순서:

1. 오류를 transport, protocol/state, tool, verification, budget/cancel로 분류한다.
2. 중단된 tool이 실제 실행됐는지 확인하고 결과가 불명확한 쓰기 작업을 무작정 반복하지 않는다.
3. 호환성이 유지되는 일시적 오류만 남은 예산 안에서 제한적으로 retry한다.
4. provider를 바꿀 때에는 native continuation state를 직접 이식하지 않는다.
5. 확인된 사실·artifact·미완료 항목·남은 예산으로 새 context를 구성한다.
6. 새 실행의 결과도 동일 verifier로 확인한다.

| 증상 | 먼저 확인할 곳 | 대응 방향 |
|---|---|---|
| tool 결과 전송 뒤 400 | 필수 blocks/signature·call ID·순서 | adapter의 protocol 보존 수정 |
| 파일 뒷부분 누락 | pagination metadata와 모델의 해석 | tool presentation/profile 실험 |
| “완료”했으나 결과 불충족 | acceptance criteria·verifier | 완료 후보와 검증 통과 분리 |
| 재개 후 같은 쓰기 반복 | checkpoint·tool 실행 기록 | side effect 확인 후 재개 |
| 새 모델이 더 느려짐 | 오래된 prompt·middleware·reset | 한 항목씩 제거하는 ablation |

## 5. Profile 효과를 검증하는 실험

| 조건 | 모델 | Profile | 질문 |
|---|---|---|---|
| A | M1 | baseline | 원래 성능은? |
| B | M1 | adapted | 같은 모델에서 profile 효과는? |
| C | M2 | baseline | 모델 변경 효과는? |
| D | M2 | adapted | 적응 효과가 다른 모델에도 이전되는가? |

과제·tool 권한·verifier·예산·환경을 같게 하고 모델이 지원하는 설정을 기록한다. 모델별 실제 토큰 사용과 비용이 같다고 가정하지 않는다. 반복 측정 결과의 성공 건수/전체 건수와 분산을 보고, 표본이 작으면 그 한계를 명시한다. A와 D만 비교하면 모델과 profile 효과를 분리할 수 없다.

- **Ablation**: prompt 보정, tool 설명, middleware를 한 번에 하나씩 제거해 기여도를 본다.
- **Regression**: 기존에 통과하던 짧은 과제·긴 과제·취소·복구가 깨지지 않는지 본다.
- **Holdout**: profile을 고치는 데 사용하지 않은 과제로 최종 확인한다.
- **기록 항목**: task ID, run ID, model/API/version, profile hash, verifier version, 성공 여부, 시간, 토큰, 비용, tool 호출 수, 실패 유형.
- **채택 조건**: 사전에 정한 성공률·비용·지연 기준을 통과한 경우에만 profile을 교체하고 이전 버전을 남긴다.

HarnessDev는 모델에 따라 harness 이전이 제한적이라고 보고한 **preprint**다. 위 실험표는 그 문제의식을 반영한 학습용 설계이며 논문의 실험 절차를 복제한 것은 아니다. [HarnessDev](https://arxiv.org/abs/2609.01437)

## Sources

- [OpenAI Reasoning](https://developers.openai.com/api/docs/guides/reasoning)
- [Claude Thinking](https://platform.claude.com/docs/en/build-with-claude/thinking)
- [Gemini Generate Content signatures](https://ai.google.dev/gemini-api/docs/generate-content/thought-signatures)
- [Gemini Interactions thinking](https://ai.google.dev/gemini-api/docs/thought-signatures)
- [Deep Agents Profiles](https://docs.langchain.com/oss/python/deepagents/profiles)
- [Anthropic: Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Anthropic: Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- [LangChain: Harness engineering](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering)
- [HarnessDev — preprint](https://arxiv.org/abs/2609.01437)
