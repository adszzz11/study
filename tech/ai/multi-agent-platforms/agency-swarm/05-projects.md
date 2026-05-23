# Part 5. Agency Swarm 실전 프로젝트

## 🟢 P1. 텔레그램 비서 Agency (★)

```
User ⇄ CEO ⇄ Mail / Calendar / Research
```

- CEO만 텔레그램 응대
- 3명의 직원이 도메인 작업
- 폴더 구조로 모듈화

## 🟡 P2. Genesis Agency — 메타 에이전시 (★★★)

VRSEN가 공개한 패턴. **에이전시가 다른 에이전시를 자동으로 만든다**.

```
Genesis Agency
   └─► "마케팅 회사 만들어" 명령
         └─► CEO/Designer/Copywriter 폴더 자동 생성
               └─► instructions.md 자동 채워짐
                     └─► 새 Agency 실행 가능
```

학습 가치 매우 큼 — 메타 추상화 이해.

## 🟡 P3. PR 리뷰 Agency (★★)

```
User ⇄ CEO ⇄ {Security Reviewer, Style Reviewer, Logic Reviewer} ⇄ Aggregator
```

3명이 같은 PR을 다른 관점에서 보고 Aggregator가 통합.

## 🔴 P4. Paperclip + Agency Swarm 통합 (★★★★)

Agency를 Python wrapper로 감싸 Paperclip 직원 1명으로 등록. 큰 회사 안에 작은 회사.

```python
# adapter.py
while True:
    task = paperclip.heartbeat("agency-research")
    if task:
        result = agency.get_completion(task["input"])
        paperclip.report(task["id"], result)
```

## Best Practices
- 폴더 구조 일관성 (lint 가능하게)
- instructions.md는 명확한 페르소나 + 출력 형식
- 도구는 항상 Pydantic
- temperature 0.3 권장 (안정성)
- thread 영속화로 다음 실행 시 컨텍스트 유지
- LiteLLM 통해 비OpenAI 모델 활용
