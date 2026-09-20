---
date: 2026-08-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Paperthin — Cheatsheet

> [[05-projects|이전: Projects]] · [[README|목차]]

## Install & Update

```bash
npx skills@latest add LilMGenius/paperthin --global --agent '*'
```

```text
/re0-upgrade  # plan과 대상 확인 → confirmation → catalog convergence
```

## Scope 선택

| 질문 | scope | 대표 skill |
|---|---|---|
| 한 artifact/claim/plan을 고칠까? | `depth` | `re0`, `factchk`, `hate`, `sip` |
| 여러 파일의 truth를 모을까? | `breadth` | `ssotize`, `re0-upgrade` |
| 여러 iteration을 이어갈까? | `coil` | `re0-loop`, `re0-memo`, `re0-work`, `nba` |
| 독립 관점의 차이를 볼까? | `mesh` | `prism` |

## 증상 → Reflex

| 증상 | 선택 | 핵심 결과 |
|---|---|---|
| 문서에 patch와 과거 설명이 누적됨 | `re0` | 현재 truth만 남긴 clean v0 |
| 요청을 잘못 읽은 것 같음 | `readchk` | 실제 ambiguity만 질문 |
| claim이 그럴듯하지만 불확실함 | `factchk` | 양방향 external evidence |
| plan의 핵심 가정이 위험함 | `hate` | objection 하나 + cheapest test |
| 평가가 자기확증처럼 보임 | `mandela` | 독립 ground truth 검사 |
| artifact 직후 QA가 필요함 | `sip` | 필요한 reflex만 route |
| 사실이 여러 파일에서 drift | `ssotize` | canonical source와 consumer |
| 다음 iteration이 매번 초기화됨 | `re0-memo` / `re0-work` | 압축된 learning과 next action |
| 실제 surface 검증이 빠짐 | `re0-loop` | `DRIVE` evidence 포함 cycle |
| 복수 관점의 차이를 보고 싶음 | `prism` | consensus보다 divergence |

## Invocation 경계

```text
model-invoked
  description trigger가 맞으면 agent가 선택 가능

user-invoked
  disable-model-invocation: true
  사람의 명시 호출 필요
```

대표 user-invoked:

- 외부 변경: `re0-release`, `re0-merge`, `re0-upgrade`
- 의도적 고비용/반론: `hate`, `macrothink`, `feynman`, `prism`

## `re0-loop`

```text
FRAME → BUILD → DRIVE → RE0-MEMO → HATE → RE0-WORK → BUILD AGAIN
```

`DRIVE`에서는 test report만 보지 말고 해당 기능의 실제 surface(browser, HTTP, desktop)를 직접 확인한다.

## 안전 Checklist

- [ ] third-party `SKILL.md`, scripts, hooks를 설치 전에 review
- [ ] global install path와 agent filesystem 권한 확인
- [ ] user-only skill을 agent가 자동 호출하지 않도록 확인
- [ ] publication/merge/upgrade 전 confirmation 확인
- [ ] `[PROOF]`를 independent benchmark로 과대해석하지 않기
- [ ] Markdown procedure와 실제 sandbox/security control을 구분
- [ ] 고칠 것이 없는 `re0` 결과는 no-op인지 확인

## 빠른 원칙

```text
작은 failure point에는 작은 reflex를 쓴다.
검사 수보다 evidence의 독립성을 본다.
파일 수보다 실제 surface에서의 proof를 본다.
현재 truth를 보존하고 stale delta를 제거한다.
외부 상태 변경은 사람이 authority를 부여한 뒤 실행한다.
```

## Sources

- https://github.com/LilMGenius/paperthin#the-index
- https://github.com/LilMGenius/paperthin/blob/main/docs/invocation.md
- https://agentskills.io/specification
