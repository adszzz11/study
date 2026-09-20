---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Google Opal Ecosystem

> [[README|목차로 돌아가기]]

## 선택 기준

Opal은 “AI 응답”보다 “공유 가능한 interactive mini-app”을 빠르게 만드는 데 맞춘다. integration automation, code ownership, self-hosting 요구가 커지면 다른 도구가 더 적합하다.

| 제품 | 가장 적합한 경우 | Opal 대비 |
|---|---|---|
| **Google Opal** | 개인/팀용 AI mini-app, multimodal workflow, 즉시 공유 | no-code와 Google AI 조합에 강함. Labs 제품이라 production governance에는 신중해야 한다. |
| **Gemini classic Gems** | 특정 역할의 반복 chat assistant | custom instruction/knowledge 기반 expert chat에 적합. Opal은 interactive UI와 multi-model workflow가 중심이다. |
| **Google AI Studio Build mode** | code ownership이 필요한 web/full-stack/Android app | full-stack runtime·Kotlin/Jetpack Compose 같은 code 산출물이 목표다. Opal은 workflow 중심이다. |
| **n8n** | SaaS/API 간 business automation, self-hosting | API 연결·데이터 변환·운영 automation이 더 깊다. |
| **Zapier Agents** | 많은 SaaS를 쓰는 업무 자동화 | app ecosystem/action automation이 강점이다. |
| **Langflow** | 개발팀의 RAG/agent/MCP와 model·vector DB 선택 | open-source Python framework로 API·MCP·self-host customization이 깊다. |

## 빠른 결정표

| 질문 | 권장 |
|---|---|
| 비개발자가 멀티모달 결과물을 공개 mini-app으로 시험하는가? | Opal |
| Google 서비스보다 다양한 SaaS의 record를 갱신해야 하는가? | n8n 또는 Zapier Agents |
| source code, CI/CD, backend API를 소유해야 하는가? | AI Studio Build mode 또는 일반 개발 stack |
| on-premise, 임의 model·vector DB, MCP server를 세밀하게 제어해야 하는가? | Langflow |
| 단지 고정 역할의 chat assistant가 필요한가? | Gemini classic Gems |

## Sources

- https://ai.google.dev/gemini-api/docs/aistudio-build-mode
- https://docs.n8n.io/
- https://help.zapier.com/hc/en-us/articles/24393442652557-Build-an-agent-in-Zapier-Agents
- https://docs.langflow.org/next
- https://developers.google.com/opal
