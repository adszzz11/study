---
date: 2026-06-23
tags:
  - tech
  - ai
  - notebooklm
  - references
type: tech-tool-study
parent: "[[README]]"
---

# NotebookLM 연동 가능성 - 참고자료

> [[02-ecosystem|이전: 생태계]] | [[README|목차로 돌아가기]] | [[04-learning/01-getting-started|다음: 시작하기]]

---

## 1. NotebookLM 공식 문서

| 문서 | URL | 확인할 내용 |
|---|---|---|
| NotebookLM Help - Learn about NotebookLM | https://support.google.com/notebooklm/answer/16164461 | source-grounded 답변, citations, notebook 개념 |
| NotebookLM Help - Add or discover new sources | https://support.google.com/notebooklm/answer/16215270 | 지원 source types, limits, Drive sync, Web URL import 제한 |
| NotebookLM Help - Notebooks in Gemini Apps | https://support.google.com/notebooklm/answer/17003757 | Gemini Apps navigation, rename/source/custom instructions sync |
| NotebookLM Help - Privacy and Terms of Use | https://support.google.com/notebooklm/answer/17004255 | 개인/Workspace/Education 계정의 데이터 처리 차이 |
| NotebookLM Help - Upgrade NotebookLM | https://support.google.com/notebooklm/answer/16213268 | plan별 limits와 기능 차이 |
| NotebookLM Help - Work/school account | https://support.google.com/notebooklm/answer/16337734 | Workspace core service, 관리자/조직 계정 조건 |
| Google Workspace NotebookLM product page | https://workspace.google.com/products/notebooklm/ | Workspace 제품 포지셔닝 |
| Google Cloud NotebookLM Enterprise | https://cloud.google.com/resources/notebooklm-enterprise | Enterprise privacy, IAM, VPC-SC, 관리 기능 |

## 2. API 대체 설계 문서

| 문서 | URL | NotebookLM 대체 포인트 |
|---|---|---|
| Gemini API document understanding | https://ai.google.dev/gemini-api/docs/document-processing | PDF/document processing, Files API, multimodal document understanding |
| Google Cloud Agent Search docs | https://docs.cloud.google.com/generative-ai-app-builder/docs | Discovery Engine data stores, generated answers, enterprise search |
| OpenAI File Search docs | https://developers.openai.com/api/docs/guides/tools-file-search | Responses API, vector stores, citations 기반 RAG |
| Claude Projects Help | https://support.claude.com/en/articles/9517075-what-are-projects | UI형 project knowledge workspace 비교 |

## 3. 검증해야 할 공식 포인트

### Source types와 limits

- PDF, websites, YouTube videos, audio files, Google Docs/Slides/Sheets, images, Word/docx, txt, md, CSV, PowerPoint/pptx, ePub, pasted text를 source로 사용할 수 있다.
- 각 source는 최대 `500,000 words` 또는 uploaded file `200MB` 범위를 기준으로 검토한다.
- Free plan은 notebook당 `50 sources` 수준의 제한을 고려한다.

### Drive sync

- Google Drive file을 source로 import하면 원본 변경이 몇 분 단위로 NotebookLM에 sync된다.
- 이 기능이 공식 문서상 “자동 연동”에 가장 가까운 경로다.
- 최초 notebook/source 연결은 별도의 공개 API가 아니라 NotebookLM UI 흐름을 전제로 설계한다.

### Web URL import

- HTML page의 text content 중심으로 scrape한다.
- images, embedded videos, nested pages, paywalled pages는 기대하지 않는다.
- PDF URL은 PDF source로 처리될 수 있다.

### Gemini Apps integration

- NotebookLM notebooks가 Gemini navigation에 보일 수 있다.
- rename, source, custom instructions 변경이 양방향 sync될 수 있다.
- NotebookLM은 sources에 grounded되지만 Gemini는 web search/tools가 섞일 수 있으므로 답변 근거 모델이 다를 수 있다.

### Privacy

- Workspace/Education 사용자는 uploads, queries, model responses가 human reviewer 검토나 AI model training에 쓰이지 않는다고 안내된다.
- 개인 계정은 feedback 제공 시 관련 content가 review/개선에 사용될 수 있으므로 업무 문서 사용 전 정책 확인이 필요하다.

## 4. 읽는 순서

1. NotebookLM Help - Learn about NotebookLM
2. NotebookLM Help - Add or discover new sources
3. NotebookLM Help - Privacy and Terms of Use
4. NotebookLM Help - Work/school account 또는 Google Cloud NotebookLM Enterprise
5. 자동화 요구가 있으면 Gemini API, Agent Search, OpenAI File Search 문서

## 관련 노트

- [[study/tech/ai/ai-ecosystem]] - 공식 문서를 바탕으로 도구를 분류할 때 참고
- [[study/tech/ai/model-context-protocol-mcp]] - API/도구 표준 연동이 필요한 경우 참고
