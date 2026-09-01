---
date: 2026-09-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Affinity AI Connector for Claude

> **한 줄 정의**: Claude Desktop이 local MCP server를 통해 실행 중인 Affinity 문서와 Scripting API를 조작하도록 연결하는 자연어 기반 디자인 자동화 계층.

## Overview

Affinity AI Connector for Claude는 반복적인 design production work를 자연어로 설명하면 Claude가 Affinity용 script를 만들고 실행하게 해 주는 desktop integration이다. 2026년 4월 Canva Create 2026에서 공개됐으며, 조사 기준일인 2026-09-01 현재 beta다.

- 대상: **Canva 계열 디자인 앱 Affinity**. 동명의 Affinity CRM MCP가 아니다.
- 연결 구조: Claude Desktop → Connector → Affinity의 local MCP server → Scripting API/document model
- 대표 작업: layer rename, batch resize, document-wide adjustment, vector cleanup, print/export preparation
- 재사용: 검증한 workflow를 Affinity **Scripting panel**에 저장해 반복 실행
- 비용: Connector beta는 무료지만 Claude account의 사용량 제한은 별도로 적용될 수 있다.
- 구분: 문서 자동화용 **AI Connector**와 생성·편집 모델 모음인 **Canva AI Studio**는 서로 다른 기능이다.

## Learning Path

- [ ] [[01-overview|Overview]] — 해결하는 문제와 핵심 특징 이해
- [ ] [[02-ecosystem|Ecosystem]] — Macro, 직접 scripting, Canva AI Studio와 비교
- [ ] [[03-references|References]] — 공식 문서와 용어 확인
- [ ] [[04-learning/01-getting-started|Getting started]] — 설치, 연결 확인, 안전한 첫 실행
- [ ] [[04-learning/02-deep-dive|Deep dive]] — MCP 구조, reusable script, 운영 안전성
- [ ] [[05-projects|Projects]] — 작은 실습부터 production workflow까지 적용
- [ ] [[cheatsheet|Cheatsheet]] — 설정 경로와 prompt pattern 빠르게 찾기

## When To Use

- layer/artboard 이름 정리처럼 현재 문서의 구조를 이해해야 하는 반복 작업
- 여러 매체 규격으로 resize·reformat·export하면서 layout을 보존해야 할 때
- parameter dialog를 가진 작은 custom tool을 빠르게 prototype할 때
- 자연어로 workflow를 탐색한 뒤 검증된 script로 고정하고 싶을 때
- non-destructive adjustment를 여러 object나 문서 전체에 일관되게 적용할 때

## When Not To Use

- 동일한 filter·resize·export를 그대로 반복해 Macro/Batch Job이면 충분할 때
- audit, test, version compatibility가 엄격한 장기 운영 자동화: 직접 scripting이 더 적합할 수 있다.
- 생성 이미지, Generative Fill, Remove Background 자체가 목적일 때: Canva AI Studio 영역이다.
- Affinity나 Claude Desktop을 실행할 수 없는 headless/server 환경
- 원본 복구 수단 없이 중요한 문서를 즉시 대량 수정해야 하는 경우

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]]
- [[tech/ai/agent-garden|Agent Garden]]

## Sources

- [Affinity AI Connector 설정 가이드](https://www.affinity.studio/help/ai-connector-setup/)
- [Affinity integrations](https://www.affinity.studio/integrations)
- [Automate design tasks in Affinity with Claude](https://www.affinity.studio/blog/automate-design-tasks-affinity-claude)
- [Canva AI integrations in Affinity](https://www.affinity.studio/canva-integrations)
- [Anthropic: Use connectors to extend Claude's capabilities](https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities)
- [MCP Architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture)

