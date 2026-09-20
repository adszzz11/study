---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Google Opal

> **한 줄 정의**: Google Opal은 자연어와 visual workflow로 prompt·AI model·tool을 연결해, 코딩 없이 배포 가능한 AI mini-app을 만드는 Google Labs 실험 제품이다.

## Overview

Opal은 반복 AI 업무를 `User Input → Generate/Agent → Output` 흐름으로 만들고, hosted preview·공유·publish까지 제공한다. 자연어로 초안을 만들고 node-based editor에서 세부 흐름을 다듬는 방식이 핵심이다.

> [!NOTE]
> 조사 기준은 2026-09-20이다. Google Labs 실험 제품이므로 model, tool, 접근 조건 및 UI는 바뀔 수 있다. 배포 전에는 [공식 Overview](https://developers.google.com/opal/overview)와 [FAQ](https://developers.google.com/opal/faq)를 다시 확인한다.

## Learning Path

- [ ] [[01-overview|1. Overview — What, Why, 핵심 개념]]
- [ ] [[02-ecosystem|2. Ecosystem — 대안과 선택 기준]]
- [ ] [[03-references|3. References — 공식 문서 지도]]
- [ ] [[04-learning/01-getting-started|4. Getting Started — 첫 mini-app 만들기]]
- [ ] [[04-learning/02-deep-dive|5. Deep Dive — Agent, context, debugging, sharing]]
- [ ] [[05-projects|6. Projects — 실전 적용 과제]]
- [ ] [[cheatsheet|7. Cheatsheet — 설계·배포 점검표]]

## When To Use

- 입력, 조사·생성 단계, 결과 UI를 한 번에 묶은 개인/소규모 팀용 mini-app이 필요할 때
- Search·Maps·이미지·영상·TTS 등 Google-native multimodal 도구를 빠르게 조합할 때
- server 코드와 hosting 운영 없이 prototype을 공유·remix할 때
- 문서·사진·YouTube 링크를 context로 넣어 반복 산출물을 만들 때

## When Not To Use

- 엄격한 SLA, audit, data residency, enterprise governance가 필요한 production system
- 복잡한 SaaS/API automation, self-hosting, 자체 model·vector DB 제어가 핵심일 때
- prompt graph나 Drive 공유 권한 노출을 허용할 수 없는 민감 정보 workflow
- 검증 없이 사실성 높은 답변을 자동 publish해야 하는 업무

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/gemini/README|Gemini]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]]

## Sources

- https://developers.google.com/opal
- https://developers.google.com/opal/overview
- https://developers.google.com/opal/faq
- https://developers.googleblog.com/en/introducing-opal/
