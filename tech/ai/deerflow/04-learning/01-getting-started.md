---
date: 2026-10-11
tags: [tech]
type: tech-tool-study
status: draft
---

# DeerFlow — 시작하기

> [[../README|목차로 돌아가기]] | [[02-deep-dive|다음: 심화]]

## Goal

repository 기반으로 최소 toolset과 명시적인 sandbox policy를 구성한 뒤, `deep-research` skill의 조사→검색→종합→report artifact 흐름을 관찰한다. 아래 명령은 version에 따라 달라질 수 있으므로 실행 전 repository README와 App Quick Start를 확인한다.

## Prerequisites

- Python 3.12+, Node.js 22+, `uv`, `pnpm`, nginx
- 사용할 LLM provider의 API key를 환경 변수 또는 secret manager로 주입할 수 있는 환경
- 검색·fetch provider와 sandbox provider의 사용 정책 확인
- 실험용 directory와 비용 상한, network/file write 허용 범위

## 1. Repository와 설정 준비

```bash
git clone https://github.com/bytedance/deer-flow.git
cd deer-flow
make setup
```

`make setup` 뒤에는 기본값을 신뢰하지 말고 LLM provider, web search, sandbox, write/bash policy를 명시한다. `config.example.yaml`를 출발점으로 다음 질문에 답한다.

| 설정 영역 | 최소 실험의 권장 선택 |
|---|---|
| model | 비용 상한이 있는 개발용 모델 1개 |
| search/fetch | DuckDuckGo search + Jina fetch 등 1개씩 |
| filesystem | 실험용 workspace만 허용 |
| bash | 필요할 때만 허용, destructive command 차단 |
| sandbox | 신뢰된 개인 개발은 LocalSandbox, 그 외는 AIO/E2B 평가 |

## 2. 최소 조사 task 실행

1. `deep-research` skill을 enable한다.
2. 공개 source만 쓰는 좁은 질문을 준다. 예: “최근 공식 release note를 근거 링크와 함께 5개 항목으로 요약해줘.”
3. planning, search, fetch, synthesis, report artifact 생성 로그를 분리해 관찰한다.
4. report의 각 주장에 source URL이 있고, 인용이 source 내용을 실제로 지지하는지 표본 검토한다.

## 3. Artifact와 file I/O 실습

CSV 하나를 올리고 `data-analysis` skill로 chart artifact 생성을 요청한다. 입력 파일, 생성 파일, 실행 command, 실패 로그가 어느 workspace에 남는지 확인한다. production data나 secret은 이 단계에 넣지 않는다.

## Checklist

- [ ] 공식 README와 현재 quick start의 version 요구사항을 확인했다.
- [ ] 모델 key를 repository·prompt·로그에 기록하지 않았다.
- [ ] search, fetch, filesystem, bash를 필요한 최소 집합으로 제한했다.
- [ ] 생성 artifact와 command가 sandbox workspace 밖을 건드리지 않는지 확인했다.
- [ ] citation과 source fidelity를 사람이 검토했다.

## Sources

- https://github.com/bytedance/deer-flow
- https://deerflow.tech/en/docs/application/quick-start
- https://deerflow.tech/en/docs/harness/tools
- https://deerflow.tech/en/docs/harness/sandbox
