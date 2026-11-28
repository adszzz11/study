---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Scion 심화: 협업 규칙과 운영 경계

## 1. 역할 계약부터 작성하기

Scion은 팀 역할을 templates·instructions로 표현할 수 있다. 다음은 설정 파일 schema가 아니라 실험용 자연어 instructions 예시다. 정책이 자동 강제된다고 가정하지 않는다.

```text
Researcher: 근거를 수집하고 notes/research.md에 URL과 불확실성을 남긴다.
Implementer: 합의된 범위의 코드를 자신의 작업 공간에서 변경한다.
Reviewer: 근거·변경·검증 결과를 대조하고 수정 요청을 남긴다.
Coordinator: 의존성을 확인하고 검토가 끝난 결과의 통합 완료를 선언한다.

공통: 다른 담당자의 파일은 동의 없이 수정하지 않는다.
막힘: 원인, 시도한 일, 필요한 결정을 메시지로 전달한다.
완료: 산출물 위치, 검증 방법, 남은 위험을 보고한다.
```

## 2. Workspace와 통신을 함께 설계하기

Shared directories를 쓰면 파일별 소유자를 정한다. Worktree·clone을 쓰면 결과 전달 방식과 통합 담당을 정한다. Group messaging은 팀 전체의 결정 공유에, direct messaging은 특정 담당자에게 묻는 데 활용할 수 있다. 구체적인 메시지 CLI 문법은 버전별 help를 따른다.

체크할 질문:

- 작업 상태의 기준은 Hub인가, 외부 task tracker인가?
- 발견 사항과 최종 산출물은 어디에 남는가?
- 어떤 막힘을 agent끼리 해결하고 언제 사람에게 알리는가?
- Notification을 받은 사람은 어떤 증거로 승인·수정을 판단하는가?

## 3. 관찰과 회고

Logs·session metrics·system health를 살펴본다. 관찰 가능한 metric의 실제 정의는 배포에서 확인한다. Relics 사례의 메시지·파일 접근 telemetry 재생을 모든 환경의 기본 기능으로 가정하지 않는다.

회고에서는 실패한 산출물뿐 아니라 중복 작업, 불필요한 메시지, 늦은 도움 요청을 기록한다. Instructions 또는 skills를 한 번에 하나씩 바꾸고 같은 과제로 다시 비교한다. Films 사례처럼 사람의 평가도 입력으로 삼되 실제 효과는 직접 측정한다.

## 4. Hosted로 옮길 때

| 경계 | 확인할 질문 |
|---|---|
| Identity·access | Roles, access boundaries, federated identity가 실제 요구에 맞는가? |
| Secrets | Agent별 credentials와 scoped secrets의 범위·회수 절차는 무엇인가? |
| State·storage | Hub state와 workspace의 저장·복구 책임은 누구에게 있는가? |
| HA | Replicated Hub·Postgres·shared storage의 장애 대응을 검증했는가? |
| 확장 | Lifecycle hooks·MCP·A2A·configuration bundles의 버전 호환성을 확인했는가? |

이는 운영 검토 질문이며 Scion의 상세 구현을 확정한 설명이 아니다. 권한 모델, 감사 로그, 보안 격리 수준은 별도 확인이 필요하다.

## 5. 학습 결과물

역할 계약, workspace 선택 이유, 실행 버전, 관찰 로그 요약, 통합 결과, 회고를 한 묶음으로 남긴다. [[tech/ai/scion-agent-orchestration-02101198/05-projects|실험 과제]]에서 단일 agent baseline과 비교한다.

## Navigation

- [[tech/ai/scion-agent-orchestration-02101198/README|Scion 학습 진입점]]

## Sources

- https://github.com/GoogleCloudPlatform/scion — README 및 제공된 dossier의 프로젝트 설명.
