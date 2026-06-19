---
date: 2026-06-20
tags:
  - tech
  - ai
  - notebooklm
  - learning
type: tech-tool-study
parent: "[[../README]]"
---

# NotebookLM - 시작하기

> [[../README|목차로 돌아가기]] | [[02-deep-dive|다음: 심화]]

---

## 1. 목표

첫 notebook을 만들고, sources를 5-10개만 넣어 NotebookLM의 핵심 동작을 확인한다.

- source import type 차이 확인
- `all sources`와 selected sources 답변 비교
- citation이 붙은 주장과 citation이 부족한 주장 구분
- Studio output별 hallucination/누락 점검
- CLI가 필요한 경우 Gemini CLI와 역할 분리

## 2. 준비물

| Source | 추천 예시 | 확인할 것 |
|--------|-----------|-----------|
| PDF | 공식 whitepaper, 논문, manual | 페이지/섹션 citation 품질 |
| Web URL | docs page, blog, changelog | text import 범위, paywall/embedded content 제한 |
| Google Docs | 직접 작성한 요약 문서 | Drive sync 여부 |
| YouTube URL | public video with captions | transcript만 import되는지 |
| Markdown/TXT | local note 또는 spec | 구조화된 heading 활용 여부 |

```text
권장 시작 크기:
- sources: 5-10개
- topic: 하나의 좁은 질문
- output: chat answer + briefing doc + quiz 정도로 제한
```

## 3. 첫 notebook 만들기

1. NotebookLM에 접속해 새 notebook을 만든다.
2. 같은 주제의 sources를 5-10개 추가한다.
3. source title을 사람이 구분하기 쉽게 정리한다.
4. source별 auto-generated summary를 훑어 import가 제대로 되었는지 확인한다.
5. notebook의 첫 질문은 넓게, 두 번째 질문은 좁게 묻는다.

```text
첫 질문 예시:
"이 sources 전체에서 NotebookLM의 핵심 기능과 한계를 한국어로 요약해줘. 각 주장에는 citation을 붙여줘."

좁은 질문 예시:
"source limits와 supported source types만 표로 정리해줘. 숫자가 들어간 항목은 반드시 citation을 붙여줘."
```

## 4. All sources vs selected sources 비교

| 실험 | 방법 | 기대 관찰 |
|------|------|-----------|
| All sources | 모든 source를 선택하고 같은 질문 | 폭넓은 답변, citation 분산 |
| Selected sources | 공식 Help 문서만 선택 | 더 제한된 답변, 근거 품질 상승 가능 |
| Mixed sources | 공식 문서 + 블로그 + 논문 | 서로 다른 관점이 섞임 |
| Single source | 문서 하나만 선택 | citation 추적이 쉬움 |

### 검증 prompt

```text
"방금 답변에서 citation이 없는 주장만 표로 뽑아줘.
열은 claim, 왜 citation이 필요한지, 확인해야 할 source 로 구성해줘."
```

```text
"이 답변 중 sources에 직접 근거가 없는 추론을 분리해줘.
근거 있음 / 약한 추론 / source 밖 주장 으로 나눠줘."
```

## 5. Studio output 맛보기

| Output | 실습 질문 |
|--------|-----------|
| Audio Overview | 핵심 주장과 누락된 caveat가 무엇인지 비교 |
| Mind Map | source structure와 mind map hierarchy가 맞는지 확인 |
| Flashcards | 암기 카드가 source 용어를 정확히 쓰는지 확인 |
| Quiz | 정답/해설이 citation 가능한지 확인 |
| Briefing doc | 실무 공유용 summary로 바로 쓸 수 있는지 확인 |

```text
검토 기준:
- 숫자, 날짜, plan limit이 정확한가?
- 공식 문서와 블로그성 해석이 섞이지 않았는가?
- "좋다/강력하다" 같은 평가가 근거 없이 붙지 않았는가?
- Audio/Video가 재미를 위해 nuance를 잃지 않았는가?
```

## 6. CLI가 필요할 때의 분기

NotebookLM 안에서 notebook을 만들고 Studio output을 만드는 작업은 web/mobile UX 중심이다. 터미널 자동화가 목적이면 다음처럼 분리한다.

| 필요 | 선택 |
|------|------|
| local docs를 terminal에서 요약 | Gemini CLI |
| repo 파일을 읽고 수정 | Codex, Gemini CLI, Claude Code 등 CLI agent |
| 사내 문서를 API로 ingest/search | Vertex AI, LangChain, LlamaIndex, custom RAG |
| agent tool workflow 표준화 | MCP |

```bash
# NotebookLM 전용 CLI가 아니라 Gemini CLI 사용 예시
npx @google/gemini-cli

gemini -p "Summarize these markdown notes into a Korean study outline."
```

## 실습 체크리스트

- [ ] notebook 생성
- [ ] PDF, web URL, Google Docs, YouTube transcript, Markdown/TXT 중 3종 이상 source 추가
- [ ] all sources와 selected sources 답변 비교
- [ ] citation 없는 주장 점검 prompt 실행
- [ ] Audio Overview, Mind Map, Flashcards 또는 Quiz 중 2개 이상 생성
- [ ] NotebookLM CLI와 Gemini CLI 차이 정리

---

## 관련 노트

- [[study/tech/ai/agent-orchestration/cli-agents]] - CLI가 필요할 때 비교할 도구군
- [[study/tech/ai/model-context-protocol-mcp]] - NotebookLM-like terminal workflow를 tool/resource로 만드는 방법
- [[study/tech/ai/llm-wiki-study]] - markdown/wiki sources를 학습 자료로 재가공하는 패턴
