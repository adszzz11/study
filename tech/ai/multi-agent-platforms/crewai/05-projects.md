# Part 5. CrewAI 실전 프로젝트

## 🟢 P1. 콘텐츠 제작 크루 (난이도 ★)

researcher → writer → editor → publisher 4명.

```python
researcher = Agent(role="리서처", ...)
writer = Agent(role="작가", ...)
editor = Agent(role="에디터", ...)
publisher = Agent(role="발행", tools=[NotionTool()])

tasks = [
    Task(description="{topic} 조사", agent=researcher),
    Task(description="조사 결과를 1page 글로", agent=writer),
    Task(description="문법·톤 교정", agent=editor),
    Task(description="Notion 페이지로 발행", agent=publisher),
]

Crew(agents=[...], tasks=tasks, process=Process.sequential).kickoff(
    inputs={"topic": "LangGraph 2026 동향"}
)
```

## 🟢 P2. PR 리뷰 크루 (난이도 ★)

style-checker + security-checker + summarizer.

3명이 같은 PR을 다른 관점에서 보고 결과 통합 → GitHub 코멘트 자동 작성.

## 🟡 P3. 가족 일정 매니저 (난이도 ★★)

Hierarchical process로 매니저가 분배:
- calendar-agent: 일정 확인
- reminder-agent: 메신저 알림
- meal-planner: 식단 제안

## 🟡 P4. Paperclip 직원으로 등록 (난이도 ★★★)

CrewAI 크루를 Python wrapper로 감싸 Paperclip heartbeat 프로토콜 구현 → 직원 1명으로 등록.

```python
# adapter.py
import requests, os
PAPERCLIP = os.getenv("PAPERCLIP_URL")

while True:
    r = requests.get(f"{PAPERCLIP}/heartbeat?agent_id=research-crew")
    if r.json().get("tasks"):
        for task in r.json()["tasks"]:
            result = ContentFlow().kickoff(inputs=task["input"])
            requests.post(f"{PAPERCLIP}/result", json={
                "task_id": task["id"],
                "output": str(result),
                "cost_usd": result.token_usage.total_cost,
            })
    time.sleep(10)
```

→ Paperclip이 비용·승인·감사 다 처리, CrewAI는 실제 일.

## 🔴 P5. 자율 트레이딩 시뮬레이션 (난이도 ★★★★)

⚠️ **시뮬레이션만**. 실제 자금 사용 금지.

market-analyst + risk-assessor + portfolio-manager Hierarchical 크루로 가짜 포트폴리오 운영. 학습용.

## Best Practices

- 첫 PoC는 Sequential 3명 이하
- backstory에 한국어 + 톤 명시
- expected_output에 예시 한 줄
- max_iter, max_rpm 항상 설정
- Flows로 가기 전엔 단순 Crew 충분
- 프로덕션은 AMP 트레이싱 필수
