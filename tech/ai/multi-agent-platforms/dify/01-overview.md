# Part 1. Dify 개요

## 🧱 5대 빌딩블록

| 블록 | 설명 |
|------|------|
| **Studio (Workflow)** | 비주얼 캔버스 — 노드를 드래그해서 LLM 흐름 정의 |
| **RAG Pipeline** | 문서 → 청킹 → 임베딩 → 검색 → 재정렬 통합 |
| **Agent** | LLM function calling 또는 ReAct 기반, 50+ 내장 도구 |
| **Prompt IDE** | 다중 모델 비교 + 프롬프트 버전 관리 |
| **LLMOps** | 사용 로그 + 평가 + 비용 추적 |

## 🎨 Workflow 캔버스 — 노드 종류

```
[Start] → [LLM] → [Knowledge Retrieval] → [If/Else] → [Code Execution] → [End]
                                            │
                                            └──→ [HTTP Request] → [Variable Aggregator]
```

대표 노드:
- LLM (모델 선택, 시스템 프롬프트, 변수 주입)
- Knowledge Retrieval (RAG)
- Code Execution (Python/Node 인라인)
- HTTP Request (외부 API)
- Tool (50+ 내장: Google Search, DALL·E, Slack 등)
- If/Else, Iteration, Variable Aggregator
- Custom Plugin

## 📚 RAG 파이프라인

```
PDF/DOCX/MD/HTML/Notion/Confluence ─► 자동 청킹
   ─► OpenAI / Cohere / BGE 임베딩
   ─► PgVector / Milvus / Qdrant / Weaviate 저장
   ─► 검색 + Cohere Rerank
   ─► LLM에 컨텍스트 전달
```

각 단계가 UI에서 설정 + 평가 도구 제공.

## 🤖 Agent 모드

두 가지:
1. **Function Calling** — 모델이 도구 호출 결정 (GPT-4, Claude 등)
2. **ReAct** — 명시적 reasoning + action 패턴 (모든 모델 가능)

50+ 내장 도구 + 자체 도구 작성 (Python plugin).

## 🌐 사용 형태

- **셀프호스팅** (Community Edition): Apache 2.0 기반 + 추가 조건. 무제한.
- **Dify Cloud**: 매니지드. 무료 sandbox 200 GPT-4 호출/월.
- **Enterprise**: 커스텀 라이선스.

## ⚖️ 장단점

### ✅ 장점
- **노코드 + 코드 둘 다** — 비기술자 PoC, 개발자 API 통합
- **RAG 풀스택** — 별도 LlamaIndex/Chroma 없이 끝
- **셀프호스팅 무제한** — 데이터 주권
- **142k★** — 가장 큰 LLM 앱 플랫폼
- **다국어** — 한국어 UI 지원
- **50+ 도구 + 플러그인**

### ❌ 단점
- **셀프호스팅 운영 부담** — Postgres·Redis·Weaviate·Worker 등 다수 컨테이너
- **복잡한 멀티에이전트 한계** — Supervisor·핸드오프 패턴 일부만
- **커스텀 노드 작성 곡선** — Plugin 시스템
- **라이선스 조건** — Apache 2.0 + 추가 (상용 서비스 시 확인 필요)
- **메모리·체크포인트 LangGraph만큼 강하지 않음**

## 🎯 적합도

| 상황 | 적합 |
|------|------|
| LLM 앱 빠른 프로토타이핑 | ⭐⭐⭐⭐⭐ |
| RAG 챗봇 | ⭐⭐⭐⭐⭐ |
| 비기술 PM·기획자와 협업 | ⭐⭐⭐⭐⭐ |
| 셀프호스팅 + 데이터 주권 | ⭐⭐⭐⭐⭐ |
| 매우 복잡한 멀티 에이전트 | ⭐⭐⭐ (LangGraph 추천) |
| Mac mini에 가볍게 | ⭐⭐⭐ (컨테이너 5+개) |

## 🔗 다음 → [02-ecosystem.md](02-ecosystem.md)
