---
date: 2026-06-20
tags:
  - tech
  - ai
  - notebooklm
  - cheatsheet
type: tech-tool-study
parent: "[[README]]"
---

# NotebookLM - 치트시트

> [[README|목차로 돌아가기]]

---

## 한 줄 구분

| 항목 | 기억할 문장 |
|------|-------------|
| NotebookLM | sources 기반으로 답변, citations, study/media artifacts를 만드는 Google research assistant |
| Gemini CLI | terminal에서 Gemini를 쓰는 Google open-source AI agent |
| NotebookLM CLI | 2026-06 기준 공식 전용 CLI/API 확인되지 않음 |
| Custom RAG | CLI/API/권한/파이프라인이 필요할 때 직접 구축하는 대안 |

## 핵심 Workflow

```text
Create notebook
  -> Add sources
  -> Ask source-grounded questions
  -> Audit citations
  -> Generate Studio outputs
  -> Review artifacts
  -> Share/export/use
```

## Source Limits 빠른 확인

| 항목 | Free 기준 메모 |
|------|----------------|
| Sources per notebook | 50개 |
| Words per source | 500,000 words |
| Local upload size | 200MB |
| Slides | Google Slides up to 100 slides |
| Sheets | Google Sheets 100k tokens 기준 언급 |

> Plan과 limits는 바뀔 수 있으므로 도입 전 공식 `Upgrade/limits`와 `Add or discover new sources` 문서를 다시 확인한다.

## 지원 Source Types

| Type | 예시 |
|------|------|
| Files | PDF, TXT, Markdown, DOCX, PPTX, CSV, ePub |
| Google Drive | Docs, Slides, Sheets |
| Web | Web URLs |
| Video | public YouTube URLs with transcript/captions |
| Audio | MP3, WAV 등 |
| Images | jpg, png, webp, gif, tiff 등 |
| Paste | copied text |

## Studio Outputs

| Output | 용도 |
|--------|------|
| Audio Overview | podcast-like discussion summary |
| Video Overview | narrated visual explainer |
| Mind Map | concept structure |
| Flashcards | spaced review / memorization |
| Quizzes | self-test |
| Infographic | visual summary |
| Slide Deck | presentation draft |
| Data Tables | structured extraction |
| Briefing/Study Guide | reading summary |

## 검증 Prompt

```text
"sources만 근거로 답해줘. source에 없는 내용은 'source에 없음'이라고 표시해줘."
```

```text
"답변의 모든 claim을 표로 분해하고, citation, source name, confidence, 검증 필요 여부를 붙여줘."
```

```text
"citation이 없는 주장만 추려서 왜 문제가 되는지와 확인할 source를 제안해줘."
```

```text
"공식 문서에 근거한 내용과 비공식 해석을 분리해줘."
```

```text
"NotebookLM 자체 기능, Gemini CLI 기능, 비공식 자동화 가능성을 구분해서 설명해줘."
```

## CLI 대체 명령

```bash
# Gemini CLI 시작
npx @google/gemini-cli

# global install
npm install -g @google/gemini-cli

# prompt mode
gemini -p "Summarize local markdown files into a Korean study note with file path citations."
```

## 선택 기준

| 필요 | 선택 |
|------|------|
| 빠른 문서 학습, citations, Audio/Video Overview | NotebookLM |
| terminal에서 local repo/docs 작업 | Gemini CLI, Codex, Claude Code |
| 조직 데이터 권한과 audit | Vertex AI/custom RAG |
| 도구 연결 표준화 | MCP |
| web-first source discovery | Deep Research, Perplexity, Gemini/ChatGPT research tools |

## 주의사항

| 위험 | 대응 |
|------|------|
| Hallucination | citation audit, source-only prompt |
| 오래된 limits | 공식 Help 문서 재확인 |
| CLI 혼동 | NotebookLM과 Gemini CLI를 명확히 분리 |
| 민감 정보 업로드 | Workspace policy와 sharing setting 확인 |
| Audio/Video 과장 | 원문과 citation으로 human review |
| 자동화 요구 | custom RAG/MCP/CLI agent로 별도 설계 |

---

## 관련 노트

- [[study/tech/ai/agent-orchestration/cli-agents]] - Gemini CLI와 다른 CLI agents 비교
- [[study/tech/ai/model-context-protocol-mcp]] - custom workflow integration
- [[study/tech/ai/litellm]] - model gateway와 custom RAG 운영
