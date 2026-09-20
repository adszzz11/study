---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# taste — Cheatsheet

> [[05-projects|이전: Projects]] | [[README|목차로 돌아가기]]

## 30초 workflow

```text
1. Job: 누구에게 어떤 행동을 일으키나?
2. Reader: 이미 아는 것 / 검증할 것은?
3. Exemplar: 실제로 열어볼 인접 artifact는?
4. Route: code / UI / document / data / system?
5. Rank: 결과를 좌우하는 결정은?
6. Source: 구체 정보가 근거에 있는가?
7. Stop: 다음 polish를 독자가 알아채는가?
```

## Create

| 원칙 | 확인 질문 |
|---|---|
| Shape follows the job | 지금 형식이 목적 때문에 선택됐는가? |
| Rank, then allocate | 가장 중요한 내용에 가장 많은 공간을 썼는가? |
| Specifics from source | 숫자·가격·정책·기능에 근거가 있는가? |
| One recommendation | 기본안 하나와 reversal condition이 있는가? |
| Finish calibration | stakes와 attention span에 비해 과하지 않은가? |

```text
Use the taste skill. Ground this work in [artifacts].
The audience is [reader], and the required action is [job].
Do not invent missing facts; mark them as [confirm: ...].
Give one recommendation and the condition that would reverse it.
```

## Critique

```text
Verdict: 핵심 판단 한 문장
Invention: source 없이 만든 것
Cut: 제거할 것
Miss: 목적에 비해 빠진 결정
Tell: generated처럼 보이게 하는 흔적
Fix: 가장 작은 유효 수정
```

```text
Use the taste critique sequence. Inspect the source artifacts first.
Lead with a verdict, then list only material Invention, Cut, Miss, Tell,
and Fix items. Do not score unless comparison requires a rubric.
```

## Domain별 먼저 볼 것

| Domain | 먼저 확인 |
|---|---|
| Code | adjacent naming, call-site, error style, test, dependency |
| UI | hierarchy, audience, primary action, component, token, real content |
| Document | 첫 문장 결론, actionability, 최근 동종 문서, source data |
| Data | 전달할 단일 비교, range, gap, outlier, audience convention |
| System | constraint, failure, migration, config, deploy, incident |

## 금지 신호

- source 없이 만든 가격, 정책, 숫자, feature
- UI의 3-card template, 가짜 logo/testimonial, 장식용 gradient
- code의 불필요한 class, config, logger, irrelevant test
- document의 관습적 intro, 반복 conclusion, 가짜 pros/cons 균형
- chart의 불필요한 series, dual axis, 변수명뿐인 title
- system의 근거 없는 queue, cache, service, scalability claim

## 품질보증 경계

`taste` 다음에 필요에 따라 반드시 별도 실행한다.

```text
compiler · type checker · tests · linter · formatter
accessibility audit · security review · human approval
```

## 설치·update 안전수칙

- `SKILL.md`, `references/`, `scripts/` 전체를 먼저 읽는다.
- 공식 installer의 symlink/copy 대상을 확인한다.
- `main` 대신 검토한 commit 또는 tag를 pin한다.
- update 전후 instruction과 script diff를 본다.
- project-local 배치로 adoption을 작게 시작한다.

## Sources

- [SKILL.md](https://raw.githubusercontent.com/Hmbown/taste/main/SKILL.md)
- [DOMAINS.md](https://raw.githubusercontent.com/Hmbown/taste/main/references/DOMAINS.md)
- [REVIEW.md](https://raw.githubusercontent.com/Hmbown/taste/main/references/REVIEW.md)
