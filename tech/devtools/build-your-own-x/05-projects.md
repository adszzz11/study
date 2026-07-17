---
date: 2026-07-17
tags: [tech]
type: tech-tool-study
status: draft
---

# Build Your Own X — Projects

> [[04-learning/02-deep-dive|이전: Deep Dive]] | [[README|목차로 돌아가기]] | [[cheatsheet|다음: Cheatsheet]]

## 공통 완료 기준

모든 project는 기능 구현뿐 아니라 evidence를 남긴다.

- [ ] 원본 tutorial URL, 확인일, version, license 기록
- [ ] 구현 범위와 제외 범위 명시
- [ ] architecture/component diagram 작성
- [ ] happy path, boundary, malformed input test 작성
- [ ] 최소 한 가지 failure mode 재현
- [ ] benchmark 또는 behavior comparison 수행
- [ ] “production에 쓰면 안 되는 이유” 정리

## Project 1: JSON Parser

**난이도**: Beginner · **권장 시간**: 1~2일

### 목표

tokenizer와 recursive descent parser를 구현해 string, number, array, object를 AST/value로 변환한다.

```text
source text → tokens → parser → value / syntax error
```

### 확장 과제

- escape와 Unicode 처리
- error offset과 line/column 표시
- malformed input fuzz test
- 표준 library parser와 differential test

## Project 2: Mini Git Object Store

**난이도**: Intermediate · **권장 시간**: 3~5일

### 목표

blob/tree/commit의 serialization과 content-addressed storage를 구현한다.

```text
content → header + body → hash → compressed object
tree + parent + metadata → commit graph
```

### 완료 기준

- 동일 content가 동일 object ID를 만드는지 검증
- 저장한 object를 다시 읽어 원문 복원
- 실제 Git이 읽을 수 있는 subset인지 범위 명시
- hash collision, corrupt object, atomic ref update가 빠졌음을 분석

## Project 3: Persistent Key-Value Database

**난이도**: Intermediate · **권장 시간**: 1~2주

### 목표

append-only log와 in-memory index를 사용해 `put/get/delete`를 구현한다.

| Milestone | 관찰할 개념 |
|---|---|
| Record encoding | framing, checksum, version |
| Append/write | sequential I/O, partial write |
| Startup scan | recovery, corruption handling |
| Index | memory/disk trade-off |
| Compaction | write amplification, stale record |

### 실험

- record size별 throughput과 p95 latency
- process 종료 후 persistence
- file tail을 잘랐을 때 recovery behavior
- compaction 전후 file size와 pause time

## Project 4: HTTP/1.1 Server

**난이도**: Intermediate · **권장 시간**: 1주

### 목표

socket accept, request parser, routing, response serialization을 연결한다.

```text
TCP socket → request framing → parser → handler → response bytes
```

### 필수 test

- partial read와 여러 packet으로 나뉜 header
- malformed request line
- `Content-Length` mismatch
- slow client와 timeout
- concurrent connection과 resource limit

TLS, proxy trust, request smuggling defense, observability가 없는 구현은 public network에 배포하지 않는다.

## Project 5: Bytecode Interpreter

**난이도**: Advanced · **권장 시간**: 2~4주

### 목표

작은 language를 lexer → parser → AST/compiler → bytecode VM pipeline으로 구현한다.

| 단계 | 산출물 |
|---|---|
| Lexer | token stream과 invalid token error |
| Parser | AST와 source location |
| Compiler | constants, instructions, jump patching |
| VM | stack, call frame, control flow |
| Runtime | value representation과 runtime error |

### 심화 과제

- AST interpreter와 bytecode VM benchmark 비교
- closure 또는 garbage collection 중 하나 추가
- bytecode verifier나 instruction disassembler 작성
- syntax/runtime error의 source location 개선

## Project 선택 matrix

| 배우고 싶은 것 | 추천 project |
|---|---|
| parsing과 error design | JSON Parser |
| hashing, DAG, object model | Mini Git |
| disk layout와 recovery | Key-Value Database |
| socket, protocol, concurrency | HTTP Server |
| compiler pipeline과 runtime | Bytecode Interpreter |

## Sources

- [Build Your Own X tutorials](https://github.com/codecrafters-io/build-your-own-x#tutorials)
- [Coding Challenges](https://codingchallenges.fyi/)
- [Nand2Tetris](https://www.nand2tetris.org/)

