---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Instinct AI: Overview

## What

Instinct는 연결한 application과 device의 문맥을 바탕으로 사용자의 요청을 이해하고, 응답 생성에 그치지 않고 third-party service에서 action을 수행할 수 있는 personal assistant다. 공식 설명은 email, messaging, screen, audio, location 등을 연결 대상 예시로 든다.

```text
request (text/call)
  → planning / reasoning
  → connected service 또는 device interaction
  → action
  → result / follow-up
```

위 loop는 공개된 product behavior로부터 정리한 개념 모델이다. 모델명, tool protocol, orchestration runtime의 구현 세부는 공개 자료에서 확인되지 않는다.

## Why

일반 chatbot은 “무엇을 할지” 답할 수 있지만, 예약·구매·후속 연락·일정 조정은 사용자가 앱을 옮겨 다니며 마무리해야 한다. Instinct의 가설은 새 UI를 익히게 하는 대신, 기존의 문자·전화 습관으로 assistant에게 delegation을 맡기면 생활 행정의 마찰을 줄일 수 있다는 것이다.

## Key Characteristics

| 영역 | 특징 | 학습 시 확인할 질문 |
|---|---|---|
| Interaction | text/call이 primary interface | 요청과 승인 의사를 얼마나 명확히 전달했는가? |
| Personal context | 허가 범위에서 email·message·document·voice·location을 사용 | 이 task에 정말 필요한 데이터만 연결했는가? |
| Computer-use orientation | phone/computer를 사람처럼 쓰도록 학습됐다고 소개 | API 없는 서비스에서도 어떤 확인 절차가 필요한가? |
| Google Workspace | Gmail, Calendar, Drive, Docs, Sheets, Slides, Tasks와 metadata 접근 | Workspace data의 사용·삭제 경계를 이해했는가? |
| Data controls | 일반 data는 training에 쓰일 수 있고 opt-out 가능; Vault material은 training 제외 | opt-out이 미래 사용분에만 적용됨을 인지했는가? |

## Risk Boundary

Autonomy는 hallucination이나 모호한 입력을 결제·대외 메시지·계약의 문제로 바꿀 수 있다. Terms는 action이 오류를 낼 수 있고 비가역적일 수 있으며, 사용자가 결과와 권한을 지속적으로 검토할 책임이 있음을 명시한다. 따라서 high-impact action은 `plan → review → explicit approval → execute → verify`로 분리한다.

## Sources

- https://instinct.com/
- https://instinct.com/terms
- https://instinct.com/privacy-policy

