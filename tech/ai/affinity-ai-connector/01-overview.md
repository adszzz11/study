---
date: 2026-09-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Affinity AI Connector 개요

## What

Affinity AI Connector for Claude는 실행 중인 Affinity desktop app과 Claude Desktop을 **Model Context Protocol (MCP)**로 연결한다. 사용자가 작업을 자연어로 지시하면 Claude가 Affinity document model을 다루는 script와 tool argument를 만들고, Connector를 통해 현재 문서에 실행한다.

결과물은 일회성 command에만 머물지 않는다. 잘 동작하는 workflow를 Scripting panel에 저장하면 Claude를 다시 호출하지 않고도 deterministic automation에 가까운 형태로 재사용할 수 있다.

## Why

전문 디자인의 병목은 창작뿐 아니라 반복적인 production work에서도 발생한다.

- 수백 개의 layer와 artboard 이름 정리
- 여러 채널용 resize, reformat, export
- 문서 전체에 같은 adjustment 적용
- SVG path cleanup과 단위 표준화
- print-ready PDF/PNG 생성과 파일명 규칙 적용
- client handoff용 파일 packaging

Macro는 정해진 순서를 반복하는 데 강하지만 문서의 의미나 사용자의 문맥적 요구를 해석하기 어렵다. 직접 scripting은 유연하지만 API 학습과 coding 역량이 필요하다. AI Connector는 자연어 탐색과 executable script 사이를 연결한다.

## 핵심 특징

| 특징 | 의미 | 주의점 |
|---|---|---|
| Natural-language workflow | 요청을 실행 가능한 Affinity script로 변환 | 모호한 prompt는 예상보다 넓은 변경을 만들 수 있음 |
| Context-aware operation | 현재 document, selection, layer, artboard를 대상으로 실행 | 대상과 범위를 명시해야 함 |
| Reusable scripting | 검증한 workflow를 Scripting panel에 저장 | 앱 update 후 regression test 필요 |
| Custom UI | 숫자·색상·강도 등을 받는 dialog/tool 생성 | generated script의 source review 권장 |
| Non-destructive 지향 | adjustment/layer 기반 workflow를 구성 가능 | 모든 생성 script가 자동으로 안전한 것은 아님 |
| MCP 기반 | Claude가 표준화된 tool interface를 사용 | Affinity 내부 tool schema/transport는 공개 contract가 아님 |

공식 사례에는 layer rename, batch resize, non-destructive adjustment, vector cleanup, print preparation, pattern generator, Roughen Curves가 있다.

## 반드시 구분할 것

### AI Connector for Claude

- document 조작과 workflow 자동화
- script 및 custom dialog 생성
- Claude Desktop과 Affinity를 모두 실행해야 하는 local integration

### Canva AI Studio

- Generative Fill, Generate Image/Vector, Remove Background, Super Resolve
- 콘텐츠 생성·보정·selection 중심
- Canva premium plan 요구 가능

Connector beta가 무료라는 안내와 Claude account 사용량, Canva AI Studio entitlement는 각각 별개의 조건이다.

## 제약

- 조사 기준일 2026-09-01 현재 beta이므로 UI, capability, compatibility가 바뀔 수 있다.
- 공식 지원 desktop platform은 macOS와 Windows다.
- Claude가 만든 script는 문서 구조나 Affinity version 차이로 실패할 수 있다.
- 내부 port, tool name, protocol version을 추측해 의존하면 update에 취약하다.

## Sources

- [Affinity integrations](https://www.affinity.studio/integrations)
- [Automate design tasks in Affinity with Claude](https://www.affinity.studio/blog/automate-design-tasks-affinity-claude)
- [Canva AI integrations in Affinity](https://www.affinity.studio/canva-integrations)
- [Affinity AI Connector 설정 가이드](https://www.affinity.studio/help/ai-connector-setup/)

