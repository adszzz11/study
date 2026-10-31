---
date: 2026-06-20
tags:
  - tech
  - ai
  - notebooklm
  - projects
type: tech-tool-study
parent: "[[README]]"
---

# NotebookLM - 실전 프로젝트

> [[README|목차로 돌아가기]]

---

## 1. 프로젝트 아이디어

| 프로젝트 | 난이도 | 학습 포인트 |
|----------|--------|------------|
| 기술 리서치 dossier 생성 | ⭐ | docs/blog/changelog source 수집, architecture/tradeoff/risk 추출 |
| 사내 onboarding notebook | ⭐⭐ | policy/runbook/architecture docs 기반 Q&A와 quiz 생성 |
| 세일즈/CS knowledge base | ⭐⭐ | FAQ/release notes/product docs 기반 답변 script |
| 강의/학습 도우미 | ⭐ | PDF/slide/video transcript 기반 flashcards, quizzes, Audio Overview |
| CLI 대체 프로젝트 | ⭐⭐⭐ | Gemini CLI + local extraction + custom RAG로 terminal research workflow 구축 |

## 2. 프로젝트 1 - 기술 리서치 dossier

### 목표

새 기술을 도입하기 전 공식 문서, changelog, blog, issue, 논문을 sources로 넣고 실무 판단에 필요한 dossier를 만든다.

| 산출물 | 질문 |
|--------|------|
| Architecture summary | "이 기술의 core architecture를 source citation과 함께 설명해줘." |
| Tradeoff table | "장점, 한계, 운영 리스크를 표로 정리해줘." |
| Migration risk | "현재 stack에서 migration blocker가 될 수 있는 항목을 뽑아줘." |
| Decision memo | "도입/보류/추가 검토 결론을 근거별로 나눠줘." |

```text
검증 prompt:
"이 dossier에서 공식 문서에 근거한 주장과 blog/논문/해석에 근거한 주장을 분리해줘."
```

## 3. 프로젝트 2 - 사내 onboarding notebook

### 목표

신규 구성원이 사내 policy, runbook, architecture docs를 빠르게 이해하도록 notebook을 만든다.

| Source | Output |
|--------|--------|
| Engineering handbook | briefing doc, FAQ |
| Architecture docs | mind map, glossary |
| Runbook | incident response checklist |
| Security policy | quiz, do/don't table |

### 운영 체크리스트

- [ ] Workspace 계정 data policy 확인
- [ ] source 문서 공유 권한 확인
- [ ] outdated runbook 제거 또는 deprecated 표시
- [ ] onboarding quiz의 정답을 human review
- [ ] notebook owner와 update cadence 지정

## 4. 프로젝트 3 - 세일즈/CS knowledge base

### 목표

제품 문서, FAQ, release notes, pricing notes를 source로 넣고 고객 질문 대응 script를 만든다.

| 사용 사례 | NotebookLM prompt |
|-----------|-------------------|
| 고객 질문 답변 | "source에 근거해 고객에게 보낼 답변 초안을 작성해줘." |
| release summary | "이번 release note에서 고객 영향이 큰 변경만 뽑아줘." |
| objection handling | "보안/가격/마이그레이션 우려에 대한 답변을 source citation과 함께 작성해줘." |
| FAQ gap | "sources로 답할 수 없는 고객 질문 유형을 목록화해줘." |

## 5. 프로젝트 4 - 강의/학습 도우미

### 목표

교재 PDF, 강의자료, public lecture transcript를 source로 넣고 학습 artifact를 만든다.

| Artifact | 활용 |
|----------|------|
| Flashcards | 용어/정의 암기 |
| Quizzes | 이해도 점검 |
| Audio Overview | 이동 중 복습 |
| Mind Map | 단원 구조 파악 |
| Study Guide | 시험 전 요약 |

```text
학습 prompt:
"이 단원의 개념을 prerequisite, core concept, common misconception, practice question으로 나눠줘."
```

## 6. 프로젝트 5 - CLI 대체 workflow

### 목표

NotebookLM 전용 공식 CLI/API가 없는 상황에서, Gemini CLI와 custom RAG로 terminal research workflow를 만든다.

```text
docs/
  -> extract text
  -> build index
  -> ask via CLI
  -> generate markdown report
  -> store citations as file paths + headings
```

| Component | 선택 |
|-----------|------|
| CLI | Gemini CLI 또는 Codex |
| Parser | `pdftotext`, `markitdown`, `pandoc`, custom script |
| Index | SQLite FTS, ripgrep, vector DB |
| RAG | LangChain, LlamaIndex, custom |
| Integration | MCP server로 search/read/report tool 노출 |

```bash
# 아주 단순한 시작점: 파일 기반 요약
gemini -p "Read the markdown files in ./sources and create a Korean research memo with file path citations."
```

## 7. Best Practices

| 영역 | 원칙 |
|------|------|
| Source curation | 적은 수의 고품질 source로 시작하고 중복 source를 제거 |
| Citation audit | 숫자, 정책, pricing, CLI/API 여부는 citation 필수 |
| Output review | Audio/Video/Quiz는 human review 후 공유 |
| Privacy | 개인 계정과 Workspace 계정의 data handling 차이 확인 |
| Automation | 반복 pipeline은 NotebookLM보다 Gemini CLI/custom RAG/MCP가 적합 |
| Maintenance | source freshness와 owner를 notebook마다 기록 |

---

## 관련 노트

- [[study/tech/ai/model-context-protocol-mcp]] - CLI 대체 workflow를 MCP server로 감싸는 프로젝트
- [[study/tech/ai/agent-orchestration/cli-agents]] - Gemini CLI 등 terminal agent 선택
- [[study/tech/ai/litellm]] - custom RAG model gateway 운영
