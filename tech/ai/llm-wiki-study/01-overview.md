# Part 1. LLM Wiki 개요

## 📅 출범 타임라인

```
2026.4.2  Karpathy gist 공개 (442a6bf555914893e9891c11519de94f)
2026.4.7  5일 만에 16M 트윗 조회, 5,000★, 15+ 구현체 출현
2026.4.12 Aaron Fulkerson "in production" 분석 글
2026.3-4  Obsidian CEO Steph Ango가 kepano/obsidian-skills 공식 발표
2026.5    13.9k★ 도달, 사실상 표준화
```

→ **단 한 달 만에 LLM 지식 관리의 새 표준이 됨**.

## 🧩 핵심 통찰: "Compounding Knowledge"

```
RAG 방식:
  새 문서 → 벡터DB 추가 → 질문 시 검색 → LLM이 답변
   각 문서는 독립. 시간이 지나도 "지식"이 더 똑똑해지지 않음.

LLM Wiki:
  새 문서 → LLM이 wiki/ 갱신 → 10-15개 페이지에 영향 → cross-ref 추가 → 모순 발견
   매 ingest마다 wiki 전체가 더 정합적·풍부해짐. "복리(compounding)".
```

Karpathy 본인의 wiki: **약 100 페이지, 400,000 단어** (소설 4-5권 분량).

## 🏛️ 3-Layer 아키텍처

```
┌──────────────────────────────────────────────────┐
│  Layer 1 — raw/ (불변, human-write)              │
│  PDF, .md 메모, 트랜스크립트, 북마크, 음성 노트   │
│  LLM은 read-only                                │
├──────────────────────────────────────────────────┤
│  Layer 2 — wiki/ (LLM이 작성·갱신)              │
│  • concepts/ — 개념 페이지                       │
│  • entities/ — 사람·장소·프로젝트                │
│  • comparisons/ — 비교 분석                      │
│  • index.md — 카탈로그                          │
│  • log.md — 작업 이력                           │
├──────────────────────────────────────────────────┤
│  Layer 3 — CLAUDE.md (스키마/운영 매뉴얼)        │
│  컨벤션, 명명 규칙, 워크플로우 지시              │
│  "raw/는 절대 수정 ✗", "wiki link는 [[slug]]"   │
└──────────────────────────────────────────────────┘
```

### Karpathy 운영 모델

> "I have the LLM agent open on one side and Obsidian open on the other.
> The LLM makes edits based on our conversation,
> and I browse the results in real time—following links, checking the graph view, reading the updated pages."

**듀얼 뷰**: LLM 에이전트(작업) + Obsidian(검토).

## ⚡ 3대 연산

### 1. Ingest (수집)
> "LLM reads the source, discusses key takeaways with you, writes a summary page, updates the index, updates relevant entity and concept pages across the wiki, and appends an entry to the log. **A single source might touch 10-15 wiki pages.**"

→ 핵심: 한 문서 ingest가 **10-15개 페이지를 한꺼번에 갱신**. 이게 compounding의 실체.

### 2. Query (질의)
> "LLM searches for relevant pages, reads them, and synthesizes an answer with citations."

답변 형식 자유: 마크다운 / 비교 표 / Marp 슬라이드 / matplotlib 차트 / Canvas.

### 3. Lint (점검)
> "Look for: contradictions between pages, stale claims that newer sources have superseded, orphan pages with no inbound links, important concepts mentioned but lacking their own page, missing cross-references, data gaps."

```
지식 부채 점검:
□ 모순된 주장
□ 새 자료에 의해 폐기된 옛 주장
□ 들어오는 링크 없는 고아 페이지
□ 언급만 되고 페이지 없는 개념
□ 누락된 cross-reference
□ 데이터 갭
```

## ⚖️ 장단점

### ✅ 장점
- **Compounding**: 매 ingest마다 wiki가 더 풍부해짐
- **인용 정확**: LLM이 wiki 페이지 → 출처 raw/ 추적 가능
- **RAG 인프라 불필요**: 벡터DB·임베딩 모델·재정렬 없음
- **사람도 그대로 읽음**: 마크다운이라 Obsidian/IDE/Git에서 그대로
- **버전 관리 가능**: Git으로 wiki의 진화 추적
- **Obsidian + 본 vault 호환**: `[[wikilink]]` 그대로 사용

### ❌ 단점
- **초기 학습 곡선**: RAG보다 운영 패턴 익숙해지는 데 시간
- **LLM 의존 + 비용**: ingest마다 큰 컨텍스트 LLM 호출
- **agent 행동 통제 필요**: raw/ 침범 방지, 명명 일관성
- **대규모 검색 비효율**: 1만+ 페이지 vault엔 vector search 보완 필요
- **모델 품질 의존**: 작은 모델은 cross-ref 누락·모순 못 발견

## 🎯 누가 쓰면 좋은가

| 상황 | 적합 |
|------|------|
| 개인 second brain (학습·연구) | ⭐⭐⭐⭐⭐ |
| 팀 위키 (Notion 대체) | ⭐⭐⭐⭐ |
| 도메인 전문 지식 축적 | ⭐⭐⭐⭐⭐ |
| 코드베이스 문서 자동화 | ⭐⭐⭐⭐ |
| 1만+ 페이지 검색 우선 | ⭐⭐ (RAG 보완 필요) |
| 즉시 응답이 핵심 | ⭐⭐⭐ (ingest는 비동기) |

## 🆚 RAG와의 1:1 비교

| 축 | RAG | LLM Wiki |
|----|-----|----------|
| 저장소 | 벡터DB | 마크다운 파일 |
| 인덱스 갱신 | 임베딩 재계산 | LLM이 wiki 갱신 |
| 답변 시 | 매번 검색 | 미리 통합된 페이지 |
| 모순 처리 | ✗ | flag로 표시 |
| 사람 가독성 | ✗ (벡터) | ⭐ (마크다운) |
| 비용 곡선 | 쿼리당 ↑ | ingest 시 ↑, 쿼리 시 ↓ |
| 인프라 | 필요 | 불필요 |
| 잘 맞는 규모 | 100k+ docs | 100-10k pages |

## 🔗 다음

→ Obsidian의 공식 대응 — [02-ecosystem.md](02-ecosystem.md)
