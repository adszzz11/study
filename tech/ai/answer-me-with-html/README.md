---
date: 2026-10-05
tags: [tech]
type: tech-tool-study
status: draft
---

# Answer me with HTML

> **한 줄 정의**: Answer me with HTML은 AI agent가 짧은 structured Markdown 초안만 작성하면 `am` CLI가 다이어그램·레이아웃·스타일을 처리해 오프라인 단일 HTML 설명 페이지로 렌더링하는 Agent Skill이다.

## Overview

LLM이 HTML/CSS/SVG를 전부 생성하면 설명 내용과 함께 반복적인 markup·좌표까지 output token으로 만들어야 한다. Answer me with HTML은 **내용과 표현을 분리**한다. agent는 extended Markdown으로 정보 구조를 쓰고, deterministic renderer가 panel, theme, SVG layout, lint를 적용한다.

기본 결과물은 CDN·웹 폰트 없이 열리는 self-contained HTML이다. `sheet`(multi-panel grid)와 `doc`(목차가 있는 single-column) template, diagram component, 선택적 narrated video/MP4 export를 제공한다. 프로젝트가 공개한 benchmark는 직접 HTML 생성 대비 output token과 시간이 줄었다고 보고하지만, 독립 검증 결과가 아니며 extra agent turn 때문에 비용은 감소하지 않았다는 점을 함께 고려해야 한다.

## Learning Path

- [ ] [[01-overview|개요]] — What/Why, 역할 분리, 핵심 특징
- [ ] [[02-ecosystem|생태계]] — 직접 HTML, Mermaid, Quarto, Marp/Marpit와 비교
- [ ] [[03-references|참고자료]] — 공식 README, Skill, CLI, benchmark 원문
- [ ] [[04-learning/01-getting-started|시작하기]] — skill 설치와 첫 HTML 렌더링
- [ ] [[04-learning/02-deep-dive|심화]] — component 선택, lint, patch, video workflow
- [ ] [[05-projects|프로젝트]] — architecture, ADR, incident, security review 적용
- [ ] [[cheatsheet|치트시트]] — command와 component 빠른 참조

## When To Use

- agent의 research·기술 설명을 채팅 prose 대신 공유 가능한 offline artifact로 전달할 때
- architecture onboarding, 비교표, lifecycle, timeline처럼 정보 밀도가 높은 설명을 빠르게 읽히게 할 때
- bespoke UI보다 일관된 layout과 재현 가능한 렌더링이 중요한 경우
- source Markdown을 보존하며 panel 단위로 반복 수정할 때

## When Not To Use

- pixel-level의 고유 UI·interaction·접근성 동작을 정밀하게 구현해야 할 때
- 기존 문서 사이트에 diagram 하나만 삽입하면 되는 경우(Mermaid 등이 더 단순할 수 있음)
- executable analysis, citation pipeline, PDF/Word 등 다중 출판 형식이 핵심인 경우(Quarto 검토)
- 발표 slide deck이 최종 산출물인 경우(Marp/Marpit 검토)

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]] — agent에 tool capability를 전달하는 표준

## Sources

- https://github.com/QingYunA/answer-me-with-html
- https://raw.githubusercontent.com/QingYunA/answer-me-with-html/main/skills/answer-me-with-html/SKILL.md
- https://raw.githubusercontent.com/QingYunA/answer-me-with-html/main/bench/README.md
