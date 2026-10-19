---
date: 2026-10-19
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Job Search — 시작하기

> [[../README|목차로 돌아가기]] | [[02-deep-dive|다음: 심화]]

## Goal

개인 Resume와 공고를 비교 가능한 data로 바꾸고, keyword와 semantic retrieval의 차이를 작은 평가 세트에서 확인한다. 이 단계에서는 자동 제출을 만들지 않는다.

## 1. Build an Evidence Profile

Resume 원문을 보존한 채 아래처럼 사실을 구조화한다. 각 항목에는 원문 문장 또는 검증 가능한 링크를 붙인다.

```yaml
experience:
  - role: Backend Engineer
    period: "2023-01..2026-10"
    evidence: "Go API와 Kubernetes 배포 운영"
skills: [Go, Kubernetes, PostgreSQL]
achievements:
  - claim: "API latency 개선"
    evidence: "resume bullet 또는 portfolio URL"
preferences:
  location: Seoul
  work_mode: hybrid
  work_authorization: "confirmed status"
```

`work authorization` 같은 민감하거나 중요한 조건은 추정하지 말고 사용자가 확인한 값만 사용한다.

## 2. Create a Job Corpus

1. 허가된 source 또는 수동 저장한 공고 30–50개를 모은다.
2. 각 JD에서 title, company, location, employment type, posted date, apply URL을 기록한다.
3. requirement를 **must-have**와 **nice-to-have**로 나누고 skill taxonomy의 canonical name과 synonym을 만든다.
4. 종료되었거나 중복된 공고를 표시하고 원본 URL과 확인 시점을 보관한다.

## 3. Compare Retrieval Baselines

| 방식 | 입력 | 장점 | 점검할 한계 |
|---|---|---|---|
| BM25 / keyword | skill, title, 지역 필터 | 빠르고 설명하기 쉬움 | synonym·인접 직무를 놓칠 수 있음 |
| embedding vector | profile/JD 의미 표현 | 표현이 다른 유사 경험을 찾음 | filter 위반·그럴듯한 오매칭 가능 |
| hybrid | 두 점수와 hard filter | recall과 precision 균형 | 가중치와 평가 데이터 필요 |

정답으로 간주할 공고 10개를 따로 정하고 `Recall@K`와 수동 정성 평가를 함께 기록한다.

```text
Recall@K = top-K 결과에 포함된 관련 공고 수 / 전체 관련 공고 수
```

## Checklist

- [ ] Resume 원문을 바꾸지 않고 evidence profile을 만들었다.
- [ ] 공고마다 source URL, 확인 시점, must-have/nice-to-have를 기록했다.
- [ ] BM25, vector, hybrid 결과를 같은 query에서 비교했다.
- [ ] 점수와 별개로 location·visa·고용형태를 hard filter로 확인했다.
- [ ] 실제 지원은 공식 사이트에서 공고 상태와 문서를 검토한 뒤 직접 수행한다.

## Sources

- https://www.linkedin.com/help/linkedin/answer/a7120158
- https://www.indeed.com/career-advice/finding-a-job/how-indeed-uses-ai-to-help-job-search
- https://www.indeed.com/help/job-seekers/articles/360028540531-indeed-job-seeker-guidelines?co=US&hl=en
