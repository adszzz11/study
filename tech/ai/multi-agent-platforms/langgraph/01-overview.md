# Part 1. LangGraph 개요

## 📌 핵심 모델

```
StateGraph
   │
   ├─ State (TypedDict/Pydantic) — 노드 간 공유되는 가변 상태
   ├─ Nodes  (함수) — state를 입력 받아 state 업데이트 반환
   └─ Edges (전이) — START → node1 → node2 → … → END
            ├─ add_edge: 무조건 전이
            └─ add_conditional_edges: 함수가 분기 결정
```

영감: Google **Pregel**(BSP 모델) + Apache Beam + NetworkX.

## 🧩 4대 강점

### 1. Durable Execution
실행 도중 죽어도 마지막 체크포인트에서 재개. cron으로 며칠씩 도는 워크플로우도 OK.

### 2. Human-in-the-loop (HITL)
임의 노드에서 `interrupt()` 호출 → 사용자 입력 받을 때까지 stop → resume.

### 3. Memory (Short + Long Term)
- Short: 그래프 state
- Long: `langgraph.checkpoint.postgres.PostgresSaver` 등으로 영속

### 4. LangSmith 통합
모든 노드 호출·LLM 호출·state 변화가 자동 trace.

## 🎯 Multi-Agent 패턴 3종

### Supervisor 패턴
```
       Supervisor
       /   |    \
   agent1 agent2 agent3
```
중앙 supervisor가 다음에 누가 일할지 결정.

### Swarm 패턴 (Handoffs)
```
agent1 ⇄ agent2 ⇄ agent3
```
에이전트끼리 직접 핸드오프.

### Hierarchical 패턴
```
   Team Supervisor
     /         \
  Team A        Team B
   /  \         /  \
  a1  a2       b1  b2
```
팀 단위 supervisor.

## ⚖️ 장단점

### ✅ 장점
- 프로덕션 1순위 — durable execution
- 체크포인트 + HITL이 1급 시민
- LangSmith로 디버깅 강력
- LangChain 생태계 자산 재사용
- A2A 프로토콜과 호환 (Google ADK 연동)

### ❌ 단점
- **학습 곡선 가장 가파름** — 그래프·상태·체크포인터 다 이해해야
- 코드량 많음 (vs CrewAI 20줄)
- LangChain 비종속이지만 사실상 LangChain 생태계와 묶임
- 비주얼 빌더 없음 (Studio는 시각화만)

## 🎯 누가 쓰면 좋은가

| 상황 | 적합도 |
|------|--------|
| 프로덕션 + 장기 실행 | ⭐⭐⭐⭐⭐ |
| 복잡한 분기·루프·조건 | ⭐⭐⭐⭐⭐ |
| HITL 승인 게이트 다수 | ⭐⭐⭐⭐⭐ |
| 첫 PoC | ⭐⭐ (CrewAI가 더 쉬움) |
| 노코드 | ⭐ |

## 🔗 다음 → [02-ecosystem.md](02-ecosystem.md)
