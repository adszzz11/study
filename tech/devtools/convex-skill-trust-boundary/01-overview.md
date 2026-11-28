---
date: 2026-11-28
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview: 무엇이 신뢰 경계를 넘는가

## What

Convex onboarding용 skills에서 사용자 입력이 외부 요청으로, 외부 응답이 로컬 실행 코드로 바뀌는 흐름을 분석한다.

| 대상 | 자료에 제시된 동작 | 쟁점 |
|---|---|---|
| `skills/quickstart/SKILL.md` | 한 문장 아이디어를 `/generate`로 POST | 외부 전송 고지가 없다는 작성자 지적 |
| `skills/add/SKILL.md` | `/add-hosting` 또는 `/add-component` 응답을 `bash`로 실행 | 실행 시 가져오는 고정되지 않은 코드 |
| `skills/labs-quickstart/SKILL.md` | 다운로드와 실행을 별도 Bash call로 분리 | 이유를 safety classifier 회피로 명시 |

## Why

맞춤형 runbook과 bootstrap 자동화는 설정 부담을 줄인다. 그러나 로컬 설정을 맡긴 사용자가 아이디어 전송과 외부 코드 실행까지 이해하고 선택했는지는 별도 문제다.

작성자는 악의를 단정하지 않고 onboarding을 안정화하려는 팀으로 해석한다고 밝혔다. 구현의 문제와 개발자의 의도, 실제 피해를 혼동하지 않는다.

## 특징과 구조

```text
사용자 아이디어 → IDEA → JSON { idea, template: "nextjs-shadcn" }
 → HTTPS POST basic-anteater-667.convex.site/generate
 → 응답 id → SLUG → /tmp/convex-qb-slug → 다음 Bash call
```

- `node`와 `JSON.stringify`로 body를 만든다.
- `curl --max-time 15`는 시간 제한이며 데이터 최소화나 보안 검증이 아니다.
- `[telemetry 1/3]` 주석과 달리 payload에는 실행 횟수뿐 아니라 아이디어 원문이 들어간다.
- 서버가 `"a run started"`를 기록한다는 주석만으로 원문 보관을 단정할 수 없다.
- JSON parsing 실패로 출력이 비어 있을 수 있고 `|| true`는 실패 전파를 막는다. 성공 여부와 후속 처리의 관찰 가능성을 점검해야 한다.
- 임시 파일은 response id 전달 수단이다. 전체 아이디어가 그 파일에 저장된다는 근거는 없다.

## 근거의 한계

Revision `6ca54f6` 발췌에 대한 분석이다. 나머지 telemetry 두 단계, 서버의 원문 저장·기간·접근권한·활용, 현재 구현은 확인되지 않았다. 짧은 아이디어도 내부 맥락을 담을 수 있지만 실제 민감정보 전송 사례는 자료에 없다.

## 다음 노트

[[tech/devtools/convex-skill-trust-boundary/04-learning/01-getting-started|로컬 tracing 실습]] · [[tech/devtools/convex-skill-trust-boundary/README|학습 경로]]

## Sources

- https://github.com/convex/convex-backend-skill/issues/64
