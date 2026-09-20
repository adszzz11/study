---
date: 2026-07-17
tags: [tech]
type: tech-tool-study
status: draft
---

# Build Your Own X — Getting Started

> [[../03-references|이전: References]] | [[../README|목차로 돌아가기]] | [[02-deep-dive|다음: Deep Dive]]

## 1. 학습 목표를 한 문장으로 정하기

project 이름보다 배우려는 mechanism을 먼저 적는다.

```text
나쁜 목표: Redis를 만든다.
좋은 목표: RESP parser와 in-memory key-value command loop를 구현하고,
          malformed request와 concurrent client의 동작을 test한다.
```

다음 중 하나를 primary axis로 고른다.

- **technology-first**: database internals처럼 원리가 목표이며 익숙한 language 사용
- **language-first**: Rust처럼 language가 목표이며 작은 project 선택
- **portfolio-first**: demo보다 design note, test evidence, limitation을 포함할 수 있는 주제 선택

## 2. Category와 tutorial 후보 찾기

1. [Tutorials](https://github.com/codecrafters-io/build-your-own-x#tutorials)에서 category를 고른다.
2. 같은 주제에서 2~3개 language/guide를 후보로 둔다.
3. [[../03-references|References]]의 검증 checklist를 적용한다.
4. source code를 그대로 따라 치기보다 milestone과 observable behavior를 추출한다.

| 평가축 | 질문 |
|---|---|
| Prerequisite | 내가 모르는 OS, network, language 개념은 무엇인가? |
| Scope | 주말 project인가, 여러 주짜리 series인가? |
| Recency | 현재 compiler와 dependency로 실행되는가? |
| Feedback | test와 expected output이 있는가? |
| Completion | 중단된 series가 아닌가? |
| Explainability | 각 component가 왜 필요한지 설명하는가? |

## 3. 안전한 workspace 준비

index 자체를 설치하는 과정은 없다. 선택한 tutorial마다 별도 repository와 격리된 dependency 환경을 만든다.

```bash
mkdir my-mini-system
cd my-mini-system
git init

# 언어별 version manager 또는 container를 사용해 version을 고정한다.
# tutorial URL, 확인일, runtime version을 README에 기록한다.
```

권장 초기 파일:

```text
my-mini-system/
├── README.md          # 목표, source URL, 실행법
├── docs/design.md     # component와 invariant
├── docs/limits.md     # 의도적으로 제외한 production concern
├── src/
├── tests/
└── benchmarks/
```

## 4. Vertical slice 정의

첫 milestone은 system 전체가 아니라 end-to-end로 관찰 가능한 가장 작은 흐름이어야 한다.

| 주제 | 첫 vertical slice |
|---|---|
| Database | 한 개 record를 encode → file에 write → restart 후 read |
| Git | blob 저장 → hash로 lookup → 원문 복원 |
| Compiler | integer expression tokenize → parse → evaluate |
| HTTP server | socket accept → request line parse → fixed response |
| Container | child process 생성 → 하나의 isolation primitive 관찰 |

## 5. Tutorial 전에 test부터 적기

```text
Given valid input   → expected output
Given empty input   → defined error or empty result
Given malformed input → process가 crash하지 않고 명시적 error
Given restart       → persistent state의 기대 동작
Given concurrent access → documented ordering 또는 rejection
```

공통 grading이 없으므로 이 test가 학습의 feedback loop가 된다. 가능하면 tutorial의 내부 function이 아니라 public interface를 검증한다.

## 6. 첫 학습 session

- [ ] 목표 mechanism 한 문장 작성
- [ ] tutorial URL, author, 확인일, license 기록
- [ ] runtime/compiler version 고정
- [ ] component diagram 작성
- [ ] 첫 vertical slice 선택
- [ ] happy path test 하나 작성
- [ ] invalid input test 하나 작성
- [ ] tutorial 없이 예상 design을 10분간 먼저 적기
- [ ] 구현 후 예상과 달랐던 점 회고

## 막혔을 때

- dependency가 깨졌다면 무작정 최신 version으로 올리기 전에 원래 version을 기록한다.
- guide의 code가 실행되지 않으면 issue, source repository, archived version을 확인한다.
- scope가 커지면 UI, distributed consensus, optimization보다 core mechanism 한 개를 남긴다.
- 설명 없이 code만 제시하는 tutorial이면 다른 guide나 theory 자료를 병행한다.

## Sources

- [Build Your Own X tutorials](https://github.com/codecrafters-io/build-your-own-x#tutorials)
- [Build Your Own X issues](https://github.com/codecrafters-io/build-your-own-x/issues)
- [Submission template](https://github.com/codecrafters-io/build-your-own-x/blob/master/ISSUE_TEMPLATE.md)

