# Part 2. LangGraph 생태계

## 🆚 vs 경쟁자

| 항목 | LangGraph | CrewAI | AutoGen | Temporal/Prefect |
|------|-----------|--------|---------|-----------------|
| **추상화** | Node/Edge/State | Agent/Task/Crew | Conversation | Workflow/Activity |
| **체크포인트** | ⭐ Native | Flows에 일부 | ✗ | ⭐ Native |
| **HITL** | ⭐ interrupt | 약 | 가능 | ⭐ signal |
| **LLM 지향** | ✅ | ✅ | ✅ | ✗ (범용 워크플로우) |
| **러닝 커브** | 높음 | 낮음 | 중 | 높음 |

LangGraph는 사실 "LLM에 특화된 미니 Temporal" 같은 위상.

## 🔄 마이그레이션 흐름

```
PoC: CrewAI ─► 프로덕션: LangGraph ─► 운영: Paperclip 직원
                           │
                           └─► A2A로 Google ADK 호출
```

## 🆚 1:1 비교

### vs CrewAI
- **CrewAI**: "역할을 설명하면 알아서 협업"
- **LangGraph**: "흐름을 명시하고 통제"
- 시작은 CrewAI, 운영은 LangGraph 흔함

### vs AutoGen
- **AutoGen**: 대화형 — 에이전트들이 채팅으로 합의
- **LangGraph**: 명시적 그래프 — 누가 언제 호출될지 통제
- AutoGen은 maintenance, LangGraph가 흡수 중

### vs Temporal (워크플로우 엔진)
- Temporal은 LLM 비전제. LangGraph는 LLM·tool calling 1급.
- 매우 큰 규모면 Temporal 위에 LangGraph 얹는 패턴도

## 🌐 함께 쓰는 스택
| 역할 | 도구 |
|------|------|
| 트레이싱 | LangSmith |
| 체크포인터 | PostgresSaver, SqliteSaver, RedisSaver |
| 메모리 | LangMem, Mem0 |
| Deploy | LangGraph Platform, FastAPI 래핑 |
| 운영 레이어 | **Paperclip**, Temporal |
| Studio | LangGraph Studio (시각화·디버깅) |

## 🔥 동향
- LangGraph가 CrewAI ★ 추월 (2026 Q1)
- **LangGraph Platform** 출시 — 매니지드 호스팅 + Cron + HITL UI
- **LangGraph Studio**: 데스크탑 IDE로 그래프 시각화
- **A2A 프로토콜** 1급 지원 → Google ADK와 cross-call 가능
- Pydantic v2 기반 state 표준화

## 🔗 다음 → [03-references.md](03-references.md)
