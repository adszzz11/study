---
date: 2026-10-22
tags: [tech]
type: tech-tool-study
status: draft
---

# Kylon Ecosystem

Kylon은 LLM 자체나 단일 automation engine보다, 조직의 agent 작업을 위한 collaboration·permission·data·operation layer에 가깝다.

| 대안군 | 강점 | Kylon과의 차이 | 적합한 경우 |
| --- | --- | --- | --- |
| ChatGPT Work / Claude | 강한 범용 reasoning, 개인 생산성, 문서 작업 | Kylon은 shared Room, records, workflow, App 운영을 제품 중심에 둔다 | 개인 비서 또는 단일 task 중심 작업 |
| Slack/Teams + AI bot | 기존 커뮤니케이션, 낮은 도입 마찰 | chat plugin보다 agent runtime, memory, permission, App/data layer를 함께 제공하려 한다 | 기존 협업 도구를 중심으로 AI bot만 추가할 때 |
| Manus / Genspark | 개인이 복합 task를 agent에 맡기기 좋다 | solo execution보다 조직 handoff, visibility, approval을 우선한다 | 한 사용자의 research·실행 task |
| Retool / Replit / Lovable | 내부 도구 또는 software 제작에 강하다 | App 생성과 그 주변의 대화·agent·업무 workflow를 결합한다 | 복잡한 개발 lifecycle, 세밀한 코드 제어 |
| n8n / Zapier / Make | 결정론적 automation, 넓은 connector 생태계 | workflow가 reasoning을 포함한 multi-step agent 작업을 지향한다 | 예측 가능하고 엄격한 규칙 기반 automation |

## Selection Questions

다음 질문에 “예”가 많으면 Kylon의 범위와 맞을 수 있다.

- 작업 결과를 개인 tab이 아니라 팀 Room에 남겨야 하는가?
- 한 업무가 SaaS 조회, record 갱신, 메시지 초안, 사람의 승인을 함께 요구하는가?
- 외부 agent의 IDE/terminal 작업도 비개발 팀과 같은 맥락에서 이어가야 하는가?
- App, workflow, permission을 별도 제품 조합 대신 한 workspace에서 운영하고 싶은가?

반대로 outcome이 완전히 규칙화되어 있고 LLM 판단이 필요 없거나, custom code review·CI/CD·database migration이 핵심이라면 전문 iPaaS나 개발 플랫폼이 더 적합하다.

## Integration Boundary

Kylon을 기존 시스템의 대체물이라기보다 orchestration workspace로 볼 수 있다.

```text
Slack / Email / CRM / Drive / GitHub
                │ Connection
                ▼
Kylon: Room + Agent + records + App + Workflow + approval
                │
                ▼
팀의 검토, handoff, 운영 이력
```

외부 시스템을 연결하더라도 각각의 Connection scope와 쓰기 권한을 좁게 두며, 공개 메시지·배포·권한 확대에는 사람의 확인 단계를 유지한다.

## Further Reading

- [[01-overview|Overview]]
- [[04-learning/02-deep-dive|Permission과 운영 심화]]
- [[05-projects|적용 프로젝트]]
