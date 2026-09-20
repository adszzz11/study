---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# ByteByteGo Ecosystem

## 비교

| 대안 | 형태 | ByteByteGo 대비 강점/차이 | 적합한 경우 |
| --- | --- | --- | --- |
| ByteByteGo | 책, visual guide, newsletter, 영상, live cohort | 빠른 시각적 개념 정리와 최신 AI 교육을 한 브랜드 안에서 제공 | backend 기초부터 AI system design까지 연결할 때 |
| [Educative Grokking Modern System Design](https://www.educative.io/courses/grokking-the-system-design-interview?aff=BYZE) | 인터랙티브 코스 | company-specific pattern, case study, mock/structured lesson에 집중 | 인터뷰 연습 루틴과 상호작용형 진도가 필요할 때 |
| [DesignGurus Grokking System Design](https://github.com/design-gurus/grokking-system-design) | pattern-based 코스 + 무료 companion | caching, sharding, replication을 재사용 가능한 pattern으로 다룬다 | 문제 사이에 전이 가능한 사고 틀을 만들 때 |
| [System Design Primer](https://github.com/donnemartin/system-design-primer) | 오픈소스 GitHub 자료 | 무료이며 breadth가 넓고 읽을 자료와 면접 문제를 폭넓게 제공 | 예산 없이 reference map을 만들 때 |
| *Designing Data-Intensive Applications* | 기술 서적 | interview 답변보다 data model, storage, replication, stream processing 원리를 깊게 다룬다 | production data system의 근본 원리를 파고들 때 |

## 선택 가이드

- **빠른 지도와 시각화**가 필요하면 ByteByteGo guide를 첫 진입점으로 둔다.
- **반복형 면접 훈련**이 목적이면 인터랙티브 코스 또는 mock interview를 병행한다.
- **원리 검증**이 필요하면 DDIA와 공식 database/queue 문서로 설계 가정을 검증한다.
- **예산 제약**이 있으면 System Design Primer로 주제를 넓게 탐색한 후, 부족한 영역만 유료 자료로 보완한다.

## Sources

- https://blog.bytebytego.com/
- https://www.educative.io/courses/grokking-the-system-design-interview?aff=BYZE
- https://github.com/design-gurus/grokking-system-design
- https://github.com/donnemartin/system-design-primer
