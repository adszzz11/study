---
date: 2026-06-20
tags:
  - tech
  - ai
  - claude
  - prompt-engineering
  - references
type: tech-tool-study
parent: "[[README]]"
---

# Claude Prompting Best Practices - 참고자료

> [[02-ecosystem|이전: 생태계]] | [[README|목차로 돌아가기]] | [[04-learning/01-getting-started|다음: 시작하기]]

---

## Anthropic 공식 문서

| 자료 | URL | 읽을 포인트 |
|------|-----|-------------|
| Prompting best practices | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | clear instruction, examples, XML tags, role prompting, long context |
| Models overview | https://platform.claude.com/docs/en/docs/about-claude/models/overview | 모델별 capability, thinking 지원, 최신 모델 차이 |
| Adaptive thinking | https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking | `thinking: {"type": "adaptive"}`, `output_config.effort` |
| Reduce hallucinations | https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations | unknown handling, direct quote grounding, citation |
| Increase consistency | https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/increase-consistency | output format, structured outputs, validation |
| Mitigate jailbreaks and prompt injections | https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks | direct/indirect injection, tool result boundary, JSON encoding |

---

## 비교 자료

| 자료 | URL | 읽을 포인트 |
|------|-----|-------------|
| OpenAI Prompt engineering guide | https://platform.openai.com/docs/guides/prompt-engineering | instructions, delimiters, examples, tools, structured outputs |
| Gemini prompting strategies | https://ai.google.dev/gemini-api/docs/prompting-strategies | clear task, examples, constraints, multimodal prompt |
| OWASP LLM01 Prompt Injection | https://genai.owasp.org/llmrisk/llm01-prompt-injection/ | direct/indirect prompt injection, mitigation controls |

---

## 읽는 순서

1. **Prompting best practices**: Claude prompting의 기본 mental model을 잡는다.
2. **Models overview**: 사용 중인 Claude 모델이 어떤 thinking/tool/output 기능을 지원하는지 확인한다.
3. **Adaptive thinking**: reasoning 깊이를 prompt 문구가 아니라 API option으로 제어하는 방식을 본다.
4. **Reduce hallucinations**: factual answer와 citation prompt를 설계한다.
5. **Mitigate jailbreaks**: untrusted content와 tool result를 instruction으로 취급하지 않는 방어를 배운다.
6. **OpenAI/Gemini/OWASP**: provider 공통 원칙과 보안 표준을 비교한다.

---

## 핵심 메모

- Prompt는 "모델에게 쓰는 자연어"가 아니라 "작업 계약서"에 가깝다.
- Claude에서는 XML tag가 prompt의 section boundary를 만드는 실용적인 도구다.
- 최신 모델에서는 reasoning을 유도하는 긴 문구보다 adaptive thinking/effort 같은 API option을 우선 고려한다.
- Tool result, 웹 문서, 사용자 업로드 파일은 untrusted data로 취급해야 한다.
- Prompt 품질은 평가셋과 회귀 테스트 없이는 장기적으로 유지하기 어렵다.

---

## 관련 노트

- [[study/tech/ai/claude]] - Claude 공식 기능과 모델별 차이 확인
- [[study/tech/ai/model-context-protocol-mcp]] - tool result와 external system boundary
- [[study/tech/ai/llm-wiki-study]] - 문서 기반 답변과 citation workflow
