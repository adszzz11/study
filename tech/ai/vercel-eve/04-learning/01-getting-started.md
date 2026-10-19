---
date: 2026-10-19
tags: [tech]
type: tech-tool-study
status: draft
---

# Vercel eve — 시작하기

> [[../README|목차로 돌아가기]] | [[02-deep-dive|다음: 심화]]

## Goal

scaffold한 agent에 명확한 policy와 read-only tool 하나를 넣고, local development에서 tool call과 event stream을 확인한다. 실제 CLI와 generated file 구조는 빠르게 변할 수 있으므로 실행 전 repository의 현재 문서를 확인한다.

## Prerequisites

- Node.js 지원 버전과 package manager
- Git에서 관리할 비밀값 정책: key를 source, prompt, eval log에 기록하지 않음
- 읽기 전용으로 제한된 첫 tool과 representative test prompt

## Scaffold

```bash
npx eve@latest init my-agent
cd my-agent
```

먼저 `agent/instructions.md`에 다음을 명시한다.

```md
# 역할
고객 문의를 분류하고 승인된 knowledge source만 요약한다.

# 금지
- 계정·환불을 변경하지 않는다.
- 근거 없는 정보를 확정적으로 말하지 않는다.

# 응답 정책
근거와 불확실성을 분리해 한국어로 답한다.
```

## First Tool Exercise

`agent/tools/`에 knowledge base를 조회하는 **read-only** TypeScript tool을 둔다. tool 입력은 schema로 검증하고, 응답에는 source identifier를 포함한다. local dev에서 다음을 확인한다.

1. prompt가 tool을 필요한 경우에만 선택하는가?
2. event stream에서 tool input·result·최종 응답을 추적할 수 있는가?
3. 잘못된 입력, 빈 결과, timeout이 사용자에게 안전하게 표현되는가?
4. tool output 안의 외부 text가 instruction이 아니라 data로 취급되는가?

## Checklist

- [ ] `instructions.md`에 목표, 금지사항, response policy를 썼다.
- [ ] 첫 tool을 read-only·최소 권한으로 제한했다.
- [ ] secret을 source control과 prompt에서 분리했다.
- [ ] tool call과 event stream을 local에서 확인했다.
- [ ] representative prompt의 기대 결과를 기록했다.

## Sources

- https://github.com/vercel/eve
- https://vercel.com/blog/introducing-eve
