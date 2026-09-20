---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: 조사 결과를 실험 가능한 결정으로 바꾸기

## Live schema를 먼저 확인한다

authenticated MCP에 연결한 뒤 `lazyweb_get_workflows`와 `tools/list`를 호출한다. 도구 이름, 입력 schema, side effect, plan별 범위를 local skill README보다 우선한다.

```text
1. get_workflows / tools/list
2. search_screens: 개별 interface pattern 탐색
3. search_flows: 순서와 decision point 탐색
4. search_experiments: variation의 근거와 한계 확인
5. agentic_search_finalize: 선택 result_ref 확정
6. 자사 제약·metric을 붙여 implementation brief 작성
```

## `result_ref`와 image 처리

검색 결과를 임시 문장으로 복사해 추적하지 말고 stable `result_ref`를 유지한다. 후보를 좁힌 후 finalize해 선택 사유를 기록하면 agent workflow가 재현 가능해진다.

이미지 비교에서는 `lazyweb_compare_image` 또는 `lazyweb_find_similar`가 준 optimized image URL을 사용한다. raw screenshot ID, 내부 storage URL, 추정한 path를 조합하지 않는다. URL의 만료·접근 범위도 caller가 가정하지 않는다.

## Growth workflow의 해석

| 산출물 | 올바른 해석 | 피할 해석 |
|---|---|---|
| Growth Score | 개선 검토의 우선순위 신호 | conversion lift 예측값 |
| recommendation | 검증할 변경 가설 | 바로 배포할 정답 |
| experiment/variation | 관찰된 차이와 조사 단서 | 증명된 winning test |
| backlog | PM이 검토할 후보 작업 | 승인된 production change |

## 권한과 side effect

- search·compare는 일반적으로 read 중심이지만, product/backlog workflow에는 write가 있을 수 있다.
- account, connection, workspace scope를 확인하고 최소 권한 token을 사용한다.
- mutation 전에 target, 영향, rollback, metric을 명시한다.
- delete는 exact confirmation을 요구하는지 live schema에서 확인하고, 모호한 자연어 동의로 실행하지 않는다.

## 연구 brief 템플릿

```markdown
# [Flow] research brief

## Decision
어떤 사용자가 어떤 단계에서 무엇을 결정해야 하는가?

## Evidence
- result_ref / source / capture date:
- 관찰한 순서·copy·interaction:

## Hypotheses
1. … because …

## Local constraints
- design token / accessibility / legal / locale:

## Experiment
- variant, primary metric, guardrails, sample/period, rollback:
```

## Sources

- https://www.lazyweb.com/product
- https://www.lazyweb.com/agent-access
- https://github.com/aboul3ata/lazyweb-skill
