---
date: 2026-10-15
tags: [tech]
type: tech-tool-study
status: draft
---

# REA — Ecosystem

[[tech/devtools/rea/README|학습 진입점]] · 이전: [[tech/devtools/rea/01-overview|Overview]] · 다음: [[tech/devtools/rea/03-references|References]]

REA는 모든 분석 엔진을 대체하기보다 agent workflow와 evidence model을 제공하는 orchestration 계층이다. 깊은 native 분석은 provider의 능력에 의존한다.

| 도구 | 주 역할 | REA와의 관계/차이 | 적합한 경우 |
|---|---|---|---|
| REA | agent-oriented orchestration, CLI/MCP, Evidence | 여러 tool과 target을 agent workflow와 증거 모델로 통합 | 조사 결과를 자체 구현·테스트로 연결할 때 |
| Ghidra | open-source SRE framework | REA의 native provider가 될 수 있음; 자체적으로도 강력한 framework | 깊은 binary 분석, script/extension 개발 |
| IDA Pro | 상용 disassembler/decompiler/debugger | REA의 선택 provider; GUI 중심 workflow도 독립적으로 완결 | 고급 상용 reverse engineering workflow |
| Hopper | macOS/Linux 중심 disassembler/decompiler | REA가 native provider로 연동 가능 | Apple 환경에서 빠른 native 조사 |
| JADX | Android DEX/APK → Java decompiler | Android 전용; REA APK workflow의 기반 도구 중 하나 | APK static analysis에 집중할 때 |
| mitmproxy / Chrome DevTools | HTTP·browser runtime 관찰 | REA가 website/HAR 조사를 agent workflow로 결합 | web traffic·UI 행태를 직접 관찰할 때 |

## 선택 기준

1. **조사 대상부터 분류한다.** Electron/JavaScript라면 실행 없는 static inspection부터, native binary라면 provider 지원과 license부터 확인한다.
2. **산출물을 정한다.** 수동으로 function 하나를 읽는다면 Ghidra·IDA·Hopper GUI가 빠를 수 있다. 여러 결과를 agent와 공유하고 implementation proof로 남긴다면 REA가 맞는다.
3. **runtime 필요성을 최소화한다.** HAR·browser capture는 static evidence로 답할 수 없는 질문에만 사용한다.
4. **provider 결과를 교차 검증한다.** decompiler pseudocode는 source가 아니며, call reference·string·실행 관찰과 함께 해석한다.

## Provider와 target의 관계

JavaScript 및 .NET static inspection은 native analysis engine 없이 가능한 범위가 있다. native 심층 분석은 Ghidra, Hopper, IDA 같은 provider를 붙인다. APK/device 작업은 JADX와 adb 같은 Android 도구에 의존할 수 있다. 즉 REA 설치만으로 모든 target에 동일한 깊이의 결과가 나오는 것은 아니다.

## Sources

- [REA provider evaluation](https://github.com/morluto/rea/blob/main/docs/provider-evaluation.md)
- [Ghidra repository](https://github.com/NationalSecurityAgency/ghidra)
- [IDA 제품 정보](https://hex-rays.com/ida-free)
- [Hopper download](https://www.hopperapp.com/download)
- [JADX repository](https://github.com/skylot/jadx)
