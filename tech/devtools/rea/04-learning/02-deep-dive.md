---
date: 2026-10-15
tags: [tech]
type: tech-tool-study
status: draft
---

# REA — Deep Dive

[[tech/devtools/rea/README|학습 진입점]] · 이전: [[tech/devtools/rea/04-learning/01-getting-started|Getting started]]

## Evidence-first 읽기

MCP 응답에서 핵심은 `structuredContent.normalized_result`와 `evidence_id`다. 결과를 읽을 때마다 다음 질문을 적용한다.

| 구분 | 기록할 것 | 예시 |
|---|---|---|
| Observed | 도구가 직접 읽거나 캡처한 사실과 위치 | preload module에 특정 IPC channel string이 존재 |
| Inferred | observed facts를 잇는 해석과 confidence | renderer가 그 channel을 사용할 가능성이 높음 |
| Unknown | evidence만으로 확정할 수 없는 부분 | native handler가 실제로 어떤 validation을 하는지 미확인 |
| Limitation | provider·환경·capture가 놓친 범위 | minified bundle, 동적 import, 실행하지 않은 code path |

각 claim에 artifact identity, command/parameter, provider version, evidence ID를 연결하면 나중에 같은 조건에서 비교하기 쉽다. snapshot은 동일 artifact와 parameter·provider 조건이 전제일 때만 의미 있는 비교 자료가 된다.

## Provider를 붙이는 순서

1. static inspection으로 filename, import, string, manifest, metadata처럼 저위험 단서를 모은다.
2. 질문이 native function/call reference/pseudocode를 요구할 때만 Ghidra, Hopper, IDA 같은 provider 조건을 확인한다.
3. provider 출력은 decompiler의 근사 표현으로 읽고, xref·call graph·runtime observation으로 교차 검증한다.
4. APK는 Manifest·resource·class/method reference에서 시작하고 필요할 때 device/adb workflow로 확장한다.

## Runtime capture의 승인 경계

browser/process capture는 파일 분석과 다르다. app을 실행하거나 UI를 누르고 request를 발생시키며 account·network·device 상태를 바꿀 수 있다. 실행 전에는 다음을 확인한다.

- target, 계정, network endpoint가 모두 승인 범위에 있는가?
- disposable test account와 isolated VM/container/device를 사용할 수 있는가?
- 로그·HAR·screenshot에 token, cookie, PII가 남을 때 보관·redaction 방법이 있는가?
- 종료 조건과 예상치 못한 data write에 대한 rollback 계획이 있는가?

## 재구현으로 넘어갈 때

REA 결과는 clean-room compatible implementation의 출발점일 수 있지만, 원본 source의 복원이나 무단 복제를 뜻하지 않는다. 공개 specification과 허가된 관찰을 우선하고, 구현 담당자가 원본을 보지 않는 절차가 필요하다면 조직의 legal/security 기준을 따른다. 구현 후에는 evidence에서 도출한 observable behavior를 test case로 옮겨 원본과 새 구현을 비교한다.

## Sources

- [REA MCP contracts](https://github.com/morluto/rea/blob/main/docs/mcp-contracts.md)
- [REA provider evaluation](https://github.com/morluto/rea/blob/main/docs/provider-evaluation.md)
- [Evidence/provenance 설계 이슈](https://github.com/morluto/rea/issues/21)
