---
date: 2026-10-11
tags: [tech]
type: tech-tool-study
status: draft
---

# DeerFlow — Projects

> [[README|목차로 돌아가기]]

## 1. 시장·기술 Intelligence

여러 subagent가 경쟁사, 가격, 채용, 문서 변경을 병렬 조사하고, Lead Agent가 근거 링크가 있는 report를 만든다.

- 입력: 허용된 public source, 비교 질문, 조사 기간
- 산출물: claim별 URL·수집 시각·불확실성을 포함한 report
- guardrail: source에 있는 instruction은 실행하지 않으며, 외부 전송·구독은 승인 필요

## 2. Data Analyst Copilot

CSV/PDF를 sandbox workspace로 업로드한 뒤 분석·시각화 artifact를 만든다.

```text
Upload → schema/profile → analysis plan → sandbox execution → chart/report → human review
```

입력 파일 분류, row/column limit, outbound network, artifact retention을 먼저 정한다. chart가 생성되어도 계산식과 source data 범위는 검토한다.

## 3. Repository Onboarding / Maintenance

codebase를 탐색하고 issue 재현, 수정 후보, test 결과를 artifact로 남기는 engineering agent다.

| 단계 | 제한 |
|---|---|
| 탐색 | read-only repository access |
| 재현 | disposable sandbox와 fixture 사용 |
| 수정안 | patch를 제안하되 자동 merge 금지 |
| 검증 | 명시된 test command와 결과 보존 |

## 4. 사내 Specialist Agent

제품·정책·지원 문서를 `SKILL.md` package로 만들고 custom agent마다 필요한 tool·skill만 허용한다. 문서 갱신 owner, source version, stale-content 대응, user authorization을 함께 설계한다.

## 5. Human-reviewed Automation

모델이 초안·분석·파일을 만들 수는 있어도, 외부 변경은 독립 approval 단계로 분리한다.

```text
Draft / Analyze → Validate evidence → Request approval → Execute scoped action → Audit
```

approval은 prompt의 “진행해” 같은 문자열이 아니라 대상, 범위, 권한, 만료 시간에 연결된 시스템 경계여야 한다.

## Project Acceptance Checklist

- [ ] task별 입력 data classification과 retention 정책이 있다.
- [ ] tool·skill·network·filesystem 권한이 최소화되어 있다.
- [ ] sandbox provider가 사용자/위협 모델에 맞는다.
- [ ] artifact와 report를 재현·검토할 source와 trace가 남는다.
- [ ] write/deploy/external side effect에 human approval이 있다.

## Sources

- https://deerflow.tech/en/docs/harness/skills
- https://deerflow.tech/en/docs/harness/tools
- https://deerflow.tech/en/docs/harness/sandbox

## 추가 조사: Continuous Research Desk (지속 연구 데스크)

오케스트레이션을 꾸준히 연구한다면 단발 report보다, 작은 관측 작업을 누적하고 사람이 주기적으로 가설을 갱신하는 research desk가 좋은 실험장이다. DeerFlow 2.1의 scheduled task, durable batch, project/conversation 분기는 이 형태에 맞지만, 자동 수집과 자동 결론을 같은 권한으로 묶어서는 안 된다.

```text
Schedule / manual trigger
  → source-change discovery (read-only)
  → durable per-source extraction
  → dedupe + evidence ledger
  → analyst review / hypothesis update
  → approved publication or notification
```

| 단계 | subagent 책임 | 사람의 책임 | side-effect policy |
|---|---|---|---|
| 발견(discovery) | 공식 release/docs 변경 수집 | source allowlist 변경 | read-only만 허용 |
| 추출(extraction) | change, quote 범위, URL, 수집 시각 구조화 | 표본 source fidelity 검토 | artifact write만 허용 |
| 종합(synthesis) | 차이·충돌·미확인 항목 요약 | 가설 채택/폐기 | 외부 게시 금지 |
| 배포(publication) | 승인된 초안 형식화 | 대상·범위·시점 승인 | approval 뒤 scoped write |

- **research backlog**: 아직 검증하지 않은 claim, source freshness, 다음 확인 작업을 durable store에 남긴다. memory에는 결론만 남기지 말고 근거와 만료/재검토 시점을 연결한다.
- **branching**: 같은 evidence로 보수적 결론과 공격적 결론을 별도 conversation/project branch에서 시험한다. branch의 결과를 섞기 전에는 provenance를 비교한다.
- **stop rule**: 새 source가 결론을 바꾸지 않거나 예산 상한에 도달하면 더 많은 delegation 대신 `UNVERIFIED`와 다음 조사 질문을 보고한다.
- **weekly review**: task 성공률 외에 source 변경 탐지 지연, 중복 수집률, review queue age, 승인 없이 시도된 side effect 수를 함께 본다.

## 추가 조사 Sources

- https://github.com/bytedance/deer-flow/releases/tag/v2.1.0
- https://deerflow.tech/en/docs/harness/subagents
- https://langchain-ai.github.io/langgraph/concepts/durable_execution/
