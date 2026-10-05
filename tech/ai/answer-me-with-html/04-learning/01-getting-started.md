---
date: 2026-10-05
tags: [tech]
type: tech-tool-study
status: draft
---

# Answer me with HTML — 시작하기

> [[../README|목차로 돌아가기]] | [[02-deep-dive|다음: 심화]]

## Goal

agent가 만든 concise Markdown draft를 `am`으로 렌더링하고, HTML이 아니라 source Markdown을 수정하는 기본 loop를 익힌다.

## Prerequisites

- Node.js 20+ 환경
- agent skill을 사용할 agent 환경
- 브라우저(생성된 local HTML 확인용)

## Install the Skill

```sh
npx skills add QingYunA/answer-me-with-html
```

설치 뒤에는 agent에게 TCP handshake, OAuth flow 또는 “Redis vs Memcached”처럼 다단계·비교형 질문을 요청한다. 설치 위치와 노출 방식은 사용하는 agent host의 skill 관리 규칙을 따른다.

## First Draft

초안은 frontmatter → `##` panel → fenced component block 순서를 따른다. 정확한 component syntax는 설치 버전의 도움말과 SKILL.md를 기준으로 한다.

````markdown
---
title: Redis vs Memcached
template: sheet
---

## Decision
짧은 결론과 선택 기준을 쓴다.

## Request path
```flow
Client -> Cache -> Database
```
````

위 예시는 구조를 보여 주는 의사 형식이다. fenced block의 유효한 문법은 다음 command로 확인한다.

```sh
am help format
am help flow
am render draft.md --no-open
```

## Inspect and Iterate

```sh
am list
am lint draft.md --style strict
am patch page.html --panel "Decision"
```

1. `--no-open`으로 HTML을 생성한다.
2. 브라우저에서 hierarchy, wrapping, diagram edge를 확인한다.
3. lint 결과는 문장 개선 제안으로 검토한다. technical term까지 기계적으로 바꾸지 않는다.
4. HTML을 직접 편집하지 말고 `am patch` 또는 draft 수정으로 원본 보존 흐름을 유지한다.

## Exercise

- [ ] `sheet`로 Redis vs Memcached의 workload·persistence·eviction·verdict panel을 만든다.
- [ ] request path를 `flow`, read/write 순서를 `sequence`로 각각 표현해 본다.
- [ ] 긴 문장을 하나 넣고 strict lint가 무엇을 지적하는지 기록한다.
- [ ] 같은 내용을 `doc`으로 바꾸고 독서 흐름의 차이를 비교한다.

## Sources

- https://github.com/QingYunA/answer-me-with-html
- https://raw.githubusercontent.com/QingYunA/answer-me-with-html/main/skills/answer-me-with-html/SKILL.md
- https://raw.githubusercontent.com/QingYunA/answer-me-with-html/main/src/cli.js
