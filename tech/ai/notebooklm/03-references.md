---
date: 2026-06-20
tags:
  - tech
  - ai
  - notebooklm
  - references
type: tech-tool-study
parent: "[[README]]"
---

# NotebookLM - 참고자료

> [[02-ecosystem|이전: 생태계]] | [[README|목차로 돌아가기]] | [[04-learning/01-getting-started|다음: 시작하기]]

---

## 공식 NotebookLM 자료

| 자료 | URL | 읽을 포인트 |
|------|-----|-------------|
| Google NotebookLM | https://notebooklm.google/ | 제품 진입점, web app |
| Learn about NotebookLM | https://support.google.com/notebooklm/answer/16164461 | AI-powered research assistant, citations, supported languages, data handling |
| Add or discover new sources | https://support.google.com/notebooklm/answer/16215270 | source types, 50 sources/free, 500,000 words, 200MB, Drive/web/YouTube 제한 |
| Audio Overview | https://support.google.com/notebooklm/answer/16212820 | AI hosts, format, 오류 가능성, 생성/공유 |
| Video Overview | https://support.google.com/notebooklm/answer/16454555 | explainer/brief/cinematic, visual style, steering prompt |
| Upgrade/limits | https://support.google.com/notebooklm/answer/16213268 | plan별 limits, premium features |
| FAQ | https://support.google.com/notebooklm/answer/16269187 | privacy, availability, sharing, 기능 제한 |
| Google Workspace NotebookLM | https://workspace.google.com/products/notebooklm/ | enterprise/workspace 도입, data protection |

## Gemini CLI 자료

| 자료 | URL | 읽을 포인트 |
|------|-----|-------------|
| Google Blog - Gemini CLI | https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemini-cli-open-source-ai-agent/ | terminal-first AI agent, open-source, Google Search grounding, MCP |
| Gemini CLI GitHub | https://github.com/google-gemini/gemini-cli | install, command, issues, license, releases |

```bash
# 공식 Gemini CLI package 예시
npx @google/gemini-cli
npm install -g @google/gemini-cli
gemini -p "Explain this repository structure."
```

## 연구/분석 자료

| 자료 | URL | 읽을 포인트 |
|------|-----|-------------|
| arXiv 2025 - NotebookLM as RAG tutor | https://arxiv.org/abs/2504.09720 | NotebookLM을 RAG tutor로 활용하는 학습 효과/한계 |
| arXiv 2025 - Audio Overviews media analysis | https://arxiv.org/abs/2511.08654 | Audio Overview의 media format, voice/podcast-like UX 분석 |

## 확인해야 할 공식 포인트

| 항목 | 확인 위치 | 메모 |
|------|-----------|------|
| Source limits | Add or discover new sources, Upgrade/limits | free/premium plan에 따라 바뀔 수 있음 |
| Supported source types | Add or discover new sources | Docs/Slides/Sheets, web URL, YouTube transcript, audio, images 포함 |
| Citation behavior | Learn about NotebookLM, chat docs | source 기반 답변과 inline citations |
| Data handling | Learn about NotebookLM, FAQ, Workspace | Workspace 계정과 개인 계정의 policy 차이 |
| CLI/API 여부 | 공식 NotebookLM 문서와 Google product pages | 2026-06 기준 전용 공식 CLI/API 확인되지 않음 |
| Gemini CLI | Google Blog, GitHub | NotebookLM이 아닌 별도 terminal agent |

## 학습 순서

1. **Learn about NotebookLM**로 제품 정의와 data handling을 먼저 읽는다.
2. **Add or discover new sources**에서 source type과 limits를 확인한다.
3. **Audio/Video Overview** 문서로 Studio artifacts의 생성 방식과 오류 가능성을 확인한다.
4. **Upgrade/FAQ/Workspace** 문서로 plan, privacy, enterprise policy를 정리한다.
5. **Gemini CLI Blog/GitHub**를 읽고 NotebookLM CLI 혼동을 해소한다.
6. 논문은 마지막에 읽고 교육/미디어 관점의 장단점을 보강한다.

---

## 관련 노트

- [[study/tech/ai/agent-orchestration/cli-agents]] - Gemini CLI가 속한 CLI agent 생태계
- [[study/tech/ai/model-context-protocol-mcp]] - Gemini CLI와 custom workflow에서 MCP를 쓰는 맥락
- [[study/tech/ai/litellm]] - custom RAG/API 대안 설계 시 참고
