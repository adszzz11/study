---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# 심화 학습: 연결 구조와 효과 검증

## Handoff 계약

아래는 구현 가능한 설계 예시이며 제품의 실제 API나 저장 형식이 아니다.

```yaml
task_id: dossier-001
from_role: researcher
to_role: writer
input_version: v1
artifact: evidence-ledger-v1
claim_ids: [E01, E02]
unknowns:
  - memory sharing scope
completion: claims mapped to evidence or marked unknown
next_action: draft with evidence IDs
```

입력 버전과 근거 ID를 유지하면 오래된 자료를 전달하거나 근거 연결을 잃는 문제를 추적하기 쉽다. 수신자가 자료에 접근할 수 있는지도 확인한다.

## 제어 흐름 설계

```text
공통 목표·원자료 → Researcher → Writer → Reviewer → 사람 승인
                                ↑          |
                                └─ 수정 요청 ┘  (예: 최대 2회)
```

- **Task routing:** 초기에는 사람이 역할과 작업을 배정한다.
- **Review gate:** 표현 문제는 Writer에, 근거 누락은 Researcher에 반환한다.
- **Completion:** 근거 없는 확정 주장 0개와 사람 승인으로 종료한다.
- **예외:** 자료 부족·실행 실패·반복 한도 도달 시 미해결 목록을 반환한다.

병렬 부서 검토로 확장한다면 통합 담당자와 충돌 해결 기준을 먼저 정한다. 중앙 coordinator나 peer-to-peer는 가능한 설계 선택이며 자료에서 확인된 구조가 아니다.

## Role·Model·Memory를 분리한 실험

1. 같은 모델과 원자료를 유지하고 single-agent와 역할 분리를 비교한다.
2. 역할 계약을 고정하고 특정 역할의 모델만 바꾸어 비교한다.
3. 메모리를 도입하면 저장 내용·공유 대상·접근 권한·보존 기간을 명시한다.
4. 입력 버전과 검토 기준을 유지하여 여러 조건을 동시에 바꾸지 않는다.

메모리 설정이 보인다는 이유로 공동 상태를 가정하지 않는다. 지속 실행은 별도 실험으로 중단 후 재개, 중간 보고, 완료 알림을 확인한다.

## 비교 기록

| 지표 | 기록 방법 | 해석 시 주의 |
|---|---|---|
| 근거 없는 주장 수 | 원자료와 최종본 대조 | 같은 판정 기준 사용 |
| 누락 수 | 사전 필수 항목과 대조 | 항목을 결과 확인 전에 고정 |
| 수정 횟수 | 검토 후 재제출 횟수 | 한도 도달 사례도 기록 |
| 사람 검토 시간 | 검토 시작부터 종료까지 | 자동 처리 시간과 구분 |
| 전체 처리 시간 | 요청부터 최종 승인까지 | handoff 대기 포함 |

한 번의 성공으로 일반화하지 않는다. 여러 입력에서 품질 이익과 조정 부담을 비교한다. dossier에는 측정값이 없으며 역할 분리의 우수성을 전제하지 않는다.

## 연결

[[tech/ai/role-based-multi-agent/05-projects|적용 프로젝트]] · [[tech/ai/role-based-multi-agent/03-references|후속 확인]] · [[tech/ai/role-based-multi-agent/README|학습 지도]]

## Sources

- 사용자 제공 dossier 및 그 안의 영상 요약. 원본 제목·제작자·출처 URL은 제공되지 않았다.
- 출처 URL: 미제공. 외부 검색이나 URL 열기는 수행하지 않았으며, 동명 제품의 사이트를 근거로 대체하지 않았다.
