---
date: 2026-06-20
tags:
  - tech
  - ai
  - claude
  - prompt-engineering
status: learning
type: tech-tool-study
---

# Claude Prompting Best Practices

> **한 줄 정의**: Claude Prompting Best Practices는 Claude API와 agentic workflow에서 원하는 정확도, 형식, reasoning, tool use, safety를 얻기 위해 prompt를 명시적, 구조적, 검증 가능하게 설계하는 실무 지침이다.

## 개요

Anthropic 공식 문서의 prompt engineering reference는 Claude를 "맥락 없는 뛰어난 신입 직원"처럼 다루라고 설명한다. 즉, Claude가 의도를 추측하게 두기보다 `goal`, `context`, `constraints`, `output format`, `examples`, `success criteria`를 명확히 제공해야 한다.

2025-2026년의 prompt engineering은 단순히 좋은 질문을 쓰는 기술을 넘어 `context engineering`, `adaptive thinking`, `tool use`, `agentic systems`, `prompt injection defense`, `evaluation`까지 포함하는 운영 설계로 확장됐다.

---

## Quick Start

```xml
<role>
You are a senior customer support triage agent.
</role>

<task>
Classify the ticket and return only valid JSON.
</task>

<context>
Audience: B2B SaaS operations team.
Priority rules: security incidents are always P0.
</context>

<input>
{{ticket_text}}
</input>

<output_format>
{
  "category": "billing|security|bug|feature_request|other",
  "priority": "P0|P1|P2|P3",
  "rationale": "one sentence"
}
</output_format>
```

---

## 학습 경로

### 1단계: 문제의식 이해

- [ ] [[01-overview|개요]] 읽기 - Claude가 모호한 prompt에서 실패하는 방식 이해
- [ ] `clear and direct instruction`, `context-first design`, `XML structuring` 용어 정리
- [ ] 좋은 prompt를 "질문"이 아니라 "작업 명세서(task specification)"로 바라보기

### 2단계: 생태계 비교

- [ ] [[02-ecosystem|생태계]]에서 Claude, OpenAI GPT, Google Gemini prompting style 비교
- [ ] [[study/tech/ai/claude]]와 연결해 Claude API/Claude Code 맥락 파악
- [ ] [[study/tech/ai/model-context-protocol-mcp]]와 연결해 tool result trust boundary 이해

### 3단계: 공식 문서 읽기

- [ ] [[03-references|참고자료]]에서 Prompting best practices, Adaptive thinking, Guardrails 확인
- [ ] hallucination 감소, consistency 증가, prompt injection mitigation 문서 읽기
- [ ] OWASP LLM01 Prompt Injection을 보안 관점에서 함께 확인

### 4단계: 실습

- [ ] [[04-learning/01-getting-started|시작하기]] - 기본 XML prompt와 few-shot prompt 작성
- [ ] [[04-learning/02-deep-dive|심화]] - tool use, adaptive thinking, guardrails, evaluation 설계

### 5단계: 실전 적용

- [ ] [[05-projects|실전 프로젝트]] - support triage, code review, RAG answer, agent tool workflow 구현
- [ ] [[cheatsheet|치트시트]] - prompt template, anti-pattern, 보안 체크리스트 빠른 참조

---

## 파일 구조

```text
https-platform-claude-com-docs-en-build/
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

## 바로가기

| 단계 | 파일 | 설명 |
|------|------|------|
| 개요 | [[01-overview]] | What/Why, 핵심 특징, 장점과 한계 |
| 생태계 | [[02-ecosystem]] | Claude/OpenAI/Gemini/OWASP 비교 |
| 참고자료 | [[03-references]] | 공식 문서와 보안 자료 |
| 시작하기 | [[04-learning/01-getting-started]] | 기본 prompt 작성 실습 |
| 심화 | [[04-learning/02-deep-dive]] | reasoning, tool use, injection defense |
| 프로젝트 | [[05-projects]] | 실전 적용 아이디어 |
| 치트시트 | [[cheatsheet]] | 빠른 템플릿과 체크리스트 |

---

## 관련 노트

- [[study/tech/ai/claude]] - Claude API, Claude Code, MCP, skills 맥락
- [[study/tech/ai/codex]] - Codex prompting/workflow와 비교
- [[study/tech/ai/model-context-protocol-mcp]] - agent tool/data integration protocol
- [[study/tech/ai/litellm]] - multi-provider LLM gateway와 evaluation 운영

---

**생성일**: 2026-06-20  
**상태**: 학습 중
