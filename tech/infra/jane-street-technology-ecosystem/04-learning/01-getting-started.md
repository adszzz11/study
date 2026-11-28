---
date: 2026-11-12
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: OCaml, Dune, Base, Async

> [[tech/infra/jane-street-technology-ecosystem/README|목차]] · [[tech/infra/jane-street-technology-ecosystem/04-learning/02-deep-dive|다음: Deep Dive]]

## 목표

- algebraic data type와 pattern matching으로 order state를 표현한다.
- `opam`, `dune`, `base`, `core`, `ppx_jane`의 역할을 구분한다.
- `Async.Deferred` workflow를 callback/Promise와 비교한다.

## 1. 환경 준비

공식 OCaml 설치 안내에 따라 `opam` switch를 만들고, 프로젝트별 compiler와 dependency를 격리한다.

```bash
opam switch create js-study 5.2.0
eval "$(opam env --switch=js-study)"
opam install dune base core async ppx_jane utop
dune init proj risk_lab
cd risk_lab
```

버전은 예시다. `Async` 및 Jane Street package의 현재 compatible OCaml/Dune version은 설치 전에 opam metadata와 repository README로 확인한다.

## 2. Type으로 order lifecycle 제한

```ocaml
open! Base

type order =
  | New of { id : int; qty : int }
  | Working of { id : int; remaining : int }
  | Filled of { id : int }
  | Cancelled of { id : int; reason : string }
[@@deriving sexp]

let cancel = function
  | New { id; _ } | Working { id; _ } -> Cancelled { id; reason = "user request" }
  | Filled _ | Cancelled _ as terminal -> terminal
```

이 구현은 terminal state에서 transition을 무시하지만, 더 엄격한 API라면 type을 분리해 `cancel`을 open order에만 적용할 수 있다. 핵심은 가능한 상태와 전이를 code review 이전에 명시하는 것이다.

## 3. `Deferred`의 모양

```ocaml
open! Core
open Async

let read_then_parse path =
  Reader.file_contents path
  >>| fun contents -> String.split_lines contents

let () =
  don't_wait_for (
    read_then_parse "ticks.csv" >>| fun rows ->
    printf "received %d rows\n" (List.length rows));
  never_returns (Scheduler.go ())
```

`>>|`는 완료 뒤 pure transformation을 연결한다. 실제 service에서는 exception handling, timeout, cancellation, bounded concurrency, backpressure를 설계에 포함한다. blocking 작업을 event loop에서 수행하지 않는다.

## 체크리스트

- [ ] ADT와 exhaustive pattern matching으로 상태를 기술했다.
- [ ] `Base`와 OCaml stdlib API 선택이 왜 다른지 기록했다.
- [ ] `dune build`와 `dune exec`로 작은 executable을 실행했다.
- [ ] `Deferred` 체인에서 blocking I/O를 피하는 방법을 조사했다.

## Sources

- https://ocaml.org/install
- https://dune.readthedocs.io/
- https://github.com/janestreet/base
- https://github.com/janestreet/core
- https://github.com/janestreet/async
