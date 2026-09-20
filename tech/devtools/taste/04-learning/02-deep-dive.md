---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# taste — Deep Dive

> [[01-getting-started|이전: Getting started]] | [[../README|목차로 돌아가기]] | [[../05-projects|다음: Projects]]

## 1. Progressive disclosure

Agent는 모든 reference를 처음부터 context에 넣지 않는다.

```text
name + description
        ↓ relevant?
     SKILL.md
        ↓ route
DOMAINS.md or REVIEW.md
        ↓
actual repository artifacts
```

이 구조는 activation 비용을 작게 유지하고, 현재 작업에 필요한 procedural knowledge만 불러온다. `taste` 자체의 reference를 읽는 것만으로 grounding이 끝나는 것은 아니다. 반드시 대상 repository의 인접 artifact까지 열어야 한다.

## 2. Create pipeline

| 단계 | 핵심 질문 | 실패 신호 |
|---|---|---|
| Ground | job, reader, exemplar는 무엇인가? | 일반론과 model memory로 시작 |
| Shape | 목적에 맞는 artifact 형태는 무엇인가? | 습관적인 deck/page 구조 |
| Rank | 결과에 가장 큰 영향을 주는 결정은? | 모든 항목이 같은 무게 |
| Source | 구체 정보가 실제 근거에 있는가? | 가짜 가격·정책·feature |
| Recommend | 기본 선택과 reversal condition은? | 무난한 옵션만 여러 개 |
| Stop | polish가 독자에게 보이는가? | stakes보다 과도한 완성도 |

## 3. Domain routing

| Domain | 먼저 보는 것 | Grounding 대상 | Generated tell |
|---|---|---|---|
| Code | naming, error style, call-site, failure | 수정 파일, 인접 파일, test, dependency | 불필요한 class/config/logger, framework만 검사하는 test |
| UI | visual hierarchy, audience, primary action | component, token, content, 동종 page | 3-card template, 가짜 logo/testimonial, 의미 없는 gradient |
| Documents | 첫 문장의 결론과 actionability | 최근 동종 문서, source data/thread/code | 관습적 intro, 가짜 균형, 반복 결론 |
| Data/charts | 전달할 단일 비교 | data range, gap, outlier, 독자 관행 | 불필요한 series, dual axis, 변수명뿐인 title |
| Systems | constraint, failure, migration | config, deploy, incident, on-call 기록 | 근거 없는 queue/cache/service, 비현실적 scale |

## 4. Critique pipeline

긴 checklist나 임의 점수보다 verdict를 먼저 제시한다.

```text
Verdict
  → Invention: source 없이 만든 것
  → Cut: 제거할 것
  → Miss: 목적에 비해 빠진 결정
  → Tell: practitioner가 알아볼 generated 흔적
  → Fix: 가장 작은 수정
```

### 예시

```text
Verdict: 배포 결정에 필요한 근거보다 일반 architecture 설명이 앞선다.
Invention: 확인되지 않은 10x traffic 가정.
Cut: queue와 cache를 소개하는 두 문단.
Miss: rollback owner와 data migration failure path.
Tell: 모든 component를 동일한 크기의 box로 표현.
Fix: 실제 deploy config를 기준으로 current/target/rollback 3단 구조로 다시 작성.
```

여러 안을 비교하거나 사용자가 score를 요구할 때만 명시적 rubric을 추가한다. score는 verdict를 대체하지 않는다.

## 5. 실패 경로

| 위험 | 완화 |
|---|---|
| 나쁜 exemplar를 충실히 복제 | exemplar 선택 이유와 품질을 먼저 검토 |
| source 부족으로 지나치게 보수적 | `[confirm: …]`와 reversal condition 사용 |
| Skill이 자동 호출되지 않음 | client discovery와 activation metadata 확인, 명시 호출 |
| judgment를 QA로 오해 | test, lint, a11y, security review 별도 실행 |
| update로 instruction 변경 | commit pin 후 diff review |
| 효과가 주관적으로만 보임 | blind comparison과 task-specific outcome 측정 |

## Sources

- [SKILL.md](https://raw.githubusercontent.com/Hmbown/taste/main/SKILL.md)
- [DOMAINS.md](https://raw.githubusercontent.com/Hmbown/taste/main/references/DOMAINS.md)
- [REVIEW.md](https://raw.githubusercontent.com/Hmbown/taste/main/references/REVIEW.md)
- [Agent Skills GitHub](https://github.com/agentskills/agentskills)

