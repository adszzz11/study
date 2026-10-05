---
date: 2026-10-05
tags: [tech]
type: tech-tool-study
status: draft
---

# Answer me with HTML — Cheatsheet

> [[README|목차로 돌아가기]]

## Snapshot

| 항목 | 내용 |
|---|---|
| 형태 | Agent Skill + `am` CLI |
| 입력 | extended Markdown draft |
| 기본 출력 | offline, self-contained single HTML |
| Runtime | Node.js `>=20` |
| Parsing / layout | `marked` / `@dagrejs/dagre` |
| Template | `sheet`, `doc` |
| Theme / mode | `blueprint`, `shadcn` / `light`, `dark` |
| License | MIT (README/package metadata에서 실행 전 재확인) |

## Core Commands

```sh
# Agent Skill 설치
npx skills add QingYunA/answer-me-with-html

# 설치된 command와 format 확인
am list
am help format
am help flow

# draft 렌더링, lint, source-preserving panel update
am render draft.md --no-open
am lint draft.md --style strict
am patch page.html --panel "Decision"
```

Option 이름과 지원 component는 설치 버전에 따라 달라질 수 있으므로 실행 전 `am help`를 우선한다.

## Component Selector

| 표현하려는 것 | 선택 |
|---|---|
| 처리 흐름·분기 | `flow` |
| 호출/응답 순서 | `sequence` |
| 계층 | `tree` |
| 시간순 사건 | `timeline` |
| limit·scope | `limits` |
| 주석 | `annot` |
| 사실 카드 | `kv` |
| 핵심 경고/결론 | `callout` |
| 비교 | Markdown table |

## Authoring Rules

1. answer와 audience를 한 문장으로 먼저 적는다.
2. frontmatter → `##` panel → fenced component block 구조를 사용한다.
3. HTML이 아니라 Markdown source를 수정한다.
4. layout 오류는 content 구조를 단순화해 먼저 해결한다.
5. lint는 review signal이며 사실성·보안을 보증하지 않는다.

## Video / MP4 Prerequisites

- narration beat가 있는 draft와 선택한 TTS provider
- MP4 export 시 Chrome, `ffmpeg`, Node.js 22+ 필요 가능
- provider API key는 prompt, source, 생성 HTML에 기록하지 않음

## Sources

- https://github.com/QingYunA/answer-me-with-html
- https://raw.githubusercontent.com/QingYunA/answer-me-with-html/main/src/cli.js
- https://raw.githubusercontent.com/QingYunA/answer-me-with-html/main/package.json
