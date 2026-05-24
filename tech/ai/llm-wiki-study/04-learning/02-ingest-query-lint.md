# 4-2. 3대 연산 — Ingest, Query, Lint

## 📥 Ingest 깊이

> "A single source might touch 10-15 wiki pages." — Karpathy

### 좋은 ingest 흐름

```
/wiki ingest raw/some-article.md
   │
   ▼
LLM이:
1. 원본 읽고 핵심 5-7 takeaway 추출
2. 사용자에게 "이 takeaway 맞나? 어떤 측면 강조?" 대화
3. 새 페이지 / 기존 페이지 결정:
     ├─ 새 entity? → entities/X.md 생성
     ├─ 새 concept? → concepts/Y.md 생성
     └─ 기존 페이지 갱신? → 변경 diff 보여줌
4. 영향받는 페이지 10-15개 동시 패치
5. 모순 발견 시 flag (자동 삭제 ✗)
6. index.md 갱신
7. log.md append
```

### Ingest 결과물 예시

`study/wiki/concepts/compounding-knowledge.md` (신규):
```markdown
---
tags: [llm-wiki, knowledge-management, karpathy]
date: 2026-05-23
source_count: 1
maintained_by: llm-wiki
---

# Compounding Knowledge

매 ingest마다 wiki 전체가 더 정합적·풍부해지는 [[llm-wiki-pattern]]의 핵심 속성.

## 정의
> 새 문서가 들어올 때 단순 추가가 아니라 wiki 전체에 통합되어,
> 이전 페이지들의 정확도·연결성이 함께 증가하는 현상.

## RAG와의 차이
[[rag-vs-llm-wiki]] 참조.

## 사례
- Karpathy 본인 wiki: 100 페이지, 400,000 단어, 모두 cross-ref
- 본 vault: ingest 1회 = study/wiki/ 10-15개 페이지 갱신

## 관련
- [[llm-wiki-pattern]]
- [[karpathy]]
- [[obsidian-skills]]

## 출처
- raw/karpathy-llm-wiki-gist.md
```

### Ingest 비용 예시

| 자료 | 영향 페이지 | LLM 토큰 in/out | 비용 (Opus) |
|------|------------|----------------|------------|
| 짧은 블로그 글 | 3-5 | 5K / 3K | $0.30 |
| 논문 (20p) | 8-12 | 30K / 8K | $1.10 |
| 책 한 챕터 | 15-20 | 60K / 15K | $2.20 |

→ ingest는 비싸지만 **1회만**. 이후 query는 wiki만 보면 됨.

### 안티패턴

| 안 함 | 이유 |
|-------|------|
| 한 번에 100 페이지 vault 통째 ingest | 비용 폭주 + 모순 인식 능력 떨어짐 |
| 같은 자료 ingest 반복 | log.md에 dedupe 체크. 갱신은 `/wiki ingest --update` |
| 너무 큰 페이지 (5000+ 단어) | 500단어 요약 + 디테일 별도 페이지 |

## 🔍 Query

### 기본
```
/wiki query "LLM Wiki와 RAG의 가장 중요한 차이 3가지"
```

흐름:
1. `wiki/index.md` 읽고 관련 페이지 후보 추출
2. 후보 페이지 본문 읽음 (보통 3-5개)
3. 답변 합성 + 출처 페이지 인용
4. (옵션) 좋은 답변은 다시 wiki 페이지로 저장

### 답변 형식 자유

> "Answers can take different forms depending on the question — a markdown page, a comparison table, a slide deck (Marp), a chart (matplotlib), a canvas." — Karpathy

예시 요청:
- `/wiki query "..." --format table`
- `/wiki query "..." --format marp`
- `/wiki query "..." --format canvas`

### 좋은 query 패턴

| 안 좋음 | 좋음 |
|--------|------|
| "LangGraph 뭐야?" | "본 vault에서 LangGraph가 다른 프레임워크와 어떻게 다르게 설명되는지 비교" |
| "AI 에이전트?" | "[[autonomous-agent]] 페이지와 [[multi-agent-orchestration]] 페이지의 모순 지점" |

→ wiki는 **연결을 묻는 질문**에 강함.

## 🧹 Lint

### 점검 항목
```bash
/wiki lint
```

자동 점검:
- **Contradiction**: 두 페이지가 같은 사실을 다르게 말함
- **Stale**: 새 자료가 옛 주장을 뒤집었는데 옛 페이지 안 갱신됨
- **Orphan**: 들어오는 wikilink 0개 페이지
- **Missing concept**: 5번 이상 언급됐는데 자체 페이지 없음
- **Missing cross-ref**: A 페이지가 B 개념 언급했는데 [[B]] 링크 없음
- **Data gap**: "TODO", "확인 필요" 같은 미해결 표시

### Lint 결과 예시
```
🔴 Contradictions (2):
  - concepts/multi-agent-pattern.md vs comparisons/crewai-vs-langgraph.md
    "CrewAI는 체크포인트 없음" vs "Flows에서 부분 체크포인트"
    제안: comparisons 페이지가 더 신선. multi-agent-pattern.md 갱신 필요.

🟡 Orphans (4):
  - entities/dotta.md (Paperclip 창업자) — 어디서도 링크 안 됨
    제안: concepts/paperclip.md에 [[dotta]] 추가.

🟡 Missing concept pages (3):
  - "lethal trifecta" — 7번 언급. 자체 페이지 없음.
  - "MCP server" — 12번 언급. 자체 페이지 없음.
  - "Agent Skills" — 5번 언급. 자체 페이지 없음.

🔵 Suggested cross-refs (12):
  - concepts/llm-wiki.md → [[compounding-knowledge]] 추가 권장
  - ...
```

### Lint 주기
- 새 ingest 5-10회마다
- 또는 주 1회 cron으로 자동

```bash
# crontab
0 9 * * 1   cd ~/vault && /wiki lint >> ~/vault/study/wiki/lint-reports/$(date +\%Y\%m\%d).md
```

## 📊 운영 KPI

| 지표 | 목표 |
|------|------|
| Orphan 페이지 비율 | < 5% |
| Contradiction 미해결 | 0 |
| 페이지당 cross-ref | 평균 3+ |
| Stale 페이지 | 0 |
| 월 ingest 수 | 본인 페이스 (보통 10-50) |

## 🔗 다음

→ Obsidian Skills 통합 → [03-obsidian-skills.md](03-obsidian-skills.md)
