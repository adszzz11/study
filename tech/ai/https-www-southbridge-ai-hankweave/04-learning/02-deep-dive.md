---
date: 2026-06-24
tags:
  - tech
  - ai
  - hankweave
  - deep-dive
  - agent-runtime
type: tech-tool-study
parent: "[[../README]]"
---

# Hankweave - 심화

> [[01-getting-started|이전: 시작하기]] | [[../README|목차로 돌아가기]] | [[../05-projects|다음: 프로젝트]]

---

## 1. Codon boundary 설계

Codon은 단순 step이 아니라 **수리 가능한 작업 단위**다. 너무 크게 잡으면 실패 원인과 rollback 지점이 흐려지고, 너무 작게 잡으면 handoff file과 overhead가 늘어난다.

| Boundary 기준 | 좋은 예 | 나쁜 신호 |
|---------------|---------|-----------|
| 산출물 | `work/research.md`, `results/report.md`처럼 명확한 output | "계속 조사"처럼 완료물이 모호함 |
| 검증 | 다음 codon/sentinel이 검사할 수 있음 | agent 내부 판단에만 의존 |
| 비용 | codon별 budget을 추정 가능 | 한 codon이 전체 비용 대부분을 소모 |
| 복구 | 실패 시 해당 codon만 재실행 가능 | 실패하면 처음부터 다시 해야 함 |

## 2. Context firewalling

`continuationMode: "fresh"`는 "이전 대화를 버리고 필요한 파일만 읽게 하는" 방식이다. 이는 long-context accumulation을 줄이지만 handoff file 품질이 중요해진다.

```text
Codon A context
  -> output: work/findings.md

Codon B fresh context
  -> reads: work/findings.md
  -> does not inherit Codon A hidden conversation state
```

Handoff file에 포함할 것:

- 결정사항과 근거
- source/citation
- unresolved question
- 다음 codon이 반드시 지켜야 할 constraint
- machine-readable checklist 또는 JSON section

## 3. Checkpoint와 rollback 정책

Hankweave는 codon 완료 시 Git commit 기반 snapshot을 만든다. 따라서 generated file 정책이 중요하다.

| 정책 | 권장 |
|------|------|
| 입력 데이터 | read-only mount 또는 별도 `data/` 경계 |
| 작업 중간물 | `work/`에 저장하고 checkpoint 포함 여부 명시 |
| 최종 산출물 | `results/` 또는 `/results` volume으로 export |
| 실행 상태 | `/executions` volume에 유지해 resume 가능하게 관리 |
| 운영 repo | agent가 만든 checkpoint commit과 사람이 관리하는 source commit을 혼동하지 않게 분리 |

## 4. Sentinel 설계

Sentinel은 main agent를 방해하지 않고 event stream을 관찰한다. 가장 효과적인 sentinel은 "좋은 조언"보다 **구체적 failure mode**를 감시한다.

| Sentinel | 감지 대상 | 출력 예 |
|----------|-----------|---------|
| Citation sentinel | source 없는 주장, missing citation | `sentinels/citation-report.json` |
| Cost sentinel | token/cost spike, budget proximity | `sentinels/cost-alert.md` |
| Drift sentinel | initial goal과 다른 방향으로 이동 | `sentinels/drift-summary.md` |
| Convention sentinel | repo style, schema, naming 위반 | `sentinels/convention-violations.json` |

Sentinel prompt는 다음처럼 좁게 만든다.

```text
Observe the event stream only for missing citations in final claims.
Do not rewrite the report.
Emit JSON with claim, reason, severity, suggested_source_location.
```

## 5. Event journal과 observability

Hankweave의 structured JSONL event journal은 long run을 사람이 조사할 수 있는 audit trail로 만든다.

확인할 질문:

- 어느 codon에서 비용이 급증했는가?
- 어떤 file이 checkpoint에 포함되었는가?
- sentinel이 어떤 event 이후 경고를 냈는가?
- failure policy가 retry, stop, rollback 중 무엇을 택했는가?

```bash
# 예시: event journal에서 codon별 cost를 조사하는 식의 운영 관점
jq 'select(.type == "cost") | {codon, dollars, tokens}' executions/*/events.jsonl
```

## 6. Docker/CI 운영 패턴

Docker/CI에서는 execution state와 final artifact를 분리한다.

```text
container
  /workspace   -> source checkout
  /data        -> read-only dataset mount
  /executions  -> resume/checkpoint state volume
  /results     -> final artifact export volume
```

```bash
bunx hankweave@latest --headless --autostart --max-cost 10
```

CI에서 특히 볼 것:

- validation을 별도 step으로 먼저 실행
- `/executions` volume을 보존해 resume 가능하게 구성
- `/results`를 artifact로 업로드
- sentinel report를 failure annotation으로 노출
- budget 초과를 hard failure로 처리

## 7. 설계 체크리스트

- [ ] 각 codon은 독립적으로 설명 가능한 output을 만든다.
- [ ] 다음 codon의 입력은 file로 명시된다.
- [ ] `fresh` context가 기본이고, 필요한 경우에만 continuation을 쓴다.
- [ ] checkpointed/output files가 분리되어 있다.
- [ ] sentinel은 하나의 failure mode만 감시한다.
- [ ] preflight validation을 CI 앞단에 둔다.
- [ ] run-level `--max-cost`와 codon-level `budget.maxDollars`를 같이 둔다.

## 관련 노트

- [[study/tech/ai/model-context-protocol-mcp]] - harness가 사용할 external tool/resource 경계
- [[study/tech/ai/agent-orchestration]] - long-running agent workflow 설계
- [[study/tech/infra/prefect]] - data pipeline task boundary와 비교
