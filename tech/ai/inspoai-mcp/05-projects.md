---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# inspoAI MCP — Projects

> [[04-learning/02-deep-dive|이전: Deep Dive]] · [[README|목차]] · [[cheatsheet|다음: Cheatsheet]]

## 1. Landing Page Sprint

경쟁 제품 다섯 개의 hero, social proof, pricing pattern을 조사하고 component hierarchy와 React 구현안을 만든다.

- **Input**: audience, value proposition, brand token, 금지 요소
- **Output**: source-linked pattern matrix, 선택 rationale, component tree, 구현 PR
- **검증**: 각 pattern이 source URL에 연결되고 copy/visual asset을 복제하지 않는지 review

## 2. Design-System Gap Audit

Figma MCP로 내부 token/component를 읽고, Inspo AI MCP로 외부 convention을 조사해 누락된 state와 accessibility pattern을 backlog로 만든다.

| 산출물 | 예시 |
|---|---|
| Gap matrix | form error, loading, empty, disabled, focus state |
| Backlog | owner, impact, evidence, token/component 영향 |
| Decision record | 외부 reference를 채택·기각한 이유 |

## 3. Brand-safe UI Generator

브랜드 가이드와 curated moodboard를 context로 주고, 생성 UI를 typography·spacing·contrast 기준으로 review하는 human-in-the-loop pipeline을 구성한다.

성공 기준은 “레퍼런스와 비슷함”이 아니라 brand token 준수, accessibility 통과, source 추적 가능성, 그리고 human approval이다.

## 4. Product Discovery Workshop

PM, Designer, Engineer가 같은 reference set을 검토한다. agent는 선택 이유와 구현 제약을 기록하고, 팀은 각 후보를 채택·보류·기각으로 결정한다.

```text
brief -> shared reference set -> pattern critique
      -> decision log -> implementation constraints -> prototype
```

## Sources

- https://www.inspoai.io/mcp
- https://developers.figma.com/docs/figma-mcp-server/
- https://modelcontextprotocol.io/specification/2025-06-18/server
