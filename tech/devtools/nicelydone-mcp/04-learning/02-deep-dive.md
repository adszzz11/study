---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: Pattern Synthesis Workflow

## Metadata-first retrieval

image를 먼저 훑으면 비슷한 visual style에 끌리기 쉽다. page type, UI element, layout pattern, description 같은 structured metadata로 후보를 좁힌 뒤 필요한 화면만 비교한다.

```text
문제 정의
  → query: page type + interaction + state
  → metadata 기반 후보군
  → 2~3개 reference 비교
  → pattern / trade-off / product constraint 기록
  → original design brief와 code
```

## 좋은 query의 구성

| 요소 | 예시 |
| --- | --- |
| Context | B2B analytics SaaS |
| Object | data table, role management, upgrade modal |
| Interaction | multi-filter, bulk action, invite acceptance |
| State | empty, loading, error, permission denied |
| 비교 기준 | information density, recovery path, keyboard access |

`settings page`처럼 넓은 요청보다 `B2B role management에서 invite pending과 permission denied state를 가진 flow`처럼 제약을 준 요청이 비교하기 좋다.

## Synthesis matrix

| 항목 | Reference A | Reference B | Original decision |
| --- | --- | --- | --- |
| Progress | stepper | inline checklist | 실제 중단 지점이 많으므로 checklist 채택 |
| Skip | 없음 | 허용 | risk가 낮은 profile step만 skip 허용 |
| Recovery | email resend | support link | resend + cooldown + accessible status 제공 |

이 표에서 reference의 사실과 팀의 결정을 섞지 않는다. 마지막 열은 자사 제품의 요구 사항과 접근성 기준을 근거로 작성한다.

## QA gate

- responsive: 좁은 viewport에서 information priority와 overflow가 명확한가?
- state: empty, loading, error, permission, partial result를 구분했는가?
- accessibility: keyboard path, visible focus, semantic label, contrast, status announcement를 확인했는가?
- originality: copy, asset, branding, 독특한 composition을 복제하지 않았는가?
- provenance: 어떤 reference가 어떤 pattern 판단에 영향을 주었는지 brief에만 남겼는가?

## Collection 운영

검색 중 장기적으로 쓸 사례만 collection에 저장한다. collection 이름은 문제 영역 중심으로 짓는다. 예: `B2B-table-states`, `activation-invite-flows`. 이미지를 모으는 것보다 각 항목에 “왜 저장했는가”를 한 줄로 적는 편이 재사용에 유리하다.

## Sources

- [Nicelydone MCP](https://nicelydone.club/mcp)
- [Nicelydone User Flows](https://nicelydone.club/flows)
- [Nicelydone Help Center](https://vzero.nicelydone.club/help/)
