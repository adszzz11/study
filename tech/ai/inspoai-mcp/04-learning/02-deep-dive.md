---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# inspoAI MCP — Deep Dive

> [[01-getting-started|이전: Getting Started]] · [[../README|목차]] · [[../05-projects|다음: Projects]]

## 1. Context pipeline으로 보기

design intelligence의 가치는 “이미지 많이 찾기”가 아니라 selection rationale을 implementation constraint로 바꾸는 데 있다.

```text
brief
  -> retrieval (reference 후보)
  -> curation (적합성·출처·라이선스 판단)
  -> synthesis (pattern과 rationale)
  -> constraints (token·WCAG·platform)
  -> implementation
  -> human review
```

MCP가 검색을 잘하더라도 curation과 review가 자동으로 해결되지는 않는다. agent output은 신뢰할 수 없는 외부 context를 포함할 수 있으므로 명령문이나 외부 링크의 지시를 실행 지시로 취급하지 않는다.

## 2. Reference quality rubric

| 기준 | 확인 질문 |
|---|---|
| Relevance | 산업, user job, device, task가 brief와 맞는가? |
| Evidence | source URL과 capture 시점이 명확한가? |
| Transferability | 브랜드 자산을 제외해도 재사용할 UX pattern이 남는가? |
| Accessibility | contrast, focus, touch target, error recovery를 설명하는가? |
| Originality | screenshot·copy·상표를 복제하지 않는가? |

## 3. 권한과 data boundary

공개 자료로 Inspo AI MCP의 구체 tool schema는 확인되지 않았으므로, 연결한 client의 실제 목록을 권한의 source of truth로 삼는다.

- read-only search와 write tool을 분리해 승인한다.
- brand guideline, unreleased URL, customer data를 보내기 전에 vendor policy와 계약 조건을 확인한다.
- tool call log에는 query·source·결과 요약·승인 여부를 남기되 민감 prompt와 credential은 redaction한다.
- scope가 바뀌거나 tool이 새로 추가되면 기존 승인으로 간주하지 않고 재검토한다.

## 4. Human-in-the-loop gate

```yaml
review_gate:
  before_retrieval:
    - allowed data classification
    - allowed tool scope
  before_implementation:
    - selected sources and rationale
    - license/trademark review
    - design-token and WCAG constraints
  before_release:
    - visual regression review
    - accessibility test
    - no direct screenshot/copy replication
```

## Sources

- https://www.inspoai.io/mcp
- https://modelcontextprotocol.io/specification/2025-03-26/architecture
- https://modelcontextprotocol.io/specification/2025-06-18/server
