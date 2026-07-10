---
date: 2026-06-20
tags:
  - tech
  - ai
  - notebooklm
  - overview
type: tech-tool-study
parent: "[[README]]"
---

# NotebookLM - 개요

> [[README|목차로 돌아가기]] | [[02-ecosystem|다음: 생태계]]

---

## 1. What - NotebookLM이란?

NotebookLM은 Google의 Gemini 기반 **source-grounded research assistant**다. 사용자가 notebook에 sources를 넣으면, NotebookLM은 그 sources를 근거로 질문에 답하고, 요약하고, 학습자료와 media artifact를 생성한다.

| 용어 | English | 설명 |
|------|---------|------|
| Notebook | notebook workspace | sources, notes, chat, Studio outputs를 묶는 작업 단위 |
| Source | source document | PDF, web URL, YouTube transcript, audio, Docs/Slides/Sheets 등 가져온 자료 |
| Citation | inline citation | 답변 근거를 source 위치와 연결하는 표시 |
| Studio | artifact generator | Audio/Video Overview, Mind Map, Flashcards, Quiz, report 등을 만드는 영역 |
| Grounding | source grounding | 모델 답변을 notebook sources에 묶는 방식 |

```text
User question
  -> selected/all sources retrieval
  -> Gemini reasoning
  -> answer with citations
  -> optional Studio artifact
```

## 2. Why - 왜 필요한가?

NotebookLM의 문제의식은 "긴 문서 묶음을 LLM에게 던지고 요약을 믿는 것"의 위험을 줄이는 데 있다. 일반 chatbot에 파일을 올리면 편하지만, 어떤 문서의 어느 주장에 근거했는지 추적하기 어렵다.

| 문제 | 일반 LLM 사용 | NotebookLM 접근 |
|------|---------------|-----------------|
| 근거 추적 | 답변이 그럴듯해도 출처 확인이 어려움 | source 기반 inline citation 제공 |
| 문서 묶음 관리 | 대화마다 파일/맥락을 다시 구성 | notebook 단위로 sources 유지 |
| 학습자료 생성 | prompt를 직접 설계해야 함 | Studio에서 guide, quiz, flashcards 등 생성 |
| 검증 | hallucination 여부를 수동으로 찾아야 함 | citation 없는 주장, source 누락을 점검하는 workflow 가능 |

## 3. 핵심 특징

### Source-grounded RAG UX

- NotebookLM은 notebook 안의 sources를 검색해 답변을 구성한다.
- 답변은 sources에 근거해야 하며, 정보가 sources에 없으면 답하지 못할 수 있다.
- `all sources`와 selected sources를 바꿔가며 답변 범위와 citation 품질을 비교할 수 있다.

### 지원 source types와 limits

| Source type | 예시 | 주의점 |
|-------------|------|--------|
| Local files | PDF, TXT, Markdown, DOCX, PPTX, CSV, ePub | source당 500,000 words 또는 upload 200MB 기준 |
| Google Drive | Docs, Slides, Sheets | Drive 원본과 auto-sync 가능, 권한 변화에 영향 |
| Web | Web URL | HTML text 중심으로 import, paywall/embedded media 제한 |
| YouTube | public YouTube URL transcript | public video와 captions/transcript 필요 |
| Audio | MP3, WAV 등 | transcript/analysis 품질 확인 필요 |
| Images | jpg, png, webp 등 | image type별 처리 품질 차이 가능 |

Free 기준으로 notebook당 source 50개 제한이 명시되어 있다. 유료 plan은 더 높은 limit과 collaboration/enterprise 기능을 제공할 수 있으므로 실제 도입 전 최신 plan 문서를 확인한다.

### Studio outputs

| Output | 용도 | 검증 포인트 |
|--------|------|-------------|
| Audio Overview | AI hosts가 source 핵심을 discussion 형식으로 설명 | 재미있는 표현이 근거를 과장하지 않는지 확인 |
| Video Overview | narration/visual 중심 video summary | 시각 자료와 source 내용의 대응 확인 |
| Mind Map | 개념 구조화 | hierarchy가 source 구조를 왜곡하지 않는지 확인 |
| Flashcards | 암기/복습 | 카드 정답의 citation과 단서 확인 |
| Quizzes | 학습 평가 | 보기와 해설이 source에 있는지 확인 |
| Infographic / Slide Deck / Data Tables | 발표/보고 artifact | 숫자, 표, 이미지 생성 오류 확인 |

### Research features

- **Fast Research / Deep Research** 흐름을 통해 web 또는 Drive sources를 찾아 notebook에 가져올 수 있다.
- Deep Research는 여러 웹사이트를 browse해 report와 sources를 만든 뒤 import하는 agentic feature로 이해하면 된다.
- 자동으로 가져온 sources라도 품질, 최신성, 권위, 중복 여부는 사용자가 검토해야 한다.

## 4. CLI 현실

NotebookLM과 CLI는 분리해서 봐야 한다.

| 주장 | 판단 |
|------|------|
| "NotebookLM 공식 CLI가 있다" | 2026-06 기준 공식 Help/제품 문서에서 전용 CLI/API는 확인되지 않는다. |
| "Google Gemini CLI가 있다" | 맞다. Gemini CLI는 terminal에서 Gemini를 쓰는 open-source AI agent다. |
| "Gemini CLI로 NotebookLM notebook을 직접 조작한다" | 공식 NotebookLM notebook 조작 도구로 보기는 어렵다. |
| "CLI 자동화가 필요하다" | Gemini CLI, Google AI Studio/Vertex AI, custom RAG, MCP workflow를 검토한다. |

```bash
# Gemini CLI 예시: NotebookLM 전용 CLI가 아니라 terminal-first Gemini agent
npx @google/gemini-cli

# prompt mode 예시
gemini -p "Summarize the markdown files in this folder with citations to file paths."
```

## 5. 장점과 한계

| 구분 | 내용 |
|------|------|
| 장점 | sources와 citations 중심 UX, 빠른 학습 artifact 생성, 비개발자도 쓰기 쉬운 web/mobile workflow |
| 장점 | Audio/Video Overview처럼 문서를 media로 재가공하는 기능이 강함 |
| 한계 | 공식 CLI/API 부재, Google 제품 UX 안에서 사용, 자동화/파이프라인 통합이 제한적 |
| 한계 | AI-generated artifact는 오류 가능성이 있어 citation과 원문 검증이 필요 |
| 한계 | source limits, plan, Workspace policy, sharing policy를 도입 전에 확인해야 함 |

## 관련 노트

- [[study/tech/ai/agent-orchestration/cli-agents]] - NotebookLM CLI 혼동 지점인 Gemini CLI 확인
- [[study/tech/ai/model-context-protocol-mcp]] - CLI/RAG 자동화를 tool workflow로 만들 때의 protocol layer
- [[study/tech/ai/litellm]] - custom assistant에서 model routing을 분리하는 방식

---

## References

- [Google NotebookLM](https://notebooklm.google/)
- [NotebookLM Help - Learn about NotebookLM](https://support.google.com/notebooklm/answer/16164461)
- [NotebookLM Help - Add or discover new sources](https://support.google.com/notebooklm/answer/16215270)
- [Google Blog - Gemini CLI](https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemini-cli-open-source-ai-agent/)
- [Gemini CLI GitHub](https://github.com/google-gemini/gemini-cli)
