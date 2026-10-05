---
date: 2026-10-05
tags: [tech]
type: tech-tool-study
status: draft
---

# fast-jev-compaction Cheatsheet

## 핵심 용어

| 용어 | 요약 |
|---|---|
| extractive pruning | 새 summary를 쓰지 않고 기존 transcript 항목을 선별한다. |
| `tool_use_id` pairing | call과 result를 함께 유지·축소·삭제하는 기준이다. |
| keep | call + result를 verbatim으로 남긴다. |
| truncate | call + result 앞부분 + 안내문을 남긴다. |
| drop | call과 result를 함께 제거한다. |
| pinned context | 첫 메시지와 최근 `preserveRecentMessages`를 보호한다. |

## 운영 전 체크리스트

- [ ] 정확한 프로젝트 명칭은 `fast-jev-compaction`으로 확인했는가?
- [ ] transcript를 외부 TypeSafe endpoint에 보내도 되는가?
- [ ] secret/private source/개인정보를 redaction했는가?
- [ ] raw transcript와 native fallback 경로를 보존했는가?
- [ ] reduction 외에 rerun, success rate, latency, cost를 측정하는가?
- [ ] Claude Code version `2.1.274+` 및 early-access function hooks 조건을 확인했는가?

## 기본값 메모

```text
preserveRecentMessages = 6
maxStateTokens        = 25,000
request upper bound   = 30,000 estimated tokens
```

> 값과 지원 조건은 upstream README에서 적용 직전에 재확인한다. 이 도구는 실험적 community project이며, fallback은 optional convenience가 아니라 안전 장치다.

## 빠른 의사결정

```text
민감 transcript인가? ─ yes → endpoint 정책/ redaction 불가면 사용하지 않음
                  └ no  → path/error 보존이 중요한가?
                                ├ yes → synthetic fixture로 benchmark
                                └ no  → native compaction 또는 fresh context 우선
```

## Links

- [[README|Overview 및 학습 경로]]
- [[04-learning/02-deep-dive|Deep dive]]
- [Upstream README](https://github.com/tamaratran/fast-jev-compaction/blob/main/README.md)
