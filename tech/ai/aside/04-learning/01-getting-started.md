---
date: 2026-06-25
tags:
  - tech
  - ai
  - aside
  - getting-started
type: tech-tool-study
parent: "[[../README]]"
---

# Aside - 시작하기

> [[../03-references|이전: 참고자료]] | [[../README|목차로 돌아가기]] | [[02-deep-dive|다음: 심화]]

---

## 1. 설치와 초기 설정

Aside는 문서 기준 macOS 15.0+에서 Aside 자체가 browser로 동작한다.

### 체크리스트

- [ ] macOS 15.0+ 환경 확인
- [ ] Aside 설치
- [ ] 기존 browser data import
- [ ] cookies, bookmarks, passwords import 여부 결정
- [ ] privacy setting 확인
- [ ] 기본 model/provider 설정

```text
Install Aside
  -> import browser data
  -> configure privacy / memory
  -> connect model provider
  -> run first task
```

---

## 2. 첫 task 작성법

첫 task는 "무엇을 할지"보다 "어디에서, 어떤 계정으로, 어디에 저장하고, 무엇은 하지 말아야 하는지"를 명확히 적는 것이 중요하다.

### Prompt template

```text
<사이트/계정>에서 <업무>를 수행해줘.
결과 artifact는 <저장 위치>에 저장해줘.
MFA, 결제, 전송, 삭제, 권한 변경이 필요하면 먼저 물어봐.
하지 말아야 할 action: <금지 목록>.
완료 후 어떤 파일/페이지를 만들었는지 요약해줘.
```

### 예시

```text
Rippling에서 이번 달 paystub PDF를 Downloads에 저장해줘.
MFA가 필요하면 나에게 질문하고, payroll setting은 변경하지 마.
완료 후 저장한 파일명과 위치를 알려줘.
```

```text
우리 support dashboard에서 지난 7일간 high-priority ticket을 확인하고,
요약 CSV를 project folder에 저장해줘.
고객에게 답장하거나 ticket 상태를 바꾸기 전에는 반드시 승인받아.
```

---

## 3. Session mode 선택

| Mode | 처음 쓸 때 추천 작업 | 주의 |
|------|----------------------|------|
| `Read only` | 조사, dashboard 읽기, vendor research | 파일 저장이나 form action은 제한 |
| `Guard` | 파일 다운로드, draft 작성, 제한된 portal 업무 | 기본값으로 두고 approval gate 확인 |
| `Full access` | 신뢰 가능한 local dev/QA 작업 | writable roots와 destructive action을 좁게 설정 |

처음에는 `Read only` 또는 `Guard`로 시작한다. `Full access`는 local app smoke test처럼 대상과 작업 범위가 명확할 때만 사용한다.

---

## 4. Password Manager access policy

Agent-safe Password Manager는 raw password를 agent에 노출하지 않고 웹사이트에 autofill payload로 입력한다.

| Policy | 의미 | 실습 |
|--------|------|------|
| `Always allow` | 조건이 맞으면 자동 입력 허용 | 낮은 위험의 내부 도구에서만 테스트 |
| `While unlocked` | unlock 상태에서만 허용 | Touch ID unlock 흐름 확인 |
| `Never` | agent autofill 금지 | 민감 계정 또는 테스트 전용 |

Payment, post, message, delete, permission change는 approval gate를 두는 습관이 좋다.

---

## 5. 개발자 첫 실습

Aside CLI는 local web app smoke test에 바로 연결할 수 있다.

```bash
aside "Open localhost:3000 and run a smoke test"
```

MCP server와 REPL도 제공한다.

```bash
aside mcp
aside repl
```

REPL에서는 screenshot, download, DOM inspection 같은 deterministic step을 확인하는 용도로 접근한다.

---

## 시작 실습 과제

| 과제 | 목표 |
|------|------|
| 첫 read-only research | vendor pricing page 3개를 열고 citation 포함 요약 |
| Guard mode file task | portal에서 PDF 다운로드 후 지정 folder에 저장 |
| Password policy test | `While unlocked` 흐름과 Touch ID prompt 확인 |
| Local smoke test | `localhost:3000` UI 탐색과 screenshot artifact 확인 |

## 관련 노트

- [[../../codex/04-learning/01-getting-started|Codex getting started]] - CLI agent 첫 task 작성 비교
- [[../../model-context-protocol-mcp/04-learning/01-getting-started|MCP getting started]] - MCP 연결 실습
- [[../../../devtools/qa/what-is-qa|QA]] - smoke test 업무 맥락
