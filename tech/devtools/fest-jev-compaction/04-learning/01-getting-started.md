---
date: 2026-10-05
tags: [tech]
type: tech-tool-study
status: draft
---

# Getting started

## 목표

live API를 연결하기 전에 unit test와 synthetic transcript에서 `keep`, `truncate`, `drop` 그리고 pair integrity가 어떻게 보이는지 확인한다.

## 준비

- upstream의 README, `tests`, TypeScript entry point를 읽는다.
- 실제 private session 대신 path와 error를 익명화한 fixture를 만든다.
- 원본 fixture를 보존해 compaction 결과와 항상 diff할 수 있게 한다.

## 최소 실습

```text
1. source read → result("src/auth.ts ...")
2. test run    → result("FAIL: auth rejects expired token ...")
3. rg search   → result("수백 줄의 이전 매치")
```

1. 각 call/result pair에 대해 **현재 task가 call을 알아야 하는가?**를 적는다.
2. 필요하다면 **result 원문이 필요한가?**를 따로 적는다.
3. 1·2는 `keep`, 1만은 `truncate`, 둘 다 아니면 `drop`이라는 가설을 세운다.
4. 결과에 result만 남거나 call만 사라지는 dangling record가 없는지 확인한다.

## 첫 비교 실험

한 fixture에서 옵션을 한 번에 하나만 바꾼다.

| 변경 | 관찰할 것 |
|---|---|
| `preserveRecentMessages` | 최신 evidence가 pinned 영역에 남는가 |
| `keepThreshold` | 보존량과 놓친 evidence가 어떻게 달라지는가 |
| `truncateHeadChars` | 앞부분만으로 error/path를 복구할 수 있는가 |

## 안전 기준

- API key와 live transcript를 fixture에 넣지 않는다.
- 민감 output은 redaction한 뒤에도 재식별 위험을 검토한다.
- reduction 비율만으로 성공을 판정하지 않는다. [[02-deep-dive#측정|측정 지표]]를 함께 기록한다.
