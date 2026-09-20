---
date: 2026-08-17
tags: [tech]
type: tech-tool-study
status: draft
---

# CodeBurn — Ecosystem

> [[01-overview|이전: Overview]] · [[README|목차로 돌아가기]] · [[03-references|다음: References]]

## 비교 표

| 도구 | 데이터/범위 | Interface | 강점 | 주요 trade-off |
|---|---|---|---|---|
| **CodeBurn** | 다수 AI IDE/CLI의 local logs | TUI, CLI, Web, Desktop, Menubar, GNOME, MCP | cross-tool 분석, task/one-shot/optimize/yield, local-first | provider schema와 heuristic 정확도에 의존 |
| **ccusage** | Claude, Codex, OpenCode, Amp, Copilot CLI, Gemini 등 local data | CLI, JSON, blocks/statusline | 성숙한 reporting, offline pricing cache, automation 친화적 | CodeBurn식 rich desktop UI와 Yield/Optimize가 중심은 아님 |
| **Tokscale** | 여러 coding agent의 local data와 일부 API/export | CLI, visualization dashboard, public profile/leaderboard | 시각화와 usage sharing, 폭넓은 source | public/social 기능을 쓸 때 privacy 경계를 별도 판단해야 함 |
| **AgentTrace** | 여러 coding agent session history와 generic JSON/JSONL | Rust TUI, CLI/report | cost뿐 아니라 latency, failure, slow-run diagnosis | CodeBurn의 delivery/optimization taxonomy와 관점이 다름 |
| **Provider dashboard** | 해당 provider의 billing/usage | Web console | invoice에 가장 가까운 공식 총액과 quota | cross-tool project/task/retry 맥락이 약함 |
| **직접 script/BI** | 원하는 log와 billing export | SQL, notebook, dashboard | 조직 정의에 맞춘 정확한 schema와 metric | parser 유지보수, pricing update, 보안 설계를 직접 책임짐 |

## 선택 기준

### CodeBurn을 우선할 때

- 여러 coding agent의 local logs를 설치 직후 자동 탐색하고 싶다.
- 비용뿐 아니라 task mix, retry, context, MCP usage, Git delivery proxy가 필요하다.
- terminal dashboard와 desktop/menubar를 같은 aggregation 결과로 보고 싶다.
- agent가 MCP를 통해 자신의 usage와 savings 후보를 조회하게 하고 싶다.

### ccusage를 우선할 때

- daily/weekly/monthly/session report와 JSON automation이 핵심이다.
- CLI와 statusline 중심의 작고 예측 가능한 workflow를 선호한다.
- pre-cached pricing을 쓰는 명시적 offline mode가 중요하다.

### Tokscale을 고려할 때

- contribution graph나 공개 profile처럼 usage를 시각적으로 공유하는 것이 목표다.
- local-only 분석을 넘어 opt-in social/leaderboard 경험이 필요하다.

### Provider dashboard를 함께 봐야 할 때

- 결제, quota, tax, credit, discount의 공식 값을 확인해야 한다.
- CodeBurn 추정치와 invoice가 다를 때 reconciliation 기준이 필요하다.

## 상호 보완 전략

```text
Provider dashboard ── 공식 청구·quota 기준
        │
        ├── CodeBurn ── cross-tool 원인 분석·optimization·delivery proxy
        │
        └── ccusage/직접 script ── 반복 report·검증용 second opinion
```

1. provider dashboard로 월 총액과 subscription 조건을 확정한다.
2. CodeBurn으로 model/project/task별 비용 원인을 좁힌다.
3. 중요한 수치는 ccusage 또는 원본 log sample로 교차 검증한다.
4. heuristic 지표는 팀 평가가 아니라 workflow 개선 가설로 사용한다.

## Sources

- https://github.com/getagentseal/codeburn
- https://codeburn.app/docs/compare
- https://github.com/ccusage/ccusage
- https://github.com/junhoyeo/tokscale
- https://github.com/luoyuctl/agenttrace

