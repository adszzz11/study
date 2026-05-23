# Part 2. Dify 생태계

## 🆚 vs 같은 카테고리 (Visual + LLM)

| 항목 | Dify | Flowise | LangFlow | n8n + AI |
|------|------|---------|----------|----------|
| 출신 | langgenius | FlowiseAI | LangChain Inc | n8n |
| 무게 | 중 | 가벼움 | 가벼움 | 무거움 (general) |
| RAG | ⭐ 풀스택 | 기본 | 기본 | (외부 필요) |
| 노코드 | ⭐ | ✅ | ✅ | ⭐ |
| ★ | 142k | 35k | 50k | 100k+ |
| 셀프호스팅 | ⭐ | ⭐ | ⭐ | ⭐ |
| 한국어 UI | ⭐ | 부분 | 부분 | ⭐ |
| 라이선스 | Apache+ | Apache 2.0 | MIT | Sustainable Use |

## 🆚 vs 본 카테고리 (코드 라이브러리)

| 항목 | Dify | CrewAI | LangGraph |
|------|------|--------|-----------|
| 시작 형태 | 캔버스 | Python | Python |
| 비기술자 사용 | ⭐ 가능 | ✗ | ✗ |
| 복잡한 상태 | 중 | 약 | ⭐ 강 |
| 멀티 에이전트 | 부분 | ⭐ | ⭐ |
| 셀프호스팅 운영 | Docker stack | 단일 프로세스 | 단일 프로세스 |

**결정**: 시각 + RAG가 중심 → Dify. 코드 + 복잡 상태 → LangGraph. 빠른 협업 → CrewAI.

## 🆚 vs Paperclip (운영 OS와)

- **Paperclip**: 에이전트 운영·예산·거버넌스 OS
- **Dify**: 에이전트·워크플로우 빌더 + 실행 플랫폼
- 조합: Dify에서 워크플로우 만들고 Paperclip 직원으로 등록 (HTTP webhook 어댑터)

## 🌐 함께 쓰는 스택

| 역할 | 추천 |
|------|------|
| 벡터DB | Weaviate(기본), Milvus, Qdrant, PgVector |
| Embedding | OpenAI, Cohere, BGE, Voyage |
| Rerank | Cohere Rerank |
| LLM | 거의 모두 (OpenAI/Anthropic/Gemini/Llama/...) |
| 모니터링 | 내장 LLMOps + Langfuse |
| 외부 노출 | Tailscale, Cloudflare Tunnel |

## 🔥 동향

- **142k★** → 가장 큰 LLM 앱 플랫폼
- **DSL 노출** — 워크플로우를 YAML로 export/import (버전 관리 가능)
- **Plugin Marketplace** — 커뮤니티가 만든 노드·도구
- **Dify on Mobile** — 모바일 앱 빌더 추가
- **MCP 지원** 추가 — Claude Code MCP 서버 그대로 통합

## 🔗 다음 → [03-references.md](03-references.md)
