# Part 2. AutoGen 생태계

## 🆚 vs 경쟁자

| 항목 | AutoGen v0.4 | AG2 (ag2ai) | LangGraph | CrewAI |
|------|--------------|-------------|-----------|--------|
| 활성도 | maintenance | 활발 | 활발 | 활발 |
| 협업 모델 | 대화 (Team) | 대화 (GroupChat) | 그래프 | 역할/Crew |
| 상태 | 약 | 약 | ⭐ 강함 | 약 (Flows 보강) |
| Studio | ✅ | 일부 | LangSmith | AMP |
| 합의/디베이트 | ⭐ | ⭐ | 가능 | 가능 |
| ★ | 58.3k (본가) | 별도 | 32.7k | 52k |

## 🔀 본가 vs ag2 선택

| 결정 | 선택 |
|------|------|
| Microsoft 지원·공식 자산 중요 | microsoft/autogen v0.4 |
| 활발한 패치·새 기능 | ag2ai/ag2 |
| 새 프로젝트 시작 | (사실 LangGraph 권장) |

## 🆚 1:1 비교

### vs LangGraph
- **AutoGen**: 대화 메타포 — 자연어로 협업 정의
- **LangGraph**: 상태 그래프 — 명시적 흐름
- **결정**: 디베이트·합의면 AutoGen, 프로덕션이면 LangGraph

### vs CrewAI
- **AutoGen**: GroupChat 안에서 자유 발화
- **CrewAI**: Task 단위 명확한 위임
- **결정**: 합의 도출 → AutoGen, 워크플로우 → CrewAI

## 🔥 동향
- v0.4가 정식 출시했지만 본가 maintenance 모드 진입
- ag2ai/ag2가 fork 차원에서 활동 — 향후 표준 후보
- **AutoGen Studio**가 노코드 빌더로 입지
- **MagenticOne**: Microsoft의 multi-agent 벤치마크 — AutoGen 위에서 동작
- Semantic Kernel(MS) + AutoGen 통합 작업 진행

## 🌐 함께 쓰는 스택
- LLM: OpenAI / Azure OpenAI 우선, Anthropic·Gemini 지원
- 도구: function calling + LangChain tools 호환
- Deploy: AutoGen Studio export → FastAPI

## 🔗 다음 → [03-references.md](03-references.md)
