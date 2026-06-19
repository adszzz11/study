---
date: 2026-06-20
tags:
  - tech
  - ai
  - claude
  - anthropic
  - system-prompt
  - prompt-governance
status: learning
type: tech-tool-study
---

# Claude System Prompts Release Notes

> **한 줄 정의**: Claude System Prompts release notes는 `claude.ai` 웹/모바일 앱이 대화 시작 시 Claude에 주입하는 core system prompt의 공개 변경 로그이며, Claude API의 `system` parameter와는 별개다.

## 개요

Anthropic은 Claude 웹 인터페이스와 iOS/Android 앱에서 현재 날짜, 응답 형식, Markdown/code block 사용, 행동 지침 같은 기본 context를 system prompt로 주입한다. 이 prompt는 응답 품질과 일관성을 개선하기 위해 주기적으로 갱신되며, 공식 문서상 **Claude API에는 적용되지 않는다**고 명시되어 있다.

이 노트의 핵심 관점은 세 가지다.

- **Transparency**: ChatGPT류 서비스의 숨은 behavior policy 일부를 공개해 모델 동작 변화를 추적할 수 있다.
- **Reproducibility 한계**: 웹 Claude에서 보이는 행동은 API model weights만의 결과가 아니다.
- **Prompt governance**: system prompt가 제품 정책, UX, safety, formatting, tool behavior를 담는 runtime policy artifact가 되었다.

## 학습 경로

| 순서 | 파일 | 무엇을 배우나 |
|------|------|---------------|
| 1 | [[01-overview]] | What/Why, 공개 system prompt의 의미, 핵심 특징 |
| 2 | [[02-ecosystem]] | Anthropic, OpenAI, Gemini instruction primitive 비교 |
| 3 | [[03-references]] | 공식 문서와 확인해야 할 source URL |
| 4 | [[04-learning/01-getting-started]] | release notes 읽는 방법과 API system prompt와의 분리 |
| 5 | [[04-learning/02-deep-dive]] | versioning, serving layer, prompt leak, mid-conversation system messages |
| 6 | [[05-projects]] | prompt governance 실전 프로젝트 아이디어 |
| 7 | [[cheatsheet]] | 핵심 구분, 체크리스트, 빠른 참조 |

## 파일 구조

```text
https-platform-claude-com-docs-en-releas/
├── README.md
├── 01-overview.md
├── 02-ecosystem.md
├── 03-references.md
├── 04-learning/
│   ├── 01-getting-started.md
│   └── 02-deep-dive.md
├── 05-projects.md
└── cheatsheet.md
```

## 30초 핵심

- `System Prompts release notes`는 `claude.ai`와 모바일 앱용 core system prompt 변경 로그다.
- API 사용자는 Messages API의 `system` parameter로 직접 role/context를 지정해야 한다.
- 2026-06-20 기준 최신 항목은 **Claude Fable 5, June 9, 2026**이다.
- Claude 4.6 이후 dateless model ID는 alias가 아니라 pinned snapshot이다.
- model snapshot이 고정되어도 request router, safety classifiers, sampling logic 같은 serving infrastructure는 바뀔 수 있다.
- prompt leak 완전 방지는 어렵기 때문에 system prompt 분리, post-processing, audits, proprietary detail 최소화가 함께 필요하다.

## 관련 노트

- [[study/tech/ai/model-context-protocol-mcp]] - agent/tool context를 runtime에 주입하는 protocol 계층
- [[study/tech/ai/litellm]] - API gateway에서 model routing과 prompt policy를 관리하는 맥락
- [[study/tech/ai/ai-ecosystem/01-overview]] - AI ecosystem 안에서 provider별 instruction primitive 비교
- [[study/tech/ai/agent-orchestration/cli-agents]] - agent runtime prompt와 tool behavior가 결합되는 운영 맥락

---

**생성일**: 2026-06-20  
**상태**: 학습 중
