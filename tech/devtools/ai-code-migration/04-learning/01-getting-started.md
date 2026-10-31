---
date: 2026-07-17
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Code Migration — Getting Started

> [[../03-references|이전: References]] | [[../README|목차로 돌아가기]] | [[02-deep-dive|다음: Deep Dive]]

## 목표

첫 실습의 산출물은 migrated code가 아니다. **migration을 해도 되는지 판단하는 feasibility report와 신뢰할 수 있는 portable judge**다.

## Step 0 — Read-only Feasibility

다음 질문을 repository evidence와 함께 답한다.

| 질문 | 수집할 evidence | 중단 신호 |
|---|---|---|
| 왜 migration하는가? | incident, hiring, security, runtime cost, ecosystem 자료 | 막연한 선호만 있음 |
| Port인가 redesign인가? | scope statement, architecture decision | 둘이 섞여 acceptance criteria가 없음 |
| test를 재사용할 수 있는가? | test 분류와 target runner prototype | 구현 detail test뿐임 |
| dependency batch가 가능한가? | import/build graph, generated code 목록 | global state와 cycle이 대부분임 |
| 편익이 verification 비용보다 큰가? | CI·token·review 예산, 예상 유지비 | 성공 기준과 비용 상한이 없음 |

```yaml
migration_decision:
  source: Python
  target: TypeScript
  mode: structure-preserving-port
  reasons:
    - shared frontend/backend types
    - runtime operations standardization
  non_goals:
    - domain redesign
    - new features
  decision: investigate  # migrate | investigate | don't-migrate
```

## Step 1 — Test 분류

기존 suite를 다음처럼 분류한다.

| 분류 | 예시 | 처리 |
|---|---|---|
| Observable contract | CLI exit code, HTTP response, output file | 양쪽 implementation에 재사용 |
| Internal implementation | private class, allocation count, call order | contract로 재작성하거나 근거를 남기고 제외 |
| Environment-sensitive | clock, locale, network, filesystem order | fixture와 normalization 도입 |
| Missing behavior | production에서만 알려진 scenario | characterization test 또는 parity fixture 추가 |

## Step 2 — Portable Judge 만들기

가장 작은 end-to-end scenario 하나를 골라 original과 target에 같은 input을 보낸다.

```text
fixture/input.json
        ├─ original runner → original/{stdout,stderr,exit,files}
        └─ target runner   → target/{stdout,stderr,exit,files}
                                  ↓
                         normalize → structured diff
```

비교 대상:

- stdout/stderr와 exit code
- generated file의 content와 metadata 중 contract인 부분
- HTTP status, headers, body
- database state 또는 emitted event
- latency·memory는 기능 parity와 분리해 threshold로 평가

Normalization은 nondeterminism만 제거해야 한다. timestamp를 지우다가 ordering bug까지 숨기지 않도록 각 rule에 이유를 기록한다.

## Step 3 — Judge를 시험하기

원본이 통과하는지만 확인하면 부족하다. 의도적으로 target prototype을 망가뜨려 test가 실패하는지 본다.

```text
Mutation A: error code 변경       → contract test가 실패해야 함
Mutation B: output ordering 변경  → ordering이 contract라면 실패해야 함
Mutation C: resource leak 삽입     → 반복/성능 gate가 실패해야 함
Mutation D: auth check 제거        → security test가 실패해야 함
```

- [ ] baseline original이 통과한다.
- [ ] 알려진 mutation이 예상 test를 실패시킨다.
- [ ] diff가 원인을 찾을 만큼 작고 구조화되어 있다.
- [ ] local과 CI에서 같은 결과가 나온다.
- [ ] 실행 시간과 비용이 반복 loop에 적합하다.

## Step 4 — 첫 Rulebook 초안

```markdown
## Error handling
- Source exception `NotFound` → target typed error `NotFoundError`
- Public message와 exit/status code는 보존한다.
- Stack trace text는 parity 대상에서 제외한다.

## Async
- Blocking I/O를 임의로 async로 redesign하지 않는다.
- Existing cancellation behavior를 characterization test로 고정한다.

## Uncertainty
- 추론으로 채우지 말고 `TODO(port): <reason>`을 남긴다.
```

Rulebook 각 항목에는 `rule id`, rationale, good/bad example, verification method를 붙이면 재생성과 audit이 쉬워진다.

## Step 5 — Disposable Mini-migration

대표성이 높고 의존성이 제한된 2–5개 파일을 선택한다.

1. Agent A가 rulebook을 엄격히 적용한다.
2. Agent B가 target language senior 관점으로 독립 변환한다.
3. Agent C가 diff와 빠진 rule을 정리한다.
4. Adversarial reviewer가 behavior·security·performance 반례를 찾는다.
5. code는 폐기하고 rulebook과 gap inventory만 보존한다.

## 종료 조건

다음 조건 전에는 대량 fan-out을 시작하지 않는다.

- feasibility decision과 non-goal이 문서화됨
- reusable contract test와 scenario parity harness가 최소 하나 존재
- mutation test가 알려진 결함을 검출함
- dependency batch와 high-risk boundary가 식별됨
- 비용, concurrency, timeout, workspace/Git policy가 정의됨

## Sources

- https://claude.com/blog/ai-code-migration
- https://github.com/anthropics/code-migration-kit-with-claude-code
- https://aclanthology.org/2025.findings-acl.140/
