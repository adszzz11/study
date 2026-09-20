---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Google Opal Cheatsheet

> [[README|목차로 돌아가기]]

## 기본 graph

```text
User Input → Generate / Agent → Output → Preview · Console → Share / Publish
```

## 구성 요소

| 요소 | 기억할 점 |
|---|---|
| `User Input` | 값의 형식·필수 여부·빈 값 fallback을 정의한다. |
| `Generate` | deterministic한 작은 변환에 적합하며 `@reference`로 context를 받는다. |
| `Agent Mode` | objective, 도구, 성공 기준, 금지 사항을 적는다. |
| `@Search`, `@Maps` | grounding 결과도 출처 URL과 날짜를 output에 보낸다. |
| `@Memory` | 편의용 상태이며 사실 검증과 privacy review를 대체하지 않는다. |
| `@Go to` | 조건 분기마다 fallback과 종료 경로를 둔다. |
| Output | webpage/Sheet의 field와 오류 표시 규칙을 명시한다. |

## prompt template

```text
목표: [사용자에게 제공할 결과]
입력: @[input]
도구: [@Search / @Maps / @Memory 등]
제약: [사실성, 형식, 금지 내용]
성공 기준: [필수 field와 검증 방법]
fallback: 정보를 확인할 수 없으면 “검증 필요”로 표시한다.
```

## publish checklist

- [ ] Console에서 핵심 step을 개별 실행했다.
- [ ] citation 없는 사실 주장과 hallucination을 검토했다.
- [ ] prompt, asset, Memory에 민감 정보가 없다.
- [ ] editor/remix 권한과 Drive ACL을 모두 확인했다.
- [ ] version restore가 최신 version을 삭제할 수 있음을 이해했다.
- [ ] target account의 현재 접근 조건을 공식 문서에서 확인했다.

## Sources

- https://developers.google.com/opal/overview
- https://developers.google.com/opal/Agent_Mode
- https://developers.google.com/opal/quickstart
- https://developers.google.com/opal/faq
