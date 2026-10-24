---
date: 2026-10-24
tags: [tech]
type: tech-tool-study
status: draft
---

# The Pragmatic Engineer — Getting started

[[tech/devtools/the-pragramitic-engineer/README|학습 진입점]] · 다음: [[tech/devtools/the-pragramitic-engineer/04-learning/02-deep-dive|Deep dive]]

## 목표

무료 Archive에서 `AI tooling`, `infra/reliability`, `engineering management` 각 1편씩 고르고, 읽은 내용을 팀 의사결정에 쓸 수 있는 evidence note로 바꾼다. 구독이나 별도 프로젝트는 필요 없다.

## 1. 글 고르기

Archive와 sitemap에서 각 주제별로 하나씩 고른다. 다음 기준을 기록한다.

- 발행일이 너무 오래되지 않았는가?
- 우리 팀의 현재 과제와 연결되는가?
- 사례에 수치, architecture, rollout 같은 확인 가능한 evidence가 있는가?
- 이미 알고 있는 vendor release 또는 내부 경험과 비교할 수 있는가?

## 2. 네 칸 note 만들기

아래 표를 글마다 복사해 채운다.

| 칸 | 질문 | 예시 |
|---|---|---|
| Claim | 글이 주장하는 변화는 무엇인가? | AI agent가 PR 생성량을 높인다. |
| Evidence | 어떤 사례·수치·원문이 뒷받침하는가? | 인터뷰, incident, 공개 release note |
| 적용 조건 | 우리 조직에서도 성립하려면 무엇이 필요한가? | test suite 신뢰도, reviewer capacity, rollback 권한 |
| 측정 지표 | 효과·위험을 무엇으로 볼 것인가? | review throughput, test pass rate, incident rate, rollback time |

## 3. 15분 synthesis

세 글을 다 읽은 뒤 다음 문장으로 정리한다.

```text
우리 팀에 영향이 큰 변화: <한 문장>
근거: <글/원문과 핵심 evidence>
확인할 가정: <우리 조직의 차이>
다음 작은 실험: <담당자·기간·metric>
```

## 완료 기준

- [ ] 세 분야에서 글을 하나씩 선정했다.
- [ ] 각 글에 claim/evidence/적용 조건/측정 지표를 작성했다.
- [ ] 원문이 필요한 숫자와 제품 사실을 별도로 확인했다.
- [ ] 하나 이상의 작은 검증 실험을 정의했다.

## Sources

- [Archive](https://newsletter.pragmaticengineer.com/archive?sort=new)
- [2025 Sitemap](https://newsletter.pragmaticengineer.com/sitemap/2025)
- [2026 Sitemap](https://newsletter.pragmaticengineer.com/sitemap/2026)
- [2025 Survey](https://newsletter.pragmaticengineer.com/p/the-pragmatic-engineer-2025-survey)
