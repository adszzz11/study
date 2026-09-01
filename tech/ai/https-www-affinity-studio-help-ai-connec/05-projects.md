---
date: 2026-09-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Practice Projects

## Project 1 — Selection-safe Layer Renamer

**목표:** 선택한 artboard 안의 unnamed layer만 규칙적으로 rename한다.

**완료 조건:**

- 선택 밖의 layer는 변경되지 않는다.
- naming collision을 탐지하고 overwrite하지 않는다.
- 실행 전 대상 수와 rename mapping을 preview한다.
- 두 번째 실행은 추가 변경을 만들지 않는다.

```text
현재 선택된 artboard 내부에서 이름이 비어 있거나 기본 이름인 layer만 찾아 줘.
`{artboard}-{role}-{index}` 규칙의 rename preview를 먼저 표로 보여 줘.
충돌은 실행하지 말고 별도로 보고해. style, geometry, order는 변경하지 마.
```

## Project 2 — Multi-channel Export Assistant

**목표:** 선택한 artboard를 channel별 규격으로 준비하고 안전하게 export한다.

**규격 예시:**

| Channel | Size | Format |
|---|---:|---|
| Square | 1080×1080 | PNG |
| Story | 1080×1920 | PNG |
| Print proof | source size | PDF |

**Guardrail:** 원본 보존, layout 유지, `./exports` 밖 쓰기 금지, 기존 파일 overwrite 금지, 결과 count 보고.

## Project 3 — Non-destructive Document Adjustment

**목표:** 문서 전체에 같은 correction을 적용하되 원본 object를 직접 변경하지 않는다.

- 별도 adjustment/layer 구조를 사용한다.
- before/after preview를 만든다.
- 적용 대상과 제외 대상을 기록한다.
- 수동 rollback 절차를 함께 저장한다.

## Project 4 — Parameterized Roughen Tool

**목표:** 선택된 curve에만 적용되는 custom dialog 기반 tool을 만든다.

필수 parameter:

- intensity
- segment/detail
- random seed
- `Duplicate before applying` checkbox
- Preview / Apply / Cancel

**Test matrix:** empty selection, open/closed curve, grouped object, locked layer, extreme parameter.

## Production 승격 체크리스트

- [ ] generated source를 review했다.
- [ ] target/scope/invariant가 코드와 UI에 반영됐다.
- [ ] representative sample과 edge case fixture가 있다.
- [ ] export path 및 overwrite behavior를 검증했다.
- [ ] Affinity와 script version을 기록했다.
- [ ] undo/rollback과 backup 절차가 있다.
- [ ] product update 후 실행할 regression checklist가 있다.
- [ ] 민감한 client data의 Claude 전달 정책을 확인했다.

## Sources

- [Automate design tasks in Affinity with Claude](https://www.affinity.studio/blog/automate-design-tasks-affinity-claude)
- [Affinity AI Connector 설정 가이드](https://www.affinity.studio/help/ai-connector-setup/)

