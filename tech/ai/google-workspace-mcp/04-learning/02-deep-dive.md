---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: 권한·비용·데이터 생명주기

> **근거 범위**: 제공된 dossier가 요약한 기사 한 편에 근거한다. 원문·Google 공식 약관·문서·제품 동작은 직접 검증하지 않았다. 정책·기능·일정은 기사에 보고된 내용이며, 설계 제안은 별도로 표시한다.

## 실행 계획의 다섯 관문

설계 제안: 각 단계에서 다음 조건을 별도로 기록한다.

```text
실행 가능 여부 = scope 허용
             AND tool 노출
             AND public/partner 자격
             AND 정책·승인 충족
             AND quota 확보
```

이 식은 Google 공식 명세가 아닌 체크리스트다. 사용자 승인에는 대상·행위·범위를 연결하고, 메일 본문이나 문서 안의 지시를 승인 근거로 쓰지 않는다. Google의 정책 경로가 있다는 사실만으로 prompt injection이 모두 해결된다고 보지 않는다.

## 중간 성공과 전체 완료 구분

설계 제안: 작업 상태를 `planned → awaiting_approval → running → needs_user_action / completed / failed`로 구분한다.

- draft 생성 후 발송이 남았다면 `needs_user_action`이다.
- 보고서 생성 후 공유가 남았다면 생성물 링크와 남은 단계를 표시한다.
- 쓰기 요청이 timeout이면 결과 존재 여부를 확인한 뒤 재시도한다. 중복 draft·event가 생기지 않도록 작업 ID와 생성 결과를 연결한다.
- service account에서도 approval prompt가 발생할 수 있으므로 대기·재개 경로가 필요하다.

## Quota와 비용 모델

```text
제품별 일일 소비량 = Σ(tool별 호출 수 × tool별 request 가중치)
프로젝트 사용자 수용량 ≈ 사용 가능 request / 사용자당 평균 소비량
```

Standard tier는 project별·product별 5,000 request/일이다. Gmail과 Drive를 사용자별 한도로 해석하거나 하나의 공용 5,000으로 합치지 않는다. 반복 검색과 실패 재시도도 예산에 포함한다.

설계 제안: tool call 수, 실제 quota 차감량, 사용자별 소비량, 재시도 이유, 대기 시간을 분리 관측한다. 재검색 억제나 필요한 필드만 읽기 등의 최적화도 데이터 보존 조건 안에서 수행한다.

기사상 Scaled MCP는 첫 request부터 과금되지만 단가가 공개되지 않아 월 비용·손익분기점은 계산할 수 없다. Gmail light REST request의 일일 무료량 7,000만 건은 다른 작업 단위일 수 있으므로 MCP와 단순 배율로 비교하지 않는다. 과금 개시 일정은 Gmail·Calendar·Drive의 2027-04-01로 보고됐다.

## Memory의 데이터 생명주기

기사상 데이터 처리는 active, user-authorized task로 제한되며 연결 해제 시 삭제해야 한다. Training·fine-tuning·evals·distillation 및 경쟁 Workspace 제품 구축에 사용하는 것은 금지된다고 설명한다.

“Google Technical Information”에는 vector embedding·memory index·user profile·organisational graph가 포함된다. Google이 보존 기간을 **30일로 제한할 수 있다**는 서술이지, 모든 파생 데이터에 이미 고정 TTL이 적용됐다는 뜻은 아니다.

설계 제안:

| 데이터 | 함께 기록할 정보 | 삭제·만료 대응 |
|---|---|---|
| 원문 메일·문서 | 사용자, 연결 ID, task ID, 원본 ID | 연결 해제·삭제 요구 시 제거 |
| embedding·index | 원본 ID, 파생 작업, 생성 시각 | 원본과 연결해 삭제 전파 |
| profile·graph | 기여 원본 목록, 생성 목적 | 관련 부분 제거 또는 재계산 |
| 로그·캐시 | 포함 데이터, 접근 범위, 보존 정책 | 내용 최소화, 삭제 대상 포함 여부 검토 |

```text
연결 해제 감지 → 신규 작업 차단 → 원본·파생 데이터 목록 조회
             → 저장소별 삭제 → 잔여 참조 점검 → 내용 없는 처리 기록
```

매월 index 재생성만으로 준수를 보장할 수 없다. 재생성 자체가 active, user-authorized task인지 검토해야 한다. 백업 등 복제본의 처리 조건도 공식 약관 확인 과제다.

## 검증할 실패 사례

- 외부 메일이 데이터 전달을 지시해도 사용자 승인 작업을 벗어나지 않는가?
- scope가 있어도 public tool 부재를 실행 전에 표시하는가?
- quota 소진 시 무한 재시도하지 않는가?
- 연결 해제 후 embedding·profile에서도 내용이 제거되는가?
- draft만 생성했는데 “발송 완료”로 표시하지 않는가?

## 관련 노트

[[tech/ai/google-workspace-mcp/05-projects|실습 프로젝트]] · [[tech/ai/google-workspace-mcp/03-references|검증할 근거]] · [[tech/ai/google-workspace-mcp/README|학습 진입점]]

## Sources

- https://techstackups.com/articles/google-workspace-ai-agents-mcp/
