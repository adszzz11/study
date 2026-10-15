---
date: 2026-10-15
tags: [tech]
type: tech-tool-study
status: draft
---

# REA — References

[[tech/devtools/rea/README|학습 진입점]] · 이전: [[tech/devtools/rea/02-ecosystem|Ecosystem]]

## REA 공식 자료

| 자료 | 확인할 내용 |
|---|---|
| [Get Started](https://rea.tools/get-started/) | 지원 client, setup 흐름, 첫 조사 |
| [GitHub repository / README](https://github.com/morluto/rea) | target 범위, 설치·명령의 현재 상태 |
| [npm: rea-agents](https://www.npmjs.com/package/rea-agents) | 배포 버전과 package metadata |
| [MCP contracts](https://github.com/morluto/rea/blob/main/docs/mcp-contracts.md) | `structuredContent.normalized_result`, `evidence_id` 계약 |
| [Roadmap](https://github.com/morluto/rea/blob/main/docs/roadmap.md) | 예정 기능과 안정성 판단 지점 |
| [Provider evaluation](https://github.com/morluto/rea/blob/main/docs/provider-evaluation.md) | provider별 capability와 비교 기준 |
| [Evidence/provenance 이슈](https://github.com/morluto/rea/issues/21) | evidence bundle·provenance 설계 배경 |

## 인접 도구

- [Ghidra](https://github.com/NationalSecurityAgency/ghidra) — disassembly, decompilation, graphing, scripting을 제공하는 open-source SRE framework
- [Hex-Rays / IDA](https://hex-rays.com/) — 상용 disassembler·decompiler 제품군
- [Hopper](https://www.hopperapp.com/download) — macOS/Linux용 disassembler·decompiler
- [JADX](https://github.com/skylot/jadx) — DEX/APK를 Java source 형태로 decompile하는 Android 특화 도구

## 읽는 순서

1. Get Started에서 현재 설치·client 연결 방법을 확인한다.
2. README에서 원하는 target과 host/provider 조건을 확인한다.
3. MCP contracts를 읽고 agent가 받은 결과에서 evidence와 limitation을 찾는다.
4. provider evaluation으로 필요한 native/APK/web capability를 대조한다.
5. Roadmap은 계획이지 보장된 기능 목록이 아니므로 실제 release·문서와 함께 판단한다.

## Sources

- [REA GitHub repository](https://github.com/morluto/rea)
- [REA Roadmap](https://github.com/morluto/rea/blob/main/docs/roadmap.md)
- [REA MCP contracts](https://github.com/morluto/rea/blob/main/docs/mcp-contracts.md)
