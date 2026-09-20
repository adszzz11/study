---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Refero MCP — Getting Started

> [[../03-references|이전: References]] · [[../README|목차]] · [[02-deep-dive|다음: Deep Dive]]

## Goal

첫 실습의 목표는 screen을 “예쁘게 복사”하는 것이 아니라, brief → research → reference lock이라는 재현 가능한 판단 기록을 만드는 것이다.

## 1. Confirm Access

Refero Pro access를 준비하고 MCP-compatible client에서 browser OAuth login을 완료한다. official repository의 Codex 설치 예시는 다음과 같다.

```bash
codex plugin marketplace add referodesign/refero_skill
codex plugin add refero@refero
```

설치 후에는 문서에 적힌 tool name을 가정하지 말고 client의 MCP tool discovery 결과를 확인한다. manifest나 config에 OAuth token/secret를 직접 기록하지 않는다.

## 2. Write a Short Brief

```yaml
screen: team invite empty state
user: B2B analytics SaaS의 workspace admin
platform: desktop web
primary_goal: teammate 초대와 권한 이해를 돕기
brand_constraints: calm, trustworthy, information-dense
research_layers: [styles, screens, flows]
```

brief 없이 “좋은 dashboard를 찾아라”라고 요청하면 결과를 평가할 기준이 없다. user, context, primary action, brand constraint, 필요한 layer를 먼저 좁힌다.

## 3. Research in Order

1. **Styles** — “신뢰감 있는 B2B analytics SaaS visual direction 세 가지를 찾아라.”
2. **Screens** — “선택한 방향에 맞는 empty state와 team invite screen 사례를 찾아라.”
3. **Flows** — “invite onboarding의 단계, 오류, completion state를 정리하라.”

각 결과에서 이름보다 관찰 가능한 trait를 적는다. 예: muted surface의 역할, heading/body density, primary CTA 위치, helper copy의 유무, error recovery의 다음 action.

## 4. Create a Reference Lock

```md
## Reference lock
- References: A, B, C
- Keep: compact table density, single clear CTA, progressive disclosure
- Exclude: saturated gradient, oversized illustration, hidden permission explanation
- Token roles: surface/subtle, text/primary, action/primary, border/default
- Flow decision: invite sent → pending state → resend/cancel/error recovery
```

reference lock은 구현자가 무엇을 보존하고 무엇을 피할지 알게 한다. product를 그대로 재현하는 specification이 아니라 synthesis의 경계다.

## 5. Implement and Validate

desktop/mobile screenshot을 reference와 나란히 보고 typography, density, spacing, color role, imagery, accessibility drift를 검사한다. “비슷해 보임” 대신 brief의 primary goal과 상태별 action이 유지되는지 확인한다.

## Completion Checklist

- [ ] Pro access와 OAuth connection을 확인했다.
- [ ] 실제 client에서 MCP tool discovery를 확인했다.
- [ ] screen, user, platform, goal, constraints가 있는 brief를 썼다.
- [ ] Styles → Screens → Flows를 순서대로 조사했다.
- [ ] 2~3개 reference의 keep/exclude trait를 기록했다.
- [ ] desktop/mobile 및 error/empty state를 visual QA했다.

## Sources

- https://github.com/referodesign/refero_skill
- https://github.com/referodesign/refero_skill/tree/master/.codex-plugin
- https://github.com/referodesign/refero_skill/blob/master/skills/refero-design/SKILL.md
