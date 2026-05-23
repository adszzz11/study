# 4-2. Environment & Messaging

## 📡 Pub/Sub 모델

```python
from metagpt.environment import Environment
from metagpt.team import Team

env = Environment(desc="소프트웨어 회사")
team = Team(env=env)

team.hire([
    ProductManager(),
    Architect(),
    ProjectManager(),
    Engineer(),
    QA(),
])

team.invest(investment=3.0)   # USD 한도
team.run_project("할 일 관리 웹앱")
await team.run(n_round=10)
```

## 📨 Message 객체

```python
from metagpt.schema import Message

msg = Message(
    content="설계 완료. 다음 단계 진행 가능.",
    role="Architect",
    cause_by=WriteDesign,
    sent_from="Architect",
    send_to=["ProjectManager"],
)
env.publish_message(msg)
```

## 🎯 Subscribe 패턴

```python
class Engineer(Role):
    def __init__(self):
        super().__init__()
        self._watch([WriteTasks])    # WriteTasks 액션 결과 메시지만 구독
```

→ Engineer는 ProjectManager의 WriteTasks 출력만 깨어남.

## 🌊 흐름 디버깅

```bash
metagpt --debug "..."

# 출력 로그에서 메시지 흐름 추적:
# [PM]→msg→[Architect]→msg→[ProjectManager]→...
```

또는 `env.history`로 모든 메시지 조회.

## 💰 비용 통제

```python
team.invest(investment=2.0)   # $2 한도. 초과 시 자동 중단
```

## ✅ 체크포인트
- [ ] Team + 5 Roles 셋업
- [ ] invest 한도 초과 시 자동 중단
- [ ] env.history로 메시지 시퀀스 분석
- [ ] custom Role 추가 + _watch로 흐름 통합

## 🔗 다음 → [03-data-interpreter.md](03-data-interpreter.md)
