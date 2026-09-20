---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# inspoAI MCP — Getting Started

> [[../03-references|이전: References]] · [[../README|목차]] · [[02-deep-dive|다음: Deep Dive]]

## Goal

첫 실습의 목표는 UI를 즉시 생성하는 것이 아니라, server가 실제로 어떤 data와 권한을 요구하고 어떤 근거를 반환하는지 안전하게 확인하는 것이다.

## 1. 현재 연결 정보 확인

[Inspo AI MCP 페이지](https://www.inspoai.io/mcp)에서 다음을 확인한다.

- client별 연결 절차와 지원 여부
- account 가입 및 billing requirement
- MCP endpoint 또는 client-native connection 방식
- privacy policy, data retention, training 사용 여부
- OAuth/API key 등 credential의 scope와 revoke 방법

공개 페이지에서 확인할 수 없다면 추정해 연결하지 말고 vendor에 문의한다.

## 2. 최소 권한으로 연결

처음에는 별도 test account 또는 최소 권한 account를 사용한다. MCP Client가 보여 주는 tool inventory를 저장해 다음을 분류한다.

| 확인 항목 | 질문 |
|---|---|
| Read | 검색·조회만 가능한가? |
| Write | moodboard 저장, upload, brand scan 시작 같은 변경 도구가 있는가? |
| Data access | URL, Figma asset, repository, prompt 내용을 어디까지 보내는가? |
| Citation | 반환값에 원본 URL·저작권 정보를 포함하는가? |
| Failure | quota, timeout, no-result가 구조화되어 반환되는가? |

## 3. 조사 요청으로 시작

첫 prompt는 구현보다 조사에 집중한다.

```text
B2B fintech onboarding의 신뢰감 있는 mobile UI references를 찾고,
navigation·form·error-state 패턴을 요약해줘.
각 항목에 source URL과, 우리 제품에 그대로 복제하면 안 되는 요소를 표시해줘.
```

결과를 받을 때는 reference의 수보다 rationale을 본다. category, target user, platform, accessibility 조건이 요청에 맞는지 확인한다.

## 4. 레퍼런스에서 구현으로

검증한 결과 중 세 가지 이하의 pattern을 선택하고 제약을 명시한다.

```text
선택한 pattern 3개를 각각의 source와 함께 요약해줘.
우리 design token과 WCAG 기준을 지키는 React component로 구현해줘.
상표, copy, illustration, screenshot layout은 복제하지 말고
pattern의 목적만 재해석해줘.
```

## 5. PoC 종료 기준

- tool scope와 data flow를 팀이 설명할 수 있다.
- 반환된 레퍼런스의 출처를 재현·검토할 수 있다.
- 구현물은 brand token, keyboard navigation, contrast를 통과한다.
- vendor 연결을 revoke했을 때 agent workflow가 안전하게 실패한다.

## Sources

- https://www.inspoai.io/mcp
- https://modelcontextprotocol.io/specification/2025-06-18/server
