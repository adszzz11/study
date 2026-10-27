---
date: 2026-10-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects

## 1. Research agent

`query planning → web search → source quality check → citation draft → human review`를 구현한다. 완료 기준은 답변마다 출처 URL이 있고, low-quality source 또는 근거 부족을 판별해 검토로 넘기는 것이다.

## 2. Customer-support triage

Routing으로 주문·환불·기술지원 specialist에 보낸다. 주문 조회는 read-only로 시작하고, 환불 같은 write action은 변경 preview와 승인 뒤에만 실행한다.

## 3. Internal knowledge copilot

권한 필터링된 RAG, citation, feedback-driven evaluation을 결합한다. 문서 권한이 retrieval 이전에 적용되는지와 인용한 source가 실제 권한 범위인지 테스트한다.

## 4. Code-review agent

repository를 read-only로 분석하고 test 실행을 제안한다. security/quality critic의 근거를 개발자가 검토한 뒤에만 PR comment를 게시한다.

## 5. Ops incident assistant

`log/metric retrieval → root-cause hypothesis → runbook recommendation → operator approval → remediation` 흐름을 만든다. 자동 remediation은 approval, time limit, rollback, audit trace 없이는 활성화하지 않는다.

## 공통 평가 지표

| 범주 | 예시 |
|---|---|
| 품질 | task success, grounded citation rate, critic agreement |
| 운영 | latency, tool error rate, retry count, token/tool cost |
| 안전 | blocked unsafe action, approval coverage, unauthorized access |

## Sources

- https://www.anthropic.com/research/building-effective-agents
- https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system
