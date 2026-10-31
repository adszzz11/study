---
date: 2026-06-23
tags:
  - tech
  - ai
  - notebooklm
  - getting-started
  - integration
type: tech-tool-study
parent: "[[../README]]"
---

# NotebookLM 연동 가능성 - 시작하기

> [[../03-references|이전: 참고자료]] | [[../README|목차로 돌아가기]] | [[02-deep-dive|다음: 심화]]

---

## 목표

공식 공개 NotebookLM API가 없는 상황에서, 이 시스템의 산출물을 NotebookLM에 연결하는 현실적인 최소 경로를 검증한다.

검증 대상:

- Google Drive source sync
- NotebookLM이 잘 읽는 export format
- Web URL source의 한계
- API 자동화가 필요한지 여부

## 실습 1: Drive sync 검증

### 절차

1. Google Docs에 테스트 문서를 만든다.
2. NotebookLM에서 새 notebook을 만든다.
3. `Add source`에서 Google Drive 문서를 import한다.
4. NotebookLM에서 문서 요약과 질문 답변을 확인한다.
5. Google Docs 원본에 새 section을 추가한다.
6. 몇 분 뒤 NotebookLM source가 갱신되는지 확인한다.

### 테스트 문서 예시

```markdown
# Research Report

## Executive Summary

이 문서는 이 시스템이 생성한 샘플 보고서다.

## Key Findings

- NotebookLM 직접 API는 확인되지 않는다.
- Drive sync는 semi-automation 경로로 사용할 수 있다.
- 완전 자동 질의/응답은 Gemini API 또는 OpenAI File Search가 더 적합하다.

## Open Questions

- sync latency는 실제 계정과 파일 크기에 따라 어느 정도인가?
- citations가 section heading을 잘 따라가는가?
```

### 확인 항목

| 항목 | 기대 결과 | 기록 |
|------|------|------|
| 최초 import | 문서 내용이 source로 인식됨 | import 성공/실패 |
| 수정 반영 | 몇 분 뒤 변경 내용 반영 | latency 측정 |
| citation | 답변에 source 근거 표시 | 정확도 평가 |
| 큰 문서 | word/file size limit 안에서 처리 | file size 기록 |

## 실습 2: 출력 포맷 정하기

이 시스템이 생성할 산출물 format을 정한다.

| 포맷 | NotebookLM 적합도 | 사용처 | 주의 |
|---|---:|---|---|
| Markdown `.md` | 높음 | 구조화된 텍스트, 기술 노트 | heading과 table을 명확히 작성 |
| PDF | 높음 | 고정 레이아웃 보고서 | OCR/복잡한 layout 품질 확인 |
| CSV | 중간 | 표 데이터 | 컬럼명과 설명 source를 함께 제공 |
| Google Docs | 높음 | Drive sync 중심 운영 | Docs API/Drive 권한 필요 |
| Web page URL | 중간 | publish된 report | text만 scrape된다고 가정 |

권장 기본값:

```text
Primary: Google Docs 또는 Markdown
Secondary: PDF summary
Data: CSV + data dictionary 문서
```

## 실습 3: Web URL source 실험

### 절차

1. 정적 HTML report를 생성한다.
2. 공개 또는 접근 가능한 URL로 publish한다.
3. NotebookLM에서 URL source로 추가한다.
4. text content만 반영되는지 확인한다.
5. 이미지, embedded video, nested page link가 누락되는지 확인한다.

### HTML report 체크리스트

- [ ] 핵심 내용은 이미지 안이 아니라 HTML text로 제공한다.
- [ ] 표는 가능한 실제 table/text로 작성한다.
- [ ] 중요한 근거 URL은 본문에 명시한다.
- [ ] nested page를 기대하지 않고 필요한 내용을 한 page에 모은다.

## 실습 4: API 대체 PoC 기준 정하기

NotebookLM UI가 아니라 시스템 내부 기능이 필요하면 다음 질문에 답한다.

| 질문 | 예/아니오 | 의미 |
|------|------|------|
| 앱에서 사용자가 질문하면 backend가 즉시 답해야 하는가? | 예면 API RAG 필요 | NotebookLM UI로는 부족 |
| 답변과 citations를 DB에 저장해야 하는가? | 예면 API RAG 필요 | 결과 회수/감사 필요 |
| 사용 권한을 문서 단위로 강제해야 하는가? | 예면 Agent Search 등 고려 | access control 필요 |
| Audio Overview가 핵심 기능인가? | 예면 NotebookLM 유지 | 대체 API로 재현 어려움 |

## 산출물

```text
notebooklm-integration-test/
├── source-format-decision.md
├── drive-sync-log.md
├── web-url-import-log.md
└── api-replacement-decision.md
```

## 관련 노트

- [[study/tech/ai/ai-ecosystem]] - 실습 결과를 도구 선택 기준에 반영
- [[study/tech/ai/litellm]] - API 대체 PoC에서 provider routing이 필요할 때 참고
