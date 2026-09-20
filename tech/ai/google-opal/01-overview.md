---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Google Opal Overview

> [[README|목차로 돌아가기]]

## What

Google Opal은 Google Labs의 no-code AI mini-app builder다. 자연어 설명으로 workflow 초안을 만들거나 visual editor에서 node를 연결해, 입력부터 결과 화면까지 구성한다. 2025-07-24에 experimental tool로 공개됐고, 2025-12부터는 Gemini web app의 “Gems from Google Labs”에서도 Opal 기반 mini-app 생성·실행 경로가 제공됐다.

## Why

단일 chatbot prompt는 사용자 입력 수집, 다단계 조사·생성, 결과 형식, 재사용·공유를 일관되게 담기 어렵다. Opal은 그 과정을 명시적 graph로 만들어 intermediate result를 확인하고 같은 workflow를 다시 실행할 수 있게 한다.

```text
User Input / uploaded asset
          ↓
Generate nodes 또는 Agent Mode
  ├─ Gemini reasoning / Code Exec
  ├─ Search · Maps grounding
  ├─ Image · Video · TTS · Music
  └─ Persistent Memory / routing
          ↓
Output: dynamic webpage · Google Drive spreadsheet
          ↓
Preview / Console debugging → Share or Publish
```

## 핵심 특징

| 구성 | 역할 | 설계 포인트 |
|---|---|---|
| `User Input` | 사용자 값·파일 수집 | 질문을 작고 검증 가능한 field로 나눈다. |
| `Generate` | prompt 기반 변환 | `@` reference로 이전 step, asset, tool을 주입한다. |
| `Agent Mode` | reasoning·tool use·다단계 조정 | micro-step 나열보다 objective와 제약을 명확히 쓴다. |
| `Output` | dynamic webpage, spreadsheet 등 | 독자가 바로 판단·행동할 수 있게 결과 format을 고정한다. |
| asset context | static file, YouTube link 등 | 출처·민감도·최신성을 먼저 판별한다. |

- 하나의 app에 복수 Output을 둘 수 있다.
- Console은 step별 실행, 순서와 실행 시간 확인을 지원해 prompt/flow debugging에 유용하다.
- Opal은 Google Drive 파일로 저장되고 version history가 자동 저장된다. 단, 과거 version 복원은 그 이후 version을 영구 삭제한다.
- Agent Mode 문서에는 Gemini 3, Veo 3.1, Nano Banana, Gemini TTS, Lyria, Search/Maps, Python Code Exec, Memory가 toolkit으로 열거돼 있다. 실제 제공 여부는 계정·시점에 따라 확인한다.

## 신뢰와 공유 경계

private가 기본값이지만, editor/remix 권한을 주면 prompt graph가 보일 수 있다. Drive file 공유도 우회 노출 경로가 될 수 있으므로 publish 전 asset, prompt, sharing ACL을 함께 점검한다. Opal 데이터는 generative model training에 사용하지 않는다고 명시되지만 일부 prompt는 troubleshooting/use-case 이해를 위해 사람이 검토할 수 있다.

## Sources

- https://developers.google.com/opal/overview
- https://developers.google.com/opal/Agent_Mode
- https://developers.googleblog.com/en/introducing-opal/
- https://blog.google/innovation-and-ai/models-and-research/google-labs/mini-apps-opal-gemini-app-experiment/
- https://developers.google.com/opal/faq
