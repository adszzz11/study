---
date: 2026-06-20
tags:
  - tech
  - ai
  - notebooklm
  - gemini
status: learning
type: tech-tool-study
---

# NotebookLM

> **한 줄 정의**: NotebookLM은 사용자가 업로드하거나 검색해 넣은 sources를 기반으로 답변, 요약, Audio/Video Overview, study artifact를 생성하는 Google의 Gemini 기반 source-grounded research assistant다.

## 개요

NotebookLM의 핵심은 긴 문서 묶음을 LLM에게 그냥 던지는 것이 아니라, **notebook 안의 sources**를 기준으로 답변과 citations를 받는 research workflow다. PDF, websites, YouTube transcript, audio, Google Docs/Slides/Sheets, Markdown, CSV, image 등을 source로 넣고, 질문/요약/학습자료 생성을 수행한다.

CLI에 대해서는 구분이 필요하다. 2026-06 기준 Google 공식 문서에서 확인되는 것은 NotebookLM web/mobile 제품이며, **NotebookLM 전용 공식 CLI/API는 확인되지 않는다**. 터미널에서 Gemini를 쓰는 공식 도구는 별도 제품인 **Gemini CLI**다.

```text
Sources
  -> Notebook
    -> Source-grounded chat with citations
    -> Studio outputs
      -> Audio Overview / Video Overview / Mind Map / Flashcards / Quiz / Reports
```

---

## 학습 경로

### 1단계: 제품의 문제의식 이해

- [ ] [[01-overview|개요]] 읽기 - source-grounded Q&A, citations, Studio artifacts
- [ ] NotebookLM과 일반 chatbot의 차이를 `source boundary` 관점에서 정리
- [ ] 공식 NotebookLM CLI/API가 없다는 점과 Gemini CLI의 역할 구분

### 2단계: 생태계 비교

- [ ] [[02-ecosystem|생태계]]에서 NotebookLM, Gemini CLI, Gemini Deep Research, ChatGPT Projects, Claude Projects, Perplexity Spaces, Custom RAG 비교
- [ ] browser/mobile UX 중심 도구와 scriptable CLI/API 중심 도구의 차이 정리
- [ ] [[study/tech/ai/agent-orchestration/cli-agents]]와 연결해 terminal-first AI agent 맥락 확인

### 3단계: 공식 자료 확인

- [ ] [[03-references|참고자료]]에서 Google NotebookLM Help, source limits, Audio/Video Overview, Gemini CLI 공식 자료 확인
- [ ] privacy, Workspace data protection, sharing policy를 별도 체크

### 4단계: 실습

- [ ] [[04-learning/01-getting-started|시작하기]] - notebook 생성, source 5-10개 추가, citation 품질 비교
- [ ] [[04-learning/02-deep-dive|심화]] - Studio outputs, Deep/Fast Research, CLI 대체 workflow 설계

### 5단계: 실전 적용

- [ ] [[05-projects|실전 프로젝트]] - 기술 리서치 dossier, onboarding notebook, knowledge base, CLI 대체 프로젝트
- [ ] [[cheatsheet|치트시트]] - limits, prompt, CLI 구분, 의사결정 기준 빠른 참조

---

## 파일 구조

```text
notebooklm-에-대해-학습하고-cli에-대해-알려줘-있다고-하던데/
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
| 개요 | [[01-overview]] | What/Why, 특징, 아키텍처, CLI 현실 |
| 생태계 | [[02-ecosystem]] | NotebookLM과 대안 도구 비교 |
| 참고자료 | [[03-references]] | 공식 문서, Help, Gemini CLI, 논문 |
| 시작하기 | [[04-learning/01-getting-started]] | 첫 notebook과 citation 검증 실습 |
| 심화 | [[04-learning/02-deep-dive]] | Studio, research feature, automation 대안 |
| 프로젝트 | [[05-projects]] | 실무 적용 아이디어 |
| 치트시트 | [[cheatsheet]] | 빠른 명령/한계/프롬프트 |

---

## 관련 노트

- [[study/tech/ai/agent-orchestration/cli-agents]] - Gemini CLI와 다른 CLI agents 비교
- [[study/tech/ai/model-context-protocol-mcp]] - NotebookLM-like workflow를 MCP/RAG로 대체할 때의 integration layer
- [[study/tech/ai/litellm]] - custom RAG나 internal assistant에서 LLM routing을 분리하는 패턴
- [[study/tech/ai/ai-ecosystem]] - AI tool landscape 맥락

---

**생성일**: 2026-06-20  
**상태**: 학습 중

## Q&A
**Q:** Claude plugin 같은 NotebookLM 확장이나 CLI 도구가 있는가?
**A:** NotebookLM 자체에는 2026-06 기준으로 공식 plugin/extension, 전용 CLI, 공식 API가 확인되지 않는다. NotebookLM은 sources를 넣고 citations, Audio/Video Overview, study artifacts를 만드는 web/mobile 중심 research product로 보는 편이 맞다. Claude 쪽을 말한 것이라면 NotebookLM plugin이라기보다 Claude Code 같은 CLI agent나 MCP 연동 생태계를 별도로 보는 문제다. terminal에서 local repo/docs를 다루려면 Gemini CLI, Codex, Claude Code 같은 CLI agent가 더 적합하고, NotebookLM-like workflow를 자동화하려면 custom RAG나 MCP server로 sources/search/read/report tool을 설계하는 쪽이 현실적이다.
