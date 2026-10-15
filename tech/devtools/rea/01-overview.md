---
date: 2026-10-15
tags: [tech]
type: tech-tool-study
status: draft
---

# REA — Overview

[[tech/devtools/rea/README|학습 진입점]] · 다음: [[tech/devtools/rea/02-ecosystem|Ecosystem]]

## What

REA(Reverse Engineer Anything)는 coding agent를 위한 local-first reverse-engineering toolchain이다. CLI와 MCP Server가 조사 interface를 제공하고, target에 맞는 provider가 static analysis 또는 runtime capture를 수행한다. 결과는 자연어 결론만이 아니라 artifact identity, source location, raw/normalized result, evidence, limitation으로 연결하는 것을 목표로 한다.

```text
Coding Agent → MCP → REA MCP Server / CLI
                         ├─ Static: JS/.NET/APK artifact
                         ├─ Runtime: browser/process capture, HAR
                         └─ Provider: Hopper/Ghidra/IDA, JADX, adb
                                   ↓
                  normalized result + Evidence ID + limitations
```

## Why

소스 없는 application의 기능을 이해하려면 보통 disassembler, decompiler, debugger, browser DevTools, traffic capture를 번갈아 사용한다. 각 결과의 형식·근거·한계가 분리되면 agent가 빈틈을 추측으로 채우기 쉽다.

REA의 가치는 조사 결과를 다음 coding step에 전달 가능한 계약으로 만드는 데 있다. agent는 evidence를 근거로 추가 질문을 하고, 허가된 범위에서 구현 가설과 테스트를 만들 수 있다. 이는 결론의 정확성을 보장하지 않는다. 관찰된 사실, 그로부터의 추론, 아직 모르는 부분을 계속 구분해야 한다.

## 핵심 특징

| 특징 | 의미 | 주의점 |
|---|---|---|
| CLI와 MCP | 같은 investigation workflow를 terminal과 MCP client에서 사용 | client별 setup·connection 방식은 다를 수 있음 |
| 다중 target | JS/Electron, .NET, APK, native, web/HAR 등 | target마다 provider와 host 요건이 다름 |
| Provider abstraction | Ghidra·IDA·Hopper·JADX·adb 등의 분석 기능을 연결 | provider 설치·license·출력 품질은 별도 관리 |
| Evidence-first | `normalized_result`, `evidence_id`로 결과와 근거를 연결 | evidence가 있어도 inference는 검증 필요 |
| Local-first | artifact 분석은 대상이 있는 host에서 실행 | AI provider에 전달되는 tool result의 정책은 별도 확인 |
| Snapshot 방향 | artifact·parameter·provider 조건을 보존·비교 | 재현성은 동일 입력과 환경 기록이 전제 |

## 분석 경계와 안전

Static inspection은 보통 파일을 읽지만, browser/process capture는 대상 실행·로그인·network request·UI interaction을 수반할 수 있다. 따라서 다음을 최소 기준으로 둔다.

- 소유하거나 명시적으로 승인받은 target만 분석한다.
- 테스트 계정·분리된 device/network를 쓰고 production credential이나 개인정보를 넣지 않는다.
- malware, third-party production app, DRM·license 보호 대상은 법적·보안 승인과 격리 절차 없이는 다루지 않는다.
- evidence에는 비밀값·개인정보가 남을 수 있으므로 저장·공유 범위를 검토한다.

## 학습 체크

- [ ] REA와 개별 decompiler/provider의 역할 차이를 설명할 수 있다.
- [ ] `observed`, `inferred`, `unknown`을 구분하여 조사 결과를 쓸 수 있다.
- [ ] static inspection과 runtime capture의 위험 차이를 설명할 수 있다.

## Sources

- [REA README](https://github.com/morluto/rea)
- [MCP contracts](https://github.com/morluto/rea/blob/main/docs/mcp-contracts.md)
- [Evidence/provenance 설계 이슈](https://github.com/morluto/rea/issues/21)
