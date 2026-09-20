---
date: 2026-07-17
tags: [tech]
type: tech-tool-study
status: draft
---

# Build Your Own X — Ecosystem

> [[01-overview|이전: Overview]] | [[README|목차로 돌아가기]] | [[03-references|다음: References]]

## 포지션

`Build Your Own X`의 강점은 자유도와 탐색 폭이다. 반대로 학습 순서, 실행 환경, feedback을 사용자가 직접 설계해야 한다. 대안은 “무엇을 만들 것인가”뿐 아니라 “어떤 feedback loop가 필요한가”로 고른다.

## 비교

| 프로젝트 | 구성 방식 | Feedback / Test | 범위 | 적합한 경우 | 주요 한계 |
|---|---|---|---|---|---|
| [Build Your Own X](https://github.com/codecrafters-io/build-your-own-x) | 기술별 외부 tutorial index | 공통 제공 없음 | 매우 넓고 systems 중심 | 원하는 내부 기술을 자유롭게 파고들 때 | roadmap·grading 부재, link rot |
| [CodeCrafters](https://app.codecrafters.io/concepts/overview) | Git, Redis, Docker 등의 staged challenge | `git push` 기반 automated test, hints, solution examples | 엄선된 infrastructure tool | 명확한 단계와 feedback이 필요할 때 | 일부 유료, 2026년 신규 challenge 개발 일시 중단 |
| [Coding Challenges](https://codingchallenges.fyi/) | language-agnostic specification | challenge별 test script와 설명 | `wc`, JSON parser, Redis 등 실용 CLI | 약 8시간의 작은 deliberate practice | 대규모 system의 깊이는 비교적 낮음 |
| [Project Based Learning](https://github.com/practical-tutorials/project-based-learning) | programming language별 tutorial index | 공통 제공 없음 | web, app, game까지 폭넓음 | 특정 language로 portfolio app을 만들 때 | framework/API 사용 중심 항목과 품질 편차 |
| [Nand2Tetris](https://www.nand2tetris.org/) | NAND gate부터 compiler·OS까지 고정 curriculum | 공식 simulator와 project materials | computer stack 하나를 종단 학습 | 일관된 bottom-up curriculum이 필요할 때 | 선택 폭이 좁고 장기 과정 |
| [Teach Yourself CS](https://teachyourselfcs.com/) | book·university course 기반 curriculum | 과정마다 다름 | CS theory와 systems fundamentals | 장기적인 이론 기반을 체계화할 때 | 즉시 완성되는 project 경험은 적음 |

## 빠른 선택 기준

| 우선순위 | 선택 |
|---|---|
| 자유도와 탐색 폭 | `Build Your Own X` |
| automated feedback | `CodeCrafters` |
| 짧고 명확한 specification | `Coding Challenges` |
| application portfolio | `Project Based Learning` |
| 완결된 bottom-up curriculum | `Nand2Tetris` |
| 이론적 빈틈 보완 | `Teach Yourself CS` |

## 조합 전략

가장 균형 잡힌 흐름은 theory, guided implementation, verification을 분리하는 것이다.

```text
Teach Yourself CS에서 개념 읽기
  → Build Your Own X에서 구현 guide 선택
  → milestone별 자체 black-box test 작성
  → reference implementation과 behavior 비교
  → benchmark와 failure diary 추가
```

### 예시: key-value database

1. OS와 database chapter로 file I/O, indexing, durability 개념을 읽는다.
2. `Build Your Own X`에서 익숙한 language의 database tutorial을 선택한다.
3. `put/get/delete`, restart persistence, malformed input을 test한다.
4. throughput과 latency를 재되 production database와 숫자 경쟁을 목표로 삼지 않는다.
5. 빠진 기능인 crash recovery, concurrent write, compaction을 문서화한다.

## 주의할 비교 오류

- GitHub list의 star 수와 curriculum 품질을 같은 지표로 보지 않는다.
- tutorial 완주와 production-grade system 구현을 동일시하지 않는다.
- CodeCrafters platform의 운영 공지를 GitHub list의 종료로 해석하지 않는다.
- automated test 통과를 architecture 이해의 충분조건으로 보지 않는다.

## Sources

- [Build Your Own X](https://github.com/codecrafters-io/build-your-own-x)
- [CodeCrafters Concepts Overview](https://app.codecrafters.io/concepts/overview)
- [CodeCrafters: Pausing New Challenges](https://codecrafters.io/blog/pausing-new-challenges)
- [Coding Challenges](https://codingchallenges.fyi/)
- [Project Based Learning](https://github.com/practical-tutorials/project-based-learning)
- [Nand2Tetris](https://www.nand2tetris.org/)
- [Teach Yourself CS](https://teachyourselfcs.com/)

