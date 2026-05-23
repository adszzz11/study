# Part 5. Swarm 학습용 예제

> 모두 학습용. 프로덕션은 Agents SDK로 가기.

## 🟢 P1. 고객 응대 triage (★)

```
user → triage → {sales | support | refunds}
```

OpenAI Cookbook의 대표 예제. 핸드오프 + context_variables 동시 학습.

## 🟢 P2. 책상 비서 (★)

3-agent: scheduler / mailer / reminder. 핸드오프로 작업 위임.

## 🟡 P3. RAG over multiple knowledge bases (★★)

각 KB마다 specialist agent. triage가 적합한 KB로 핸드오프.

## 🟡 P4. Swarm → Agents SDK 1:1 포팅 실습 (★★)

같은 시나리오를 두 API로 작성하면서 차이 체득. 가장 학습 효과 큼.

## ⚠️ Best Practices (학습용)

- `max_turns` 명시 (5-10)
- 각 에이전트 instructions에 "위임 후엔 답하지 말 것" 명시
- context_variables 단순하게 유지
- 학습 끝나면 Agents SDK로 옮기기
