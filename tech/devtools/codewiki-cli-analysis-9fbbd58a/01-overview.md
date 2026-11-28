---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview

## What

codewiki-cli는 기존 Google CodeWiki 문서를 읽는 비공식 CLI다. `<repo>`는 `owner/repo` 또는 GitHub URL을 받는다. Node.js 20 이상이 필요하며 로컬 build에 pnpm을 사용한다.

## Why

문서를 통째로 읽으면 질문과 무관한 내용이 Agent context를 차지한다. README의 원칙은 “List sections first, then request only the section content you need”다. 목록 탐색과 본문 읽기를 분리해 현재 질문에 필요한 자료를 고른다.

## 핵심 기능

| 명령 | 반환 또는 동작 | 목적 |
|---|---|---|
| `search <query> --limit 5` | 저장소 검색, limit 1~50 | 대상 찾기 |
| `sections <repo>` | ID·제목·요약·anchor, 본문 제외 | 범위 선택 |
| `content <repo> <section-id>` | 선택한 섹션 Markdown | 주제 읽기 |
| `content <repo> <section-id> --chunks` | heading·block 경계로 분할 | 작은 읽기 단위 |
| `cache directory [path]` | cache 경로 조회·설정 | 저장 위치 관리 |
| `cache clear` | cached wiki documents 삭제 | 로컬 정리 |

## 데이터 흐름과 경계

```text
sections / content
  → 저장소별 cache
    → 최초 요청: full wiki fetch → JSON 저장
    → 이후 요청: 저장된 cache 사용
  → 목록 또는 선택한 섹션 출력
```

`--refresh`는 `sections`와 `content`에서 새 사본을 가져온다. 선택적 출력은 context 투입량을 조절하지만 최초 fetch를 섹션 단위로 줄이지는 않는다. Cache TTL·자동 만료·동시 접근 제어·손상 복구는 자료에서 확인되지 않는다.

## 기술스택 요약

- Runtime: Node.js 20 이상, 로컬 실행 entry point는 `bin/run.js`.
- Build·개발 도구: pnpm, formatting·lint·typecheck·test 명령 제공.
- 데이터 원천: Google CodeWiki의 undocumented RPC.
- 저장·출력: 저장소별 JSON cache와 Markdown, heading·block 기반 chunk.
- Agent 배포: `.agents/skills/codewiki-cli`에 built CLI 포함. 세부 구현 언어·의존성은 이 자료로 확정하지 않는다.

## 신뢰 범위

수집 화면의 5 commits·0 stars·0 forks는 당시 관찰값이며 현재 수치나 품질 증거가 아니다. 검증 명령의 존재와 실제 통과·coverage·성능은 별개다. 문서와 소스의 일치 여부는 직접 확인해야 한다.

다음: [[tech/devtools/codewiki-cli-analysis-9fbbd58a/02-ecosystem|작업 방식 비교]] · [[tech/devtools/codewiki-cli-analysis-9fbbd58a/README|학습 진입점]]


## Sources

- https://github.com/miinhho/codewiki-cli — 제공된 dossier의 README 기반 정리. 실습 및 성능 검증은 미실행.
