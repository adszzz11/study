---
date: 2026-10-15
tags: [tech]
type: tech-tool-study
status: draft
---

# REA 학습 가이드

> **한 줄 정의**: REA(Reverse Engineer Anything)는 AI coding agent가 MCP/CLI로 로컬 artifact와 runtime을 조사하고, Evidence를 붙여 동작을 재구성하도록 돕는 오픈소스 reverse-engineering toolchain이다.

## Overview

REA는 disassembler, debugger, browser DevTools, network capture처럼 흩어진 분석 단계를 agent-native workflow로 연결한다. agent는 MCP를 통해 조사하고 `normalized_result`, `evidence_id`, limitation을 받아 관찰과 추론을 분리한 설명·구현·테스트로 이어 간다.

- 대상: native binary, JavaScript/Electron, website, .NET assembly, APK/device, firmware, HAR, EVM bytecode, ELF/crash record 등
- 분석 위치: artifact가 있는 local host. REA는 artifact를 hosted analysis service에 올리지 않는다고 설명하지만, tool result를 받는 AI provider의 data policy는 별도로 확인한다.
- 경계: source code를 복구하거나 app을 자동 복제하는 도구가 아니다. runtime capture는 실제 실행·상호작용을 포함할 수 있으므로 권한 있는 software와 격리 환경에서만 쓴다.
- 조사 기준: dossier 기준 2026-10 npm 공개 최신 버전은 `rea-agents 6.4.0`이다. 도입 전 npm과 release를 다시 확인한다.

## Learning Path

- [ ] [[tech/devtools/rea/01-overview|1. Overview]] — What/Why와 Evidence-first 모델 이해하기
- [ ] [[tech/devtools/rea/02-ecosystem|2. Ecosystem]] — REA와 Ghidra·IDA·Hopper·JADX를 구분하기
- [ ] [[tech/devtools/rea/03-references|3. References]] — 공식 계약과 provider 자료 확인하기
- [ ] [[tech/devtools/rea/04-learning/01-getting-started|4. Getting started]] — 실행 없이 JavaScript/Electron artifact 조사하기
- [ ] [[tech/devtools/rea/04-learning/02-deep-dive|5. Deep dive]] — Evidence, provider, runtime safety를 적용하기
- [ ] [[tech/devtools/rea/05-projects|6. Projects]] — 허가된 migration·audit 사례에 적용하기
- [ ] [[tech/devtools/rea/cheatsheet|7. Cheatsheet]] — 명령과 조사 질문을 빠르게 복습하기

## When To Use

- source가 없거나 불완전한 **권한 있는** artifact의 특정 기능·format·IPC·network 행태를 문서화해야 할 때
- 여러 분석 도구의 결과를 coding agent가 인용 가능한 evidence로 묶어 compatible implementation 또는 migration을 준비할 때
- JavaScript/Electron, .NET, APK, web/HAR 등 서로 다른 target을 동일한 조사 흐름으로 다루고 싶을 때

## When Not To Use

- 소유권·라이선스·승인 범위가 불명확한 third-party production app 또는 malware를 즉시 분석하려는 경우
- 단지 source repository를 읽거나 API 문서를 확인하면 되는 경우
- GUI 기반 debugger/decompiler의 장시간 수동 분석, exploit 개발, 침해 대응처럼 REA orchestration보다 전문 도구와 절차가 중심인 경우

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/ripgrep/README|ripgrep]] — artifact 주변 source·문서에서 문자열과 경로를 빠르게 탐색할 때 함께 쓸 수 있다.

## Sources

- [REA 시작 가이드](https://rea.tools/get-started/)
- [REA GitHub repository](https://github.com/morluto/rea)
- [rea-agents npm package](https://www.npmjs.com/package/rea-agents)
- [REA MCP contracts](https://github.com/morluto/rea/blob/main/docs/mcp-contracts.md)
- [REA Roadmap](https://github.com/morluto/rea/blob/main/docs/roadmap.md)
