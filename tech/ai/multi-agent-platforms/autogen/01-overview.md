# Part 1. AutoGen / AG2 개요

## 📌 분기를 먼저 이해

```
2024.10 — AutoGen 0.2 (Microsoft Research)
                │
       ┌────────┴─────────┐
       ▼                  ▼
microsoft/autogen      ag2ai/ag2
   (v0.4 재설계)         (v0.2 직계 계승)
   이벤트 드리븐         "Open AutoGen"
   AssistantAgent       ConversableAgent
   maintenance 모드     활발히 개발
```

**현재 (2026 Q2)**:
- 본가 `microsoft/autogen`은 README가 maintenance 표기 — 새 프로젝트 시작엔 신중
- `ag2ai/ag2`는 v0.2 API 유지하면서 적극 개발

## 🧩 핵심 추상화

### v0.2 / AG2 — ConversableAgent
- 모든 에이전트의 기반 클래스
- 메시지 송수신·function calling·human input 통합

### v0.4 — AssistantAgent + Teams
- 더 작은 단위
- Team(GroupChat 후속)이 에이전트 묶음
- async-first

## 🎭 핵심 패턴

### 1. Two-Agent Chat
```python
user_proxy.initiate_chat(assistant, message="피보나치 코드 작성")
```

### 2. GroupChat
```
        GroupChatManager (selector)
       /         |          \
  coder       reviewer      critic
```
- Manager가 다음 발화자 결정
- 모든 에이전트가 같은 대화 공유
- 합의 도출에 적합

### 3. Sequential Chat
명시적 순서 (CrewAI sequential과 유사)

### 4. Nested Chat
한 에이전트 내부에서 별도 채팅 시작

## ⚖️ 장단점

### ✅ 장점
- 대화형 합의·debate 패턴이 자연스러움
- AutoGen Studio로 노코드 빌더
- Microsoft Research 자산 (오래된 논문·벤치마크)
- Function calling 1급
- Human input 통합 쉬움

### ❌ 단점
- **GroupChat 비용 폭주 위험**: 4-agent × 5 round = 최소 20 LLM 호출
- 본가 maintenance 모드 — 새 프로젝트는 ag2 또는 LangGraph
- 상태/체크포인트 약함
- 두 버전 분기로 학습 자료 혼란
- API 변경 잦았음

## 🎯 적합도

| 상황 | 적합 |
|------|------|
| 디베이트·합의 도출 | ⭐⭐⭐⭐⭐ |
| 코드 자동 생성 (coder+reviewer) | ⭐⭐⭐⭐ |
| Microsoft 생태계 연동 | ⭐⭐⭐⭐ |
| 프로덕션 + 장기 운영 | ⭐⭐ (LangGraph 추천) |
| 실시간 응답 | ⭐⭐ (대화 라운드 비용) |

## 🔗 다음 → [02-ecosystem.md](02-ecosystem.md)
