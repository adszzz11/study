# 4-3. RAG 파이프라인

## 📚 Knowledge Base 생성

1. **Studio → Knowledge → Create**
2. Source 선택:
   - File upload (PDF, DOCX, MD, TXT, HTML, ...)
   - Notion (OAuth 연동)
   - Confluence
   - Web crawler (URL)
3. **Chunking**:
   - Automatic: 기본
   - Custom: separator, max_tokens, overlap 설정
4. **Embedding Model**:
   - `text-embedding-3-small` (저비용)
   - `text-embedding-3-large` (품질)
   - BGE, Voyage 등
5. **Indexing Method**:
   - High Quality (임베딩 + 키워드)
   - Economy (키워드만)

## 🔍 Retrieval 설정

**Studio → KB → Settings → Retrieval Settings**:

- **Search method**: Vector / Full-text / Hybrid
- **Top K**: 5-10
- **Score threshold**: 0.5
- **Rerank**: Cohere Rerank 활성화 (정확도 ↑)

## 🔄 워크플로우에 통합

```
Start (user_input)
  │
  ▼
Knowledge Retrieval (kb=my-docs, query={{#start.user_input#}})
  │
  ▼
LLM (system: "다음 컨텍스트만 사용해 답하라:
  {{#retrieval.documents#}}"
  user: {{#start.user_input#}})
  │
  ▼
End
```

## 📈 평가

**Studio → Evaluation**:
- Golden 데이터셋 업로드 (질문 + 기대 답변)
- LLM-as-judge로 정확도 자동 채점
- 다른 retrieval 설정 비교

## 🔧 한국어 RAG 팁

- **Embedding**: `text-embedding-3-large` 또는 BGE-M3 (다국어 강함)
- **Chunking**: 한국어는 token이 영어 대비 1.5-2배 → max_tokens 작게
- **Rerank**: Cohere Rerank 3.5 (다국어 지원) 필수에 가까움
- **Prompt**: "한국어로만 답변" 명시

## ⚠️ 흔한 실수

| 증상 | 대응 |
|------|------|
| Retrieval 결과 부정확 | Chunk size 조정. Rerank 켜기 |
| 인덱싱 시간 매우 김 | embedding API rate limit. worker 스케일 |
| 컨텍스트 너무 길어 비용↑ | Top K 줄이기, summary 우선 |
| 같은 문서 중복 결과 | Deduplication 활성화 |
| 한국어 검색 약함 | 다국어 임베딩 모델로 |

## ✅ 체크포인트
- [ ] KB 1개에 10+ 문서 인덱싱
- [ ] Hybrid + Rerank로 검색 품질 비교
- [ ] 워크플로우에서 Retrieval 결과 LLM에 주입
- [ ] Evaluation 데이터셋 정확도 60% 이상

## 🔗 다음 → [04-agents-and-api.md](04-agents-and-api.md)
