# Part 2. CrewAI 생태계

## 🆚 vs 주요 경쟁자

| 항목 | CrewAI | LangGraph | AutoGen | Agency Swarm | Paperclip |
|------|--------|-----------|---------|--------------|-----------|
| **첫 코드까지** | 5분 | 30분+ | 15분 | 10분 | (코딩 아님) |
| **추상화 수준** | 높음 (role/task) | 낮음 (node/edge) | 중간 (conversation) | 높음 (CEO/agent) | (운영 OS) |
| **상태 관리** | 약 (Flows 보강) | ⭐ 강함 | 약 | 대화 단위 | DB 큐 |
| **체크포인트** | ✗ (Flows에 일부) | ⭐ Native | ✗ | ✗ | DB persistent |
| **HITL** | 약 | ⭐ Interrupt | 가능 | 가능 | 승인 워크플로우 |
| **러닝 커브** | ⭐ 최저 | 높음 | 중 | 낮음 | 낮음 |
| **프로덕션 준비** | Flows 추가 시 | ⭐ 표준 | maintenance | OK | 운영 OS |

## 🔄 흔한 마이그레이션 경로

```
CrewAI (프로토타입) ─► CrewAI Flows ─► LangGraph (프로덕션)
                                          │
                                          └─► Paperclip 직원으로 등록 (운영)
```

## 🆚 CrewAI vs LangGraph (가장 흔한 결정)

| 결정 기준 | CrewAI 선택 | LangGraph 선택 |
|----------|------------|----------------|
| 첫 PoC | ✅ | |
| 워크플로우가 명확하고 선형 | ✅ | |
| 복잡한 분기·루프·상태 | | ✅ |
| 체크포인트 + HITL 필수 | | ✅ |
| 비기술 PM이 흐름 이해할 수 있어야 | ✅ | |
| 엔터프라이즈 + 감사로그 | (AMP) | ✅ |
| LangChain 자산 재사용 | | ✅ |

## 🌐 함께 쓰는 스택

| 역할 | 추천 |
|------|------|
| LLM 라우팅 | LiteLLM, OpenRouter |
| 메모리 | CrewAI 내장 + Mem0, Letta |
| RAG | LlamaIndex, Chroma |
| Observability | CrewAI AMP, LangSmith, Helicone |
| Deploy | CrewAI Cloud, FastAPI 래핑, AWS Lambda |
| 운영 레이어 | **Paperclip** (직원으로 CrewAI 크루 등록) |

## 🔥 최신 동향

- **CrewAI Flows GA** (2025): 이벤트 드리븐 + 상태 머신. LangGraph 대비 강점
- **AMP Suite**: 트레이싱·콘트롤플레인·24/7 서포트 (유료)
- **CrewAI Studio**: 비주얼 빌더 (β)
- **MCP 지원**: 도구 인터페이스 표준화
- **LangGraph 추격**: LangGraph가 ★ 추월 — CrewAI도 프로덕션 강화 가속화

## 🔗 다음 → [03-references.md](03-references.md)
