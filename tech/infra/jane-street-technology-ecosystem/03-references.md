---
date: 2026-11-12
tags: [tech]
type: tech-tool-study
status: draft
---

# References: 공식 자료 읽기 순서

> [[tech/infra/jane-street-technology-ecosystem/README|목차]] · [[tech/infra/jane-street-technology-ecosystem/04-learning/01-getting-started|다음: 시작하기]]

## 권장 순서

1. 회사의 technology/market-making/ML 페이지로 문제와 조직 맥락을 잡는다.
2. GitHub organization에서 package README, release, issue를 따라 공개 stack의 경계를 확인한다.
3. `Base`, `Core`, `Async_kernel`을 읽고 runtime vocabulary를 익힌다.
4. `Incremental`, `Bonsai`로 dataflow와 UI 모델을 본다.
5. `magic-trace`의 system requirements를 확인한 후 profiler를 시도한다.
6. OxCaml은 mode documentation과 compiler status를 함께 읽는다.

## Primary Sources

- [Technology](https://www.janestreet.com/technology/)
- [What We Do / Overview](https://www.janestreet.com/what-we-do/overview/)
- [Machine Learning](https://www.janestreet.com/join-jane-street/machine-learning/)
- [Software Engineer role](https://www.janestreet.com/join-jane-street/position/8594541002/)
- [Jane Street GitHub organization](https://github.com/janestreet)
- [Base](https://github.com/janestreet/base)
- [Core](https://github.com/janestreet/core)
- [Async kernel](https://github.com/janestreet/async_kernel)
- [Incremental](https://github.com/janestreet/incremental)
- [Bonsai](https://github.com/janestreet/bonsai)
- [magic-trace](https://github.com/janestreet/magic-trace)
- [OxCaml mode system](https://oxcaml.org/documentation/modes/intro/)

## 검증 메모

- repository 별 license, supported OCaml version, release date는 실습 직전에 다시 확인한다.
- public code가 internal platform 전체를 의미하지는 않는다.
- hiring page는 기술 방향을 읽는 보조 자료이며 API contract로 취급하지 않는다.

## Sources

- https://github.com/janestreet
- https://www.janestreet.com/technology/
- https://oxcaml.org/documentation/modes/intro/
