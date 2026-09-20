---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Mobbin MCP — Deep Dive

## 조사에서 결정까지

좋은 MCP 사용은 검색 결과 하나를 모방하는 작업이 아니다. 다음 순서로 evidence를 product decision으로 바꾼다.

1. **질문을 분해한다.** 대상 사용자, task, platform, 성공 지표, 규제·기술 제약을 정한다.
2. **검색한다.** screen·flow·section 중 질문에 맞는 단위를 골라 후보를 넓게 모은다.
3. **후보를 묶는다.** 같은 목적의 사례를 묶고 화면 수가 아닌 interaction sequence를 비교한다.
4. **패턴을 분리한다.** 공통 패턴, 빈번하지만 상황 의존적인 패턴, 예외를 나눈다.
5. **결정한다.** 자사 사용자·brand·accessibility·compliance·구현 비용을 근거로 채택 또는 제외한다.
6. **코드화한다.** 결정, reference 링크, 구현 영향, acceptance criteria를 agent에 전달한다.

## Research memo 형식

```md
## Decision: cancellation flow의 exit survey는 optional으로 둔다

- Evidence: 조사한 flow에서 취소 확정 전 이유 수집과 대안 제시가 자주 함께 나타났다.
- Pattern: 이유 수집은 짧고 건너뛸 수 있으며, 최종 취소 CTA는 분명하다.
- Constraint: 우리 서비스는 retention offer를 제공하지 않으며, 개인정보 수집 안내가 필요하다.
- Decision: optional single-select survey + skip + 분명한 cancel confirmation을 사용한다.
- References: Mobbin 원본 링크 목록
- Implementation impact: `CancellationReasonSheet`, analytics event, privacy copy 검토
```

## Prompt 설계

나쁜 요청은 “좋은 checkout을 찾아줘”처럼 평가 기준이 없다. 다음 정보를 포함하면 결과가 검토 가능한 조사로 바뀐다.

- 제품 영역과 platform: `mobile fintech`, `B2B SaaS website`
- 사용자 task: `biometric login`, `plan cancellation`
- 표본과 비교 방식: `15개`, `공통/예외로 나눠 표로 정리`
- 산출물: `pattern, risk, source link, implementation implication`
- 금지사항: `copy나 asset을 복제하지 말 것`

예시:

```text
subscription cancellation flow를 15개 조사해라.
각 flow에서 (1) 취소 이유 수집, (2) retention offer, (3) confirmation,
(4) 재가입 안내를 표로 비교하고, 공통 패턴과 예외를 분리해라.
각 권고안에는 Mobbin 원본 링크와 우리 모바일 앱 적용 시 구현 영향을 붙여라.
특정 제품의 copy나 asset은 재사용하지 마라.
```

## 품질과 법적 경계

- 표본이 한 industry나 유명 brand에 쏠렸는지 확인한다.
- reference의 인기·시각적 완성도와 사용자 성과를 혼동하지 않는다.
- accessibility, localization, privacy, compliance는 Mobbin 결과만으로 판단하지 않는다.
- source link가 없는 요약은 review 가능성이 낮으므로 evidence와 함께 기록한다.
- 디자인의 아이디어와 타사 표현물을 구별하고, 후자는 복제하지 않는다.

## Sources

- [Mobbin MCP features](https://docs.mobbin.com/mcp/features)
- [Mobbin MCP](https://mobbin.com/mcp)
- [MCP introduction](https://modelcontextprotocol.io/docs/getting-started/intro)
