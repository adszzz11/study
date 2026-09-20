---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Mobbin MCP — Projects

## 1. Paywall 개선

구독형 app의 paywall 20~40개를 조사한다. `price anchoring`, cancellation reassurance, benefit hierarchy를 표로 추출하고, 이를 자체 experiment 가설로 바꾼다.

- 산출물: reference table, pattern memo, A/B test hypothesis, 구현 backlog
- 주의: 경쟁사의 price copy나 visual asset을 그대로 쓰지 않는다.

## 2. KYC / Onboarding specification

fintech 또는 health app의 permission, identity verification, progressive disclosure 사례를 찾는다. compliance 요구와 UX 요구를 구분한 screen specification을 작성한다.

- 산출물: 단계별 flow map, required/optional 정보, error recovery, legal review 질문
- 검증: 실제 규제 준수 여부는 전문 검토로 확인하며 reference를 준수 증거로 취급하지 않는다.

## 3. Checkout conversion audit

e-commerce checkout flow를 비교하여 guest checkout, delivery option, error recovery, trust signal의 공통 pattern을 backlog로 만든다.

| 항목 | 조사 질문 | 구현 확인 |
|---|---|---|
| Guest checkout | 로그인 강제 전환은 언제 나타나는가? | 계정 없이 구매 가능한가? |
| Delivery | 비용·도착일·옵션을 언제 보여주는가? | 변경이 총액에 즉시 반영되는가? |
| Error recovery | validation 오류는 어느 입력 근처에 나타나는가? | focus, message, 재시도 경로가 있는가? |
| Trust signal | 보안·반품·결제 안내는 어디에 배치되는가? | 과도한 방해 없이 이해되는가? |

## 4. Design-to-code handoff

Mobbin MCP로 외부 pattern을 research하고 Figma MCP로 내부 design system과 frame context를 읽는다. 구현 agent에는 **외부 evidence**, **내부 component 제약**, **acceptance criteria**를 분리해 전달한다.

## 5. Design review bot workflow

PRD의 feature intent를 입력받아 Mobbin reference와 현재 UI를 비교하는 memo를 생성한다.

```text
입력: PRD, 현재 화면, Mobbin 검색 query
출력: 근거 링크 + 권고안 + 구현 영향 + open questions
검토: PM, Design, Engineering이 채택 여부를 결정
```

이 workflow는 자동 승인 도구가 아니다. reference 선택의 편향, 내부 제약, 저작권·브랜드 경계는 사람이 검토한다.

## Sources

- [Mobbin MCP](https://mobbin.com/mcp)
- [Mobbin MCP features](https://docs.mobbin.com/mcp/features)
- [Figma MCP server documentation](https://developers.figma.com/docs/figma-mcp-server/)
