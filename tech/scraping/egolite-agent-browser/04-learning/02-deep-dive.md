---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# ego(lite) 심화: Space, Snapshot, Runtime

[[tech/scraping/egolite-agent-browser/README|README]] · [[tech/scraping/egolite-agent-browser/04-learning/01-getting-started|시작하기]]

## 실행 구조

```text
ego-browser nodejs
  → CLI Bridge
  → Browser Process
  → on-demand Node Service / Runtime
  → globalThis.ego native binding + CDP
  → Task Space
```

여러 Runtime은 동시 실행할 수 있다. 이는 여러 조사 task를 병렬화하는 데 유용하지만, 동일 account의 mutation은 race condition을 만들 수 있으므로 write task를 직렬화해야 한다.

## Snapshot 사용 규칙

Snapshot은 browser accessibility tree를 압축한 structured text와 임시 ref로 제공한다. 매 action을 별도 model-tool round trip으로 쪼개기보다 Node.js script 안에서 관찰·조작을 묶어 token/tool call 비용을 줄이려는 설계다.

- navigation, submit, tab switch, dynamic rerender 뒤에는 반드시 re-snapshot한다.
- Snapshot에 없는 ref는 클릭하지 않는다.
- iframe·shadow DOM이라도 먼저 Snapshot에 어떤 UI가 노출되는지 확인한다.
- 실패한 action 뒤에는 screenshot 추측보다 새 Snapshot으로 상태를 재확인한다.

## security와 운영 경계

저장 password/cookie/token을 직접 export하지 못하도록 제한한다고 설명되지만, agent는 사용자가 승인한 authenticated page content에는 접근할 수 있다. 따라서 다음을 운영 policy에 포함한다.

- 최소 권한 account와 read-only task로 pilot한다.
- export, submit, publish, delete는 explicit confirmation을 둔다.
- task별 목적, 접근 system, 생성된 artifact를 기록하고 종료 후 tab을 review한다.
- telemetry, privacy, data retention은 도입 전 최신 정책으로 검토한다.

## learnings 활용

반복 사이트에는 `manifest.json`, notes, tools로 구성된 site learning을 둔다. login flow, 안정적인 화면 판별법, 인간 승인 지점, known failure를 기록하면 agent workflow의 재현성을 높일 수 있다. 단, 사이트 UI가 바뀌면 learning을 재검증한다.

## Sources

- https://github.com/citrolabs/ego-lite/wiki/Ego-Browser-CLI-Architecture
- https://www.egolite.app/document/en/docs/space
- https://github.com/citrolabs/ego-lite/blob/main/AGENTS.md
- https://www.egolite.app/privacy

