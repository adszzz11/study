---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Google Opal Deep Dive

> [[01-getting-started|이전: Getting Started]] · [[../README|목차로 돌아가기]]

## 1. linear chain과 Agent Mode

선형 `Generate` chain은 단계와 handoff가 명확할 때 적합하다. 반면 Agent Mode는 objective를 향해 reasoning, tool use, multi-step coordination을 수행한다.

| 상황 | 권장 방식 |
|---|---|
| 입력 정규화 → 정해진 형식의 요약 | linear Generate chain |
| 조사 결과에 따라 Search·Maps·Code Exec 사용을 판단 | Agent Mode |
| 정해진 규칙에 따른 분기 | `@Go to` routing |
| 이전 세션의 선호·기록 재사용 | Persistent Memory |

Agent prompt는 모든 micro-step을 강제하기보다 목적, 성공 기준, 금지 사항, 사용할 도구를 쓴다.

```text
목표: 사용자의 여행 조건에 맞는 검증 가능한 itinerary를 만든다.
도구: 위치·운영 정보에는 @Maps와 @Search를 사용한다.
제약: 확인 불가 정보는 추정하지 말고 표시한다.
출력: 날짜별 일정, 이동 근거, 각 장소의 source URL.
```

## 2. context와 routing

`@` reference는 이전 step, asset, tool의 결과를 prompt에 연결한다. 이 연결을 이름과 목적이 보이게 유지해야 debugging이 쉽다. 조건부 흐름은 `@Go to` routing으로 설계하되, 모든 분기에 fallback Output 또는 재입력 경로를 둔다.

Persistent Memory는 편의 기능이지 진실의 원천이 아니다. 기억된 선호·기록은 사용자가 확인·수정할 수 있게 보여 주고, 민감 정보나 장기 보존이 부적절한 값을 넣지 않는다.

## 3. output contract

dynamic webpage와 spreadsheet에는 모두 검증 가능한 contract가 필요하다.

```text
필수 field: claim | evidence URL | confidence/unknown | generated_at
금지: source 없이 확정적 수치 제시
fallback: evidence가 없으면 “검증 필요”와 빈 URL을 명시
```

## 4. debugging 순서

1. Preview에서 전체 happy path를 실행한다.
2. Console에서 실패한 step을 개별 실행한다.
3. input과 `@` reference가 실제로 어떤 intermediate output을 받았는지 비교한다.
4. prompt를 한 번에 여러 군데 바꾸지 않고, 한 가설씩 수정·재실행한다.
5. 빈 값, 긴 asset, 상충하는 지시, tool failure를 별도 test case로 둔다.

## 5. share·version·privacy

| 위험 | 완화 |
|---|---|
| editor/remix가 prompt graph를 노출 | viewer/editor/remix 권한을 분리하고 비밀을 prompt에 넣지 않는다. |
| Drive sharing으로 예상 밖 접근 | Drive ACL을 별도 점검하고 test account로 확인한다. |
| 과거 version 복원이 최신 작업을 삭제 | 복원 전 현재 version을 별도 복제한다. |
| 생성 결과의 사실 오류 | citation, human review, publish 전 checklist를 둔다. |

Gemini 내 mini-app 생성 조건은 personal Google Account, 18세 이상, English, desktop으로 문서화돼 있다. 지역·계정·시점에 따라 달라질 수 있으므로 실제 사용 직전에 Help 문서를 확인한다.

## Sources

- https://developers.google.com/opal/Agent_Mode
- https://developers.google.com/opal/overview
- https://developers.google.com/opal/faq
- https://support.google.com/gemini/answer/16802014?hl=en-GB
