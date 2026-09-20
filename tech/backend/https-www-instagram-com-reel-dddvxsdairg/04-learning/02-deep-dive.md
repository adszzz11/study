---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# 심화: 기술 Claim 검증

> [[01-getting-started|이전: 시작하기]] | [[../README|목차로 돌아가기]]

## 검증 pipeline

```text
Reel claim
  -> 정확한 문장으로 전사
  -> claim type 분류
  -> official source 탐색
  -> version/date 범위 확인
  -> 최소 재현 또는 반례 확인
  -> supported / qualified / contradicted / unknown 판정
```

## Claim type별 질문

| 유형 | 확인 질문 | 우선 source |
|---|---|---|
| Feature | 실제 지원하는가? 어느 plan/version인가? | official docs, release notes |
| Performance | baseline, dataset, hardware, sample size는? | benchmark methodology |
| Cost | usage unit, free tier, hidden cost는? | official pricing |
| Security | data retention, auth, isolation은? | security/privacy docs |
| Integration | protocol, SDK, runtime 제약은? | API reference, repository |
| Ease of use | demo 조건과 production 조건이 같은가? | getting started, limitations |

## 판정 rubric

| 판정 | 의미 |
|---|---|
| `supported` | official source와 재현 결과가 claim을 지지 |
| `qualified` | 조건이나 제한을 붙이면 성립 |
| `contradicted` | authoritative source 또는 재현 결과와 충돌 |
| `unknown` | 판단할 근거 부족 |

현재 Reel의 모든 기술 claim은 내용 자체를 확보하지 못했으므로 `unknown`이다.

## Verification matrix template

```markdown
| Claim | Reel timestamp | Official evidence | Version/date | Reproduction | Verdict |
|---|---:|---|---|---|---|
| ... | 00:00 | URL | ... | command/result | unknown |
```

## 재현 시 주의점

- demo에서 생략된 environment variable, credential, network condition을 기록한다.
- 최신 version만 시험하고 과거 영상의 claim을 무효화하지 않는다. 영상 당시 version도 확인한다.
- 성능 수치는 동일한 input, region, hardware, concurrency로 비교한다.
- destructive command나 외부 서비스 생성은 별도 승인을 받은 뒤 실행한다.
- secret과 개인 계정 정보는 공개 vault에 기록하지 않는다.

## Sources

- [원본 Instagram Reel](https://www.instagram.com/reel/DddvxSdAIrG/)
- 사용자 제공 dossier

