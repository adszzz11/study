---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Scion Projects

아래는 학습용 제안이다. 제공 사례의 재현이나 성능 입증 결과가 아니다.

## Project 1: 두 Agent의 근거 검토

- **과제:** 작은 공개 repository의 기능 1개를 Researcher가 조사하고 Reviewer가 근거와 결론을 대조한다.
- **구성:** 두 agent, shared directory, 서로 다른 보고 파일. 하나의 파일을 동시에 편집하지 않는다.
- **산출물:** 출처 목록, 조사 보고서, 검토 보고서, 사람이 수정한 최종 결론.
- **완료:** 핵심 주장마다 근거가 있고 reviewer의 반론이 해결되거나 미해결로 명시된다.
- **관찰:** 잘못된 주장, 중복 조사, 도움 요청, 사람의 검토 시간을 기록한다.

## Project 2: Worktree 기반 구현과 Review

- **과제:** 작은 수정 하나를 Implementer가 수행하고 Reviewer가 검증한다.
- **구성:** 작업별 Git worktree, 통합 담당 1명, 파일·branch 소유권 명시.
- **산출물:** 변경 diff, 필요한 테스트 결과, review 의견, 통합 기록.
- **완료:** 요구 동작과 필요한 검증을 충족하고 통합 담당자가 결과를 확인한다.
- **관찰:** 충돌, 재작업, 동기화 비용을 남긴다. 자동 merge를 전제하지 않는다.

## Project 3: Instructions 개선 실험

- **과제:** 동일한 작업에서 역할·도움 요청·완료 기준을 명시하기 전후를 비교한다.
- **구성:** Harness·model·과제 조건을 가능한 한 고정하고 instructions만 바꾼다.
- **산출물:** 두 버전의 instructions, 실행 기록, 사람 평가, 다음 실험 제안.
- **완료:** 무엇이 바뀌었는지와 효과를 구분하고 표본이 작다는 한계를 적는다.

## 공통 평가표

| 항목 | 기록 방법 |
|---|---|
| 결과 품질 | 같은 rubric으로 정확성·완료 범위 평가 |
| 전체 시간 | 준비·실행·검토·통합 시간을 모두 기록 |
| 사용 비용 | 확인 가능한 usage·청구 자료 기록; 미확인은 미확인 표시 |
| 조정 비용 | 메시지·중복 작업·충돌·재작업 기록 |
| 사람 개입 | 개입 횟수·이유·소요 시간 |
| 재현 조건 | Version·harness·model·runtime·instructions 버전 |

먼저 단일 harness baseline을 남긴다. 소수 실행만으로 일반적 생산성·비용 우위를 주장하지 않는다.

## Navigation

- [[tech/ai/scion-agent-orchestration-02101198/README|Scion 학습 진입점]]

## Sources

- https://github.com/GoogleCloudPlatform/scion — README 및 제공된 dossier의 프로젝트 설명.
