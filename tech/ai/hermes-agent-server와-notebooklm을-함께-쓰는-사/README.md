---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Hermes Agent Server와 NotebookLM을 함께 쓰는 사례

> **한 줄 정의**: Hermes Agent가 학습·대화에서 만든 검증 가능한 Study Note를 Google Docs/Drive로 발행하고, NotebookLM이 자동 동기화된 source로 읽어 질의·복습·Audio Overview에 쓰는 개인 지식 파이프라인이다.

## Overview

Hermes의 `MEMORY.md`와 `USER.md`는 현재 작업에 필요한 사실과 선호를 담는 작고 curated된 memory다. 여기에 학습 원문, 인용, 논증, 오답을 계속 누적하면 retrieval 품질과 검토 가능성이 함께 떨어진다.

대신 Hermes가 research 결과를 **검토 가능한 Study Note**로 추출·검증·정리하고, 주제별 단일 Google Doc으로 발행한다. NotebookLM은 그 Doc을 source-grounded 학습 계층으로 사용한다. 즉, Hermes는 작업과 기억을, NotebookLM은 읽기·질문·복습을 맡는다.

```text
Hermes sessions / web research / external memory
                    │
          Extract → Verify → Curate
                    │
     Study Note (.md 또는 Google Doc)
                    │
        Google Drive의 단일 Google Doc
                    │ (NotebookLM auto-sync)
              NotebookLM notebook
                    │
       Q&A · 비교 · quiz · briefing · Audio Overview
```

## Learning Path

- [ ] [[01-overview|1. Overview — What, Why, architecture]]
- [ ] [[02-ecosystem|2. Ecosystem — 대안과 선택 기준]]
- [ ] [[03-references|3. References — 공식 문서 지도]]
- [ ] [[04-learning/01-getting-started|4. Getting Started — 첫 Study Note 발행]]
- [ ] [[04-learning/02-deep-dive|5. Deep Dive — memory, provenance, automation]]
- [ ] [[05-projects|6. Projects — 단계별 실습 과제]]
- [ ] [[cheatsheet|7. Cheatsheet — 운영 체크리스트]]

## When To Use

- Hermes로 조사·대화한 결과를 사람이 다시 읽고 반복 학습하고 싶을 때
- 주제별 living document를 NotebookLM에서 source 근거와 함께 질문하고 싶을 때
- agent의 operational memory와 장기 학습 기록을 분리하고 싶을 때
- Google Drive를 이미 개인 지식 문서의 공유·버전 관리 장소로 쓸 때
- 원문 URL, 확신도, open question을 남긴 재검증 가능한 노트가 필요할 때

## When Not To Use

- Hermes가 NotebookLM의 질의 결과까지 공식 write/read API로 완전 자동화해야 할 때
- 문서의 업데이트를 검토 없이 곧바로 external source에 공개하면 안 되는 민감한 업무일 때
- agent가 실시간으로 대규모 지식 retrieval을 해야 하고 사람이 읽는 학습 산출물은 불필요할 때
- Enterprise Cloud/IAM 운영, source 권한, 감사 요구를 감당할 수 없는데 Enterprise API를 도입하려 할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]]
- [[tech/ai/litellm/README|LiteLLM]]

## Sources

- https://github.com/NousResearch/hermes-agent
- https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/api-server.md
- https://hermes-agent.nousresearch.com/docs/user-guide/features/memory
- https://support.google.com/gemininotebook/answer/16215270?co=GENIE.Platform%3DDesktop&hl=en-6
- https://workspaceupdates.googleblog.com/2026/05/keep-your-sources-up-to-date-with-automatic-Drive-syncing-in-NotebookLM.html
