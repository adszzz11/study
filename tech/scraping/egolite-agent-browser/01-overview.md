---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# ego(lite) Overview

[[tech/scraping/egolite-agent-browser/README|README]]로 돌아가기.

## What

ego(lite)는 수정 Chromium desktop app과 `ego-browser` CLI/Node.js SDK를 결합한 local-first automation 제품이다. agent는 단일 Node.js script에서 navigation, snapshot, click, fill, 출력까지 수행한다.

## Why

Playwright, Browser Use, `agent-browser`는 보통 별도 browser 또는 CDP session을 제어한다. 이 방식은 사용 중인 profile의 cookies·extensions·로그인 상태를 재사용하기 어렵고, 사람의 mouse·focus와 agent 작업이 충돌할 수 있다.

ego(lite)는 agent에게 별도 `Space`를 주고 사용자는 기존 탭을 계속 쓰게 한다. Chrome data import로 기존 session을 활용하며, 완료된 작업 탭은 남아 audit과 human takeover에 쓸 수 있다.

## 핵심 특징

| 구성 | 역할 | 주의점 |
|---|---|---|
| `Space` / Task Space | task별 tabs, cookies, storage와 control handoff를 분리 | authenticated session을 쓰므로 완전한 security sandbox는 아님 |
| `Snapshot` | accessibility tree를 structured text와 `@92` 같은 임시 ref로 제공 | DOM 변경 뒤 ref는 폐기하고 re-snapshot |
| `ego-browser` | CLI/SDK에서 단일 script로 browser task 실행 | native desktop app/CLI가 준비되어야 함 |
| `learnings` | `manifest.json`, notes, tools로 사이트별 knowledge pack 축적 | 오래된 site knowledge는 정기 검증 필요 |

공식 설명에 따르면 Snapshot은 native engine 차원에서 cross-origin iframe과 shadow DOM을 다룬다. selector를 추측하기보다 현재 Snapshot의 ref를 사용하는 흐름이 page 변화에 더 견고하다.

## 기술스택 요약

ego(lite)는 수정 Chromium desktop app 위에 Node.js 기반 `ego-browser` CLI/SDK를 올린 제품이다. agent는 `globalThis.ego` native binding과 CDP를 통해 Task Space를 제어하고, Snapshot/accessibility tree로 UI를 읽는다. TypeScript/ESM harness·Skill·API는 공개되어 있지만 desktop browser/native binding은 closed-source로 제공된다.

## Sources

- https://www.egolite.app/document/en/docs/product-introduce
- https://www.egolite.app/document/en/docs/snapshot
- https://github.com/citrolabs/ego-lite/blob/main/AGENTS.md

