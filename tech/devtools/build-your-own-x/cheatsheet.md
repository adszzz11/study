---
date: 2026-07-17
tags: [tech]
type: tech-tool-study
status: draft
---

# Build Your Own X — Cheatsheet

> [[05-projects|이전: Projects]] | [[README|목차로 돌아가기]]

## 30초 요약

```text
Build Your Own X = 실행 도구가 아니라 외부 tutorial catalog
강점 = 넓은 주제 × 여러 language × 무료
빈칸 = curriculum + grading + 공통 test + production 보증
학습법 = 목표 mechanism → 작은 vertical slice → 자체 test → gap analysis
```

## 시작 순서

1. [Tutorials](https://github.com/codecrafters-io/build-your-own-x#tutorials)에서 category 선택
2. technology-first인지 language-first인지 결정
3. 후보 2~3개의 link, 최신성, 완결성, license 확인
4. 첫 vertical slice와 제외 범위 작성
5. public behavior test를 먼저 준비
6. 구현 후 reference behavior와 비교
7. benchmark, failure diary, production gap 기록

## Tutorial 선택 scorecard

각 항목을 `0`(없음), `1`(부분적), `2`(충분)로 평가한다.

| 항목 | 질문 |
|---|---|
| Goal fit | 배우려는 mechanism을 실제로 다루는가? |
| Recency | 현재 toolchain으로 재현 가능한가? |
| Completeness | series와 source code가 끝까지 있는가? |
| Explanation | code뿐 아니라 design 이유를 설명하는가? |
| Feedback | test, fixture, expected output이 있는가? |
| Scope | 가용 시간에 맞는 vertical slice가 있는가? |
| License | text와 code 재사용 조건이 명확한가? |

합계가 낮으면 다른 guide를 고르거나 theory/test 자료를 별도로 보강한다. 점수는 품질 인증이 아니라 비교를 명시적으로 만드는 도구다.

## 주제별 첫 slice

| 주제 | 최소 end-to-end 동작 |
|---|---|
| Database | encode → disk write → restart → read |
| Git | blob hash → store → lookup → decode |
| Compiler | tokenize → parse → evaluate expression |
| HTTP server | accept → parse request line → respond |
| Shell | read command → parse argv → spawn process |
| Container | child process → isolation 하나 적용 → 관찰 |

## Test menu

```text
Happy path       정상 input/output
Boundary         empty, zero, max length, EOF
Malformed input  invalid syntax, corrupt bytes
Restart          persistence와 recovery
Differential     reference tool과 behavior 비교
Property         encode/decode round trip 같은 invariant
Fuzz             parser와 decoder의 crash 탐색
Concurrency      ordering, race, deadlock, overload
```

## 기록할 design decision

```markdown
## Decision
- Context:
- Chosen design:
- Alternatives:
- Invariant:
- Failure modes:
- Measurement:
- Production gap:
```

## 대안 선택

| 필요한 것 | 선택 |
|---|---|
| 최대 탐색 폭과 자유도 | Build Your Own X |
| automated test와 단계별 hint | CodeCrafters |
| 하루 안팎의 작은 specification | Coding Challenges |
| app portfolio | Project Based Learning |
| hardware-to-software 고정 과정 | Nand2Tetris |
| theory 중심 장기 curriculum | Teach Yourself CS |

## 위험 신호

- last update와 dependency version을 확인할 수 없다.
- source code만 있고 expected behavior나 설명이 없다.
- tutorial subset과 실제 protocol/version의 경계가 불명확하다.
- test가 happy path 하나뿐이다.
- toy implementation을 production-ready라고 표현한다.
- license와 attribution 조건이 없다.

## 완료 checklist

- [ ] 내부 component를 그림 없이도 설명할 수 있다.
- [ ] 핵심 invariant와 failure mode를 각각 3개 말할 수 있다.
- [ ] tutorial 없이 최소 기능을 다시 구현할 수 있다.
- [ ] reference implementation과 다른 behavior를 설명할 수 있다.
- [ ] benchmark 조건과 결과를 재현할 수 있다.
- [ ] production에서 빠진 요구 사항을 문서화했다.

## Sources

- [Build Your Own X](https://github.com/codecrafters-io/build-your-own-x)
- [Build Your Own X issues](https://github.com/codecrafters-io/build-your-own-x/issues)
- [CodeCrafters Concepts Overview](https://app.codecrafters.io/concepts/overview)
- [Teach Yourself CS](https://teachyourselfcs.com/)
