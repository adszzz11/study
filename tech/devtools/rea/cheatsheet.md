---
date: 2026-10-15
tags: [tech]
type: tech-tool-study
status: draft
---

# REA Cheatsheet

[[tech/devtools/rea/README|학습 진입점]]

## 안전한 기본 순서

1. 승인 범위와 target path를 확인한다.
2. 실행 없는 static inspection을 먼저 한다.
3. `normalized_result`, `evidence_id`, limitation을 읽는다.
4. observed / inferred / unknown을 분리해 다음 질문을 만든다.
5. runtime capture는 test account·격리 환경·명시적 승인 뒤에만 한다.

## 환경 및 setup

```sh
# 지원 Node.js 범위: 22.19+, 24.11+, 또는 26+
node --version
npm --version

# agent 연결 설정 (변경 전 계획과 diff 검토)
npx rea-agents@latest setup
npx rea-agents@latest setup --client codex
```

## JavaScript / Electron static inspection

```sh
npx -y rea-agents@latest analyze-javascript-application \
  /absolute/path/to/authorized-app --json
```

| 확인 항목 | 기억할 점 |
|---|---|
| `structuredContent.normalized_result` | agent가 해석할 정규화된 결과 |
| `evidence_id` | claim을 뒷받침하는 evidence 연결자 |
| artifact identity | 어느 build/file을 조사했는지 식별 |
| source location | module, function, offset, path 등 근거 위치 |
| limitation/confidence | 결과가 놓친 범위와 확실성 |

## Agent 질문 템플릿

```text
이 artifact의 <feature>가 어떤 module/import/IPC 또는 request 경로로
구현되는지 설명하라. 각 주장을 evidence ID와 위치에 연결하고,
observed / inferred / unknown 및 limitation을 분리하라.
```

## 빠른 판단

| 필요 | 첫 선택 |
|---|---|
| JS/Electron 기능 단서 | REA static inspection |
| native call graph·pseudocode | REA + Ghidra/Hopper/IDA provider |
| APK class·resource 조사 | REA APK workflow + JADX |
| web request/UI 행태 | 승인된 환경에서 REA website/HAR workflow 또는 DevTools |
| 수동으로 한 function을 깊게 분석 | Ghidra·IDA·Hopper GUI부터 고려 |

## 절대 건너뛰지 않을 것

- 권한 없는 software, production credential, malware를 실습 target으로 쓰지 않는다.
- decompiler output과 string match를 source code·확정된 실행 경로로 취급하지 않는다.
- HAR·log·evidence bundle을 공유하기 전 token, cookie, PII를 검토한다.

## Sources

- [REA Get Started](https://rea.tools/get-started/)
- [rea-agents npm package](https://www.npmjs.com/package/rea-agents)
- [REA MCP contracts](https://github.com/morluto/rea/blob/main/docs/mcp-contracts.md)
