---
date: 2026-10-15
tags: [tech]
type: tech-tool-study
status: draft
---

# REA — Getting Started

[[tech/devtools/rea/README|학습 진입점]] · 다음: [[tech/devtools/rea/04-learning/02-deep-dive|Deep dive]]

## 목표

권한 있는 JavaScript/Electron artifact를 **실행하지 않고** 조사해 module, import, IPC 단서와 evidence를 읽는 흐름을 익힌다. 첫 실습 target에는 공개 sample 또는 본인이 만든 build artifact를 사용한다.

## 1. 사전 점검

- Node.js `22.19+`, `24.11+` 또는 `26+`와 npm을 준비한다.
- 분석할 absolute path와 artifact의 소유·승인 범위를 확인한다.
- credential, 개인정보, production session이 들어 있는 profile·cache를 target으로 선택하지 않는다.
- npm 버전과 지원 조건은 실행 직전 [package page](https://www.npmjs.com/package/rea-agents)에서 재확인한다.

```sh
node --version
npm --version
```

## 2. Agent 연결 계획 확인

먼저 setup이 바꾸려는 connection·instruction을 검토한다. 설정 파일을 변경하는 명령이므로 팀 정책과 diff를 확인한 뒤 적용한다.

```sh
# 지원 agent를 자동 감지하는 setup 계획 확인 후 적용
npx rea-agents@latest setup

# Codex만 대상으로 할 때
npx rea-agents@latest setup --client codex
```

## 3. Static analysis 실행

다음은 JavaScript/Electron application의 static inspection 예시다. `/absolute/path/to/app`은 승인받은 실습 artifact의 실제 절대 경로로 바꾼다.

```sh
npx -y rea-agents@latest analyze-javascript-application \
  /absolute/path/to/app --json
```

출력 원본을 보존하고, artifact path, hash/identity가 있다면 함께 기록한다. `--json` 결과가 커질 수 있으므로 비밀값이 포함되지 않았는지 검토한 후 저장·공유한다.

## 4. Agent에 evidence 기반 질문하기

> 이 app의 search feature가 어떤 module/import/IPC 경로로 구현되는지 설명하라. 각 주장에 evidence를 붙이고, 관찰한 사실(observed), 그로부터의 추론(inferred), 아직 확인하지 못한 부분(unknown)을 분리하라.

좋은 답변은 evidence ID나 location을 인용하고, “renderer에서 호출한다” 같은 결론과 그 결론의 직접 증거를 구별한다. 단일 string match만으로 실행 경로를 확정하지 않는다.

## 완료 기준

- [ ] 실행 없는 artifact 조사 결과를 얻었다.
- [ ] `normalized_result`와 `evidence_id`를 찾았다.
- [ ] feature 하나에 대해 observed / inferred / unknown 메모를 작성했다.
- [ ] 다음 조사 질문을 evidence의 공백에 맞춰 만들었다.

## Sources

- [REA Get Started](https://rea.tools/get-started/)
- [rea-agents npm package](https://www.npmjs.com/package/rea-agents)
- [REA MCP contracts](https://github.com/morluto/rea/blob/main/docs/mcp-contracts.md)
