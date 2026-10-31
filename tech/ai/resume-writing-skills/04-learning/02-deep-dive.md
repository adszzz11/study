---
date: 2026-09-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: evidence gate, QA, rendering

> [[../README|목차로 돌아가기]] · [[01-getting-started|이전: Getting Started]]

## 1. Evidence gate를 상태 기계로 만들기

| 상태 | 의미 | 출력 정책 |
|---|---|---|
| `verified` | source와 evidence가 모두 있음 | claim에 사용 가능 |
| `source_only` | 후보자 기록은 있으나 별도 evidence 없음 | 약한 표현 또는 승인 질문 |
| `needs_confirmation` | 기간·수치·역할이 불명확 | draft에 질문으로 남김 |
| `unsupported` | JD에만 있고 후보자 source에 없음 | Resume claim에 사용 금지 |

Achievement bullet은 `Challenge → Action → Result` 또는 `X-Y-Z` 구조를 쓴다. 단, Result의 숫자를 모르면 result를 발명하지 않는다.

```text
[scope/challenge]에서 [action]을 수행하여 [verified result]를 만들었다.
```

## 2. Dual QA

### ATS-friendly 점검

- `Experience`, `Education`, `Skills` 같은 일반 heading과 선형 읽기 순서를 쓴다.
- text가 image·복잡한 table·header/footer에만 있지 않은지 plain-text export로 확인한다.
- JD의 핵심 표현은 evidence가 있는 경우에만 자연스럽게 포함한다.
- 파일명, 확장자, employer의 upload instruction을 따른다.

### Human readability 점검

- 첫 화면에서 role, recent impact, 핵심 기술이 보이는가?
- bullet 하나가 action, scope, outcome을 짧게 전달하는가?
- 같은 buzzword가 반복되거나 JD를 기계적으로 복사하지 않았는가?
- reader가 metric의 비교 기준과 기간을 이해할 수 있는가?

## 3. Privacy와 approval

입력 최소화가 기본이다. 주민번호, 여권·계좌 정보, 상세 주소, 인증 비밀값, 불필요한 가족·건강 정보는 넣지 않는다. candidate source와 tailored output의 저장 위치·공유 권한·LLM provider retention policy를 확인한다.

최종 checklist는 지원자가 직접 승인한다.

```text
[ ] 모든 날짜·직책·회사명이 사실이다.
[ ] 모든 metric에 계산 또는 확인 근거가 있다.
[ ] unsupported claim과 placeholder가 없다.
[ ] 연락처·link·지역 형식이 이 지원에 맞다.
[ ] 제출 파일을 text와 visual rendering으로 모두 확인했다.
```

## 4. RenderCV pipeline

RenderCV는 YAML에서 PDF, Typst, Markdown, HTML, PNG를 생성할 수 있다. content source와 theme/layout을 분리하면 공고별 version을 재현하고 Git diff를 검토하기 쉽다.

```bash
rendercv new "Name"
rendercv render Name_CV.yaml
```

생성 뒤에는 PDF만 열어 보지 말고 PNG page를 확인한다. overflow, 잘린 link, 예상치 못한 page break는 source validation과 별개의 visual defect다.

## Sources

- https://docs.rendercv.com/user_guide/index.html
- https://docs.rendercv.com/user_guide/cli_reference/
- https://github.com/StephanieKoehl/resume-best-practices
