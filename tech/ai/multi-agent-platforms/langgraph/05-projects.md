# Part 5. LangGraph 실전 프로젝트

## 🟢 P1. 승인 게이트가 있는 이메일 봇 (★)

받은 메일 분류 → 답장 초안 → **사용자 승인** → 발송.

핵심: `interrupt()` 한 번이면 끝. 사용자 응답을 기다리는 동안 다른 thread 계속 동작.

## 🟢 P2. 시간여행 가능한 PR 리뷰 (★★)

리뷰 단계마다 체크포인트 → 사용자가 "마음에 안 듦"하면 이전 단계로 되돌려 재실행. CrewAI로는 어려운 패턴.

## 🟡 P3. Supervisor + 4명 도메인 직원 (★★★)

- supervisor: LLM이 누구에게 할당
- researcher / coder / writer / publisher 4명
- 각 직원은 prebuilt `create_react_agent`

→ Paperclip 직원으로 등록해 통합 운영

## 🟡 P4. Cron 워크플로우 (★★)

LangGraph Platform Cron으로 매일 07시 morning briefing 그래프 실행.

```python
# 그래프는 평범한 supervisor
# LangGraph Platform에서 cron schedule만 등록
```

## 🔴 P5. Self-correcting RAG (★★★★)

```
retrieve ─► grade ─┬─► good ──► generate
                   │
                   └─► bad ───► rewrite_query ─► retrieve (루프)
```

LangGraph 공식 튜토리얼 [Self-RAG] 참고. 분기·루프·체크포인트의 진수.

## Best Practices

- thread_id로 사용자/세션 격리
- 모든 노드를 idempotent하게
- interrupt 자리에 timeout 설정
- recursion_limit 명시
- LangSmith 항상 켜기 (디버깅 비용 대비 가치 큼)
- 큰 state는 외부 storage 참조로 (체크포인트 비대화 방지)
