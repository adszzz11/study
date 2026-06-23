---
date: 2026-06-23
tags:
  - tech
  - ai
  - notebooklm
  - cheatsheet
type: tech-tool-study
parent: "[[README]]"
---

# NotebookLM 연동 가능성 - 치트시트

## 한 줄 결론

2026-06 기준 NotebookLM은 공식 공개 API로 backend에서 직접 호출하기보다, **Drive source sync를 이용한 semi-automation** 또는 **Gemini/OpenAI/Agent Search 기반 API RAG 대체**로 설계하는 것이 현실적이다.

## 가능한 것

| 작업 | 가능성 | 메모 |
|------|------|------|
| Markdown/PDF/CSV 생성 후 NotebookLM source로 추가 | 높음 | 가장 단순한 느슨한 연동 |
| Google Drive 파일을 source로 import 후 자동 갱신 | 중간 | 몇 분 단위 sync |
| Web URL을 source로 추가 | 중간 | HTML text 중심, embedded content 제한 |
| NotebookLM UI에서 chat, summary, Audio/Video Overview 사용 | 높음 | NotebookLM의 핵심 가치 |
| 앱 backend에서 자동 Q&A API 구현 | 낮음 | NotebookLM 대신 programmable RAG 권장 |

## 어려운 것

| 작업 | 이유 | 대안 |
|------|------|------|
| notebook 자동 생성 | 공식 공개 API 미확인 | 수동 생성 또는 다른 RAG API |
| source 자동 업로드 | 공식 공개 API 미확인 | Drive 파일 생성 후 수동 import |
| chat 자동 실행 | 공식 공개 API 미확인 | Gemini API/OpenAI File Search |
| 결과 자동 회수 | UI 중심 도구 | API RAG로 구현 |
| browser automation 운영 | 약관/안정성/UI 변경 리스크 | 공식 API가 있는 대체 서비스 |

## source format 권장

```text
1. Google Docs: Drive sync 중심 운영
2. Markdown: 구조화된 기술 문서와 노트
3. PDF: 고정 보고서와 배포본
4. CSV: 표 데이터, data dictionary와 함께 사용
5. Web URL: 공개 text report
```

## 선택 기준

| 상황 | 선택 |
|------|------|
| 사용자가 NotebookLM에서 직접 탐색한다 | NotebookLM |
| 매일 문서가 갱신된다 | NotebookLM + Google Drive |
| 앱에서 자동 답변이 필요하다 | Gemini API / OpenAI File Search |
| enterprise access control이 중요하다 | Google Cloud Agent Search |
| Audio/Video Overview가 핵심이다 | NotebookLM 유지 |

## MVP 아키텍처

```text
이 시스템
  -> research-report.md
  -> summary.pdf
  -> Google Drive folder
  -> NotebookLM Drive source
  -> 사용자 NotebookLM 탐색
```

## 보안 체크

- 개인 계정인지 Workspace/Education/Enterprise인지 확인한다.
- 민감 문서는 feedback, human review, training 정책을 확인한 뒤 source로 추가한다.
- Drive sharing 범위와 NotebookLM notebook sharing 범위를 분리해서 점검한다.
- source limit, file size, sync latency를 실제 계정에서 측정한다.

## 빠른 질문 세트

```text
Q1. NotebookLM 공식 API로 notebook 생성/질문 실행 가능한가?
A1. 2026-06 기준 공식 공개 API는 확인되지 않는다.

Q2. 그럼 자동 연동은 전혀 안 되나?
A2. Drive 파일 생성/갱신 + NotebookLM Drive source sync는 가능하다. 최초 연결은 수동 전제다.

Q3. 완전 자동 질의응답이 필요하면?
A3. NotebookLM 대신 Gemini API, Google Cloud Agent Search, OpenAI File Search를 검토한다.

Q4. Web URL source는 웹페이지 전체를 읽나?
A4. HTML text 중심이다. 이미지, embedded videos, nested pages, paywalled pages는 제한된다.
```

## 관련 노트

- [[study/tech/ai/ai-ecosystem]]
- [[study/tech/ai/model-context-protocol-mcp]]
- [[study/tech/ai/litellm]]
